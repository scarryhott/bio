# Copyright 2025 Radical Numerics Inc.
#
# This source code is licensed under the Apache License, Version 2.0, found in the
# LICENSE file in the root directory of this source tree.

"""
RND1 sampling module for masked diffusion generation.

This module implements entropy-based token selection for iterative denoising
in diffusion language models. Supports both greedy and stochastic sampling
with optional prefix/suffix constraints and infilling.

Closure integration (scarryhott/bio): when closure_mode is not "off", each
denoising step may consult the Potential Gate for admission. Baseline RND1
confidence/entropy schedules remain available; scores never authorize closure
identity. Model weights and Apache-2.0 copyright remain Radical Numerics Inc.
"""

from __future__ import annotations

from typing import Any, Literal

import torch
import torch.nn as nn

ClosureMode = Literal["off", "probe", "full"]


def apply_top_k_filtering(logits: torch.Tensor, k: int) -> torch.Tensor:
    """
    Apply top-k filtering to logits: with non-top-k values set to -inf
    """
    top_k_values, top_k_indices = torch.topk(logits, min(k, logits.size(-1)), dim=-1)
    filtered_logits = torch.full_like(logits, float("-inf"))
    filtered_logits.scatter_(-1, top_k_indices, top_k_values)
    return filtered_logits


def apply_top_p_filtering(logits: torch.Tensor, p: float) -> torch.Tensor:
    """
    Apply top-p (nucleus) filtering to logits: with tokens beyond threshold set to -inf
    """
    sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
    cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)

    # Remove tokens with cumulative probability above threshold
    sorted_indices_to_remove = cumulative_probs > p
    sorted_indices_to_remove[..., 0] = False  # Keep at least one token
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()

    indices_to_remove = sorted_indices_to_remove.scatter(
        -1, sorted_indices, sorted_indices_to_remove
    )
    return logits.masked_fill(indices_to_remove, float("-inf"))


@torch.no_grad()
def diffusion_sample(
    model: nn.Module,
    seq_len: int = 256,
    num_steps: int = 256,
    top_k: int | None = None,
    top_p: float | None = None,
    temperature: float = 1.0,
    greedy: bool = True,
    mask_token_id: int = 151669,
    prefix_ids: torch.LongTensor | None = None,
    suffix_ids: torch.LongTensor | None = None,
    infill_length: int | None = None,
    eos_token_id: int = 151645,
    pad_token_id: int | None = None,
    bos_token_id: int | None = None,
    device: str | torch.device | None = None,
    visualizer: object | None = None,
    add_eos_at_end: bool = False,
    eb_gamma: float | None = None,
    # Closure integration (default preserves unmodified upstream behavior)
    closure_mode: ClosureMode = "off",
    closure_config: Any | None = None,
    return_closure_trace: bool = False,
    biological_context: dict[str, Any] | None = None,
) -> torch.LongTensor | dict[str, Any]:
    """
    Perform masked diffusion sampling with entropy-based token selection.

    Args:
        model: The RND1 language model
        seq_len: Target sequence length
        num_steps: Number of denoising steps
        top_k: Optional top-k filtering for sampling (None = no filtering)
        top_p: Optional nucleus (top-p) filtering for sampling (None = no filtering)
               When both top_k and top_p are set, top_k is applied first, then top_p
        temperature: Temperature for sampling (higher = more random, lower = more deterministic)
                    Values close to 0 are clamped to 1e-8 to avoid division by zero
        greedy: Whether to use greedy sampling (True) or stochastic (False)
        mask_token_id: Token ID for masked positions (default: 151669)
        prefix_ids: Optional prefix token IDs to preserve
        suffix_ids: Optional suffix token IDs to preserve
        infill_length: Length of infill region between prefix/suffix
        eos_token_id: End of sequence token ID (default: 151645)
        pad_token_id: Padding token ID (default: None, uses 0 if needed)
        bos_token_id: Beginning of sequence token ID (default: None)
        device: Device for computation (None = infer from model)
        visualizer: Optional visualizer for live visualization
        add_eos_at_end: Whether to force EOS token at the end of the sequence
        eb_gamma: Optional entropy-bound gamma for upstream EB schedule
        closure_mode: "off" (baseline), "probe" (telemetry only), or "full" (closure admission)
        closure_config: Optional closure.types.ClosureConfig
        return_closure_trace: If True, return dict with sequences and closure telemetry
        biological_context: Optional external biological hair context

    Denoising step under closure (probe/full):
        RND1 proposal → local token support → nonlocal hair → global sequence relation
        → return reconstruction → ordered potential-gate admission
        → commit / remain open / reject → next denoising basis

    Returns:
        Generated token IDs as LongTensor, or a dict when return_closure_trace is True
    """
    model.eval()

    device = next(model.parameters()).device if device is None else torch.device(device)

    if pad_token_id is None:
        pad_token_id = 0

    # Closure carrier (lazy import keeps baseline path light when mode is off)
    carrier = None
    closure_trace: list[dict[str, Any]] = []
    forward_passes = 0
    pre_len = 0
    suf_len = 0
    if closure_mode != "off" or closure_config is not None or return_closure_trace:
        from closure.sampler_bridge import make_carrier
        from closure.types import ClosureConfig

        if closure_config is None:
            cfg = ClosureConfig(mode=closure_mode)
        else:
            cfg = ClosureConfig(
                mode=closure_mode,
                return_depth=closure_config.return_depth,
                local_radius=closure_config.local_radius,
                distant_radius=closure_config.distant_radius,
                open_state_threshold=closure_config.open_state_threshold,
                contradiction_threshold=closure_config.contradiction_threshold,
                minimum_finite_progress=closure_config.minimum_finite_progress,
                track_return_side=closure_config.track_return_side,
                use_hidden_state_hair=closure_config.use_hidden_state_hair,
                use_expert_routing_hair=closure_config.use_expert_routing_hair,
                require_independent_return=closure_config.require_independent_return,
                emit_telemetry=closure_config.emit_telemetry,
                max_open_fraction=closure_config.max_open_fraction,
            )
        carrier = make_carrier(cfg)

    # Build initial masked sequence
    # When prefix_ids is provided, we create a sequence of length seq_len where:
    # - The prefix occupies the first pre_len positions
    # - The remaining (seq_len - pre_len) positions are filled with mask tokens to be generated
    if prefix_ids is not None or suffix_ids is not None:
        if prefix_ids is not None:
            prefix_ids = (
                prefix_ids.to(device)
                if isinstance(prefix_ids, torch.Tensor)
                else torch.tensor(prefix_ids, device=device)
            )
            pre_len = prefix_ids.shape[-1] if prefix_ids.dim() > 0 else 0
        else:
            pre_len = 0

        if suffix_ids is not None:
            suffix_ids = (
                suffix_ids.to(device)
                if isinstance(suffix_ids, torch.Tensor)
                else torch.tensor(suffix_ids, device=device)
            )
            suf_len = suffix_ids.shape[-1] if suffix_ids.dim() > 0 else 0
        else:
            suf_len = 0

        reserved = 1 if eos_token_id is not None else 0
        used = pre_len + suf_len + reserved

        if used > seq_len:
            raise ValueError(
                f"Combined length of prefix ({pre_len}), suffix ({suf_len}), "
                f"and special tokens ({reserved}) = {used} exceeds seq_len ({seq_len}). "
                f"Please increase seq_len or reduce input lengths."
            )
        elif used == seq_len:
            raise ValueError(
                f"No space for generation: prefix ({pre_len}) + suffix ({suf_len}) "
                f"+ special tokens ({reserved}) = seq_len ({seq_len}). "
                f"Need at least 1 position for generation."
            )

        infill_length = min(infill_length or (seq_len - used), seq_len - used)

        x = torch.full((1, seq_len), pad_token_id, dtype=torch.long, device=device)
        pos = 0
        # if bos_token_id is not None:
        #     x[0, pos] = bos_token_id; pos += 1
        if eos_token_id is not None and add_eos_at_end:
            x[0, -1] = eos_token_id
        if pre_len > 0:
            x[0, pos : pos + pre_len] = prefix_ids.flatten()[:pre_len]
            pos += pre_len
        fill_start, fill_end = pos, pos + infill_length
        x[0, fill_start:fill_end] = mask_token_id
        # print(fill_start, fill_end, seq_len, used, x[0, -1])
        pos = fill_end
        if suf_len > 0:
            x[0, pos : pos + suf_len] = suffix_ids.flatten()[:suf_len]
            pos += suf_len

        init_maskable = torch.zeros_like(x, dtype=torch.bool)
        init_maskable[0, fill_start:fill_end] = True
    else:
        x = torch.full((1, seq_len), mask_token_id, dtype=torch.long, device=device)
        if bos_token_id is not None:
            x[0, 0] = bos_token_id
        if eos_token_id is not None and add_eos_at_end:
            x[0, -1] = eos_token_id
        init_maskable = x.eq(mask_token_id)

    if bos_token_id is not None:
        init_maskable[:, 0] = False
    if eos_token_id is not None:
        init_maskable &= x.ne(eos_token_id)
    init_maskable &= x.ne(pad_token_id)

    maskable = init_maskable.clone()
    xt = x.clone()

    if visualizer:
        visualizer.start_visualization(xt, maskable, num_steps)

    def forward_scores(tokens):
        """Compute predictions and entropy scores for next tokens."""
        nonlocal forward_passes
        forward_passes += 1
        # Try with input_ids parameter first (standard HF models)
        try:
            model_output = model(input_ids=tokens)
        except TypeError:
            # Fall back to positional argument
            model_output = model(tokens)

        # Apply temperature scaling (with safety for near-zero temperature)
        safe_temperature = max(temperature, 1e-8)  # Prevent division by zero
        logits = model_output.logits / safe_temperature

        # Apply filtering strategies
        # Note: When both top_k and top_p are provided, they are applied sequentially:
        # First top_k filters to k tokens, then top_p filters from those k tokens
        if top_k is not None and top_k > 0:
            logits = apply_top_k_filtering(logits, top_k)

        if top_p is not None and 0 < top_p < 1.0:
            logits = apply_top_p_filtering(logits, top_p)

        # Convert to log probabilities
        logp = torch.log_softmax(logits, dim=-1)

        # Greedy or stochastic sampling
        if greedy:
            pred_next = logp.argmax(-1)
        else:
            pred_next = torch.distributions.Categorical(logits=logp).sample()

        conf_next = torch.gather(logp, -1, pred_next.unsqueeze(-1)).squeeze(-1)

        p = logp.exp()
        ent_next = -(p * logp).sum(-1)

        # Shift predictions: pos i predicts token i+1
        pred_i = tokens.clone()
        conf_i = torch.full_like(conf_next, torch.finfo(conf_next.dtype).min)
        ent_i = torch.zeros_like(ent_next)

        pred_i[:, 1:] = pred_next[:, :-1]
        conf_i[:, 1:] = conf_next[:, :-1]
        ent_i[:, 1:] = ent_next[:, :-1]

        return pred_i, conf_i, ent_i

    pred_i, conf_i, ent_i = forward_scores(xt)
    total_masked = init_maskable.sum(1, keepdim=True)
    finf = torch.finfo(conf_i.dtype)

    for step in range(num_steps - 1, 0, -1):
        # --- Baseline RND1 proposal schedule (always computed) ---
        if eb_gamma is not None:
            # Error proxy: lower = better (unmask earlier - importance sampling)
            err = -conf_i.clone()
            err = err.masked_fill(~maskable, finf.max)

            sorted_err, idx = torch.sort(err, dim=-1)
            entropy_sorted = torch.gather(ent_i, 1, idx)

            # EB criterion: acc_entropy - cummax_entropy <= gamma
            acc_entropy = torch.cumsum(entropy_sorted, dim=-1)
            cummax_entropy, _ = torch.cummax(entropy_sorted, dim=-1)
            valid = (acc_entropy - cummax_entropy) <= eb_gamma

            to_unmask = torch.zeros_like(maskable)
            B, L = maskable.shape
            for b in range(B):
                maskable_idx = idx[b]
                valid_b = valid[b]

                # how many satisfy the bound
                k_b = int(valid_b.sum().item())

                if k_b > 0:
                    chosen = maskable_idx[:k_b]
                    candidate = torch.zeros_like(maskable[b])
                    candidate[chosen] = True
                    to_unmask[b] = candidate & maskable[b]
        else:
            rate = step / num_steps
            cutoff_len = (total_masked * rate).long().clamp(min=0)

            # Choose HIGH-entropy tokens to keep masked
            sel_scores = ent_i.masked_fill(~maskable, -finf.max)
            B, L = sel_scores.shape
            k_max = cutoff_len.max().item()
            if k_max > 0:
                sss, idx = torch.topk(sel_scores, k_max, dim=-1, largest=True)
                keep_mask = torch.zeros_like(sel_scores, dtype=torch.bool)
                for b in range(B):
                    k_b = int(cutoff_len[b].item())
                    if k_b > 0:
                        keep_mask[b, idx[b, :k_b]] = True
            else:
                keep_mask = torch.zeros_like(sel_scores, dtype=torch.bool)

            to_unmask = maskable & ~keep_mask

        # --- Closure admission (off: baseline; probe: telemetry; full: controls) ---
        if carrier is not None and carrier.config.mode != "off":
            from closure.sampler_bridge import admit_denoising_step

            step_result = admit_denoising_step(
                carrier=carrier,
                xt=xt,
                pred_i=pred_i,
                conf_i=conf_i,
                ent_i=ent_i,
                maskable=maskable,
                baseline_to_unmask=to_unmask,
                step=step,
                prefix_len=pre_len,
                suffix_len=suf_len,
                biological_context=biological_context,
            )
            to_unmask = step_result.commit_mask
            closure_trace.append(
                {
                    "step": step,
                    "mode": carrier.config.mode,
                    "committed": int(to_unmask.sum().item()),
                    "open": int(step_result.open_mask.sum().item()),
                    "rejected": int(step_result.reject_mask.sum().item()),
                    "ordered_support": step_result.ordered_support,
                    "telemetry": step_result.telemetry,
                    "resolutions": {
                        str(k): v.value for k, v in step_result.resolutions.items()
                    },
                }
            )

        if to_unmask.any():
            xt[to_unmask] = pred_i[to_unmask]
            maskable[to_unmask] = False

        if visualizer:
            visualizer.update_step(xt, maskable, num_steps - step, ent_i, conf_i)

        if maskable.any():
            pred_i, conf_i, ent_i = forward_scores(xt)

    if maskable.any():
        # Final fill: baseline always commits remaining masks. In full closure mode,
        # remaining uncertain tokens may stay marked OPEN in the trace while still
        # receiving a provisional token so generation terminates finitely.
        if carrier is not None and carrier.config.mode == "full":
            closure_trace.append(
                {
                    "step": 0,
                    "mode": "full",
                    "final_open_positions": maskable[0].nonzero(as_tuple=False).flatten().tolist(),
                    "note": "finite termination fill; unresolved openings recorded",
                }
            )
        xt[maskable] = pred_i[maskable]
        maskable[:] = False

    if visualizer:
        visualizer.stop_visualization()

    if return_closure_trace:
        ordered_support: tuple[str, ...] = ()
        if carrier is not None:
            from dataclasses import asdict

            from closure.digest import digest

            ordered_support = tuple(digest(asdict(a)) for a in carrier.ordered_history)
        return {
            "sequences": xt,
            "closure_mode": closure_mode,
            "closure_trace": closure_trace,
            "committed_trace": [] if carrier is None else list(carrier.committed_trace),
            "ordered_support": ordered_support,
            "forward_passes": forward_passes,
            "open_positions": [] if carrier is None else list(carrier.open_positions),
            "epistemic_status": {
                "finite_controller": "RERUNNABLE",
                "sampler_integration": "RERUNNABLE",
                "full_model_benchmark": "OPEN EMPIRICAL CLAIM",
                "architecture": "DESIGN DERIVATION",
            },
        }

    return xt

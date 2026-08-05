# Copyright 2026 scarryhott/bio contributors.
"""RND1 probe-ordering telemetry. Never treats scores as closure identity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch

from .hair import build_holistic_hair
from .types import ClosureConfig, HairComposition


@dataclass(frozen=True)
class TokenAdmission:
    admit: torch.Tensor
    open: torch.Tensor
    telemetry: dict[str, torch.Tensor | Any]
    hair: HairComposition | None = None


def closure_token_admission(
    confidence: torch.Tensor,
    entropy: torch.Tensor,
    maskable: torch.Tensor,
    target_count: int,
    radius: int = 2,
    config: ClosureConfig | None = None,
    tokens: torch.Tensor | None = None,
    prefix_len: int = 0,
    suffix_len: int = 0,
    hidden_summary: dict[str, Any] | None = None,
    expert_routing: dict[str, Any] | None = None,
    denoising_history: list[dict[str, Any]] | None = None,
    biological_context: dict[str, Any] | None = None,
    step_index: int = 0,
) -> TokenAdmission:
    """Order RND1 probes without treating the score as closure identity.

    Admitted positions are provisional microactions; semantic closure still
    requires an independently transformed return through ClosureRuntime.
    """
    cfg = config or ClosureConfig()
    local_radius = cfg.local_radius if config else radius
    distant_radius = cfg.distant_radius

    active = maskable.to(confidence.dtype)
    count = active.sum(1, keepdim=True).clamp_min(1)
    mean = (confidence * active).sum(1, keepdim=True) / count
    var = (((confidence - mean) ** 2) * active).sum(1, keepdim=True) / count
    local = torch.sigmoid((confidence - mean) / var.sqrt().clamp_min(1e-5))

    def _roll_mean(src: torch.Tensor, rad: int) -> torch.Tensor:
        numerator = torch.zeros_like(src)
        denominator = torch.zeros_like(src)
        for distance in range(1, rad + 1):
            for direction in (-1, 1):
                shifted = torch.roll(src, direction * distance, dims=1)
                shifted_mask = torch.roll(active, direction * distance, dims=1)
                numerator += shifted * shifted_mask
                denominator += shifted_mask
        return numerator / denominator.clamp_min(1)

    hair_local = _roll_mean(local, local_radius)
    hair_distant = _roll_mean(local, distant_radius)
    global_digest = (local * active).sum(1, keepdim=True) / count
    returned = torch.tanh(
        0.40 * local + 0.20 * hair_local + 0.15 * hair_distant + 0.25 * global_digest
    )
    residual = (returned - local).abs()
    probe_score = returned + 0.25 * (1 - residual) - 0.25 * torch.tanh(entropy)

    # Open-state threshold: uncertain tokens stay open when residual is large.
    uncertain = residual > cfg.open_state_threshold
    contradiction = residual > cfg.contradiction_threshold

    score = probe_score.masked_fill(~maskable, float("-inf"))
    admit = torch.zeros_like(maskable)
    for batch in range(score.shape[0]):
        available_idx = maskable[batch].nonzero(as_tuple=False).flatten()
        if available_idx.numel() == 0:
            continue
        ranked = torch.topk(score[batch, available_idx], k=available_idx.numel()).indices
        ordered = available_idx[ranked]
        kept = 0
        for pos in ordered.tolist():
            if contradiction[batch, pos]:
                continue
            if uncertain[batch, pos] and kept >= max(cfg.minimum_finite_progress, 1):
                continue
            admit[batch, pos] = True
            kept += 1
            if kept >= max(target_count, cfg.minimum_finite_progress):
                break

    open_mask = maskable & ~admit
    hair_comp = None
    if tokens is not None and tokens.shape[0] > 0:
        tok_list = tokens[0].detach().cpu().tolist()
        mask_list = maskable[0].detach().cpu().tolist()
        local_list = local[0].detach().cpu().tolist()
        hair_comp = build_holistic_hair(
            tokens=tok_list,
            maskable=mask_list,
            local_scores=local_list,
            prefix_len=prefix_len,
            suffix_len=suffix_len,
            local_radius=local_radius,
            distant_radius=distant_radius,
            hidden_summary=hidden_summary if cfg.use_hidden_state_hair else None,
            expert_routing=expert_routing if cfg.use_expert_routing_hair else None,
            denoising_history=denoising_history,
            biological_context=biological_context,
            step_index=step_index,
        )

    return TokenAdmission(
        admit=admit,
        open=open_mask,
        telemetry={
            "local": local,
            "hair_local": hair_local,
            "hair_distant": hair_distant,
            "global_digest": global_digest,
            "returned": returned,
            "return_residual": residual,
            "probe_score": probe_score,
            "uncertain": uncertain,
            "contradiction": contradiction,
            # Explicitly labeled as axiometric shadows, not identity:
            "axiometric_shadows_only": True,
        },
        hair=hair_comp,
    )

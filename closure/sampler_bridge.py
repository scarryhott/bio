# Copyright 2026 scarryhott/bio contributors.
"""Bridge from RND1 diffusion steps into the closure carrier."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

import torch

from .digest import digest
from .connected_return import (
    evaluate_connected_return,
    make_occurrence,
)
from .rnd_controller import TokenAdmission, closure_token_admission
from .runtime import ClosureRuntime
from .types import (
    ClosureCarrier,
    ClosureConfig,
    HairComposition,
    MicroAction,
    PotentialGate,
    Resolution,
    ReturnWitness,
    StepAdmission,
)


def make_sequence_gate(
    *,
    gate_id: str = "rnd1-diffusion",
    relation_key: str = "sequence-token-admission",
    mandate: dict[str, Any] | None = None,
) -> PotentialGate:
    return PotentialGate(
        gate_id=gate_id,
        originless_basis="predual:rnd1-masked-diffusion",
        ball={"kind": "masked_sequence", "actor_tails": {}},
        possible_hair=[],
        semantics={"relation_key": relation_key},
        openings=["next_denoising_step"],
        admissibility={
            "controlled_boundaries": ["model_echo", "self"],
            "difference_preservation": True,
            "recursive_recoverability": True,
        },
        mandate=mandate
        or {
            "required_witness_fields": ["local_viability", "global_consequence"],
            "generation_constraints": {},
        },
        return_side="ball",
    )


def make_carrier(config: ClosureConfig, gate: PotentialGate | None = None) -> ClosureCarrier:
    g = gate or make_sequence_gate()
    return ClosureCarrier(
        gate=g,
        ball=g.ball,
        hair=HairComposition(),
        semantics=g.semantics,
        openings=list(g.openings),
        mandate=g.mandate,
        return_partition={"side": g.return_side or "ball", "complement": "hair"},
        axiometric_evidence={},
        config=config,
    )


def baseline_unmask_mask(
    *,
    maskable: torch.Tensor,
    ent_i: torch.Tensor,
    conf_i: torch.Tensor,
    step: int,
    num_steps: int,
    total_masked: torch.Tensor,
    eb_gamma: float | None,
) -> torch.Tensor:
    """Exact upstream RND1 admission schedule (entropy / optional EB)."""
    finf = torch.finfo(conf_i.dtype)
    if eb_gamma is not None:
        err = -conf_i.clone()
        err = err.masked_fill(~maskable, finf.max)
        sorted_err, idx = torch.sort(err, dim=-1)
        entropy_sorted = torch.gather(ent_i, 1, idx)
        acc_entropy = torch.cumsum(entropy_sorted, dim=-1)
        cummax_entropy, _ = torch.cummax(entropy_sorted, dim=-1)
        valid = (acc_entropy - cummax_entropy) <= eb_gamma
        to_unmask = torch.zeros_like(maskable)
        B = maskable.shape[0]
        for b in range(B):
            maskable_idx = idx[b]
            k_b = int(valid[b].sum().item())
            if k_b > 0:
                chosen = maskable_idx[:k_b]
                candidate = torch.zeros_like(maskable[b])
                candidate[chosen] = True
                to_unmask[b] = candidate & maskable[b]
        return to_unmask

    rate = step / num_steps
    cutoff_len = (total_masked * rate).long().clamp(min=0)
    sel_scores = ent_i.masked_fill(~maskable, -finf.max)
    B, _L = sel_scores.shape
    k_max = int(cutoff_len.max().item())
    if k_max > 0:
        _sss, idx = torch.topk(sel_scores, k_max, dim=-1, largest=True)
        keep_mask = torch.zeros_like(sel_scores, dtype=torch.bool)
        for b in range(B):
            k_b = int(cutoff_len[b].item())
            if k_b > 0:
                keep_mask[b, idx[b, :k_b]] = True
    else:
        keep_mask = torch.zeros_like(sel_scores, dtype=torch.bool)
    return maskable & ~keep_mask


def admit_denoising_step(
    *,
    carrier: ClosureCarrier,
    xt: torch.Tensor,
    pred_i: torch.Tensor,
    conf_i: torch.Tensor,
    ent_i: torch.Tensor,
    maskable: torch.Tensor,
    baseline_to_unmask: torch.Tensor,
    step: int,
    prefix_len: int = 0,
    suffix_len: int = 0,
    hidden_summary: dict[str, Any] | None = None,
    expert_routing: dict[str, Any] | None = None,
    biological_context: dict[str, Any] | None = None,
) -> StepAdmission:
    """Apply closure_mode policy to one denoising step."""
    cfg = carrier.config
    runtime = ClosureRuntime()
    target = int(baseline_to_unmask[0].sum().item()) if baseline_to_unmask.any() else 0

    admission: TokenAdmission = closure_token_admission(
        confidence=conf_i,
        entropy=ent_i,
        maskable=maskable,
        target_count=max(target, cfg.minimum_finite_progress if target else 0),
        config=cfg,
        tokens=xt,
        prefix_len=prefix_len,
        suffix_len=suffix_len,
        hidden_summary=hidden_summary,
        expert_routing=expert_routing,
        denoising_history=carrier.committed_trace,
        biological_context=biological_context,
        step_index=step,
    )
    if admission.hair is not None:
        carrier.hair = admission.hair

    carrier.axiometric_evidence = {
        "step": step,
        "confidence_mean": float(conf_i[maskable].mean().item()) if maskable.any() else 0.0,
        "entropy_mean": float(ent_i[maskable].mean().item()) if maskable.any() else 0.0,
        "probe_rank": admission.hair.probe_rank_scalar() if admission.hair else 0.0,
        "note": "axiometric shadows only; not closure identity",
    }

    if cfg.mode == "off":
        commit = baseline_to_unmask.clone()
        open_mask = maskable & ~commit
        reject = torch.zeros_like(maskable)
        return StepAdmission(
            commit_mask=commit,
            open_mask=open_mask,
            reject_mask=reject,
            resolutions={},
            telemetry={"mode": "off"},
            ordered_support=(),
        )

    if cfg.mode == "probe":
        # Telemetry computed; baseline remains authoritative.
        commit = baseline_to_unmask.clone()
        open_mask = maskable & ~commit
        reject = torch.zeros_like(maskable)
        telemetry = dict(admission.telemetry)
        telemetry["mode"] = "probe"
        telemetry["baseline_authoritative"] = True
        return StepAdmission(
            commit_mask=commit,
            open_mask=open_mask,
            reject_mask=reject,
            resolutions={},
            telemetry=telemetry if cfg.emit_telemetry else {"mode": "probe"},
            ordered_support=runtime.ordered_support(carrier.gate),
        )

    connected = cfg.mode == "full-connected-return"

    # full / full-connected-return: closure controls admission
    commit = admission.admit & maskable
    # Ensure finite progress when baseline wanted progress and candidates exist.
    if target > 0 and not commit.any() and maskable.any():
        score = admission.telemetry["probe_score"]
        for b in range(maskable.shape[0]):
            avail = maskable[b].nonzero(as_tuple=False).flatten()
            if avail.numel() == 0:
                continue
            best = avail[torch.argmax(score[b, avail])]
            commit[b, best] = True

    reject = admission.telemetry["contradiction"] & maskable & ~commit
    open_mask = maskable & ~commit & ~reject

    # Connected-return: label candidate occurrences and admit only under
    # unique contact-derived order + complete primitive support recovery.
    connected_verdict = None
    if connected:
        candidates: list = []
        for b in range(commit.shape[0]):
            for pos in commit[b].nonzero(as_tuple=False).flatten().tolist():
                residual = float(admission.telemetry["return_residual"][b, pos].item())
                independent = residual > cfg.open_state_threshold * 0.5
                occ = make_occurrence(
                    token_id=int(pred_i[b, pos].item()),
                    position=int(pos),
                    step=step,
                    prior_mask=True,
                    ancestry="denoising_return",
                    return_side=str(carrier.return_partition.get("side", "ball")),
                    residual=residual,
                    independently_transformed=independent,
                )
                candidates.append(occ)
        connected_verdict = evaluate_connected_return(candidates)
        carrier.labeled_occurrences.extend(candidates)
        carrier.connected_return_trace.append(
            {
                "step": step,
                "status": connected_verdict.status,
                "shared_contacts": connected_verdict.shared_contacts,
                "support_size": len(connected_verdict.holistic_support),
                "admissible": len(connected_verdict.admissible_occurrence_ids),
            }
        )
        allowed = set(connected_verdict.admissible_occurrence_ids)
        if not connected_verdict.admits:
            # Leave all candidates OPEN — do not inflate tokens on broken return.
            for b in range(commit.shape[0]):
                open_mask[b] = open_mask[b] | commit[b]
                commit[b] = False
        else:
            for b in range(commit.shape[0]):
                for pos in commit[b].nonzero(as_tuple=False).flatten().tolist():
                    # Match by reconstructing the same occurrence id.
                    residual = float(admission.telemetry["return_residual"][b, pos].item())
                    independent = residual > cfg.open_state_threshold * 0.5
                    oid = make_occurrence(
                        token_id=int(pred_i[b, pos].item()),
                        position=int(pos),
                        step=step,
                        prior_mask=True,
                        ancestry="denoising_return",
                        return_side=str(carrier.return_partition.get("side", "ball")),
                        residual=residual,
                        independently_transformed=independent,
                    ).occurrence_id
                    if oid not in allowed:
                        commit[b, pos] = False
                        open_mask[b, pos] = True

        # Finite progress floor: if baseline demanded progress and everything stayed
        # OPEN due to incomplete multi-cell contacts, allow minimum_finite_progress
        # only when each singleton passes primitive return (single-cell OK path).
        if target > 0 and not commit.any() and candidates:
            singleton = evaluate_connected_return(candidates[:1])
            if singleton.admits:
                pos = candidates[0].position
                commit[0, pos] = True
                open_mask[0, pos] = False
                connected_verdict = singleton

    resolutions: dict[int, Resolution] = {}
    for b in range(commit.shape[0]):
        positions = commit[b].nonzero(as_tuple=False).flatten().tolist()
        for pos in positions:
            prior = carrier.gate.ball.get("actor_tails", {}).get("sampler", "root")
            action = MicroAction(
                actor_id="sampler",
                relation_key=str(carrier.semantics.get("relation_key")),
                prior_tail=prior,
                semantic_pointing=f"token@{pos}",
                context=f"step:{step}",
                payload={
                    "token_id": int(pred_i[b, pos].item()),
                    "position": int(pos),
                    "confidence": float(conf_i[b, pos].item()),
                    "entropy": float(ent_i[b, pos].item()),
                    "connected_return": connected,
                },
                step_index=step,
                position=int(pos),
                token_id=int(pred_i[b, pos].item()),
            )
            runtime.append_action(carrier.gate, action)
            carrier.ordered_history.append(action)

            residual = float(admission.telemetry["return_residual"][b, pos].item())
            independent = residual > cfg.open_state_threshold * 0.5
            if cfg.require_independent_return and not independent:
                resolutions[int(pos)] = Resolution.OPEN
                witness = ReturnWitness(
                    source_boundary="model_echo",
                    transformed_context=f"step:{step}:pos:{pos}",
                    recovered_relation=str(carrier.semantics.get("relation_key")),
                    ordered_support=runtime.ordered_support(carrier.gate),
                    consequence={},
                )
                receipt = runtime.resolve(carrier.gate, witness)
                resolutions[int(pos)] = receipt.resolution
                continue

            next_opening = "next_denoising_step" if open_mask[b].any() else None
            if connected and connected_verdict is not None and connected_verdict.admits:
                next_opening = "child_connected_return_opening"

            witness = ReturnWitness(
                source_boundary="denoising_return"
                if not connected
                else "connected_return",
                transformed_context=f"step:{step}:pos:{pos}:residual:{residual:.4f}",
                recovered_relation=str(carrier.semantics.get("relation_key")),
                ordered_support=runtime.ordered_support(carrier.gate),
                consequence={
                    "local_viability": True,
                    "global_consequence": True,
                    "independently_transformed": True,
                    "connected_return_status": None
                    if connected_verdict is None
                    else connected_verdict.status,
                },
                transformation_path=(f"noise→token@{pos}", f"step:{step}"),
                return_discrepancy=residual,
                return_side=carrier.return_partition.get("side"),
                next_opening=next_opening,
            )
            receipt = runtime.resolve(carrier.gate, witness)
            resolutions[int(pos)] = receipt.resolution
            if receipt.write_back_allowed:
                carrier.committed_trace.append(
                    {
                        "step": step,
                        "position": int(pos),
                        "token_id": int(pred_i[b, pos].item()),
                        "resolution": receipt.resolution.value,
                        "digest": receipt.basis_digest,
                        "support": receipt.ordered_support,
                    }
                )
            elif receipt.resolution is Resolution.REFUSED:
                commit[b, pos] = False
                open_mask[b, pos] = True

    carrier.step_index = step
    carrier.open_positions = open_mask[0].nonzero(as_tuple=False).flatten().tolist()
    telemetry = dict(admission.telemetry) if cfg.emit_telemetry else {}
    telemetry["mode"] = cfg.mode
    telemetry["resolutions"] = {str(k): v.value for k, v in resolutions.items()}
    if connected_verdict is not None:
        telemetry["connected_return"] = {
            "status": connected_verdict.status,
            "shared_contacts": list(connected_verdict.shared_contacts),
            "holistic_support_size": len(connected_verdict.holistic_support),
            "admits": connected_verdict.admits,
        }
    return StepAdmission(
        commit_mask=commit,
        open_mask=open_mask,
        reject_mask=reject,
        resolutions=resolutions,
        telemetry=telemetry,
        ordered_support=runtime.ordered_support(carrier.gate),
    )


def support_digest(actions: list[MicroAction]) -> tuple[str, ...]:
    return tuple(digest(asdict(a)) for a in actions)

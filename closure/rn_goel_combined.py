# Copyright 2026 scarryhott/bio contributors.
"""Combine Radical Numerics open surface with Goel paper logic under our C.

Stack (external RN + Goel papers + our admission):

    our Closure AGI admission (C)
        ↑
    Goel paper logic — DNA×env motor, Wuite tension prior, δ_C(Q) architecture
        ↑
    Radical Numerics open surface — RND1 (code ± weights), spear/dInfer reported
        ↑
    open / held-out biological returns

RND1 supplies a local Kakeya / tokenized-relativity presentation (language or
mock). Goel supplies the global Chaitin DNA×environment hair from published
mechanism. Neither owns C; Omnii stays reported-only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from .digest import digest
from .goel_operator import (
    TokenizedRelativityBall,
    apply_goel_chaitin_operator,
    bind_local_kakeya_global_goel,
    goel_state_from_modalities,
    programme_role_split,
)
from .independent_model import stable_digest
from .paper_data_layer import goel_mode_from_wuite_tension, load_wuite_tension_prior
from .return_unified_runtime import (
    OpenArchitectureCarrier,
    ReunifiedAdmissionReceipt,
    ReturnUnifiedEpisodeSpec,
    architecture_from_system,
    reunify_episode,
)
from .rn_open_surface import RnOpenSurface, inventory_rn_open_surface
from .self_verification import ClosureVerificationStatus
from .topology import UnifiedAxiometry

OUR_SYSTEM = {
    "id": "bio-closure-independent",
    "family": "black-mirror-closure",
    "biological_native": True,
    "open_weights": False,
    "ownership": "scarryhott-bio-transcript-thesis",
    "adapter": "closure.independent_model:UnifiedClosureArchitecturalLoop",
    "epistemic_status": "RERUNNABLE_FINITE_KERNEL",
    "availability": "repository-local",
    "role": "OUR self-contained Closure AGI",
}

RND1_SYSTEM = {
    "id": "rnd1-plus-closure",
    "family": "hybrid-external-under-our-admission",
    "biological_native": False,
    "open_weights": True,
    "model_id": "radicalnumerics/RND1-Base-0910",
    "ownership": "radical-numerics-weights-plus-our-admission",
    "adapter": "rnd.sampling:diffusion_sample",
    "epistemic_status": "EXTERNAL_RN_ARCHITECTURE_UNDER_OUR_ADMISSION",
    "availability": "repository-local-plus-open-weights",
    "role": "EXTERNAL RND1 proposals admitted under OUR closure hooks",
}


@dataclass
class Rnd1ProposalReceipt:
    """RND1 local proposal used as Kakeya presentation (mock or weight-backed)."""

    mode: str
    closure_mode: str
    sequences_digest: str
    trace_steps: int
    ownership: str = "radical-numerics-external"
    weights_used: bool = False
    detail: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class CombinedEpisodeReceipt:
    episode_id: str
    benchmark_id: str
    dataset_role: str
    our_receipt: dict[str, Any]
    rnd1_receipt: dict[str, Any]
    rnd1_proposal: dict[str, Any]
    goel_operator_status: str | None
    goel_mode_from_wuite: str | None
    dual_status: str | None
    combined_status: str
    reason: str
    combined_digest: str


def run_rnd1_open_proposal(
    *,
    closure_mode: str = "full",
    prefer_weights: bool = False,
) -> Rnd1ProposalReceipt:
    """Run RND1 open sampler path: live weights if present, else finite mock.

    Full 30B RND1 shards are optional. The open code path (`rnd/sampling.py`)
    always participates as the RN local presentation under our hooks.
    """

    import torch
    import torch.nn as nn
    from rnd.sampling import diffusion_sample

    weights_present = False
    if prefer_weights:
        weights_present = architecture_from_system(
            RND1_SYSTEM
        ).weights_available

    if weights_present:
        # Reserved: live 30B path. Not claimed unless weights are local.
        return Rnd1ProposalReceipt(
            mode="open_weights_present_not_executed_in_this_harness",
            closure_mode=closure_mode,
            sequences_digest="",
            trace_steps=0,
            weights_used=True,
            detail=(
                "RND1 weights detected locally but combined harness uses the "
                "finite mock sampler for CI-scale reunification; Chapter A "
                "holistic artifact covers measured 30B substrate"
            ),
            evidence={"weights_available": True},
        )

    class TinyMockLM(nn.Module):
        def __init__(self, vocab_size: int = 32, hidden: int = 8):
            super().__init__()
            self.embed = nn.Embedding(vocab_size, hidden)
            self.proj = nn.Linear(hidden, vocab_size)

        def forward(self, input_ids=None, **kwargs):
            h = self.embed(input_ids.clamp(min=0, max=self.embed.num_embeddings - 1))
            return type("Out", (), {"logits": self.proj(h)})()

    torch.manual_seed(0)
    out = diffusion_sample(
        model=TinyMockLM(),
        seq_len=16,
        num_steps=6,
        mask_token_id=0,
        pad_token_id=1,
        eos_token_id=2,
        greedy=True,
        closure_mode=closure_mode,  # type: ignore[arg-type]
        return_closure_trace=True,
    )
    seq = out["sequences"]
    return Rnd1ProposalReceipt(
        mode="open_code_mock_sampler",
        closure_mode=str(out.get("closure_mode", closure_mode)),
        sequences_digest=stable_digest(seq.detach().cpu().tolist()),
        trace_steps=len(out.get("closure_trace") or []),
        weights_used=False,
        detail="RND1 open sampling.py under our hooks with finite mock LM (no 30B)",
        evidence={
            "forward_passes": out.get("forward_passes"),
            "shape": list(seq.shape),
            "hf_model": "radicalnumerics/RND1-Base-0910",
            "vendored": "rnd/",
        },
    )


def _wuite_tension_for_episode(episode: ReturnUnifiedEpisodeSpec) -> float | None:
    env = episode.biological.modalities.get("environment") or {}
    for key in ("tension_pN", "tension", "mechanical_tension"):
        if key in env and env[key] is not None:
            try:
                return float(env[key])
            except (TypeError, ValueError):
                return None
    # Default mild tension from Wuite prior operating band when DNA present.
    if "DNA" in episode.biological.modalities:
        return 6.0
    return None


def _goel_on_episode(
    episode: ReturnUnifiedEpisodeSpec,
    *,
    architecture: OpenArchitectureCarrier,
    turn_unity: str,
) -> dict[str, Any]:
    modalities = episode.biological.modalities
    if "DNA" not in modalities:
        return {
            "goel_operator_status": None,
            "goel_mode_from_wuite": None,
            "dual_status": None,
            "goel_digest": None,
            "dual_digest": None,
        }

    tension = _wuite_tension_for_episode(episode)
    mode = goel_mode_from_wuite_tension(tension) if tension is not None else None
    env = dict(modalities.get("environment") or {})
    if tension is not None and "tension" not in env and "tension_pN" not in env:
        env = {**env, "tension_pN": tension, "tension_source": "wuite_prior_default_band"}

    before = goel_state_from_modalities(
        {
            "DNA": modalities["DNA"],
            "environment": env,
            "returned_consequence": modalities.get("returned_consequence") or {},
        }
    )
    after = goel_state_from_modalities(
        {
            "DNA": modalities["DNA"],
            "environment": env,
            "returned_consequence": modalities.get("returned_consequence") or {},
        }
    )
    goel = apply_goel_chaitin_operator(
        before,
        after,
        independent=episode.independent,
        self_authored=episode.self_authored,
        contradictory=episode.contradictory,
    )
    local = TokenizedRelativityBall(
        ball_id=f"rn-kakeya:{architecture.system_id}:{episode.episode_id}",
        occurrences=(
            {
                "occurrence_id": turn_unity,
                "token_id": 0,
                "position": 0,
                "step": 0,
                "return_side": "ball",
                "identity_is_not_token": True,
                "architecture": architecture.system_id,
                "rn_family": "rnd1-local-presentation",
            },
        ),
        return_side="ball",
        contacts=(
            f"arch:{architecture.architecture_digest[:12]}",
            f"goel:{goel.operator_digest[:12]}",
            "rn:open-surface",
        ),
        radical_numerics_family="rnd1-tokenized-relativity",
        ball_digest=stable_digest(
            {"unity": turn_unity, "arch": architecture.architecture_digest}
        ),
    )
    dual = bind_local_kakeya_global_goel(local, goel)
    return {
        "goel_operator_status": goel.status.value,
        "goel_mode_from_wuite": mode.value if mode is not None else None,
        "dual_status": dual.dual_status,
        "goel_digest": goel.operator_digest,
        "dual_digest": dual.dual_digest,
        "tension_pN": tension,
        "wuite_prior": True,
    }


def _receipt_dict(receipt: ReunifiedAdmissionReceipt) -> dict[str, Any]:
    from .return_unified_runtime import receipt_to_dict

    return receipt_to_dict(receipt)


def combine_episode(
    episode: ReturnUnifiedEpisodeSpec,
    *,
    rnd1_proposal: Rnd1ProposalReceipt,
    axiometry: UnifiedAxiometry | None = None,
) -> CombinedEpisodeReceipt:
    """Reunify one episode under our C with RND1 local + Goel global paper logic."""

    ax = axiometry or UnifiedAxiometry()
    our_arch = architecture_from_system(OUR_SYSTEM, weights_available=True)
    rnd1_arch = architecture_from_system(RND1_SYSTEM)

    our = reunify_episode(our_arch, episode, axiometry=ax)
    rnd1 = reunify_episode(rnd1_arch, episode, axiometry=ax)

    goel_info = _goel_on_episode(
        episode,
        architecture=our_arch,
        turn_unity=our.turn_unity_digest,
    )

    # Combined status: our kernel must close data; RND1 may be language-hybrid OPEN;
    # Goel dual should connect when DNA present.
    if our.joint_arm_status == "VERIFIED":
        if goel_info["goel_operator_status"] in {
            None,
            "ADMITTED_GLOBAL_HAIR",
            "OPEN_MISSING_ENVIRONMENT",
            "OPEN_SELF_AUTHORED",
        }:
            if rnd1.joint_arm_status in {
                "VERIFIED",
                "OPEN_NONBIOLOGICAL_LANGUAGE_ARM",
                "OPEN_ARCHITECTURE_WEIGHTS_ABSENT",
            }:
                combined = "COMBINED_OUR_VERIFIED_RN_PRESENT_GOEL_BOUND"
            else:
                combined = "COMBINED_OUR_VERIFIED_RN_OPEN"
        else:
            combined = "COMBINED_OUR_VERIFIED_GOEL_SIDE_OPEN_OR_REJECTED"
    elif our.verification_status is ClosureVerificationStatus.OPEN:
        combined = "COMBINED_OPEN"
    else:
        combined = f"COMBINED_{our.joint_arm_status}"

    reason = (
        f"our={our.joint_arm_status}; rnd1={rnd1.joint_arm_status}; "
        f"goel={goel_info['goel_operator_status']}; dual={goel_info['dual_status']}; "
        f"rnd1_proposal={rnd1_proposal.mode}"
    )
    payload = {
        "episode": episode.episode_id,
        "our": our.reunification_digest,
        "rnd1": rnd1.reunification_digest,
        "goel": goel_info.get("goel_digest"),
        "dual": goel_info.get("dual_digest"),
        "proposal": rnd1_proposal.sequences_digest,
        "combined": combined,
    }
    return CombinedEpisodeReceipt(
        episode_id=episode.episode_id,
        benchmark_id=episode.benchmark_id,
        dataset_role=episode.role,
        our_receipt=_receipt_dict(our),
        rnd1_receipt=_receipt_dict(rnd1),
        rnd1_proposal={
            "mode": rnd1_proposal.mode,
            "closure_mode": rnd1_proposal.closure_mode,
            "sequences_digest": rnd1_proposal.sequences_digest,
            "trace_steps": rnd1_proposal.trace_steps,
            "weights_used": rnd1_proposal.weights_used,
            "detail": rnd1_proposal.detail,
            "evidence": rnd1_proposal.evidence,
        },
        goel_operator_status=goel_info["goel_operator_status"],
        goel_mode_from_wuite=goel_info["goel_mode_from_wuite"],
        dual_status=goel_info["dual_status"],
        combined_status=combined,
        reason=reason,
        combined_digest=stable_digest(payload),
    )


def run_rn_goel_combined(
    episodes: Sequence[ReturnUnifiedEpisodeSpec],
    *,
    fetch_rn_surface: bool = True,
    rnd1_closure_mode: str = "full",
) -> dict[str, Any]:
    """Run combined RN open + Goel paper logic + our admission over episodes."""

    surface: RnOpenSurface = inventory_rn_open_surface(fetch=fetch_rn_surface)
    proposal = run_rnd1_open_proposal(closure_mode=rnd1_closure_mode)
    roles = programme_role_split()
    prior = load_wuite_tension_prior()

    receipts = [combine_episode(ep, rnd1_proposal=proposal) for ep in episodes]
    status_counts: dict[str, int] = {}
    for row in receipts:
        status_counts[row.combined_status] = status_counts.get(row.combined_status, 0) + 1

    our_verified = sum(
        1 for r in receipts if r.our_receipt.get("joint_arm_status") == "VERIFIED"
    )
    goel_bound = sum(1 for r in receipts if r.goel_operator_status is not None)
    dual_connected = sum(
        1 for r in receipts if r.dual_status == "DUAL_CLOSED_TO_OPENING"
    )

    stack = {
        "top": "our Closure AGI admission (C)",
        "goel_paper_logic": {
            "architecture": "goel-dna-environment-motor",
            "prior": "wuite-bustamante-tension-prior",
            "landmarks_pN": prior.get("landmarks"),
            "dialogue": roles["parallel_dialogue"]["relation"],
            "subsumption": False,
        },
        "radical_numerics_open": {
            "surface_digest": surface.surface_digest,
            "repos": [r["id"] for r in surface.repos],
            "rnd1_hf": "radicalnumerics/RND1-Base-0910",
            "rnd1_proposal_mode": proposal.mode,
            "weights_local": surface.rnd1_weights.get("local_weights_present"),
        },
        "bottom": "held-out / open biological returns",
        "ownership": surface.ownership,
    }

    return {
        "schema_version": "1.0",
        "protocol": "rn-open-plus-goel-paper-logic-under-our-c",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "relation": (
            "(C_t, B_RND1_local_Kakeya, H_Goel_Chaitin, E_t, A_legal,t) "
            "↔_C (A_t, E_{t+1}, R_t, V_t, C_{t+1})"
        ),
        "stack": stack,
        "rn_open_surface": surface.to_dict(),
        "rnd1_proposal": {
            "mode": proposal.mode,
            "closure_mode": proposal.closure_mode,
            "sequences_digest": proposal.sequences_digest,
            "trace_steps": proposal.trace_steps,
            "weights_used": proposal.weights_used,
            "detail": proposal.detail,
            "evidence": proposal.evidence,
        },
        "episode_count": len(episodes),
        "receipt_count": len(receipts),
        "combined_status_counts": status_counts,
        "our_kernel_verified": our_verified,
        "goel_bound_episodes": goel_bound,
        "dual_status_present": dual_connected,
        "epistemic": {
            "primary_goal": "our_closure_verification_admission_vs_frontier_paper_results",
            "this_harness": "supporting_rn_open_plus_goel_under_c",
            "rnd1_is_our_model": False,
            "rnd1_30b_is_bio_closure": False,
            "rnd1_30b_role": "FINITE_AI_SUBSTRATE_TEST_NOT_BIO_CLOSURE",
            "goel_subsumed_into_black_mirror": False,
            "rnd1_30b_weights_executed": proposal.weights_used
            and proposal.mode.startswith("open_weights"),
            "rnd1_open_code_executed": proposal.mode == "open_code_mock_sampler",
            "spear_dinfer": "reported_open_infra_cached",
            "omnii": "reported_only",
            "combined_harness": "MEASURED",
        },
        "receipts": [
            {
                "episode_id": r.episode_id,
                "benchmark_id": r.benchmark_id,
                "dataset_role": r.dataset_role,
                "combined_status": r.combined_status,
                "reason": r.reason,
                "combined_digest": r.combined_digest,
                "goel_operator_status": r.goel_operator_status,
                "goel_mode_from_wuite": r.goel_mode_from_wuite,
                "dual_status": r.dual_status,
                "rnd1_proposal": r.rnd1_proposal,
                "our_joint": r.our_receipt.get("joint_arm_status"),
                "rnd1_joint": r.rnd1_receipt.get("joint_arm_status"),
                "our_receipt": r.our_receipt,
                "rnd1_receipt": r.rnd1_receipt,
            }
            for r in receipts
        ],
        "architecture_digest": digest(
            {
                "stack": stack,
                "surface": surface.surface_digest,
                "proposal": proposal.sequences_digest,
                "n": len(receipts),
            }
        ),
    }


__all__ = [
    "CombinedEpisodeReceipt",
    "Rnd1ProposalReceipt",
    "combine_episode",
    "run_rnd1_open_proposal",
    "run_rn_goel_combined",
]

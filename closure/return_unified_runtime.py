# Copyright 2026 scarryhott/bio contributors.
"""Return-unified reunification of open architectures and biological data.

Open architectures and held-out return data are lifted into one episode carrier:

    (C_t, E_t, A_legal,t) ↔_C (A_t, E_{t+1}, R_t, V_t, C_{t+1})

Learned scores, fitness, and confidence remain axiometric shadows. Verification
topology is admitted inside the return — never as a post-hoc filter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .biology import BiologicalEpisode, biological_episode_to_carrier, shadow_cannot_certify
from .goel_operator import (
    TokenizedRelativityBall,
    apply_goel_chaitin_operator,
    bind_local_kakeya_global_goel,
    goel_state_from_modalities,
)
from .independent_model import (
    Admission,
    ArchitecturalLoopTurn,
    UnifiedClosureArchitecturalLoop,
    stable_digest,
)
from .self_verification import (
    ClosureVerificationReceipt,
    ClosureVerificationStatus,
    closure_verification_is_authoritative,
    verify_closure_operation,
)
from .topology import (
    UnifiedAxiometry,
    VerificationTopology,
    admit_verification_topology,
)
from .types import ClosureReceipt, Resolution

@dataclass(frozen=True)
class OpenArchitectureCarrier:
    """Open architecture identity reunified into the episode — not a score oracle."""

    system_id: str
    family: str
    biological_native: bool
    open_weights: bool
    weights_available: bool
    proposal_mode: str
    architecture_digest: str
    representation_shadow: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReturnUnifiedEpisodeSpec:
    episode_id: str
    benchmark_id: str
    biological: BiologicalEpisode
    source_observation: Any
    legal_actions: tuple[Any, ...]
    returned_observation: Any
    next_legal_actions: tuple[Any, ...]
    independent: bool = True
    contradictory: bool = False
    self_authored: bool = False
    role: str = "held-out-return"


@dataclass(frozen=True)
class ReunifiedAdmissionReceipt:
    """Joint receipt for architecture + data + topology under unified admission."""

    system_id: str
    benchmark_id: str
    episode_id: str
    architecture: OpenArchitectureCarrier
    modalities: tuple[str, ...]
    operation_admission: Admission
    topology_resolution: Resolution
    verification_status: ClosureVerificationStatus
    write_back_allowed: bool
    authoritative: bool
    shadows_present_noncertifying: bool
    learned_claim_status: str
    data_admission_status: str
    joint_arm_status: str
    reason: str
    reunification_digest: str
    turn_unity_digest: str
    verification_digest: str
    goel_operator_status: str | None = None
    goel_quantum_claim: str | None = None
    dual_kakeya_goel_status: str | None = None
    goel_operator_digest: str | None = None
    dual_digest: str | None = None

def probe_weights_available(system: Mapping[str, Any], *, cache_roots: Iterable[Path] | None = None) -> bool:
    """Detect whether open weights appear locally without downloading."""

    system_id = str(system.get("id", ""))
    if system_id == "bio-closure-independent":
        return True
    if not system.get("open_weights", False):
        return system_id.startswith("bio-closure")

    needles: list[str] = []
    if system.get("model_id"):
        needles.append(str(system["model_id"]).replace("/", "--").lower())
        needles.append(str(system["model_id"]).split("/")[-1].lower())
    if system.get("model_name"):
        needles.append(str(system["model_name"]).lower().replace("_", "-"))
    family = str(system.get("family", "")).lower()
    if family:
        needles.append(family)

    roots = list(cache_roots or [])
    if not roots:
        home = Path.home()
        roots = [
            home / ".cache" / "huggingface" / "hub",
            Path("/tmp/hf-cache"),
        ]

    for root in roots:
        if not root.exists():
            continue
        names = {p.name.lower() for p in root.iterdir()} if root.is_dir() else set()
        for needle in needles:
            if any(needle in name for name in names):
                return True
    return False


def architecture_from_system(
    system: Mapping[str, Any],
    *,
    weights_available: bool | None = None,
) -> OpenArchitectureCarrier:
    available = (
        probe_weights_available(system)
        if weights_available is None
        else weights_available
    )
    system_id = str(system["id"])
    if system_id == "bio-closure-independent":
        mode = "independent_kernel"
    elif system_id.startswith("rnd1"):
        mode = "language_hybrid_receipt" if available else "open_weights_absent"
    elif available:
        mode = "open_weights_present"
    else:
        mode = "open_weights_absent"

    payload = {
        "system_id": system_id,
        "family": system.get("family"),
        "adapter": system.get("adapter"),
        "model_id": system.get("model_id"),
        "model_name": system.get("model_name"),
        "repository": system.get("repository"),
        "dataset": system.get("dataset"),
        "proposal_mode": mode,
        "weights_available": available,
    }
    return OpenArchitectureCarrier(
        system_id=system_id,
        family=str(system.get("family", "unknown")),
        biological_native=bool(system.get("biological_native", False)),
        open_weights=bool(system.get("open_weights", False)),
        weights_available=available,
        proposal_mode=mode,
        architecture_digest=stable_digest(payload),
        representation_shadow={
            "epistemic_status": system.get("epistemic_status"),
            "availability": system.get("availability"),
            "role": system.get("role"),
        },
    )


def episode_from_record(record: Mapping[str, Any]) -> ReturnUnifiedEpisodeSpec:
    biological = BiologicalEpisode(
        modalities={k: dict(v) for k, v in record["modalities"].items()},
        shared_relation=str(record["shared_relation"]),
        openings=tuple(record.get("openings") or ()),
        axiometric_shadows=dict(record.get("axiometric_shadows") or {}),
    )
    biological.validate()
    return ReturnUnifiedEpisodeSpec(
        episode_id=str(record["episode_id"]),
        benchmark_id=str(record["benchmark_id"]),
        biological=biological,
        source_observation=record["source_observation"],
        legal_actions=tuple(record["legal_actions"]),
        returned_observation=record["returned_observation"],
        next_legal_actions=tuple(record["next_legal_actions"]),
        independent=bool(record.get("independent", True)),
        contradictory=bool(record.get("contradictory", False)),
        self_authored=bool(record.get("self_authored", False)),
        role=str(record.get("role", "held-out-return")),
    )


def load_finite_bio_episodes(path: Path) -> list[ReturnUnifiedEpisodeSpec]:
    import json

    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return [episode_from_record(row) for row in data["episodes"]]


def _verification_topology_for_episode(
    episode: ReturnUnifiedEpisodeSpec,
    architecture: OpenArchitectureCarrier,
) -> VerificationTopology:
    cycle = {
        "path": [
            "local_proposal",
            "developmental_ecological_propagation",
            "transformed_return",
            "resolution",
        ],
        "shared_relation": episode.biological.shared_relation,
        "modalities": sorted(episode.biological.modalities),
    }
    # Encode/eval layers must coincide for topology admission; architecture
    # identity is carried in ball/hair perspectives, not as topos mismatch.
    topos = {
        "relation": episode.biological.shared_relation,
        "episode": episode.episode_id,
        "benchmark": episode.benchmark_id,
    }
    openings = list(episode.biological.openings) or ["next-return-layer"]
    return VerificationTopology(
        topology_id=f"return-unified:{episode.benchmark_id}:{architecture.system_id}",
        basis_cycle=dict(cycle),
        closure_cycle=dict(cycle),
        encoding_topos=dict(topos),
        relation_topos=dict(topos),
        openings=openings,
        ball_perspective={
            "side": "organism_local",
            "architecture": architecture.architecture_digest,
        },
        hair_perspective={
            "side": "environment_return",
            "system_id": architecture.system_id,
        },
    )


def _learned_claim_status(architecture: OpenArchitectureCarrier) -> str:
    if architecture.proposal_mode == "independent_kernel":
        return "KERNEL_EXECUTED"
    if architecture.proposal_mode == "open_weights_absent":
        return "OPEN_WEIGHTS_ABSENT"
    if architecture.proposal_mode == "language_hybrid_receipt":
        return "LANGUAGE_HYBRID_RECEIPT_ONLY"
    if architecture.proposal_mode == "open_weights_present":
        return "OPEN_WEIGHTS_PRESENT_NOT_YET_ADAPTER_EXECUTED"
    return "OPEN"


def _joint_arm_status(
    *,
    architecture: OpenArchitectureCarrier,
    verification: ClosureVerificationReceipt,
) -> str:
    """Joint biological arm closes only when data+topology verify and architecture can execute."""

    if verification.status is ClosureVerificationStatus.REJECTED:
        return "REJECTED"
    data_ok = verification.status is ClosureVerificationStatus.VERIFIED
    if architecture.proposal_mode == "independent_kernel" and data_ok:
        return "VERIFIED"
    if architecture.proposal_mode == "open_weights_absent":
        return "OPEN_ARCHITECTURE_WEIGHTS_ABSENT" if data_ok else "OPEN"
    if architecture.proposal_mode.startswith("open_weights_present"):
        return "OPEN_ADAPTER_EXECUTION" if data_ok else "OPEN"
    if architecture.proposal_mode == "language_hybrid_receipt":
        return "OPEN_NONBIOLOGICAL_LANGUAGE_ARM"
    return "OPEN"


def reunify_episode(
    architecture: OpenArchitectureCarrier,
    episode: ReturnUnifiedEpisodeSpec,
    *,
    loop: UnifiedClosureArchitecturalLoop | None = None,
    axiometry: UnifiedAxiometry | None = None,
) -> ReunifiedAdmissionReceipt:
    """Reunify architecture carrier + biological return into admissible verification."""

    # Force carrier construction so modality separation is checked before admission.
    biological_episode_to_carrier(
        episode.biological,
        gate_id=f"bio:{episode.episode_id}:{architecture.system_id}",
    )
    shadows_present = shadow_cannot_certify(episode.biological.axiometric_shadows)

    model = loop or UnifiedClosureArchitecturalLoop()
    # Architecture identity enters the source observation as a reunified relation,
    # never as a certifying score. Shared-loop runs seal against prior C_t.
    source = {
        "observation": episode.source_observation,
        "architecture": {
            "system_id": architecture.system_id,
            "digest": architecture.architecture_digest,
            "proposal_mode": architecture.proposal_mode,
        },
        "modalities": sorted(episode.biological.modalities),
        "shared_relation": episode.biological.shared_relation,
        "prior_c_t": model.memory.authoritative_digest,
        "admitted_unities_before": len(model.memory.admitted),
    }
    returned = {
        "observation": episode.returned_observation,
        "architecture_digest": architecture.architecture_digest,
        "shared_relation": episode.biological.shared_relation,
    }

    turn: ArchitecturalLoopTurn = model.transact(
        source,
        episode.legal_actions,
        returned,
        episode.next_legal_actions,
        independent=episode.independent,
        self_authored=episode.self_authored,
        contradictory=episode.contradictory,
    )

    topo = _verification_topology_for_episode(episode, architecture)
    topology_receipt: ClosureReceipt = admit_verification_topology(
        axiometry or UnifiedAxiometry(),
        topo,
    )
    verification = verify_closure_operation(turn, topology_receipt)

    learned = _learned_claim_status(architecture)
    data_status = verification.status.value
    joint = _joint_arm_status(architecture=architecture, verification=verification)

    goel_status = None
    goel_quantum = None
    goel_digest = None
    dual_status = None
    dual_digest = None
    modalities = episode.biological.modalities
    if "DNA" in modalities:
        before = goel_state_from_modalities(
            {
                "DNA": modalities["DNA"],
                "environment": modalities.get("environment")
                or {"milieu": "unspecified_pre_return"},
                "returned_consequence": modalities.get("returned_consequence") or {},
            }
        )
        after_env = dict(modalities.get("environment") or {"milieu": "unspecified_post_return"})
        # Returned consequence may update environmental coupling without collapsing DNA.
        after = goel_state_from_modalities(
            {
                "DNA": modalities["DNA"],
                "environment": after_env,
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
        goel_status = goel.status.value
        goel_quantum = goel.quantum_claim
        goel_digest = goel.operator_digest
        # Local Kakeya stand-in: architecture digest as tokenized relative ball
        # (full RND1 connected-return attaches when that arm executes).
        local = TokenizedRelativityBall(
            ball_id=f"kakeya:{architecture.system_id}:{episode.episode_id}",
            occurrences=(
                {
                    "occurrence_id": turn.unity.unity_digest,
                    "token_id": 0,
                    "position": 0,
                    "step": 0,
                    "return_side": "ball",
                    "identity_is_not_token": True,
                    "architecture": architecture.system_id,
                },
            ),
            return_side="ball",
            contacts=(
                f"arch:{architecture.architecture_digest[:12]}",
                f"goel:{goel.operator_digest[:12]}",
            ),
            radical_numerics_family="tokenized-relativity-reunification",
            ball_digest=stable_digest(
                {
                    "unity": turn.unity.unity_digest,
                    "arch": architecture.architecture_digest,
                }
            ),
        )
        dual = bind_local_kakeya_global_goel(local, goel)
        dual_status = dual.dual_status
        dual_digest = dual.dual_digest

    reason_parts = [verification.reason, f"learned_claim={learned}", f"joint={joint}"]
    if goel_status:
        reason_parts.append(f"goel={goel_status}")
    if dual_status:
        reason_parts.append(f"dual={dual_status}")
    if shadows_present:
        reason_parts.append("axiometric_shadows_present_noncertifying")

    payload = {
        "system": architecture.system_id,
        "benchmark": episode.benchmark_id,
        "episode": episode.episode_id,
        "architecture": architecture.architecture_digest,
        "unity": turn.unity.unity_digest,
        "verification": verification.verification_digest,
        "joint": joint,
        "learned": learned,
        "goel": goel_digest,
        "dual": dual_digest,
    }

    return ReunifiedAdmissionReceipt(
        system_id=architecture.system_id,
        benchmark_id=episode.benchmark_id,
        episode_id=episode.episode_id,
        architecture=architecture,
        modalities=tuple(sorted(episode.biological.modalities)),
        operation_admission=turn.comparison.admission,
        topology_resolution=topology_receipt.resolution,
        verification_status=verification.status,
        write_back_allowed=verification.write_back_allowed,
        authoritative=closure_verification_is_authoritative(verification),
        shadows_present_noncertifying=shadows_present,
        learned_claim_status=learned,
        data_admission_status=data_status,
        joint_arm_status=joint,
        reason="; ".join(reason_parts),
        reunification_digest=stable_digest(payload),
        turn_unity_digest=turn.unity.unity_digest,
        verification_digest=verification.verification_digest,
        goel_operator_status=goel_status,
        goel_quantum_claim=goel_quantum,
        dual_kakeya_goel_status=dual_status,
        goel_operator_digest=goel_digest,
        dual_digest=dual_digest,
    )

def receipt_to_dict(receipt: ReunifiedAdmissionReceipt) -> dict[str, Any]:
    return {
        "system_id": receipt.system_id,
        "benchmark_id": receipt.benchmark_id,
        "episode_id": receipt.episode_id,
        "architecture": {
            "system_id": receipt.architecture.system_id,
            "family": receipt.architecture.family,
            "biological_native": receipt.architecture.biological_native,
            "open_weights": receipt.architecture.open_weights,
            "weights_available": receipt.architecture.weights_available,
            "proposal_mode": receipt.architecture.proposal_mode,
            "architecture_digest": receipt.architecture.architecture_digest,
            "representation_shadow": dict(receipt.architecture.representation_shadow),
        },
        "modalities": list(receipt.modalities),
        "operation_admission": receipt.operation_admission.value,
        "topology_resolution": receipt.topology_resolution.value,
        "verification_status": receipt.verification_status.value,
        "write_back_allowed": receipt.write_back_allowed,
        "authoritative": receipt.authoritative,
        "shadows_present_noncertifying": receipt.shadows_present_noncertifying,
        "learned_claim_status": receipt.learned_claim_status,
        "data_admission_status": receipt.data_admission_status,
        "joint_arm_status": receipt.joint_arm_status,
        "reason": receipt.reason,
        "reunification_digest": receipt.reunification_digest,
        "turn_unity_digest": receipt.turn_unity_digest,
        "verification_digest": receipt.verification_digest,
        "goel_operator_status": receipt.goel_operator_status,
        "goel_quantum_claim": receipt.goel_quantum_claim,
        "dual_kakeya_goel_status": receipt.dual_kakeya_goel_status,
        "goel_operator_digest": receipt.goel_operator_digest,
        "dual_digest": receipt.dual_digest,
    }


__all__ = [
    "OpenArchitectureCarrier",
    "ReturnUnifiedEpisodeSpec",
    "ReunifiedAdmissionReceipt",
    "architecture_from_system",
    "episode_from_record",
    "load_finite_bio_episodes",
    "probe_weights_available",
    "receipt_to_dict",
    "reunify_episode",
]

# Copyright 2026 scarryhott/bio contributors.
"""Biological double-slit as relative verification inside our Closure AGI return.

Goel's biological double-slit is not an external side check. Both slit arms run
as return-unified episodes through our independent closure model; δ_C(Q) is
resolved from the relative residue after independent return — default OPEN
until artifact-excluded interference is witnessed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .biology import BiologicalEpisode
from .digest import digest
from .goel_operator import (
    BiologicalDoubleSlitGate,
    BiologicalDoubleSlitReceipt,
    BiologicalDoubleSlitStatus,
    evaluate_biological_double_slit,
)
from .independent_model import Admission, UnifiedClosureArchitecturalLoop, stable_digest
from .return_unified_runtime import (
    OpenArchitectureCarrier,
    ReunifiedAdmissionReceipt,
    ReturnUnifiedEpisodeSpec,
    architecture_from_system,
    reunify_episode,
)
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


@dataclass(frozen=True)
class DoubleSlitArmReceipt:
    """One slit arm reunified through our closure model."""

    arm_id: str
    path_kind: str
    episode_id: str
    reunify: ReunifiedAdmissionReceipt
    operation_admission: str
    verification_status: str
    write_back_allowed: bool


@dataclass
class DoubleSlitRelativeReturn:
    """Relative verification architecture for δ_C(Q) inside our model return."""

    kind: str = "BIOLOGICAL_DOUBLE_SLIT_RELATIVE_RETURN"
    epistemic_status: str = "RERUNNABLE_FINITE_RELATIVE_VERIFICATION"
    common_bio_token_digest: str = ""
    arm_thermal: DoubleSlitArmReceipt | None = None
    arm_coherence: DoubleSlitArmReceipt | None = None
    relative_residue: dict[str, Any] = field(default_factory=dict)
    relative_architecture: dict[str, Any] = field(default_factory=dict)
    slit_gate: BiologicalDoubleSlitReceipt | None = None
    delta_c_q: str = "OPEN"
    ran_inside_closure_model: bool = True
    reason: str = ""
    return_digest: str = ""

    def to_dict(self) -> dict[str, Any]:
        def arm_dict(arm: DoubleSlitArmReceipt | None) -> dict[str, Any] | None:
            if arm is None:
                return None
            return {
                "arm_id": arm.arm_id,
                "path_kind": arm.path_kind,
                "episode_id": arm.episode_id,
                "operation_admission": arm.operation_admission,
                "verification_status": arm.verification_status,
                "write_back_allowed": arm.write_back_allowed,
                "joint_arm_status": arm.reunify.joint_arm_status,
                "goel_operator_status": arm.reunify.goel_operator_status,
                "topology_resolution": arm.reunify.topology_resolution.value,
            }

        slit = None
        if self.slit_gate is not None:
            slit = {
                "status": self.slit_gate.status.value,
                "delta_c_q": self.slit_gate.delta_c_q,
                "chaitin_global_hair": self.slit_gate.chaitin_global_hair,
                "write_back_allowed": self.slit_gate.write_back_allowed,
                "reason": self.slit_gate.reason,
                "gate_digest": self.slit_gate.gate_digest,
            }
        return {
            "kind": self.kind,
            "epistemic_status": self.epistemic_status,
            "ran_inside_closure_model": self.ran_inside_closure_model,
            "common_bio_token_digest": self.common_bio_token_digest,
            "arm_thermal": arm_dict(self.arm_thermal),
            "arm_coherence": arm_dict(self.arm_coherence),
            "relative_residue": dict(self.relative_residue),
            "relative_architecture": dict(self.relative_architecture),
            "slit_gate": slit,
            "delta_c_q": self.delta_c_q,
            "reason": self.reason,
            "return_digest": self.return_digest,
        }


def _arm_episode(
    *,
    arm_id: str,
    path_kind: str,
    dna: Mapping[str, Any],
    environment: Mapping[str, Any],
    returned_consequence: Mapping[str, Any],
    source_observation: Mapping[str, Any],
    returned_observation: Mapping[str, Any],
    independent: bool = True,
    self_authored: bool = False,
    contradictory: bool = False,
) -> ReturnUnifiedEpisodeSpec:
    modalities = {
        "DNA": dict(dna),
        "environment": dict(environment),
        "returned_consequence": dict(returned_consequence),
    }
    biological = BiologicalEpisode(
        modalities=modalities,
        shared_relation="biological-double-slit-relative-return",
        openings=("delta_c_q_interference_layer", "next-control-channel"),
        axiometric_shadows={"coherence_ratio_claim": 1.1, "confidence": 0.9},
    )
    biological.validate()
    return ReturnUnifiedEpisodeSpec(
        episode_id=f"double-slit-{arm_id}",
        benchmark_id="biological-double-slit",
        biological=biological,
        source_observation=dict(source_observation),
        legal_actions=(
            {"act": "read_base", "path": path_kind},
            {"act": "hold"},
        ),
        returned_observation=dict(returned_observation),
        next_legal_actions=({"act": "observe_relative_residue"},),
        independent=independent,
        contradictory=contradictory,
        self_authored=self_authored,
        role="double-slit-relative-arm",
    )


def _wrap_arm(
    arm_id: str,
    path_kind: str,
    receipt: ReunifiedAdmissionReceipt,
) -> DoubleSlitArmReceipt:
    return DoubleSlitArmReceipt(
        arm_id=arm_id,
        path_kind=path_kind,
        episode_id=receipt.episode_id,
        reunify=receipt,
        operation_admission=receipt.operation_admission.value,
        verification_status=receipt.verification_status.value,
        write_back_allowed=receipt.write_back_allowed,
    )


def run_double_slit_relative_return(
    *,
    architecture: OpenArchitectureCarrier | None = None,
    axiometry: UnifiedAxiometry | None = None,
    interference_signature_reported: bool = False,
    thermal_control_excluded: bool = False,
    mechanical_control_excluded: bool = False,
    detector_artifact_excluded: bool = False,
    claimed_coherence_gt_base_read: bool = True,
) -> DoubleSlitRelativeReturn:
    """Run both slit arms through our Closure AGI and resolve δ_C(Q) relatively.

    Thermal path and coherence-candidate path share DNA locus / bio-token identity
    but differ in environmental path presentation. Each arm reunifies independently.
    The relative residue (what does not coincide after return) is the Chaitin
    global-hair candidate for δ_C(Q). Default remains OPEN without artifact-excluded
    independent interference.
    """

    arch = architecture or architecture_from_system(OUR_SYSTEM, weights_available=True)
    ax = axiometry or UnifiedAxiometry()
    dna = {"sequence": "ATGCGTAC", "locus": "synthetic:double_slit", "motor": "polymerase"}

    # Arm L — classical / thermal environmental path (control presentation).
    thermal_ep = _arm_episode(
        arm_id="thermal",
        path_kind="thermal_environmental_path",
        dna=dna,
        environment={
            "milieu": "defined",
            "tension": 0.2,
            "path": "thermal",
            "slit": "L",
        },
        returned_consequence={
            "base_read": "G",
            "path": "thermal",
            "measured": True,
            "interference": False,
        },
        source_observation={
            "DNA": dna["sequence"],
            "path": "thermal",
            "phase": "pre-return",
        },
        returned_observation={
            "DNA": dna["sequence"],
            "path": "thermal",
            "base_read": "G",
            "phase": "post-return",
            "measured": True,
        },
    )

    # Arm R — coherence-candidate path (same DNA, alternate slit presentation).
    # Without witnessed interference + controls, this arm still returns classically;
    # the *relative* architecture is what δ_C(Q) inspects.
    coherence_env = {
        "milieu": "defined",
        "tension": 0.2,
        "path": "coherence_candidate",
        "slit": "R",
        "quantum_carrier": {
            "claim": "tau_coherence_gt_tau_base_read",
            "witnessed": False,
        },
    }
    coherence_ep = _arm_episode(
        arm_id="coherence",
        path_kind="coherence_candidate_path",
        dna=dna,
        environment=coherence_env,
        returned_consequence={
            "base_read": "G",
            "path": "coherence_candidate",
            "measured": True,
            "interference": interference_signature_reported,
        },
        source_observation={
            "DNA": dna["sequence"],
            "path": "coherence_candidate",
            "phase": "pre-return",
        },
        returned_observation={
            "DNA": dna["sequence"],
            "path": "coherence_candidate",
            "base_read": "G",
            "phase": "post-return",
            "measured": True,
            "interference_signature": interference_signature_reported,
        },
    )

    thermal_receipt = reunify_episode(arch, thermal_ep, axiometry=ax)
    coherence_receipt = reunify_episode(arch, coherence_ep, axiometry=ax)
    thermal_arm = _wrap_arm("thermal", "thermal_environmental_path", thermal_receipt)
    coherence_arm = _wrap_arm(
        "coherence", "coherence_candidate_path", coherence_receipt
    )

    bio_token = digest(
        {
            "DNA": dna,
            "relation": "biological-double-slit-relative-return",
            "modalities": ["DNA", "environment", "returned_consequence"],
        }
    )

    # Relative residue under C: path identity differs; base_read may coincide.
    # Coincidence of classical base_read without artifact-excluded interference
    # does not close δ_C(Q) — that would be false collapse into a score.
    relative_residue = {
        "shared_dna_locus": dna["locus"],
        "shared_base_read": (
            thermal_ep.returned_observation.get("base_read")
            == coherence_ep.returned_observation.get("base_read")
        ),
        "path_identity_differs": True,
        "thermal_unity": thermal_receipt.turn_unity_digest,
        "coherence_unity": coherence_receipt.turn_unity_digest,
        "unities_identical": (
            thermal_receipt.turn_unity_digest == coherence_receipt.turn_unity_digest
        ),
        "both_arms_operation_admitted": (
            thermal_receipt.operation_admission is Admission.ADMITTED
            and coherence_receipt.operation_admission is Admission.ADMITTED
        ),
        "both_arms_data_verified": (
            thermal_receipt.verification_status is ClosureVerificationStatus.VERIFIED
            and coherence_receipt.verification_status
            is ClosureVerificationStatus.VERIFIED
        ),
        "interference_in_return": interference_signature_reported,
        "controls": {
            "thermal_excluded": thermal_control_excluded,
            "mechanical_excluded": mechanical_control_excluded,
            "detector_excluded": detector_artifact_excluded,
        },
    }

    # Independently returned relative verification requires both arms closed as
    # classical returns *and* a witnessed interference residue with controls.
    independently_returned = bool(
        relative_residue["both_arms_data_verified"]
        and relative_residue["both_arms_operation_admitted"]
        and interference_signature_reported
        and thermal_control_excluded
        and mechanical_control_excluded
        and detector_artifact_excluded
        and not relative_residue["unities_identical"]
    )

    gate = BiologicalDoubleSlitGate(
        bio_token_digest=bio_token,
        dna_locus=dna,
        environment={"slits": ["L_thermal", "R_coherence"], "tension": 0.2},
        claimed_coherence_gt_base_read=claimed_coherence_gt_base_read,
        interference_signature_reported=interference_signature_reported,
        thermal_control_excluded=thermal_control_excluded,
        mechanical_control_excluded=mechanical_control_excluded,
        detector_artifact_excluded=detector_artifact_excluded,
        independently_returned=independently_returned,
    )
    slit = evaluate_biological_double_slit(gate)

    relative_architecture = {
        "verification_kind": "relative_two_arm_return_inside_closure_model",
        "model": "closure.independent_model:UnifiedClosureArchitecturalLoop",
        "owner": "ours",
        "not_external_side_check": True,
        "arms": ["thermal_environmental_path", "coherence_candidate_path"],
        "global_hair": "goel_chaitin_delta_c_q",
        "local_ball": "bio_token_kakeya",
        "admission_rule": (
            "δ_C(Q) admits only when relative interference residue returns "
            "independently with thermal/mechanical/detector controls excluded"
        ),
        "default": "OPEN",
        "contrast": (
            "Existing models would score coherence; this architecture runs both "
            "paths as returns and leaves Q open without witnessed relative residue"
        ),
    }

    reason = (
        f"relative return inside our closure model: "
        f"thermal={thermal_arm.verification_status}, "
        f"coherence={coherence_arm.verification_status}; "
        f"{slit.reason}"
    )
    payload = {
        "bio_token": bio_token,
        "thermal": thermal_receipt.reunification_digest,
        "coherence": coherence_receipt.reunification_digest,
        "residue": relative_residue,
        "delta": slit.delta_c_q,
        "status": slit.status.value,
    }
    return DoubleSlitRelativeReturn(
        common_bio_token_digest=bio_token,
        arm_thermal=thermal_arm,
        arm_coherence=coherence_arm,
        relative_residue=relative_residue,
        relative_architecture=relative_architecture,
        slit_gate=slit,
        delta_c_q=slit.delta_c_q,
        ran_inside_closure_model=True,
        reason=reason,
        return_digest=stable_digest(payload),
    )


__all__ = [
    "DoubleSlitArmReceipt",
    "DoubleSlitRelativeReturn",
    "run_double_slit_relative_return",
]

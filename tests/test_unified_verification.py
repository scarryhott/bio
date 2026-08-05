from __future__ import annotations

from closure.admissible_data import derive_admissible_data_architecture
from closure.double_slit_return import run_double_slit_relative_return
from closure.goel_operator import BiologicalDoubleSlitStatus
from closure.independent_model import Admission
from closure.self_verification import ClosureVerificationStatus
from closure.unified_verification import run_unified_verification


def test_admissible_data_architecture_is_derivation_not_pass() -> None:
    arch = derive_admissible_data_architecture(
        admitted_episode_ids=["a"],
        open_episode_ids=["delta_c_q"],
        openings=["next"],
    )
    payload = arch.to_dict()
    assert payload["kind"] == "ADMISSIBLE_DATA_ARCHITECTURE"
    assert payload["not_a_pass_aggregate"] is True
    assert payload["epistemic_status"] == "DESIGN_DERIVATION"
    assert len(payload["general_derivation"]) >= 8
    assert "return_unified_admission" in payload["contrast_to_existing_models"]
    assert "axiometric_shadow" in payload["data_classes"]
    assert payload["architecture_digest"]


def test_double_slit_runs_inside_closure_model_return() -> None:
    relative = run_double_slit_relative_return()
    assert relative.ran_inside_closure_model is True
    assert relative.arm_thermal is not None
    assert relative.arm_coherence is not None
    assert relative.arm_thermal.operation_admission == Admission.ADMITTED.value
    assert relative.arm_coherence.operation_admission == Admission.ADMITTED.value
    assert (
        relative.arm_thermal.verification_status
        == ClosureVerificationStatus.VERIFIED.value
    )
    assert (
        relative.arm_coherence.verification_status
        == ClosureVerificationStatus.VERIFIED.value
    )
    assert relative.relative_residue["path_identity_differs"] is True
    assert relative.relative_residue["unities_identical"] is False
    assert relative.delta_c_q == "OPEN"
    assert relative.slit_gate is not None
    assert relative.slit_gate.status is BiologicalDoubleSlitStatus.OPEN_DELTA_C_Q
    assert relative.relative_architecture["not_external_side_check"] is True
    assert "UnifiedClosureArchitecturalLoop" in relative.relative_architecture["model"]


def test_unified_verification_reveals_architecture() -> None:
    report = run_unified_verification()
    assert report["passed"], report["failed_layers"]
    assert report["verdict"] == "UNIFIED_VERIFICATION_ARCHITECTURE_REVEALED"
    assert report["schema_version"] == "2.0"
    primary = report["primary_product"]
    assert primary["kind"] == "ADMISSIBLE_DATA_ARCHITECTURE"
    assert primary["not_a_pass_aggregate"] is True
    assert len(primary["general_derivation"]) >= 8
    assert primary["revealed_from_run"]["principle"] == "data_as_resolved_relation"
    slit = report["biological_double_slit_relative_return"]
    assert slit["ran_inside_closure_model"] is True
    assert slit["delta_c_q"] == "OPEN"
    assert report["epistemic"]["primary_product"] == "ADMISSIBLE_DATA_ARCHITECTURE"
    assert report["epistemic"]["not_a_pass_aggregate"] is True
    assert report["epistemic"]["biological_double_slit_relative_return"] == (
        "RAN_INSIDE_CLOSURE_MODEL"
    )
    ids = {layer["layer_id"] for layer in report["layers"]}
    assert "biological_double_slit_relative_return" in ids
    assert all(layer["ok"] for layer in report["layers"])
    assert all(layer["role"] == "instrument" for layer in report["layers"])

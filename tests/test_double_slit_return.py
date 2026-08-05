from __future__ import annotations

from closure.double_slit_return import run_double_slit_relative_return
from closure.goel_operator import BiologicalDoubleSlitStatus


def test_interference_without_controls_stays_open_inside_model() -> None:
    relative = run_double_slit_relative_return(
        interference_signature_reported=True,
        thermal_control_excluded=False,
    )
    assert relative.ran_inside_closure_model is True
    assert relative.delta_c_q == "OPEN"
    assert relative.slit_gate is not None
    assert relative.slit_gate.status is BiologicalDoubleSlitStatus.OPEN_MISSING_CONTROLS


def test_relative_architecture_contrasts_scoring_models() -> None:
    relative = run_double_slit_relative_return()
    arch = relative.relative_architecture
    assert arch["verification_kind"] == "relative_two_arm_return_inside_closure_model"
    assert "Existing models would score coherence" in arch["contrast"]
    assert arch["default"] == "OPEN"

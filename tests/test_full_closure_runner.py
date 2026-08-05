from __future__ import annotations

from benchmarks.run_full_closure import run_full_closure


def test_full_closure_reunifies_suite_arms() -> None:
    report = run_full_closure()
    assert report["receipt_count"] >= 20
    assert report["kernel_positive_verified"] == 5
    assert report["joint_arm_status_counts"]["VERIFIED"] == 5
    assert report["joint_arm_status_counts"]["OPEN_ARCHITECTURE_WEIGHTS_ABSENT"] >= 1
    assert report["verification_status_counts"]["VERIFIED"] >= 5
    assert report["epistemic"]["finite_kernel_data_topology_reunification"] == "MEASURED"
    assert report["epistemic"]["full_biological_unification_agi_execution"] == "OPEN"

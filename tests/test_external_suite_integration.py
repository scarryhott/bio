from __future__ import annotations

from closure.external_suite import run_external_suite
from closure.our_closure_verify import verify_our_closure


def test_external_suite_requires_and_passes_our_gate() -> None:
    gate = verify_our_closure()
    assert gate.passed

    report = run_external_suite()
    assert report["passed"], report["summary"]["failed"]
    assert report["verdict"] == "EXTERNAL_SUITE_INTEGRATED"
    assert report["ownership"]["rnd1_is_our_model"] is False
    assert report["epistemic"]["omnii"] == "REPORTED_ONLY"
    assert report["epistemic"]["biological_three_arm_result"] == "OPEN"

    check_ids = {c["check_id"] for c in report["checks"]}
    assert "our_closure_gate" in check_ids
    assert "rnd1_upstream_manifest" in check_ids
    assert "rnd1_mock_sampler_hooks" in check_ids
    assert "paper_architecture_data_layer" in check_ids
    assert report["ownership"]["external_is_not_weights_only"] is True
    assert report["epistemic"]["external_stack"] == "PAPERS_PLUS_DATA_PLUS_OPTIONAL_WEIGHTS"
    assert "opengenome2" in report["paper_data_layer"]["datasets"]
    assert "goel-dna-environment-motor" in report["paper_data_layer"]["paper_architectures"]

    external = [r for r in report["receipts"] if r["system_id"] != "bio-closure-independent"]
    assert external
    assert not any(r.get("learned_claim_status") == "KERNEL_EXECUTED" for r in external)

    omnii = report["omnii_reported_rows"]
    assert omnii
    assert all(row["status"] == "REPORTED_ONLY_NOT_RERUN" for row in omnii)


def test_evo_without_weights_stays_open_joint() -> None:
    report = run_external_suite(include_nonbiological=False, include_reported=False)
    evo = [
        r
        for r in report["receipts"]
        if r["system_id"].startswith("evo") and "open-self" not in r["episode_id"]
    ]
    assert evo
    for row in evo:
        if not row.get("weights_available_probed"):
            assert row["joint_arm_status"] in {
                "OPEN_ARCHITECTURE_WEIGHTS_ABSENT",
                "OPEN",
            }

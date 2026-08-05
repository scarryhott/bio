from __future__ import annotations

from closure.our_closure_verify import report_to_dict, verify_our_closure


def test_our_closure_reunified_and_verified() -> None:
    report = verify_our_closure()
    assert report.ownership_ok
    assert report.passed, report.summary["failed"]
    assert report.verdict == "OUR_CLOSURE_REUNIFIED_VERIFIED"
    payload = report_to_dict(report)
    assert payload["summary"]["external_architectures_deferred"] is True
    assert all(c["ok"] for c in payload["checks"])
    # Only our kernel episodes — no evo/rnd1 system ids in receipts
    assert all(r["system_id"] == "bio-closure-independent" for r in payload["episode_receipts"])
    assert any(r["joint_arm_status"] == "VERIFIED" for r in payload["episode_receipts"])
    assert any(r["verification_status"] == "OPEN" for r in payload["episode_receipts"])

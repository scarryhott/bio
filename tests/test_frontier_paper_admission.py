from __future__ import annotations

from closure.frontier_paper_admission import (
    frontier_claims,
    load_frontier_catalog,
    run_frontier_paper_admission,
)


def test_programme_priority_is_our_closure_vs_frontier_not_rnd1() -> None:
    catalog = load_frontier_catalog()
    priority = catalog["programme_priority"]
    assert priority["primary"] == "our_closure_verification_admission_vs_frontier_paper_results"
    assert priority["rnd1_30b_role"] == "FINITE_AI_SUBSTRATE_TEST_NOT_BIO_CLOSURE"
    claims = frontier_claims(catalog)
    rnd1 = next(c for c in claims if c.claim_id == "rnd1-30b-finite-ai-substrate-test")
    assert rnd1.our_admission_role == "FINITE_AI_TEST_NOT_BIO_CLOSURE"
    assert any(c.claim_id == "evo2-nature-2026-opengenome2" for c in claims)
    assert any(c.claim_id == "omnii-health-preview-reported" for c in claims)
    assert any(c.claim_id == "goel-pnas-dna-environment-motor" for c in claims)


def test_frontier_paper_admission_primary_run() -> None:
    report = run_frontier_paper_admission(include_open_data=True)
    assert report["passed"], report["verdict"]
    assert report["verdict"] == "OUR_CLOSURE_ADMISSION_VS_FRONTIER_PAPERS_MEASURED"
    assert report["epistemic"]["primary_goal"] == (
        "our_closure_verification_admission_vs_frontier_paper_results"
    )
    assert report["epistemic"]["rnd1_30b_is_bio_closure"] is False
    assert report["rnd1_30b_finite_ai_test"]["not_bio_closure"] is True
    assert report["our_closure_gate"]["passed"] is True
    # Frontier scores never certify
    for row in report["frontier_claims"]:
        assert row["scores_certify_closure"] is False

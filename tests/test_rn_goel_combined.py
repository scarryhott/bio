from __future__ import annotations

from closure.biology import BiologicalEpisode
from closure.return_unified_runtime import ReturnUnifiedEpisodeSpec
from closure.rn_goel_combined import combine_episode, run_rnd1_open_proposal, run_rn_goel_combined
from closure.rn_open_surface import RN_OPEN_REPOS, inventory_rn_open_surface


def _dna_episode() -> ReturnUnifiedEpisodeSpec:
    biological = BiologicalEpisode(
        modalities={
            "DNA": {"sequence": "ATGCGTAC", "locus": "test"},
            "environment": {"milieu": "defined", "tension_pN": 6},
            "returned_consequence": {"viability": "maintained", "measured": True},
        },
        shared_relation="rn-goel-combined-test",
        openings=("next",),
    )
    biological.validate()
    return ReturnUnifiedEpisodeSpec(
        episode_id="rn-goel-test-001",
        benchmark_id="sequence-likelihood",
        biological=biological,
        source_observation={"DNA": "ATGCGTAC", "phase": "pre"},
        legal_actions=({"act": "score_context"},),
        returned_observation={"DNA": "ATGCGTAC", "measured_viability": "maintained"},
        next_legal_actions=({"act": "observe"},),
        independent=True,
    )


def test_rn_open_repos_include_rnd1_spear_dinfer() -> None:
    ids = {r["id"] for r in RN_OPEN_REPOS}
    assert {"RND1", "spear", "dInfer"} <= ids


def test_rnd1_open_proposal_runs_mock_under_hooks() -> None:
    proposal = run_rnd1_open_proposal(closure_mode="full")
    assert proposal.mode == "open_code_mock_sampler"
    assert proposal.ownership == "radical-numerics-external"
    assert proposal.trace_steps > 0
    assert proposal.sequences_digest
    assert proposal.weights_used is False


def test_combine_episode_binds_goel_and_rn() -> None:
    proposal = run_rnd1_open_proposal()
    receipt = combine_episode(_dna_episode(), rnd1_proposal=proposal)
    assert receipt.our_receipt["joint_arm_status"] == "VERIFIED"
    assert receipt.goel_operator_status == "ADMITTED_GLOBAL_HAIR"
    assert receipt.goel_mode_from_wuite == "polymerase"
    assert receipt.dual_status == "DUAL_CLOSED_TO_OPENING"
    assert receipt.combined_status == "COMBINED_OUR_VERIFIED_RN_PRESENT_GOEL_BOUND"
    assert receipt.rnd1_proposal["mode"] == "open_code_mock_sampler"


def test_run_rn_goel_combined_offline_surface(monkeypatch) -> None:
    # Avoid network in unit test — use cached/no-fetch inventory.
    surface = inventory_rn_open_surface(fetch=False)
    assert surface.ownership["rnd1_is_our_model"] is False
    report = run_rn_goel_combined([_dna_episode()], fetch_rn_surface=False)
    assert report["our_kernel_verified"] == 1
    assert report["goel_bound_episodes"] == 1
    assert report["epistemic"]["rnd1_is_our_model"] is False
    assert report["epistemic"]["goel_subsumed_into_black_mirror"] is False
    assert "RND1" in report["stack"]["radical_numerics_open"]["repos"]
    assert report["stack"]["goel_paper_logic"]["subsumption"] is False

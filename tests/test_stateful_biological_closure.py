from __future__ import annotations

from closure.biology import BiologicalEpisode
from closure.dataset_adapters import load_all_open_episodes
from closure.independent_model import ORIGINLESS_GENESIS
from closure.return_unified_runtime import ReturnUnifiedEpisodeSpec, load_finite_bio_episodes
from closure.stateful_biological_closure import (
    StatefulBiologicalClosure,
    order_episodes_for_stateful_run,
    run_stateful_biological_closure,
)


def _ep(episode_id: str, benchmark_id: str, role: str, *, dna: str = "ATGC") -> ReturnUnifiedEpisodeSpec:
    biological = BiologicalEpisode(
        modalities={
            "DNA": {"sequence": dna, "locus": episode_id},
            "environment": {"milieu": "defined"},
            "returned_consequence": {"measured": True, "label": episode_id},
        },
        shared_relation=f"rel-{episode_id}",
        openings=("next",),
    )
    biological.validate()
    return ReturnUnifiedEpisodeSpec(
        episode_id=episode_id,
        benchmark_id=benchmark_id,
        biological=biological,
        source_observation={"id": episode_id, "phase": "pre"},
        legal_actions=({"act": "observe"}, {"act": "hold"}),
        returned_observation={"id": episode_id, "phase": "post", "measured": True},
        next_legal_actions=({"act": "observe"},),
        independent=True,
        role=role,
    )


def test_c_t_carries_across_episodes_not_reset() -> None:
    runtime = StatefulBiologicalClosure()
    e1 = _ep("traitgym-000", "variant-effect", "open-dataset:traitgym", dna="AAAA")
    e2 = _ep("clinvar-000", "variant-effect", "open-dataset:clinvar", dna="CCCC")
    s1 = runtime.run_episode(e1)
    s2 = runtime.run_episode(e2)
    assert s1.c_before == ORIGINLESS_GENESIS
    assert s1.c_after != ORIGINLESS_GENESIS
    assert s2.c_before == s1.c_after
    assert s2.carried_prior is True
    assert s2.admitted_count_before >= 1
    assert runtime.chain_is_stateful()


def test_fresh_loop_each_call_is_not_stateful_aggregate() -> None:
    """Contrast: separate reunify without shared loop resets C_0 each time."""

    from closure.return_unified_runtime import architecture_from_system, reunify_episode
    from closure.stateful_biological_closure import OUR_SYSTEM

    arch = architecture_from_system(OUR_SYSTEM, weights_available=True)
    e1 = _ep("a", "variant-effect", "open-dataset:traitgym", dna="AAAA")
    e2 = _ep("b", "variant-effect", "open-dataset:clinvar", dna="CCCC")
    # Independent loops — seals do not share C_t.
    r1 = reunify_episode(arch, e1)  # new loop inside
    r2 = reunify_episode(arch, e2)  # another new loop
    assert r1.turn_unity_digest != r2.turn_unity_digest


def test_cross_dataset_hypotheses_open_until_return() -> None:
    runtime = StatefulBiologicalClosure()
    runtime.run_all(
        [
            _ep("traitgym-000", "variant-effect", "open-dataset:traitgym"),
            _ep("clinvar-000", "variant-effect", "open-dataset:clinvar"),
            _ep("proteingym-000", "variant-effect", "open-dataset:proteingym"),
            _ep("rnagym-000", "rna-fitness", "open-dataset:rnagym"),
            _ep("opengenome2-seq-000", "sequence-likelihood", "open-dataset:opengenome2"),
        ]
    )
    hyps = runtime.derive_cross_dataset_hypotheses()
    assert hyps
    assert all(h.delta_c == "OPEN" for h in hyps)
    kinds = {h.hypothesis_id.split("-")[0] for h in hyps}
    # at least joint variant and nrr bundle styles present
    assert any("joint_variant" in h.hypothesis_id for h in hyps)
    assert any("nrr-bundle" in h.hypothesis_id for h in hyps)
    report = runtime.report()
    assert report["stateful_chain"] is True
    assert report["epistemic"]["not_aggregate_of_separate_closes"] is True
    assert report["epistemic"]["new_resolutions_empirically_closed"] is False


def test_run_stateful_on_finite_and_open_cache() -> None:
    from pathlib import Path

    finite_path = Path(__file__).resolve().parents[1] / "benchmarks" / "finite_bio_returns.json"
    episodes = list(load_finite_bio_episodes(finite_path))
    open_eps = load_all_open_episodes()
    if open_eps:
        episodes.extend(open_eps)
    report = run_stateful_biological_closure(episodes)
    assert report["passed"], report["verdict"]
    assert report["verdict"] == "STATEFUL_BIOLOGICAL_CLOSURE_CHAIN_MEASURED"
    assert report["stateful_chain"] is True
    assert report["admitted_unities"] >= 1
    # Chain continuity on steps
    steps = report["steps"]
    for i in range(1, len(steps)):
        assert steps[i]["c_before"] == steps[i - 1]["c_after"]


def test_order_puts_finite_before_open_datasets() -> None:
    eps = [
        _ep("rnagym-000", "rna-fitness", "open-dataset:rnagym"),
        _ep("seq-lik-001", "sequence-likelihood", "held-out-return"),
        _ep("traitgym-000", "variant-effect", "open-dataset:traitgym"),
    ]
    ordered = order_episodes_for_stateful_run(eps)
    assert ordered[0].episode_id == "seq-lik-001"
    assert ordered[1].episode_id == "traitgym-000"
    assert ordered[2].episode_id == "rnagym-000"

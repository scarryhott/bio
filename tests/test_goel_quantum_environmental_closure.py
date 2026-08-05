# Copyright 2026 scarryhott/bio contributors.
from __future__ import annotations

from closure.goel_quantum_environmental_closure import (
    BIO_CLOSURE_LEVELS,
    GOEL_QE_ADMISSIBILITY_CHART,
    bind_episode_quantum_env,
    derive_goel_quantum_environmental_closure,
)
from closure.level6_reciprocal_topology import (
    GaloisPair,
    ReciprocalTopology,
    balanced_hodge_candidate,
    run_reunified_level6,
)
from closure.return_unified_runtime import load_finite_bio_episodes
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODES = ROOT / "benchmarks" / "finite_bio_returns.json"


def test_level6_r6_square_and_unitarity() -> None:
    P = ReciprocalTopology()
    z = GaloisPair(complex(0.7, -1.1), complex(-0.3, 0.8))
    sq = P.level6_square(z)
    assert abs(sq.ball - z.ball) < 1e-10
    assert abs(sq.hair - z.hair) < 1e-10
    x = GaloisPair(complex(0.4, 1.2), complex(-0.7, 0.3))
    y = GaloisPair(complex(-0.2, 0.9), complex(1.3, -0.5))
    assert abs(P.cross_pairing(P.apply(x), P.apply(y)) - P.cross_pairing(x, y)) < 1e-10
    assert P.determinant == 1


def test_level6_reunified_run_verifies_internal() -> None:
    run = run_reunified_level6()
    assert run.internal_closure_hodge_counterexample
    assert run.r6_square_identity
    assert run.intrinsic_unitarity
    assert run.level5_forgets_orientation
    assert run.level6_retains_orientation
    assert run.p2_candidate["hodge_type"] == [2, 2]
    assert run.p2_candidate["total_weight"] == "1"
    assert run.classical_hodge_counterexample.startswith("OPEN")


def test_balanced_hodge_p2_topology_weight() -> None:
    h = balanced_hodge_candidate(2)
    assert h.degree == 4
    assert h.hodge_type == (2, 2)
    assert h.topology_fixed
    assert not h.outside_cycle_map_proved


def test_goel_qe_chart_covers_admissible_stages() -> None:
    assert len(GOEL_QE_ADMISSIBILITY_CHART) == 10
    assert GOEL_QE_ADMISSIBILITY_CHART[0].stage_id == "originless_basis"
    assert GOEL_QE_ADMISSIBILITY_CHART[-1].stage_id == "repartition_next"
    assert any(r.quantum_status_at_stage == "OPEN_unless_witnessed" for r in GOEL_QE_ADMISSIBILITY_CHART)


def test_bio_levels_include_ivi3_and_r6() -> None:
    ids = {row["level_id"] for row in BIO_CLOSURE_LEVELS}
    assert "ivi3_quantum_env" in ids
    assert "level6_r6_return" in ids
    assert "delta_c_q_gate" in ids


def test_bind_dna_env_episode_admits_classical_q_open() -> None:
    episodes = load_finite_bio_episodes(EPISODES)
    dna = next(e for e in episodes if "DNA" in e.biological.modalities)
    binding = bind_episode_quantum_env(dna)
    assert binding.has_dna
    assert binding.r6_square_holds
    assert binding.unitary_pairing_holds
    if binding.has_environment:
        assert binding.classical_hair_admitted
        assert binding.delta_c_q == "OPEN"
        assert binding.quantum_env_closed is False


def test_derive_goel_quantum_environmental_closure() -> None:
    report = derive_goel_quantum_environmental_closure(include_stateful=True)
    assert report["passed"]
    assert report["verdict"] == "GOEL_QUANTUM_ENVIRONMENTAL_CLOSURE_DERIVED"
    assert report["level6_reunified"]["verdict"] == "REUNIFIED_INTERNAL_CLOSURE_HODGE_VERIFIED"
    assert report["summary"]["classical_goel_hair_admitted"] > 0
    assert report["summary"]["quantum_environmental_closed"] == 0
    assert report["summary"]["delta_c_q_open"] > 0
    assert report["epistemic"]["quantum_environmental_empirical"] == "OPEN_DELTA_C_Q"
    assert report["relation"]["R6_squared"] == "id"
    assert len(report["data_admissibility_chart"]) == 10
    assert report["admissible_data_architecture"]["kind"] == "ADMISSIBLE_DATA_ARCHITECTURE"
    assert report["stateful_biological_closure"]["stateful_chain"] is True

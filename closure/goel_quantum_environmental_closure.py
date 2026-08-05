# Copyright 2026 scarryhott/bio contributors.
"""Quantum–environmental closure of the Goel operator via bio Levels + data chart.

Derives — from transcripts + reunified Level-6 axiometry + admissible-data
architecture — how Goel's DNA×environment (±Q) operator closes as global
Chaitin hair under our bio closure:

    DNA motor / bio-token Kakeya  =  z_B   (local ball partition)
    Environment (± quantum)       =  z_H   (global hair curvature)
    Reciprocal topology           P = diag(2, 1/2)
    Level-6 return                R_6 = σ ∘ P,   R_6² = id
    Unitary cross form            ⟨Px,Py⟩_C = ⟨x,y⟩_C

Admissible-data stages chart how Q becomes (or fails to become) identity.
Classical DNA×env hair may admit without witnessed Q; quantum environmental
closure requires independent R_6 return of a witnessed carrier — otherwise
δ_C(Q)=OPEN (biological double-slit gate).

Does not claim classical Chaitin Ω, classical Hodge CE, or empirical
interference closure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from .admissible_data import (
    ADMISSIBLE_DATA_DERIVATION,
    DATA_CLASSES,
    derive_admissible_data_architecture,
)
from .digest import digest
from .goel_operator import (
    BiologicalDoubleSlitGate,
    GoelOperatorStatus,
    TokenizedRelativityBall,
    apply_goel_chaitin_operator,
    bind_local_kakeya_global_goel,
    evaluate_biological_double_slit,
    goel_state_from_modalities,
    programme_role_split,
)
from .independent_model import stable_digest
from .level6_reciprocal_topology import (
    GaloisPair,
    ReciprocalTopology,
    run_reunified_level6,
)
from .return_unified_runtime import (
    ReturnUnifiedEpisodeSpec,
    load_finite_bio_episodes,
)
from .stateful_biological_closure import (
    StatefulBiologicalClosure,
    order_episodes_for_stateful_run,
)

ROOT = Path(__file__).resolve().parents[1]
EPISODES_PATH = ROOT / "benchmarks" / "finite_bio_returns.json"


# ---------------------------------------------------------------------------
# Bio-level chart: IVI / ball–hair / Goel–Q binding
# ---------------------------------------------------------------------------

BIO_CLOSURE_LEVELS: tuple[dict[str, Any], ...] = (
    {
        "level_id": "ivi0_pure_place",
        "name": "IVI-0 Pure Place",
        "goel_role": "pre-DNA / pre-environment — only 0↔∞ dual limits",
        "partition": None,
        "transcript": "docs/transcript_closure/closure_structure_map.json#ivi0",
    },
    {
        "level_id": "ivi1_adjacency",
        "name": "IVI-1 Adjacency",
        "goel_role": "DNA locus adjacent to milieu without forced coupling",
        "partition": "undirected DNA–env contact",
        "transcript": "docs/transcript_closure/closure_structure_map.json#ivi1",
    },
    {
        "level_id": "ivi2_orientation",
        "name": "IVI-2 Orientation",
        "goel_role": "polymerase direction / tension-tuned motor orientation",
        "partition": "directed motor path on DNA",
        "transcript": "docs/transcript_closure/closure_structure_map.json#ivi2",
    },
    {
        "level_id": "ivi3_quantum_env",
        "name": "IVI-3 Triality / quantum–environmental",
        "goel_role": (
            "local non-invertibility + resuperposition on DNA×env; "
            "quantum = partial verification on relations (transcript bridge)"
        ),
        "partition": "z_B ⊕ z_H with possible Q on hair fiber",
        "transcript": "docs/transcript_closure/closure_structure_map.json#quantum",
        "equals": "quantum-gravity axiometry / Goel Q hypothesis locus",
    },
    {
        "level_id": "ball_partition",
        "name": "Local Kakeya bio-token ball (z_B)",
        "goel_role": "DNA template occurrences inside bio-tokens; weight 2",
        "partition": "z_B",
        "topology_weight": "2",
    },
    {
        "level_id": "hair_curvature",
        "name": "Global Chaitin–Goel hair (z_H)",
        "goel_role": "environment ± quantum carrier; weight 1/2",
        "partition": "z_H",
        "topology_weight": "1/2",
    },
    {
        "level_id": "level6_r6_return",
        "name": "Level-6 Galois ball→hair return",
        "goel_role": "R_6 = σ∘P; R_6²=id — quantum-env closure identity",
        "partition": "R_6(z_B, z_H)",
        "identity": "R_6^2 = id",
    },
    {
        "level_id": "delta_c_q_gate",
        "name": "Biological double-slit δ_C(Q)",
        "goel_role": "witnessed interference return or OPEN",
        "partition": "orientation-sensitive Level-6 residue",
        "default": "OPEN",
    },
)


# ---------------------------------------------------------------------------
# Admissible-data chart specialized to Goel quantum–environmental closure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GoelQEChartRow:
    """One row of the data-admissibility chart for Goel Q–env closure."""

    stage_id: str
    admissible_statement: str
    goel_quantum_env_realization: str
    level6_operator: str
    writes_memory: bool
    quantum_status_at_stage: str
    data_class: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "admissible_statement": self.admissible_statement,
            "goel_quantum_env_realization": self.goel_quantum_env_realization,
            "level6_operator": self.level6_operator,
            "writes_memory": self.writes_memory,
            "quantum_status_at_stage": self.quantum_status_at_stage,
            "data_class": self.data_class,
        }


GOEL_QE_ADMISSIBILITY_CHART: tuple[GoelQEChartRow, ...] = (
    GoelQEChartRow(
        "originless_basis",
        ADMISSIBLE_DATA_DERIVATION[0].statement,
        "C_t prior to DNA/env split; Goel motor not yet polarized",
        "C before z_B ⊕ z_H",
        False,
        "not_yet_posed",
        "provisional_observation",
    ),
    GoelQEChartRow(
        "expose_observation_field",
        ADMISSIBLE_DATA_DERIVATION[1].statement,
        "Expose DNA template (ball) and milieu/Q carrier (hair) as candidates",
        "z = z_B ⊕ z_H provisional",
        False,
        "provisional_Q_candidate",
        "provisional_observation",
    ),
    GoelQEChartRow(
        "provisional_transform",
        ADMISSIBLE_DATA_DERIVATION[2].statement,
        "Provisional polymerase act under tension without write-back",
        "P = diag(2, 1/2) weights applied provisionally",
        False,
        "shadow_only",
        "axiometric_shadow",
    ),
    GoelQEChartRow(
        "preserve_pre_return",
        ADMISSIBLE_DATA_DERIVATION[3].statement,
        "Seal pre-return DNA×env relation for non-identical recovery",
        "pre-R_6 sealed relation",
        False,
        "sealed_not_resolved",
        "provisional_observation",
    ),
    GoelQEChartRow(
        "environmental_transform",
        ADMISSIBLE_DATA_DERIVATION[4].statement,
        "Environment transforms motor mode (Goel: DNA=piano, env=fingers)",
        "κ_{1/2} hair curvature on z_H",
        False,
        "env_coupled_classical_path",
        "returned_consequence",
    ),
    GoelQEChartRow(
        "independent_return",
        ADMISSIBLE_DATA_DERIVATION[5].statement,
        "Independent DNA×env return — not polymerase echo",
        "R_6 = σ∘P ball-into-hair",
        False,
        "classical_ok_Q_pending",
        "returned_consequence",
    ),
    GoelQEChartRow(
        "endogenous_topology",
        ADMISSIBLE_DATA_DERIVATION[6].statement,
        "ω_C = i z_B ∧ z_H ∈ H^{1,1}; unitary ⟨·,·⟩_C from return",
        "P(ω_C)=ω_C; R_6(ω_C)=ω_C",
        False,
        "topology_fixed_Q_not_certified",
        "relative_interference_residue",
    ),
    GoelQEChartRow(
        "delta_c_resolution",
        ADMISSIBLE_DATA_DERIVATION[7].statement,
        "δ_C(Q): witnessed interference → admit; else OPEN (double-slit gate)",
        "Level-6 orientation residue vs Level-5 shadow",
        False,
        "OPEN_unless_witnessed",
        "open_candidate",
    ),
    GoelQEChartRow(
        "integrate_resolved_relation",
        ADMISSIBLE_DATA_DERIVATION[8].statement,
        "Admit classical env-coupled hair; Q only if witnessed R_6 return",
        "write-back under dual Close(B) ∧ Close(H_Goel)",
        True,
        "classical_admit_Q_OPEN_default",
        "admitted_memory",
    ),
    GoelQEChartRow(
        "repartition_next",
        ADMISSIBLE_DATA_DERIVATION[9].statement,
        "Repartition next bio-token ball and Goel–Chaitin hair under C_{t+1}",
        "R_6²=id then next opening",
        False,
        "carry_OPEN_Q_forward",
        "open_candidate",
    ),
)


@dataclass
class QuantumEnvEpisodeBinding:
    """One bio episode bound through Level-6 Goel Q–env closure."""

    episode_id: str
    benchmark_id: str
    has_dna: bool
    has_environment: bool
    quantum_claim: str
    goel_status: str | None
    dual_status: str | None
    level6_pair: dict[str, Any]
    r6_square_holds: bool
    unitary_pairing_holds: bool
    delta_c_q: str
    classical_hair_admitted: bool
    quantum_env_closed: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "benchmark_id": self.benchmark_id,
            "has_dna": self.has_dna,
            "has_environment": self.has_environment,
            "quantum_claim": self.quantum_claim,
            "goel_status": self.goel_status,
            "dual_status": self.dual_status,
            "level6_pair": self.level6_pair,
            "r6_square_holds": self.r6_square_holds,
            "unitary_pairing_holds": self.unitary_pairing_holds,
            "delta_c_q": self.delta_c_q,
            "classical_hair_admitted": self.classical_hair_admitted,
            "quantum_env_closed": self.quantum_env_closed,
            "reason": self.reason,
        }


def _complex_from_digest(seed: str, salt: str) -> complex:
    h = digest({"seed": seed, "salt": salt})
    # Map hex digest into a bounded complex presentation (relational, not physics units).
    a = int(h[:8], 16) / 0xFFFFFFFF
    b = int(h[8:16], 16) / 0xFFFFFFFF
    return complex(0.25 + 1.5 * a, -1.25 + 2.0 * b)


def _galois_pair_from_modalities(
    modalities: Mapping[str, Any], episode_id: str
) -> GaloisPair:
    """DNA → ball fiber; environment (+ optional Q) → hair fiber."""

    dna = modalities.get("DNA") or {}
    env = modalities.get("environment") or {}
    q = modalities.get("quantum")
    if q is None and isinstance(env, Mapping):
        q = env.get("quantum_carrier")
    ball = _complex_from_digest(episode_id, f"ball:{stable_digest(dna)}")
    hair_payload = {"env": dict(env) if isinstance(env, Mapping) else env, "q": q}
    hair = _complex_from_digest(episode_id, f"hair:{stable_digest(hair_payload)}")
    return GaloisPair(ball=ball, hair=hair)


def bind_episode_quantum_env(
    episode: ReturnUnifiedEpisodeSpec,
    *,
    topology: ReciprocalTopology | None = None,
) -> QuantumEnvEpisodeBinding:
    """Bind one bio episode to Level-6 Goel quantum–environmental closure."""

    P = topology or ReciprocalTopology()
    modalities = episode.biological.modalities
    has_dna = "DNA" in modalities and bool(modalities["DNA"])
    has_env = "environment" in modalities and bool(modalities["environment"])

    pair = _galois_pair_from_modalities(modalities, episode.episode_id)
    r6sq = P.level6_square(pair)
    r6_ok = abs(r6sq.ball - pair.ball) <= 1e-9 and abs(r6sq.hair - pair.hair) <= 1e-9
    # Unitary check on this pair against a fixed partner probe.
    probe = GaloisPair(complex(0.5, 0.2), complex(-0.3, 0.7))
    unitary_ok = abs(
        P.cross_pairing(P.apply(pair), P.apply(probe))
        - P.cross_pairing(pair, probe)
    ) <= 1e-9

    goel_status = None
    dual_status = None
    quantum_claim = "NO_QUANTUM_CARRIER_ASSERTED"
    classical_admit = False
    delta_c_q = "OPEN"
    quantum_closed = False
    reason = "insufficient DNA×env modalities for Goel hair"

    if has_dna and has_env:
        before = goel_state_from_modalities(
            {
                "DNA": modalities["DNA"],
                "environment": modalities.get("environment") or {},
                "quantum": modalities.get("quantum") or {},
            }
        )
        after_env = dict(modalities.get("environment") or {})
        after = goel_state_from_modalities(
            {
                "DNA": modalities["DNA"],
                "environment": after_env,
                "returned_consequence": modalities.get("returned_consequence") or {},
                "quantum": modalities.get("quantum") or {},
            }
        )
        goel = apply_goel_chaitin_operator(
            before,
            after,
            independent=episode.independent,
            self_authored=episode.self_authored,
            contradictory=episode.contradictory,
        )
        goel_status = goel.status.value
        quantum_claim = goel.quantum_claim
        classical_admit = (
            goel.status is GoelOperatorStatus.ADMITTED_GLOBAL_HAIR
            and goel.write_back_allowed
        )

        local = TokenizedRelativityBall(
            ball_id=f"qe:{episode.episode_id}",
            occurrences=(
                {
                    "occurrence_id": episode.episode_id,
                    "token_id": 0,
                    "position": 0,
                    "step": 0,
                    "return_side": "ball",
                    "identity_is_not_token": True,
                },
            ),
            return_side="ball",
            contacts=("dna", "env"),
            ball_digest=digest({"ep": episode.episode_id, "ball": pair.ball.real}),
        )
        dual = bind_local_kakeya_global_goel(local, goel)
        dual_status = dual.dual_status

        # Quantum environmental closure: witnessed Q carrier + classical hair + R6.
        q_witnessed = quantum_claim == "QUANTUM_CARRIER_WITNESSED_EMPIRICAL"
        slit = evaluate_biological_double_slit(
            BiologicalDoubleSlitGate(
                bio_token_digest=local.ball_digest,
                dna_locus=dict(modalities["DNA"]),
                environment=dict(after_env),
                claimed_coherence_gt_base_read=q_witnessed,
                interference_signature_reported=q_witnessed,
                thermal_control_excluded=q_witnessed,
                mechanical_control_excluded=q_witnessed,
                detector_artifact_excluded=q_witnessed,
                independently_returned=q_witnessed and episode.independent,
            )
        )
        delta_c_q = slit.delta_c_q
        quantum_closed = (
            q_witnessed
            and classical_admit
            and r6_ok
            and unitary_ok
            and slit.write_back_allowed
        )
        if quantum_closed:
            reason = "quantum-environmental R_6 return admitted (witnessed Q)"
        elif classical_admit and not q_witnessed:
            reason = (
                "classical Goel DNA×env hair admitted under Level-6 unitary form; "
                "δ_C(Q)=OPEN — quantum environmental closure not yet witnessed"
            )
        else:
            reason = f"goel={goel_status}; dual={dual_status}; δ_C(Q)={delta_c_q}"

    return QuantumEnvEpisodeBinding(
        episode_id=episode.episode_id,
        benchmark_id=episode.benchmark_id,
        has_dna=has_dna,
        has_environment=has_env,
        quantum_claim=quantum_claim,
        goel_status=goel_status,
        dual_status=dual_status,
        level6_pair={
            "ball": [pair.ball.real, pair.ball.imag],
            "hair": [pair.hair.real, pair.hair.imag],
            "P": ["2", "1/2"],
            "R6": "sigma o P",
        },
        r6_square_holds=r6_ok,
        unitary_pairing_holds=unitary_ok,
        delta_c_q=delta_c_q,
        classical_hair_admitted=classical_admit,
        quantum_env_closed=quantum_closed,
        reason=reason,
    )


def derive_goel_quantum_environmental_closure(
    episodes: Sequence[ReturnUnifiedEpisodeSpec] | None = None,
    *,
    include_stateful: bool = True,
) -> dict[str, Any]:
    """Full derivation: bio levels + admissibility chart + Level-6 + Goel Q-env."""

    level6 = run_reunified_level6()

    if episodes is None:
        episodes = load_finite_bio_episodes(EPISODES_PATH)

    ordered = order_episodes_for_stateful_run(list(episodes))
    bindings = [bind_episode_quantum_env(ep) for ep in ordered]

    # Prefer DNA×env episodes for chart instantiation.
    dna_env = [b for b in bindings if b.has_dna and b.has_environment]
    classical_admitted = sum(1 for b in dna_env if b.classical_hair_admitted)
    quantum_closed = sum(1 for b in dna_env if b.quantum_env_closed)
    open_q = sum(1 for b in dna_env if b.delta_c_q == "OPEN")

    stateful_report = None
    if include_stateful:
        state = StatefulBiologicalClosure()
        state.run_all(ordered)
        # Seal Goel Q-env hypotheses into the stateful ledger as OPEN candidates.
        for b in dna_env:
            if b.classical_hair_admitted and b.delta_c_q == "OPEN":
                state.open_candidates.append(
                    {
                        "kind": "goel_quantum_environmental",
                        "episode_id": b.episode_id,
                        "delta_c_q": "OPEN",
                        "proposition": (
                            "Level-6 unitary DNA×env hair admitted; quantum "
                            "environmental carrier unresolved pending independent "
                            "interference return"
                        ),
                    }
                )
        stateful_report = {
            "stateful_chain": state.chain_is_stateful(),
            "final_c_t": state.c_t,
            "admitted_unities": state.admitted_count,
            "goel_qe_open_candidates": sum(
                1
                for c in state.open_candidates
                if c.get("kind") == "goel_quantum_environmental"
            ),
        }

    admitted_ids = [b.episode_id for b in dna_env if b.classical_hair_admitted]
    open_ids = [b.episode_id for b in dna_env if b.delta_c_q == "OPEN"]
    open_ids.append("delta_c_q_goel_quantum_environmental")

    data_arch = derive_admissible_data_architecture(
        admitted_episode_ids=admitted_ids,
        open_episode_ids=open_ids,
        openings=[
            "next-environmental-coupling",
            "delta_c_q_biological_double_slit",
            "goel_quantum_environmental_R6_return",
        ],
        ownership={
            "closure_agi": "ours_transcript_ivi_nrr",
            "goel_programme": "parallel_not_subsumption",
            "level6": "reunified_reciprocal_topology",
            "rnd1_is_our_model": False,
        },
    )

    roles = programme_role_split()

    # Core derived relation for quantum environmental closure.
    derived_relation = {
        "z": "z_B ⊕ z_H",
        "z_B": "DNA / bio-token Kakeya local ball (weight 2)",
        "z_H": "environment ± quantum carrier as global Chaitin hair (weight 1/2)",
        "P": "diag(2, 1/2)",
        "R6": "sigma o P",
        "R6_squared": "id",
        "unitary": "⟨P x, P y⟩_C = ⟨x, y⟩_C",
        "omega_C": "i z_B ∧ z_H ∈ H^{1,1}, fixed by P and R6",
        "classical_goel_hair": "ADMITTED when DNA×env independently returned",
        "quantum_environmental_closure": (
            "requires witnessed Q carrier through R6 + artifact-excluded "
            "interference; default δ_C(Q)=OPEN"
        ),
        "goel_binding": "DNA=piano, environment=fingers; Q not free identity upgrade",
    }

    internal_ok = bool(level6.internal_closure_hodge_counterexample)
    chart_ok = len(GOEL_QE_ADMISSIBILITY_CHART) == len(ADMISSIBLE_DATA_DERIVATION)
    levels_ok = len(BIO_CLOSURE_LEVELS) >= 6
    r6_on_episodes = all(b.r6_square_holds for b in dna_env) if dna_env else False
    unitary_on_episodes = (
        all(b.unitary_pairing_holds for b in dna_env) if dna_env else False
    )
    classical_path_ok = classical_admitted > 0 and quantum_closed == 0
    # Honest: we derive the *architecture* of Q-env closure; empirical Q stays OPEN.
    derivation_ok = all(
        (
            internal_ok,
            chart_ok,
            levels_ok,
            r6_on_episodes,
            unitary_on_episodes,
            classical_path_ok,
            data_arch.kind == "ADMISSIBLE_DATA_ARCHITECTURE",
        )
    )

    verdict = (
        "GOEL_QUANTUM_ENVIRONMENTAL_CLOSURE_DERIVED"
        if derivation_ok
        else "GOEL_QUANTUM_ENVIRONMENTAL_CLOSURE_INCOMPLETE"
    )

    return {
        "schema_version": "1.0",
        "protocol": "goel-quantum-environmental-closure-via-bio-levels-and-data-chart",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "passed": derivation_ok,
        "relation": derived_relation,
        "bio_closure_levels": list(BIO_CLOSURE_LEVELS),
        "data_admissibility_chart": [row.to_dict() for row in GOEL_QE_ADMISSIBILITY_CHART],
        "data_classes": dict(DATA_CLASSES),
        "admissible_data_architecture": data_arch.to_dict(),
        "level6_reunified": {
            "verdict": (
                "REUNIFIED_INTERNAL_CLOSURE_HODGE_VERIFIED"
                if internal_ok
                else "OPEN"
            ),
            "r6_square_identity": level6.r6_square_identity,
            "intrinsic_unitarity": level6.intrinsic_unitarity,
            "fractal_hypotenuse_return": level6.fractal_hypotenuse_return,
            "lambert_triangle_time": level6.lambert_triangle_time_holds,
            "kakeya_reconstruction": level6.kakeya_reconstruction_exact,
            "level5_forgets_orientation": level6.level5_forgets_orientation,
            "level6_retains_orientation": level6.level6_retains_orientation,
            "p2_candidate": level6.p2_candidate,
            "classical_hodge_counterexample": level6.classical_hodge_counterexample,
            "basis_id": level6.basis_id,
            "trace_id": level6.trace_id,
        },
        "episode_bindings": [b.to_dict() for b in bindings],
        "summary": {
            "episodes_total": len(bindings),
            "dna_env_episodes": len(dna_env),
            "classical_goel_hair_admitted": classical_admitted,
            "quantum_environmental_closed": quantum_closed,
            "delta_c_q_open": open_q,
            "r6_square_on_dna_env": r6_on_episodes,
            "unitary_on_dna_env": unitary_on_episodes,
        },
        "stateful_biological_closure": stateful_report,
        "parallel_dialogue": roles["parallel_dialogue"],
        "ownership": roles["ownership"],
        "epistemic": {
            "derived": "quantum_environmental_closure_architecture_of_goel_operator",
            "classical_dna_env_hair": "MEASURED_ADMITTED_WHEN_COUPLED",
            "quantum_environmental_empirical": "OPEN_DELTA_C_Q",
            "level6_internal": "VERIFIED" if internal_ok else "OPEN",
            "classical_hodge_ce": "OPEN",
            "not_claimed": [
                "classical Chaitin Omega",
                "empirical interference closure",
                "classical Hodge counterexample",
                "Goel subsumed into Black Mirror",
                "RND1 ownership of Chaitin hair",
            ],
            "transcript_basis": [
                "docs/transcript_closure/closure_structure_map.json",
                "docs/CHAITIN_CONNECTED_RETURN_DERIVATION.md",
                "docs/GOEL_DNA_ENVIRONMENT_CHAITIN_OPERATOR.md",
            ],
        },
        "architecture_digest": digest(
            {
                "verdict": verdict,
                "basis": level6.basis_id,
                "trace": level6.trace_id,
                "classical": classical_admitted,
                "q_closed": quantum_closed,
                "chart": [r.stage_id for r in GOEL_QE_ADMISSIBILITY_CHART],
            }
        ),
    }


__all__ = [
    "BIO_CLOSURE_LEVELS",
    "GOEL_QE_ADMISSIBILITY_CHART",
    "GoelQEChartRow",
    "QuantumEnvEpisodeBinding",
    "bind_episode_quantum_env",
    "derive_goel_quantum_environmental_closure",
]

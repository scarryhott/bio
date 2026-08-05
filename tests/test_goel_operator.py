from __future__ import annotations

from closure.connected_return import LocalCell, make_occurrence
from closure.goel_operator import (
    GoelDNAEnvironmentState,
    GoelOperatorStatus,
    PolymeraseMode,
    apply_goel_chaitin_operator,
    bind_local_kakeya_global_goel,
    goel_state_from_modalities,
    infer_polymerase_mode,
    programme_role_split,
    tokenized_relativity_ball_from_cells,
)
from closure.types import Resolution


def test_tension_switches_polymerase_mode() -> None:
    assert infer_polymerase_mode(tension=0.1) is PolymeraseMode.POLYMERASE
    assert infer_polymerase_mode(tension=0.7) is PolymeraseMode.EXONUCLEASE
    assert infer_polymerase_mode(tension=0.99) is PolymeraseMode.STALLED


def test_goel_global_hair_requires_environment() -> None:
    before = GoelDNAEnvironmentState(dna_template={"seq": "ATGC"}, environment={})
    after = GoelDNAEnvironmentState(dna_template={"seq": "ATGC"}, environment={})
    receipt = apply_goel_chaitin_operator(before, after)
    assert receipt.status is GoelOperatorStatus.OPEN_MISSING_ENVIRONMENT
    assert receipt.resolution is Resolution.OPEN
    assert not receipt.write_back_allowed


def test_environment_coupled_dna_admits_global_chaitin_hair() -> None:
    before = goel_state_from_modalities(
        {
            "DNA": {"sequence": "ATGCGTAC"},
            "environment": {"media": "defined", "tension": 0.2},
        }
    )
    after = goel_state_from_modalities(
        {
            "DNA": {"sequence": "ATGCGTAC"},
            "environment": {"media": "defined", "tension": 0.2, "measured": True},
            "returned_consequence": {"measured": True},
        }
    )
    receipt = apply_goel_chaitin_operator(before, after, independent=True)
    assert receipt.status is GoelOperatorStatus.ADMITTED_GLOBAL_HAIR
    assert receipt.resolution is Resolution.CLOSED_TO_OPENING
    assert receipt.write_back_allowed
    assert receipt.environment_coupled


def test_unwitnessed_quantum_claim_stays_open_while_hair_may_admit() -> None:
    before = GoelDNAEnvironmentState(
        dna_template={"seq": "AT"},
        environment={"milieu": "a"},
        quantum_carrier={"model": "hypothesized"},
    )
    after = GoelDNAEnvironmentState(
        dna_template={"seq": "AT"},
        environment={"milieu": "b"},
        quantum_carrier={"model": "hypothesized"},
    )
    receipt = apply_goel_chaitin_operator(before, after)
    assert receipt.status is GoelOperatorStatus.ADMITTED_GLOBAL_HAIR
    assert receipt.quantum_claim == "OPEN_QUANTUM_UNWITNESSED"


def test_dual_local_kakeya_and_global_goel() -> None:
    occ = make_occurrence(
        token_id=7,
        position=0,
        step=1,
        prior_mask=True,
        ancestry="test",
        return_side="ball",
        residual=0.1,
        independently_transformed=True,
    )
    cell = LocalCell(
        cell_id="c1",
        rank=1,
        rotation_capacity=1,
        occurrences=(occ,),
        start_contact=occ.contact_boundary(),
        end_contact=occ.contact_boundary() + "|end",
        fold_seam="fold",
    )
    local = tokenized_relativity_ball_from_cells((cell,), ball_id="rn-local")
    assert local.occurrences[0]["identity_is_not_token"] is True

    before = GoelDNAEnvironmentState(
        dna_template={"seq": "ATG"},
        environment={"e": 1},
    )
    after = GoelDNAEnvironmentState(
        dna_template={"seq": "ATG"},
        environment={"e": 2},
    )
    global_hair = apply_goel_chaitin_operator(before, after)
    dual = bind_local_kakeya_global_goel(local, global_hair)
    assert dual.dual_status == "DUAL_CLOSED_TO_OPENING"


def test_programme_role_split_names_rn_local_and_goel_global() -> None:
    roles = programme_role_split()
    assert roles["ownership"]["rnd1_is_our_model"] is False
    assert roles["parallel_dialogue"]["subsumption"] is False
    assert "↔" in roles["parallel_dialogue"]["relation"] or "leftrightarrow" in roles[
        "parallel_dialogue"
    ]["relation"].lower()
    assert "goel" in roles["global_chaitin_operator"]["realization"]
    assert roles["local_kakeya_ball_hair_cycle"]["owner"] == "ours"
    assert "bio_token" in roles["local_kakeya_ball_hair_cycle"]["realization"] or "bio-token" in roles[
        "local_kakeya_ball_hair_cycle"
    ]["realization"].replace("_", "-")
    assert "classical Chaitin Ω" in roles["global_chaitin_operator"]["not_claimed"]
    assert "Goel subsumed into Black Mirror" in roles["global_chaitin_operator"]["not_claimed"]


def test_biological_double_slit_is_chaitin_global_hair_open_by_default() -> None:
    from closure.goel_operator import (
        BiologicalDoubleSlitGate,
        BiologicalDoubleSlitStatus,
        evaluate_biological_double_slit,
    )
    from closure.digest import digest

    gate = BiologicalDoubleSlitGate(
        bio_token_digest=digest({"DNA": "ATGC", "environment": {"tension": 0.2}}),
        dna_locus={"sequence": "ATGC", "motor": "polymerase"},
        environment={"tension": 0.2, "milieu": "defined"},
        claimed_coherence_gt_base_read=True,
    )
    receipt = evaluate_biological_double_slit(gate)
    assert receipt.chaitin_global_hair is True
    assert receipt.delta_c_q == "OPEN"
    assert receipt.status is BiologicalDoubleSlitStatus.OPEN_DELTA_C_Q
    assert not receipt.write_back_allowed


def test_biological_double_slit_interference_without_controls_stays_open() -> None:
    from closure.goel_operator import (
        BiologicalDoubleSlitGate,
        BiologicalDoubleSlitStatus,
        evaluate_biological_double_slit,
    )

    gate = BiologicalDoubleSlitGate(
        bio_token_digest="tok",
        dna_locus={"sequence": "AT"},
        environment={"e": 1},
        claimed_coherence_gt_base_read=True,
        interference_signature_reported=True,
        independently_returned=True,
        thermal_control_excluded=False,
    )
    receipt = evaluate_biological_double_slit(gate)
    assert receipt.status is BiologicalDoubleSlitStatus.OPEN_MISSING_CONTROLS
    assert receipt.delta_c_q == "OPEN"

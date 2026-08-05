from closure import (
    DERIVED_TOPOLOGY_IDS,
    UnifiedAxiometry,
    admit_verification_topology,
    ball_hair_topology,
    biological_nonidentical_topology,
    closure_chaitin_topology,
    fold_glue_topology,
    kakeya_contact_topology,
    partition_curvature_topology,
    rotation_extension_topology,
    self_limit_topology,
    topos_turing_topology,
    zero_infinity_topology,
)


def test_expected_project_topologies_are_exported() -> None:
    assert {
        "kakeya_contact",
        "closure_chaitin_ordered_support",
        "zero_infinity_predual",
        "local_ball_global_hair",
        "partition_curvature_return_side",
        "fold_glue_nonidentical_recovery",
        "self_limit_return_trajectory",
        "rotation_extension",
        "topos_turing_reciprocal_admissibility",
        "biological_nonidentical_recovery",
    } <= DERIVED_TOPOLOGY_IDS


def test_topology_constructors_produce_aligned_return_candidates() -> None:
    candidates = [
        kakeya_contact_topology(
            occurrences=("o1", "o2"), contacts=(("o1", "o2"),)
        ),
        closure_chaitin_topology(
            labeled_occurrences=("o1", "o2"),
            primitive_cells=("p1",),
            holistic_cell="h1",
        ),
        zero_infinity_topology(local_basis="0", global_continuation="inf"),
        ball_hair_topology(ball="local", hair="global"),
        partition_curvature_topology(left="black", right="white", observer_side="left"),
        fold_glue_topology(carriers=("DNA", "RNA"), maintained_relation="expression"),
        self_limit_topology(trajectory=("start", "return"), recovered_relation="same_relation"),
        rotation_extension_topology(presentation="rotation", transformed_return="extension"),
        topos_turing_topology(relational_state="R", invariant_state="U"),
        biological_nonidentical_topology(
            modalities=("DNA", "RNA", "protein", "phenotype"),
            returned_relation="cross_scale_recovery",
        ),
    ]

    axiometry = UnifiedAxiometry()
    for topology in candidates:
        assert topology.encode_eval_aligned()
        receipt = admit_verification_topology(axiometry, topology)
        assert receipt.write_back_allowed
        assert receipt.resolution.value in {"CLOSED_HIGHER", "CLOSED_TO_OPENING"}


def test_derived_topologies_are_not_identity_authority() -> None:
    topology = kakeya_contact_topology(
        occurrences=("o1", "o2"), contacts=(("o1", "o2"),)
    )
    assert topology.axiometric_shadows["identity_authority"] is False

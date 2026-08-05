"""Finite closure controls — retained original four plus expanded unit coverage."""

from closure import (
    BiologicalPerspective,
    ClosureRuntime,
    CoevolutionCarrier,
    MicroAction,
    Resolution,
    ReturnWitness,
    UnifiedAxiometry,
    VerificationTopology,
    admit_verification_topology,
    assert_admissible,
    construct_next_topos,
    default_admissibility_policy,
    digest,
    interaction_digest,
    partition_curvature_digest,
    to_potential_gate,
)
from closure.biology import BiologicalEpisode, biological_episode_to_carrier, shadow_cannot_certify
from closure.topology import UNIFIED_AXIOMETRY_MOTIFS


def build_gate():
    left = BiologicalPerspective(
        perspective_id="organism-A",
        local_state={"phenotype": "baseline"},
        developmental_history=("zygote", "development", "adult"),
        ecological_relations=("niche-1",),
        mandate={"reversible": True},
    )
    right = BiologicalPerspective(
        perspective_id="environment-B",
        local_state={"resource": "changed"},
        developmental_history=("season-1", "season-2"),
        ecological_relations=("organism-A",),
        mandate={"preserve_difference": True},
    )
    return to_potential_gate(
        CoevolutionCarrier(left, right, "adaptive-relation", ("future-niche",)),
        gate_id="gate-1",
    )


def test_closed_to_opening_and_ordered_support():
    gate = build_gate()
    runtime = ClosureRuntime()
    runtime.append_action(
        gate,
        MicroAction("organism-A", "adaptive-relation", "root", "behavior-change", "niche-1"),
    )
    support = runtime.ordered_support(gate)
    witness = ReturnWitness(
        source_boundary="field-observation",
        transformed_context="later ecological state",
        recovered_relation="adaptive-relation",
        ordered_support=support,
        consequence={"local_viability": True, "global_consequence": "niche changed"},
        next_opening="future-niche",
        transformation_path=("develop", "return"),
    )
    receipt = runtime.resolve(gate, witness)
    assert receipt.resolution is Resolution.CLOSED_TO_OPENING
    assert receipt.basis_digest.startswith("interaction_C:")


def test_reordered_support_is_false_collapse():
    gate = build_gate()
    runtime = ClosureRuntime()
    runtime.append_action(gate, MicroAction("organism-A", "adaptive-relation", "root", "a", "niche"))
    runtime.append_action(
        gate,
        MicroAction("environment-B", "adaptive-relation", "root", "b", "niche"),
    )
    support = runtime.ordered_support(gate)
    witness = ReturnWitness(
        source_boundary="field-observation",
        transformed_context="later state",
        recovered_relation="adaptive-relation",
        ordered_support=tuple(reversed(support)),
        consequence={"local_viability": True, "global_consequence": True},
    )
    assert runtime.resolve(gate, witness).resolution is Resolution.FALSE_COLLAPSE


def test_controlled_model_echo_remains_open():
    gate = build_gate()
    runtime = ClosureRuntime()
    witness = ReturnWitness(
        source_boundary="organism-A",
        transformed_context="self replay",
        recovered_relation="adaptive-relation",
        ordered_support=(),
        consequence={"local_viability": True, "global_consequence": True},
    )
    assert runtime.resolve(gate, witness).resolution is Resolution.OPEN


def test_refusal_blocks_learning_commit():
    gate = build_gate()
    receipt = ClosureRuntime().resolve(
        gate,
        ReturnWitness("participant", "proposal", None, (), refused=True),
    )
    assert receipt.resolution is Resolution.REFUSED
    assert receipt.write_back_allowed is False


def test_all_five_resolution_states():
    runtime = ClosureRuntime()
    gate = build_gate()
    assert runtime.resolve(gate, None).resolution is Resolution.OPEN

    gate = build_gate()
    runtime.append_action(gate, MicroAction("organism-A", "adaptive-relation", "root", "a", "c"))
    support = runtime.ordered_support(gate)
    closed = runtime.resolve(
        gate,
        ReturnWitness(
            "field",
            "t",
            "adaptive-relation",
            support,
            consequence={"local_viability": True, "global_consequence": True},
            transformation_path=("x",),
        ),
    )
    assert closed.resolution is Resolution.CLOSED_HIGHER

    gate = build_gate()
    runtime.append_action(gate, MicroAction("organism-A", "adaptive-relation", "root", "a", "c"))
    support = runtime.ordered_support(gate)
    opening = runtime.resolve(
        gate,
        ReturnWitness(
            "field",
            "t",
            "adaptive-relation",
            support,
            consequence={"local_viability": True, "global_consequence": True},
            next_opening="child",
            transformation_path=("x",),
        ),
    )
    assert opening.resolution is Resolution.CLOSED_TO_OPENING

    gate = build_gate()
    runtime.append_action(gate, MicroAction("organism-A", "adaptive-relation", "root", "a", "c"))
    bad = runtime.resolve(
        gate,
        ReturnWitness("field", "t", "wrong", runtime.ordered_support(gate), consequence={}),
    )
    assert bad.resolution is Resolution.FALSE_COLLAPSE

    gate = build_gate()
    refused = runtime.resolve(gate, ReturnWitness("x", "y", None, (), refused=True))
    assert refused.resolution is Resolution.REFUSED


def test_child_gate_recoverability():
    runtime = ClosureRuntime()
    parent = build_gate()
    runtime.append_action(parent, MicroAction("organism-A", "adaptive-relation", "root", "a", "c"))
    child = runtime.spawn_child_gate(parent, gate_id="child-1", opening="future-niche")
    # Child action that does not extend parent support fails recoverability.
    runtime.append_action(child, MicroAction("organism-A", "adaptive-relation", "root", "z", "c"))
    support = runtime.ordered_support(child)
    assert child.parent_support is not None
    assert support[: len(child.parent_support)] != child.parent_support
    receipt = runtime.resolve(
        child,
        ReturnWitness(
            "field",
            "t",
            "adaptive-relation",
            support,
            consequence={"local_viability": True, "global_consequence": True},
            transformation_path=("y",),
        ),
    )
    assert receipt.resolution is Resolution.FALSE_COLLAPSE

    # Recoverable child: replay parent support then extend.
    child_ok = runtime.spawn_child_gate(parent, gate_id="child-2", opening="future-niche")
    parent_action = parent.ordered_actions[0]
    runtime.append_action(
        child_ok,
        MicroAction(
            parent_action.actor_id,
            parent_action.relation_key,
            "root",
            parent_action.semantic_pointing,
            parent_action.context,
            payload=dict(parent_action.payload),
        ),
    )
    assert runtime.ordered_support(child_ok) == child_ok.parent_support


def test_return_side_involution():
    runtime = ClosureRuntime()
    assert runtime.invert_return_side("local") == "global"
    assert runtime.invert_return_side(runtime.invert_return_side("ball")) == "ball"


def test_non_repetition_no_new_rank():
    runtime = ClosureRuntime()
    gate = build_gate()
    runtime.append_action(gate, MicroAction("organism-A", "adaptive-relation", "root", "a", "c"))
    support = runtime.ordered_support(gate)
    w = ReturnWitness(
        "field",
        "t",
        "adaptive-relation",
        support,
        consequence={"local_viability": True, "global_consequence": True},
        transformation_path=("x",),
    )
    first = runtime.resolve(gate, w)
    assert first.new_closure_rank is True
    # Identical replay without new independent transform
    second = runtime.resolve(
        gate,
        ReturnWitness(
            "field",
            "t",
            "adaptive-relation",
            support,
            consequence={"local_viability": True, "global_consequence": True},
            transformation_path=("x",),
        ),
    )
    assert second.resolution is Resolution.OPEN
    assert second.new_closure_rank is False


def test_digest_stable_under_renaming_sensitive_to_partition():
    a = partition_curvature_digest(
        {"side": "ball", "label": "Earth"},
        {"fold": 1, "name": "alpha"},
    )
    b = partition_curvature_digest(
        {"side": "ball", "label": "Terra"},
        {"fold": 1, "name": "beta"},
    )
    assert a == b
    c = partition_curvature_digest({"side": "hair"}, {"fold": 1})
    assert a != c


def test_telemetry_separated_from_identity():
    d1 = interaction_digest(
        originless_basis="predual:r",
        gate_id="g",
        ordered_support=("a",),
        relation="r",
        resolution="CLOSED_HIGHER",
        next_opening=None,
    )
    # Confidence/entropy must not enter identity digest helpers used here.
    assert "confidence" not in d1
    assert digest({"score": 0.9}) != d1
    assert shadow_cannot_certify({"fitness": 0.99}) is True


def test_unified_axiometry_policy_rejects_fixed_catalog():
    assert assert_admissible(default_admissibility_policy()) == []
    assert len(UNIFIED_AXIOMETRY_MOTIFS) >= 10
    bad = default_admissibility_policy()
    bad["treat_score_as_identity"] = True
    bad["topologies_are_fixed_catalog"] = True
    violations = assert_admissible(bad)
    assert "axiometry_is_shadow:violated" in violations
    assert "generator_not_totality:violated" in violations


def test_verification_topology_admitted_in_resolution_not_catalog():
    axiometry = UnifiedAxiometry()
    # Incomplete cycles remain OPEN — not pre-rejected by a fixed list.
    open_topo = VerificationTopology(
        topology_id="open-ball",
        basis_cycle={"homology": "curl-a"},
        closure_cycle={"homotopy": "div-b"},
    )
    open_receipt = admit_verification_topology(axiometry, open_topo)
    assert open_receipt.resolution is Resolution.OPEN
    assert "open-ball" in axiometry.open_candidates

    # Cycle equality + encode/eval alignment admits through resolution.
    admitted = VerificationTopology(
        topology_id="equal-cycles",
        basis_cycle={"cycle": 1, "kind": "homology"},
        closure_cycle={"cycle": 1, "kind": "homology"},
        encoding_topos={"layer": "E"},
        relation_topos={"layer": "E"},
        openings=["next_layer"],
    )
    receipt = admit_verification_topology(axiometry, admitted)
    assert receipt.resolution is Resolution.CLOSED_TO_OPENING
    assert "equal-cycles" in axiometry.admitted
    assert admitted.status is Resolution.CLOSED_TO_OPENING

    # Forced fixed chart collapses.
    forced = VerificationTopology(
        topology_id="forced-chart",
        basis_cycle={"cycle": 2},
        closure_cycle={"cycle": 2},
        encoding_topos={"layer": "F"},
        relation_topos={"layer": "F"},
        axiometric_shadows={"force_fixed_chart": True, "score": 0.99},
    )
    collapsed = admit_verification_topology(axiometry, forced)
    assert collapsed.resolution is Resolution.FALSE_COLLAPSE

    # Generator constructs further candidate topos from admitted parent.
    child = construct_next_topos(
        axiometry,
        admitted,
        topology_id="child-layer",
        basis_cycle={"cycle": 3},
        closure_cycle={"cycle": 3},
    )
    assert child.topology_id in axiometry.open_candidates
    assert child.status is Resolution.OPEN


def test_biological_episode_nonflat():
    episode = BiologicalEpisode(
        modalities={
            "DNA": {"seq": "ATGC"},
            "protein": {"fold": "alpha"},
            "environment": {"temp": 37},
            "returned_consequence": {"viability": True},
        },
        shared_relation="expression",
        axiometric_shadows={"fitness": 0.8, "confidence": 0.9},
    )
    carrier = biological_episode_to_carrier(episode, gate_id="bio-1")
    assert "DNA" in carrier.ball["modalities"]
    assert carrier.axiometric_evidence["fitness"] == 0.8
    assert carrier.gate.admissibility["nonidentical_reciprocal_recovery"] is True

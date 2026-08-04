from closure import (
    BiologicalPerspective,
    ClosureRuntime,
    CoevolutionCarrier,
    MicroAction,
    Resolution,
    ReturnWitness,
    to_potential_gate,
)


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
    support = tuple(runtime._receipt(gate, Resolution.OPEN, None, None, {}).ordered_support)
    witness = ReturnWitness(
        source_boundary="field-observation",
        transformed_context="later ecological state",
        recovered_relation="adaptive-relation",
        ordered_support=support,
        consequence={"local_viability": True, "global_consequence": "niche changed"},
        next_opening="future-niche",
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
        MicroAction(
            "environment-B", "adaptive-relation", "root", "b", "niche",
        ),
    )
    support = runtime._receipt(gate, Resolution.OPEN, None, None, {}).ordered_support
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

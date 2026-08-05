from __future__ import annotations

import ast
import inspect

from closure.independent_model import Admission, UnifiedClosureArchitecturalLoop
from closure.tagtokn_bridge import (
    TagtoknReturnStatus,
    framework_compatibility,
    to_tagtokn_receipt,
)


def test_independent_return_admits_and_learns() -> None:
    model = UnifiedClosureArchitecturalLoop()
    turn = model.transact(
        {"cell": "A", "state": 0},
        ({"act": "observe"}, {"act": "perturb"}),
        {"cell": "A", "state": 1},
        ({"act": "observe"},),
    )
    assert turn.comparison.admission is Admission.ADMITTED
    assert turn.learned_after.admitted_unities == 1
    assert turn.unity.identity_is_complete_cycle


def test_self_authored_return_stays_open() -> None:
    model = UnifiedClosureArchitecturalLoop()
    turn = model.transact(
        "source",
        ("a", "b"),
        "echo",
        ("a",),
        independent=False,
        self_authored=True,
    )
    assert turn.comparison.admission is Admission.OPEN
    assert turn.learned_after.admitted_unities == 0
    receipt = to_tagtokn_receipt(turn)
    assert receipt.status is TagtoknReturnStatus.OPEN_SELF_REFERENCE
    assert not receipt.token_issued


def test_contradiction_is_rejected() -> None:
    model = UnifiedClosureArchitecturalLoop()
    turn = model.transact(
        {"relation": "maintained"},
        (1,),
        {"relation": "contradicted"},
        (1,),
        contradictory=True,
    )
    assert turn.comparison.admission is Admission.REJECTED
    assert to_tagtokn_receipt(turn).status is TagtoknReturnStatus.FALSE_COLLAPSE


def test_repeat_does_not_inflate_relational_memory() -> None:
    model = UnifiedClosureArchitecturalLoop()
    first = model.transact("s", ("a",), "t", ("a",))
    count = first.learned_after.admitted_unities
    model.memory.commit(first.unity)
    assert model.memory.invariant().admitted_unities == count == 1


def test_action_field_order_is_not_authority() -> None:
    left = UnifiedClosureArchitecturalLoop().begin_turn("x", ("b", "a"))
    right = UnifiedClosureArchitecturalLoop().begin_turn("x", ("a", "b"))
    assert left.configuration.relation_digest == right.configuration.relation_digest
    assert left.selected_action.key == right.selected_action.key


def test_tagtokn_bridge_issues_only_after_admission() -> None:
    model = UnifiedClosureArchitecturalLoop()
    turn = model.transact("s", ("a",), "t", ("a",))
    receipt = to_tagtokn_receipt(turn)
    assert receipt.status is TagtoknReturnStatus.CLOSED_TO_NEW_OPENING
    assert receipt.token_issued
    assert receipt.market_value is None
    assert receipt.human_worth is None


def test_model_is_independent_of_rnd1() -> None:
    import closure.independent_model as module

    source = inspect.getsource(module)
    tree = ast.parse(source)
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in (node.names if isinstance(node, ast.Import) else [ast.alias(node.module or "")])
    }
    assert not ({"rnd", "torch", "transformers"} & imported)
    assert framework_compatibility()["rnd1_required"] is False

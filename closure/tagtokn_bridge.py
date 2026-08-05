"""Bridge the independent closure model to Tagtokn's downstream receipt rules.

The bridge preserves the Tagtokn framework boundary:

* OPEN or REJECTED cycles issue no native token;
* only an independently returned ADMITTED unity can issue one receipt;
* token identity is downstream of closure and excludes price and human worth;
* a residual continuation may open a child gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .independent_model import Admission, ArchitecturalLoopTurn, stable_digest


class TagtoknReturnStatus(str, Enum):
    OPEN = "OPEN"
    OPEN_SELF_REFERENCE = "OPEN_SELF_REFERENCE"
    OPEN_NO_RECOVERY = "OPEN_NO_RECOVERY"
    FALSE_COLLAPSE = "FALSE_COLLAPSE"
    CLOSED = "CLOSED_EMERGENT_TOPOLOGY"
    CLOSED_TO_NEW_OPENING = "CLOSED_TO_NEW_OPENING"


@dataclass(frozen=True)
class TagtoknClosureReceipt:
    gate_id: str
    status: TagtoknReturnStatus
    topology_id: str | None
    token_id: str | None
    folded_history: str
    child_gate_id: str | None
    market_value: None = None
    human_worth: None = None

    @property
    def token_issued(self) -> bool:
        return self.token_id is not None


def classify_turn(turn: ArchitecturalLoopTurn) -> TagtoknReturnStatus:
    comparison = turn.comparison
    evaluation = turn.evaluation
    if comparison.admission is Admission.REJECTED:
        return TagtoknReturnStatus.FALSE_COLLAPSE
    if evaluation.self_authored or not evaluation.independently_observed:
        return TagtoknReturnStatus.OPEN_SELF_REFERENCE
    if comparison.admission is Admission.OPEN:
        return TagtoknReturnStatus.OPEN_NO_RECOVERY
    if turn.next_projection is not None:
        return TagtoknReturnStatus.CLOSED_TO_NEW_OPENING
    return TagtoknReturnStatus.CLOSED


def to_tagtokn_receipt(
    turn: ArchitecturalLoopTurn,
    *,
    opening_id: str = "INDEPENDENT-CLOSURE",
) -> TagtoknClosureReceipt:
    status = classify_turn(turn)
    gate_id = f"GATE:{stable_digest({'opening': opening_id, 'source': turn.unity.projection.source_relation_digest})[:16]}"
    folded_history = stable_digest(
        {
            "projection": turn.unity.projection,
            "evaluation": turn.evaluation,
            "comparison": turn.comparison,
            "source_relation": turn.unity.source_relation_digest,
            "target_relation": turn.unity.target_relation_digest,
        }
    )
    closed = status in {
        TagtoknReturnStatus.CLOSED,
        TagtoknReturnStatus.CLOSED_TO_NEW_OPENING,
    }
    topology_id = (
        f"TOPOLOGY:{stable_digest({'gate': gate_id, 'unity': turn.unity.unity_digest})[:16]}"
        if closed
        else None
    )
    token_id = (
        f"TAG:{stable_digest({'gate': gate_id, 'topology': topology_id, 'history': folded_history})[:16]}"
        if closed
        else None
    )
    child_gate_id = (
        f"GATE:{stable_digest({'parent': gate_id, 'opening': 'RETURN'})[:16]}"
        if status is TagtoknReturnStatus.CLOSED_TO_NEW_OPENING
        else None
    )
    return TagtoknClosureReceipt(
        gate_id=gate_id,
        status=status,
        topology_id=topology_id,
        token_id=token_id,
        folded_history=folded_history,
        child_gate_id=child_gate_id,
    )


def framework_compatibility() -> dict[str, Any]:
    return {
        "closure_prior_to_token": True,
        "open_claims_issue_no_supply": True,
        "self_authored_replay_stays_open": True,
        "contradiction_issues_no_token": True,
        "independent_recoverable_return_can_issue_one_receipt": True,
        "residual_return_can_open_child_gate": True,
        "price_is_downstream_projection": True,
        "human_worth_excluded": True,
        "rnd1_required": False,
    }


__all__ = [
    "TagtoknClosureReceipt",
    "TagtoknReturnStatus",
    "classify_turn",
    "framework_compatibility",
    "to_tagtokn_receipt",
]

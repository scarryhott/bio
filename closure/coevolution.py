from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .types import PotentialGate


@dataclass(frozen=True)
class BiologicalPerspective:
    perspective_id: str
    local_state: dict[str, Any]
    developmental_history: tuple[str, ...]
    ecological_relations: tuple[str, ...]
    mandate: dict[str, Any]


@dataclass(frozen=True)
class CoevolutionCarrier:
    left: BiologicalPerspective
    right: BiologicalPerspective
    shared_relation: str
    openings: tuple[str, ...]


def to_potential_gate(carrier: CoevolutionCarrier, gate_id: str) -> PotentialGate:
    """Create a shared gate without reducing either participant to the other.

    Selection, fitness, model confidence, and prevalence may be stored as evidence,
    but do not define the closure identity.
    """
    ball = {
        "active_perspective": carrier.left.perspective_id,
        "left_state": carrier.left.local_state,
        "ordered_left_history": carrier.left.developmental_history,
        "actor_tails": {},
    }
    possible_hair = [
        {
            "source": carrier.right.perspective_id,
            "state": carrier.right.local_state,
            "ordered_history": carrier.right.developmental_history,
            "ecological_relations": carrier.right.ecological_relations,
        }
    ]
    return PotentialGate(
        gate_id=gate_id,
        originless_basis=f"predual:{carrier.shared_relation}",
        ball=ball,
        possible_hair=possible_hair,
        semantics={"relation_key": carrier.shared_relation},
        openings=list(carrier.openings),
        admissibility={
            "controlled_boundaries": [carrier.left.perspective_id],
            "difference_preservation": True,
            "recursive_recoverability": True,
        },
        mandate={
            "left": carrier.left.mandate,
            "right": carrier.right.mandate,
            "required_witness_fields": ["local_viability", "global_consequence"],
        },
    )

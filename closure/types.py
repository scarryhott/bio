from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Resolution(str, Enum):
    CLOSED_HIGHER = "CLOSED_HIGHER"
    CLOSED_TO_OPENING = "CLOSED_TO_OPENING"
    OPEN = "OPEN"
    FALSE_COLLAPSE = "FALSE_COLLAPSE"
    REFUSED = "REFUSED"


@dataclass(frozen=True)
class MicroAction:
    actor_id: str
    relation_key: str
    prior_tail: str
    semantic_pointing: str
    context: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReturnWitness:
    source_boundary: str
    transformed_context: str
    recovered_relation: str | None
    ordered_support: tuple[str, ...]
    consequence: dict[str, Any] = field(default_factory=dict)
    next_opening: str | None = None
    refused: bool = False


@dataclass
class PotentialGate:
    gate_id: str
    originless_basis: str
    ball: dict[str, Any]
    possible_hair: list[dict[str, Any]]
    semantics: dict[str, Any]
    openings: list[str]
    admissibility: dict[str, Any]
    mandate: dict[str, Any]
    ordered_actions: list[MicroAction] = field(default_factory=list)
    status: Resolution = Resolution.OPEN


@dataclass(frozen=True)
class ClosureReceipt:
    gate_id: str
    resolution: Resolution
    basis_digest: str
    ordered_support: tuple[str, ...]
    recovered_relation: str | None
    next_opening: str | None
    evidence: dict[str, Any]

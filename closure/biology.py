# Copyright 2026 scarryhott/bio contributors.
"""Biological and coevolutionary adapter.

Modalities remain separately recoverable. Mutation likelihood, fitness, confidence,
and phenotype probability are axiometric shadows — they may propose an act but
cannot certify closure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .types import ClosureCarrier, ClosureConfig, HairComposition, PotentialGate, Resolution


BIOLOGICAL_RELATIONS = (
    "DNA",
    "RNA",
    "protein",
    "cell_state",
    "tissue_context",
    "organism_state",
    "environment",
    "intervention",
    "returned_consequence",
)


@dataclass(frozen=True)
class BiologicalPerspective:
    perspective_id: str
    local_state: dict[str, Any]
    developmental_history: tuple[str, ...]
    ecological_relations: tuple[str, ...]
    mandate: dict[str, Any]
    modality: str = "organism_state"


@dataclass(frozen=True)
class BiologicalEpisode:
    """Structured multi-modality episode without flat embedding collapse."""

    modalities: dict[str, dict[str, Any]]
    shared_relation: str
    openings: tuple[str, ...] = ()
    axiometric_shadows: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        unknown = set(self.modalities) - set(BIOLOGICAL_RELATIONS)
        if unknown:
            raise ValueError(f"unknown biological modalities: {sorted(unknown)}")


@dataclass(frozen=True)
class CoevolutionCarrier:
    left: BiologicalPerspective
    right: BiologicalPerspective
    shared_relation: str
    openings: tuple[str, ...]


def to_potential_gate(carrier: CoevolutionCarrier, gate_id: str) -> PotentialGate:
    """Create a shared gate without reducing either participant to the other."""
    ball = {
        "active_perspective": carrier.left.perspective_id,
        "left_state": carrier.left.local_state,
        "ordered_left_history": carrier.left.developmental_history,
        "left_modality": carrier.left.modality,
        "actor_tails": {},
    }
    possible_hair = [
        {
            "source": carrier.right.perspective_id,
            "state": carrier.right.local_state,
            "ordered_history": carrier.right.developmental_history,
            "ecological_relations": carrier.right.ecological_relations,
            "modality": carrier.right.modality,
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
        return_side="ball",
    )


def biological_episode_to_carrier(
    episode: BiologicalEpisode,
    *,
    gate_id: str,
    config: ClosureConfig | None = None,
) -> ClosureCarrier:
    """Map a biological episode onto G_t without flattening modalities."""
    episode.validate()
    gate = PotentialGate(
        gate_id=gate_id,
        originless_basis=f"predual:bio:{episode.shared_relation}",
        ball={
            "modalities": {k: dict(v) for k, v in episode.modalities.items()},
            "actor_tails": {},
        },
        possible_hair=[
            {"source": name, "state": state}
            for name, state in episode.modalities.items()
            if name != "organism_state"
        ],
        semantics={"relation_key": episode.shared_relation, "kind": "biological"},
        openings=list(episode.openings),
        admissibility={
            "controlled_boundaries": ["organism_state", "model_echo"],
            "difference_preservation": True,
            "recursive_recoverability": True,
            "nonidentical_reciprocal_recovery": True,
        },
        mandate={
            "required_witness_fields": ["local_viability", "global_consequence"],
            "recovery": "developmental_or_ecological",
        },
        return_side="organism",
    )
    hair = HairComposition()
    if "environment" in episode.modalities or "returned_consequence" in episode.modalities:
        from .types import HairSource

        hair.external_biological = HairSource(
            kind="external_biological_context",
            payload={
                "environment": episode.modalities.get("environment"),
                "returned_consequence": episode.modalities.get("returned_consequence"),
            },
            scalar=float(episode.axiometric_shadows.get("fitness", 0.0)),
        )
    return ClosureCarrier(
        gate=gate,
        ball=gate.ball,
        hair=hair,
        semantics=gate.semantics,
        openings=list(gate.openings),
        mandate=gate.mandate,
        return_partition={"side": "organism", "complement": "environment"},
        axiometric_evidence=dict(episode.axiometric_shadows),
        config=config or ClosureConfig(),
    )


def biological_act_path() -> tuple[str, ...]:
    """Required resolution path for a biological act."""
    return (
        "local_proposal",
        "developmental_ecological_propagation",
        "transformed_return",
        "resolution",
    )


def shadow_cannot_certify(shadows: dict[str, Any]) -> bool:
    """Fitness/confidence/phenotype probability never certify closure alone."""
    certifying_keys = {
        "mutation_likelihood",
        "fitness",
        "confidence",
        "phenotype_probability",
        "entropy",
        "score",
    }
    return any(k in shadows for k in certifying_keys)  # present ⇒ must stay axiometric


def resolution_from_biological_return(
    *,
    independent: bool,
    contradiction: bool,
    next_opening: str | None,
    refused: bool,
) -> Resolution:
    if refused:
        return Resolution.REFUSED
    if contradiction:
        return Resolution.FALSE_COLLAPSE
    if not independent:
        return Resolution.OPEN
    if next_opening:
        return Resolution.CLOSED_TO_OPENING
    return Resolution.CLOSED_HIGHER

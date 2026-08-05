# Copyright 2026 scarryhott/bio contributors.
# Re-export biological coevolution surface for backward-compatible imports.
from .biology import (
    BIOLOGICAL_RELATIONS,
    BiologicalEpisode,
    BiologicalPerspective,
    CoevolutionCarrier,
    biological_act_path,
    biological_episode_to_carrier,
    resolution_from_biological_return,
    shadow_cannot_certify,
    to_potential_gate,
)

__all__ = [
    "BIOLOGICAL_RELATIONS",
    "BiologicalEpisode",
    "BiologicalPerspective",
    "CoevolutionCarrier",
    "biological_act_path",
    "biological_episode_to_carrier",
    "resolution_from_biological_return",
    "shadow_cannot_certify",
    "to_potential_gate",
]

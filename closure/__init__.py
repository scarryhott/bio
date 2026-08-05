# Copyright 2026 scarryhott/bio contributors.
"""Closure-derived admissible verification for RND1 and biological coevolution."""

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
from .connected_return import (
    ConnectedReturnVerdict,
    LabeledOccurrence,
    LocalCell,
    evaluate_connected_return,
    make_occurrence,
)
from .digest import digest, interaction_digest, partition_curvature_digest
from .hair import build_holistic_hair
from .runtime import ClosureRuntime
from .topology import (
    ADMISSIBLE_TOPOLOGIES,
    UNIFIED_AXIOMETRY_MOTIFS,
    DerivationMotif,
    UnifiedAxiometry,
    VerificationTopology,
    admit_verification_topology,
    assert_admissible,
    construct_next_topos,
    default_admissibility_policy,
    topology_to_gate,
)
from .types import (
    ClosureCarrier,
    ClosureConfig,
    ClosureMode,
    ClosureReceipt,
    HairComposition,
    HairSource,
    MicroAction,
    PotentialGate,
    Resolution,
    ReturnWitness,
    StepAdmission,
)

__all__ = [
    "ADMISSIBLE_TOPOLOGIES",
    "BIOLOGICAL_RELATIONS",
    "BiologicalEpisode",
    "BiologicalPerspective",
    "ClosureCarrier",
    "ClosureConfig",
    "ClosureMode",
    "ClosureReceipt",
    "ClosureRuntime",
    "CoevolutionCarrier",
    "ConnectedReturnVerdict",
    "DerivationMotif",
    "HairComposition",
    "HairSource",
    "LabeledOccurrence",
    "LocalCell",
    "MicroAction",
    "PotentialGate",
    "Resolution",
    "ReturnWitness",
    "StepAdmission",
    "UNIFIED_AXIOMETRY_MOTIFS",
    "UnifiedAxiometry",
    "VerificationTopology",
    "admit_verification_topology",
    "assert_admissible",
    "biological_act_path",
    "biological_episode_to_carrier",
    "build_holistic_hair",
    "construct_next_topos",
    "default_admissibility_policy",
    "digest",
    "evaluate_connected_return",
    "interaction_digest",
    "make_occurrence",
    "partition_curvature_digest",
    "resolution_from_biological_return",
    "shadow_cannot_certify",
    "to_potential_gate",
    "topology_to_gate",
]

try:
    from .rnd_controller import TokenAdmission, closure_token_admission
    from .sampler_bridge import admit_denoising_step, baseline_unmask_mask, make_carrier
except ImportError:  # pragma: no cover
    TokenAdmission = None
    closure_token_admission = None
    admit_denoising_step = None
    baseline_unmask_mask = None
    make_carrier = None
else:
    __all__.extend(
        [
            "TokenAdmission",
            "closure_token_admission",
            "admit_denoising_step",
            "baseline_unmask_mask",
            "make_carrier",
        ]
    )

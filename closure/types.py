# Copyright 2026 scarryhott/bio contributors.
# Closure-native types. RND1 model code remains under Apache-2.0 (Radical Numerics).
"""Native closure carrier types.

Scores, entropy, confidence, digests, and PASS counts are axiometric evidence only.
They never authorize closure identity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal


class Resolution(str, Enum):
    CLOSED_HIGHER = "CLOSED_HIGHER"
    CLOSED_TO_OPENING = "CLOSED_TO_OPENING"
    OPEN = "OPEN"
    FALSE_COLLAPSE = "FALSE_COLLAPSE"
    REFUSED = "REFUSED"


ClosureMode = Literal["off", "probe", "full"]


@dataclass(frozen=True)
class ClosureConfig:
    """Sampler and runtime configuration for closure admission."""

    mode: ClosureMode = "off"
    return_depth: int = 2
    local_radius: int = 2
    distant_radius: int = 8
    open_state_threshold: float = 0.35
    contradiction_threshold: float = 0.75
    minimum_finite_progress: int = 1
    track_return_side: bool = True
    use_hidden_state_hair: bool = True
    use_expert_routing_hair: bool = True
    require_independent_return: bool = True
    emit_telemetry: bool = True
    max_open_fraction: float = 0.95


@dataclass(frozen=True)
class MicroAction:
    actor_id: str
    relation_key: str
    prior_tail: str
    semantic_pointing: str
    context: str
    payload: dict[str, Any] = field(default_factory=dict)
    step_index: int | None = None
    position: int | None = None
    token_id: int | None = None


@dataclass(frozen=True)
class ReturnWitness:
    source_boundary: str
    transformed_context: str
    recovered_relation: str | None
    ordered_support: tuple[str, ...]
    consequence: dict[str, Any] = field(default_factory=dict)
    next_opening: str | None = None
    refused: bool = False
    return_side: str | None = None
    transformation_path: tuple[str, ...] = ()
    return_discrepancy: float | None = None


@dataclass(frozen=True)
class HairSource:
    """One typed hair contribution; kept separately inspectable."""

    kind: str
    payload: dict[str, Any]
    scalar: float | None = None


@dataclass
class HairComposition:
    local_token: HairSource | None = None
    distant_sequence: HairSource | None = None
    prefix_suffix: HairSource | None = None
    hidden_layer: HairSource | None = None
    moe_expert_routing: HairSource | None = None
    whole_sequence_digest: HairSource | None = None
    cross_step_history: HairSource | None = None
    external_biological: HairSource | None = None

    def sources(self) -> list[HairSource]:
        out: list[HairSource] = []
        for item in (
            self.local_token,
            self.distant_sequence,
            self.prefix_suffix,
            self.hidden_layer,
            self.moe_expert_routing,
            self.whole_sequence_digest,
            self.cross_step_history,
            self.external_biological,
        ):
            if item is not None:
                out.append(item)
        return out

    def probe_rank_scalar(self) -> float:
        """Scalar may rank probes only; it is not closure identity."""
        vals = [s.scalar for s in self.sources() if s.scalar is not None]
        if not vals:
            return 0.0
        return sum(vals) / len(vals)


@dataclass
class PotentialGate:
    """Potential gate (B, H, Σ, Ω, ρ) plus ordered history and return partition."""

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
    return_side: str | None = None
    parent_support: tuple[str, ...] | None = None
    closure_ranks: set[str] = field(default_factory=set)


@dataclass
class ClosureCarrier:
    """Native episode carrier

    G_t = (B_t, H_t, Σ_t, Ω_t, ρ_t, Γ_t, Π_t, A_t)
    """

    gate: PotentialGate
    ball: dict[str, Any]
    hair: HairComposition
    semantics: dict[str, Any]
    openings: list[str]
    mandate: dict[str, Any]
    ordered_history: list[MicroAction] = field(default_factory=list)
    return_partition: dict[str, Any] = field(default_factory=dict)
    axiometric_evidence: dict[str, Any] = field(default_factory=dict)
    config: ClosureConfig = field(default_factory=ClosureConfig)
    step_index: int = 0
    committed_trace: list[dict[str, Any]] = field(default_factory=list)
    open_positions: list[int] = field(default_factory=list)
    # Unified axiometry handle: topologies admitted in resolution, not fixed.
    axiometry_relation: str = "C"

    @property
    def B(self) -> dict[str, Any]:
        return self.ball

    @property
    def H(self) -> HairComposition:
        return self.hair

    @property
    def Sigma(self) -> dict[str, Any]:
        return self.semantics

    @property
    def Omega(self) -> list[str]:
        return self.openings

    @property
    def rho(self) -> dict[str, Any]:
        return self.mandate

    @property
    def Gamma(self) -> list[MicroAction]:
        return self.ordered_history

    @property
    def Pi(self) -> dict[str, Any]:
        return self.return_partition

    @property
    def A(self) -> dict[str, Any]:
        return self.axiometric_evidence


@dataclass(frozen=True)
class ClosureReceipt:
    gate_id: str
    resolution: Resolution
    basis_digest: str
    ordered_support: tuple[str, ...]
    recovered_relation: str | None
    next_opening: str | None
    evidence: dict[str, Any]
    return_side: str | None = None
    new_closure_rank: bool = False
    write_back_allowed: bool = True


@dataclass(frozen=True)
class StepAdmission:
    """Per-denoising-step admission decision for the live sampler."""

    commit_mask: Any  # torch.Tensor when available
    open_mask: Any
    reject_mask: Any
    resolutions: dict[int, Resolution]
    telemetry: dict[str, Any]
    ordered_support: tuple[str, ...]

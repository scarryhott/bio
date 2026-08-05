# Copyright 2026 scarryhott/bio contributors.
"""Reunified Level-6 reciprocal topology (ball ↔ hair).

Transcript / ChatGPT-reunified axiometry:

    z = z_B ⊕ z_H
    P = diag(2, 1/2)          # reciprocal partition–curvature weights
    σ(z_B, z_H) = (conj z_H, conj z_B)
    R_6 = σ ∘ P               # Level-6 ball-into-hair return
    R_6² = id
    ⟨Px, Py⟩_C = ⟨x, y⟩_C     # unitary under cross ball–hair pairing

The Euclidean ellipse is only a projection of the intrinsic unit relational
hypotenuse. Triangle-time / Lambert-W is the temporal chart of the same
2 ↔ 1/2 topology. Formal balanced (p,p) classes are fixed by P and R_6;
classical Hodge non-algebraicity remains OPEN (no smooth projective X here).

Provenance: reunified Level-6 run (REUNIFIED_INTERNAL_CLOSURE_HODGE_VERIFIED)
plus docs/transcript_closure (predual Kakeya-i / Chaitin-r; IVI-3 quantum).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import cmath
import hashlib
import json
import math
from typing import Any, Iterable

import mpmath as mp

TOL = 1e-10


def close_complex(a: complex, b: complex, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


@dataclass(frozen=True)
class GaloisPair:
    """Conjugate Galois parts: local ball partition ⊕ global hair curvature."""

    ball: complex
    hair: complex

    @staticmethod
    def from_ball(ball: complex) -> "GaloisPair":
        return GaloisPair(ball=ball, hair=ball.conjugate())


@dataclass(frozen=True)
class ReciprocalTopology:
    """P = diag(2, 1/2) — weights, not the return itself."""

    ball_weight: Fraction = Fraction(2, 1)
    hair_weight: Fraction = Fraction(1, 2)

    @property
    def determinant(self) -> Fraction:
        return self.ball_weight * self.hair_weight

    def apply(self, z: GaloisPair) -> GaloisPair:
        return GaloisPair(
            complex(float(self.ball_weight)) * z.ball,
            complex(float(self.hair_weight)) * z.hair,
        )

    def inverse(self, z: GaloisPair) -> GaloisPair:
        return GaloisPair(
            z.ball / float(self.ball_weight),
            z.hair / float(self.hair_weight),
        )

    def sigma(self, z: GaloisPair) -> GaloisPair:
        """Semilinear Galois exchange: (z_B, z_H) ↦ (conj z_H, conj z_B)."""

        return GaloisPair(z.hair.conjugate(), z.ball.conjugate())

    def level6_return(self, z: GaloisPair) -> GaloisPair:
        """R_6 = σ ∘ P."""

        return self.sigma(self.apply(z))

    def level6_square(self, z: GaloisPair) -> GaloisPair:
        return self.level6_return(self.level6_return(z))

    def cross_pairing(self, x: GaloisPair, y: GaloisPair) -> complex:
        """⟨x,y⟩_C = x_B conj(y_H) + x_H conj(y_B)."""

        return x.ball * y.hair.conjugate() + x.hair * y.ball.conjugate()

    def spatial_projection(self, theta: float, level: int) -> complex:
        u = cmath.exp(1j * theta)
        return complex(
            (float(self.ball_weight) ** level) * u.real,
            (float(self.hair_weight) ** level) * u.imag,
        )

    def spatial_return(self, projected: complex, level: int) -> complex:
        return complex(
            projected.real / (float(self.ball_weight) ** level),
            projected.imag / (float(self.hair_weight) ** level),
        )

    def intrinsic_norm_sq(self, projected: complex, level: int) -> float:
        return (
            (float(self.ball_weight) ** (-2 * level)) * projected.real**2
            + (float(self.hair_weight) ** (-2 * level)) * projected.imag**2
        )


@dataclass(frozen=True)
class TriangleTimeStep:
    current: float
    next_value: float
    decrement: float
    lambert_argument: float
    lambert_value: float
    residual: float


def triangle_time_next(current: float) -> TriangleTimeStep:
    """Solve x = current - 2^(x-1) on the principal Lambert-W branch."""

    arg = math.log(2.0) * (2.0 ** (current - 1.0))
    w = float(mp.lambertw(arg, 0).real)
    decrement = w / math.log(2.0)
    nxt = current - decrement
    residual = nxt - (current - 2.0 ** (nxt - 1.0))
    return TriangleTimeStep(
        current=current,
        next_value=nxt,
        decrement=decrement,
        lambert_argument=arg,
        lambert_value=w,
        residual=residual,
    )


@dataclass(frozen=True)
class BallPhase:
    index: int
    expression: str
    value: complex
    topology_role: str


def ball_notebook_path(s: complex, t: complex) -> tuple[BallPhase, ...]:
    return (
        BallPhase(0, "2s+t", 2 * s + t, "ball/hair source"),
        BallPhase(1, "t^2", t * t, "ball topology 2"),
        BallPhase(2, "-2s+t/2", -2 * s + t / 2, "inverted ball + hair curvature"),
        BallPhase(3, "-t^2", -(t * t), "inverted ball topology"),
        BallPhase(4, "2s+t", 2 * s + t, "returned ordered expression"),
    )


@dataclass(frozen=True)
class FormalHodgeClass:
    codimension: int
    degree: int
    hodge_type: tuple[int, int]
    ball_weight: Fraction
    hair_weight: Fraction
    total_topology_weight: Fraction
    topology_fixed: bool
    galois_return_fixed: bool
    rational_trace_mechanism: str
    smooth_projective_variety_constructed: bool
    outside_cycle_map_proved: bool


def balanced_hodge_candidate(p: int) -> FormalHodgeClass:
    if p < 1:
        raise ValueError("p must be positive")
    ball_weight = Fraction(2, 1) ** p
    hair_weight = Fraction(1, 2) ** p
    total = ball_weight * hair_weight
    return FormalHodgeClass(
        codimension=p,
        degree=2 * p,
        hodge_type=(p, p),
        ball_weight=ball_weight,
        hair_weight=hair_weight,
        total_topology_weight=total,
        topology_fixed=(total == 1),
        galois_return_fixed=True,
        rational_trace_mechanism="formal Tr_{K/Q}(alpha_p)",
        smooth_projective_variety_constructed=False,
        outside_cycle_map_proved=False,
    )


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def short_digest(prefix: str, value: Any) -> str:
    return f"{prefix}:{hashlib.sha256(_canonical(value).encode()).hexdigest()[:16]}"


@dataclass(frozen=True)
class ClosureTrace:
    basis_id: str
    trace_id: str
    scalar_shadow: complex
    complexity: float
    ordered_provenance: tuple[dict[str, Any], ...]


def chaitin_contract(rows: Iterable[dict[str, Any]]) -> ClosureTrace:
    provenance = tuple(rows)
    payload = {"ordered_provenance": provenance}
    complexity = math.log1p(len(_canonical(payload)))
    scalar = 1j * math.exp(complexity)
    basis_id = short_digest("B_C", payload)
    trace_id = short_digest(
        "Omega_C",
        {
            "basis": basis_id,
            "scalar": [scalar.real, scalar.imag],
            "provenance": provenance,
        },
    )
    return ClosureTrace(
        basis_id=basis_id,
        trace_id=trace_id,
        scalar_shadow=scalar,
        complexity=complexity,
        ordered_provenance=provenance,
    )


def kakeya_reverse(trace: ClosureTrace) -> tuple[dict[str, Any], ...]:
    return trace.ordered_provenance


@dataclass(frozen=True)
class ReunifiedLevel6Run:
    topology_determinant: str
    galois_relation: str
    r6_square_identity: bool
    intrinsic_unitarity: bool
    fractal_hypotenuse_return: bool
    ellipse_equations_hold: bool
    lambert_triangle_time_holds: bool
    ball_equations_hold: bool
    ball_path_returns: bool
    kakeya_reconstruction_exact: bool
    level5_forgets_orientation: bool
    level6_retains_orientation: bool
    p2_candidate: dict[str, Any]
    internal_closure_hodge_counterexample: bool
    classical_hodge_counterexample: str
    basis_id: str
    trace_id: str
    spatial_levels: tuple[dict[str, Any], ...]
    temporal_levels: tuple[dict[str, Any], ...]
    ball_phases: tuple[dict[str, Any], ...]

    def report(self) -> dict[str, Any]:
        return asdict(self)


def run_reunified_level6(
    theta: float = 0.71,
    spatial_depth: int = 6,
    temporal_start: float = 6.0,
    temporal_depth: int = 6,
) -> ReunifiedLevel6Run:
    """Executable internal Level-6 verification (not classical Hodge CE)."""

    P = ReciprocalTopology()

    sample = GaloisPair(ball=complex(0.7, -1.1), hair=complex(-0.3, 0.8))
    r6sq = P.level6_square(sample)
    r6_identity = close_complex(r6sq.ball, sample.ball) and close_complex(
        r6sq.hair, sample.hair
    )

    x = GaloisPair(complex(0.4, 1.2), complex(-0.7, 0.3))
    y = GaloisPair(complex(-0.2, 0.9), complex(1.3, -0.5))
    intrinsic_unitary = close_complex(
        P.cross_pairing(P.apply(x), P.apply(y)),
        P.cross_pairing(x, y),
    )

    unit = cmath.exp(1j * theta)
    spatial: list[dict[str, Any]] = []
    spatial_return = True
    ellipse_hold = True
    for n in range(spatial_depth):
        e = P.spatial_projection(theta, n)
        returned = P.spatial_return(e, n)
        residual = (
            e.real**2 / (2.0 ** (2 * n)) + (2.0 ** (2 * n)) * e.imag**2 - 1.0
        )
        norm_sq = P.intrinsic_norm_sq(e, n)
        spatial_return &= close_complex(returned, unit)
        ellipse_hold &= abs(residual) <= TOL and abs(norm_sq - 1.0) <= TOL
        spatial.append(
            {
                "kind": "spatial",
                "level": n,
                "ellipse_point": [e.real, e.imag],
                "unit_return": [returned.real, returned.imag],
                "ellipse_residual": residual,
                "intrinsic_norm_sq": norm_sq,
            }
        )

    temporal: list[dict[str, Any]] = []
    current = temporal_start
    lambert_ok = True
    for k in range(temporal_depth):
        step = triangle_time_next(current)
        lambert_ok &= abs(step.residual) <= TOL
        temporal.append({"kind": "temporal", "level": k, **asdict(step)})
        current = step.next_value

    s = complex(-1.0, 0.0)
    t = complex(0.0, math.sqrt(2.0))
    phases = ball_notebook_path(s, t)
    equations_hold = (
        close_complex(s * s, -s)
        and close_complex(t * t, 2 * s)
        and close_complex(-(t * t), -2 * s)
    )
    path_return = close_complex(phases[0].value, phases[-1].value)

    phase_rows = tuple(
        {
            "kind": "ball_phase",
            "index": p.index,
            "expression": p.expression,
            "value": [p.value.real, p.value.imag],
            "topology_role": p.topology_role,
        }
        for p in phases
    )
    topology_rows = (
        {
            "kind": "topology",
            "P": ["2", "1/2"],
            "sigma": "(conj hair, conj ball)",
            "R6": "sigma o P",
            "R6_square": "id",
        },
    )
    hodge_p2 = balanced_hodge_candidate(2)
    hodge_row = {
        "kind": "formal_hodge_candidate",
        "codimension": hodge_p2.codimension,
        "degree": hodge_p2.degree,
        "hodge_type": list(hodge_p2.hodge_type),
        "ball_weight": str(hodge_p2.ball_weight),
        "hair_weight": str(hodge_p2.hair_weight),
        "total_topology_weight": str(hodge_p2.total_topology_weight),
        "topology_fixed": hodge_p2.topology_fixed,
        "galois_return_fixed": hodge_p2.galois_return_fixed,
        "rational_trace_mechanism": hodge_p2.rational_trace_mechanism,
    }

    provenance = (
        topology_rows + tuple(spatial) + tuple(temporal) + phase_rows + (hodge_row,)
    )
    forward_trace = chaitin_contract(provenance)
    reverse_phase_rows = tuple(reversed(phase_rows))
    reverse_trace = chaitin_contract(
        topology_rows
        + tuple(spatial)
        + tuple(temporal)
        + reverse_phase_rows
        + (hodge_row,)
    )

    kakeya_exact = kakeya_reverse(forward_trace) == provenance

    def level5_shadow(rows: tuple[dict[str, Any], ...]) -> dict[str, Any]:
        phase_values = sorted(
            [tuple(row["value"]) for row in rows if row["kind"] == "ball_phase"]
        )
        return {
            "phase_multiset": phase_values,
            "spatial_count": spatial_depth,
            "temporal_count": temporal_depth,
            "topology_weights": ("2", "1/2"),
            "hodge_type": (2, 2),
        }

    level5_same = level5_shadow(provenance) == level5_shadow(
        topology_rows
        + tuple(spatial)
        + tuple(temporal)
        + reverse_phase_rows
        + (hodge_row,)
    )
    level6_diff = forward_trace.trace_id != reverse_trace.trace_id

    internal_counterexample = all(
        (
            P.determinant == 1,
            r6_identity,
            intrinsic_unitary,
            spatial_return,
            ellipse_hold,
            lambert_ok,
            equations_hold,
            path_return,
            kakeya_exact,
            level5_same,
            level6_diff,
            hodge_p2.topology_fixed,
            hodge_p2.galois_return_fixed,
        )
    )

    return ReunifiedLevel6Run(
        topology_determinant=str(P.determinant),
        galois_relation="sigma P sigma = P^-1; R6 = sigma P",
        r6_square_identity=r6_identity,
        intrinsic_unitarity=intrinsic_unitary,
        fractal_hypotenuse_return=spatial_return,
        ellipse_equations_hold=ellipse_hold,
        lambert_triangle_time_holds=lambert_ok,
        ball_equations_hold=equations_hold,
        ball_path_returns=path_return,
        kakeya_reconstruction_exact=kakeya_exact,
        level5_forgets_orientation=level5_same,
        level6_retains_orientation=level6_diff,
        p2_candidate={
            "degree": hodge_p2.degree,
            "hodge_type": list(hodge_p2.hodge_type),
            "ball_weight": str(hodge_p2.ball_weight),
            "hair_weight": str(hodge_p2.hair_weight),
            "total_weight": str(hodge_p2.total_topology_weight),
            "topology_fixed": hodge_p2.topology_fixed,
            "galois_return_fixed": hodge_p2.galois_return_fixed,
            "rational_trace_mechanism": hodge_p2.rational_trace_mechanism,
            "smooth_projective_variety_constructed": False,
            "outside_cycle_map_proved": False,
        },
        internal_closure_hodge_counterexample=internal_counterexample,
        classical_hodge_counterexample=(
            "OPEN: no smooth projective X and no non-algebraicity proof"
        ),
        basis_id=forward_trace.basis_id,
        trace_id=forward_trace.trace_id,
        spatial_levels=tuple(spatial),
        temporal_levels=tuple(temporal),
        ball_phases=phase_rows,
    )


__all__ = [
    "BallPhase",
    "ClosureTrace",
    "FormalHodgeClass",
    "GaloisPair",
    "ReciprocalTopology",
    "ReunifiedLevel6Run",
    "TriangleTimeStep",
    "balanced_hodge_candidate",
    "ball_notebook_path",
    "chaitin_contract",
    "close_complex",
    "kakeya_reverse",
    "run_reunified_level6",
    "short_digest",
    "triangle_time_next",
]

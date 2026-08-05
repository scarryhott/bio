# Copyright 2026 scarryhott/bio contributors.
"""Executable constructors for project-derived closure topologies.

These are recurring return-disclosed structures already used across the ARC/AGI,
Closure–Chaitin, Black Mirror, and biological-coevolution projects. They are not
a fixed whitelist: every constructed topology must still be admitted, refused,
collapsed, or left OPEN through the return-unified runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .topology import VerificationTopology


@dataclass(frozen=True)
class DerivedTopologySpec:
    topology_id: str
    family: str
    statement: str
    constructor: Callable[..., VerificationTopology]
    epistemic_status: str = "PROJECT-DERIVED / RETURN-ADMITTED"


def _topology(
    topology_id: str,
    *,
    basis: dict[str, Any],
    closure: dict[str, Any],
    ball: dict[str, Any],
    hair: dict[str, Any],
    openings: tuple[str, ...],
    semantics: dict[str, Any],
) -> VerificationTopology:
    return VerificationTopology(
        topology_id=topology_id,
        basis_cycle=basis,
        closure_cycle=closure,
        ball_perspective=ball,
        hair_perspective=hair,
        encoding_topos={"topology": topology_id, "semantics": semantics},
        relation_topos={"topology": topology_id, "semantics": semantics},
        openings=list(openings),
        axiometric_shadows={"derived_topology": True, "identity_authority": False},
    )


def kakeya_contact_topology(
    *, occurrences: tuple[str, ...], contacts: tuple[tuple[str, str], ...]
) -> VerificationTopology:
    """Order local presentations through shared contacts, not supplied order."""
    contact_graph = {"occurrences": occurrences, "contacts": contacts}
    return _topology(
        "kakeya_contact",
        basis={"local_needles": occurrences, "contact_graph": contacts},
        closure={"contact_order": occurrences, "contact_graph": contacts},
        ball={"presentations": occurrences},
        hair={"shared_contacts": contacts},
        openings=("primitive_return_cells", "holistic_return_cell"),
        semantics={"law": "order_from_shared_contacts", "graph": contact_graph},
    )


def closure_chaitin_topology(
    *,
    labeled_occurrences: tuple[str, ...],
    primitive_cells: tuple[str, ...],
    holistic_cell: str,
) -> VerificationTopology:
    """Finite ordered-support topology; not classical numerical Chaitin Omega."""
    support = {
        "occurrences": labeled_occurrences,
        "primitive_cells": primitive_cells,
        "holistic_cell": holistic_cell,
    }
    return _topology(
        "closure_chaitin_ordered_support",
        basis={"labeled_occurrences": labeled_occurrences, "primitive_cells": primitive_cells},
        closure=support,
        ball={"local_string_presentations": labeled_occurrences},
        hair={"recursive_support": holistic_cell},
        openings=("next_configured_return",),
        semantics={"law": "primitive_returns_support_one_holistic_return", **support},
    )


def zero_infinity_topology(*, local_basis: Any, global_continuation: Any) -> VerificationTopology:
    return _topology(
        "zero_infinity_predual",
        basis={"zero_predual": local_basis, "fold": "0_to_infinity"},
        closure={"infinity_continuation": global_continuation, "fold": "0_to_infinity"},
        ball={"localized_projection": local_basis},
        hair={"open_continuation": global_continuation},
        openings=("repolarize",),
        semantics={"law": "originless_predual_before_local_polarization"},
    )


def ball_hair_topology(*, ball: Any, hair: Any, return_side: str = "ball") -> VerificationTopology:
    relation = {"ball": ball, "hair": hair, "return_side": return_side}
    return _topology(
        "local_ball_global_hair",
        basis=relation,
        closure=relation,
        ball={"state": ball, "return_side": return_side},
        hair={"state": hair, "complement_of": return_side},
        openings=("return_repartition",),
        semantics={"law": "local_global_are_perspectival_projections"},
    )


def partition_curvature_topology(
    *, left: Any, right: Any, observer_side: str
) -> VerificationTopology:
    involution = {"left": right, "right": left, "observer_side": observer_side}
    return _topology(
        "partition_curvature_return_side",
        basis=involution,
        closure=involution,
        ball={"observer_side": observer_side, "visible": left if observer_side == "left" else right},
        hair={"complement": right if observer_side == "left" else left},
        openings=("hidden_origin_attribution",),
        semantics={"law": "curvature_swaps_sides_and_returns_exactly"},
    )


def fold_glue_topology(*, carriers: tuple[str, ...], maintained_relation: str) -> VerificationTopology:
    relation = {"distinct_carriers": carriers, "maintained_relation": maintained_relation}
    return _topology(
        "fold_glue_nonidentical_recovery",
        basis=relation,
        closure=relation,
        ball={"local_sections": carriers},
        hair={"glued_relation": maintained_relation},
        openings=("cross_modal_return",),
        semantics={"law": "glue_without_identity_collapse"},
    )


def self_limit_topology(*, trajectory: tuple[Any, ...], recovered_relation: Any) -> VerificationTopology:
    relation = {"trajectory": trajectory, "recovered_relation": recovered_relation}
    return _topology(
        "self_limit_return_trajectory",
        basis=relation,
        closure=relation,
        ball={"initial_basis": trajectory[0] if trajectory else None},
        hair={"continuation": trajectory[1:]},
        openings=("next_self_limit",),
        semantics={"law": "identity_from_completed_return_trajectory"},
    )


def rotation_extension_topology(*, presentation: Any, transformed_return: Any) -> VerificationTopology:
    relation = {"presentation": presentation, "transformed_return": transformed_return}
    return _topology(
        "rotation_extension",
        basis=relation,
        closure=relation,
        ball={"rotation_presentation": presentation},
        hair={"extension_return": transformed_return},
        openings=("next_rotation_extension",),
        semantics={"law": "rotation_and_extension_are_paired_return_presentations"},
    )


def topos_turing_topology(*, relational_state: Any, invariant_state: Any) -> VerificationTopology:
    reciprocal = {
        "R": relational_state,
        "U": invariant_state,
        "A(C(R))": relational_state,
        "C(A(U))": invariant_state,
    }
    return _topology(
        "topos_turing_reciprocal_admissibility",
        basis=reciprocal,
        closure=reciprocal,
        ball={"relational_state": relational_state},
        hair={"invariant_state": invariant_state},
        openings=("next_mutual_admission",),
        semantics={"law": "computation_and_observable_state_co_determine_continuation"},
    )


def biological_nonidentical_topology(
    *, modalities: tuple[str, ...], returned_relation: str
) -> VerificationTopology:
    relation = {"modalities": modalities, "returned_relation": returned_relation}
    return _topology(
        "biological_nonidentical_recovery",
        basis=relation,
        closure=relation,
        ball={"modalities": modalities},
        hair={"returned_relation": returned_relation},
        openings=("next_biological_scale",),
        semantics={"law": "distinct_modalities_recover_one_relation_without_flattening"},
    )


DERIVED_TOPOLOGY_SPECS: tuple[DerivedTopologySpec, ...] = (
    DerivedTopologySpec("kakeya_contact", "contact order", "Shared contacts reconstruct local presentation order.", kakeya_contact_topology),
    DerivedTopologySpec("closure_chaitin_ordered_support", "contact order", "Primitive returned cells support one holistic return.", closure_chaitin_topology),
    DerivedTopologySpec("zero_infinity_predual", "predual closure", "Originless 0↔∞ fold precedes local polarization.", zero_infinity_topology),
    DerivedTopologySpec("local_ball_global_hair", "perspectival projection", "Local and global are return-repartitioned projections.", ball_hair_topology),
    DerivedTopologySpec("partition_curvature_return_side", "perspectival partition", "Curvature exchanges complementary return sides and returns exactly.", partition_curvature_topology),
    DerivedTopologySpec("fold_glue_nonidentical_recovery", "gluing", "Distinct carriers glue without identity collapse.", fold_glue_topology),
    DerivedTopologySpec("self_limit_return_trajectory", "trajectory", "Identity is recovered through the completed return trajectory.", self_limit_topology),
    DerivedTopologySpec("rotation_extension", "trajectory", "Rotation and extension are paired return presentations.", rotation_extension_topology),
    DerivedTopologySpec("topos_turing_reciprocal_admissibility", "mutual admissibility", "Computation and observed state co-determine continuation.", topos_turing_topology),
    DerivedTopologySpec("biological_nonidentical_recovery", "biological", "Distinct biological modalities recover one relation without flattening.", biological_nonidentical_topology),
)

DERIVED_TOPOLOGY_IDS = frozenset(spec.topology_id for spec in DERIVED_TOPOLOGY_SPECS)

# Copyright 2026 scarryhott/bio contributors.
"""Digest utilities.

A digest *references* an interaction closure; it cannot replace the ordered path.
Renaming labels that do not change partition–curvature relations must leave the
digest stable. Changing those relations must change the digest.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def digest(value: object, *, length: int = 24) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()[:length]


def interaction_digest(
    *,
    originless_basis: str,
    gate_id: str,
    ordered_support: tuple[str, ...],
    relation: str | None,
    resolution: str,
    next_opening: str | None,
    return_side: str | None = None,
    transformation_path: tuple[str, ...] = (),
    return_discrepancy: float | None = None,
    openings: tuple[str, ...] = (),
) -> str:
    """Reference digest for an interaction closure C(U)."""
    basis = {
        "originless_basis": originless_basis,
        "gate": gate_id,
        "support": ordered_support,
        "relation": relation,
        "resolution": resolution,
        "next_opening": next_opening,
        "return_side": return_side,
        "transformation_path": transformation_path,
        "return_discrepancy": return_discrepancy,
        "openings": openings,
    }
    return f"interaction_C:{digest(basis)}"


def partition_curvature_digest(
    partition: dict[str, Any],
    curvature: dict[str, Any],
) -> str:
    """Digest sensitive to partition–curvature relations, not cosmetic names."""
    payload = {
        "partition_structure": _strip_cosmetic_names(partition),
        "curvature_structure": _strip_cosmetic_names(curvature),
    }
    return digest(payload)


def _strip_cosmetic_names(value: Any) -> Any:
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if key in {"label", "display_name", "name", "cosmetic_id"}:
                continue
            out[key] = _strip_cosmetic_names(item)
        return out
    if isinstance(value, (list, tuple)):
        return [_strip_cosmetic_names(v) for v in value]
    return value

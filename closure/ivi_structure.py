# Copyright 2026 scarryhott/bio contributors.
"""Transcript-derived IVI–NRR structure spine (ours — not Radical Numerics).

Loads docs/transcript_closure/closure_structure_map.json and exposes the IVI
ladder and core structures as finite, auditable objects for the bio runtime.
Does not claim classical RH, Chaitin Ω, or Kakeya proofs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

STRUCTURE_MAP_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "transcript_closure"
    / "closure_structure_map.json"
)


@dataclass(frozen=True)
class IVILevel:
    level_id: str
    name: str
    rules: tuple[str, ...]
    enables: str | None = None
    equals: str | None = None


@dataclass(frozen=True)
class CoreStructure:
    structure_id: str
    name: str
    rule: str
    depends_on: tuple[str, ...] = ()
    pairs: tuple[str, ...] = ()
    level: str | None = None


@lru_cache(maxsize=1)
def load_structure_map(path: str | None = None) -> dict[str, Any]:
    target = Path(path) if path else STRUCTURE_MAP_PATH
    with target.open(encoding="utf-8") as handle:
        return json.load(handle)


def thesis_statement(data: dict[str, Any] | None = None) -> str:
    return str((data or load_structure_map())["thesis"])


def ivi_ladder(data: dict[str, Any] | None = None) -> tuple[IVILevel, ...]:
    rows = []
    for row in (data or load_structure_map())["ladder"]:
        rows.append(
            IVILevel(
                level_id=str(row["id"]),
                name=str(row["name"]),
                rules=tuple(row.get("rules") or ()),
                enables=row.get("enables"),
                equals=row.get("equals"),
            )
        )
    return tuple(rows)


def core_structures(data: dict[str, Any] | None = None) -> tuple[CoreStructure, ...]:
    rows = []
    for row in (data or load_structure_map())["core_structures"]:
        rows.append(
            CoreStructure(
                structure_id=str(row["id"]),
                name=str(row["name"]),
                rule=str(row["rule"]),
                depends_on=tuple(row.get("depends_on") or ()),
                pairs=tuple(row.get("pairs") or ()),
                level=row.get("level"),
            )
        )
    return tuple(rows)


def predual_pairs(data: dict[str, Any] | None = None) -> tuple[str, ...]:
    for structure in core_structures(data):
        if structure.structure_id == "predual":
            return structure.pairs
    return ()


def ownership_declaration() -> dict[str, Any]:
    return {
        "closure_agi_owner": "scarryhott/bio transcript thesis (IVI–NRR)",
        "radical_numerics_role": "external_architecture_comparator_only",
        "rnd1_is_our_model": False,
        "local_kakeya_owner": "our_ivi_connected_return",
        "global_chaitin_owner": "our_binding_of_goel_dna_environment",
        "structure_map": str(STRUCTURE_MAP_PATH.relative_to(STRUCTURE_MAP_PATH.parents[1])),
    }


def spine_digest() -> dict[str, Any]:
    data = load_structure_map()
    return {
        "thesis": thesis_statement(data),
        "ivi_levels": [level.level_id for level in ivi_ladder(data)],
        "core_structure_ids": [row.structure_id for row in core_structures(data)],
        "predual_pairs": list(predual_pairs(data)),
        "bridge_ids": [row["id"] for row in data.get("bridge_rules", [])],
        "ownership": ownership_declaration(),
    }


__all__ = [
    "STRUCTURE_MAP_PATH",
    "CoreStructure",
    "IVILevel",
    "core_structures",
    "ivi_ladder",
    "load_structure_map",
    "ownership_declaration",
    "predual_pairs",
    "spine_digest",
    "thesis_statement",
]

# Copyright 2026 scarryhott/bio contributors.
"""Paper architectures + open datasets layered under our Closure AGI.

External work is not RND1-weights-only. Referenced papers (Goel, Radical
Numerics / Evo / Omnii) and related open datasets supply architectures and
held-out returns that compose under our admission — weights are optional.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from .goel_operator import PolymeraseMode, infer_polymerase_mode

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "benchmarks" / "paper_architecture_data_catalog.json"
TENSION_PRIOR_PATH = ROOT / "benchmarks" / "data_priors" / "wuite_bustamante_tension_prior.json"


@dataclass(frozen=True)
class PaperArchitecture:
    architecture_id: str
    family: str
    role: str
    ownership: str
    epistemic_status: str
    data_bindings: tuple[str, ...]
    papers: tuple[dict[str, Any], ...]
    places_on_top_of: tuple[str, ...]
    module: str | None = None
    weights: tuple[str, ...] = ()


@dataclass(frozen=True)
class OpenDataset:
    dataset_id: str
    kind: str
    adapter_status: str
    benchmark_families: tuple[str, ...]
    paper_architectures: tuple[str, ...]
    url: str | None = None
    local_path: str | None = None
    return_type: str | None = None


@lru_cache(maxsize=1)
def load_catalog(path: str | None = None) -> dict[str, Any]:
    target = Path(path) if path else CATALOG_PATH
    with target.open(encoding="utf-8") as handle:
        return json.load(handle)


def paper_architectures(data: dict[str, Any] | None = None) -> tuple[PaperArchitecture, ...]:
    rows = []
    for row in (data or load_catalog())["paper_architectures"]:
        rows.append(
            PaperArchitecture(
                architecture_id=str(row["id"]),
                family=str(row["family"]),
                role=str(row["role"]),
                ownership=str(row["ownership"]),
                epistemic_status=str(row["epistemic_status"]),
                data_bindings=tuple(row.get("data_bindings") or ()),
                papers=tuple(row.get("papers") or ()),
                places_on_top_of=tuple(row.get("places_on_top_of") or ()),
                module=row.get("module"),
                weights=tuple(row.get("weights") or ()),
            )
        )
    return tuple(rows)


def open_datasets(data: dict[str, Any] | None = None) -> tuple[OpenDataset, ...]:
    rows = []
    for row in (data or load_catalog())["datasets"]:
        rows.append(
            OpenDataset(
                dataset_id=str(row["id"]),
                kind=str(row["kind"]),
                adapter_status=str(row["adapter_status"]),
                benchmark_families=tuple(row.get("benchmark_families") or ()),
                paper_architectures=tuple(row.get("paper_architectures") or ()),
                url=row.get("url") or row.get("hf"),
                local_path=row.get("local_path"),
                return_type=row.get("return_type"),
            )
        )
    return tuple(rows)


def stack_declaration(data: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = data or load_catalog()
    return {
        "stack": catalog["stack"],
        "composition_rules": catalog["composition_rules"],
        "rnd1_weights_are_not_the_whole_external_stack": True,
        "paper_architecture_count": len(catalog["paper_architectures"]),
        "dataset_count": len(catalog["datasets"]),
    }


def load_wuite_tension_prior(path: Path | None = None) -> dict[str, Any]:
    target = path or TENSION_PRIOR_PATH
    with target.open(encoding="utf-8") as handle:
        return json.load(handle)


def goel_mode_from_wuite_tension(tension_pN: float) -> PolymeraseMode:
    """Map published tension landmarks into Goel operator modes.

    Uses Wuite/Bustamante Nature 2000 landmarks (stall ~34 pN, exo ~>40 pN)
    as a literature prior for the Goel DNA×environment architecture layer.
    """

    prior = load_wuite_tension_prior()
    stall = float(prior["landmarks"]["stall_approx_pN"])
    exo = float(prior["landmarks"]["exonuclease_acceleration_above_pN"])
    # Normalize pN into the finite [0,1] tension used by infer_polymerase_mode.
    if tension_pN >= exo:
        return PolymeraseMode.EXONUCLEASE
    if tension_pN >= stall:
        return PolymeraseMode.STALLED
    # Map 0..stall onto 0..switching band below exonuclease threshold.
    normalized = min(max(tension_pN / stall, 0.0), 0.94)
    return infer_polymerase_mode(tension=normalized, switching_tension=0.95, stall_tension=0.95)


def datasets_for_architecture(architecture_id: str) -> tuple[OpenDataset, ...]:
    return tuple(
        row for row in open_datasets() if architecture_id in row.paper_architectures
    )


def architectures_for_dataset(dataset_id: str) -> tuple[PaperArchitecture, ...]:
    return tuple(
        row for row in paper_architectures() if dataset_id in row.data_bindings
    )


def local_dataset_availability() -> dict[str, dict[str, Any]]:
    """Report which catalog datasets are locally present vs download-open."""

    from .dataset_adapters import open_dataset_cache_availability

    cache = open_dataset_cache_availability()
    out: dict[str, dict[str, Any]] = {}
    for row in open_datasets():
        present = False
        path = row.local_path
        if row.local_path:
            present = (ROOT / row.local_path).exists()
        cache_hit = cache.get(row.dataset_id, {})
        if cache_hit.get("local_present"):
            present = True
            path = cache_hit.get("local_path") or path
        status = row.adapter_status
        if cache_hit.get("local_present"):
            status = "CACHED_ONLINE_SAMPLE"
        out[row.dataset_id] = {
            "adapter_status": status,
            "catalog_adapter_status": row.adapter_status,
            "local_path": path,
            "local_present": present,
            "url": row.url,
            "kind": row.kind,
            "benchmark_families": list(row.benchmark_families),
            "cache": cache_hit or None,
        }
    return out


def paper_data_layer_digest() -> dict[str, Any]:
    catalog = load_catalog()
    availability = local_dataset_availability()
    local_ready = [k for k, v in availability.items() if v["local_present"]]
    download_open = [
        k
        for k, v in availability.items()
        if str(v.get("catalog_adapter_status") or v["adapter_status"]).startswith("OPEN_")
        and not v["local_present"]
    ]
    cached_online = [
        k
        for k, v in availability.items()
        if v.get("cache") and v["cache"].get("local_present")
    ]
    return {
        "stack": stack_declaration(catalog),
        "paper_architectures": [a.architecture_id for a in paper_architectures(catalog)],
        "datasets": [d.dataset_id for d in open_datasets(catalog)],
        "local_ready_datasets": local_ready,
        "download_open_datasets": download_open,
        "cached_online_samples": cached_online,
        "availability": availability,
        "goel_bound": any(
            a.architecture_id == "goel-dna-environment-motor"
            for a in paper_architectures(catalog)
        ),
        "rnd1_is_only_optional_weight_layer": True,
    }


__all__ = [
    "CATALOG_PATH",
    "OpenDataset",
    "PaperArchitecture",
    "TENSION_PRIOR_PATH",
    "architectures_for_dataset",
    "datasets_for_architecture",
    "goel_mode_from_wuite_tension",
    "load_catalog",
    "load_wuite_tension_prior",
    "local_dataset_availability",
    "open_datasets",
    "paper_architectures",
    "paper_data_layer_digest",
    "stack_declaration",
]

# Copyright 2026 scarryhott/bio contributors.
"""Radical Numerics open surface inventory (repos + optional RND1 weights).

RND1 / spear / dInfer / assets remain Radical Numerics external open artifacts.
They are never our Closure AGI. This module inventories and caches small open
metadata so combined Goel+RN runs can cite a concrete open surface.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .digest import digest
from .return_unified_runtime import probe_weights_available

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "benchmarks" / "data_cache" / "rn_open"
UPSTREAM_COMMIT = (ROOT / "UPSTREAM_COMMIT").read_text(encoding="utf-8").strip()
USER_AGENT = "bio-closure-agi/0.1 (rn-open-surface)"

# Public Radical Numerics GitHub org surface relevant to this programme.
RN_OPEN_REPOS: tuple[dict[str, str], ...] = (
    {
        "id": "RND1",
        "url": "https://github.com/RadicalNumerics/RND1",
        "role": "diffusion language model inference (vendored in rnd/)",
        "license": "Apache-2.0",
        "programme_use": "local_kakeya_presentation_carrier",
    },
    {
        "id": "spear",
        "url": "https://github.com/RadicalNumerics/spear",
        "role": "Structured Primitives for Efficient Architecture Research",
        "license": "Apache-2.0",
        "programme_use": "reported_open_infra_not_vendored",
    },
    {
        "id": "dInfer",
        "url": "https://github.com/RadicalNumerics/dInfer",
        "role": "Efficient inference framework for diffusion LMs",
        "license": "Apache-2.0",
        "programme_use": "reported_open_infra_not_vendored",
    },
    {
        "id": "assets",
        "url": "https://github.com/RadicalNumerics/assets",
        "role": "Brand/assets repo",
        "license": "unspecified",
        "programme_use": "provenance_only",
    },
)

RND1_HF_MODEL = "radicalnumerics/RND1-Base-0910"
RND1_HF_URL = f"https://huggingface.co/{RND1_HF_MODEL}"


@dataclass
class RnOpenSurface:
    """Concrete open Radical Numerics surface available to combined runs."""

    generated_at: str
    org: str = "https://github.com/RadicalNumerics"
    vendored_rnd1_commit: str = UPSTREAM_COMMIT
    repos: list[dict[str, Any]] = field(default_factory=list)
    rnd1_weights: dict[str, Any] = field(default_factory=dict)
    rnd1_config_local: str | None = None
    ownership: dict[str, Any] = field(default_factory=dict)
    surface_digest: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "org": self.org,
            "vendored_rnd1_commit": self.vendored_rnd1_commit,
            "repos": list(self.repos),
            "rnd1_weights": dict(self.rnd1_weights),
            "rnd1_config_local": self.rnd1_config_local,
            "ownership": dict(self.ownership),
            "surface_digest": self.surface_digest,
            "not_our_closure_agi": True,
        }


def _http_get_text(url: str, *, timeout: float = 60.0) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _http_get_json(url: str, *, timeout: float = 60.0) -> Any:
    return json.loads(_http_get_text(url, timeout=timeout))


def fetch_rnd1_open_config(*, force: bool = False) -> Path:
    """Download RND1 HF config.json (small open-weights metadata, not 30B shards)."""

    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / "RND1-Base-0910.config.json"
    if out.exists() and not force:
        return out
    url = f"https://huggingface.co/{RND1_HF_MODEL}/resolve/main/config.json"
    text = _http_get_text(url)
    out.write_text(text, encoding="utf-8")
    meta = {
        "model_id": RND1_HF_MODEL,
        "file": "config.json",
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "note": "open config only; safetensor shards not downloaded by this adapter",
    }
    (CACHE / "RND1-Base-0910.config.meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    return out


def fetch_rn_repo_readme(repo_id: str, *, force: bool = False) -> Path | None:
    """Cache README excerpt from an RN open repo for provenance."""

    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"{repo_id}.README.excerpt.md"
    if out.exists() and not force:
        return out
    for branch in ("main", "master"):
        url = f"https://raw.githubusercontent.com/RadicalNumerics/{repo_id}/{branch}/README.md"
        try:
            text = _http_get_text(url)
        except (HTTPError, URLError, TimeoutError, OSError):
            continue
        out.write_text(text[:4000] + ("\n…\n" if len(text) > 4000 else ""), encoding="utf-8")
        return out
    return None


def inventory_rn_open_surface(*, fetch: bool = True, force: bool = False) -> RnOpenSurface:
    """Build the Radical Numerics open surface used by combined Goel runs."""

    repos: list[dict[str, Any]] = []
    for row in RN_OPEN_REPOS:
        entry = dict(row)
        if fetch:
            path = fetch_rn_repo_readme(row["id"], force=force)
            entry["readme_cache"] = (
                str(path.relative_to(ROOT)) if path and path.exists() else None
            )
        if row["id"] == "RND1":
            entry["vendored_path"] = "rnd/"
            entry["vendored_commit"] = UPSTREAM_COMMIT
            entry["hf_model"] = RND1_HF_MODEL
        repos.append(entry)

    config_path = None
    if fetch:
        try:
            config_path = fetch_rnd1_open_config(force=force)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            config_path = None
            config_error = str(exc)
        else:
            config_error = None
    else:
        candidate = CACHE / "RND1-Base-0910.config.json"
        config_path = candidate if candidate.exists() else None
        config_error = None

    weight_probe = {
        "model_id": RND1_HF_MODEL,
        "hf_url": RND1_HF_URL,
        "local_weights_present": probe_weights_available(
            {"open_weights": True, "model_id": RND1_HF_MODEL, "id": "rnd1-base-0910"}
        ),
        "config_cached": bool(config_path and config_path.exists()),
        "config_error": config_error,
        "epistemic": (
            "OPEN_WEIGHTS_OPTIONAL — 30B safetensors not required for combined "
            "paper-logic + mock-sampler path; config metadata is open"
        ),
    }

    ownership = {
        "rnd1_is_our_model": False,
        "spear_is_our_model": False,
        "dinfer_is_our_model": False,
        "closure_agi": "ours_transcript_ivi_nrr",
        "radical_numerics_role": "external_open_architecture_and_infra",
        "goel_role": "parallel_paper_logic_global_chaitin_hair",
    }
    surface = RnOpenSurface(
        generated_at=datetime.now(timezone.utc).isoformat(),
        repos=repos,
        rnd1_weights=weight_probe,
        rnd1_config_local=(
            str(config_path.relative_to(ROOT)) if config_path and config_path.exists() else None
        ),
        ownership=ownership,
    )
    surface.surface_digest = digest(
        {
            "commit": surface.vendored_rnd1_commit,
            "repos": [r["id"] for r in repos],
            "weights": weight_probe,
            "config": surface.rnd1_config_local,
        }
    )
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "rn_open_surface.json").write_text(
        json.dumps(surface.to_dict(), indent=2) + "\n", encoding="utf-8"
    )
    return surface


__all__ = [
    "CACHE",
    "RND1_HF_MODEL",
    "RN_OPEN_REPOS",
    "RnOpenSurface",
    "fetch_rnd1_open_config",
    "fetch_rn_repo_readme",
    "inventory_rn_open_surface",
]

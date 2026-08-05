# Copyright 2026 scarryhott/bio contributors.
"""Our Closure verification admission against stated frontier paper results.

PRIMARY programme goal:

    M_ClosureBio  vs  FrontierPaperResults
    inside return-unified admission

Frontier paper scores / preview tables are axiometric shadows. They never
certify C. RND1-30B is recorded only as a finite AI substrate test — not bio
closure.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .dataset_adapters import load_all_open_episodes
from .digest import digest
from .our_closure_verify import verify_our_closure
from .return_unified_runtime import (
    architecture_from_system,
    load_finite_bio_episodes,
    reunify_episode,
)
from .self_verification import ClosureVerificationStatus

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "benchmarks" / "frontier_paper_results.json"
FINITE_EPISODES = ROOT / "benchmarks" / "finite_bio_returns.json"
HOLISTIC_ARTIFACT = ROOT / "benchmarks" / "results" / "cloud_holistic_unified.json"

OUR_SYSTEM = {
    "id": "bio-closure-independent",
    "family": "black-mirror-closure",
    "biological_native": True,
    "open_weights": False,
    "ownership": "scarryhott-bio-transcript-thesis",
    "adapter": "closure.independent_model:UnifiedClosureArchitecturalLoop",
    "epistemic_status": "RERUNNABLE_FINITE_KERNEL",
    "availability": "repository-local",
    "role": "OUR self-contained Closure AGI — primary bio admission",
}


@dataclass
class FrontierClaimView:
    claim_id: str
    family: str
    epistemic_status: str
    our_admission_role: str
    benchmark_families: tuple[str, ...]
    scores_certify_closure: bool
    stated_results: dict[str, Any]
    programme_chapter: str | None = None


def load_frontier_catalog(path: Path | None = None) -> dict[str, Any]:
    target = path or CATALOG_PATH
    return json.loads(target.read_text(encoding="utf-8"))


def frontier_claims(data: dict[str, Any] | None = None) -> list[FrontierClaimView]:
    catalog = data or load_frontier_catalog()
    out: list[FrontierClaimView] = []
    for row in catalog["claims"]:
        out.append(
            FrontierClaimView(
                claim_id=str(row["id"]),
                family=str(row["family"]),
                epistemic_status=str(row["epistemic_status"]),
                our_admission_role=str(row["our_admission_role"]),
                benchmark_families=tuple(row.get("benchmark_families") or ()),
                scores_certify_closure=bool(row.get("scores_certify_closure", False)),
                stated_results=dict(row.get("stated_results") or {}),
                programme_chapter=row.get("programme_chapter"),
            )
        )
    return out


def _our_admission_on_episodes(episodes: list) -> dict[str, Any]:
    architecture = architecture_from_system(OUR_SYSTEM, weights_available=True)
    by_family: dict[str, dict[str, int]] = {}
    rows: list[dict[str, Any]] = []
    for episode in episodes:
        receipt = reunify_episode(architecture, episode)
        fam = episode.benchmark_id
        bucket = by_family.setdefault(
            fam, {"verified": 0, "open": 0, "rejected": 0, "total": 0}
        )
        bucket["total"] += 1
        status = receipt.verification_status
        if status is ClosureVerificationStatus.VERIFIED and receipt.joint_arm_status == "VERIFIED":
            bucket["verified"] += 1
            label = "VERIFIED"
        elif status is ClosureVerificationStatus.REJECTED:
            bucket["rejected"] += 1
            label = "REJECTED"
        else:
            bucket["open"] += 1
            label = receipt.joint_arm_status
        rows.append(
            {
                "episode_id": episode.episode_id,
                "benchmark_id": fam,
                "role": episode.role,
                "joint_arm_status": receipt.joint_arm_status,
                "verification_status": receipt.verification_status.value,
                "admission_label": label,
            }
        )
    return {"by_benchmark_family": by_family, "episodes": rows}


def _rnd1_finite_ai_test_record(catalog: dict[str, Any]) -> dict[str, Any]:
    claim = next(
        c for c in catalog["claims"] if c["id"] == "rnd1-30b-finite-ai-substrate-test"
    )
    artifact_present = HOLISTIC_ARTIFACT.exists()
    return {
        "role": "FINITE_AI_SUBSTRATE_TEST_NOT_BIO_CLOSURE",
        "claim_id": claim["id"],
        "epistemic_status": claim["epistemic_status"],
        "stated_results": claim["stated_results"],
        "local_holistic_artifact_present": artifact_present,
        "local_artifact": claim.get("local_artifact"),
        "programme_chapter": claim.get("programme_chapter"),
        "not_bio_closure": True,
        "note": (
            "RND1-30B four-mode hybrid is a single finite AI/language substrate "
            "test under our hooks. It does not decide biological closure admission."
        ),
    }


def run_frontier_paper_admission(
    *,
    include_open_data: bool = True,
    episodes_path: Path | None = None,
) -> dict[str, Any]:
    """Primary run: our Closure admission against stated frontier paper results."""

    catalog = load_frontier_catalog()
    priority = catalog["programme_priority"]
    claims = frontier_claims(catalog)

    # Gate: our internal reunify+verify must hold.
    our_report = verify_our_closure(episodes_path=episodes_path or FINITE_EPISODES)
    episodes = load_finite_bio_episodes(episodes_path or FINITE_EPISODES)
    if include_open_data:
        episodes = list(episodes) + list(load_all_open_episodes())

    admission = _our_admission_on_episodes(episodes)

    # Map each frontier claim to our admission on overlapping benchmark families.
    claim_rows: list[dict[str, Any]] = []
    for claim in claims:
        if claim.our_admission_role == "FINITE_AI_TEST_NOT_BIO_CLOSURE":
            claim_rows.append(
                {
                    "claim_id": claim.claim_id,
                    "family": claim.family,
                    "epistemic_status": claim.epistemic_status,
                    "our_admission_role": claim.our_admission_role,
                    "overlap_families": [],
                    "our_admission_summary": None,
                    "stated_results": claim.stated_results,
                    "scores_certify_closure": False,
                    "comparison": "EXCLUDED_FROM_BIO_PRIMARY — finite AI substrate test only",
                }
            )
            continue

        overlap = {
            fam: admission["by_benchmark_family"].get(fam)
            for fam in claim.benchmark_families
            if fam in admission["by_benchmark_family"]
        }
        verified = sum((v or {}).get("verified", 0) for v in overlap.values())
        total = sum((v or {}).get("total", 0) for v in overlap.values())
        claim_rows.append(
            {
                "claim_id": claim.claim_id,
                "family": claim.family,
                "epistemic_status": claim.epistemic_status,
                "our_admission_role": claim.our_admission_role,
                "overlap_families": list(claim.benchmark_families),
                "our_admission_summary": {
                    "verified": verified,
                    "total": total,
                    "by_family": overlap,
                },
                "stated_results": claim.stated_results,
                "scores_certify_closure": claim.scores_certify_closure,
                "comparison": (
                    "OUR_ADMISSION_ON_HELD_OUT_RETURNS vs PAPER_STATED_SHADOW"
                    if total
                    else "PAPER_STATED_ONLY_NO_LOCAL_OVERLAP_YET"
                ),
            }
        )

    bio_claims = [
        r for r in claim_rows if r["our_admission_role"] != "FINITE_AI_TEST_NOT_BIO_CLOSURE"
    ]
    bio_ok = our_report.passed and all(
        r["scores_certify_closure"] is False for r in bio_claims
    )
    has_verified = any(
        (r.get("our_admission_summary") or {}).get("verified", 0) > 0 for r in bio_claims
    )
    primary_closed = bio_ok and has_verified

    verdict = (
        "OUR_CLOSURE_ADMISSION_VS_FRONTIER_PAPERS_MEASURED"
        if primary_closed
        else "OUR_CLOSURE_ADMISSION_VS_FRONTIER_PAPERS_INCOMPLETE"
    )

    return {
        "schema_version": "1.0",
        "protocol": "our-closure-admission-vs-frontier-paper-results",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "programme_priority": priority,
        "relation": (
            "M_ClosureBio vs FrontierPaperResults "
            "inside return-unified admission; "
            "RND1-30B = FINITE_AI_SUBSTRATE_TEST_NOT_BIO_CLOSURE"
        ),
        "verdict": verdict,
        "passed": primary_closed,
        "our_closure_gate": {
            "verdict": our_report.verdict,
            "passed": our_report.passed,
        },
        "our_admission": admission,
        "frontier_claims": claim_rows,
        "rnd1_30b_finite_ai_test": _rnd1_finite_ai_test_record(catalog),
        "epistemic": {
            "primary_goal": "our_closure_verification_admission_vs_frontier_paper_results",
            "frontier_scores_are_shadows": True,
            "rnd1_30b_is_bio_closure": False,
            "rnd1_30b_role": "FINITE_AI_SUBSTRATE_TEST_NOT_BIO_CLOSURE",
            "omnii": "REPORTED_ONLY",
            "evo_live_weights": "OPEN",
            "delta_c_q": "OPEN",
        },
        "architecture_digest": digest(
            {
                "priority": priority,
                "verdict": verdict,
                "gate": our_report.verdict,
                "claims": [c.claim_id for c in claims],
            }
        ),
    }


__all__ = [
    "CATALOG_PATH",
    "FrontierClaimView",
    "frontier_claims",
    "load_frontier_catalog",
    "run_frontier_paper_admission",
]

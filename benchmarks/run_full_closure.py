#!/usr/bin/env python3
"""Run full return-unified closure over open architectures and finite bio data.

Reunifies suite manifest systems with held-out biological return episodes into
admissible verification. Does not invent Evo/RND1 likelihoods when weights are
absent: those arms stay OPEN for architecture execution while data+topology may
still VERIFIED under the independent return path.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmarks.plan_radical_numerics_suite import build_plan, load_manifest, summarize
from closure.return_unified_runtime import (
    architecture_from_system,
    load_finite_bio_episodes,
    receipt_to_dict,
    reunify_episode,
)

DEFAULT_EPISODES = Path(__file__).with_name("finite_bio_returns.json")
DEFAULT_OUT = Path(__file__).with_name("results") / "full_closure_reunified.json"


def run_full_closure(
    *,
    include_nonbiological: bool = False,
    include_reported: bool = False,
    ours_only: bool = False,
    episodes_path: Path = DEFAULT_EPISODES,
    negative_controls: bool = True,
) -> dict[str, Any]:
    manifest = load_manifest()
    systems = {row["id"]: row for row in manifest["systems"]}
    plan = build_plan(
        manifest,
        include_nonbiological=include_nonbiological,
        include_reported=include_reported,
    )
    if ours_only:
        plan = [arm for arm in plan if arm.system_id == "bio-closure-independent"]
    episodes = load_finite_bio_episodes(episodes_path)
    by_benchmark: dict[str, list] = {}
    for episode in episodes:
        if not negative_controls and episode.role.startswith("negative-control"):
            continue
        by_benchmark.setdefault(episode.benchmark_id, []).append(episode)

    receipts: list[dict[str, Any]] = []
    for arm in plan:
        system = systems[arm.system_id]
        architecture = architecture_from_system(system)
        for episode in by_benchmark.get(arm.benchmark_id, []):
            receipt = reunify_episode(architecture, episode)
            receipts.append(receipt_to_dict(receipt))

    joint_counts = Counter(row["joint_arm_status"] for row in receipts)
    verification_counts = Counter(row["verification_status"] for row in receipts)
    learned_counts = Counter(row["learned_claim_status"] for row in receipts)
    goel_counts = Counter(
        row["goel_operator_status"] for row in receipts if row.get("goel_operator_status")
    )
    dual_counts = Counter(
        row["dual_kakeya_goel_status"]
        for row in receipts
        if row.get("dual_kakeya_goel_status")
    )

    kernel_verified = [
        row
        for row in receipts
        if row["system_id"] == "bio-closure-independent"
        and row["joint_arm_status"] == "VERIFIED"
        and not str(row["episode_id"]).endswith("open-self")
        and "open-self" not in row["episode_id"]
    ]
    kernel_controls_open = [
        row
        for row in receipts
        if row["system_id"] == "bio-closure-independent"
        and row["episode_id"].endswith("open-self")
    ]

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol": "return-unified-full-closure-reunification",
        "relation": "(C_t, E_t, A_legal,t) ↔_C (A_t, E_{t+1}, R_t, V_t, C_{t+1})",
        "manifest_status_date": manifest["status_date"],
        "plan_summary": summarize(manifest, plan),
        "episodes_path": str(episodes_path.relative_to(ROOT))
        if episodes_path.is_relative_to(ROOT)
        else str(episodes_path),
        "episode_count": len(episodes),
        "receipt_count": len(receipts),
        "joint_arm_status_counts": dict(sorted(joint_counts.items())),
        "verification_status_counts": dict(sorted(verification_counts.items())),
        "learned_claim_status_counts": dict(sorted(learned_counts.items())),
        "goel_operator_status_counts": dict(sorted(goel_counts.items())),
        "dual_kakeya_goel_status_counts": dict(sorted(dual_counts.items())),
        "kernel_positive_verified": len(kernel_verified),
        "kernel_negative_control_open_or_rejected": len(
            [r for r in kernel_controls_open if r["verification_status"] != "VERIFIED"]
        ),
        "epistemic": {
            "finite_kernel_data_topology_reunification": "MEASURED"
            if kernel_verified
            else "OPEN",
            "external_open_weight_biological_suite": "OPEN",
            "full_biological_unification_agi_execution": "OPEN",
            "note": (
                "VERIFIED joint arms require independent Bio Closure kernel on "
                "held-out returns. Evo/OpenGenome2 arms reunify architecture "
                "carriers and data into admission but stay OPEN until weights "
                "and adapters execute inside the same return."
            ),
        },
        "receipts": receipts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-nonbiological", action="store_true")
    parser.add_argument("--include-reported", action="store_true")
    parser.add_argument(
        "--ours-only",
        action="store_true",
        help="restrict to bio-closure-independent (prefer benchmarks/verify_our_closure.py)",
    )
    parser.add_argument("--episodes", type=Path, default=DEFAULT_EPISODES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--skip-negative-controls", action="store_true")
    parser.add_argument("--json", action="store_true", help="print summary JSON to stdout")
    args = parser.parse_args()

    report = run_full_closure(
        include_nonbiological=args.include_nonbiological,
        include_reported=args.include_reported,
        ours_only=args.ours_only,
        episodes_path=args.episodes,
        negative_controls=not args.skip_negative_controls,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    summary = {
        "out": str(args.out),
        "receipt_count": report["receipt_count"],
        "joint_arm_status_counts": report["joint_arm_status_counts"],
        "verification_status_counts": report["verification_status_counts"],
        "goel_operator_status_counts": report["goel_operator_status_counts"],
        "dual_kakeya_goel_status_counts": report["dual_kakeya_goel_status_counts"],
        "kernel_positive_verified": report["kernel_positive_verified"],
        "epistemic": report["epistemic"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(
            f"wrote {args.out} "
            f"receipts={report['receipt_count']} "
            f"kernel_verified={report['kernel_positive_verified']} "
            f"joint={report['joint_arm_status_counts']}"
        )


if __name__ == "__main__":
    main()

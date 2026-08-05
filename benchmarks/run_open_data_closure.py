#!/usr/bin/env python3
"""Reunify downloaded/online open-dataset episodes through closure runtime.

Our kernel uses one shared C_t across episodes (stateful biological closure).
External Evo/Omnii arms reunify as carriers without owning C.
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
from closure.dataset_adapters import (
    fetch_all_open_samples,
    load_all_open_episodes,
    load_cache_manifest,
    receipt_to_dict,
)
from closure.return_unified_runtime import (
    architecture_from_system,
    receipt_to_dict as reunify_receipt_to_dict,
    reunify_episode,
)
from closure.stateful_biological_closure import (
    StatefulBiologicalClosure,
    order_episodes_for_stateful_run,
)

DEFAULT_OUT = Path(__file__).with_name("results") / "open_data_closure_reunified.json"


def run_open_data_closure(
    *,
    fetch: bool = False,
    force_fetch: bool = False,
    ours_only: bool = False,
    include_reported: bool = False,
    stateful: bool = True,
) -> dict[str, Any]:
    fetch_receipts = []
    if fetch or not load_all_open_episodes():
        fetch_receipts = [
            receipt_to_dict(r)
            for r in fetch_all_open_samples(force=force_fetch)
        ]

    episodes = load_all_open_episodes()
    if not episodes:
        raise RuntimeError(
            "no open-dataset episodes available; run benchmarks/download_open_datasets.py"
        )

    if stateful and ours_only:
        from closure.stateful_biological_closure import run_stateful_biological_closure

        stateful_report = run_stateful_biological_closure(episodes)
        return {
            "schema_version": "1.1",
            "protocol": "open-dataset-stateful-biological-closure",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "fetch_receipts": fetch_receipts,
            "cache_manifest": load_cache_manifest(),
            "stateful_biological_closure": stateful_report,
            "episode_count": stateful_report["episode_count"],
            "receipt_count": stateful_report["episode_count"],
            "joint_arm_status_counts": {
                "VERIFIED": stateful_report["verified_joint_arms"],
            },
            "kernel_positive_verified": stateful_report["verified_joint_arms"],
            "epistemic": {
                **stateful_report["epistemic"],
                "open_datasets_executed": True,
                "stateful_chain": stateful_report["stateful_chain"],
            },
            "receipts": stateful_report["steps"],
        }

    manifest = load_manifest()
    systems = {row["id"]: row for row in manifest["systems"]}
    plan = build_plan(
        manifest,
        include_nonbiological=False,
        include_reported=include_reported,
    )
    if ours_only:
        plan = [arm for arm in plan if arm.system_id == "bio-closure-independent"]

    by_benchmark: dict[str, list] = {}
    for episode in order_episodes_for_stateful_run(episodes):
        by_benchmark.setdefault(episode.benchmark_id, []).append(episode)

    our_state = StatefulBiologicalClosure() if stateful else None
    # Track which episodes already entered the shared our-kernel chain.
    seen_our: set[str] = set()
    receipts: list[dict[str, Any]] = []

    for arm in plan:
        system = systems[arm.system_id]
        architecture = architecture_from_system(system)
        for episode in by_benchmark.get(arm.benchmark_id, []):
            if arm.system_id == "bio-closure-independent" and our_state is not None:
                if episode.episode_id in seen_our:
                    continue
                step = our_state.run_episode(episode)
                seen_our.add(episode.episode_id)
                row = step.to_dict()
            else:
                receipt = reunify_episode(architecture, episode)
                row = reunify_receipt_to_dict(receipt)
            row["dataset_role"] = episode.role
            receipts.append(row)

    # Ensure every episode hit the shared our-kernel chain once (plan may miss some).
    if our_state is not None:
        for episode in order_episodes_for_stateful_run(episodes):
            if episode.episode_id not in seen_our:
                step = our_state.run_episode(episode)
                seen_our.add(episode.episode_id)
                row = step.to_dict()
                row["dataset_role"] = episode.role
                receipts.append(row)
        our_state.derive_cross_dataset_hypotheses()
        stateful_summary = our_state.report()
    else:
        stateful_summary = None

    joint = Counter(r["joint_arm_status"] for r in receipts)
    verification = Counter(r["verification_status"] for r in receipts)
    learned = Counter(r.get("learned_claim_status", "n/a") for r in receipts)
    by_dataset: Counter[str] = Counter()
    for ep in episodes:
        ds = ep.role.split(":", 1)[-1] if ":" in ep.role else ep.role
        by_dataset[ds] += 1

    kernel_verified = [
        r
        for r in receipts
        if r.get("system_id") == "bio-closure-independent"
        and r["joint_arm_status"] == "VERIFIED"
    ]
    return {
        "schema_version": "1.1",
        "protocol": "open-dataset-return-unified-closure",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "relation": (
            "C_0 --E_i--> C_i on our kernel (stateful); "
            "external arms reunify carriers without owning C"
        ),
        "fetch_receipts": fetch_receipts,
        "cache_manifest": load_cache_manifest(),
        "plan_summary": summarize(manifest, plan),
        "episode_count": len(episodes),
        "episodes_by_dataset": dict(by_dataset),
        "receipt_count": len(receipts),
        "joint_arm_status_counts": dict(joint),
        "verification_status_counts": dict(verification),
        "learned_claim_status_counts": dict(learned),
        "kernel_positive_verified": len(kernel_verified),
        "stateful_biological_closure": stateful_summary,
        "epistemic": {
            "open_datasets_executed": True,
            "full_opengenome2_corpus_mirrored": False,
            "opengenome2_family_via": "ncbi-nucleotide-online-stand-in",
            "evo_weights_executed": False,
            "stateful_chain": bool(stateful_summary and stateful_summary.get("stateful_chain")),
            "not_aggregate_of_separate_closes": bool(
                stateful_summary and stateful_summary.get("stateful_chain")
            ),
            "omnii": "reported_only" if include_reported else "excluded",
            "note": (
                "Our kernel carries one C_t across open-data episodes. "
                "Evo arms stay OPEN_ARCHITECTURE_WEIGHTS_ABSENT until weights execute."
            ),
        },
        "receipts": receipts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="fetch/refresh samples first")
    parser.add_argument("--force-fetch", action="store_true")
    parser.add_argument("--ours-only", action="store_true")
    parser.add_argument("--include-reported", action="store_true")
    parser.add_argument("--no-stateful", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = run_open_data_closure(
        fetch=args.fetch or args.force_fetch,
        force_fetch=args.force_fetch,
        ours_only=args.ours_only,
        include_reported=args.include_reported,
        stateful=not args.no_stateful,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    summary = {
        "out": str(args.out),
        "episode_count": report["episode_count"],
        "episodes_by_dataset": report.get("episodes_by_dataset"),
        "receipt_count": report["receipt_count"],
        "joint_arm_status_counts": report["joint_arm_status_counts"],
        "kernel_positive_verified": report["kernel_positive_verified"],
        "stateful_chain": report.get("epistemic", {}).get("stateful_chain"),
        "epistemic": report["epistemic"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(
            f"OPEN_DATA_CLOSURE episodes={report['episode_count']} "
            f"receipts={report['receipt_count']} "
            f"kernel_verified={report['kernel_positive_verified']} "
            f"stateful={report.get('epistemic', {}).get('stateful_chain')} → {args.out}"
        )
        if report.get("episodes_by_dataset"):
            print("datasets:", report["episodes_by_dataset"])
        print("joint:", report["joint_arm_status_counts"])
        sc = report.get("stateful_biological_closure") or {}
        if sc.get("cross_dataset_hypotheses"):
            print("cross-dataset hypotheses:", len(sc["cross_dataset_hypotheses"]), "(δ_C=OPEN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

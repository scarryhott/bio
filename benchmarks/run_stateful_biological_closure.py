#!/usr/bin/env python3
"""Run one shared C_t across all biological episodes (stateful closure).

Replaces Aggregate(Close(E_i)) with Close(E_1 ↔ … ↔ E_n) under a single
UnifiedClosureArchitecturalLoop + UnifiedAxiometry, then derives cross-dataset
hypotheses (δ_C=OPEN until independent return).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from closure.dataset_adapters import load_all_open_episodes
from closure.return_unified_runtime import load_finite_bio_episodes
from closure.stateful_biological_closure import run_stateful_biological_closure

DEFAULT_FINITE = Path(__file__).with_name("finite_bio_returns.json")
DEFAULT_OUT = Path(__file__).with_name("results") / "stateful_biological_closure.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finite", type=Path, default=DEFAULT_FINITE)
    parser.add_argument("--include-open-data", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    episodes = list(load_finite_bio_episodes(args.finite))
    if args.include_open_data:
        episodes.extend(load_all_open_episodes())

    report = run_stateful_biological_closure(episodes)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    summary = {
        "out": str(args.out),
        "verdict": report["verdict"],
        "passed": report["passed"],
        "stateful_chain": report["stateful_chain"],
        "episode_count": report["episode_count"],
        "admitted_unities": report["admitted_unities"],
        "hypotheses_open": report["hypotheses_open"],
        "final_c_t": report["final_c_t"][:16] + "…",
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        status = "PASS" if report["passed"] else "FAIL"
        print(
            f"{status} {report['verdict']} "
            f"episodes={report['episode_count']} "
            f"admitted={report['admitted_unities']} "
            f"hypotheses_open={report['hypotheses_open']} → {args.out}"
        )
        print("chain: C_0 → E_1 → C_1 → … (not Aggregate(Close(E_i)))")
        for h in report["cross_dataset_hypotheses"]:
            print(f"  [δ_C={h['delta_c']}] {h['hypothesis_id']}: {h['proposition'][:88]}…")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

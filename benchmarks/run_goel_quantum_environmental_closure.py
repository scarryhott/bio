#!/usr/bin/env python3
# Copyright 2026 scarryhott/bio contributors.
"""Derive Goel quantum–environmental closure via bio levels + data chart."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from closure.dataset_adapters import load_all_open_episodes  # noqa: E402
from closure.goel_quantum_environmental_closure import (  # noqa: E402
    derive_goel_quantum_environmental_closure,
)
from closure.return_unified_runtime import load_finite_bio_episodes  # noqa: E402

DEFAULT_OUT = Path(__file__).with_name("results") / "goel_quantum_environmental_closure.json"
EPISODES = ROOT / "benchmarks" / "finite_bio_returns.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--include-open-data", action="store_true")
    parser.add_argument("--no-stateful", action="store_true")
    args = parser.parse_args()

    episodes = load_finite_bio_episodes(EPISODES)
    if args.include_open_data:
        try:
            episodes = list(episodes) + list(load_all_open_episodes())
        except Exception as exc:  # noqa: BLE001 — cache may be partial
            print(f"open-data skipped: {exc}", file=sys.stderr)

    report = derive_goel_quantum_environmental_closure(
        episodes, include_stateful=not args.no_stateful
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    summary = {
        "verdict": report["verdict"],
        "passed": report["passed"],
        "classical_goel_hair_admitted": report["summary"]["classical_goel_hair_admitted"],
        "quantum_environmental_closed": report["summary"]["quantum_environmental_closed"],
        "delta_c_q_open": report["summary"]["delta_c_q_open"],
        "level6": report["level6_reunified"]["verdict"],
        "basis_id": report["level6_reunified"]["basis_id"],
        "trace_id": report["level6_reunified"]["trace_id"],
        "output": str(args.out),
    }
    print(json.dumps(summary, indent=2))
    print(
        f"{'PASS' if report['passed'] else 'OPEN'} {report['verdict']} "
        f"classical_hair={report['summary']['classical_goel_hair_admitted']} "
        f"Q_closed={report['summary']['quantum_environmental_closed']} "
        f"δ_C(Q)_OPEN={report['summary']['delta_c_q_open']} → {args.out}"
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""PRIMARY: our Closure verification admission vs stated frontier paper results.

RND1-30B is not this run — it is a finite AI substrate test only
(see cloud_holistic_unified.json / Chapter A).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from closure.frontier_paper_admission import run_frontier_paper_admission

DEFAULT_OUT = Path(__file__).with_name("results") / "frontier_paper_admission.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-open-data", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = run_frontier_paper_admission(include_open_data=not args.no_open_data)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    summary = {
        "out": str(args.out),
        "verdict": report["verdict"],
        "passed": report["passed"],
        "primary_goal": report["epistemic"]["primary_goal"],
        "rnd1_30b_is_bio_closure": report["epistemic"]["rnd1_30b_is_bio_closure"],
        "our_closure_gate": report["our_closure_gate"],
        "rnd1_30b_finite_ai_test": report["rnd1_30b_finite_ai_test"]["role"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        status = "PASS" if report["passed"] else "FAIL"
        print(f"{status} {report['verdict']} → {args.out}")
        print("PRIMARY:", report["epistemic"]["primary_goal"])
        print(
            "RND1-30B:",
            report["rnd1_30b_finite_ai_test"]["role"],
            "(not bio closure)",
        )
        print(
            "our gate:",
            report["our_closure_gate"]["verdict"],
            "passed=",
            report["our_closure_gate"]["passed"],
        )
        for row in report["frontier_claims"]:
            if row["our_admission_role"] == "FINITE_AI_TEST_NOT_BIO_CLOSURE":
                continue
            summ = row.get("our_admission_summary") or {}
            print(
                f"  [{row['epistemic_status']}] {row['claim_id']}: "
                f"our_verified={summ.get('verified', 0)}/{summ.get('total', 0)} "
                f"— {row['comparison']}"
            )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

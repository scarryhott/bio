#!/usr/bin/env python3
"""Integrate external Radical Numerics tests — gated on our Closure AGI verify.

Runs only after OUR_CLOSURE_REUNIFIED_VERIFIED. External systems remain
comparators (RND1/Evo/Omnii), never our model.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from closure.external_suite import run_external_suite

DEFAULT_OUT = Path(__file__).with_name("results") / "external_suite_integrated.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--skip-nonbiological", action="store_true")
    parser.add_argument("--skip-reported", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--force-without-gate",
        action="store_true",
        help="debug only — do not use for authoritative integration",
    )
    args = parser.parse_args()

    report = run_external_suite(
        include_nonbiological=not args.skip_nonbiological,
        include_reported=not args.skip_reported,
        require_gate=not args.force_without_gate,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    summary = {
        "out": str(args.out),
        "verdict": report["verdict"],
        "passed": report["passed"],
        "checks_passed": report["summary"]["checks_passed"],
        "checks_total": report["summary"]["checks_total"],
        "failed": report["summary"]["failed"],
        "epistemic": report.get("epistemic"),
        "ownership": report.get("ownership"),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        status = "PASS" if report["passed"] else "FAIL"
        print(
            f"{status} {report['verdict']} "
            f"{report['summary']['checks_passed']}/{report['summary']['checks_total']} "
            f"→ {args.out}"
        )
        if report["summary"]["failed"]:
            print("failed:", ", ".join(report["summary"]["failed"]))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

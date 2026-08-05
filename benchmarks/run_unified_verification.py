#!/usr/bin/env python3
"""Reveal admissible-data architecture via holistic unified verification."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from closure.unified_verification import run_unified_verification

DEFAULT_OUT = Path(__file__).with_name("results") / "unified_verification.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = run_unified_verification()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    primary = report["primary_product"]
    summary = {
        "out": str(args.out),
        "verdict": report["verdict"],
        "passed": report["passed"],
        "primary_product": primary["kind"],
        "architecture_digest": primary.get("architecture_digest"),
        "delta_c_q": report["epistemic"]["delta_c_q_biological_double_slit"],
        "double_slit_inside_model": report["epistemic"][
            "biological_double_slit_relative_return"
        ],
        "instrument_layers_passed": report["instrument_layers_passed"],
        "instrument_layers_total": report["instrument_layers_total"],
        "failed_layers": report["failed_layers"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        status = "PASS" if report["passed"] else "FAIL"
        print(
            f"{status} {report['verdict']} "
            f"primary={primary['kind']} "
            f"instruments={report['instrument_layers_passed']}/"
            f"{report['instrument_layers_total']} "
            f"δ_C(Q)={report['epistemic']['delta_c_q_biological_double_slit']} "
            f"→ {args.out}"
        )
        print("  derivation steps:")
        for step in primary["general_derivation"][:4]:
            print(f"    - {step['step_id']}: {step['statement'][:72]}…")
        print(f"    … ({len(primary['general_derivation'])} steps total)")
        print(
            "  double-slit:",
            report["biological_double_slit_relative_return"]["kind"],
            "inside our closure model;",
            f"δ_C(Q)={report['biological_double_slit_relative_return']['delta_c_q']}",
        )
        for layer in report["layers"]:
            mark = "x" if layer["ok"] else " "
            print(f"  [{mark}] instrument/{layer['layer_id']}: {layer['verdict']}")
        if report["failed_layers"]:
            print("failed:", ", ".join(report["failed_layers"]))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

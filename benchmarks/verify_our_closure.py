#!/usr/bin/env python3
"""Reunify and verify OUR Closure AGI before external architecture/data tests.

Excludes Radical Numerics RND1/Evo/Omnii from pass criteria.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from closure.our_closure_verify import report_to_dict, verify_our_closure

DEFAULT_OUT = Path(__file__).with_name("results") / "our_closure_reunified_verified.json"
DEFAULT_EPISODES = Path(__file__).with_name("finite_bio_returns.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=Path, default=DEFAULT_EPISODES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = verify_our_closure(episodes_path=args.episodes)
    payload = report_to_dict(report)
    payload["generated_at"] = datetime.now(timezone.utc).isoformat()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = {
        "out": str(args.out),
        "verdict": payload["verdict"],
        "passed": payload["passed"],
        "checks_passed": payload["summary"]["checks_passed"],
        "checks_total": payload["summary"]["checks_total"],
        "failed": payload["summary"]["failed"],
        "external_architectures_deferred": True,
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        status = "PASS" if payload["passed"] else "FAIL"
        print(
            f"{status} {payload['verdict']} "
            f"{payload['summary']['checks_passed']}/{payload['summary']['checks_total']} "
            f"→ {args.out}"
        )
        if payload["summary"]["failed"]:
            print("failed:", ", ".join(payload["summary"]["failed"]))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

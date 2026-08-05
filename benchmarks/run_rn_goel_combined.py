#!/usr/bin/env python3
"""Combine Radical Numerics open surface + Goel paper logic under our Closure AGI.

Uses:
  - RND1 open code (± optional weights; mock sampler if 30B absent)
  - RN org open repos (spear, dInfer, …) as cached provenance
  - Goel DNA×env + Wuite tension prior from papers
  - held-out finite bio returns and/or downloaded open-dataset samples
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
from closure.rn_goel_combined import run_rn_goel_combined

DEFAULT_FINITE = Path(__file__).with_name("finite_bio_returns.json")
DEFAULT_OUT = Path(__file__).with_name("results") / "rn_goel_combined.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finite", type=Path, default=DEFAULT_FINITE)
    parser.add_argument(
        "--include-open-data",
        action="store_true",
        help="also reunify downloaded TraitGym/RNAGym/ClinVar/… episodes",
    )
    parser.add_argument("--no-fetch-rn", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    episodes = load_finite_bio_episodes(args.finite)
    if args.include_open_data:
        episodes = list(episodes) + list(load_all_open_episodes())

    report = run_rn_goel_combined(
        episodes,
        fetch_rn_surface=not args.no_fetch_rn,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    summary = {
        "out": str(args.out),
        "episode_count": report["episode_count"],
        "combined_status_counts": report["combined_status_counts"],
        "our_kernel_verified": report["our_kernel_verified"],
        "goel_bound_episodes": report["goel_bound_episodes"],
        "rnd1_proposal_mode": report["rnd1_proposal"]["mode"],
        "rn_repos": report["stack"]["radical_numerics_open"]["repos"],
        "architecture_digest": report["architecture_digest"],
        "epistemic": report["epistemic"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(
            f"RN+GOEL COMBINED episodes={report['episode_count']} "
            f"our_verified={report['our_kernel_verified']} "
            f"goel_bound={report['goel_bound_episodes']} "
            f"rnd1={report['rnd1_proposal']['mode']} → {args.out}"
        )
        print("stack: our C ← Goel papers ← RN open (RND1/spear/dInfer) ← returns")
        print("combined:", report["combined_status_counts"])
        print("RN repos:", ", ".join(report["stack"]["radical_numerics_open"]["repos"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

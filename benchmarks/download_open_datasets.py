#!/usr/bin/env python3
"""Download / fetch online samples for catalogued open biological datasets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from closure.dataset_adapters import fetch_all_open_samples, receipt_to_dict
from closure.paper_data_layer import paper_data_layer_digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="refetch even if cached")
    parser.add_argument("--n", type=int, default=3, help="rows per HF/NCBI sample")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    receipts = fetch_all_open_samples(force=args.force, n=args.n)
    digest = paper_data_layer_digest()
    summary = {
        "fetched": [receipt_to_dict(r) for r in receipts],
        "cached_online_samples": digest.get("cached_online_samples"),
        "local_ready_datasets": digest.get("local_ready_datasets"),
        "download_open_datasets": digest.get("download_open_datasets"),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        for row in summary["fetched"]:
            print(
                f"{'OK' if row['ok'] else 'FAIL'} {row['dataset_id']} "
                f"n={row['n_rows']} via {row['transport']} → {row['local_path']} "
                f"[{row['epistemic_status']}]"
            )
        print("local_ready:", ", ".join(digest["local_ready_datasets"]))
        print("still_download_open:", ", ".join(digest["download_open_datasets"]) or "(none)")
    return 0 if all(r.ok for r in receipts) else 1


if __name__ == "__main__":
    raise SystemExit(main())

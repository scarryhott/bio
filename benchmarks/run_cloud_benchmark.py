#!/usr/bin/env python3
"""Cloud GPU runner for the RND1 closure benchmark (30B).

Designed for a GPU VM / Modal / HF Job with:
  - CUDA + enough VRAM for radicalnumerics/RND1-Base-0910
  - disk for HF cache (~60GB+ recommended for bf16)

Usage on a provisioned GPU host (repo checked out):

  pip install -e ".[test]"
  python benchmarks/run_cloud_benchmark.py \\
    --modes off probe full \\
    --seeds 1 2 3 4 5 \\
    --steps 32 \\
    --out benchmarks/results/cloud_latest.json

This script does not invent performance claims; it writes OPEN EMPIRICAL CLAIM artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="radicalnumerics/RND1-Base-0910")
    parser.add_argument("--modes", nargs="+", default=["off", "probe", "full"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[1, 2, 3, 4, 5])
    parser.add_argument("--steps", type=int, default=32)
    parser.add_argument("--prompt", default="The living cell maintains")
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "benchmarks" / "results" / "cloud_latest.json",
    )
    args = parser.parse_args()

    try:
        import torch
    except ImportError:
        print("torch required", file=sys.stderr)
        return 1

    print("torch", torch.__version__)
    print("cuda_available", torch.cuda.is_available())
    if not torch.cuda.is_available():
        print(
            "ERROR: no CUDA GPU visible. Provision a GPU host before running the 30B benchmark.",
            file=sys.stderr,
        )
        return 2
    for i in range(torch.cuda.device_count()):
        p = torch.cuda.get_device_properties(i)
        print(f"gpu{i}", p.name, f"{p.total_memory/1024**3:.1f} GiB")

    cmd = [
        sys.executable,
        str(ROOT / "benchmarks" / "compare_rnd1_closure.py"),
        "--model",
        args.model,
        "--modes",
        *args.modes,
        "--seeds",
        *[str(s) for s in args.seeds],
        "--steps",
        str(args.steps),
        "--prompt",
        args.prompt,
        "--out",
        str(args.out),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    print("Running:", " ".join(cmd))
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, env=env)
    elapsed = time.time() - t0
    meta = {
        "epistemic_status": "OPEN EMPIRICAL CLAIM",
        "elapsed_s": elapsed,
        "returncode": proc.returncode,
        "cuda": True,
        "model": args.model,
        "modes": args.modes,
        "seeds": args.seeds,
    }
    meta_path = args.out.with_suffix(".meta.json")
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2))
    print("Wrote", meta_path)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

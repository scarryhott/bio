#!/usr/bin/env python3
"""Live verify against https://github.com/RadicalNumerics/RND1.

Clones (or reuses) the upstream tree, checks commit + pristine hashes, and runs
baseline off-mode behavioral equivalence.

  python scripts/verify_radicalnumerics.py
  RND1_UPSTREAM_PATH=/path/to/RND1 python scripts/verify_radicalnumerics.py
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "docs" / "upstream" / "RND1_MANIFEST.json").read_text())
ORG = "https://github.com/RadicalNumerics"
REPO = "https://github.com/RadicalNumerics/RND1.git"
COMMIT = MANIFEST["upstream_commit"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_upstream() -> Path:
    env = os.environ.get("RND1_UPSTREAM_PATH")
    if env:
        return Path(env)
    cached = Path("/tmp/RN_verify/RND1_live")
    if cached.exists() and (cached / "rnd" / "sampling.py").exists():
        return cached
    dest = Path(tempfile.mkdtemp(prefix="rnd1_verify_")) / "RND1"
    subprocess.check_call(["git", "clone", "--depth", "1", REPO, str(dest)])
    return dest


def main() -> int:
    print(f"Organization: {ORG}")
    print(f"Upstream:     {REPO}")
    print(f"Expect commit:{COMMIT}")
    upstream = ensure_upstream()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=upstream).decode().strip()
    print(f"Live commit:  {head}")
    if head != COMMIT:
        print("WARNING: live HEAD differs from recorded UPSTREAM_COMMIT / manifest")
        print("  Re-copy pristine files and refresh docs/upstream/RND1_MANIFEST.json if intentional.")

    failures = []
    for rel, expected in MANIFEST["pristine_files"].items():
        bio = ROOT / rel
        live = upstream / rel
        if not live.exists():
            failures.append(f"missing upstream {rel}")
            continue
        live_hash = sha256(live)
        bio_hash = sha256(bio)
        if live_hash != expected:
            failures.append(f"manifest stale for {rel}: live={live_hash} expected={expected}")
        if bio_hash != expected:
            failures.append(f"bio pristine drift {rel}: bio={bio_hash} expected={expected}")
        else:
            print(f"OK pristine {rel}")

    for rel in MANIFEST["intentionally_modified"]:
        if sha256(ROOT / rel) == sha256(upstream / rel):
            failures.append(f"expected intentional delta missing: {rel}")
        else:
            print(f"OK modified {rel}")

    # Behavioral off-mode equivalence
    env = os.environ.copy()
    env["RND1_UPSTREAM_PATH"] = str(upstream)
    env["PYTHONPATH"] = str(ROOT)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_radicalnumerics_verify.py"],
        cwd=ROOT,
        env=env,
    )
    if proc.returncode != 0:
        failures.append("pytest radicalnumerics verify failed")

    if failures:
        print("FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: integrated and verified against Radical Numerics / RND1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

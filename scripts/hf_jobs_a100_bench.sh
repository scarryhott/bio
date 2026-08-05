#!/usr/bin/env bash
set -euo pipefail
pip install -q -U pip hf_transfer
pip install -q "transformers>=4.45" accelerate rich huggingface_hub
cd /bio
export PYTHONPATH=/bio:${PYTHONPATH:-}
python - <<'PY'
import torch
print("torch", torch.__version__, "cuda", torch.cuda.is_available())
if torch.cuda.is_available():
    p = torch.cuda.get_device_properties(0)
    print("gpu", p.name, round(p.total_memory / 1024**3, 1), "GiB")
PY
mkdir -p /tmp/bio_results
# Full unified verification = 30B holistic compare across all sampler modes.
python benchmarks/compare_rnd1_closure.py \
  --model radicalnumerics/RND1-Base-0910 \
  --modes off probe full full-connected-return \
  --seeds 1 2 3 4 5 \
  --steps 32 \
  --out /tmp/bio_results/cloud_holistic_unified.json
python - <<'PY'
from huggingface_hub import HfApi
import os, time, json, shutil
from pathlib import Path
api = HfApi()
run_id = os.environ.get("JOB_ID") or time.strftime("%Y%m%dT%H%M%SZ")
src = Path("/tmp/bio_results/cloud_holistic_unified.json")
# Also write cloud_latest.json alias for continuity
shutil.copy(src, "/tmp/bio_results/cloud_latest.json")
meta = {
    "epistemic_status": "OPEN EMPIRICAL CLAIM until quality criteria close",
    "verification_kind": "FULL_UNIFIED_30B_HOLISTIC_COMPARISON",
    "modes": ["off", "probe", "full", "full-connected-return"],
    "model": "radicalnumerics/RND1-Base-0910",
    "job_id": run_id,
    "note": (
        "Finite reunification is not this closure. "
        "This artifact is the full unified verification: 30B holistic mode compare."
    ),
}
Path("/tmp/bio_results/holistic_meta.json").write_text(json.dumps(meta, indent=2))
api.upload_folder(
    folder_path="/tmp/bio_results",
    repo_id="scarryhott/bio-closure-benchmarks",
    repo_type="dataset",
    path_in_repo=f"runs/hfjobs_a100_holistic_{run_id}",
)
print("uploaded to scarryhott/bio-closure-benchmarks", run_id)
PY

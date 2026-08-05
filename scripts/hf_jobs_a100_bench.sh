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
python benchmarks/compare_rnd1_closure.py \
  --model radicalnumerics/RND1-Base-0910 \
  --modes off probe full \
  --seeds 1 2 3 4 5 \
  --steps 32 \
  --out /tmp/bio_results/cloud_latest.json
python - <<'PY'
from huggingface_hub import HfApi
import os, time
api = HfApi()
run_id = os.environ.get("JOB_ID") or time.strftime("%Y%m%dT%H%M%SZ")
api.upload_folder(
    folder_path="/tmp/bio_results",
    repo_id="scarryhott/bio-closure-benchmarks",
    repo_type="dataset",
    path_in_repo=f"runs/hfjobs_a100_{run_id}",
)
print("uploaded to scarryhott/bio-closure-benchmarks", run_id)
PY

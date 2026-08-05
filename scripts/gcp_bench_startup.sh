#!/usr/bin/env bash
# Startup script for GCP L4 benchmark VM — runs RND1 closure compare then shuts down.
set -euo pipefail
exec > >(tee -a /var/log/bio-bench.log) 2>&1
echo "=== bio closure cloud bench start $(date -Is) ==="
export HOME=/root
export HF_HOME=/mnt/disks/model-cache/hf
mkdir -p "$HF_HOME" /opt/bio-results

# NVIDIA driver wait
for i in $(seq 1 60); do
  if command -v nvidia-smi >/dev/null && nvidia-smi >/dev/null 2>&1; then
    nvidia-smi
    break
  fi
  echo "waiting for GPU driver ($i)"
  sleep 10
done

apt-get update -y
apt-get install -y git python3-pip python3-venv

cd /opt
if [[ ! -d bio ]]; then
  git clone https://github.com/scarryhott/bio.git bio
fi
# Overlay tarball if present (local uncommitted tree)
if [[ -f /opt/bio-src.tgz ]]; then
  rm -rf /opt/bio
  mkdir -p /opt/bio
  tar -xzf /opt/bio-src.tgz -C /opt/bio
fi

cd /opt/bio
python3 -m venv /opt/venv
source /opt/venv/bin/activate
pip install -U pip
pip install torch --index-url https://download.pytorch.org/whl/cu124
pip install -e ".[test]" bitsandbytes accelerate transformers rich

python benchmarks/compare_rnd1_closure.py \
  --model radicalnumerics/RND1-Base-0910 \
  --modes off probe full \
  --seeds 1 2 3 4 5 \
  --steps 32 \
  --load-in-4bit \
  --out /opt/bio-results/cloud_latest.json

cp /opt/bio-results/cloud_latest.json /opt/bio/benchmarks/results/cloud_latest.json || true
echo "=== bench done $(date -Is) ==="
# Keep instance up for result pull; do not auto-delete here.

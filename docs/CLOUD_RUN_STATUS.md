# Cloud 30B run status

## Verdict

```text
CLOSED_FULL_MODEL_CAUSAL_INTEGRATION
OPEN_HOLISTIC_QUALITY_ADVANTAGE
```

See `docs/STAGE_STATUS.md` for the full epistemic reading.

## Hugging Face Jobs — COMPLETED

| Field | Value |
|-------|-------|
| Account | `scarryhott` |
| Job | [`6a736104a00abefd4b293eef`](https://huggingface.co/jobs/scarryhott/6a736104a00abefd4b293eef) (`a100-large`, ~145 s wall) |
| Results dataset | [`scarryhott/bio-closure-benchmarks`](https://huggingface.co/datasets/scarryhott/bio-closure-benchmarks/tree/main/runs/hfjobs_a100_6a736104a00abefd4b293eef) |
| Local artifact | `benchmarks/results/cloud_latest.json` |
| Entrypoint | `scripts/hf_jobs_a100_bench.sh` |

| Mode | Mean latency | vs `off` | Note |
|------|-------------:|----------|------|
| `off` | 4.77 s | — | Baseline |
| `probe` | 4.70 s | identical tokens | Non-interfering observation (961 open events) |
| `full` | 4.98 s | **63/68** diffs every seed | Causal actuation; ~4.4 % latency overhead |

Hardware: NVIDIA A100-SXM4-80GB, bf16, ≈58 GB allocated.

Not a quality win. Lower `coherence_shadow` under `full` keeps holistic advantage OPEN.

## Earlier path notes

* First inline `bash` launch → ERROR 127 (command mangled); fixed via script mount.
* Credits required after initial 402.
* GCP `tnc-stream-clean-8264` VM `bio-rnd1-bench` (L4) remains **STOPPED** after OOM; disk billable until deleted.

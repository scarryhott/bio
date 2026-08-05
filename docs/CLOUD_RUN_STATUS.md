# Cloud 30B run status

## Full unified verification (= 30B holistic comparison)

**Definition:** full unified verification is the 30B holistic mode compare
(`off | probe | full | full-connected-return`) on `RND1-Base-0910`.

| Field | Value |
|-------|-------|
| Job | [`6a7372606b79c09949c23580`](https://huggingface.co/jobs/scarryhott/6a7372606b79c09949c23580) **COMPLETED** |
| Results | [`hfjobs_a100_holistic_…`](https://huggingface.co/datasets/scarryhott/bio-closure-benchmarks/tree/main/runs/hfjobs_a100_holistic_6a7372606b79c09949c23580) |
| Local | `benchmarks/results/cloud_holistic_unified.json` |
| Thesis | `docs/UNIFICATION_THESIS.md` |

| Mode | Mean latency | Open | Coherence | vs `off` |
|------|-------------:|-----:|----------:|----------|
| off | 5.80 s | 0 | 0.731 | — |
| probe | 6.03 s | 961 | 0.731 | identical |
| full | 6.43 s | 961 | 0.448 | 63/68 |
| full-connected-return | 5.88 s | 1953 | 0.075 | 61/68; ≠ full |

Quality advantages remain OPEN.

## Prior A100 causal run (off/probe/full only)

| Field | Value |
|-------|-------|
| Job | [`6a736104a00abefd4b293eef`](https://huggingface.co/jobs/scarryhott/6a736104a00abefd4b293eef) |
| Results | [`scarryhott/bio-closure-benchmarks`](https://huggingface.co/datasets/scarryhott/bio-closure-benchmarks/tree/main/runs/hfjobs_a100_6a736104a00abefd4b293eef) |
| Local | `benchmarks/results/cloud_latest.json` |

| Mode | Mean latency | vs `off` | Note |
|------|-------------:|----------|------|
| `off` | 4.77 s | — | Baseline |
| `probe` | 4.70 s | identical tokens | Non-interfering observation (961 open events) |
| `full` | 4.98 s | **63/68** diffs every seed | Causal actuation; ~4.4 % latency overhead |

Hardware: NVIDIA A100-SXM4-80GB, bf16, ≈58 GB allocated.

Not a quality win. Lower `coherence_shadow` under `full` keeps holistic advantage OPEN.
`full-connected-return` quality remains separately open until the holistic job finishes.

## Earlier path notes

* First inline `bash` launch → ERROR 127 (command mangled); fixed via script mount.
* Credits required after initial 402.
* GCP `tnc-stream-clean-8264` VM `bio-rnd1-bench` (L4) remains **STOPPED** after OOM; disk billable until deleted.

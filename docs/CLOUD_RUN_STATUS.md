# Cloud 30B run status

## Role in the programme (non-negotiable)

This artifact is a **finite AI / language-substrate test** of Radical Numerics
RND1-Base-0910 under our admission hooks.

It is **not** biological closure and **not** the programme primary.

**Primary bio goal:** our Closure verification admission vs stated frontier
paper results:

```bash
python3.11 benchmarks/run_frontier_paper_admission.py
```

## Finite AI substrate test (= 30B holistic comparison)

**Definition:** Chapter A — 30B mode compare
(`off | probe | full | full-connected-return`) on `RND1-Base-0910`.

| Field | Value |
|-------|-------|
| Job | [`6a7372606b79c09949c23580`](https://huggingface.co/jobs/scarryhott/6a7372606b79c09949c23580) **COMPLETED** |
| Results | [`hfjobs_a100_holistic_…`](https://huggingface.co/datasets/scarryhott/bio-closure-benchmarks/tree/main/runs/hfjobs_a100_holistic_6a7372606b79c09949c23580) |
| Local | `benchmarks/results/cloud_holistic_unified.json` |
| Epistemic | `MEASURED_FINITE_AI_SUBSTRATE_TEST` / `FINITE_AI_SUBSTRATE_TEST_NOT_BIO_CLOSURE` |
| Thesis | `docs/UNIFICATION_THESIS.md` (Chapter A only) |

| Mode | Mean latency | Open | Coherence | vs `off` |
|------|-------------:|-----:|----------:|----------|
| off | 5.80 s | 0 | 0.731 | — |
| probe | 6.03 s | 961 | 0.731 | identical |
| full | 6.43 s | 961 | 0.448 | 63/68 |
| full-connected-return | 5.88 s | 1953 | 0.075 | 61/68; ≠ full |

Language/substrate quality advantages remain OPEN. Bio closure is decided
elsewhere (frontier paper admission), not by these coherence numbers.

## Prior A100 causal run (off/probe/full only — historical)

Superseded as the Chapter A record by the four-mode holistic artifact above.
Figures below are the first three-mode job only:

| Field | Value |
|-------|-------|
| Job | [`6a736104a00abefd4b293eef`](https://huggingface.co/jobs/scarryhott/6a736104a00abefd4b293eef) |
| Results | [`scarryhott/bio-closure-benchmarks`](https://huggingface.co/datasets/scarryhott/bio-closure-benchmarks/tree/main/runs/hfjobs_a100_6a736104a00abefd4b293eef) |

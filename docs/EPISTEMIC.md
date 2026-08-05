# Epistemic status

Explicit labels used throughout this repository:

| Label | Meaning |
|-------|---------|
| **RERUNNABLE** | Deterministic finite controller or mock-sampler path; CI green means this |
| **REPORTED ARTIFACT** | Provenance records, benchmark JSON, or measured logs stored as evidence |
| **DESIGN DERIVATION** | Architecture derived from unified Black Mirror / IVI–NRR closure axiometry |
| **OPEN EMPIRICAL CLAIM** | Requires external eval beyond token diffs / shadows; not asserted by CI |

## Full unified verification (= 30B holistic comparison)

The full unified verification **is** the GPU holistic compare of all four modes on
`RND1-Base-0910`:

```text
off | probe | full | full-connected-return
```

That artifact is **measured and committed**:

* `benchmarks/results/cloud_holistic_unified.json`
* HF run `hfjobs_a100_holistic_6a7372606b79c09949c23580`
* Thesis: `docs/UNIFICATION_THESIS.md`

```text
MEASURED_FULL_UNIFIED_30B_HOLISTIC_COMPARISON
CLOSED_FULL_MODEL_CAUSAL_INTEGRATION
CLOSED_FULL_MODEL_CONNECTED_RETURN_EXECUTION
OPEN_HOLISTIC_QUALITY_ADVANTAGE
OPEN_CONNECTED_RETURN_QUALITY_ADVANTAGE
```

| Mode | Mean latency | OPEN | Coherence | vs `off` |
|------|-------------:|-----:|----------:|----------|
| `off` | 5.80 s | 0 | 0.731 | baseline |
| `probe` | 6.03 s | 961 | 0.731 | identical |
| `full` | 6.43 s | 961 | 0.448 | 63/68 |
| `full-connected-return` | 5.88 s | 1953 | 0.075 | 61/68; ≠ `full` |

Harness (reproduce):

```bash
python benchmarks/compare_rnd1_closure.py \
  --model radicalnumerics/RND1-Base-0910 \
  --modes off probe full full-connected-return \
  --seeds 1 2 3 4 5 --steps 32
```

## Connected-return controller

`full-connected-return` is implemented (`closure/connected_return.py`), default remains
`closure_mode="off"`, pristine Radical Numerics files and pinned commit unchanged.
Execution on 30B is CLOSED; quality advantage is OPEN.

Chaitin material used here is only the project’s **finite connected-return /
ordered-support** reading — not Kolmogorov universality, RH, or unrestricted
incompleteness proofs.

## Claims that remain open

- Holistic generation-quality advantage under full mode (coherence shadow presently lower)
- Connected-return quality advantage under `full-connected-return` (execution measured; quality OPEN)
- Empirical biological validation of the coevolution adapter
- Any unrestricted AGI claim; any universal Chaitin–Kakeya / RH law
- Sybil / controller independence (Lean records the boundary; does not close it)

## What AGI cannot be (Phase 6 Lean negatives)

Machine-checked **negative** results on the abstract admission structure — not empirical
claims about this deployment — are catalogued in `docs/AGI_NEGATIVE_FORMAL.md`
(modules NRRF568–574). Salient forbids:

- self-certifying authorship / model-echo closure
- per-step token inflation from archived activity
- action before return, or learning commit after refusal
- Boolean admissibility; wash as new topology; archive ⇒ verdict
- local-only or global-only value closure; scalar \(K\) as token
- digest-only or fabricated inner-unity authority
- physical substrate unification by connected-return token
- fixed catalogue of verification topologies

## What is not closure identity

Scores, entropy, confidence, digests, fitness, phenotype probability, PASS counts,
coherence shadows, and token-diff tallies are axiometric shadows or instruments.
They may order probes or describe runs. They do not authorize closure.

A fixed list of “admissible topologies” is also not identity. Under the unified
axiometry, topologies are admitted through resolution; derivation motifs describe
the operator, they do not inventory the charts.

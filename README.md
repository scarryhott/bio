# Bio Closure Architecture on RND1

This repository contains the public Apache-2.0 [`RadicalNumerics/RND1`](https://github.com/RadicalNumerics/RND1) inference source tree integrated with a Black Mirror / IVI–NRR closure-derived admissible-verification layer for biological and coevolutionary actuation. It now also contains the independently derived closure-native architectural loop as a separate proposal-and-return model.

## Upstream

- Source: `RadicalNumerics/RND1`
- Copied commit: see `UPSTREAM_COMMIT`
- Model weights (external): `radicalnumerics/RND1-Base-0910`
- License: Apache License 2.0 (`LICENSE`, `NOTICE`)

Model weights are **not** stored in this repository.

## Repository map

| Area | Role | Epistemic status |
|------|------|------------------|
| `rnd/` | Copied upstream RND1 source + closure hooks in `sampling.py` | RERUNNABLE (baseline path) |
| `closure/` | Potential Gate, runtime, biology, connected return, independent closure-native model, Tagtokn bridge | DESIGN DERIVATION / RERUNNABLE finite controls |
| `tests/` | Finite unit + mock sampler + Radical Numerics verify + independent-model controls (42 tests) | RERUNNABLE |
| `benchmarks/` | Full-model GPU harness + 30B holistic artifact | REPORTED ARTIFACT (measured); quality still OPEN |
| `docs/` | Architecture, epistemic labels, stage status, unification thesis, independent-model provenance | DESIGN DERIVATION / REPORTED ARTIFACT |
| `UPSTREAM.md` | Provenance | REPORTED ARTIFACT |

**Stage verdict** (see `docs/STAGE_STATUS.md`):

```text
CLOSED_FULL_MODEL_CAUSAL_INTEGRATION
CLOSED_FULL_MODEL_CONNECTED_RETURN_EXECUTION
MEASURED_FULL_UNIFIED_30B_HOLISTIC_COMPARISON
CLOSED_INDEPENDENT_CLOSURE_MODEL_PORT
OPEN_INDEPENDENT_CLOSURE_VS_RND1_COMPARISON
OPEN_HOLISTIC_QUALITY_ADVANTAGE
OPEN_CONNECTED_RETURN_QUALITY_ADVANTAGE
```

Authoritative 30B artifact: `benchmarks/results/cloud_holistic_unified.json`  
(HF run `hfjobs_a100_holistic_6a7372606b79c09949c23580`).  
Thesis: `docs/UNIFICATION_THESIS.md`.

| Mode | Mean latency | vs `off` |
|------|-------------:|----------|
| `off` | 5.80 s | baseline |
| `probe` | 6.03 s | identical (0/68) |
| `full` | 6.43 s | 63/68 diffs |
| `full-connected-return` | 5.88 s | 61/68 diffs; ≠ `full`; 1953 OPEN |

Not a quality win.

## Unified axiometry

One intrinsic relation \(\mathcal C\) (not a fixed chart list). Verification topologies are **candidates admitted in their own resolution** — basis/closure cycle equality and encode↔eval alignment — under the same states as any other episode. Derivation motifs guide *how* admission works; they are not a catalog of pre-approved topologies.

## Native carrier

\[
G_t=(B_t,H_t,\Sigma_t,\Omega_t,\rho_t,\Gamma_t,\Pi_t,\mathcal A_t)
\]

Resolution states: `CLOSED_HIGHER` | `CLOSED_TO_OPENING` | `OPEN` | `FALSE_COLLAPSE` | `REFUSED`

Entropy, confidence, digests, fitness, and PASS counts are axiometric shadows in \(\mathcal A_t\). They do not authorize closure.

**AGI claim surface:** Phase 6 Lean negatives (`docs/AGI_NEGATIVE_FORMAL.md`) state what
closure-native AGI **cannot** be (self-certifying echo, token inflation, pre-return
action, Boolean/wash/projection substitution, etc.). They do not assert AGI here.

## Independent closure-native model

`closure/independent_model.py` ports the project model `UnifiedClosureArchitecturalLoop` as an independent executable arm:

```text
(C_t, E_t, A_legal,t)
→ A_t
→ (E_t+1, A_legal,t+1)
→ C_t+1
```

It originates provisional actions from admitted relational history and the complete current legal-action field. It has no RND1, Torch, Transformers, logits, confidence, or entropy dependency. Only an independently observed, recoverable whole-cycle return enters authoritative memory; self-authored or missing returns remain OPEN, contradictions are rejected, and repeated receipts do not inflate memory.

`closure/tagtokn_bridge.py` checks the model against the `scarryhott/tagtokn` framework: closure remains prior to tokens, OPEN claims issue no supply, circular replay stays OPEN, contradiction issues nothing, and only an admitted independent return can issue a downstream semantic receipt. See `docs/INDEPENDENT_CLOSURE_MODEL.md`.

The intended comparison now has three distinct arms:

1. native RND1;
2. independent closure-native model;
3. RND1 + closure hybrid.

The independent-vs-RND1 head-to-head remains OPEN until both operate against matched tasks and independently returned environments.

## Generation modes

```python
closure_mode: Literal["off", "probe", "full", "full-connected-return"] = "off"
```

- `off` — unmodified upstream RND1 admission
- `probe` — closure telemetry computed; baseline admission authoritative
- `full` — closure controls token admission
- `full-connected-return` — contact-ordered connected return (executed on 30B; quality still OPEN)

Every denoising step under probe/full/full-connected-return follows:

```text
RND1 proposal → local token support → nonlocal hair → global sequence relation
→ return reconstruction → ordered potential-gate admission
→ commit / remain open / reject → next denoising basis
```

## Quick start

```bash
pip install -e ".[test,linting]"
pytest -q
```

Full unified 30B holistic benchmark (GPU + HF weights):

```bash
python benchmarks/compare_rnd1_closure.py \
  --model radicalnumerics/RND1-Base-0910 \
  --modes off probe full full-connected-return \
  --seeds 1 2 3 4 5 \
  --steps 32
```

## Status

This repository now contains both the live RND1 closure hybrid and the independently derived closure-native proposal/return loop. The measured 30B holistic compare verifies **causal** `probe`/`full` separation and **executed** `full-connected-return` on `RND1-Base-0910`. The independent model's finite controls are closed, but its matched comparison against RND1 has not yet been run. The repository does **not** claim unrestricted AGI, empirical biological validation, or improved generation quality.

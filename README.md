# Bio Closure Architecture on RND1

This repository contains the public Apache-2.0 [`RadicalNumerics/RND1`](https://github.com/RadicalNumerics/RND1) inference source tree integrated with a Black Mirror / IVI–NRR closure-derived admissible-verification layer for biological and coevolutionary actuation. It now also contains the independently derived closure-native architectural loop and a full comparison framework for the open Radical Numerics-associated biological suite.

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
| `tests/` | Finite unit, mock sampler, independent-kernel, and full-suite manifest controls | RERUNNABLE |
| `benchmarks/` | RND1 GPU harness, 30B artifact, open-suite manifest and planner | MEASURED ARTIFACT + FRAMEWORK DEFINITION |
| `docs/` | Architecture, stage status, thesis, provenance, full open-suite comparison | DESIGN DERIVATION / REPORTED ARTIFACT |
| `UPSTREAM.md` | Provenance | REPORTED ARTIFACT |

**Stage verdict** (see `docs/STAGE_STATUS.md`):

```text
CLOSED_FULL_MODEL_CAUSAL_INTEGRATION
CLOSED_FULL_MODEL_CONNECTED_RETURN_EXECUTION
MEASURED_FULL_UNIFIED_30B_HOLISTIC_COMPARISON
CLOSED_INDEPENDENT_CLOSURE_MODEL_PORT
CLOSED_RADICAL_NUMERICS_MODEL_AND_DATA_PROVENANCE
CLOSED_FULL_RADICAL_NUMERICS_OPEN_SUITE_COMPARISON_FRAMEWORK
OPEN_FULL_RADICAL_NUMERICS_BIOLOGICAL_SUITE_RUN
OPEN_BIO_CLOSURE_VS_RADICAL_NUMERICS_BIOLOGICAL_RESULT
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

## Radical Numerics model and biology distinction

Radical Numerics is the company that released RND1 and publicly identifies its team with the Evo/Evo 2 biological-model programme. Those facts do not make RND1 itself a biological foundation model.

- **RND1-Base-0910** is a 30.5B sparse diffusion language model converted from Qwen3-30B-A3B and continually pretrained for diffusion-language behavior. Its reported evaluations are general language, reasoning, mathematics, and code tasks. Its public materials do not identify a dedicated DNA/genomics training corpus.
- **Evo 1 / Evo 1.5** are open genome-model baselines trained on OpenGenome and related genomic data.
- **Evo 2** is a fully open genome-model family trained on `OpenGenome2`, with more than 8.8 trillion curated nucleotides. Public checkpoints include 1B, 7B, 20B, and 40B variants; the 7B model is the primary accessible baseline, while 20B and 40B are hardware-gated stronger baselines.
- **Omnii** is Radical Numerics' next-generation genome-language-model research preview. The company reports ClinVar, TraitGym, RNAGym, CNV, and related evaluations, but public weights and a complete reproducibility package are not currently available.

Therefore the completed 30B run in this repository is an **RND1 language-model hybrid/substrate experiment**, not Bio Closure versus Radical Numerics' biological model. See `docs/RADICAL_NUMERICS_BIOLOGY_DATA_PROVENANCE.md`.

## Full Radical Numerics open-suite framework

The repository now defines the complete reproducible comparison boundary:

```text
A. independent Bio Closure kernel
B. Evo 1 / Evo 2 native biological models
C. Evo biological proposal + closure return/admission
D. RND1 and RND1 + closure as a separate language/substrate chapter
E. Omnii as reported-only until a public interface or weights exist
```

Machine-readable suite definition:

```text
benchmarks/radical_numerics_suite_manifest.json
```

Auditable planner:

```bash
python benchmarks/plan_radical_numerics_suite.py --json
python benchmarks/plan_radical_numerics_suite.py --include-reported --json
python benchmarks/plan_radical_numerics_suite.py --benchmark variant-effect
```

The manifest covers sequence likelihood, variant effect, gene completion, RNA fitness, and perturbation-response tasks. It enforces identical held-out returns, exact checkpoint and dataset provenance, separation of native and hybrid arms, and forbids reported-only Omnii results from being labelled as reruns. See `docs/FULL_RADICAL_NUMERICS_OPEN_SUITE_COMPARISON.md`.

The framework is closed; dataset adapters, Evo 2 + closure integration, and the complete biological suite run remain open.

## Unified axiometry

One intrinsic relation \(\mathcal C\) (not a fixed chart list). Verification topologies are **candidates admitted in their own resolution** — basis/closure cycle equality and encode↔eval alignment — under the same states as any other episode. Derivation motifs guide *how* admission works; they are not a catalog of pre-approved topologies.

## Native carrier

\[
G_t=(B_t,H_t,\Sigma_t,\Omega_t,\rho_t,\Gamma_t,\Pi_t,\mathcal A_t)
\]

Resolution states: `CLOSED_HIGHER` | `CLOSED_TO_OPENING` | `OPEN` | `FALSE_COLLAPSE` | `REFUSED`

Entropy, confidence, digests, fitness, and PASS counts are axiometric shadows in \(\mathcal A_t\). They do not authorize closure.

**AGI claim surface:** Phase 6 Lean negatives (`docs/AGI_NEGATIVE_FORMAL.md`) state what closure-native AGI **cannot** be. They do not assert AGI here.

## Independent closure-native model

`closure/independent_model.py` ports `UnifiedClosureArchitecturalLoop` as an independent executable arm:

```text
(C_t, E_t, A_legal,t)
→ A_t
→ (E_t+1, A_legal,t+1)
→ C_t+1
```

It originates provisional actions from admitted relational history and the complete current legal-action field. It has no RND1, Torch, Transformers, logits, confidence, or entropy dependency. Only an independently observed, recoverable whole-cycle return enters authoritative memory; self-authored or missing returns remain OPEN, contradictions are rejected, and repeated receipts do not inflate memory.

`closure/tagtokn_bridge.py` keeps Tagtokn downstream of closure. See `docs/INDEPENDENT_CLOSURE_MODEL.md`.

## Generation modes

```python
closure_mode: Literal["off", "probe", "full", "full-connected-return"] = "off"
```

- `off` — unmodified upstream RND1 admission
- `probe` — closure telemetry computed; baseline admission authoritative
- `full` — closure controls token admission
- `full-connected-return` — contact-ordered connected return, executed on 30B; quality still OPEN

## Quick start

```bash
pip install -e ".[test,linting]"
pytest -q
```

Full unified RND1 benchmark:

```bash
python benchmarks/compare_rnd1_closure.py \
  --model radicalnumerics/RND1-Base-0910 \
  --modes off probe full full-connected-return \
  --seeds 1 2 3 4 5 \
  --steps 32
```

## Status

This repository contains the measured RND1 closure hybrid, the independent Black Mirror Bio Closure kernel, and the complete comparison framework for the open Evo/Evo 2 suite plus reported-only Omnii. The framework is executable as a plan and validated by finite controls, but no full biological-suite benchmark has yet been run. The repository does **not** claim unrestricted AGI, empirical biological validation, superiority over Radical Numerics biological models, or improved generation quality.

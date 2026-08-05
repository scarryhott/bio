# Bio Closure AGI (ours) vs frontier paper results

This repository implements a **self-contained Closure AGI** for biology from the
IVI–NRR / Black Mirror architectural thesis (transcripts +
`docs/transcript_closure/`).

**Programme authority:** `docs/PROGRAMME.md`

**Primary goal:** our Closure verification admission against **stated frontier
paper results** (Evo 2 / OpenGenome2, Omnii reported, Goel, TraitGym, RNAGym, …).

**RND1 is not our model** and the 30B hybrid is **not** bio closure — it is a
**finite AI substrate test** only (`docs/CLOUD_RUN_STATUS.md`).
Ownership map: `docs/OUR_CLOSURE_AGI_VS_RADICAL_NUMERICS.md`.

## Upstream (external RND1 vendoring)

- Source: `RadicalNumerics/RND1`
- Copied commit: see `UPSTREAM_COMMIT`
- Model weights (external): `radicalnumerics/RND1-Base-0910`
- License: Apache License 2.0 (`LICENSE`, `NOTICE`)

Model weights are **not** stored in this repository.

## Repository map

| Area | Role | Epistemic status |
|------|------|------------------|
| `closure/` | **Our** Closure AGI: IVI spine, runtime, biology, Kakeya return, Goel hair, frontier admission | DESIGN / RERUNNABLE / MEASURED |
| `benchmarks/` | Frontier paper catalog, open-data cache, reunification, primary runners | MEASURED + FRAMEWORK |
| `docs/` | Programme priority, ownership, thesis, Goel, return-unified runtime | DESIGN / REPORTED |
| `rnd/` | **External** RND1 inference + our admission hooks | Finite AI test harness only |
| `tests/` | Finite unit, mock sampler, independent-kernel, frontier admission | RERUNNABLE |
| `UPSTREAM.md` | RND1 provenance (external) | REPORTED ARTIFACT |

**Authoritative priority** (`docs/PROGRAMME.md` / `docs/STAGE_STATUS.md`):

\[
M_{\mathrm{ClosureBio}}
\;\text{vs}\;
\text{FrontierPaperResults}
\quad\text{inside return-unified admission}
\]

\[
\text{RND1-30B}(\pm C)
\;=\;
\text{FINITE\_AI\_SUBSTRATE\_TEST}
\;\neq\;
\text{bio closure}
\]

```text
CLOSED_PROGRAMME_PRIORITY_OUR_CLOSURE_VS_FRONTIER_PAPERS
CLOSED_RND1_30B_AS_FINITE_AI_SUBSTRATE_TEST_NOT_BIO
MEASURED_STATEFUL_BIOLOGICAL_CLOSURE_CHAIN
MEASURED_GOEL_QUANTUM_ENVIRONMENTAL_CLOSURE_DERIVED
MEASURED_OUR_CLOSURE_REUNIFIED_VERIFIED
MEASURED_EXTERNAL_SUITE_INTEGRATED
MEASURED_OPEN_DATASET_ONLINE_SAMPLES_IN_CLOSURE
OPEN_CROSS_DATASET_EMPIRICAL_RESOLUTIONS
OPEN_DELTA_C_Q_BIOLOGICAL_DOUBLE_SLIT
OPEN_BIO_CLOSURE_VS_RADICAL_NUMERICS_BIOLOGICAL_RESULT
OPEN_EVO_WEIGHT_EXECUTION_ON_CATALOGUED_DATA
```

**Role split:** local Kakeya + global Chaitin/Goel are **ours**; RND1/Evo/Omnii
are **Radical Numerics external** architectures.

**Primary command:**

```bash
python3.11 benchmarks/run_frontier_paper_admission.py
```

→ `OUR_CLOSURE_ADMISSION_VS_FRONTIER_PAPERS_MEASURED`  
(`benchmarks/results/frontier_paper_admission.json`)

**Stateful biological run** (one shared \(C_t\) across datasets, not aggregate closes):

```bash
python3.11 benchmarks/run_stateful_biological_closure.py --include-open-data
```

→ `STATEFUL_BIOLOGICAL_CLOSURE_CHAIN_MEASURED`  
Cross-dataset \(h\) are derived with \(\delta_C=\mathrm{OPEN}\) until independent return.

**Goel quantum–environmental closure** (Level-6 \(R_6=\sigma\circ P\)):

```bash
python3.11 benchmarks/run_goel_quantum_environmental_closure.py
```

→ `GOEL_QUANTUM_ENVIRONMENTAL_CLOSURE_DERIVED`  
Classical DNA×env hair admits; \(\delta_C(Q)\) stays OPEN (`docs/GOEL_QUANTUM_ENVIRONMENTAL_CLOSURE.md`).

**Our Closure AGI** must pass internal reunify+verify
(`benchmarks/verify_our_closure.py` → `OUR_CLOSURE_REUNIFIED_VERIFIED`).
External suite integrates papers + open datasets + optional weights
(`docs/PAPER_ARCHITECTURE_DATA_LAYER.md`). Live Evo weight execution remains OPEN.

### Finite AI substrate test (Chapter A — not bio)

Artifact: `benchmarks/results/cloud_holistic_unified.json`  
(HF run `hfjobs_a100_holistic_6a7372606b79c09949c23580`).

| Hybrid mode | Mean latency | vs `off` |
|------|-------------:|----------|
| `off` | 5.80 s | baseline |
| `probe` | 6.03 s | identical (0/68) |
| `full` | 6.43 s | 63/68 diffs |
| `full-connected-return` | 5.88 s | 61/68 diffs; ≠ `full`; 1953 OPEN |

Not a quality win; not the biological programme conclusion.

## Return-unified runtime: not pre/post training

Closure is not pretraining, post-training, reranking, an external benchmark, or a downstream verifier attached after a model prediction. It is the return-unified runtime in which data, action, environment, candidate verification topology, and memory become jointly admissible.

Incorrect pipeline:

```text
train model
→ generate prediction
→ closure checks prediction
→ accept or reject
```

Project runtime:

```text
current relational basis
↔ available observations and actions
↔ provisional transformation
↔ environmental return
↔ verification topology generated within the return
↔ integrated next basis
```

This is inherited from the ARC/AGI interaction carrier:

```text
U_t = (E_t, A_legal,t, A_t, E_t+1, T_t, ...)
C(U_t) = interaction_C:<digest>
S_t+1 = Integrate(S_t, C(U_t), rho_t)
```

The maintained interaction relation is the closure identity. Action identifiers, scores, confidence, entropy, PASS counts, and benchmark labels are instruments or shadows, not closure authority.

Biological data is integrated only as its relation is resolved. DNA, RNA, protein, phenotype, environment, intervention history, learned-model state, and measured consequence are partial perspectives of one unresolved episode; concatenation or a shared embedding does not itself unify them.

Candidate verification topologies are part of the episode. They can be admitted, rejected, refused, or left OPEN through the same return they attempt to resolve. Local ball and global hair are repartitioned by return rather than fixed permanently in advance.

See `docs/RETURN_UNIFIED_BIO_AGI_RUNTIME.md`.

## Radical Numerics model and biology distinction

Radical Numerics is the company that released RND1 and publicly identifies its team with the Evo/Evo 2 biological-model programme. Those facts do not make RND1 itself a biological foundation model.

- **RND1-Base-0910** is a 30.5B sparse diffusion language model converted from Qwen3-30B-A3B and continually pretrained for diffusion-language behavior. Its reported evaluations are general language, reasoning, mathematics, and code tasks. Its public materials do not identify a dedicated DNA/genomics training corpus.
- **Evo 1 / Evo 1.5** are open genome-model baselines trained on OpenGenome and related genomic data.
- **Evo 2** is a fully open genome-model family trained on `OpenGenome2`, with more than 8.8 trillion curated nucleotides. Public checkpoints include 1B, 7B, 20B, and 40B variants; the 7B model is the primary accessible baseline, while 20B and 40B are hardware-gated stronger baselines.
- **Omnii** is Radical Numerics' next-generation genome-language-model research preview. The company reports ClinVar, TraitGym, RNAGym, CNV, and related evaluations, but public weights and a complete reproducibility package are not currently available.

Therefore the completed 30B run in this repository is an **RND1 language-model hybrid/substrate experiment**, not Bio Closure versus Radical Numerics' biological model. See `docs/RADICAL_NUMERICS_BIOLOGY_DATA_PROVENANCE.md`.

## Full Radical Numerics open-suite framework

The repository defines the reproducible comparison boundary:

```text
A. native learned biological runtime
B. closure-native return-unified runtime
C. learned-representation return-unified runtime
D. RND1 and RND1 + closure as a separate language/substrate chapter
E. Omnii as reported-only until a public interface or weights exist
```

This replaces the weaker framing in which Evo/Evo 2 merely generate proposals that a later closure filter accepts or rejects. Learned representations participate inside the same return-unified episode with biological observations, available actions, organism/environment transformation, independent return, verification-topology admission, and memory continuation.

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

The manifest covers sequence likelihood, variant effect, gene completion, RNA fitness, and perturbation-response tasks. It enforces identical held-out returns, exact checkpoint and dataset provenance, separation of native and unified runtime organizations, and forbids reported-only Omnii results from being labelled as reruns. See `docs/FULL_RADICAL_NUMERICS_OPEN_SUITE_COMPARISON.md`.

The framework is closed; dataset adapters, Evo 2 participation inside the return-unified runtime, physical Goel polymerase runtime / witnessed quantum carriers, and the complete biological suite run remain open. The Goel **binding** (global Chaitin DNA–env operator) and Radical Numerics **local Kakeya** role split are documented in `docs/GOEL_DNA_ENVIRONMENT_CHAITIN_OPERATOR.md`.

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

`closure/independent_model.py` ports `UnifiedClosureArchitecturalLoop` as an independent executable kernel:

```text
(C_t, E_t, A_legal,t)
→ A_t
→ (E_t+1, A_legal,t+1)
→ C_t+1
```

It originates provisional actions from admitted relational history and the complete current legal-action field. It has no RND1, Torch, Transformers, logits, confidence, or entropy dependency. Only an independently observed, recoverable whole-cycle return enters authoritative memory; self-authored or missing returns remain OPEN, contradictions are rejected, and repeated receipts do not inflate memory.

This finite kernel is a component of the return-unified architecture, not a complete biological predictor followed by verification. `closure/tagtokn_bridge.py` keeps Tagtokn downstream of closure. See `docs/INDEPENDENT_CLOSURE_MODEL.md`.

## Generation modes

```python
closure_mode: Literal["off", "probe", "full", "full-connected-return"] = "off"
```

- `off` — unmodified upstream RND1 admission
- `probe` — closure telemetry computed; baseline admission authoritative
- `full` — closure controls token admission
- `full-connected-return` — contact-ordered connected return, executed on 30B; quality still OPEN

These modes are an implemented substrate experiment, not the final biological return-unified runtime.

## Quick start

```bash
pip install -e ".[test,linting]"
python3.11 -m pytest -q
python3.11 benchmarks/run_frontier_paper_admission.py
python3.11 benchmarks/run_unified_verification.py
```

Finite AI substrate test only (RND1-30B — **not** bio closure):

```bash
python benchmarks/compare_rnd1_closure.py \
  --model radicalnumerics/RND1-Base-0910 \
  --modes off probe full full-connected-return \
  --seeds 1 2 3 4 5 \
  --steps 32
```

## Status

**Primary:** our Closure admission vs stated frontier paper results is MEASURED
(`benchmarks/run_frontier_paper_admission.py`). Authority: `docs/PROGRAMME.md`.

Supporting: independent Black Mirror Bio Closure kernel, open Evo/Evo 2 suite
framework, Omnii reported-only, return-unified runtime, open-dataset samples.
RND1-30B hybrid is a **finite AI substrate test only**. Live Evo weight execution
and full biological superiority claims remain OPEN.

The repository does **not** claim unrestricted AGI, empirical biological
superiority over Radical Numerics biological models, or improved generation quality.

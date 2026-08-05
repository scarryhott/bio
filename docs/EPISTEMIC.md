# Epistemic status

Explicit labels used throughout this repository:

| Label | Meaning |
|-------|---------|
| **RERUNNABLE** | Deterministic finite controller or mock-sampler path; CI green means this |
| **REPORTED ARTIFACT** | Provenance records, benchmark JSON, or measured logs stored as evidence |
| **DESIGN DERIVATION** | Architecture derived from unified Black Mirror / IVI–NRR closure axiometry |
| **OPEN EMPIRICAL CLAIM** | Requires matched-task / returned-environment eval; not asserted by CI |

## Programme thesis (authoritative)

See `docs/UNIFICATION_THESIS.md`:

# Bio Closure and Radical Numerics  
## Independent Return, Learned Proposal, and the Three-Arm Test of Closure-Native AGI

\[
M_{\mathrm{RND1}}
\;\text{vs}\;
M_{\mathrm{ClosureBio}}
\;\text{vs}\;
M_{\mathrm{RND1+Closure}}
\]

| Arm | What it is | Empirical status |
|-----|------------|------------------|
| Radical Numerics | Learned 30B proposal topology | Hybrid modes measured; alone vs closure OPEN |
| Independent Bio Closure | Closure-native action/return/learning loop | Port CLOSED; vs RND1 OPEN |
| Hybrid | RND1 proposal + closure admission | Four-mode A100 MEASURED; quality OPEN |

### Architecture CLOSED

```text
CLOSED_INDEPENDENT_BIO_CLOSURE_MODEL_PORT
CLOSED_RND1_CLOSURE_HYBRID_EXECUTION
CLOSED_THREE_ARM_COMPARISON_ARCHITECTURE
```

### Empirical thesis OPEN

```text
OPEN_BIO_CLOSURE_VS_RADICAL_NUMERICS_RESULT
OPEN_HYBRID_VS_INDEPENDENT_ADVANTAGE
OPEN_BIOLOGICAL_RETURN_VALIDATION
```

## Chapter A — hybrid four-mode run (not the programme conclusion)

Artifact: `benchmarks/results/cloud_holistic_unified.json`  
(`hfjobs_a100_holistic_6a7372606b79c09949c23580`)

```text
MEASURED_HYBRID_30B_FOUR_MODE_COMPARISON
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

Token coherence is **not** the score for \(M_{\mathrm{ClosureBio}}\).

## Claims that remain open

- Bio Closure vs Radical Numerics on matched biological returned tasks
- Hybrid vs independent advantage
- Biological return validation
- Holistic / connected-return **quality** advantages on language probes
- Unrestricted AGI; universal Chaitin / RH; Sybil independence

## What is not closure identity

Scores, entropy, confidence, digests, fitness, PASS counts, coherence shadows,
and token-diff tallies are axiometric shadows. They do not authorize closure.

# Full Radical Numerics open-suite comparison framework

Status date: 2026-08-05

## Purpose

This document defines the complete comparison surface between the independent
Black Mirror Bio Closure kernel and every relevant Radical Numerics-associated
system that is currently open enough to reproduce. It also records systems that
are publicly described but not yet reproducible.

The framework closes the comparison design. It does **not** claim that the full
biological suite has been executed.

## Suite boundary

### Runnable open systems

1. **Independent Bio Closure kernel**
   - repository-local;
   - closure-native proposal, sealed action, independent return, admission, and
     relational memory;
   - no RND1, Torch, Transformers, logits, confidence, or entropy dependency.

2. **RND1-Base-0910**
   - open general diffusion language model;
   - retained as a language-model and substrate baseline;
   - not treated as a genomics model.

3. **RND1 + closure**
   - existing hybrid arm;
   - measured on the 30B language model;
   - not counted as the biological comparison.

4. **Evo 1 / Evo 1.5 family**
   - open genomic foundation models trained on OpenGenome;
   - useful as historical prokaryotic and specialized genomic baselines.

5. **Evo 2 open checkpoints**
   - `evo2_1b_base` for smoke tests only;
   - `evo2_7b` as the primary accessible biological baseline;
   - `evo2_20b` as the strong single-H100 baseline;
   - `evo2_40b` as the strongest fully open baseline when hardware permits.

6. **OpenGenome2**
   - public training dataset associated with Evo 2;
   - more than 8.8 trillion curated nucleotides across all domains of life;
   - available as raw FASTA and processed JSONL through the Evo 2 release.

### Reported but not reproducible as a local arm

**Omnii** is recorded as a Radical Numerics biological research-preview system.
Its published preview names ClinVar, TraitGym, RNAGym, and copy-number-variant
evaluations, but public weights, complete training provenance, and a reproducible
local evaluation package are not presently available. Omnii may be included in
comparison tables only as a reported external result, never as a rerun.

## Biological benchmark families

The framework combines the open suite across five kinds of returned relation.

### Sequence likelihood

```text
held-in sequence context
→ model likelihood or ranking
→ held-out nucleotide return
```

This establishes a common low-level genomic baseline but is not by itself a
closure test.

### Variant-effect prediction

Candidate open sources include TraitGym, BRCA1 DMS, BRCA2 SGE, ClinVar, and
ProteinGym where licensing and task compatibility permit.

```text
reference sequence + variant + context
→ predicted consequence
→ independently measured or clinically curated return
```

### Gene completion

```text
partial genomic context
→ proposed continuation
→ held-out gene sequence and annotation return
```

### RNA fitness

RNAGym supplies tasks in which a sequence-level proposal can be compared with a
held-out measured fitness return.

### Perturbation response

LINCS L1000, scPerturb, and related public single-cell intervention datasets are
the strongest match to the Black Mirror learn→close→act cycle:

```text
initial cell state
+ intervention
→ proposed consequence
→ measured expression or phenotype return
→ ADMITTED | OPEN | REJECTED
```

This family requires multimodal adapters and is not reducible to raw DNA-token
continuation.

## Required arms for each runnable biological task

At minimum:

```text
A. independent Bio Closure kernel
B. Evo 2 native
C. Evo 2 proposal + closure return/admission
```

Where technically meaningful, the study may add Evo 1, multiple Evo 2 sizes, and
reported Omnii numbers. RND1 remains a separate language/substrate chapter and
must not be silently substituted for Evo 2.

## Fairness and provenance controls

Every result must record:

- exact dataset release, license, and checksum;
- train/validation/test split and leakage controls;
- exact model checkpoint or revision;
- identical held-out cases for every comparable arm;
- model-native input encoding and any adapter transformation;
- hardware, precision, context length, and inference settings;
- whether the arm is native, closure-native, hybrid, hosted, or reported-only;
- output score and closure resolution separately;
- OPEN cases without forcing them into incorrect or correct labels;
- contradiction, refusal, and missing-return rates;
- latency, memory, and compute cost.

No PASS count, digest, token difference, confidence score, or market receipt is
closure authority.

## Holistic evaluation record

A complete result row should contain:

```text
case identity
source biological carrier
legal proposal field
model proposal
pre-return seal
independent returned consequence
ordered support
resolution state
biological task score
OPEN / contradiction classification
resource use
provenance digest
```

The biological task score and the closure identity remain distinct. A high AUROC
cannot certify closure, and an OPEN resolution is not automatically a failed
biological prediction.

## Repository implementation

- `benchmarks/radical_numerics_suite_manifest.json` is the machine-readable
  availability and benchmark manifest.
- `benchmarks/plan_radical_numerics_suite.py` validates the manifest and produces
  auditable runnable plans.
- `tests/test_radical_numerics_suite_manifest.py` prevents Omnii from being
  misclassified as runnable and prevents RND1 from being treated as a biological
  baseline by default.

Example:

```bash
python benchmarks/plan_radical_numerics_suite.py --json
python benchmarks/plan_radical_numerics_suite.py --include-reported --json
python benchmarks/plan_radical_numerics_suite.py --benchmark variant-effect
```

## Current verdict

```text
CLOSED_FULL_RADICAL_NUMERICS_OPEN_SUITE_COMPARISON_FRAMEWORK
CLOSED_OPEN_VS_REPORTED_MODEL_BOUNDARY
CLOSED_BIOLOGICAL_BENCHMARK_FAMILY_MANIFEST
OPEN_DATASET_ADAPTER_IMPLEMENTATION
OPEN_EVO2_PLUS_CLOSURE_INTEGRATION
OPEN_FULL_RADICAL_NUMERICS_BIOLOGICAL_SUITE_RUN
OPEN_BIO_CLOSURE_COMPARATIVE_RESULT
```

The existing RND1 holistic artifact remains valid as a language-model hybrid
experiment. It is not relabelled as an Evo 2, Omnii, or full biological-suite
result.

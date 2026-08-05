# Radical Numerics biology and data provenance

Status date: 2026-08-05

This document separates the Radical Numerics text-model experiment already run in this repository from the company's biological-model programme and from the public datasets cited by that programme.

## Company identity

Radical Numerics publicly describes itself as an AI laboratory for general biological intelligence and states that its team is behind Evo and Evo 2. The same company also released RND1.

That common company identity does **not** make RND1 a biological foundation model.

## Model distinction

### RND1-Base-0910

RND1 is an experimental 30.5B-parameter sparse mixture-of-experts diffusion **language model**, with about 3.3B parameters active per token. Radical Numerics says it was converted from Qwen3-30B-A3B and continually pretrained for 500B tokens to acquire diffusion behaviour.

Its published evaluation suite is language-model oriented: MMLU, ARC-C, RACE, BBH, GSM8K, and MBPP. The public RND1 materials do not identify a dedicated genomics, DNA, RNA, protein, or biological training corpus.

Therefore the completed `RND1-Base-0910` run in this repository is a language-model substrate/hybrid experiment, not a direct Bio Closure versus Radical Numerics biological-model comparison.

Primary sources:

- https://www.radicalnumerics.ai/blog/rnd1
- https://huggingface.co/radicalnumerics/RND1-Base-0910

### Evo 2

Evo 2 is a genome model associated with work by researchers who later formed or joined Radical Numerics, published with Arc Institute and collaborators. The Nature paper explicitly identifies its training data.

The paper reports:

- Evo 2 7B trained on 2.4 trillion tokens;
- Evo 2 40B trained on 9.3 trillion tokens;
- training dataset `OpenGenome2`;
- more than 8.8 trillion curated, non-redundant nucleotides;
- sequence data spanning bacteria, archaea, eukarya, and bacteriophage.

This is the clearest public data-grounded biological baseline currently relevant to the closure programme.

Primary source:

- https://www.nature.com/articles/s41586-026-10176-5

### Omnii

Radical Numerics describes Omnii as its next-generation genome language model and presents it as a multimodal biological system. The public research preview reports evaluations on named biological benchmarks, including:

- ClinVar coding and noncoding SNVs and indels;
- ClinVar copy-number variants;
- TraitGym complex-trait benchmarks;
- RNAGym RNA-fitness benchmarks;
- an 80:20 hold-out-by-gene split used for several variant-effect evaluations.

The preview provides benchmark tables and task descriptions. It does not yet provide a complete public training-data inventory or a reproducibility package equivalent to the Evo 2/OpenGenome2 release.

Primary sources:

- https://www.radicalnumerics.ai/about
- https://www.radicalnumerics.ai/blog/radical-numerics-seed
- https://www.radicalnumerics.ai/blog/omnii-health-preview

## Programme architecture (ownership-correct)

Authority: `docs/PROGRAMME.md`.

**Primary biological comparison:**

1. **Independent Bio Closure kernel** — our verification admission on held-out returns.
2. **Stated frontier paper / open-bio results** — Evo 2 ± OpenGenome2, Omnii reported, Goel paper logic, TraitGym/RNAGym/….

**Finite AI substrate test only (not bio closure):**

3. **Native RND1 / RND1+closure** — 30B language hybrid under our hooks (Chapter A).

The completed 30B benchmark compared language modes only. It did not evaluate
our Closure AGI against a biological Radical Numerics model.

## Correct biological thesis comparison

The biologically relevant programme compares:

1. the independent Bio Closure kernel;
2. stated frontier paper results and open biological architectures such as Evo 2;
3. optionally, the biological model plus closure return/admission when weights execute.

Omnii remains reported-only until a usable public evaluation interface exists.
RND1-30B is excluded from the bio primary.

## Dataset requirement

A full closure comparison needs more than raw DNA continuation — and more than
RND1 weights. The external stack gathers **paper architectures** and **open
datasets** (Goel, Evo/OpenGenome2, Omnii-reported tasks, TraitGym, RNAGym,
ProteinGym, ClinVar, perturbation sets, Wuite–Bustamante tension prior). See
`docs/PAPER_ARCHITECTURE_DATA_LAYER.md` and
`benchmarks/paper_architecture_data_catalog.json`.

The selected public benchmark must expose or permit a held-out returned consequence:

```text
initial sequence / cell / organism state
+ intervention or context
→ measured molecular, cellular, phenotypic, or fitness outcome
```

That permits the closure-native model to distinguish:

```text
ADMITTED | OPEN | REJECTED
```

from an independently returned consequence rather than from a self-authored score.

Candidate public benchmark families include OpenGenome2/Evo 2 evaluation tasks, ClinVar variant-effect tasks, RNAGym, TraitGym, ProteinGym, perturbational single-cell datasets, LINCS L1000, and other intervention-response datasets. Dataset licensing, splits, leakage, and accessible ground truth must be recorded before any result is called a comparison.

## Current verdict

```text
CLOSED_RND1_LANGUAGE_MODEL_PROVENANCE
CLOSED_RADICAL_NUMERICS_COMPANY_IDENTITY
CLOSED_EVO2_OPEN_GENOME_DATA_PROVENANCE
REPORTED_OMNII_BENCHMARK_PREVIEW
CLOSED_PROGRAMME_PRIORITY_OUR_CLOSURE_VS_FRONTIER_PAPERS
CLOSED_RND1_30B_AS_FINITE_AI_SUBSTRATE_TEST_NOT_BIO
MEASURED_OUR_CLOSURE_ADMISSION_VS_FRONTIER_PAPERS
OPEN_PUBLIC_BIOLOGICAL_THREE_ARM_RUN
OPEN_BIO_CLOSURE_VS_RADICAL_NUMERICS_BIOLOGICAL_RESULT
```

No result in this repository currently establishes superiority over Evo 2, Omnii, or another Radical Numerics biological model. Our admission against their **stated** paper/preview surfaces is MEASURED; live weight reruns remain OPEN.

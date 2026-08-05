# Paper architectures and open data under our Closure AGI

Status date: 2026-08-05

## Correction

The external programme is **not** “RND1 weights only.”

```text
our Closure AGI admission (C)
    ↑
paper-derived architectures (Goel, Evo/OpenGenome2, Omnii-reported, RND1-language)
    ↑
open / literature datasets and held-out returns
    ↑
optional open weights (RND1, Evo 2, …) when present
```

Weights are an optional bottom layer. Papers and datasets are first-class.

**Primary runner** (our C vs stated frontier paper results):

```bash
python3.11 benchmarks/run_frontier_paper_admission.py
```

Catalog: `benchmarks/frontier_paper_results.json`  
Authority: `docs/PROGRAMME.md`

**Combined RN open + Goel paper path** (supporting — RND1 remains finite AI test):

```bash
python3.11 benchmarks/run_rn_goel_combined.py --include-open-data
```

Stack: our \(C\) ← Goel DNA×env + Wuite prior ← RN open (RND1 code/±weights, spear, dInfer) ← returns.  
Artifact: `benchmarks/results/rn_goel_combined.json`. RND1 30B shards remain optional; open `rnd/sampling.py` mock path executes under our hooks when weights are absent.

Machine catalog: `benchmarks/paper_architecture_data_catalog.json`  
Runtime: `closure/paper_data_layer.py`  
Gated suite check: `paper_architecture_data_layer` in `benchmarks/run_external_suite.py`

## Paper architectures

| Id | Source | Role under our C |
|----|--------|------------------|
| `goel-dna-environment-motor` | Goel thesis + PNAS 2001/2003 + *Quantum Aspects of Life* 2008; Wuite/Bustamante 2000 prior | Global Chaitin DNA×env hair |
| `evo2-opengenome2-runtime` | Nature Evo 2 paper | Open bio LM architecture + OpenGenome2 |
| `evo1-opengenome` | Evo 1 line | Historical prokaryotic baseline |
| `rnd1-diffusion-language` | RND1 report/blog | Optional language presentation carrier |
| `omnii-reported-genome-lm` | Omnii preview | Reported tasks only (no local rerun) |

## Datasets found / bound

| Dataset | Status here | Return type |
|---------|-------------|-------------|
| OpenGenome2 | **online stand-in** (NCBI nucleotide; full HF corpus not mirrored) | genomic context / continuation |
| OpenGenome | download-open | historical genomic context |
| TraitGym | **downloaded sample** (HF datasets-server) | regulatory variant consequence |
| RNAGym | **downloaded sample** (HF fitness split) | RNA fitness / structure |
| ProteinGym | **downloaded sample** (reference CSV) | protein DMS / clinical |
| ClinVar | **online service** (NCBI E-utilities) | clinical variant return |
| LINCS L1000 / scPerturb | download-open (multimodal) | perturbation phenotype |
| Wuite–Bustamante tension prior | **local** literature prior | polymerase mode vs tension |
| finite bio returns | **local** | multi-modality episodes |

Local prior file: `benchmarks/data_priors/wuite_bustamante_tension_prior.json`  
(Goel operator modes from published landmarks; not a remeasurement.)

Downloaded / online cache: `benchmarks/data_cache/`  
Adapters: `closure/dataset_adapters.py`  
Commands:

```bash
python3.11 benchmarks/download_open_datasets.py --force
python3.11 benchmarks/run_open_data_closure.py
```

Artifact: `benchmarks/results/open_data_closure_reunified.json`

## Composition rules

* `weights_optional: true`
* Do not equate RND1 weights with the biological external stack
* Goel architecture binds under our Chaitin hair
* Omnii remains reported-only until a public interface exists
* Every downloaded dataset row must record license, split, revision

## Verdict

```text
CLOSED_PAPER_ARCHITECTURE_DATA_CATALOG
MEASURED_PAPER_DATA_LAYER_IN_EXTERNAL_SUITE
MEASURED_OPEN_DATASET_ONLINE_SAMPLES_IN_CLOSURE
MEASURED_OUR_CLOSURE_ADMISSION_VS_FRONTIER_PAPERS
CLOSED_RND1_30B_AS_FINITE_AI_SUBSTRATE_TEST_NOT_BIO
OPEN_FULL_OPENGENOME2_CORPUS_MIRROR
OPEN_EVO_WEIGHT_EXECUTION_ON_CATALOGUED_DATA
OPEN_BIOLOGICAL_THREE_ARM_RESULT
OPEN_LINCS_SCPERTURB_ADAPTERS
```

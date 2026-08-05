# Upstream provenance

This work incorporates the public `RadicalNumerics/RND1` source tree from the
[Radical Numerics](https://github.com/RadicalNumerics) GitHub organization.

| Field | Value |
|-------|-------|
| Organization | https://github.com/RadicalNumerics |
| Upstream repository | https://github.com/RadicalNumerics/RND1 |
| Upstream default branch | `main` |
| Copied commit | see `UPSTREAM_COMMIT` / `docs/upstream/RND1_MANIFEST.json` |
| License | Apache License 2.0 |
| Copyright | Copyright 2025 Radical Numerics Inc. (`LICENSE`, `NOTICE`) |
| Public model reference | `radicalnumerics/RND1-Base-0910` |
| Org site | https://radicalnumerics.ai/ |

## Verification against Radical Numerics

Recorded verification artifact: `docs/upstream/RND1_MANIFEST.json` (REPORTED ARTIFACT).

```bash
python scripts/verify_radicalnumerics.py
# or
RND1_UPSTREAM_PATH=/path/to/RND1 pytest -q tests/test_radicalnumerics_verify.py
```

Checks:

1. Org + repo identity and recorded commit
2. Byte-identical pristine upstream files (model, config, visualizer, LICENSE, NOTICE, demo)
3. Intentional closure deltas only in `sampling.py`, `generation_config.py`, `generation_utils.py`, `__init__.py`
4. `closure_mode="off"` behavioral equivalence to live `diffusion_sample`
5. External weights remain `radicalnumerics/RND1-Base-0910` (not vendored)

Related org repos ([spear](https://github.com/RadicalNumerics/spear), [dInfer](https://github.com/RadicalNumerics/dInfer), sglang, cutlass, …) are **not** vendored; this integration targets RND1 inference only.

## What was copied

From commit in `UPSTREAM_COMMIT`:

- `rnd/` package (`configuration_rnd.py`, `modeling_rnd.py`, `sampling.py`, …)
- `LICENSE`, `NOTICE`, `demo_rnd_generation.py`, upstream `.gitignore` / pre-commit config
- Upstream README preserved at `docs/upstream/RND1_README.md`

Model weights are **not** copied. Load them from Hugging Face.

## What was added

- `closure/` — unified IVI–NRR / Black Mirror axiometry; topologies admitted in resolution
- Closure hooks in `rnd/sampling.py`, `rnd/generation_config.py`, `rnd/generation_utils.py`
- Finite tests, mock sampler tests, Radical Numerics verify tests, full-model benchmark harness

## History note

The GitHub connector used for the initial scaffold lacked a whole-repository fork operation. The full public source is present in-tree with Apache-2.0 notices intact and the exact upstream commit recorded. Upstream git history remains on `RadicalNumerics/RND1`; this repository does not rewrite Radical Numerics authorship.

## License interaction

Closure-native modules are provided for use with the Apache-2.0 RND1 code. The upstream license and copyright notices are preserved. Closure does not claim ownership of the upstream model or weights.

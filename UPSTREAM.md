# Upstream provenance

This work is derived from the public `RadicalNumerics/RND1` repository.

- Upstream repository: `RadicalNumerics/RND1`
- Upstream default branch: `main`
- License: Apache License 2.0
- Public model reference: `radicalnumerics/RND1-Base-0910`

The upstream inference design uses iterative masked diffusion and entropy/confidence-based token commitment. This repository preserves that model role while adding a separate closure-derived controller. Closure determines whether a proposal is admitted, refused, rejected, or remains open; it does not modify the meaning of the upstream license or claim ownership of the upstream model.

## Source reconciliation

The GitHub connector does not expose a repository-fork operation. The integration therefore records upstream provenance and reconstructs the compatible package surface plus closure-native modules in this repository. Model weights are loaded from the upstream Hugging Face identifier and are not copied into Git.

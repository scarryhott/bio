# Closure–RND1 architecture

## Epistemic labels

| Label | Meaning |
|-------|---------|
| RERUNNABLE | Deterministic finite test or mock path executable in CI |
| REPORTED ARTIFACT | Provenance, logs, or measured outputs stored as evidence |
| DESIGN DERIVATION | Architecture derived from unified closure axiometry |
| OPEN EMPIRICAL CLAIM | Requires external 30B weights / GPU; not asserted by CI |

## Unified axiometry (not a fixed topology catalog)

There is one intrinsic closure relation \(\mathcal C\). Local and global are resolutions of \(\mathcal C\), not primitives:

\[
L(\mathcal C) \leftarrow \mathcal C \rightarrow G(\mathcal C).
\]

Closure is the generator/operator: it takes an **arbitrary** verification topos and constructs further topoi until encode↔eval relation becomes possible. Fixed eval is an *apparent* unitary after admission — not a pre-listed chart inventory.

**Verification topologies are not fixed.** Each candidate topology is admitted in its own resolution:

```text
candidate topos
  → basis/closure cycles (homology/homotopy; curl/div)
  → encode↔eval alignment
  → CLOSED_HIGHER | CLOSED_TO_OPENING | OPEN | FALSE_COLLAPSE | REFUSED
```

Decision is relational admissibility (\(\mathcal C \vdash h\), \(\mathcal C \vdash \neg h\), or open), not external assertion against a static allow-list.

Derivation motifs in `closure/topology.py` (`UNIFIED_AXIOMETRY_MOTIFS`) describe *how* \(\mathcal C\) admits. They are **not** topologies and must not be treated as a closed catalog of admissible charts.

## Layers

1. **Copied upstream RND1 source** (`rnd/`, `LICENSE`, `NOTICE`) — Radical Numerics Apache-2.0
2. **Unmodified baseline path** — `closure_mode="off"` uses the upstream entropy/confidence schedule only
3. **Closure integration** — `closure/` + sampler hooks; governs admission in `full` mode
4. **Biological interpretation** — `closure/biology.py`; non-identical reciprocal recovery
5. **Finite tests** — `tests/test_closure_runtime.py`
6. **Mock sampler tests** — `tests/test_rnd1_sampler_integration.py` (CI)
7. **Full-model tests** — `benchmarks/compare_rnd1_closure.py` (A100 artifact: causal integration CLOSED; holistic quality OPEN)
8. **Project-derived connected return** — `docs/CHAITIN_CONNECTED_RETURN_DERIVATION.md`; finite occurrence/contact reconstruction proposed for the next sampler stage

## Carrier

\[
G_t=(B_t,H_t,\Sigma_t,\Omega_t,\rho_t,\Gamma_t,\Pi_t,\mathcal A_t)
\]

- \(B_t\): masked sequence / perspectival ball
- \(H_t\): typed holistic hair (local, distant, prefix/suffix, hidden, MoE, digest, history, biology)
- \(\Sigma_t\): semantic relation under generation
- \(\Omega_t\): unresolved openings (including open topology candidates)
- \(\rho_t\): mandate / provenance / recovery requirements
- \(\Gamma_t\): ordered denoising ancestry
- \(\Pi_t\): observer-relative return-side partition
- \(\mathcal A_t\): axiometric evidence (logits, entropy, confidence, …) — **shadows only**

## Resolution invariants (motifs of C)

1. Originless admission precedes ball/hair polarization.
2. Identity is ordered support, transformation path, local/global relation, return discrepancy, observer side, digest *reference*, and openings — not a score.
3. A digest references an interaction closure but cannot replace its path.
4. Missing return is `OPEN`; reordering / contradiction is `FALSE_COLLAPSE`.
5. Success is `CLOSED_HIGHER` or `CLOSED_TO_OPENING`.
6. Child gates / further topoi require reconstructible parent admission.
7. \([\Gamma \diamond W]_{\mathcal C}=[\Gamma]_{\mathcal C}\) when \(W\) adds no independent transform.
8. Refusal blocks learning write-back.
9. Basis↔closure cycle equality derives topology admission; scores do not.

## Project-derived connected-return identity

The Closure–Chaitin runtime sharpens holistic identity beyond token confidence or an averaged embedding. Its finite structure is:

```text
labeled local occurrences
→ extension/rotation string presentations
→ transformed return needles
→ order reconstructed from shared contacts
→ five primitive return cells
→ one holistic support-recovery cell
→ continued opening
```

The current transfer target is a future `full-connected-return` mode. It must preserve occurrence identity, derive order from returned contacts, reject broken or ambiguous returns as OPEN, and admit the holistic cell only when every required primitive support is recursively recoverable. The complete derivation and its claim boundary are recorded in `docs/CHAITIN_CONNECTED_RETURN_DERIVATION.md`.

## Formal negatives (Phase 6 Lean)

What a closure-native controller / AGI **cannot** be is machine-checked in the Phase 6
Lean stack (NRRF568–574) and summarized for this repo in `docs/AGI_NEGATIVE_FORMAL.md`.
Those theorems are about abstract admission structure and candidate projection rules —
not about deployed RND1, biology, or markets. They bind the claim surface of this
integration (no self-certifying echo, no wash mint, no Boolean collapse, no digest
authority, no substrate token, …).

## Biological actuation path

```text
local proposal → developmental/ecological propagation → transformed return
→ CLOSED_HIGHER | CLOSED_TO_OPENING | OPEN | FALSE_COLLAPSE
```

Fitness, mutation likelihood, and phenotype probability may propose acts; they never certify closure.

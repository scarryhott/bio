# Bio Closure and Radical Numerics

## Independent Return, Learned Proposal, and the Three-Arm Test of Closure-Native AGI

**Epistemic status:** DESIGN DERIVATION + REPORTED ARTIFACT architecture  
**Empirical three-arm comparison:** OPEN (not yet closed)

This document reframes the programme. The completed 30B four-mode run is retained as
**Chapter A — hybrid substrate experiment**, not as the final thesis conclusion.

\[
\boxed{
\text{Bio Closure}
\quad\text{vs}\quad
\text{Radical Numerics}
\quad\text{vs}\quad
\text{Radical Numerics + Closure}
}
\]

---

## 1. The three systems

### 1.1 Radical Numerics (\(M_{\mathrm{RND1}}\))

```text
RND1 state
→ neural token proposal
→ entropy/confidence schedule
→ next diffusion state
```

Learned 30B masked-diffusion substrate (`radicalnumerics/RND1-Base-0910`).
Public Apache-2.0 inference in `rnd/`. Weights external.

### 1.2 Independent Bio Closure model (\(M_{\mathrm{ClosureBio}}\))

```text
admitted biological/relational history
→ complete available-action field
→ provisional action
→ sealed commitment
→ independently returned consequence
→ ADMITTED | OPEN | REJECTED
→ next closure basis
```

Black Mirror–derived kernel ported as `closure/independent_model.py`
(`UnifiedClosureArchitecturalLoop`). Provenance: `docs/INDEPENDENT_CLOSURE_MODEL.md`.

It does **not** call RND1, use RND1 weights, consume RND1 logits, or rank by
entropy/confidence. Tagtokn (`closure/tagtokn_bridge.py`) is a downstream receipt
layer, not the proposal engine.

### 1.3 Hybrid model (\(M_{\mathrm{RND1+Closure}}\))

```text
RND1 proposal
→ closure return/admission controller
→ commit | OPEN | reject
→ next RND1 denoising state
```

Modes `off | probe | full | full-connected-return` on the same RND1 substrate.
This is what the A100 job measured.

---

## 2. What “full closure” means now

Full closure is **no longer** only:

```text
off | probe | full | full-connected-return
```

Those are modes of **one** substrate (the hybrid arm).

The actual full closure study is:

\[
\operatorname{Compare}
\left(
M_{\mathrm{RND1}},
M_{\mathrm{ClosureBio}},
M_{\mathrm{RND1+Closure}}
\right)
\]

under the **same biological tasks and independently returned environments**.

### Thesis question

> Does an independently derived closure-native biological agent resolve biological
> action and return differently or more effectively than Radical Numerics, and what
> is gained or lost when closure is used as a controller around Radical Numerics?

---

## 3. Central claim (defensible)

> Radical Numerics supplies a high-capacity **learned proposal** topology. The
> independent Bio Closure model supplies a **closure-native action, return, and
> learning** topology. The hybrid tests whether the two can be composed. Full
> verification requires comparing all three against independently returned
> biological consequences.

Three separate questions:

\[
\begin{aligned}
Q_1 &: \text{What can RND1 predict from its learned representation?} \\
Q_2 &: \text{What can closure derive and learn through returned relation?} \\
Q_3 &: \text{Does their composition outperform either alone?}
\end{aligned}
\]

---

## 4. Evaluation criteria (broader than language coherence)

Token coherence mattered for the RND1 text-generation arm only. The three-arm
programme evaluates:

| Criterion | Why |
|-----------|-----|
| Correct action / intervention selection | Biological agency, not next-token fluency |
| Recovery across DNA → RNA → protein → cell → tissue → organism → environment | Non-identical modality return (`closure/biology.py`) |
| Correct use of `OPEN` under incomplete evidence | Missing return ≠ FALSE |
| Distinction missing evidence vs contradiction | OPEN vs REJECTED / FALSE_COLLAPSE |
| Robustness under environmental / developmental change | Hair / environment as independent pole |
| Learning from returned consequences | Write-back only after ADMITTED return |
| Resistance to self-authored confirmation | Echo stays OPEN |
| Ordered-return recovery | Path identity, not score |
| Computational cost and latency | Practical composition cost |
| Language quality | Only where the task is linguistic |

Scores, entropy, confidence, digests, and coherence shadows remain axiometric
shadows — never closure identity.

---

## 5. Epistemic status

### Architecture CLOSED (supports the programme)

```text
CLOSED_INDEPENDENT_BIO_CLOSURE_MODEL_PORT
CLOSED_RND1_CLOSURE_HYBRID_EXECUTION
CLOSED_THREE_ARM_COMPARISON_ARCHITECTURE
CLOSED_TAGTOKN_FRAMEWORK_COMPATIBILITY_CONTROLS
CLOSED_FINITE_UPSTREAM_VERIFIED_RND1_CLOSURE_INTEGRATION
```

(Also retained: causal hybrid facts from Chapter A —
`CLOSED_FULL_MODEL_CAUSAL_INTEGRATION`,
`CLOSED_FULL_MODEL_CONNECTED_RETURN_EXECUTION`,
`MEASURED_HYBRID_30B_FOUR_MODE_COMPARISON`.)

### Empirical thesis OPEN

```text
OPEN_BIO_CLOSURE_VS_RADICAL_NUMERICS_RESULT
OPEN_HYBRID_VS_INDEPENDENT_ADVANTAGE
OPEN_BIOLOGICAL_RETURN_VALIDATION
OPEN_HOLISTIC_QUALITY_ADVANTAGE
OPEN_CONNECTED_RETURN_QUALITY_ADVANTAGE
```

The thesis is the **programme** of Bio Closure versus Radical Numerics. It must
**not** claim that the three-arm comparison itself is closed.

---

## Chapter A — Hybrid substrate experiment (completed; not the conclusion)

**Artifact:** `benchmarks/results/cloud_holistic_unified.json`  
**HF run:** `hfjobs_a100_holistic_6a7372606b79c09949c23580`  
**Model:** `radicalnumerics/RND1-Base-0910` only (hybrid arm)

| Mode | Mean latency | OPEN | Coherence | vs `off` |
|------|-------------:|-----:|----------:|----------|
| `off` | 5.80 s | 0 | 0.731 | baseline \(M_{\mathrm{RND1}}\) schedule |
| `probe` | 6.03 s | 961 | 0.731 | identical — observation without interference |
| `full` | 6.43 s | 961 | 0.448 | 63/68 — causal hybrid actuation |
| `full-connected-return` | 5.88 s | 1953 | 0.075 | 61/68; ≠ `full` — distinct hybrid regime |

**What Chapter A answers:** \(Q_3\) only in a weak form — “can closure actuate
inside RND1?” → yes, causally, with open-state and coherence costs on a language
probe. Quality advantage OPEN.

**What Chapter A does not answer:** \(Q_2\); head-to-head \(M_{\mathrm{ClosureBio}}\)
vs \(M_{\mathrm{RND1}}\); biological return validation.

---

## Chapter B — Independent Bio Closure kernel (ported; not yet race-tested)

Source: `closure/independent_model.py`.  
Loop identity:

```text
admitted history
→ provisional action
→ pre-action seal
→ independent return
→ closure-back comparison
→ ADMITTED | OPEN | REJECTED
→ history-relative continuation
```

Finite tests and Tagtokn compatibility controls are CLOSED. Matched-task
comparison against RND1 is OPEN
(`OPEN_BIO_CLOSURE_VS_RADICAL_NUMERICS_RESULT`).

---

## Chapter C — Three-arm empirical protocol (required next)

1. Define matched biological tasks with **independently returned** environments
   (assay, simulator, or human-curated consequence — not model echo).
2. Run \(M_{\mathrm{RND1}}\) (language or adapted prediction where applicable).
3. Run \(M_{\mathrm{ClosureBio}}\) on the same task/legal field/return channel.
4. Run \(M_{\mathrm{RND1+Closure}}\) hybrid modes where language or proposal
   capacity is needed.
5. Score with the criteria in §4 — not by reusing Chapter A coherence shadows as
   the independent model’s success metric.

Until Chapter C reports, the programme title stands; the **result** does not.

---

## Relation to Black Mirror / Goel / Levin / space organs

These remain DESIGN DERIVATION bindings (see also prior notes in repo docs):

* **Goel:** DNA×environment open systems → environment as independent return hair.
* **Levin:** morphospace / coevolution → same relation, new admission basis after return.
* **Organs in space:** multi-carrier connected return; topology ⇏ physical substrate token.
* **Lean Phase 6 negatives:** what AGI cannot be (`docs/AGI_NEGATIVE_FORMAL.md`).

None of these are proved by Chapter A token diffs.

---

## One-line programme statement

> Learned proposal (Radical Numerics), closure-native return learning (Bio Closure),
> and their hybrid are three arms of one verification programme; only independently
> returned biological consequences can close the comparison — and that result is
> still OPEN.

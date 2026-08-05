# Independent closure-native model

## Source identity

This package ports the independently derived project model named
`UnifiedClosureArchitecturalLoop` into `scarryhott/bio` as a first-class model,
separate from the RND1 sampler controller.

Its native operation is:

```text
(C_t, E_t, A_legal,t)
→ A_t
→ (E_t+1, A_legal,t+1)
→ C_t+1
```

The model originates proposals from its own admitted relational history and the
complete current legal-action field. It does not call RND1, use RND1 weights,
consume RND1 logits, or rank by entropy/confidence.

## Closure identity

The complete identity-bearing unit is:

```text
admitted history
→ provisional action
→ pre-action seal
→ independent return
→ closure-back comparison
→ ADMITTED | OPEN | REJECTED
→ history-relative continuation
```

A model echo or self-authored replay remains `OPEN`. Missing witness or return
authority remains `OPEN`. A contradictory or unrecoverable return is
`REJECTED`. Only a complete independently returned cycle is `ADMITTED` and
enters authoritative memory. Repetition does not inflate memory.

## Relationship to the three-arm programme

Programme thesis: `docs/UNIFICATION_THESIS.md`.

The existing 30B result is **Chapter A** — hybrid substrate only:

```text
RND1 proposal + closure admission
```

This package is arm \(M_{\mathrm{ClosureBio}}\):

```text
closure-native proposal + closure-native return resolution
```

A valid future comparison is:

1. native RND1;
2. independent closure-native model;
3. RND1 + closure hybrid;

under matched biological tasks and independently returned environments. Token
coherence from the previous RND1 run is not a score for this independent model.
Empirical status: `OPEN_BIO_CLOSURE_VS_RADICAL_NUMERICS_RESULT`.

## Tagtokn compatibility audit

The bridge in `closure/tagtokn_bridge.py` was checked against Tagtokn's native
framework:

- originless closure precedes token issuance;
- OPEN claims do not count as supply;
- self-authored replay stays OPEN;
- contradiction issues no token;
- only an independently returned admitted unity issues one semantic receipt;
- residual continuation can open a child gate;
- price and human worth remain downstream/excluded projections.

Tagtokn is therefore a receipt and network-projection layer around the model,
not the model's proposal engine or closure authority.

## Scope

This is a provenance-preserving compact executable port of the project's
independent loop, not a byte-identical mirror of the entire historical workspace.
It is a finite software architecture and does not prove unrestricted AGI,
consciousness, biological closure, or physical unification.

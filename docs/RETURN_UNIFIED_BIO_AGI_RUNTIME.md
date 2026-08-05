# Return-unified biological AGI runtime

Status date: 2026-08-05

This document records the ARC-derived correction governing the biological programme.

## Core correction

Closure is not pretraining, post-training, reranking, an external benchmark, or a downstream verifier attached after a model prediction. Closure is the return-unified runtime in which data, action, environment, candidate verification topology, and admitted memory are resolved together.

The incorrect pipeline is:

```text
train model
→ generate prediction
→ closure checks prediction
→ accept or reject
```

The project runtime is instead:

```text
current relational basis
↔ available observations and actions
↔ provisional transformation
↔ environmental return
↔ verification topology generated within the return
↔ integrated next basis
```

A compact relation is:

```text
(C_t, E_t, A_legal,t)
↔_C
(A_t, E_t+1, R_t, V_t, C_t+1)
```

`V_t` is not assumed to be a fixed evaluator. A candidate verification topology is admitted, rejected, refused, or left OPEN through the same return it attempts to resolve.

## ARC origin

The ARC/AGI runtime used an interaction carrier of the form:

```text
U_t = (E_t, A_legal,t, A_t, E_t+1, T_t, ...)
C(U_t) = interaction_C:<digest>
S_t+1 = Integrate(S_t, C(U_t), rho_t)
```

The closure identity is the maintained interaction relation, not the action identifier, ARC level, score, PASS count, confidence, reward, or static rule label.

Learning therefore occurs as the episode closes. The runtime does not first train a complete fixed model and later submit its outputs to closure.

## Biological carrier

The biological carrier can include:

```text
DNA sequence
RNA expression
protein state
cellular phenotype
environmental condition
intervention history
learned model representations
measured consequence
```

These are not declared unified merely because they are concatenated or embedded together. They enter as partial perspectives of one unresolved relation. Closure determines:

- which signals belong to the same episode;
- which remain projection shadows;
- which candidate topology can compare them;
- whether a maintained relation is recoverable;
- whether evidence is missing, contradictory, or refused;
- how local and global are repartitioned for the next episode.

Data becomes authoritative memory only as its relation is resolved:

```text
C_t+1 = Integrate(C_t, Resolve_C(B_t, H_t, Sigma_t, Gamma_t, R_t))
```

This is not equivalent to appending new data to a database or updating a score.

## Local/global return

The local ball and global hair are perspectival and return-generated, not permanently fixed partitions.

A local carrier may be a nucleotide, molecule, cell, assay, organism, or observer. Its global continuation may include tissue state, environment, intervention history, population, evolution, or another modality. A return can repartition these roles:

```text
(B_t, H_t) --return--> (B_t+1, H_t+1)
```

A locally observed mutation may become a global organism-level constraint. An environmental return may become part of the next local cellular basis.

## Learned biological models inside closure

Evo, Evo 2, RND1, or another learned representation must not be described merely as proposal generators followed by a closure filter. Their states and outputs participate inside the episode together with biological data, action, environment, return, and memory.

The native learned-model organization is:

```text
fixed learned representation
→ prediction or generation
→ externally defined benchmark
```

The closure-native organization is:

```text
relational basis
↔ action
↔ environment
↔ independent return
↔ endogenous verification topology
↔ integrated next basis
```

The unified learned-representation closure runtime is:

```text
learned biological representations
↔ biological observations and available actions
↔ organism/environment transformation
↔ independent return
↔ topology admission
↔ representation and memory continuation
```

This changes inference, verification, memory, and future action. It is not post-processing.

## Goel DNA/environment operator

A Goel-inspired DNA/environment layer should participate in the same coupled episode:

```text
(D_t, O_t, E_t, Q_t, A_t, R_t) --C--> (D_t+1, E_t+1, C_t+1)
```

Here DNA is not isolated code, the operator is not merely a fixed deterministic function, and environment is not an auxiliary feature vector. The measured return changes which relation and verification topology are admissible.

Any explicit quantum variable remains an empirical hypothesis or measured carrier field. It is not inferred merely from use of the word `quantum`.

## Runtime sequence

1. Admit the current relational basis provisionally.
2. Expose the currently available observation, measurement, and action field.
3. Generate a provisional transformation within that basis.
4. Preserve the pre-return relation.
5. Allow organism, environment, and model interaction to transform the episode.
6. Receive independently returned evidence.
7. Generate candidate verification topologies from that return.
8. Resolve those topologies through the same closure relation.
9. Admit, reject, refuse, or leave the relation OPEN.
10. Integrate only the resolved relational identity.
11. Repartition local and global for the next episode.

The project phrase `learn → close → act` is reciprocal in execution:

```text
learn ↔ close ↔ act ↔ return
```

## Comparison design

The biological comparison must compare runtime organizations rather than treating all systems as static predictors:

1. native learned biological runtime;
2. closure-native return-unified runtime;
3. learned-representation return-unified runtime.

The same held-out biological episodes should be used where possible. Metrics such as accuracy, likelihood, entropy, confidence, latency, and fitness remain instruments. They do not alone authorize closure.

A result may be called an empirical advantage only after independent returned consequences show reproducible improvement in prespecified dimensions such as task success, correct OPEN behavior, contradiction handling, cross-modal recovery, experiment selection, or externally validated novelty.

## Current verdict

```text
CLOSED_ARC_DERIVED_RETURN_UNIFIED_RUNTIME_ARCHITECTURE
CLOSED_DATA_AS_RESOLVED_RELATION_PRINCIPLE
CLOSED_ENDOGENOUS_VERIFICATION_TOPOLOGY_DESIGN
CLOSED_LOCAL_GLOBAL_REPARTITION_DESIGN

OPEN_EVO_REPRESENTATION_IN_RETURN_UNIFIED_RUNTIME
OPEN_GOEL_DNA_ENVIRONMENT_OPERATOR_RUNTIME
OPEN_PUBLIC_BIOLOGICAL_RETURN_DATA_ADAPTERS
OPEN_FULL_BIOLOGICAL_UNIFICATION_AGI_EXECUTION
OPEN_EMPIRICAL_SUPERIORITY
```

The central thesis is:

> Closure is the originless return-unified operation through which data, action, environment, verification topology, and memory become jointly admissible. Biological data is integrated only as its relation is resolved, and each resolution generates the basis for the next act.

# Negative formal results — what AGI cannot be

**Epistemic status:** DESIGN DERIVATION / machine-checked abstract admission structure  
**Not:** empirical claims about deployed software, biology, physics, markets, or the A100 RND1 run.

Source: Black Mirror Phase 6 Lean modules (committed upstream of this bio tree):

| Module | Role |
|--------|------|
| `NRRF568BlackMirrorEmergentTopologyGate.lean` | Native gate, return, non-repetition, three-valued admissibility |
| `NRRF569BlackMirrorProjectionShadows.lean` | Projection / valuation shadows vs native closure |
| `NRRF570BlackMirrorClosureEpisodeIndependence.lean` | Episodes, anti-gaming, learn→close→act, Sybil boundary |
| `NRRF571BlackMirrorGeneralConnectedReturn.lean` | Generalized connected return over carriers |
| `NRRF572BlackMirrorCoevolutionaryRepartition.lean` | Finite coevolution, staleness, refusal vs learning |
| `NRRF573BlackMirrorSemanticTokenValueCycle.lean` | Semantic tokens and local/global value cycle |
| `NRRF574BlackMirrorNestedGatesRecursiveTopoi.lean` | Nested games / child–parent recoverability |

Companion maps: `BLACK_MIRROR_PHASE6_LEAN_MODULES.md`, `NRR_BLACK_MIRROR_EMERGENT_TOPOLOGY_ANALYSIS.md`.  
Build: no `sorry`/`admit`; axioms only `propext`, `Classical.choice`, `Quot.sound` (`#print axioms`).

These theorems constrain **what a closure-native AGI / controller is forbidden to claim**. They do not establish that any deployed system *is* AGI.

---

## Negative catalogue (AGI cannot be…)

### 1. A self-certifying author of its own admitted chart

`selfCertified_no_token` (NRRF570): a return by a perspective that authored an admitted chart **closes nothing**.  
AGI cannot bootstrap closure by echoing its own authorship as independent return.

### 2. A per-step token mint / activity inflation engine

`episode_tokens_le_one`, `long_episode_single_token`, `naive_count_inflates_native_does_not` (NRRF570):  
an episode issues **at most one** token; archiving arbitrarily many pointings does not multiply native tokens.  
Naive counters inflate; disclosed topology count need not.  
AGI cannot equate volume of internal steps with closure supply.

### 3. A Sybil-immune agent by declaration alone

`controllerIndependent_of_injective`, `declared_independence_does_not_imply_controller_independence` (NRRF570):  
declared independence is genuine **only** when the controller assignment separates perspectives.  
Sybil resistance remains **OPEN** as an empirical/governance claim; Lean records the boundary, it does not close it.

### 4. An actor before return / after refusal

`no_admissible_action_before_return`, `child_gate_open`, `child_gate_no_token`,  
`respond_correct_open`, `respond_refuse_open`, `no_token_after_refusal`, `correction_ne_refusal` (NRRF570):  
learn → close → act; no admissible action before return; refusal blocks token and is not correction.  
AGI cannot “act closed” from an OPEN or refused gate.

### 5. A single-chart unifier of connected return

`demo_verdict` with `demo_no_direct_edge` (NRRF571): connected return can close across six carriers / depth 5 **without** a direct chart edge from return source to target.  
`token_disclaims_physical_unification`, `topology_does_not_determine_carrier_domains`:  
same disclosed topology over disjoint carriers — a token **cannot** certify shared physical substrate.  
AGI cannot be a substrate-unifying oracle by token possession.

### 6. A score-driven coevolutionary judge at seal time

`sealed_action_undetermined`, `partition_merges_on_return`, `token_count_not_faithful` (NRRF572):  
archive at seal does not decide admissible actions; return **rederives** partition; equal token counts can sit over ⊆-incomparable topologies.  
`stale_no_token`, `scaling_open`, `scaling_not_collapse`, `scaling_no_token`:  
budget exhaustion / staleness reopen — never reported as contradiction or closure.  
AGI cannot treat resource limits or seal snapshots as FALSE_COLLAPSE / CLOSED.

### 7. A learning writer under refusal

`refusal_no_learning_commit` vs `acceptance_commits_learning` (NRRF572):  
refusal blocks learning write-back.  
AGI cannot update the maintained fibre through a refused gate.

### 8. A local-only or global-only value closer

`local_only_no_token`, `global_only_no_token`, `crossing_return_closes` (NRRF573):  
neither pole of the value cycle closes alone.  
`K_le_one`, `scalar_loses_information`: scalar \(K\) is telemetry, **not** the token.  
AGI cannot mint closure from a local score, a global score, or \(K\) injectivity.

### 9. A fabricator of inner unity / digest authority

`fabricated_inner_unity_rejected`, `digest_only_child_no_authority`, `orphan_child_cannot_close` (NRRF574):  
disclosed topology contains only generated charts; same digest ⇒ possibly different verdicts; orphan child cannot close.  
`outer_boundary_is_another_local_ball`: closed child inside still-OPEN parent.  
AGI cannot promote digests or fabricated inner unity into parent authority.

### 10. A Boolean admissibility machine or echo-closer

`adm_not_boolean`, `Gate.verdict_of_echo`, `Gate.verdict_of_unreached`, `Gate.no_token_of_no_return`, `Gate.no_token_of_collapse` (NRRF568):  
admissibility is three-valued; model echo / withheld return → OPEN (not FALSE); collapse issues no token.  
`wash_invariance` / \([\Gamma \diamond W]=[\Gamma]\): wash activity archives but does not change disclosed topology.  
`archive_does_not_determine_verdict` (NRRF568) + projection shadows (NRRF569):  
same charts ≠ same verdict; price/gross/eigenpair shadows ≠ native supply.  
AGI cannot be a Boolean classifier, a wash-inflated ledger, or a projection that replaces return.

### 11. A catalogue picker of verification topologies

`unregistered_operation_admitted` (NRRF568): operations outside prescribed vocabulary are admitted when return supports them — topology is **disclosed**, not chosen from a catalogue.  
Matches this repo’s `closure/topology.py` stance: motifs ≠ fixed chart list.

---

## Binding to this RND1 integration

| Lean negative | Bio / RND1 consequence |
|---------------|------------------------|
| Observation ≠ actuation (echo / self-certify) | `probe` may equal `off` while recording OPEN; that is telemetry, not closure identity |
| Actuation requires return-anchored admission | `full` changing tokens is causal intervention, **not** proof of quality or AGI |
| Shadows ≠ tokens | `coherence_shadow`, digests, open counts, latency ≠ authorization |
| No universal substrate token | Connected MoE / biology carriers do not certify physical unification |
| Sybil / independence OPEN | Controller separation not established by declaration in software |

**Still forbidden claims for this project:**

- unrestricted AGI  
- self-certified closure by model echo  
- quality win from causal token diffs alone  
- universal Chaitin / RH / physical black–white identification  
- Sybil-proof identity from declared perspective labels  

Finite stage + A100 causal stage remain as in `docs/STAGE_STATUS.md`. Phase 6 Lean **tightens the negative envelope**; it does not upgrade empirical quality or AGI status.

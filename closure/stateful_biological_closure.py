# Copyright 2026 scarryhott/bio contributors.
"""Stateful biological closure: one shared C_t across all episodes.

Transcript doctrine (IVI–NRR / identifiability retained):

    Closure is the generator that takes relations and constructs further
    structure; NRR absorbs admissible diagonals into a multi-directional
    bundle; what survives across cycles is the ledger of admissible relations.

This module replaces aggregate Close(E_i) with the stronger chain:

    C_0 --E_1--> C_1 --E_2--> C_2 --…--> C_n

and derives unresolved cross-dataset propositions h from that common history.
Newly generated h remains δ_C(h)=OPEN until an independent empirical return
witnesses it — scores never certify.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Sequence

from .digest import digest
from .independent_model import (
    ORIGINLESS_GENESIS,
    Admission,
    UnifiedClosureArchitecturalLoop,
    stable_digest,
)
from .return_unified_runtime import (
    OpenArchitectureCarrier,
    ReunifiedAdmissionReceipt,
    ReturnUnifiedEpisodeSpec,
    architecture_from_system,
    receipt_to_dict,
    reunify_episode,
)
from .self_verification import ClosureVerificationStatus
from .topology import UnifiedAxiometry

OUR_SYSTEM = {
    "id": "bio-closure-independent",
    "family": "black-mirror-closure",
    "biological_native": True,
    "open_weights": False,
    "ownership": "scarryhott-bio-transcript-thesis",
    "adapter": "closure.independent_model:UnifiedClosureArchitecturalLoop",
    "epistemic_status": "RERUNNABLE_FINITE_KERNEL",
    "availability": "repository-local",
    "role": "OUR self-contained Closure AGI — stateful biological run",
}


@dataclass(frozen=True)
class CrossDatasetHypothesis:
    """Unresolved proposition generated from multi-dataset admitted relations."""

    hypothesis_id: str
    proposition: str
    supporting_episode_ids: tuple[str, ...]
    supporting_datasets: tuple[str, ...]
    modalities_spanned: tuple[str, ...]
    benchmark_families: tuple[str, ...]
    delta_c: str
    status: str
    proposed_resolution: dict[str, Any]
    reason: str
    nrr_role: str = "multi_directional_admissible_bundle_candidate"

    def to_dict(self) -> dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "proposition": self.proposition,
            "supporting_episode_ids": list(self.supporting_episode_ids),
            "supporting_datasets": list(self.supporting_datasets),
            "modalities_spanned": list(self.modalities_spanned),
            "benchmark_families": list(self.benchmark_families),
            "delta_c": self.delta_c,
            "status": self.status,
            "proposed_resolution": dict(self.proposed_resolution),
            "reason": self.reason,
            "nrr_role": self.nrr_role,
        }


@dataclass
class StatefulEpisodeStep:
    """One link in C_t → E → C_{t+1}."""

    index: int
    episode_id: str
    benchmark_id: str
    dataset_role: str
    c_before: str
    c_after: str
    admitted_count_before: int
    admitted_count_after: int
    receipt: ReunifiedAdmissionReceipt
    carried_prior: bool

    def to_dict(self) -> dict[str, Any]:
        row = receipt_to_dict(self.receipt)
        row.update(
            {
                "index": self.index,
                "dataset_role": self.dataset_role,
                "c_before": self.c_before,
                "c_after": self.c_after,
                "admitted_count_before": self.admitted_count_before,
                "admitted_count_after": self.admitted_count_after,
                "carried_prior": self.carried_prior,
                "chain": "C_t → E → C_{t+1}",
            }
        )
        return row


@dataclass
class StatefulBiologicalClosure:
    """One shared loop + axiometry for the complete biological run."""

    loop: UnifiedClosureArchitecturalLoop = field(
        default_factory=UnifiedClosureArchitecturalLoop
    )
    axiometry: UnifiedAxiometry = field(default_factory=UnifiedAxiometry)
    architecture: OpenArchitectureCarrier | None = None
    steps: list[StatefulEpisodeStep] = field(default_factory=list)
    open_candidates: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    hypotheses: list[CrossDatasetHypothesis] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.architecture is None:
            self.architecture = architecture_from_system(
                OUR_SYSTEM, weights_available=True
            )

    @property
    def c_t(self) -> str:
        return self.loop.memory.authoritative_digest

    @property
    def admitted_count(self) -> int:
        return len(self.loop.memory.admitted)

    def run_episode(self, episode: ReturnUnifiedEpisodeSpec) -> StatefulEpisodeStep:
        """Admit one episode into the shared evolving closure."""

        c_before = self.c_t
        n_before = self.admitted_count
        carried = c_before != ORIGINLESS_GENESIS or n_before > 0

        receipt = reunify_episode(
            self.architecture,  # type: ignore[arg-type]
            episode,
            loop=self.loop,
            axiometry=self.axiometry,
        )
        c_after = self.c_t
        n_after = self.admitted_count

        step = StatefulEpisodeStep(
            index=len(self.steps),
            episode_id=episode.episode_id,
            benchmark_id=episode.benchmark_id,
            dataset_role=episode.role,
            c_before=c_before,
            c_after=c_after,
            admitted_count_before=n_before,
            admitted_count_after=n_after,
            receipt=receipt,
            carried_prior=carried,
        )
        self.steps.append(step)

        if receipt.verification_status is ClosureVerificationStatus.OPEN or (
            receipt.operation_admission is Admission.OPEN
        ):
            self.open_candidates.append(
                {
                    "episode_id": episode.episode_id,
                    "benchmark_id": episode.benchmark_id,
                    "openings": list(episode.biological.openings),
                    "joint_arm_status": receipt.joint_arm_status,
                }
            )
        if receipt.operation_admission is Admission.REJECTED:
            self.rejected.append(
                {
                    "episode_id": episode.episode_id,
                    "benchmark_id": episode.benchmark_id,
                    "reason": receipt.reason,
                }
            )
        return step

    def run_all(
        self, episodes: Sequence[ReturnUnifiedEpisodeSpec]
    ) -> list[StatefulEpisodeStep]:
        ordered = order_episodes_for_stateful_run(episodes)
        return [self.run_episode(ep) for ep in ordered]

    def derive_cross_dataset_hypotheses(self) -> list[CrossDatasetHypothesis]:
        """Generate unresolved h from multi-dataset admitted ledger (NRR bundle).

        Does not invent empirical truth. New h defaults to δ_C=OPEN until an
        independent cross-dataset return witnesses a resolution.
        """

        admitted_steps = [
            s
            for s in self.steps
            if s.receipt.verification_status is ClosureVerificationStatus.VERIFIED
            and s.receipt.write_back_allowed
        ]
        by_dataset: dict[str, list[StatefulEpisodeStep]] = {}
        by_family: dict[str, list[StatefulEpisodeStep]] = {}
        modalities: set[str] = set()
        for step in admitted_steps:
            ds = _dataset_id(step.dataset_role, step.episode_id)
            by_dataset.setdefault(ds, []).append(step)
            by_family.setdefault(step.benchmark_id, []).append(step)
            modalities.update(step.receipt.modalities)

        generated: list[CrossDatasetHypothesis] = []

        # TraitGym + ClinVar → joint regulatory/clinical variant proposition.
        if "traitgym" in by_dataset and "clinvar" in by_dataset:
            left = by_dataset["traitgym"]
            right = by_dataset["clinvar"]
            generated.append(
                _hypothesis(
                    kind="joint_variant_regulatory_clinical",
                    left=left,
                    right=right,
                    modalities=("DNA", "returned_consequence"),
                    families=("variant-effect",),
                    proposition=(
                        "Admitted TraitGym regulatory-variant returns and ClinVar "
                        "clinical returns jointly constrain a cross-cohort variant "
                        "consequence relation that is not identical to either alone"
                    ),
                )
            )

        # ProteinGym + RNAGym → cross-molecule fitness coupling.
        if "proteingym" in by_dataset and "rnagym" in by_dataset:
            generated.append(
                _hypothesis(
                    kind="cross_molecule_fitness_coupling",
                    left=by_dataset["proteingym"],
                    right=by_dataset["rnagym"],
                    modalities=("protein", "RNA", "returned_consequence"),
                    families=("variant-effect", "rna-fitness"),
                    proposition=(
                        "Admitted ProteinGym DMS reference returns and RNAGym "
                        "fitness returns jointly open a cross-molecule fitness "
                        "coupling not reducible to either assay alone"
                    ),
                )
            )

        # OpenGenome2-family genomic context + variant-effect → continuation/phenotype bridge.
        if "opengenome2" in by_dataset and (
            "traitgym" in by_dataset or "clinvar" in by_dataset
        ):
            right = by_dataset.get("traitgym") or by_dataset["clinvar"]
            generated.append(
                _hypothesis(
                    kind="genomic_context_variant_bridge",
                    left=by_dataset["opengenome2"],
                    right=right,
                    modalities=("DNA", "returned_consequence"),
                    families=("sequence-likelihood", "gene-completion", "variant-effect"),
                    proposition=(
                        "Admitted genomic-context returns and variant-effect returns "
                        "jointly generate an unresolved bridge from local sequence "
                        "context to held-out phenotypic/clinical consequence"
                    ),
                )
            )

        # NRR multi-family bundle when ≥3 benchmark families admitted.
        families = sorted(by_family)
        if len(families) >= 3:
            support = [s for fam in families for s in by_family[fam]]
            datasets = tuple(sorted({_dataset_id(s.dataset_role, s.episode_id) for s in support}))
            hyp_id = digest(
                {
                    "kind": "nrr_multi_family_bundle",
                    "families": families,
                    "c": self.c_t,
                    "n": len(support),
                }
            )[:16]
            generated.append(
                CrossDatasetHypothesis(
                    hypothesis_id=f"nrr-bundle-{hyp_id}",
                    proposition=(
                        "NRR-style multi-directional bundle over admitted benchmark "
                        f"families {families}: collapse of any single family is not "
                        "the closure identity; the retained ledger spans all admitted "
                        "diagonals pending further independent return"
                    ),
                    supporting_episode_ids=tuple(s.episode_id for s in support),
                    supporting_datasets=datasets,
                    modalities_spanned=tuple(sorted(modalities)),
                    benchmark_families=tuple(families),
                    delta_c="OPEN",
                    status="OPEN_UNRESOLVED_CROSS_DATASET",
                    proposed_resolution={
                        "act": "seek_independent_cross_family_return",
                        "forbidden_certifiers": [
                            "AUROC",
                            "AUPRC",
                            "fitness",
                            "confidence",
                            "PASS_count",
                        ],
                        "requires": "held-out return spanning ≥2 families",
                    },
                    reason=(
                        "Transcript NRR: higher object absorbs admissible diagonals; "
                        "δ_C remains OPEN without independent multi-family return"
                    ),
                )
            )

        self.hypotheses = generated
        return generated

    def chain_is_stateful(self) -> bool:
        """True iff C_t carries forward (not reset) across successive admits."""

        if len(self.steps) < 2:
            return False
        for i in range(1, len(self.steps)):
            prev = self.steps[i - 1]
            cur = self.steps[i]
            if cur.c_before != prev.c_after:
                return False
            # After a successful write-back, authority must move (or stay only if
            # duplicate unity — still prior-linked).
            if (
                prev.receipt.write_back_allowed
                and cur.receipt.write_back_allowed
                and cur.admitted_count_before < 1
            ):
                return False
        return True

    def report(self) -> dict[str, Any]:
        if not self.hypotheses:
            self.derive_cross_dataset_hypotheses()
        verified = sum(
            1
            for s in self.steps
            if s.receipt.joint_arm_status == "VERIFIED"
        )
        stateful = self.chain_is_stateful()
        verdict = (
            "STATEFUL_BIOLOGICAL_CLOSURE_CHAIN_MEASURED"
            if stateful and verified > 0
            else "STATEFUL_BIOLOGICAL_CLOSURE_INCOMPLETE"
        )
        return {
            "schema_version": "1.0",
            "protocol": "stateful-biological-closure-across-datasets",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "relation": (
                "C_0 --E_1--> C_1 --E_2--> … --E_n--> C_n ; "
                "Close(E_1 ↔ … ↔ E_n) not Aggregate(Close(E_i))"
            ),
            "transcript_basis": {
                "closure_operator": "generator over relations until eval/halting possible",
                "nrr": "multi-directional admissible bundle above single collapses",
                "identifiability_retained": (
                    "ledger/memory of admissible relations across cycles"
                ),
                "map": "docs/transcript_closure/closure_structure_map.json",
            },
            "verdict": verdict,
            "passed": stateful and verified > 0,
            "stateful_chain": stateful,
            "episode_count": len(self.steps),
            "verified_joint_arms": verified,
            "final_c_t": self.c_t,
            "admitted_unities": self.admitted_count,
            "quarantined": len(self.loop.memory.quarantined),
            "open_candidates": list(self.open_candidates),
            "rejected": list(self.rejected),
            "cross_dataset_hypotheses": [h.to_dict() for h in self.hypotheses],
            "hypotheses_open": sum(1 for h in self.hypotheses if h.delta_c == "OPEN"),
            "epistemic": {
                "not_aggregate_of_separate_closes": stateful,
                "cross_dataset_resolutions_derived": bool(self.hypotheses),
                "new_resolutions_empirically_closed": False,
                "delta_c_new_h": "OPEN",
                "rnd1_30b_is_bio_closure": False,
            },
            "steps": [s.to_dict() for s in self.steps],
            "architecture_digest": digest(
                {
                    "final_c": self.c_t,
                    "n": len(self.steps),
                    "admitted": self.admitted_count,
                    "hypotheses": [h.hypothesis_id for h in self.hypotheses],
                }
            ),
        }


def _dataset_id(role: str, episode_id: str) -> str:
    if role.startswith("open-dataset:"):
        return role.split(":", 1)[1]
    if episode_id.startswith("traitgym"):
        return "traitgym"
    if episode_id.startswith("clinvar"):
        return "clinvar"
    if episode_id.startswith("rnagym"):
        return "rnagym"
    if episode_id.startswith("proteingym"):
        return "proteingym"
    if episode_id.startswith("opengenome2"):
        return "opengenome2"
    if episode_id.startswith("double-slit"):
        return "double-slit"
    return "finite-goel-env-returns"


def _hypothesis(
    *,
    kind: str,
    left: Sequence[StatefulEpisodeStep],
    right: Sequence[StatefulEpisodeStep],
    modalities: tuple[str, ...],
    families: tuple[str, ...],
    proposition: str,
) -> CrossDatasetHypothesis:
    support = list(left) + list(right)
    datasets = tuple(sorted({_dataset_id(s.dataset_role, s.episode_id) for s in support}))
    hyp_id = digest(
        {
            "kind": kind,
            "left": [s.receipt.turn_unity_digest for s in left],
            "right": [s.receipt.turn_unity_digest for s in right],
        }
    )[:16]
    return CrossDatasetHypothesis(
        hypothesis_id=f"{kind}-{hyp_id}",
        proposition=proposition,
        supporting_episode_ids=tuple(s.episode_id for s in support),
        supporting_datasets=datasets,
        modalities_spanned=modalities,
        benchmark_families=families,
        delta_c="OPEN",
        status="OPEN_UNRESOLVED_CROSS_DATASET",
        proposed_resolution={
            "act": "propose_joint_relation_then_seek_independent_return",
            "support_unities": [s.receipt.turn_unity_digest for s in support[:6]],
            "forbidden_certifiers": ["score", "AUROC", "fitness", "confidence"],
        },
        reason=(
            "Derived from admitted multi-dataset ledger under shared C_t; "
            "δ_C(h)=OPEN until independent empirical return spanning supports"
        ),
    )


def order_episodes_for_stateful_run(
    episodes: Sequence[ReturnUnifiedEpisodeSpec],
) -> list[ReturnUnifiedEpisodeSpec]:
    """Order so history accumulates: finite controls → open datasets by family."""

    priority = {
        "finite-goel-env-returns": 0,
        "opengenome2": 1,
        "traitgym": 2,
        "clinvar": 3,
        "proteingym": 4,
        "rnagym": 5,
        "double-slit": 6,
    }

    def key(ep: ReturnUnifiedEpisodeSpec) -> tuple[int, str, str]:
        ds = _dataset_id(ep.role, ep.episode_id)
        return (priority.get(ds, 50), ep.benchmark_id, ep.episode_id)

    return sorted(episodes, key=key)


def run_stateful_biological_closure(
    episodes: Sequence[ReturnUnifiedEpisodeSpec],
) -> dict[str, Any]:
    """Execute the complete biological run on one shared loop and axiometry."""

    runtime = StatefulBiologicalClosure()
    runtime.run_all(episodes)
    return runtime.report()


__all__ = [
    "CrossDatasetHypothesis",
    "StatefulBiologicalClosure",
    "StatefulEpisodeStep",
    "order_episodes_for_stateful_run",
    "run_stateful_biological_closure",
]

# Copyright 2026 scarryhott/bio contributors.
"""General derivation of admissible data under unified closure.

Holistic verification is not a PASS aggregate over existing checks. It reveals
the architecture by which data becomes admissible:

    provisional observation → legal action → environmental transform
      → independent return → endogenous verification topology
      → δ_C resolution → admitted memory | OPEN | refuse | reject

Scores, fitness, confidence, weight presence, and PASS counts remain shadows.
Existing train→predict→filter models never generate this derivation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .digest import digest
from .topology import UNIFIED_AXIOMETRY_MOTIFS


@dataclass(frozen=True)
class DerivationStep:
    """One step in the general admissible-data derivation."""

    step_id: str
    statement: str
    writes_memory: bool
    epistemic_note: str = ""


# Ordered general derivation — architecture, not a checklist of suites.
ADMISSIBLE_DATA_DERIVATION: tuple[DerivationStep, ...] = (
    DerivationStep(
        "originless_basis",
        "Admit current relational basis C_t provisionally; ball/hair are projections, not priors.",
        False,
        "C is prior to subject/object and to any dataset inventory.",
    ),
    DerivationStep(
        "expose_observation_field",
        "Expose provisional observation, measurement, and action field A_legal,t as candidates.",
        False,
        "Provisional data is not yet admissible identity.",
    ),
    DerivationStep(
        "provisional_transform",
        "Generate provisional act A_t inside the current basis without write-back.",
        False,
    ),
    DerivationStep(
        "preserve_pre_return",
        "Preserve the pre-return relation so return can recover identity non-identically.",
        False,
    ),
    DerivationStep(
        "environmental_transform",
        "Allow organism / environment / architecture interaction to transform the episode.",
        False,
        "Environment is a modality, not an auxiliary feature vector.",
    ),
    DerivationStep(
        "independent_return",
        "Receive independently returned consequence R_t (not model echo from a controlled boundary).",
        False,
        "Missing return → OPEN; self-authored echo → OPEN; contradiction → REJECTED.",
    ),
    DerivationStep(
        "endogenous_topology",
        "Generate candidate verification topology V_t from the return (not a fixed chart catalog).",
        False,
    ),
    DerivationStep(
        "delta_c_resolution",
        "Resolve δ_C(h): C ⊢ h, C ⊢ ¬h, or open — relational admissibility, not external assertion.",
        False,
    ),
    DerivationStep(
        "integrate_resolved_relation",
        "Integrate only the resolved relational identity into C_{t+1}; shadows never certify.",
        True,
        "Write-back is allowed only for jointly verified operation ∧ topology.",
    ),
    DerivationStep(
        "repartition_next",
        "Repartition local (Kakeya bio-token) and global (Goel–Chaitin hair, incl. δ_C(Q)) for the next episode.",
        False,
    ),
)


DATA_CLASSES: dict[str, str] = {
    "provisional_observation": (
        "Candidate ball/hair presentation before return — not memory."
    ),
    "returned_consequence": (
        "Independently measured modality that can complete a recovery cycle."
    ),
    "axiometric_shadow": (
        "Likelihood, fitness, confidence, entropy, PASS counts — may propose, never certify."
    ),
    "open_candidate": (
        "δ_C open: retained as an opening / next topos layer, not discarded as a suite failure."
    ),
    "admitted_memory": (
        "Resolved relation with write_back_allowed — enters C_{t+1}."
    ),
    "refused_or_collapsed": (
        "Mandate refusal or false collapse — positively non-admissible."
    ),
    "relative_interference_residue": (
        "Double-slit relative difference across arms; becomes δ_C(Q) only after "
        "artifact-excluded independent return."
    ),
}


CONTRAST_TO_EXISTING_MODELS: dict[str, str] = {
    "train_predict_filter": (
        "Learned proposal → prediction → external score/filter. Data is training fuel; "
        "admission is post-hoc ranking."
    ),
    "benchmark_suite_pass": (
        "Aggregated PASS/FAIL over fixed tasks. Pass counts are shadows, not identity."
    ),
    "return_unified_admission": (
        "Data becomes admissible only as its relation is resolved inside one return "
        "with endogenous verification topology. Holistic verification reveals this "
        "architecture — it does not reduce to containing a pass."
    ),
}


@dataclass
class AdmissibleDataArchitecture:
    """Revealed architecture of admissible data from a holistic verification run."""

    kind: str = "ADMISSIBLE_DATA_ARCHITECTURE"
    epistemic_status: str = "DESIGN_DERIVATION"
    relation: str = (
        "(C_t, B_bio_token, H_Goel_Chaitin_incl_δ_C(Q), E_t, A_legal,t) "
        "↔_C (A_t, E_{t+1}, R_t, V_t, C_{t+1})"
    )
    derivation_steps: tuple[DerivationStep, ...] = ADMISSIBLE_DATA_DERIVATION
    data_classes: dict[str, str] = field(default_factory=lambda: dict(DATA_CLASSES))
    motifs: tuple[str, ...] = field(
        default_factory=lambda: tuple(m.motif_id for m in UNIFIED_AXIOMETRY_MOTIFS)
    )
    contrast_to_existing_models: dict[str, str] = field(
        default_factory=lambda: dict(CONTRAST_TO_EXISTING_MODELS)
    )
    revealed_from_run: dict[str, Any] = field(default_factory=dict)
    architecture_digest: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "epistemic_status": self.epistemic_status,
            "not_a_pass_aggregate": True,
            "relation": self.relation,
            "general_derivation": [
                {
                    "step_id": s.step_id,
                    "statement": s.statement,
                    "writes_memory": s.writes_memory,
                    "epistemic_note": s.epistemic_note,
                }
                for s in self.derivation_steps
            ],
            "data_classes": dict(self.data_classes),
            "motifs": list(self.motifs),
            "contrast_to_existing_models": dict(self.contrast_to_existing_models),
            "revealed_from_run": dict(self.revealed_from_run),
            "architecture_digest": self.architecture_digest,
        }


def derive_admissible_data_architecture(
    *,
    admitted_episode_ids: Sequence[str],
    open_episode_ids: Sequence[str],
    refused_or_rejected_ids: Sequence[str] = (),
    openings: Sequence[str] = (),
    double_slit_relative: Mapping[str, Any] | None = None,
    ownership: Mapping[str, Any] | None = None,
) -> AdmissibleDataArchitecture:
    """Derive the admissible-data architecture revealed by a holistic run.

    The primary product is this architecture. Layer PASS marks are instruments
    that may appear in revealed_from_run — they never replace the derivation.
    """

    revealed = {
        "admitted_memory_episodes": list(admitted_episode_ids),
        "open_candidate_episodes": list(open_episode_ids),
        "refused_or_rejected_episodes": list(refused_or_rejected_ids),
        "next_openings": list(openings),
        "double_slit_relative_verification": dict(double_slit_relative or {}),
        "ownership": dict(
            ownership
            or {
                "closure_agi": "ours",
                "rnd1_is_our_model": False,
            }
        ),
        "principle": "data_as_resolved_relation",
        "certifiers_forbidden": [
            "mutation_likelihood",
            "fitness",
            "confidence",
            "entropy",
            "PASS_count",
            "weight_presence",
            "thermodynamic_efficiency_figures",
        ],
    }
    arch = AdmissibleDataArchitecture(revealed_from_run=revealed)
    arch.architecture_digest = digest(
        {
            "kind": arch.kind,
            "relation": arch.relation,
            "steps": [s.step_id for s in arch.derivation_steps],
            "revealed": revealed,
        }
    )
    return arch


__all__ = [
    "ADMISSIBLE_DATA_DERIVATION",
    "AdmissibleDataArchitecture",
    "CONTRAST_TO_EXISTING_MODELS",
    "DATA_CLASSES",
    "DerivationStep",
    "derive_admissible_data_architecture",
]

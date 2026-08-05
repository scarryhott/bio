# Copyright 2026 scarryhott/bio contributors.
"""Goel DNA×environment operator in parallel with Black Mirror Closure Axiometry.

PARALLEL DIALOGUE — not subsumption:

  Goel Consciousness Science  ↔  Black Mirror Closure Axiometry

Goel supplies the open-system living-motor programme, (M,E,I), and the
biological double-slit empirical roadmap. Black Mirror supplies originless C,
independent return ρ, and δ_C verification. Neither programme is reduced to
the other (see docs/GOEL_BLACK_MIRROR_PARALLEL_DIALOGUE.md).

Operational alignment in this runtime:

* Global Chaitin hair engages Goel's DNA×environment (±Q) carrier.
* Biological double-slit is a candidate Chaitin global-hair return for δ_C(Q);
  until independent artifact-excluded return, δ_C(Q)=OPEN.
* Local Kakeya / tokenized relativity is our bio-token ball (RN may propose
  tokens into it; RND1 is not our model).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .connected_return import ConnectedReturnVerdict, LocalCell
from .digest import digest
from .types import HairSource, Resolution, ReturnWitness


class PolymeraseMode(str, Enum):
    """Goel tension-tuned motor modes (PNAS 2001/2003 family)."""

    POLYMERASE = "polymerase"
    EXONUCLEASE = "exonuclease"
    STALLED = "stalled"
    SWITCHING = "switching"


class GoelOperatorStatus(str, Enum):
    ADMITTED_GLOBAL_HAIR = "ADMITTED_GLOBAL_HAIR"
    OPEN_MISSING_ENVIRONMENT = "OPEN_MISSING_ENVIRONMENT"
    OPEN_QUANTUM_UNWITNESSED = "OPEN_QUANTUM_UNWITNESSED"
    OPEN_SELF_AUTHORED = "OPEN_SELF_AUTHORED"
    REJECTED_CONTRADICTION = "REJECTED_CONTRADICTION"
    REFUSED = "REFUSED"


class BiologicalDoubleSlitStatus(str, Enum):
    """Chaitin global-hair gate for Goel's biological double-slit programme."""

    OPEN_DELTA_C_Q = "OPEN_DELTA_C_Q"
    OPEN_MISSING_CONTROLS = "OPEN_MISSING_CONTROLS"
    OPEN_COHERENCE_UNWITNESSED = "OPEN_COHERENCE_UNWITNESSED"
    REJECTED_ARTIFACT_DOMINANCE = "REJECTED_ARTIFACT_DOMINANCE"
    ADMITTED_INTERFERENCE_RETURN = "ADMITTED_INTERFERENCE_RETURN"


@dataclass(frozen=True)
class GoelProvenance:
    """Primary Goel sources used for the binding (citations, not authority)."""

    thesis: str = (
        "Anita Goel, Single Molecule Dynamics of Motor Enzymes Along DNA "
        "(Harvard Physics PhD; advisors Herschbach/Wilson)"
    )
    selected_publications_url: str = "https://sites.harvard.edu/goel/selected-publications/"
    harvard_site: str = "https://sites.harvard.edu/goel/"
    papers: tuple[str, ...] = (
        "Goel, Frank-Kamenetskii, Ellenberger, Herschbach, "
        "Tuning DNA strings: Modulating the rate of DNA replication with mechanical tension, "
        "PNAS 98(15):8485–8489 (2001). https://doi.org/10.1073/pnas.151261198",
        "Goel, Astumian, Herschbach, "
        "Tuning and switching a DNA polymerase motor with mechanical tension, "
        "PNAS 100(17):9699–9704 (2003). https://doi.org/10.1073/pnas.1033134100",
        "Goel, Ellenberger, Frank-Kamenetskii, Herschbach, "
        "Unifying Themes in DNA Replication, "
        "J. Biomol. Struct. Dyn. 19(4):571–584 (2002).",
        "Goel, Molecular Evolution: a role for quantum mechanics in the dynamics of "
        "molecular machines that read DNA, in Quantum Aspects of Life "
        "(Abbott, Davies, Pati eds.), World Scientific (2008).",
        "Goel & Vogel, Harnessing biological motors…, Nature Nanotechnology 3:465–475 (2008).",
        "Goel biological double-slit / living-systems quantum programme — "
        "https://www.essentiafoundation.org/what-if-the-molecular-machines-that-read-and-write-your-dna-are-quantum/seeing/",
    )
    parallel_dialogue: str = (
        "Goel Consciousness Science ↔ Black Mirror Closure Axiometry "
        "(docs/GOEL_BLACK_MIRROR_PARALLEL_DIALOGUE.md) — not subsumption"
    )


@dataclass(frozen=True)
class GoelDNAEnvironmentState:
    """Open-system DNA motor state: sequence + milieu, not sequence alone."""

    dna_template: Mapping[str, Any]
    environment: Mapping[str, Any]
    polymerase_mode: PolymeraseMode = PolymeraseMode.POLYMERASE
    tension: float | None = None
    nucleotide_concentration: float | None = None
    quantum_carrier: Mapping[str, Any] | None = None
    axiometric_shadows: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TokenizedRelativityBall:
    """Local Kakeya / bio-token presentation (tokenized relativity).

    Token equality ≠ occurrence identity. Local ball is relative to return side,
    contacts, and ordered support — never an absolute token chart. Optional
    external proposals (e.g. RND1) may enter this ball; they do not own it.
    """

    ball_id: str
    occurrences: tuple[dict[str, Any], ...]
    return_side: str
    contacts: tuple[str, ...]
    radical_numerics_family: str = "bio-token-kakeya-local"
    ball_digest: str = ""


@dataclass(frozen=True)
class BiologicalDoubleSlitGate:
    """Goel biological double-slit as Chaitin global-hair return candidate.

    Tests whether τ_coherence > τ_base_read with artifact-excluded interference.
    Default epistemic state is OPEN (δ_C(Q)=OPEN) until independent return.
    """

    bio_token_digest: str
    dna_locus: Mapping[str, Any]
    environment: Mapping[str, Any]
    claimed_coherence_gt_base_read: bool = False
    interference_signature_reported: bool = False
    thermal_control_excluded: bool = False
    mechanical_control_excluded: bool = False
    detector_artifact_excluded: bool = False
    independently_returned: bool = False


@dataclass(frozen=True)
class BiologicalDoubleSlitReceipt:
    status: BiologicalDoubleSlitStatus
    delta_c_q: str
    chaitin_global_hair: bool
    write_back_allowed: bool
    reason: str
    gate_digest: str
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GoelChaitinOperatorReceipt:
    """Global Chaitin-side hair receipt from a Goel DNA×environment act."""

    status: GoelOperatorStatus
    resolution: Resolution
    state_before: GoelDNAEnvironmentState
    state_after: GoelDNAEnvironmentState
    independent_return: bool
    environment_coupled: bool
    quantum_claim: str
    operator_digest: str
    recovered_relation: str
    next_opening: str | None
    write_back_allowed: bool
    provenance: GoelProvenance
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DualClosureBindingReceipt:
    """Local Kakeya ball ∧ global Goel–Chaitin hair under unified C."""

    local_ball: TokenizedRelativityBall
    global_hair: GoelChaitinOperatorReceipt
    local_connected: ConnectedReturnVerdict | None
    dual_status: str
    dual_digest: str
    reason: str


GOEL_PROVENANCE = GoelProvenance()


def infer_polymerase_mode(
    *,
    tension: float | None,
    switching_tension: float = 0.65,
    stall_tension: float = 0.95,
) -> PolymeraseMode:
    """Finite stand-in for Goel tension tuning/switching (not a biophysical replica)."""

    if tension is None:
        return PolymeraseMode.POLYMERASE
    if tension >= stall_tension:
        return PolymeraseMode.STALLED
    if tension >= switching_tension:
        return PolymeraseMode.EXONUCLEASE
    if tension >= switching_tension * 0.85:
        return PolymeraseMode.SWITCHING
    return PolymeraseMode.POLYMERASE


def goel_state_from_modalities(modalities: Mapping[str, Mapping[str, Any]]) -> GoelDNAEnvironmentState:
    dna = dict(modalities.get("DNA") or {})
    environment = dict(modalities.get("environment") or {})
    quantum = None
    if isinstance(modalities.get("quantum"), Mapping):
        quantum = dict(modalities["quantum"])
    elif isinstance(environment.get("quantum_carrier"), Mapping):
        quantum = dict(environment["quantum_carrier"])
    tension = environment.get("tension")
    if tension is None:
        tension = environment.get("mechanical_tension")
    conc = environment.get("nucleotide_concentration")
    mode = infer_polymerase_mode(
        tension=float(tension) if tension is not None else None
    )
    return GoelDNAEnvironmentState(
        dna_template=dna,
        environment={k: v for k, v in environment.items() if k != "quantum_carrier"},
        polymerase_mode=mode,
        tension=float(tension) if tension is not None else None,
        nucleotide_concentration=float(conc) if conc is not None else None,
        quantum_carrier=quantum,
        axiometric_shadows={
            k: modalities.get("returned_consequence", {}).get(k)
            for k in ("fitness", "confidence", "relative_fitness")
            if isinstance(modalities.get("returned_consequence"), Mapping)
            and k in modalities["returned_consequence"]
        },
    )


def apply_goel_chaitin_operator(
    before: GoelDNAEnvironmentState,
    after: GoelDNAEnvironmentState,
    *,
    independent: bool = True,
    self_authored: bool = False,
    contradictory: bool = False,
    refused: bool = False,
    quantum_witnessed: bool | None = None,
) -> GoelChaitinOperatorReceipt:
    """Resolve DNA×environment as the global Chaitin reverse-hair under C.

    Environment must participate. Quantum language without a witnessed carrier
    leaves the quantum *claim* OPEN without blocking an otherwise independent
    classical open-system return.
    """

    environment_coupled = bool(before.environment) and bool(after.environment)
    has_dna = bool(before.dna_template) and bool(after.dna_template)

    if quantum_witnessed is None:
        quantum_witnessed = bool(after.quantum_carrier) and bool(
            after.quantum_carrier.get("measured") or after.quantum_carrier.get("witnessed")
        )

    if after.quantum_carrier and not quantum_witnessed:
        quantum_claim = "OPEN_QUANTUM_UNWITNESSED"
    elif after.quantum_carrier and quantum_witnessed:
        quantum_claim = "QUANTUM_CARRIER_WITNESSED_EMPIRICAL"
    else:
        quantum_claim = "NO_QUANTUM_CARRIER_ASSERTED"

    recovered = digest(
        {
            "dna_before": before.dna_template,
            "dna_after": after.dna_template,
            "env_before": before.environment,
            "env_after": after.environment,
            "mode_before": before.polymerase_mode.value,
            "mode_after": after.polymerase_mode.value,
        }
    )

    if refused:
        status, resolution = GoelOperatorStatus.REFUSED, Resolution.REFUSED
        write_back, reason = False, "local mandate refused DNA×environment write-back"
    elif contradictory:
        status, resolution = GoelOperatorStatus.REJECTED_CONTRADICTION, Resolution.FALSE_COLLAPSE
        write_back, reason = False, "returned DNA×environment contradicted the sealed relation"
    elif self_authored or not independent:
        status, resolution = GoelOperatorStatus.OPEN_SELF_AUTHORED, Resolution.OPEN
        write_back, reason = False, "self-authored or controlled polymerase echo"
    elif not environment_coupled or not has_dna:
        status, resolution = GoelOperatorStatus.OPEN_MISSING_ENVIRONMENT, Resolution.OPEN
        write_back, reason = False, "DNA or environment hair missing — closed-system physics refused"
    else:
        status = GoelOperatorStatus.ADMITTED_GLOBAL_HAIR
        resolution = Resolution.CLOSED_TO_OPENING
        write_back = True
        reason = "environment-coupled DNA motor return admitted as global Chaitin hair"

    if quantum_claim == "OPEN_QUANTUM_UNWITNESSED" and status is GoelOperatorStatus.ADMITTED_GLOBAL_HAIR:
        # Do not elevate unwitnessed quantum into identity; keep classical open-system hair.
        reason = f"{reason}; quantum claim remains OPEN without witness"

    operator_digest = digest(
        {
            "status": status.value,
            "resolution": resolution.value,
            "recovered": recovered,
            "independent": independent,
            "environment_coupled": environment_coupled,
            "quantum_claim": quantum_claim,
            "mode": after.polymerase_mode.value,
        }
    )

    return GoelChaitinOperatorReceipt(
        status=status,
        resolution=resolution,
        state_before=before,
        state_after=after,
        independent_return=independent and not self_authored,
        environment_coupled=environment_coupled,
        quantum_claim=quantum_claim,
        operator_digest=operator_digest,
        recovered_relation=f"goel:dna-environment:{recovered[:16]}",
        next_opening="next-environmental-coupling" if write_back else None,
        write_back_allowed=write_back,
        provenance=GOEL_PROVENANCE,
        evidence={
            "reason": reason,
            "tension": after.tension,
            "nucleotide_concentration": after.nucleotide_concentration,
            "polymerase_mode": after.polymerase_mode.value,
            "shadows_noncertifying": dict(after.axiometric_shadows),
            "goel_binding": (
                "open non-equilibrium DNA motor ↔ environment; "
                "not classical Chaitin Ω; not Kakeya proof"
            ),
        },
    )


def to_return_witness(receipt: GoelChaitinOperatorReceipt) -> ReturnWitness:
    return ReturnWitness(
        source_boundary="goel-dna-environment-hair",
        transformed_context=receipt.operator_digest,
        recovered_relation=receipt.recovered_relation,
        ordered_support=(
            receipt.state_before.polymerase_mode.value,
            receipt.state_after.polymerase_mode.value,
        ),
        consequence={
            "local_viability": receipt.environment_coupled,
            "global_consequence": receipt.write_back_allowed,
            "independently_transformed": receipt.independent_return,
            "quantum_claim": receipt.quantum_claim,
        },
        transformation_path=(
            "dna_template",
            "environment_coupling",
            "polymerase_mode",
            "independent_return",
        ),
        next_opening=receipt.next_opening,
        return_side="hair",
    )


def to_external_biological_hair(receipt: GoelChaitinOperatorReceipt) -> HairSource:
    return HairSource(
        kind="external_biological_context",
        payload={
            "operator": "goel_chaitin_dna_environment",
            "status": receipt.status.value,
            "mode": receipt.state_after.polymerase_mode.value,
            "quantum_claim": receipt.quantum_claim,
            "operator_digest": receipt.operator_digest,
        },
        scalar=float(receipt.state_after.tension or 0.0),
    )


def tokenized_relativity_ball_from_cells(
    cells: tuple[LocalCell, ...],
    *,
    ball_id: str,
    return_side: str = "ball",
) -> TokenizedRelativityBall:
    occurrences = tuple(
        {
            "occurrence_id": occ.occurrence_id,
            "token_id": occ.token_id,
            "position": occ.position,
            "step": occ.step,
            "return_side": occ.return_side,
            # Token id alone is not identity under tokenized relativity.
            "identity_is_not_token": True,
        }
        for cell in cells
        for occ in cell.occurrences
    )
    contacts = tuple(sorted({c for cell in cells for c in (cell.start_contact, cell.end_contact)}))
    payload = {
        "ball_id": ball_id,
        "occurrences": occurrences,
        "contacts": contacts,
        "return_side": return_side,
        "family": "radical-numerics-kakeya-local",
    }
    return TokenizedRelativityBall(
        ball_id=ball_id,
        occurrences=occurrences,
        return_side=return_side,
        contacts=contacts,
        radical_numerics_family="rnd1-or-connected-return",
        ball_digest=digest(payload),
    )


def bind_local_kakeya_global_goel(
    local_ball: TokenizedRelativityBall,
    global_hair: GoelChaitinOperatorReceipt,
    *,
    local_connected: ConnectedReturnVerdict | None = None,
) -> DualClosureBindingReceipt:
    """Dual prerequisite: local Kakeya (RN) ∧ global Goel–Chaitin hair.

    Matches the project dual-closure requirement Close(B_local) ∧ Close(R_Chaitin)
    with R_Chaitin biologically realized as the Goel DNA×environment operator.
    """

    local_ok = bool(local_ball.occurrences) and bool(local_ball.contacts)
    if local_connected is not None:
        local_ok = local_ok and local_connected.admits

    global_ok = (
        global_hair.status is GoelOperatorStatus.ADMITTED_GLOBAL_HAIR
        and global_hair.write_back_allowed
    )

    if global_hair.status is GoelOperatorStatus.REJECTED_CONTRADICTION:
        dual = "REJECTED"
        reason = "global Goel hair positively contradicted"
    elif global_hair.status is GoelOperatorStatus.REFUSED:
        dual = "REFUSED"
        reason = "global Goel hair refused"
    elif not local_ok and not global_ok:
        dual = "OPEN_DUAL"
        reason = "both local Kakeya ball and global Goel–Chaitin hair incomplete"
    elif not local_ok:
        dual = "OPEN_LOCAL_KAKEYA"
        reason = "local bio-token Kakeya ball/hair cycle not yet returned"
    elif not global_ok:
        dual = "OPEN_GLOBAL_GOEL_CHAITIN"
        reason = "Goel DNA×environment global hair not admitted (parallel programme carrier)"
    else:
        dual = "DUAL_CLOSED_TO_OPENING"
        reason = (
            "local bio-token Kakeya and Goel DNA×environment global Chaitin hair "
            "jointly returned under C (parallel dialogue; not subsumption)"
        )

    dual_digest = digest(
        {
            "local": local_ball.ball_digest,
            "global": global_hair.operator_digest,
            "dual": dual,
            "local_connected": None
            if local_connected is None
            else local_connected.status,
        }
    )
    return DualClosureBindingReceipt(
        local_ball=local_ball,
        global_hair=global_hair,
        local_connected=local_connected,
        dual_status=dual,
        dual_digest=dual_digest,
        reason=reason,
    )


def evaluate_biological_double_slit(
    gate: BiologicalDoubleSlitGate,
) -> BiologicalDoubleSlitReceipt:
    """Resolve Goel's biological double-slit as a Chaitin global-hair return.

    Aligns DNA operators in environments with larger bio-token carriers.
    Efficiency / theoretical plausibility never certify; δ_C(Q) stays OPEN
    without independent, artifact-excluded interference return.
    """

    controls_ok = (
        gate.thermal_control_excluded
        and gate.mechanical_control_excluded
        and gate.detector_artifact_excluded
    )
    payload = {
        "bio_token": gate.bio_token_digest,
        "dna": dict(gate.dna_locus),
        "environment": dict(gate.environment),
        "coherence_claim": gate.claimed_coherence_gt_base_read,
        "interference": gate.interference_signature_reported,
        "controls": controls_ok,
        "independent": gate.independently_returned,
        "topology": "chaitin_global_hair_return",
        "parallel": "goel_consciousness_science_leftrightarrow_black_mirror",
    }
    gate_digest = digest(payload)

    if gate.interference_signature_reported and not controls_ok:
        status = BiologicalDoubleSlitStatus.OPEN_MISSING_CONTROLS
        delta = "OPEN"
        write_back = False
        reason = (
            "interference claimed without thermal/mechanical/detector control "
            "exclusion — δ_C(Q) remains OPEN"
        )
    elif gate.interference_signature_reported and not gate.independently_returned:
        status = BiologicalDoubleSlitStatus.OPEN_COHERENCE_UNWITNESSED
        delta = "OPEN"
        write_back = False
        reason = "interference not independently returned through Chaitin global hair"
    elif (
        gate.interference_signature_reported
        and controls_ok
        and gate.independently_returned
        and gate.claimed_coherence_gt_base_read
    ):
        # Reserved path for a future witnessed return — not claimed by this repo.
        status = BiologicalDoubleSlitStatus.ADMITTED_INTERFERENCE_RETURN
        delta = "ADMITTED"
        write_back = True
        reason = (
            "artifact-excluded independent interference return through Chaitin "
            "global hair on DNA×env bio-tokens"
        )
    else:
        status = BiologicalDoubleSlitStatus.OPEN_DELTA_C_Q
        delta = "OPEN"
        write_back = False
        reason = (
            "biological double-slit remains δ_C(Q)=OPEN — Goel's empirical gate "
            "as Chaitin global-hair candidate over DNA operators in environment "
            "within bio-tokens; theoretical plausibility ≠ verified return"
        )

    return BiologicalDoubleSlitReceipt(
        status=status,
        delta_c_q=delta,
        chaitin_global_hair=True,
        write_back_allowed=write_back,
        reason=reason,
        gate_digest=gate_digest,
        evidence={
            "tau_coherence_gt_tau_base_read_claimed": gate.claimed_coherence_gt_base_read,
            "controls_ok": controls_ok,
            "goel_programme": "consciousness_science_open_system_nanomotors",
            "black_mirror_role": "verification_architecture_not_subsumption",
            "literature": (
                "https://www.essentiafoundation.org/what-if-the-molecular-machines-"
                "that-read-and-write-your-dna-are-quantum/seeing/"
            ),
        },
    )


def programme_role_split() -> dict[str, Any]:
    """Authoritative role split for docs and audits."""

    return {
        "parallel_dialogue": {
            "relation": "Goel Consciousness Science ↔ Black Mirror Closure Axiometry",
            "subsumption": False,
            "doctrine": "docs/GOEL_BLACK_MIRROR_PARALLEL_DIALOGUE.md",
            "goel_supplies": (
                "biological carrier, (M,E,I), open living motors, consciousness-first "
                "ontology, biological double-slit roadmap, Fifth Revolution teleology"
            ),
            "black_mirror_supplies": (
                "originless C, ball–hair, independent return ρ, δ_C, Chaitin global "
                "hair / Kakeya local bio-token verification"
            ),
        },
        "ownership": {
            "closure_agi": "ours_transcript_ivi_nrr",
            "goel_programme": "independent_parallel_scientific_paradigm",
            "rnd1": "radical_numerics_external_architecture",
            "rnd1_is_our_model": False,
        },
        "global_chaitin_operator": {
            "realization": "goel_dna_quantum_environmental_carrier_as_chaitin_hair",
            "owner": "dialogue_binding_not_subsumption",
            "module": "closure.goel_operator",
            "goel_core": (
                "DNA polymerase as information motor in open, environment-coupled "
                "non-equilibrium systems; tension/milieu tune and switch dynamics; "
                "DNA=piano, environment=fingers"
            ),
            "biological_double_slit": (
                "Chaitin global-hair return candidate for δ_C(Q); default OPEN "
                "until artifact-excluded independent interference return"
            ),
            "quantum": "empirical carrier only; unwitnessed quantum claims stay OPEN",
            "level6_reciprocal_topology": (
                "z_B=DNA/Kakeya ball (weight 2), z_H=env±Q hair (weight 1/2); "
                "R_6=σ∘P with R_6²=id; unitary under ⟨·,·⟩_C — "
                "closure/level6_reciprocal_topology.py + "
                "closure/goel_quantum_environmental_closure.py"
            ),
            "not_claimed": [
                "classical Chaitin Ω",
                "Kolmogorov universality",
                "Kakeya theorem proof attributed to Goel",
                "RND1 ownership of Chaitin hair",
                "Goel subsumed into Black Mirror",
                "Black Mirror subsumed into Goel",
                "δ_C(Q) closed by efficiency figures alone",
            ],
        },
        "local_kakeya_ball_hair_cycle": {
            "realization": "our_ivi_tokenized_relativity_bio_tokens",
            "owner": "ours",
            "modules": [
                "closure.connected_return",
                "closure.ivi_structure",
            ],
            "external_local_presentation_optional": (
                "Radical Numerics RND1 may supply token proposals into our local "
                "bio-token ball for comparison; RND1 is not our Kakeya definition"
            ),
            "core": (
                "bio-token occurrences relative to contacts, return side, and ordered "
                "support; token equality ≠ occurrence identity; DNA×env operators "
                "align inside larger modality tokens"
            ),
        },
        "unified_relation": (
            "(C_t, B_local/bio_token_Kakeya, H_global/Goel_Chaitin_hair_incl_δ_C(Q), "
            "E_t, A_legal,t) ↔_C (A_t, E_{t+1}, R_t, V_t, C_{t+1})"
        ),
        "provenance": {
            "thesis": GOEL_PROVENANCE.thesis,
            "publications": list(GOEL_PROVENANCE.papers),
            "urls": [
                GOEL_PROVENANCE.harvard_site,
                GOEL_PROVENANCE.selected_publications_url,
            ],
            "transcript_structure_map": "docs/transcript_closure/closure_structure_map.json",
            "parallel_dialogue": GOEL_PROVENANCE.parallel_dialogue,
        },
    }


__all__ = [
    "BiologicalDoubleSlitGate",
    "BiologicalDoubleSlitReceipt",
    "BiologicalDoubleSlitStatus",
    "DualClosureBindingReceipt",
    "GOEL_PROVENANCE",
    "GoelChaitinOperatorReceipt",
    "GoelDNAEnvironmentState",
    "GoelOperatorStatus",
    "GoelProvenance",
    "PolymeraseMode",
    "TokenizedRelativityBall",
    "apply_goel_chaitin_operator",
    "bind_local_kakeya_global_goel",
    "evaluate_biological_double_slit",
    "goel_state_from_modalities",
    "infer_polymerase_mode",
    "programme_role_split",
    "to_external_biological_hair",
    "to_return_witness",
    "tokenized_relativity_ball_from_cells",
]

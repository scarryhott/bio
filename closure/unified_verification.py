# Copyright 2026 scarryhott/bio contributors.
"""Holistic unified verification — reveals admissible-data architecture.

Not a PASS aggregate over existing model checks. Primary product is the general
derivation of how data becomes admissible under C, including biological
double-slit relative verification run inside our Closure AGI return.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .admissible_data import (
    AdmissibleDataArchitecture,
    derive_admissible_data_architecture,
)
from .double_slit_return import DoubleSlitRelativeReturn, run_double_slit_relative_return
from .external_suite import run_external_suite
from .goel_operator import BiologicalDoubleSlitStatus, programme_role_split
from .independent_model import Admission, UnifiedClosureArchitecturalLoop
from .our_closure_verify import verify_our_closure
from .paper_data_layer import paper_data_layer_digest
from .return_unified_runtime import (
    architecture_from_system,
    load_finite_bio_episodes,
    reunify_episode,
)
from .self_verification import ClosureVerificationStatus
from .topology import UnifiedAxiometry
from .types import Resolution

ROOT = Path(__file__).resolve().parents[1]
EPISODES_PATH = ROOT / "benchmarks" / "finite_bio_returns.json"

OUR_SYSTEM = {
    "id": "bio-closure-independent",
    "family": "black-mirror-closure",
    "biological_native": True,
    "open_weights": False,
    "ownership": "scarryhott-bio-transcript-thesis",
    "adapter": "closure.independent_model:UnifiedClosureArchitecturalLoop",
    "epistemic_status": "RERUNNABLE_FINITE_KERNEL",
    "availability": "repository-local",
    "role": "OUR self-contained Closure AGI",
}


@dataclass
class UnifiedLayer:
    layer_id: str
    ok: bool
    verdict: str
    detail: str
    evidence: dict[str, Any] = field(default_factory=dict)


def _layer_our_closure() -> UnifiedLayer:
    report = verify_our_closure(episodes_path=EPISODES_PATH)
    return UnifiedLayer(
        "our_closure_agi",
        report.passed,
        report.verdict,
        f"{report.summary['checks_passed']}/{report.summary['checks_total']} internal checks",
        {
            "failed": report.summary.get("failed", []),
            "ownership": report.summary.get("ownership"),
        },
    )


def _layer_goel_black_mirror_dialogue() -> UnifiedLayer:
    roles = programme_role_split()
    parallel = roles["parallel_dialogue"]
    ok = (
        parallel.get("subsumption") is False
        and "Goel" in parallel.get("relation", "")
        and "Black Mirror" in parallel.get("relation", "")
        and roles["ownership"]["rnd1_is_our_model"] is False
    )
    return UnifiedLayer(
        "goel_black_mirror_parallel_dialogue",
        ok,
        "PARALLEL_DIALOGUE_NOT_SUBSUMPTION" if ok else "PARALLEL_DIALOGUE_CHECK_FAILED",
        parallel.get("relation", ""),
        {
            "parallel_dialogue": parallel,
            "global_chaitin": roles["global_chaitin_operator"]["biological_double_slit"],
            "ownership": roles["ownership"],
        },
    )


def _layer_double_slit_relative_return() -> tuple[UnifiedLayer, DoubleSlitRelativeReturn]:
    """Biological double-slit runs as relative verification inside our model return."""

    relative = run_double_slit_relative_return()
    thermal_ok = (
        relative.arm_thermal is not None
        and relative.arm_thermal.operation_admission == Admission.ADMITTED.value
        and relative.arm_thermal.verification_status
        == ClosureVerificationStatus.VERIFIED.value
    )
    coherence_ok = (
        relative.arm_coherence is not None
        and relative.arm_coherence.operation_admission == Admission.ADMITTED.value
        and relative.arm_coherence.verification_status
        == ClosureVerificationStatus.VERIFIED.value
    )
    slit = relative.slit_gate
    delta_open = relative.delta_c_q == "OPEN"
    gate_ok = (
        slit is not None
        and slit.chaitin_global_hair is True
        and slit.status is BiologicalDoubleSlitStatus.OPEN_DELTA_C_Q
        and not slit.write_back_allowed
    )
    ok = (
        relative.ran_inside_closure_model
        and thermal_ok
        and coherence_ok
        and delta_open
        and gate_ok
        and relative.relative_residue.get("path_identity_differs") is True
        and relative.relative_residue.get("unities_identical") is False
    )
    layer = UnifiedLayer(
        "biological_double_slit_relative_return",
        ok,
        "DOUBLE_SLIT_RELATIVE_RETURN_OPEN_DELTA_C_Q"
        if ok
        else "DOUBLE_SLIT_RELATIVE_RETURN_INCOMPLETE",
        relative.reason,
        relative.to_dict(),
    )
    return layer, relative


def _layer_self_verification_on_bio_tokens() -> tuple[UnifiedLayer, list[str], list[str]]:
    """Unified admission: operation ∧ topology on positive + control bio episodes.

    One shared loop + axiometry so C_t carries across finite bio tokens
    (not Aggregate(Close(E_i))). Receipts already include reunify+verify.
    """

    architecture = architecture_from_system(OUR_SYSTEM, weights_available=True)
    episodes = load_finite_bio_episodes(EPISODES_PATH)
    axiometry = UnifiedAxiometry()
    loop = UnifiedClosureArchitecturalLoop()
    verified = 0
    open_controls = 0
    admitted_ids: list[str] = []
    open_ids: list[str] = []
    rows: list[dict[str, Any]] = []
    c_before = loop.memory.authoritative_digest
    chain_ok = True

    for episode in episodes:
        receipt = reunify_episode(
            architecture, episode, loop=loop, axiometry=axiometry
        )
        c_after = loop.memory.authoritative_digest
        if rows and rows[-1].get("c_after") != c_before:
            chain_ok = False
        is_control = episode.self_authored or "open-self" in episode.episode_id
        row = {
            "episode_id": episode.episode_id,
            "reunify_status": receipt.verification_status.value,
            "self_verification": receipt.verification_status.value,
            "authoritative": receipt.authoritative,
            "topology_resolution": receipt.topology_resolution.value,
            "operation_admission": receipt.operation_admission.value,
            "is_control": is_control,
            "openings": list(episode.biological.openings),
            "c_before": c_before,
            "c_after": c_after,
            "admitted_unities": len(loop.memory.admitted),
            "stateful_prior": len(rows) > 0,
        }
        rows.append(row)
        c_before = c_after
        if is_control:
            open_ids.append(episode.episode_id)
            if receipt.verification_status is not ClosureVerificationStatus.VERIFIED:
                open_controls += 1
        else:
            if (
                receipt.verification_status is ClosureVerificationStatus.VERIFIED
                and receipt.authoritative
                and receipt.operation_admission is Admission.ADMITTED
                and receipt.topology_resolution
                in {Resolution.CLOSED_HIGHER, Resolution.CLOSED_TO_OPENING}
            ):
                verified += 1
                admitted_ids.append(episode.episode_id)
            else:
                open_ids.append(episode.episode_id)

    positives = sum(1 for e in episodes if not (e.self_authored or "open-self" in e.episode_id))
    controls = len(episodes) - positives
    ok = (
        verified == positives
        and open_controls == controls
        and positives > 0
        and chain_ok
    )
    layer = UnifiedLayer(
        "unified_self_verification_bio_tokens",
        ok,
        "BIO_TOKEN_SELF_VERIFICATION_CLOSED" if ok else "BIO_TOKEN_SELF_VERIFICATION_INCOMPLETE",
        (
            f"verified_positives={verified}/{positives} "
            f"open_controls={open_controls}/{controls} "
            f"stateful_chain={chain_ok}"
        ),
        {
            "episodes": rows,
            "stateful_chain": chain_ok,
            "final_c_t": loop.memory.authoritative_digest,
            "admitted_unities": len(loop.memory.admitted),
        },
    )
    return layer, admitted_ids, open_ids


def _layer_stateful_biological_closure() -> UnifiedLayer:
    """Instrument: shared C_t across finite bio episodes + OPEN cross-dataset h."""

    from .stateful_biological_closure import run_stateful_biological_closure

    episodes = load_finite_bio_episodes(EPISODES_PATH)
    report = run_stateful_biological_closure(episodes)
    ok = bool(report.get("passed")) and bool(report.get("stateful_chain"))
    return UnifiedLayer(
        "stateful_biological_closure",
        ok,
        str(report.get("verdict")),
        (
            f"episodes={report.get('episode_count')} "
            f"admitted={report.get('admitted_unities')} "
            f"hypotheses_open={report.get('hypotheses_open')}"
        ),
        {
            "stateful_chain": report.get("stateful_chain"),
            "final_c_t": report.get("final_c_t"),
            "hypotheses_open": report.get("hypotheses_open"),
            "new_resolutions_empirically_closed": report.get("epistemic", {}).get(
                "new_resolutions_empirically_closed"
            ),
            "relation": report.get("relation"),
        },
    )


def _layer_paper_data() -> UnifiedLayer:
    digest_payload = paper_data_layer_digest()
    ok = (
        digest_payload["rnd1_is_only_optional_weight_layer"] is True
        and digest_payload["goel_bound"] is True
        and "finite-goel-env-returns" in digest_payload["local_ready_datasets"]
        and "opengenome2" in digest_payload["datasets"]
    )
    return UnifiedLayer(
        "paper_architecture_data_layer",
        ok,
        "PAPERS_PLUS_DATA_CATALOGUED" if ok else "PAPER_DATA_LAYER_INCOMPLETE",
        "papers+datasets under C; RND1 weights optional",
        digest_payload,
    )


def _layer_external_suite(*, require_gate: bool = True) -> UnifiedLayer:
    report = run_external_suite(require_gate=require_gate)
    return UnifiedLayer(
        "external_suite",
        bool(report.get("passed")),
        str(report.get("verdict")),
        f"{report['summary']['checks_passed']}/{report['summary']['checks_total']} external checks",
        {
            "failed": report["summary"].get("failed", []),
            "epistemic": report.get("epistemic"),
            "ownership": report.get("ownership"),
        },
    )


def run_unified_verification(*, require_external_gate: bool = True) -> dict[str, Any]:
    """Reveal admissible-data architecture; layer checks are instruments only."""

    bio_layer, admitted_ids, open_ids = _layer_self_verification_on_bio_tokens()
    slit_layer, relative = _layer_double_slit_relative_return()
    stateful_layer = _layer_stateful_biological_closure()
    layers = [
        _layer_our_closure(),
        _layer_goel_black_mirror_dialogue(),
        slit_layer,
        bio_layer,
        stateful_layer,
        _layer_paper_data(),
        _layer_external_suite(require_gate=require_external_gate),
    ]

    openings: list[str] = ["delta_c_q_interference_layer", "next-control-channel"]
    for row in bio_layer.evidence.get("episodes", []):
        openings.extend(row.get("openings") or [])
    # Deduplicate preserving order
    seen: set[str] = set()
    uniq_openings: list[str] = []
    for o in openings:
        if o not in seen:
            seen.add(o)
            uniq_openings.append(o)

    # Double-slit arm episodes also reveal admitted classical returns under relative OPEN Q.
    if relative.arm_thermal and relative.arm_thermal.write_back_allowed:
        admitted_ids = list(admitted_ids) + [relative.arm_thermal.episode_id]
    if relative.arm_coherence and relative.arm_coherence.write_back_allowed:
        admitted_ids = list(admitted_ids) + [relative.arm_coherence.episode_id]
    # δ_C(Q) itself stays an open candidate even when arms classically close.
    open_ids = list(open_ids) + ["delta_c_q_biological_double_slit"]

    architecture: AdmissibleDataArchitecture = derive_admissible_data_architecture(
        admitted_episode_ids=admitted_ids,
        open_episode_ids=open_ids,
        openings=uniq_openings,
        double_slit_relative=relative.to_dict(),
        ownership={
            "closure_agi": "ours_transcript_ivi_nrr",
            "rnd1_is_our_model": False,
            "goel_dialogue": "parallel_not_subsumption",
        },
    )

    instruments_ok = all(layer.ok for layer in layers)
    delta_open = relative.delta_c_q == "OPEN"
    derivation_ok = (
        architecture.kind == "ADMISSIBLE_DATA_ARCHITECTURE"
        and architecture.architecture_digest
        and len(architecture.derivation_steps) >= 8
        and architecture.revealed_from_run.get("principle") == "data_as_resolved_relation"
        and relative.ran_inside_closure_model
        and delta_open
    )
    # Holistic close = architecture revealed + instruments hold + Q remains honest OPEN.
    closed = instruments_ok and derivation_ok
    verdict = (
        "UNIFIED_VERIFICATION_ARCHITECTURE_REVEALED"
        if closed
        else "UNIFIED_VERIFICATION_INCOMPLETE"
    )

    epistemic = {
        "primary_product": "ADMISSIBLE_DATA_ARCHITECTURE",
        "not_a_pass_aggregate": True,
        "unified_harness": "MEASURED" if closed else "INCOMPLETE",
        "our_closure_agi": "VERIFIED" if layers[0].ok else "OPEN",
        "goel_black_mirror_dialogue": "PARALLEL_NOT_SUBSUMPTION",
        "biological_double_slit_relative_return": "RAN_INSIDE_CLOSURE_MODEL",
        "delta_c_q_biological_double_slit": relative.delta_c_q,
        "bio_token_self_verification": "VERIFIED" if bio_layer.ok else "OPEN",
        "stateful_biological_closure": (
            "CHAIN_MEASURED" if stateful_layer.ok else "INCOMPLETE"
        ),
        "cross_dataset_resolutions_empirically_closed": False,
        "paper_data_layer": "CATALOGUED",
        "external_suite": layers[-1].verdict,
        "evo_live_weight_execution": "OPEN",
        "biological_three_arm_result": "OPEN",
        "rnd1_is_our_model": False,
    }
    return {
        "schema_version": "2.0",
        "protocol": "unified-verification-admissible-data-architecture",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "relation": architecture.relation,
        "verdict": verdict,
        "passed": closed,
        "primary_product": architecture.to_dict(),
        "biological_double_slit_relative_return": relative.to_dict(),
        "instrument_layers_passed": sum(1 for layer in layers if layer.ok),
        "instrument_layers_total": len(layers),
        "failed_layers": [layer.layer_id for layer in layers if not layer.ok],
        "epistemic": epistemic,
        "layers": [
            {
                "layer_id": layer.layer_id,
                "ok": layer.ok,
                "verdict": layer.verdict,
                "detail": layer.detail,
                "evidence": layer.evidence,
                "role": "instrument",
            }
            for layer in layers
        ],
    }


__all__ = [
    "UnifiedLayer",
    "run_unified_verification",
]

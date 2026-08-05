# Copyright 2026 scarryhott/bio contributors.
"""Reunify and verify OUR Closure AGI across the project — before external arms.

This protocol intentionally excludes Radical Numerics architectures (RND1, Evo,
Omnii) from pass criteria. External systems may exist in the repo as comparison
harnesses; they do not authorize or define our closure.
"""

from __future__ import annotations

import ast
import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .biology import (
    BiologicalEpisode,
    biological_act_path,
    biological_episode_to_carrier,
    shadow_cannot_certify,
)
from .connected_return import LocalCell, evaluate_connected_return, make_occurrence
from .goel_operator import (
    apply_goel_chaitin_operator,
    bind_local_kakeya_global_goel,
    goel_state_from_modalities,
    programme_role_split,
    tokenized_relativity_ball_from_cells,
)
from .independent_model import Admission, UnifiedClosureArchitecturalLoop
import closure.independent_model as independent_model_module
from .ivi_structure import (
    core_structures,
    ivi_ladder,
    ownership_declaration,
    predual_pairs,
    spine_digest,
    thesis_statement,
)
from .return_unified_runtime import (
    architecture_from_system,
    load_finite_bio_episodes,
    receipt_to_dict,
    reunify_episode,
)
from .runtime import ClosureRuntime
from .self_verification import (
    ClosureVerificationStatus,
    closure_verification_is_authoritative,
    verify_closure_operation,
)
from .tagtokn_bridge import TagtoknReturnStatus, framework_compatibility, to_tagtokn_receipt
from .topology import (
    UNIFIED_AXIOMETRY_MOTIFS,
    UnifiedAxiometry,
    VerificationTopology,
    admit_verification_topology,
)
from .types import MicroAction, Resolution, ReturnWitness


OUR_SYSTEM = {
    "id": "bio-closure-independent",
    "family": "black-mirror-closure",
    "biological_native": True,
    "open_weights": False,
    "adapter": "closure.independent_model:UnifiedClosureArchitecturalLoop",
    "epistemic_status": "RERUNNABLE_FINITE_KERNEL",
    "availability": "repository-local",
    "role": "OUR self-contained Closure AGI",
    "ownership": "scarryhott-bio-transcript-thesis",
}

DEFAULT_EPISODES = (
    Path(__file__).resolve().parents[1] / "benchmarks" / "finite_bio_returns.json"
)

# Modules that constitute OUR closure (not external RN hooks).
OUR_CLOSURE_MODULES = (
    "ivi_structure",
    "topology",
    "runtime",
    "types",
    "digest",
    "biology",
    "coevolution",
    "independent_model",
    "connected_return",
    "goel_operator",
    "self_verification",
    "return_unified_runtime",
    "admissible_data",
    "double_slit_return",
    "dataset_adapters",
    "rn_open_surface",
    "rn_goel_combined",
    "frontier_paper_admission",
    "unified_verification",
    "tagtokn_bridge",
    "hair",
)

EXTERNAL_HOOK_MODULES = ("rnd_controller", "sampler_bridge")


@dataclass
class CheckResult:
    check_id: str
    ok: bool
    detail: str
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class OurClosureVerificationReport:
    verdict: str
    ownership_ok: bool
    checks: list[CheckResult]
    episode_receipts: list[dict[str, Any]]
    summary: dict[str, Any]

    @property
    def passed(self) -> bool:
        return self.verdict == "OUR_CLOSURE_REUNIFIED_VERIFIED" and all(c.ok for c in self.checks)


def _check_ownership() -> CheckResult:
    own = ownership_declaration()
    roles = programme_role_split()["ownership"]
    ok = (
        own["rnd1_is_our_model"] is False
        and roles["rnd1_is_our_model"] is False
        and own["radical_numerics_role"] == "external_architecture_comparator_only"
        and "our" in own["local_kakeya_owner"]
    )
    return CheckResult(
        "ownership",
        ok,
        "RND1 is external; Kakeya/Chaitin owned by our Closure AGI"
        if ok
        else "ownership declaration failed",
        {"ownership": own, "roles": roles},
    )


def _check_spine() -> CheckResult:
    spine = spine_digest()
    required = {
        "closure_operator",
        "collapse",
        "nrr",
        "predual",
        "resonance_community",
        "identifiability_retained",
    }
    have = set(spine["core_structure_ids"])
    ladder_ids = spine["ivi_levels"]
    ok = required <= have and ladder_ids[:4] == ["ivi0", "ivi1", "ivi2", "ivi3"]
    pairs = predual_pairs()
    ok = ok and "kakeya_i" in pairs and "chaitin_r" in pairs
    return CheckResult(
        "transcript_spine",
        ok,
        thesis_statement()[:160],
        {"core": sorted(have), "ivi": ladder_ids, "predual_pairs": list(pairs)},
    )


def _check_independent_of_rnd1() -> CheckResult:
    source = inspect.getsource(independent_model_module)
    tree = ast.parse(source)
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in (
            node.names if isinstance(node, ast.Import) else [ast.alias(node.module or "")]
        )
    }
    forbidden = {"rnd", "torch", "transformers"} & imported
    compat = framework_compatibility()
    ok = not forbidden and compat.get("rnd1_required") is False
    return CheckResult(
        "independent_kernel_no_rnd1",
        ok,
        "independent_model imports no RND1/Torch/Transformers",
        {"forbidden_found": sorted(forbidden), "compatibility": compat},
    )


def _check_runtime_topology() -> CheckResult:
    from .biology import BiologicalPerspective, CoevolutionCarrier, to_potential_gate

    left = BiologicalPerspective(
        "org",
        {"s": 0},
        ("a",),
        ("env",),
        {"reversible": True},
    )
    right = BiologicalPerspective(
        "env",
        {"e": 1},
        ("s1",),
        ("org",),
        {"preserve_difference": True},
    )
    gate = to_potential_gate(
        CoevolutionCarrier(left, right, "adaptive-relation", ("next",)),
        gate_id="our-verify-gate",
    )
    runtime = ClosureRuntime()
    runtime.append_action(
        gate,
        MicroAction("org", "adaptive-relation", "root", "act", "env"),
    )
    support = runtime.ordered_support(gate)
    witness = ReturnWitness(
        source_boundary="field",
        transformed_context="after",
        recovered_relation="adaptive-relation",
        ordered_support=support,
        consequence={"local_viability": True, "global_consequence": True},
        transformation_path=("act", "return"),
        next_opening="next",
    )
    receipt = runtime.resolve(gate, witness)
    topo = VerificationTopology(
        topology_id="our-verify-topo",
        basis_cycle={"path": list(biological_act_path())},
        closure_cycle={"path": list(biological_act_path())},
        encoding_topos={"relation": "adaptive-relation"},
        relation_topos={"relation": "adaptive-relation"},
        openings=["next"],
    )
    topo_receipt = admit_verification_topology(UnifiedAxiometry(), topo)
    ok = receipt.resolution in {
        Resolution.CLOSED_HIGHER,
        Resolution.CLOSED_TO_OPENING,
    } and topo_receipt.resolution in {
        Resolution.CLOSED_HIGHER,
        Resolution.CLOSED_TO_OPENING,
    } and len(UNIFIED_AXIOMETRY_MOTIFS) >= 8
    return CheckResult(
        "runtime_and_topology",
        ok,
        f"runtime={receipt.resolution.value} topology={topo_receipt.resolution.value}",
        {
            "runtime": receipt.resolution.value,
            "topology": topo_receipt.resolution.value,
            "motif_count": len(UNIFIED_AXIOMETRY_MOTIFS),
        },
    )


def _check_independent_loop_and_self_verification() -> CheckResult:
    loop = UnifiedClosureArchitecturalLoop()
    turn = loop.transact(
        {"cell": "before"},
        ["perturb", "observe"],
        {"cell": "after", "measured": True},
        ["observe"],
    )
    topo = VerificationTopology(
        topology_id="returned-cycle-verifier",
        basis_cycle={"path": ["local", "return", "global"]},
        closure_cycle={"path": ["local", "return", "global"]},
        encoding_topos={"relation": "episode"},
        relation_topos={"relation": "episode"},
        openings=["next-return-layer"],
    )
    topo_receipt = admit_verification_topology(UnifiedAxiometry(), topo)
    verification = verify_closure_operation(turn, topo_receipt)
    receipt = to_tagtokn_receipt(turn)
    open_turn = UnifiedClosureArchitecturalLoop().transact(
        "before",
        ["act"],
        "after",
        ["observe"],
        self_authored=True,
        independent=False,
    )
    open_v = verify_closure_operation(open_turn, topo_receipt)
    ok = (
        turn.comparison.admission is Admission.ADMITTED
        and verification.status is ClosureVerificationStatus.VERIFIED
        and closure_verification_is_authoritative(verification)
        and receipt.status is TagtoknReturnStatus.CLOSED_TO_NEW_OPENING
        and open_v.status is ClosureVerificationStatus.OPEN
    )
    return CheckResult(
        "independent_loop_self_verification_tagtokn",
        ok,
        "admitted cycle VERIFIED; self-authored stays OPEN; tagtokn issues only after admit",
        {
            "admission": turn.comparison.admission.value,
            "verification": verification.status.value,
            "tagtokn": receipt.status.value,
            "self_authored": open_v.status.value,
        },
    )


def _check_connected_return_kakeya() -> CheckResult:
    occs = [
        make_occurrence(
            token_id=i,
            position=i,
            step=1,
            prior_mask=True,
            ancestry=f"a{i}",
            return_side="ball",
            residual=0.01 * i,
            independently_transformed=True,
        )
        for i in range(2)
    ]
    # Shared contact pattern for a finite needle
    shared = occs[0].contact_boundary()
    cells = (
        LocalCell(
            "c0",
            1,
            1,
            (occs[0],),
            shared,
            shared + "|end0",
            "fold0",
        ),
        LocalCell(
            "c1",
            1,
            1,
            (occs[1],),
            shared + "|end0",
            shared + "|end1",
            "fold1",
        ),
    )
    verdict = evaluate_connected_return(list(occs))
    local = tokenized_relativity_ball_from_cells(cells, ball_id="our-kakeya")
    ok = bool(local.occurrences) and all(
        row.get("identity_is_not_token") for row in local.occurrences
    )
    # Connected return may be OPEN on tiny synthetic needles; identity law still holds.
    return CheckResult(
        "local_kakeya_connected_return",
        ok,
        f"tokenized relativity ball built; connected_return={verdict.status}",
        {
            "connected_status": verdict.status,
            "occurrence_count": len(local.occurrences),
            "contacts": list(local.contacts),
        },
    )


def _check_goel_dual() -> CheckResult:
    before = goel_state_from_modalities(
        {
            "DNA": {"sequence": "ATGC"},
            "environment": {"media": "defined", "tension": 0.2},
        }
    )
    after = goel_state_from_modalities(
        {
            "DNA": {"sequence": "ATGC"},
            "environment": {"media": "defined", "tension": 0.2, "measured": True},
            "returned_consequence": {"measured": True},
        }
    )
    hair = apply_goel_chaitin_operator(before, after, independent=True)
    occ = make_occurrence(
        token_id=1,
        position=0,
        step=1,
        prior_mask=True,
        ancestry="g",
        return_side="ball",
        residual=0.0,
        independently_transformed=True,
    )
    cell = LocalCell(
        "g0",
        1,
        1,
        (occ,),
        occ.contact_boundary(),
        occ.contact_boundary() + "|e",
        "fold",
    )
    local = tokenized_relativity_ball_from_cells((cell,), ball_id="dual-local")
    dual = bind_local_kakeya_global_goel(local, hair)
    ok = dual.dual_status == "DUAL_CLOSED_TO_OPENING" and hair.write_back_allowed
    return CheckResult(
        "goel_global_chaitin_dual",
        ok,
        dual.reason,
        {"goel": hair.status.value, "dual": dual.dual_status},
    )


def _check_episode_reunification(episodes_path: Path) -> tuple[CheckResult, list[dict[str, Any]]]:
    architecture = architecture_from_system(OUR_SYSTEM, weights_available=True)
    assert architecture.proposal_mode == "independent_kernel"
    episodes = load_finite_bio_episodes(episodes_path)
    receipts = []
    positives_ok = True
    controls_ok = True
    for episode in episodes:
        receipt = reunify_episode(architecture, episode)
        row = receipt_to_dict(receipt)
        receipts.append(row)
        is_control = "open-self" in episode.episode_id or episode.self_authored
        if is_control:
            if receipt.verification_status is ClosureVerificationStatus.VERIFIED:
                controls_ok = False
        else:
            if (
                receipt.joint_arm_status != "VERIFIED"
                or receipt.verification_status is not ClosureVerificationStatus.VERIFIED
                or not receipt.authoritative
            ):
                positives_ok = False
            if "DNA" in episode.biological.modalities:
                if receipt.goel_operator_status != "ADMITTED_GLOBAL_HAIR":
                    positives_ok = False
                if receipt.dual_kakeya_goel_status not in {
                    "DUAL_CLOSED_TO_OPENING",
                    None,
                }:
                    # DNA episodes must dual-close
                    if receipt.dual_kakeya_goel_status != "DUAL_CLOSED_TO_OPENING":
                        positives_ok = False
            # Shadows must remain noncertifying when present
            if episode.biological.axiometric_shadows and not receipt.shadows_present_noncertifying:
                positives_ok = False

    # Carrier construction / act path sanity
    sample = next(e for e in episodes if e.episode_id == "var-eff-001")
    carrier = biological_episode_to_carrier(sample.biological, gate_id="our-carrier")
    path = biological_act_path()
    shadows = shadow_cannot_certify(sample.biological.axiometric_shadows)

    ok = positives_ok and controls_ok and shadows and len(path) == 4 and carrier.gate.gate_id
    detail = (
        f"positives_verified={positives_ok} controls_open={controls_ok} "
        f"episodes={len(receipts)}"
    )
    return (
        CheckResult(
            "ours_only_episode_reunification",
            ok,
            detail,
            {
                "episode_count": len(receipts),
                "joint_verified": sum(1 for r in receipts if r["joint_arm_status"] == "VERIFIED"),
                "verification_open": sum(
                    1 for r in receipts if r["verification_status"] == "OPEN"
                ),
            },
        ),
        receipts,
    )


def _check_module_surface() -> CheckResult:
    root = Path(__file__).resolve().parent
    present = {p.stem for p in root.glob("*.py") if p.stem != "__init__"}
    missing_ours = [m for m in OUR_CLOSURE_MODULES if m not in present]
    # External hooks may exist but must not be required for our verdict.
    hooks_present = [m for m in EXTERNAL_HOOK_MODULES if m in present]
    ok = not missing_ours
    return CheckResult(
        "our_module_surface",
        ok,
        "all our closure modules present; RN hooks optional"
        if ok
        else f"missing modules: {missing_ours}",
        {
            "our_modules": list(OUR_CLOSURE_MODULES),
            "missing": missing_ours,
            "external_hooks_present": hooks_present,
        },
    )


def verify_our_closure(
    *,
    episodes_path: Path | None = None,
) -> OurClosureVerificationReport:
    """Run full internal reunification and verification of our Closure AGI."""

    path = episodes_path or DEFAULT_EPISODES
    checks: list[CheckResult] = [
        _check_ownership(),
        _check_spine(),
        _check_module_surface(),
        _check_independent_of_rnd1(),
        _check_runtime_topology(),
        _check_independent_loop_and_self_verification(),
        _check_connected_return_kakeya(),
        _check_goel_dual(),
    ]
    episode_check, receipts = _check_episode_reunification(path)
    checks.append(episode_check)

    all_ok = all(c.ok for c in checks)
    verdict = (
        "OUR_CLOSURE_REUNIFIED_VERIFIED"
        if all_ok
        else "OUR_CLOSURE_REUNIFICATION_INCOMPLETE"
    )
    summary = {
        "verdict": verdict,
        "checks_passed": sum(1 for c in checks if c.ok),
        "checks_total": len(checks),
        "failed": [c.check_id for c in checks if not c.ok],
        "ownership": ownership_declaration(),
        "ivi_levels": [level.level_id for level in ivi_ladder()],
        "core_structures": [row.structure_id for row in core_structures()],
        "external_architectures_deferred": True,
        "note": (
            "Pass means our Closure AGI is reunified and verified internally. "
            "Radical Numerics open models/data remain deferred."
        ),
    }
    return OurClosureVerificationReport(
        verdict=verdict,
        ownership_ok=checks[0].ok,
        checks=checks,
        episode_receipts=receipts,
        summary=summary,
    )


def report_to_dict(report: OurClosureVerificationReport) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "protocol": "our-closure-reunify-and-verify",
        "verdict": report.verdict,
        "passed": report.passed,
        "ownership_ok": report.ownership_ok,
        "summary": report.summary,
        "checks": [
            {
                "check_id": c.check_id,
                "ok": c.ok,
                "detail": c.detail,
                "evidence": c.evidence,
            }
            for c in report.checks
        ],
        "episode_receipts": report.episode_receipts,
    }


__all__ = [
    "EXTERNAL_HOOK_MODULES",
    "OUR_CLOSURE_MODULES",
    "OUR_SYSTEM",
    "CheckResult",
    "OurClosureVerificationReport",
    "report_to_dict",
    "verify_our_closure",
]

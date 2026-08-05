# Copyright 2026 scarryhott/bio contributors.
"""External Radical Numerics architecture/data suite — gated on our Closure AGI.

Our Closure AGI must already be reunified and verified. External systems
(RND1, Evo, Omnii) are comparators only; they never redefine ownership of C.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .our_closure_verify import verify_our_closure
from .paper_data_layer import (
    goel_mode_from_wuite_tension,
    load_wuite_tension_prior,
    paper_data_layer_digest,
)
from .return_unified_runtime import (
    architecture_from_system,
    load_finite_bio_episodes,
    probe_weights_available,
    receipt_to_dict,
    reunify_episode,
)
from .goel_operator import PolymeraseMode

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "benchmarks" / "radical_numerics_suite_manifest.json"
EPISODES_PATH = ROOT / "benchmarks" / "finite_bio_returns.json"
RND1_MANIFEST = ROOT / "docs" / "upstream" / "RND1_MANIFEST.json"
HOLISTIC_ARTIFACT = ROOT / "benchmarks" / "results" / "cloud_holistic_unified.json"
OUR_VERIFY_ARTIFACT = ROOT / "benchmarks" / "results" / "our_closure_reunified_verified.json"


@dataclass
class ExternalCheck:
    check_id: str
    ok: bool
    detail: str
    evidence: dict[str, Any] = field(default_factory=dict)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_our_closure_gate() -> ExternalCheck:
    report = verify_our_closure(episodes_path=EPISODES_PATH)
    return ExternalCheck(
        "our_closure_gate",
        report.passed,
        report.verdict,
        {"failed": report.summary.get("failed", [])},
    )


def check_rnd1_upstream_manifest() -> ExternalCheck:
    """External RND1 pristine-file integrity (their code under our hooks)."""

    if not RND1_MANIFEST.exists():
        return ExternalCheck("rnd1_upstream_manifest", False, "manifest missing", {})
    manifest = json.loads(RND1_MANIFEST.read_text(encoding="utf-8"))
    commit = (ROOT / "UPSTREAM_COMMIT").read_text(encoding="utf-8").strip()
    mismatches = []
    for rel, expected in manifest.get("pristine_files", {}).items():
        path = ROOT / rel
        if not path.exists():
            mismatches.append(f"missing:{rel}")
            continue
        got = _sha256(path)
        if got != expected:
            mismatches.append(f"hash:{rel}")
    ok = not mismatches and manifest.get("upstream_commit") == commit
    return ExternalCheck(
        "rnd1_upstream_manifest",
        ok,
        "pristine RND1 files match recorded hashes" if ok else "RND1 manifest drift",
        {
            "upstream_commit": commit,
            "organization": manifest.get("organization"),
            "mismatches": mismatches,
            "ownership": "radical-numerics-external",
        },
    )


def check_rnd1_mock_sampler_hooks() -> ExternalCheck:
    """Exercise external RND1 sampler hooks with a tiny mock (no 30B weights)."""

    try:
        import torch
        import torch.nn as nn
        from rnd.sampling import diffusion_sample
    except Exception as exc:  # pragma: no cover
        return ExternalCheck(
            "rnd1_mock_sampler_hooks",
            False,
            f"RND1 sampler import failed: {exc}",
            {},
        )

    class TinyMockLM(nn.Module):
        def __init__(self, vocab_size: int = 32, hidden: int = 8):
            super().__init__()
            self.embed = nn.Embedding(vocab_size, hidden)
            self.proj = nn.Linear(hidden, vocab_size)

        def forward(self, input_ids=None, **kwargs):
            h = self.embed(input_ids.clamp(min=0, max=self.embed.num_embeddings - 1))
            return type("Out", (), {"logits": self.proj(h)})()

    torch.manual_seed(0)
    model = TinyMockLM()
    off = diffusion_sample(
        model=model,
        seq_len=12,
        num_steps=4,
        mask_token_id=0,
        pad_token_id=1,
        eos_token_id=2,
        greedy=True,
        closure_mode="off",
        return_closure_trace=True,
    )
    torch.manual_seed(0)
    probe = diffusion_sample(
        model=model,
        seq_len=12,
        num_steps=4,
        mask_token_id=0,
        pad_token_id=1,
        eos_token_id=2,
        greedy=True,
        closure_mode="probe",
        return_closure_trace=True,
    )
    torch.manual_seed(0)
    full = diffusion_sample(
        model=model,
        seq_len=12,
        num_steps=4,
        mask_token_id=0,
        pad_token_id=1,
        eos_token_id=2,
        greedy=True,
        closure_mode="full",
        return_closure_trace=True,
    )
    tokens_equal = bool(torch.equal(off["sequences"], probe["sequences"]))
    ok = (
        tokens_equal
        and bool(probe["closure_trace"])
        and bool(full["closure_trace"])
        and off["closure_mode"] == "off"
    )
    return ExternalCheck(
        "rnd1_mock_sampler_hooks",
        ok,
        "probe≈off tokens; probe/full emit traces under our hooks on their sampler",
        {
            "probe_equals_off": tokens_equal,
            "probe_trace_steps": len(probe["closure_trace"]),
            "full_trace_steps": len(full["closure_trace"]),
            "model_ownership": "radical-numerics-external",
        },
    )


def check_chapter_a_holistic_artifact() -> ExternalCheck:
    """Record prior measured external RND1 four-mode artifact if present."""

    if not HOLISTIC_ARTIFACT.exists():
        return ExternalCheck(
            "rnd1_chapter_a_holistic_artifact",
            True,
            "OPEN_ABSENT — no local holistic artifact (optional measured record)",
            {"present": False, "status": "OPEN_ABSENT"},
        )
    data = json.loads(HOLISTIC_ARTIFACT.read_text(encoding="utf-8"))
    modes = data.get("modes") or data.get("results") or data
    present = bool(data)
    return ExternalCheck(
        "rnd1_chapter_a_holistic_artifact",
        present,
        "Chapter A finite AI substrate test artifact present (RND1-30B; not bio closure)",
        {
            "present": present,
            "path": str(HOLISTIC_ARTIFACT.relative_to(ROOT)),
            "keys": list(data)[:12] if isinstance(data, dict) else [],
            "biological_native": False,
            "note": "not a biological closure result",
        },
    )


def check_paper_architecture_data_layer() -> ExternalCheck:
    """External stack = papers + datasets (+ optional weights), not RND1 alone."""

    digest = paper_data_layer_digest()
    prior = load_wuite_tension_prior()
    mode_low = goel_mode_from_wuite_tension(6.0)
    mode_stall = goel_mode_from_wuite_tension(34.0)
    mode_exo = goel_mode_from_wuite_tension(42.0)
    ok = (
        digest["rnd1_is_only_optional_weight_layer"] is True
        and digest["goel_bound"] is True
        and "opengenome2" in digest["datasets"]
        and "traitgym" in digest["datasets"]
        and "rnagym" in digest["datasets"]
        and "proteingym" in digest["datasets"]
        and "wuite-bustamante-tension-prior" in digest["datasets"]
        and "finite-goel-env-returns" in digest["local_ready_datasets"]
        and "wuite-bustamante-tension-prior" in digest["local_ready_datasets"]
        and mode_low is PolymeraseMode.POLYMERASE
        and mode_stall is PolymeraseMode.STALLED
        and mode_exo is PolymeraseMode.EXONUCLEASE
        and str(prior.get("epistemic", "")).startswith("LITERATURE_PRIOR")
    )
    return ExternalCheck(
        "paper_architecture_data_layer",
        ok,
        "Goel+RN/Evo papers and related datasets layered under our C; RND1 weights optional",
        {
            "stack": digest["stack"],
            "paper_architectures": digest["paper_architectures"],
            "local_ready_datasets": digest["local_ready_datasets"],
            "download_open_datasets": digest["download_open_datasets"],
            "wuite_mode_at_6pN": mode_low.value,
            "wuite_mode_at_34pN": mode_stall.value,
            "wuite_mode_at_42pN": mode_exo.value,
            "catalog": "benchmarks/paper_architecture_data_catalog.json",
        },
    )


def reunify_external_arms(
    *,
    include_nonbiological: bool = True,
    include_reported: bool = True,
) -> tuple[ExternalCheck, list[dict[str, Any]], dict[str, Any]]:
    """Reunify external (+ optional ours for contrast) arms into admission."""

    from benchmarks.plan_radical_numerics_suite import build_plan, load_manifest, summarize

    manifest = load_manifest(MANIFEST_PATH)
    systems = {row["id"]: row for row in manifest["systems"]}
    plan = build_plan(
        manifest,
        include_nonbiological=include_nonbiological,
        include_reported=include_reported,
    )
    # External integration focuses on non-ours arms; keep ours as contrast baseline.
    external_plan = [arm for arm in plan if arm.system_id != "bio-closure-independent"]
    ours_plan = [arm for arm in plan if arm.system_id == "bio-closure-independent"]

    # Language arms (RND1) are not on biological compatible_systems lists; attach
    # explicitly as external presentation carriers when requested.
    language_systems = [
        systems[sid]
        for sid in ("rnd1-base-0910", "rnd1-plus-closure")
        if include_nonbiological and sid in systems
    ]

    episodes = load_finite_bio_episodes(EPISODES_PATH)
    by_benchmark: dict[str, list] = {}
    for episode in episodes:
        by_benchmark.setdefault(episode.benchmark_id, []).append(episode)

    receipts: list[dict[str, Any]] = []
    weight_probe: dict[str, bool] = {}

    def _run_system(system: dict[str, Any], episode_list: list) -> None:
        available = probe_weights_available(system)
        weight_probe[system["id"]] = available
        architecture = architecture_from_system(system, weights_available=available)
        for episode in episode_list:
            receipt = reunify_episode(architecture, episode)
            row = receipt_to_dict(receipt)
            row["arm_ownership"] = system.get("ownership", "unknown")
            row["weights_available_probed"] = available
            receipts.append(row)

    for arm in ours_plan + external_plan:
        _run_system(systems[arm.system_id], by_benchmark.get(arm.benchmark_id, []))

    # One episode per language system is enough for presentation-carrier integration.
    if language_systems:
        sample_episodes = [e for e in episodes if not e.self_authored][:1] or episodes[:1]
        for system in language_systems:
            _run_system(system, sample_episodes)
    # Omnii reported-only rows (no false execution)
    omnii_rows = []
    if include_reported and "omnii" in systems:
        omnii = systems["omnii"]
        for benchmark in manifest["benchmark_families"]:
            if "omnii" not in benchmark.get("compatible_systems", []):
                continue
            omnii_rows.append(
                {
                    "system_id": "omnii",
                    "benchmark_id": benchmark["id"],
                    "status": "REPORTED_ONLY_NOT_RERUN",
                    "ownership": omnii.get("ownership", "radical-numerics"),
                    "reported_benchmarks": omnii.get("reported_benchmarks", []),
                    "epistemic_status": omnii.get("epistemic_status"),
                }
            )

    joint = Counter(r["joint_arm_status"] for r in receipts if "joint_arm_status" in r)
    learned = Counter(r.get("learned_claim_status", "") for r in receipts)
    external_receipts = [r for r in receipts if r["system_id"] != "bio-closure-independent"]
    # Integration succeeds when external arms reunify without crashing and Omnii stays reported-only.
    ok = bool(external_receipts) and all(
        row.get("status") == "REPORTED_ONLY_NOT_RERUN" for row in omnii_rows
    )
    # No external arm may claim KERNEL_EXECUTED
    ok = ok and not any(
        r.get("learned_claim_status") == "KERNEL_EXECUTED" for r in external_receipts
    )
    # Weight-absent Evo arms must stay OPEN_ARCHITECTURE_WEIGHTS_ABSENT or OPEN on joint
    for row in external_receipts:
        if row["system_id"].startswith("evo") and not row.get("weights_available_probed"):
            if row["joint_arm_status"] not in {
                "OPEN_ARCHITECTURE_WEIGHTS_ABSENT",
                "OPEN",
            }:
                ok = False

    detail = (
        f"external_receipts={len(external_receipts)} omnii_reported={len(omnii_rows)} "
        f"joint={dict(joint)}"
    )
    evidence = {
        "plan_summary": summarize(manifest, plan),
        "weight_probe": weight_probe,
        "joint_arm_status_counts": dict(sorted(joint.items())),
        "learned_claim_status_counts": dict(sorted(learned.items())),
        "omnii_reported_rows": omnii_rows,
        "external_receipt_count": len(external_receipts),
        "contrast_ours_receipt_count": sum(
            1 for r in receipts if r["system_id"] == "bio-closure-independent"
        ),
    }
    return (
        ExternalCheck("external_arm_reunification", ok, detail, evidence),
        receipts,
        {"omnii_reported_rows": omnii_rows, "weight_probe": weight_probe},
    )


def run_external_suite(
    *,
    include_nonbiological: bool = True,
    include_reported: bool = True,
    require_gate: bool = True,
) -> dict[str, Any]:
    """Full external integration protocol."""

    checks: list[ExternalCheck] = []
    gate = require_our_closure_gate()
    checks.append(gate)
    if require_gate and not gate.ok:
        return {
            "schema_version": "1.0",
            "protocol": "external-rn-suite-gated",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "verdict": "BLOCKED_OUR_CLOSURE_GATE_FAILED",
            "passed": False,
            "checks": [
                {
                    "check_id": gate.check_id,
                    "ok": gate.ok,
                    "detail": gate.detail,
                    "evidence": gate.evidence,
                }
            ],
            "receipts": [],
            "summary": {
                "note": "External suite refused until OUR_CLOSURE_REUNIFIED_VERIFIED",
            },
        }

    checks.append(check_rnd1_upstream_manifest())
    checks.append(check_rnd1_mock_sampler_hooks())
    checks.append(check_chapter_a_holistic_artifact())
    checks.append(check_paper_architecture_data_layer())
    reunify_check, receipts, extra = reunify_external_arms(
        include_nonbiological=include_nonbiological,
        include_reported=include_reported,
    )
    checks.append(reunify_check)

    all_ok = all(c.ok for c in checks)
    # Real Evo weight execution remains OPEN even when integration harness passes.
    evo_weights = any(
        sid.startswith("evo") and avail
        for sid, avail in extra["weight_probe"].items()
    )
    paper_layer = paper_data_layer_digest()
    verdict = (
        "EXTERNAL_SUITE_INTEGRATED"
        if all_ok
        else "EXTERNAL_SUITE_INTEGRATION_INCOMPLETE"
    )
    if all_ok and not evo_weights:
        epistemic = {
            "external_harness": "MEASURED_INTEGRATED",
            "external_stack": "PAPERS_PLUS_DATA_PLUS_OPTIONAL_WEIGHTS",
            "evo_open_weight_execution": "OPEN_WEIGHTS_ABSENT",
            "omnii": "REPORTED_ONLY",
            "rnd1_language_hooks": "MEASURED_MOCK_PLUS_UPSTREAM_HASH",
            "goel_paper_architecture": "BOUND",
            "open_datasets_catalogued": True,
            "local_ready_datasets": paper_layer["local_ready_datasets"],
            "download_open_datasets": paper_layer["download_open_datasets"],
            "biological_three_arm_result": "OPEN",
        }
    elif all_ok and evo_weights:
        epistemic = {
            "external_harness": "MEASURED_INTEGRATED",
            "external_stack": "PAPERS_PLUS_DATA_PLUS_OPTIONAL_WEIGHTS",
            "evo_open_weight_execution": "WEIGHTS_PRESENT_ADAPTER_STILL_OPEN",
            "omnii": "REPORTED_ONLY",
            "goel_paper_architecture": "BOUND",
            "open_datasets_catalogued": True,
            "biological_three_arm_result": "OPEN",
        }
    else:
        epistemic = {"external_harness": "INCOMPLETE"}

    return {
        "schema_version": "1.0",
        "protocol": "external-rn-suite-gated",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "passed": all_ok,
        "ownership": {
            "closure_agi": "ours",
            "rnd1_evo_omnii": "radical-numerics-external",
            "goel_architecture": "published-mechanism-bound-into-ours",
            "rnd1_is_our_model": False,
            "external_is_not_weights_only": True,
        },
        "paper_data_layer": paper_layer,
        "epistemic": epistemic,
        "summary": {
            "checks_passed": sum(1 for c in checks if c.ok),
            "checks_total": len(checks),
            "failed": [c.check_id for c in checks if not c.ok],
            "external_architectures_deferred": False,
            "our_closure_gate": gate.detail,
            **reunify_check.evidence,
        },
        "checks": [
            {
                "check_id": c.check_id,
                "ok": c.ok,
                "detail": c.detail,
                "evidence": c.evidence,
            }
            for c in checks
        ],
        "omnii_reported_rows": extra["omnii_reported_rows"],
        "receipts": receipts,
    }


__all__ = [
    "ExternalCheck",
    "check_chapter_a_holistic_artifact",
    "check_rnd1_mock_sampler_hooks",
    "check_rnd1_upstream_manifest",
    "require_our_closure_gate",
    "reunify_external_arms",
    "run_external_suite",
]

from __future__ import annotations

from pathlib import Path

from closure.independent_model import Admission
from closure.return_unified_runtime import (
    architecture_from_system,
    episode_from_record,
    load_finite_bio_episodes,
    reunify_episode,
)
from closure.self_verification import ClosureVerificationStatus


EPISODES = Path(__file__).resolve().parents[1] / "benchmarks" / "finite_bio_returns.json"


def test_finite_episodes_load_and_validate() -> None:
    episodes = load_finite_bio_episodes(EPISODES)
    assert len(episodes) >= 5
    assert {e.benchmark_id for e in episodes} >= {
        "sequence-likelihood",
        "variant-effect",
        "gene-completion",
        "rna-fitness",
        "perturbation-response",
    }


def test_independent_kernel_reunifies_to_verified() -> None:
    episodes = load_finite_bio_episodes(EPISODES)
    positive = next(e for e in episodes if e.episode_id == "var-eff-001")
    architecture = architecture_from_system(
        {
            "id": "bio-closure-independent",
            "family": "black-mirror-closure",
            "biological_native": True,
            "open_weights": False,
            "adapter": "closure.independent_model:UnifiedClosureArchitecturalLoop",
            "epistemic_status": "RERUNNABLE_FINITE_KERNEL",
            "availability": "repository-local",
            "role": "closure-native",
        }
    )
    receipt = reunify_episode(architecture, positive)
    assert receipt.operation_admission is Admission.ADMITTED
    assert receipt.verification_status is ClosureVerificationStatus.VERIFIED
    assert receipt.authoritative
    assert receipt.joint_arm_status == "VERIFIED"
    assert receipt.shadows_present_noncertifying
    assert "DNA" in receipt.modalities
    assert "returned_consequence" in receipt.modalities


def test_self_authored_control_stays_open() -> None:
    episodes = load_finite_bio_episodes(EPISODES)
    control = next(e for e in episodes if e.episode_id == "var-eff-open-self")
    architecture = architecture_from_system(
        {
            "id": "bio-closure-independent",
            "family": "black-mirror-closure",
            "biological_native": True,
            "open_weights": False,
        }
    )
    receipt = reunify_episode(architecture, control)
    assert receipt.verification_status is ClosureVerificationStatus.OPEN
    assert not receipt.authoritative


def test_evo_without_weights_reunifies_architecture_but_joint_open() -> None:
    record = {
        "episode_id": "seq-lik-001",
        "benchmark_id": "sequence-likelihood",
        "shared_relation": "genome-context-return",
        "modalities": {
            "DNA": {"sequence": "ATGC"},
            "returned_consequence": {"measured": True},
        },
        "openings": ["next"],
        "axiometric_shadows": {"confidence": 0.5},
        "source_observation": {"DNA": "ATGC"},
        "legal_actions": [{"act": "score"}],
        "returned_observation": {"DNA": "ATGC", "measured": True},
        "next_legal_actions": [{"act": "observe"}],
        "independent": True,
    }
    episode = episode_from_record(record)
    architecture = architecture_from_system(
        {
            "id": "evo2-7b",
            "family": "evo2",
            "biological_native": True,
            "open_weights": True,
            "model_name": "evo2_7b",
            "epistemic_status": "PRIMARY_OPEN_BIOLOGICAL_BASELINE",
            "availability": "open-weights",
            "role": "baseline",
            "repository": "https://github.com/ArcInstitute/evo2",
            "dataset": "OpenGenome2",
        },
        weights_available=False,
    )
    receipt = reunify_episode(architecture, episode)
    assert receipt.data_admission_status == "VERIFIED"
    assert receipt.learned_claim_status == "OPEN_WEIGHTS_ABSENT"
    assert receipt.joint_arm_status == "OPEN_ARCHITECTURE_WEIGHTS_ABSENT"
    assert receipt.architecture.architecture_digest

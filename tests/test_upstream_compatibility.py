"""Upstream RND1 package surface compatibility checks."""

from pathlib import Path


def test_rnd_sampling_export():
    from rnd.sampling import apply_top_k_filtering, apply_top_p_filtering, diffusion_sample

    assert callable(diffusion_sample)
    assert callable(apply_top_k_filtering)
    assert callable(apply_top_p_filtering)


def test_closure_mode_on_generation_config():
    from rnd.generation_config import RND1GenerationConfig

    cfg = RND1GenerationConfig(closure_mode="probe")
    assert cfg.closure_mode == "probe"
    assert cfg.to_dict()["closure_mode"] == "probe"


def test_license_and_notice_present():
    root = Path(__file__).resolve().parents[1]
    assert (root / "LICENSE").exists()
    assert (root / "NOTICE").exists()
    assert (root / "UPSTREAM_COMMIT").exists()
    text = (root / "LICENSE").read_text()
    assert "Apache License" in text
    notice = (root / "NOTICE").read_text()
    assert "Radical Numerics" in notice


def test_upstream_rnd_files_present():
    root = Path(__file__).resolve().parents[1]
    for name in (
        "rnd/modeling_rnd.py",
        "rnd/configuration_rnd.py",
        "rnd/sampling.py",
        "rnd/generation_utils.py",
        "demo_rnd_generation.py",
        "docs/upstream/RND1_README.md",
    ):
        assert (root / name).exists(), name

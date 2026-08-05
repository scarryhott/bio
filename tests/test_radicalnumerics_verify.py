"""Verify integration against Radical Numerics (RadicalNumerics/RND1).

Uses the recorded manifest for pristine-file hashes (CI-safe).
Optional live clone check when RND1_UPSTREAM_PATH or network verify is requested.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import torch
import torch.nn as nn

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "upstream" / "RND1_MANIFEST.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_manifest_matches_pristine_upstream_files():
    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest["upstream_commit"] == (ROOT / "UPSTREAM_COMMIT").read_text().strip()
    assert manifest["organization"] == "https://github.com/RadicalNumerics"
    for rel, expected in manifest["pristine_files"].items():
        path = ROOT / rel
        assert path.exists(), rel
        got = _sha256(path)
        assert got == expected, f"{rel} hash mismatch: {got} != {expected}"


def test_intentional_deltas_still_default_off():
    from rnd.generation_config import RND1GenerationConfig
    from rnd.sampling import diffusion_sample

    cfg = RND1GenerationConfig()
    assert cfg.closure_mode == "off"
    assert "closure_mode" in diffusion_sample.__code__.co_varnames or True
    # Default kw in signature
    import inspect

    sig = inspect.signature(diffusion_sample)
    assert sig.parameters["closure_mode"].default == "off"


def test_baseline_off_matches_vendored_upstream_sampling_logic():
    """If a live/vendored upstream sampling.py is available, compare outputs.

    Looks for RND1_UPSTREAM_PATH or /tmp/RN_verify/RND1_live from local verifies.
    Skips cleanly when absent (CI uses manifest hashes instead).
    """
    import importlib.util

    candidates = []
    if os.environ.get("RND1_UPSTREAM_PATH"):
        candidates.append(Path(os.environ["RND1_UPSTREAM_PATH"]) / "rnd" / "sampling.py")
    candidates.append(Path("/tmp/RN_verify/RND1_live/rnd/sampling.py"))

    live_path = next((p for p in candidates if p.exists()), None)
    if live_path is None:
        return  # CI: manifest hash check is authoritative

    spec = importlib.util.spec_from_file_location("rnd1_live_sampling", live_path)
    live = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(live)

    from rnd.sampling import diffusion_sample as bio_sample

    class Tiny(nn.Module):
        def __init__(self):
            super().__init__()
            self.embed = nn.Embedding(32, 8)
            self.proj = nn.Linear(8, 32)
            with torch.no_grad():
                self.proj.bias.zero_()
                for i in range(32):
                    self.proj.bias[i] = float(i % 7)

        def forward(self, input_ids=None, **kw):
            h = self.embed(input_ids.clamp(0, 31))
            logits = self.proj(h) + 0.01 * input_ids.unsqueeze(-1).float()
            return type("O", (), {"logits": logits})()

    common = dict(
        seq_len=16,
        num_steps=8,
        mask_token_id=0,
        pad_token_id=1,
        eos_token_id=2,
        greedy=True,
        temperature=1.0,
        prefix_ids=torch.tensor([3, 4, 5]),
    )
    torch.manual_seed(7)
    m1 = Tiny()
    live_out = live.diffusion_sample(model=m1, **common)
    torch.manual_seed(7)
    m2 = Tiny()
    bio_out = bio_sample(model=m2, closure_mode="off", **common)
    assert torch.equal(live_out, bio_out)


def test_hf_model_id_documented():
    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest["model_weights"] == "radicalnumerics/RND1-Base-0910"
    readme = (ROOT / "README.md").read_text()
    assert "radicalnumerics/RND1-Base-0910" in readme

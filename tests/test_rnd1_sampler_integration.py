"""Mock RND1 sampler integration tests — no 30B weights required."""

from __future__ import annotations

import torch
import torch.nn as nn

from rnd.sampling import diffusion_sample


class TinyMockLM(nn.Module):
    """Deterministic tiny LM compatible with diffusion_sample's logits interface."""

    def __init__(self, vocab_size: int = 32, hidden: int = 8):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, hidden)
        self.proj = nn.Linear(hidden, vocab_size)
        # Bias vocabulary so argmax is stable and position-dependent.
        with torch.no_grad():
            self.proj.bias.zero_()
            for i in range(vocab_size):
                self.proj.bias[i] = float(i % 7)

    def forward(self, input_ids=None, **kwargs):
        if input_ids is None:
            raise TypeError("input_ids required")
        h = self.embed(input_ids.clamp(min=0, max=self.embed.num_embeddings - 1))
        logits = self.proj(h)
        # Make logits slightly input-dependent for entropy variation.
        logits = logits + 0.01 * input_ids.unsqueeze(-1).float()
        return type("Out", (), {"logits": logits})()


def _run(mode: str, **kwargs):
    torch.manual_seed(0)
    model = TinyMockLM()
    return diffusion_sample(
        model=model,
        seq_len=16,
        num_steps=8,
        mask_token_id=0,
        pad_token_id=1,
        eos_token_id=2,
        greedy=True,
        temperature=1.0,
        closure_mode=mode,
        return_closure_trace=True,
        **kwargs,
    )


def test_baseline_off_reproducible():
    a = _run("off")
    b = _run("off")
    assert torch.equal(a["sequences"], b["sequences"])
    assert a["closure_mode"] == "off"
    assert a["closure_trace"] == []


def test_probe_does_not_alter_tokens_vs_off():
    off = _run("off")
    probe = _run("probe")
    assert torch.equal(off["sequences"], probe["sequences"])
    assert probe["closure_trace"], "probe mode should emit telemetry steps"
    assert all(step["mode"] == "probe" for step in probe["closure_trace"] if "mode" in step)


def test_full_mode_terminates_and_emits_trace():
    full = _run("full")
    assert full["sequences"].shape == (1, 16)
    assert full["forward_passes"] >= 1
    assert full["closure_trace"]
    # Finite progress: no remaining masks in the returned sequence tensor path
    assert (full["sequences"] != 0).any()


def test_prefix_suffix_infill_modes():
    model = TinyMockLM()
    torch.manual_seed(1)
    out = diffusion_sample(
        model=model,
        seq_len=20,
        num_steps=6,
        mask_token_id=0,
        pad_token_id=1,
        eos_token_id=2,
        prefix_ids=torch.tensor([3, 4, 5]),
        suffix_ids=torch.tensor([6, 7]),
        greedy=True,
        closure_mode="off",
    )
    assert out.shape == (1, 20)
    assert out[0, 0:3].tolist() == [3, 4, 5]


def test_topk_topp_greedy_stochastic():
    model = TinyMockLM()
    for greedy, top_k, top_p in [
        (True, None, None),
        (False, 5, None),
        (False, None, 0.9),
        (False, 5, 0.8),
    ]:
        torch.manual_seed(2)
        out = diffusion_sample(
            model=model,
            seq_len=12,
            num_steps=4,
            mask_token_id=0,
            pad_token_id=1,
            eos_token_id=2,
            greedy=greedy,
            top_k=top_k,
            top_p=top_p,
            closure_mode="off",
        )
        assert out.shape == (1, 12)


def test_deterministic_seed_closure_trace():
    def run():
        torch.manual_seed(42)
        model = TinyMockLM()
        return diffusion_sample(
            model=model,
            seq_len=16,
            num_steps=8,
            mask_token_id=0,
            pad_token_id=1,
            eos_token_id=2,
            greedy=True,
            closure_mode="full",
            return_closure_trace=True,
        )

    a = run()
    b = run()
    assert torch.equal(a["sequences"], b["sequences"])
    assert a["ordered_support"] == b["ordered_support"]


def test_closure_telemetry_aligns_with_commits():
    full = _run("full")
    for step in full["closure_trace"]:
        if "committed" in step:
            assert step["committed"] >= 0
            assert "ordered_support" in step


def test_full_connected_return_terminates_and_traces():
    out = _run("full-connected-return")
    assert out["sequences"].shape == (1, 16)
    assert out["forward_passes"] >= 1
    assert out["closure_mode"] == "full-connected-return"
    assert out["closure_trace"]
    modes = {s.get("mode") for s in out["closure_trace"] if "mode" in s}
    assert "full-connected-return" in modes
    # Still finite generation
    assert (out["sequences"] != 0).any()


def test_modes_reunified_off_probe_full_connected():
    """Reunified mode surface: off≡probe tokens; full/connected are actuated."""
    off = _run("off")
    probe = _run("probe")
    full = _run("full")
    connected = _run("full-connected-return")
    assert torch.equal(off["sequences"], probe["sequences"])
    assert off["sequences"].shape == full["sequences"].shape == connected["sequences"].shape
    assert connected["closure_mode"] == "full-connected-return"

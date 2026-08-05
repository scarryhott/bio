#!/usr/bin/env python3
# Copyright 2026 scarryhott/bio contributors.
"""Full-model benchmark harness for radicalnumerics/RND1-Base-0910.

Requires external weights and GPU. Results are OPEN EMPIRICAL CLAIM artifacts —
do not treat scores, latency, or PASS counts as closure identity.

Example:
  python benchmarks/compare_rnd1_closure.py \\
    --model radicalnumerics/RND1-Base-0910 \\
    --modes off probe full \\
    --seeds 1 2 3 4 5
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import torch


@dataclass
class RunMetrics:
    mode: str
    seed: int
    output_tokens: list[int]
    completion_len: int
    latency_s: float
    forward_passes: int
    tokens_committed_per_step: list[int]
    open_token_events: int
    contradiction_events: int
    return_residual_mean: float | None
    gpu_memory_allocated_mb: float | None
    closure_path_digest: str | None
    epistemic_status: str = "OPEN EMPIRICAL CLAIM"


def _gpu_mem_mb() -> float | None:
    if not torch.cuda.is_available():
        return None
    return torch.cuda.max_memory_allocated() / (1024 * 1024)


def run_once(model, tokenizer, *, mode: str, seed: int, prompt: str, steps: int) -> RunMetrics:
    from closure.digest import digest
    from rnd.sampling import diffusion_sample

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.cuda.reset_peak_memory_stats()

    prefix = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    t0 = time.perf_counter()
    result = diffusion_sample(
        model=model,
        seq_len=min(128, prefix.shape[-1] + 64),
        num_steps=steps,
        prefix_ids=prefix,
        greedy=True,
        closure_mode=mode,  # type: ignore[arg-type]
        return_closure_trace=True,
    )
    latency = time.perf_counter() - t0
    sequences = result["sequences"]
    trace = result.get("closure_trace", [])
    committed = [int(s.get("committed", 0)) for s in trace if "committed" in s]
    open_events = sum(int(s.get("open", 0)) for s in trace if "open" in s)
    contradictions = sum(int(s.get("rejected", 0)) for s in trace if "rejected" in s)
    residuals = []
    for s in trace:
        tel = s.get("telemetry") or {}
        rr = tel.get("return_residual")
        if rr is not None and hasattr(rr, "mean"):
            residuals.append(float(rr.mean().item()))
    path_digest = digest(result.get("ordered_support", ()))
    return RunMetrics(
        mode=mode,
        seed=seed,
        output_tokens=sequences[0].tolist(),
        completion_len=int(sequences.shape[-1]),
        latency_s=latency,
        forward_passes=int(result.get("forward_passes", 0)),
        tokens_committed_per_step=committed,
        open_token_events=open_events,
        contradiction_events=contradictions,
        return_residual_mean=(sum(residuals) / len(residuals)) if residuals else None,
        gpu_memory_allocated_mb=_gpu_mem_mb(),
        closure_path_digest=path_digest,
    )


def coherence_shadow(tokens: list[int]) -> float:
    """Axiometric shadow only — not closure identity."""
    if len(tokens) < 2:
        return 0.0
    repeats = sum(1 for a, b in zip(tokens, tokens[1:], strict=False) if a == b)
    return 1.0 - repeats / (len(tokens) - 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="radicalnumerics/RND1-Base-0910")
    parser.add_argument("--modes", nargs="+", default=["off", "probe", "full"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[1, 2, 3, 4, 5])
    parser.add_argument("--steps", type=int, default=32)
    parser.add_argument("--prompt", default="The living cell maintains")
    parser.add_argument("--out", type=Path, default=Path("benchmarks/results/latest.json"))
    parser.add_argument(
        "--load-in-4bit",
        action="store_true",
        help="Load with bitsandbytes 4-bit (for 24GB GPUs). OPEN EMPIRICAL CLAIM setup.",
    )
    args = parser.parse_args()

    print(
        "NOTE: This harness produces REPORTED ARTIFACT / OPEN EMPIRICAL CLAIM metrics.\n"
        "Do not interpret scores, entropy, confidence, digests, or PASS counts as closure identity."
    )

    try:
        from transformers import AutoModel, AutoTokenizer
    except ImportError as exc:
        raise SystemExit("transformers required for full-model benchmark") from exc

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    load_kwargs: dict[str, Any] = {"trust_remote_code": True}
    if args.load_in_4bit:
        try:
            from transformers import BitsAndBytesConfig
            import transformers.modeling_utils as modeling_utils

            # MoE 30B on 24GB: skip CUDA caching-allocator warmup (reserves a second huge buffer).
            modeling_utils.caching_allocator_warmup = lambda *a, **k: None  # type: ignore[assignment]
        except ImportError as exc:
            raise SystemExit("bitsandbytes/transformers BitsAndBytesConfig required") from exc
        load_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            llm_int8_enable_fp32_cpu_offload=True,
        )
        # MoE 30B often exceeds 24GB even in 4-bit; allow GPU+CPU split.
        if torch.cuda.is_available():
            load_kwargs["device_map"] = "auto"
            load_kwargs["max_memory"] = {0: "12GiB", "cpu": "120GiB"}
            load_kwargs["offload_folder"] = str(Path("/tmp/rnd1-offload"))
            Path("/tmp/rnd1-offload").mkdir(parents=True, exist_ok=True)
    else:
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        load_kwargs["torch_dtype"] = dtype
        if torch.cuda.is_available():
            load_kwargs["device_map"] = "auto"
    try:
        from rnd import RND1LM

        model = RND1LM.from_pretrained(args.model, **load_kwargs)
    except Exception:
        model = AutoModel.from_pretrained(args.model, **load_kwargs)
    if not hasattr(model, "hf_device_map") and not args.load_in_4bit:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
    model.eval()
    print(
        "device",
        next(model.parameters()).device,
        "dtype",
        next(model.parameters()).dtype,
        "load_in_4bit",
        args.load_in_4bit,
    )

    rows: list[dict[str, Any]] = []
    for mode in args.modes:
        for seed in args.seeds:
            metrics = run_once(
                model,
                tokenizer,
                mode=mode,
                seed=seed,
                prompt=args.prompt,
                steps=args.steps,
            )
            row = asdict(metrics)
            row["coherence_shadow"] = coherence_shadow(metrics.output_tokens)
            rows.append(row)
            print(
                f"mode={mode} seed={seed} latency={metrics.latency_s:.3f}s "
                f"forwards={metrics.forward_passes} open_events={metrics.open_token_events}"
            )

    # Pairwise output differences (baseline vs closure) — descriptive only
    by_seed: dict[int, dict[str, list[int]]] = {}
    for row in rows:
        by_seed.setdefault(row["seed"], {})[row["mode"]] = row["output_tokens"]
    diffs = []
    for seed, modes in by_seed.items():
        if "off" in modes and "full" in modes:
            off_t, full_t = modes["off"], modes["full"]
            n = min(len(off_t), len(full_t))
            diff = sum(1 for i in range(n) if off_t[i] != full_t[i])
            diffs.append({"seed": seed, "off_vs_full_token_diffs": diff, "compared_len": n})

    args.out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": args.model,
        "epistemic_status": "OPEN EMPIRICAL CLAIM",
        "disclaimer": (
            "No score, entropy, confidence, digest, or PASS count is closure identity. "
            "Improved performance is not claimed unless measurements explicitly support it."
        ),
        "runs": rows,
        "baseline_vs_closure_diffs": diffs,
    }
    args.out.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

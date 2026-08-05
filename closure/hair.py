# Copyright 2026 scarryhott/bio contributors.
"""Holistic typed hair construction for RND1 denoising steps."""

from __future__ import annotations

from typing import Any

from .types import HairComposition, HairSource


def build_holistic_hair(
    *,
    tokens: list[int] | None = None,
    maskable: list[bool] | None = None,
    local_scores: list[float] | None = None,
    prefix_len: int = 0,
    suffix_len: int = 0,
    local_radius: int = 2,
    distant_radius: int = 8,
    hidden_summary: dict[str, Any] | None = None,
    expert_routing: dict[str, Any] | None = None,
    denoising_history: list[dict[str, Any]] | None = None,
    biological_context: dict[str, Any] | None = None,
    step_index: int = 0,
) -> HairComposition:
    """Compose typed hair sources. Scalar blend ranks probes only."""
    tokens = tokens or []
    maskable = maskable or [False] * len(tokens)
    local_scores = local_scores or [0.0] * len(tokens)
    n = len(tokens)

    local_vals: list[float] = []
    distant_vals: list[float] = []
    for i in range(n):
        if not maskable[i]:
            continue
        local_n = 0.0
        local_d = 0.0
        distant_n = 0.0
        distant_d = 0.0
        for d in range(1, max(local_radius, distant_radius) + 1):
            for j in (i - d, i + d):
                if j < 0 or j >= n:
                    continue
                weight = local_scores[j]
                if d <= local_radius:
                    local_n += weight
                    local_d += 1.0
                if d <= distant_radius:
                    distant_n += weight
                    distant_d += 1.0
        local_vals.append(local_n / local_d if local_d else 0.0)
        distant_vals.append(distant_n / distant_d if distant_d else 0.0)

    committed = [t for t, m in zip(tokens, maskable, strict=False) if not m]
    seq_digest = None
    if committed:
        # Lightweight whole-sequence digest reference (not identity).
        from .digest import digest

        seq_digest = digest({"committed_tokens": committed, "length": n})

    prefix_suffix_scalar = 0.0
    if n:
        filled = sum(1 for m in maskable if not m)
        prefix_suffix_scalar = min(1.0, (prefix_len + suffix_len + filled) / max(n, 1))

    hair = HairComposition(
        local_token=HairSource(
            kind="local_token",
            payload={"radius": local_radius, "values": local_vals},
            scalar=_mean(local_vals),
        ),
        distant_sequence=HairSource(
            kind="distant_sequence",
            payload={"radius": distant_radius, "values": distant_vals},
            scalar=_mean(distant_vals),
        ),
        prefix_suffix=HairSource(
            kind="prefix_suffix_relation",
            payload={"prefix_len": prefix_len, "suffix_len": suffix_len},
            scalar=prefix_suffix_scalar,
        ),
        whole_sequence_digest=HairSource(
            kind="whole_sequence_digest",
            payload={"digest": seq_digest, "n": n},
            scalar=1.0 if seq_digest else 0.0,
        ),
        cross_step_history=HairSource(
            kind="cross_step_denoising_history",
            payload={"step": step_index, "history_len": len(denoising_history or [])},
            scalar=min(1.0, len(denoising_history or []) / 16.0),
        ),
    )

    if hidden_summary is not None:
        hair.hidden_layer = HairSource(
            kind="hidden_layer_relation",
            payload=hidden_summary,
            scalar=float(hidden_summary.get("norm", 0.0)),
        )
    if expert_routing is not None:
        hair.moe_expert_routing = HairSource(
            kind="moe_expert_routing",
            payload=expert_routing,
            scalar=float(expert_routing.get("entropy", 0.0)),
        )
    if biological_context is not None:
        hair.external_biological = HairSource(
            kind="external_biological_context",
            payload=biological_context,
            scalar=float(biological_context.get("viability_shadow", 0.0)),
        )
    return hair


def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0

# Copyright 2025 Radical Numerics Inc.
#
# This source code is licensed under the Apache License, Version 2.0, found in the
# LICENSE file in the root directory of this source tree.

"""
Radical Numerics Diffusion (RND1) - Diffusion-based Language Model.

Heavy HuggingFace / modeling imports are lazy so `rnd.sampling` can be used in
lightweight tests without requiring a fully compatible transformers stack.
"""

from __future__ import annotations

from typing import Any

__version__ = "0.1.0"

__all__ = [
    "RND1Config",
    "RND1GenerationConfig",
    "RND1LM",
    "RND1Model",
    "RND1PreTrainedModel",
    "RND1Attention",
    "RND1DecoderLayer",
    "RND1SparseMoeBlock",
    "RND1GenerationMixin",
    "TerminalVisualizer",
    "SimpleProgressBar",
    "apply_top_k_filtering",
    "apply_top_p_filtering",
    "diffusion_sample",
]


def __getattr__(name: str) -> Any:
    if name in {"apply_top_k_filtering", "apply_top_p_filtering", "diffusion_sample"}:
        from . import sampling

        return getattr(sampling, name)

    if name == "RND1GenerationConfig":
        from .generation_config import RND1GenerationConfig

        return RND1GenerationConfig

    if name == "RND1Config":
        from .configuration_rnd import RND1Config

        return RND1Config

    if name in {
        "RND1LM",
        "RND1Attention",
        "RND1DecoderLayer",
        "RND1Model",
        "RND1PreTrainedModel",
        "RND1SparseMoeBlock",
    }:
        from . import modeling_rnd

        return getattr(modeling_rnd, name)

    if name == "RND1GenerationMixin":
        from .generation_utils import RND1GenerationMixin

        return RND1GenerationMixin

    if name in {"TerminalVisualizer", "SimpleProgressBar"}:
        from . import terminal_visualizer

        return getattr(terminal_visualizer, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _register_auto_classes() -> None:
    try:
        from transformers import AutoConfig, AutoModel, AutoModelForMaskedLM

        from .configuration_rnd import RND1Config
        from .modeling_rnd import RND1LM, RND1Model

        AutoConfig.register("rnd1", RND1Config)
        AutoModel.register(RND1Config, RND1Model)
        AutoModelForMaskedLM.register(RND1Config, RND1LM)
    except Exception:
        # transformers unavailable or incompatible in the active environment
        pass


_register_auto_classes()

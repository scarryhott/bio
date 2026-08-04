from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class TokenAdmission:
    admit: torch.Tensor
    open: torch.Tensor
    telemetry: dict[str, torch.Tensor]


def closure_token_admission(
    confidence: torch.Tensor,
    entropy: torch.Tensor,
    maskable: torch.Tensor,
    target_count: int,
    radius: int = 2,
) -> TokenAdmission:
    """Order RND1 probes without treating the score as closure identity.

    This finite controller supplies local/hair/global/return telemetry. Its
    admitted positions are provisional microactions; semantic closure still
    requires an independent ReturnWitness through ClosureRuntime.
    """
    active = maskable.to(confidence.dtype)
    count = active.sum(1, keepdim=True).clamp_min(1)
    mean = (confidence * active).sum(1, keepdim=True) / count
    var = (((confidence - mean) ** 2) * active).sum(1, keepdim=True) / count
    local = torch.sigmoid((confidence - mean) / var.sqrt().clamp_min(1e-5))

    numerator = torch.zeros_like(local)
    denominator = torch.zeros_like(local)
    for distance in range(1, radius + 1):
        for direction in (-1, 1):
            shifted = torch.roll(local, direction * distance, dims=1)
            shifted_mask = torch.roll(active, direction * distance, dims=1)
            numerator += shifted * shifted_mask
            denominator += shifted_mask
    hair = numerator / denominator.clamp_min(1)
    global_digest = (local * active).sum(1, keepdim=True) / count
    returned = torch.tanh(0.55 * local + 0.25 * hair + 0.20 * global_digest)
    residual = (returned - local).abs()
    probe_score = returned + 0.25 * (1 - residual) - 0.25 * torch.tanh(entropy)

    score = probe_score.masked_fill(~maskable, float("-inf"))
    admit = torch.zeros_like(maskable)
    for batch in range(score.shape[0]):
        available = int(maskable[batch].sum())
        k = min(max(target_count, 1), available)
        if k:
            admit[batch, torch.topk(score[batch], k=k).indices] = True

    open_mask = maskable & ~admit
    return TokenAdmission(
        admit=admit,
        open=open_mask,
        telemetry={
            "local": local,
            "hair": hair,
            "global_digest": global_digest,
            "returned": returned,
            "return_residual": residual,
            "probe_score": probe_score,
        },
    )

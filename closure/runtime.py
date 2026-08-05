# Copyright 2026 scarryhott/bio contributors.
"""Finite closure runtime: ordered return, non-repetition, refusal, child gates."""

from __future__ import annotations

from dataclasses import asdict

from .digest import digest, interaction_digest
from .types import (
    ClosureCarrier,
    ClosureReceipt,
    MicroAction,
    PotentialGate,
    Resolution,
    ReturnWitness,
)


class ClosureRuntime:
    """Finite closure carrier controller.

    Scores may order probes, but they never authorize closure. Admission requires
    ordered support, transformed return, mandate compliance, and recoverability.
    """

    def append_action(self, gate: PotentialGate, action: MicroAction) -> None:
        tails = gate.ball.setdefault("actor_tails", {})
        expected = tails.get(action.actor_id, action.prior_tail)
        if expected != action.prior_tail:
            raise ValueError("microaction ancestry does not match the actor closure tail")
        gate.ordered_actions.append(action)
        tails[action.actor_id] = digest(asdict(action))

    def ordered_support(self, gate: PotentialGate) -> tuple[str, ...]:
        return tuple(digest(asdict(a)) for a in gate.ordered_actions)

    def resolve(self, gate: PotentialGate, witness: ReturnWitness | None) -> ClosureReceipt:
        if witness is None:
            return self._receipt(
                gate,
                Resolution.OPEN,
                None,
                None,
                {"reason": "missing return"},
                new_rank=False,
                write_back=False,
            )

        if witness.refused:
            gate.status = Resolution.REFUSED
            return self._receipt(
                gate,
                Resolution.REFUSED,
                witness.recovered_relation,
                witness.next_opening,
                {"reason": "local mandate refused write-back"},
                return_side=witness.return_side,
                new_rank=False,
                write_back=False,
            )

        action_support = self.ordered_support(gate)
        if witness.ordered_support != action_support:
            gate.status = Resolution.FALSE_COLLAPSE
            return self._receipt(
                gate,
                Resolution.FALSE_COLLAPSE,
                witness.recovered_relation,
                witness.next_opening,
                {"reason": "ordered support mismatch or reordered return"},
                return_side=witness.return_side,
                new_rank=False,
                write_back=False,
            )

        if gate.parent_support is not None:
            # Child gate recoverability: child support must extend parent support.
            if action_support[: len(gate.parent_support)] != gate.parent_support:
                gate.status = Resolution.FALSE_COLLAPSE
                return self._receipt(
                    gate,
                    Resolution.FALSE_COLLAPSE,
                    witness.recovered_relation,
                    witness.next_opening,
                    {"reason": "child support not reconstructible through parent"},
                    return_side=witness.return_side,
                    new_rank=False,
                    write_back=False,
                )

        controlled = set(gate.admissibility.get("controlled_boundaries", []))
        if witness.source_boundary in controlled:
            return self._receipt(
                gate,
                Resolution.OPEN,
                witness.recovered_relation,
                witness.next_opening,
                {"reason": "no independent relational curvature"},
                return_side=witness.return_side,
                new_rank=False,
                write_back=False,
            )

        expected_relation = gate.semantics.get("relation_key")
        if witness.recovered_relation != expected_relation:
            gate.status = Resolution.FALSE_COLLAPSE
            return self._receipt(
                gate,
                Resolution.FALSE_COLLAPSE,
                witness.recovered_relation,
                witness.next_opening,
                {"reason": "returned relation was not recoverable"},
                return_side=witness.return_side,
                new_rank=False,
                write_back=False,
            )

        required = set(gate.mandate.get("required_witness_fields", []))
        if not required.issubset(witness.consequence):
            return self._receipt(
                gate,
                Resolution.OPEN,
                witness.recovered_relation,
                witness.next_opening,
                {"reason": "required witness or provenance remains absent"},
                return_side=witness.return_side,
                new_rank=False,
                write_back=False,
            )

        # Non-repetition: identical relational replay creates no new rank.
        # [Γ⋄W]_C = [Γ]_C when W introduces no independently transformed relation.
        rank_key = digest(
            {
                "support": action_support,
                "relation": witness.recovered_relation,
                "path": witness.transformation_path,
                "side": witness.return_side or gate.return_side,
                "discrepancy": witness.return_discrepancy,
            }
        )
        if rank_key in gate.closure_ranks:
            return self._receipt(
                gate,
                Resolution.OPEN,
                witness.recovered_relation,
                witness.next_opening,
                {"reason": "finite self-repetition creates no new closure rank"},
                return_side=witness.return_side,
                new_rank=False,
                write_back=False,
            )

        if witness.next_opening:
            gate.status = Resolution.CLOSED_TO_OPENING
            gate.closure_ranks.add(rank_key)
            return self._receipt(
                gate,
                Resolution.CLOSED_TO_OPENING,
                witness.recovered_relation,
                witness.next_opening,
                {"reason": "parent returned and generated child opening"},
                return_side=witness.return_side,
                new_rank=True,
                write_back=True,
            )

        gate.status = Resolution.CLOSED_HIGHER
        gate.closure_ranks.add(rank_key)
        return self._receipt(
            gate,
            Resolution.CLOSED_HIGHER,
            witness.recovered_relation,
            None,
            {"reason": "non-identical transformed return recovered the maintained relation"},
            return_side=witness.return_side,
            new_rank=True,
            write_back=True,
        )

    def spawn_child_gate(
        self,
        parent: PotentialGate,
        *,
        gate_id: str,
        opening: str,
        return_side: str | None = None,
    ) -> PotentialGate:
        parent_support = self.ordered_support(parent)
        ball = {k: v for k, v in parent.ball.items() if k != "actor_tails"}
        ball["actor_tails"] = {}
        ball["parent_gate"] = parent.gate_id
        return PotentialGate(
            gate_id=gate_id,
            originless_basis=parent.originless_basis,
            ball=ball,
            possible_hair=list(parent.possible_hair),
            semantics=dict(parent.semantics),
            openings=[opening],
            admissibility=dict(parent.admissibility),
            mandate=dict(parent.mandate),
            return_side=return_side or parent.return_side,
            parent_support=parent_support,
        )

    def invert_return_side(self, side: str) -> str:
        mapping = {"local": "global", "global": "local", "ball": "hair", "hair": "ball"}
        return mapping.get(side, f"complement:{side}")

    def integrate_carrier(
        self,
        carrier: ClosureCarrier,
        witness: ReturnWitness | None,
    ) -> ClosureReceipt:
        carrier.gate.ordered_actions = list(carrier.ordered_history)
        receipt = self.resolve(carrier.gate, witness)
        if receipt.write_back_allowed and receipt.resolution in {
            Resolution.CLOSED_HIGHER,
            Resolution.CLOSED_TO_OPENING,
        }:
            carrier.committed_trace.append(
                {
                    "step": carrier.step_index,
                    "resolution": receipt.resolution.value,
                    "support": receipt.ordered_support,
                    "digest": receipt.basis_digest,
                }
            )
        return receipt

    def _receipt(
        self,
        gate: PotentialGate,
        resolution: Resolution,
        relation: str | None,
        next_opening: str | None,
        evidence: dict,
        *,
        return_side: str | None = None,
        new_rank: bool = False,
        write_back: bool = True,
    ) -> ClosureReceipt:
        support = self.ordered_support(gate)
        basis = interaction_digest(
            originless_basis=gate.originless_basis,
            gate_id=gate.gate_id,
            ordered_support=support,
            relation=relation,
            resolution=resolution.value,
            next_opening=next_opening,
            return_side=return_side or gate.return_side,
            openings=tuple(gate.openings),
        )
        return ClosureReceipt(
            gate_id=gate.gate_id,
            resolution=resolution,
            basis_digest=basis,
            ordered_support=support,
            recovered_relation=relation,
            next_opening=next_opening,
            evidence=evidence,
            return_side=return_side or gate.return_side,
            new_closure_rank=new_rank,
            write_back_allowed=write_back and resolution is not Resolution.REFUSED,
        )

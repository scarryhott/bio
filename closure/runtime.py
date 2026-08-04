from __future__ import annotations

import hashlib
import json
from dataclasses import asdict

from .types import ClosureReceipt, MicroAction, PotentialGate, Resolution, ReturnWitness


def _digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode()).hexdigest()[:24]


class ClosureRuntime:
    """Finite closure carrier.

    Scores may order probes, but they never authorize closure. Admission requires
    ordered support, transformed return, mandate compliance, and recoverability.
    """

    def append_action(self, gate: PotentialGate, action: MicroAction) -> None:
        tails = gate.ball.setdefault("actor_tails", {})
        expected = tails.get(action.actor_id, action.prior_tail)
        if expected != action.prior_tail:
            raise ValueError("microaction ancestry does not match the actor closure tail")
        gate.ordered_actions.append(action)
        tails[action.actor_id] = _digest(asdict(action))

    def resolve(self, gate: PotentialGate, witness: ReturnWitness | None) -> ClosureReceipt:
        if witness is None:
            return self._receipt(gate, Resolution.OPEN, None, None, {"reason": "missing return"})

        if witness.refused:
            gate.status = Resolution.REFUSED
            return self._receipt(
                gate, Resolution.REFUSED, witness.recovered_relation, witness.next_opening,
                {"reason": "local mandate refused write-back"},
            )

        action_support = tuple(_digest(asdict(a)) for a in gate.ordered_actions)
        if witness.ordered_support != action_support:
            gate.status = Resolution.FALSE_COLLAPSE
            return self._receipt(
                gate, Resolution.FALSE_COLLAPSE, witness.recovered_relation, witness.next_opening,
                {"reason": "ordered support mismatch or reordered return"},
            )

        controlled = set(gate.admissibility.get("controlled_boundaries", []))
        if witness.source_boundary in controlled:
            return self._receipt(
                gate, Resolution.OPEN, witness.recovered_relation, witness.next_opening,
                {"reason": "no independent relational curvature"},
            )

        expected_relation = gate.semantics.get("relation_key")
        if witness.recovered_relation != expected_relation:
            gate.status = Resolution.FALSE_COLLAPSE
            return self._receipt(
                gate, Resolution.FALSE_COLLAPSE, witness.recovered_relation, witness.next_opening,
                {"reason": "returned relation was not recoverable"},
            )

        required = set(gate.mandate.get("required_witness_fields", []))
        if not required.issubset(witness.consequence):
            return self._receipt(
                gate, Resolution.OPEN, witness.recovered_relation, witness.next_opening,
                {"reason": "required witness or provenance remains absent"},
            )

        if witness.next_opening:
            gate.status = Resolution.CLOSED_TO_OPENING
            return self._receipt(
                gate, Resolution.CLOSED_TO_OPENING, witness.recovered_relation,
                witness.next_opening, {"reason": "parent returned and generated child opening"},
            )

        gate.status = Resolution.CLOSED_HIGHER
        return self._receipt(
            gate, Resolution.CLOSED_HIGHER, witness.recovered_relation, None,
            {"reason": "non-identical transformed return recovered the maintained relation"},
        )

    def _receipt(
        self,
        gate: PotentialGate,
        resolution: Resolution,
        relation: str | None,
        next_opening: str | None,
        evidence: dict,
    ) -> ClosureReceipt:
        support = tuple(_digest(asdict(a)) for a in gate.ordered_actions)
        basis = {
            "originless_basis": gate.originless_basis,
            "gate": gate.gate_id,
            "support": support,
            "relation": relation,
            "resolution": resolution.value,
            "next_opening": next_opening,
        }
        return ClosureReceipt(
            gate_id=gate.gate_id,
            resolution=resolution,
            basis_digest=f"interaction_C:{_digest(basis)}",
            ordered_support=support,
            recovered_relation=relation,
            next_opening=next_opening,
            evidence=evidence,
        )

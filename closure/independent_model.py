"""Standalone closure-native learner ported from UnifiedClosureArchitecturalLoop.

The model is independent of Radical Numerics/RND1. Its transition is:

    (C_t, E_t, A_legal,t) -> A_t
      -> (E_t+1, A_legal,t+1) -> C_t+1

Only an independently returned, recoverable complete cycle enters memory.
Self-authored/missing returns stay OPEN; contradictions are REJECTED. Digests
are deterministic receipts, never closure authority.
"""

from __future__ import annotations

import base64
import dataclasses
import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping

ORIGINLESS_GENESIS = "ORIGINLESS-CLOSURE-PRIOR"


def stable_digest(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=lambda x: asdict(x) if hasattr(x, "__dataclass_fields__") else str(x),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


class InterfaceValueError(ValueError):
    pass


class Admission(str, Enum):
    ADMITTED = "ADMITTED"
    OPEN = "OPEN"
    REJECTED = "REJECTED"


def canonical_value(value: Any) -> Any:
    if value is None:
        return {"$none": True}
    if isinstance(value, bool):
        return {"$bool": value}
    if isinstance(value, int) and not isinstance(value, bool):
        return {"$int": str(value)}
    if isinstance(value, float):
        if math.isnan(value):
            return {"$real": "nan"}
        if math.isinf(value):
            return {"$real": "+inf" if value > 0 else "-inf"}
        return {"$real": value}
    if isinstance(value, str):
        return {"$text": value}
    if isinstance(value, (bytes, bytearray, memoryview)):
        return {"$bytes": base64.b64encode(bytes(value)).decode()}
    if isinstance(value, Enum):
        return {"$enum": [type(value).__qualname__, canonical_value(value.value)]}
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {"$dataclass": [type(value).__qualname__, canonical_value(asdict(value))]}
    if isinstance(value, Mapping):
        rows = [(canonical_value(k), canonical_value(v)) for k, v in value.items()]
        rows.sort(key=lambda row: json.dumps(row, sort_keys=True, default=str))
        return {"$map": rows}
    if isinstance(value, tuple):
        return {"$tuple": [canonical_value(v) for v in value]}
    if isinstance(value, list):
        return {"$list": [canonical_value(v) for v in value]}
    if isinstance(value, (set, frozenset)):
        rows = [canonical_value(v) for v in value]
        rows.sort(key=lambda row: json.dumps(row, sort_keys=True, default=str))
        return {"$set": rows}
    raise InterfaceValueError(f"unsupported finite carrier type: {type(value)!r}")


def canonical_json(value: Any) -> str:
    return json.dumps(canonical_value(value), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class OpaqueAction:
    original: Any
    canonical: Any
    key: str

    @classmethod
    def from_value(cls, value: Any) -> "OpaqueAction":
        canonical = canonical_value(value)
        return cls(value, canonical, json.dumps(canonical, sort_keys=True, separators=(",", ":")))


@dataclass(frozen=True)
class OpaqueConfiguration:
    observation: Any
    actions: tuple[OpaqueAction, ...]
    observation_digest: str
    legal_field_digest: str
    relation_digest: str

    @classmethod
    def form(cls, observation: Any, legal_actions: Iterable[Any]) -> "OpaqueConfiguration":
        by_key: dict[str, OpaqueAction] = {}
        for raw in legal_actions:
            action = OpaqueAction.from_value(raw)
            by_key.setdefault(action.key, action)
        actions = tuple(by_key[key] for key in sorted(by_key))
        observation_digest = stable_digest(canonical_value(observation))
        legal_field_digest = stable_digest([action.canonical for action in actions])
        relation_digest = stable_digest(
            {"observation": observation_digest, "legal_field": legal_field_digest}
        )
        return cls(observation, actions, observation_digest, legal_field_digest, relation_digest)


@dataclass(frozen=True)
class ProvisionalProjection:
    prior_unity_digest: str
    source_relation_digest: str
    action_key: str
    intent_digest: str
    seal_digest: str


@dataclass(frozen=True)
class IndependentEvaluation:
    returned_seal_digest: str
    observed_action_key: str
    target_relation_digest: str
    effect_digest: str
    independently_observed: bool
    witness_accessible: bool
    authorized: bool
    self_authored: bool
    refused: bool
    contradictory: bool
    return_digest: str


@dataclass(frozen=True)
class ClosureBackComparison:
    prior_relation_recovered: bool
    seal_recovered: bool
    action_recovered: bool
    effect_recovered: bool
    return_is_independent: bool
    witness_is_accessible: bool
    authorized: bool
    domain_return_consistent: bool
    admission: Admission
    reason: str
    comparison_digest: str


@dataclass(frozen=True)
class ArchitecturalUnity:
    projection: ProvisionalProjection
    evaluation: IndependentEvaluation
    comparison: ClosureBackComparison
    source_relation_digest: str
    target_relation_digest: str
    unity_digest: str
    identity_is_complete_cycle: bool = True


@dataclass(frozen=True)
class LoopInvariant:
    authoritative_digest: str
    admitted_unities: int
    relation_presentations: int
    invariant_digest: str


@dataclass(frozen=True)
class InterfaceProjection:
    configuration: OpaqueConfiguration
    selected_action: OpaqueAction
    closure_projection: ProvisionalProjection


@dataclass(frozen=True)
class ArchitecturalLoopTurn:
    source_configuration: OpaqueConfiguration
    target_configuration: OpaqueConfiguration
    selected_action: OpaqueAction
    learned_before: LoopInvariant
    evaluation: IndependentEvaluation
    comparison: ClosureBackComparison
    unity: ArchitecturalUnity
    learned_after: LoopInvariant
    next_projection: InterfaceProjection | None


@dataclass
class ClosureLoopMemory:
    authoritative_digest: str = ORIGINLESS_GENESIS
    admitted: dict[str, ArchitecturalUnity] = field(default_factory=dict)
    quarantined: list[ArchitecturalUnity] = field(default_factory=list)

    def invariant(self) -> LoopInvariant:
        relations = {
            relation
            for unity in self.admitted.values()
            for relation in (unity.source_relation_digest, unity.target_relation_digest)
        }
        return LoopInvariant(
            self.authoritative_digest,
            len(self.admitted),
            len(relations),
            stable_digest(
                {
                    "authority": self.authoritative_digest,
                    "unities": sorted(self.admitted),
                    "relations": sorted(relations),
                }
            ),
        )

    def commit(self, unity: ArchitecturalUnity) -> LoopInvariant:
        if unity.comparison.admission is not Admission.ADMITTED:
            self.quarantined.append(unity)
            return self.invariant()
        if unity.unity_digest not in self.admitted:
            self.admitted[unity.unity_digest] = unity
            self.authoritative_digest = stable_digest(
                {"parent": self.authoritative_digest, "unity": unity.unity_digest}
            )
        return self.invariant()


class UnifiedClosureArchitecturalLoop:
    """Independent proposal, return resolution, and admitted-history learner."""

    PIPELINE = (
        "learn_from_admitted_relations",
        "project_provisional_action",
        "seal_before_evaluation",
        "receive_independent_return",
        "closure_back_comparison",
        "commit_or_quarantine",
        "project_next_action",
    )

    def __init__(self) -> None:
        self.memory = ClosureLoopMemory()

    @property
    def protocol_digest(self) -> str:
        return stable_digest(self.PIPELINE)

    def begin_turn(self, observation: Any, legal_actions: Iterable[Any]) -> InterfaceProjection:
        configuration = OpaqueConfiguration.form(observation, legal_actions)
        if not configuration.actions:
            raise ValueError("complete legal action field must be non-empty")
        tried = {
            unity.projection.action_key
            for unity in self.memory.admitted.values()
            if unity.source_relation_digest == configuration.relation_digest
        }
        selected = next(
            (action for action in configuration.actions if action.key not in tried),
            configuration.actions[0],
        )
        intent = stable_digest(
            {
                "source": configuration.relation_digest,
                "action": selected.key,
                "history": self.memory.invariant().invariant_digest,
            }
        )
        seal = stable_digest(
            {
                "prior": self.memory.authoritative_digest,
                "source": configuration.relation_digest,
                "action": selected.key,
                "intent": intent,
            }
        )
        return InterfaceProjection(
            configuration,
            selected,
            ProvisionalProjection(
                self.memory.authoritative_digest,
                configuration.relation_digest,
                selected.key,
                intent,
                seal,
            ),
        )

    def close_turn(
        self,
        pending: InterfaceProjection,
        returned_observation: Any,
        next_legal_actions: Iterable[Any],
        *,
        independent: bool = True,
        witness_accessible: bool = True,
        authorized: bool = True,
        self_authored: bool = False,
        refused: bool = False,
        contradictory: bool = False,
        domain_return_consistent: bool = True,
    ) -> ArchitecturalLoopTurn:
        before = self.memory.invariant()
        target = OpaqueConfiguration.form(returned_observation, next_legal_actions)
        effect = stable_digest(
            {
                "source": pending.configuration.observation_digest,
                "action": pending.selected_action.canonical,
                "return": target.observation_digest,
            }
        )
        evaluation = IndependentEvaluation(
            pending.closure_projection.seal_digest,
            pending.selected_action.key,
            target.relation_digest,
            effect,
            independent,
            witness_accessible,
            authorized,
            self_authored,
            refused,
            contradictory,
            stable_digest(
                {
                    "seal": pending.closure_projection.seal_digest,
                    "action": pending.selected_action.key,
                    "target": target.relation_digest,
                    "effect": effect,
                    "independent": independent,
                    "self_authored": self_authored,
                }
            ),
        )
        relation_ok = (
            pending.configuration.relation_digest
            == pending.closure_projection.source_relation_digest
        )
        seal_ok = evaluation.returned_seal_digest == pending.closure_projection.seal_digest
        action_ok = evaluation.observed_action_key == pending.selected_action.key
        effect_ok = bool(evaluation.effect_digest)
        consistent = domain_return_consistent and not contradictory

        if refused:
            admission, reason = Admission.REJECTED, "local mandate refused write-back"
        elif not consistent:
            admission, reason = Admission.REJECTED, "returned consequence contradicted relation"
        elif self_authored or not independent:
            admission, reason = Admission.OPEN, "self-authored or controlled return"
        elif not witness_accessible or not authorized:
            admission, reason = Admission.OPEN, "return witness or authorization absent"
        elif not all((relation_ok, seal_ok, action_ok, effect_ok)):
            admission, reason = Admission.REJECTED, "complete returned cycle unrecoverable"
        else:
            admission, reason = Admission.ADMITTED, "complete causal return recovered as unity"

        comparison_payload = {
            "relation": relation_ok,
            "seal": seal_ok,
            "action": action_ok,
            "effect": effect_ok,
            "independent": independent and not self_authored,
            "witness": witness_accessible,
            "authorized": authorized and not refused,
            "consistent": consistent,
            "admission": admission.value,
            "reason": reason,
        }
        comparison = ClosureBackComparison(
            relation_ok,
            seal_ok,
            action_ok,
            effect_ok,
            independent and not self_authored,
            witness_accessible,
            authorized and not refused,
            consistent,
            admission,
            reason,
            stable_digest(comparison_payload),
        )
        unity = ArchitecturalUnity(
            pending.closure_projection,
            evaluation,
            comparison,
            pending.configuration.relation_digest,
            target.relation_digest,
            stable_digest(
                {
                    "projection": pending.closure_projection,
                    "evaluation": evaluation,
                    "comparison": comparison,
                }
            ),
        )
        after = self.memory.commit(unity)
        next_projection = (
            self.begin_turn(returned_observation, next_legal_actions) if target.actions else None
        )
        return ArchitecturalLoopTurn(
            pending.configuration,
            target,
            pending.selected_action,
            before,
            evaluation,
            comparison,
            unity,
            after,
            next_projection,
        )

    def transact(
        self,
        observation: Any,
        legal_actions: Iterable[Any],
        returned_observation: Any,
        next_legal_actions: Iterable[Any],
        **return_flags: Any,
    ) -> ArchitecturalLoopTurn:
        return self.close_turn(
            self.begin_turn(observation, legal_actions),
            returned_observation,
            next_legal_actions,
            **return_flags,
        )


__all__ = [
    "Admission",
    "ArchitecturalLoopTurn",
    "ArchitecturalUnity",
    "ClosureBackComparison",
    "ClosureLoopMemory",
    "IndependentEvaluation",
    "InterfaceProjection",
    "InterfaceValueError",
    "LoopInvariant",
    "OpaqueAction",
    "OpaqueConfiguration",
    "ORIGINLESS_GENESIS",
    "ProvisionalProjection",
    "UnifiedClosureArchitecturalLoop",
    "canonical_json",
    "canonical_value",
    "stable_digest",
]

"""Closure verification whose verifier is itself admitted through closure.

This module composes two independently resolved relations:

1. an architectural episode closes through a complete returned cycle; and
2. the candidate verification topology used to interpret that episode is itself
   admitted through the unified closure runtime.

Neither a digest, score, PASS count, nor a predeclared verifier can certify the
composition.  Failure of either side leaves the claim OPEN or REJECTED without
writing it into authoritative closure memory.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .independent_model import Admission, ArchitecturalLoopTurn, stable_digest
from .types import ClosureReceipt, Resolution


class ClosureVerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    OPEN = "OPEN"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class ClosureVerificationReceipt:
    """Receipt for a closure operation verified by a closure-admitted topology."""

    operation_unity_digest: str
    topology_basis_digest: str
    operation_admission: Admission
    topology_resolution: Resolution
    status: ClosureVerificationStatus
    write_back_allowed: bool
    reason: str
    verification_digest: str


def _topology_is_closed(receipt: ClosureReceipt) -> bool:
    return receipt.resolution in {
        Resolution.CLOSED_HIGHER,
        Resolution.CLOSED_TO_OPENING,
    } and receipt.write_back_allowed


def verify_closure_operation(
    turn: ArchitecturalLoopTurn,
    topology_receipt: ClosureReceipt,
) -> ClosureVerificationReceipt:
    """Verify a closure operation only through a closure-admitted verifier.

    The operation and verifier remain distinct carriers.  Their conjunction is
    authoritative only when both independently resolve as closed.  OPEN takes
    precedence over rejection when evidence or independence is missing; a
    positively contradictory/refused/collapsed side is REJECTED.
    """

    operation_admission = turn.comparison.admission
    topology_resolution = topology_receipt.resolution

    operation_complete = (
        turn.unity.identity_is_complete_cycle
        and turn.comparison.prior_relation_recovered
        and turn.comparison.seal_recovered
        and turn.comparison.action_recovered
        and turn.comparison.effect_recovered
        and turn.comparison.return_is_independent
        and turn.comparison.witness_is_accessible
        and turn.comparison.authorized
        and turn.comparison.domain_return_consistent
    )

    topology_closed = _topology_is_closed(topology_receipt)
    topology_open = topology_resolution is Resolution.OPEN
    topology_rejected = topology_resolution in {
        Resolution.FALSE_COLLAPSE,
        Resolution.REFUSED,
    }

    if operation_admission is Admission.REJECTED or topology_rejected:
        status = ClosureVerificationStatus.REJECTED
        write_back = False
        reason = "operation or verification topology positively rejected"
    elif operation_admission is Admission.OPEN or topology_open:
        status = ClosureVerificationStatus.OPEN
        write_back = False
        reason = "operation or verification topology lacks an admissible return"
    elif operation_admission is not Admission.ADMITTED or not operation_complete:
        status = ClosureVerificationStatus.OPEN
        write_back = False
        reason = "complete independently returned operation cycle is not recoverable"
    elif not topology_closed:
        status = ClosureVerificationStatus.OPEN
        write_back = False
        reason = "verification topology is not closure-admitted for write-back"
    else:
        status = ClosureVerificationStatus.VERIFIED
        write_back = True
        reason = "operation and its verification topology are jointly closure-admitted"

    payload: dict[str, Any] = {
        "operation_unity": turn.unity.unity_digest,
        "operation_admission": operation_admission.value,
        "operation_complete": operation_complete,
        "topology_basis": topology_receipt.basis_digest,
        "topology_resolution": topology_resolution.value,
        "topology_write_back": topology_receipt.write_back_allowed,
        "status": status.value,
        "write_back": write_back,
        "reason": reason,
    }

    return ClosureVerificationReceipt(
        operation_unity_digest=turn.unity.unity_digest,
        topology_basis_digest=topology_receipt.basis_digest,
        operation_admission=operation_admission,
        topology_resolution=topology_resolution,
        status=status,
        write_back_allowed=write_back,
        reason=reason,
        verification_digest=stable_digest(payload),
    )


def closure_verification_is_authoritative(receipt: ClosureVerificationReceipt) -> bool:
    """Authority follows joint returned closure, never the receipt digest itself."""

    return (
        receipt.status is ClosureVerificationStatus.VERIFIED
        and receipt.write_back_allowed
        and receipt.operation_admission is Admission.ADMITTED
        and receipt.topology_resolution
        in {Resolution.CLOSED_HIGHER, Resolution.CLOSED_TO_OPENING}
    )


__all__ = [
    "ClosureVerificationReceipt",
    "ClosureVerificationStatus",
    "closure_verification_is_authoritative",
    "verify_closure_operation",
]

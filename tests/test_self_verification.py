from closure.independent_model import UnifiedClosureArchitecturalLoop
from closure.self_verification import (
    ClosureVerificationStatus,
    closure_verification_is_authoritative,
    verify_closure_operation,
)
from closure.topology import UnifiedAxiometry, VerificationTopology, admit_verification_topology


def admitted_topology_receipt():
    topology = VerificationTopology(
        topology_id="returned-cycle-verifier",
        basis_cycle={"path": ["local", "return", "global"]},
        closure_cycle={"path": ["local", "return", "global"]},
        encoding_topos={"relation": "episode"},
        relation_topos={"relation": "episode"},
        openings=["next-return-layer"],
    )
    return admit_verification_topology(UnifiedAxiometry(), topology)


def test_jointly_returned_operation_and_topology_are_verified():
    loop = UnifiedClosureArchitecturalLoop()
    turn = loop.transact(
        {"cell": "before"},
        ["perturb", "observe"],
        {"cell": "after", "measured": True},
        ["observe"],
    )

    receipt = verify_closure_operation(turn, admitted_topology_receipt())

    assert receipt.status is ClosureVerificationStatus.VERIFIED
    assert receipt.write_back_allowed
    assert closure_verification_is_authoritative(receipt)


def test_self_authored_operation_remains_open_even_with_closed_topology():
    loop = UnifiedClosureArchitecturalLoop()
    turn = loop.transact(
        "before",
        ["act"],
        "after",
        ["observe"],
        self_authored=True,
        independent=False,
    )

    receipt = verify_closure_operation(turn, admitted_topology_receipt())

    assert receipt.status is ClosureVerificationStatus.OPEN
    assert not receipt.write_back_allowed
    assert not closure_verification_is_authoritative(receipt)


def test_contradictory_operation_is_rejected_not_converted_to_open():
    loop = UnifiedClosureArchitecturalLoop()
    turn = loop.transact(
        "before",
        ["act"],
        "contradiction",
        ["observe"],
        contradictory=True,
    )

    receipt = verify_closure_operation(turn, admitted_topology_receipt())

    assert receipt.status is ClosureVerificationStatus.REJECTED
    assert not receipt.write_back_allowed


def test_open_topology_cannot_certify_an_admitted_operation():
    open_topology = VerificationTopology(
        topology_id="unresolved-verifier",
        basis_cycle={"side": "local"},
        closure_cycle={"side": "global"},
    )
    topology_receipt = admit_verification_topology(UnifiedAxiometry(), open_topology)

    loop = UnifiedClosureArchitecturalLoop()
    turn = loop.transact("before", ["act"], "after", ["observe"])
    receipt = verify_closure_operation(turn, topology_receipt)

    assert receipt.status is ClosureVerificationStatus.OPEN
    assert not receipt.write_back_allowed

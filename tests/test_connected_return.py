"""Finite connected-return controller tests — Chaitin-derived, not classical Ω."""

from __future__ import annotations

from closure.connected_return import (
    evaluate_connected_return,
    make_occurrence,
    reconstruct_order_from_contacts,
    build_local_cells,
)


def _occ(pos: int, step: int = 1, *, independent: bool = True, residual: float = 0.4, ancestry: str = "denoising_return"):
    return make_occurrence(
        token_id=10 + pos,
        position=pos,
        step=step,
        prior_mask=True,
        ancestry=ancestry,
        return_side="ball",
        residual=residual,
        independently_transformed=independent,
    )


def test_contact_order_admits_chain():
    occs = [_occ(i) for i in range(6)]
    verdict = evaluate_connected_return(occs)
    assert verdict.status == "OK"
    assert verdict.admits
    assert len(verdict.holistic_support) == 6
    assert verdict.shared_contacts or len(verdict.ordered_cells) == 1


def test_same_pole_echo_is_false():
    occs = [
        _occ(i, independent=False, residual=0.0, ancestry="model_echo")
        for i in range(3)
    ]
    verdict = evaluate_connected_return(occs)
    assert verdict.status == "FALSE_SAME_POLE"
    assert not verdict.admits
    assert verdict.admissible_occurrence_ids == ()


def test_missing_occurrences_open():
    verdict = evaluate_connected_return([])
    assert verdict.status == "OPEN_MISSING_RETURN"


def test_broken_contact_open_needle_order():
    # Two cells with positions far apart and no shared contacts.
    a = make_occurrence(
        token_id=1,
        position=0,
        step=1,
        prior_mask=True,
        ancestry="denoising_return",
        return_side="ball",
        residual=0.5,
        independently_transformed=True,
    )
    b = make_occurrence(
        token_id=99,
        position=100,
        step=9,
        prior_mask=True,
        ancestry="denoising_return",
        return_side="hair",
        residual=0.5,
        independently_transformed=True,
    )
    cells = build_local_cells([a, b])
    # Force two cells by building separately if partition collapsed
    if len(cells) < 2:
        from closure.connected_return import LocalCell
        from closure.digest import digest

        cells = [
            LocalCell(
                cell_id="a",
                rank=1,
                rotation_capacity=1,
                occurrences=(a,),
                start_contact=a.contact_boundary(),
                end_contact=a.contact_boundary(),
                fold_seam=digest({"a": 1}),
            ),
            LocalCell(
                cell_id="b",
                rank=2,
                rotation_capacity=2,
                occurrences=(b,),
                start_contact=b.contact_boundary(),
                end_contact=b.contact_boundary(),
                fold_seam=digest({"b": 1}),
            ),
        ]
    status, ordered, shared = reconstruct_order_from_contacts(cells)
    assert status == "OPEN_NEEDLE_ORDER"
    assert ordered == ()
    assert shared == ()


def test_token_equality_does_not_erase_occurrence_identity():
    a = make_occurrence(
        token_id=7,
        position=1,
        step=1,
        prior_mask=True,
        ancestry="denoising_return",
        return_side="ball",
        residual=0.4,
        independently_transformed=True,
    )
    b = make_occurrence(
        token_id=7,
        position=2,
        step=1,
        prior_mask=True,
        ancestry="denoising_return",
        return_side="ball",
        residual=0.4,
        independently_transformed=True,
    )
    assert a.occurrence_id != b.occurrence_id

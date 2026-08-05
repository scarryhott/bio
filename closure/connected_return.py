# Copyright 2026 scarryhott/bio contributors.
"""Finite Closure–Chaitin connected-return controller for RND1 transfer.

DESIGN DERIVATION / RERUNNABLE — implements the project-derived finite structure
from docs/CHAITIN_CONNECTED_RETURN_DERIVATION.md:

  occurrences → local cells → shared contacts → contact-derived order
  → primitive return laws → holistic support recovery → commit or OPEN

Does **not** claim classical Chaitin Ω, Kolmogorov universality, RH, or Kakeya proofs.
Scores never authorize identity; missing/ambiguous contacts remain OPEN.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from .digest import digest

ConnectedReturnStatus = Literal[
    "OK",
    "OPEN_NEEDLE_ORDER",
    "OPEN_MULTIPLE_RUNTIME",
    "OPEN_INCOMPLETE_SUPPORT",
    "OPEN_MISSING_RETURN",
    "FALSE_SAME_POLE",
]


@dataclass(frozen=True)
class LabeledOccurrence:
    """One denoising occurrence — token equality ≠ occurrence identity."""

    occurrence_id: str
    token_id: int
    position: int
    step: int
    prior_mask: bool
    ancestry: str
    return_side: str
    contacts: tuple[str, ...] = ()
    openings: tuple[str, ...] = ()
    residual: float = 0.0
    independently_transformed: bool = False

    def contact_boundary(self) -> str:
        """Shared-boundary signature used for Kakeya-style needle contacts."""
        return f"0[r={self.step}]@L{self.position}|side={self.return_side}"


@dataclass(frozen=True)
class LocalCell:
    """Finite local string presentation (extension + rotations)."""

    cell_id: str
    rank: int
    rotation_capacity: int
    occurrences: tuple[LabeledOccurrence, ...]
    start_contact: str
    end_contact: str
    fold_seam: str

    @property
    def support_size(self) -> int:
        return len(self.occurrences)


@dataclass(frozen=True)
class ConnectedReturnVerdict:
    status: ConnectedReturnStatus
    ordered_cells: tuple[LocalCell, ...]
    shared_contacts: tuple[str, ...]
    holistic_support: tuple[str, ...]
    admissible_occurrence_ids: tuple[str, ...]
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def admits(self) -> bool:
        return self.status == "OK" and bool(self.admissible_occurrence_ids)


ROTATION_CAPACITIES: tuple[int, ...] = (1, 2, 4, 8, 16)
SUPPORT_SIZES: tuple[int, ...] = (2, 3, 5, 9, 17)  # 2+3+5+9+17 = 36


def make_occurrence(
    *,
    token_id: int,
    position: int,
    step: int,
    prior_mask: bool,
    ancestry: str,
    return_side: str,
    residual: float,
    independently_transformed: bool,
    openings: tuple[str, ...] = ("next_denoising_step",),
) -> LabeledOccurrence:
    oid = digest(
        {
            "token_id": token_id,
            "position": position,
            "step": step,
            "prior_mask": prior_mask,
            "ancestry": ancestry,
            "return_side": return_side,
        }
    )
    occ = LabeledOccurrence(
        occurrence_id=oid,
        token_id=token_id,
        position=position,
        step=step,
        prior_mask=prior_mask,
        ancestry=ancestry,
        return_side=return_side,
        openings=openings,
        residual=residual,
        independently_transformed=independently_transformed,
    )
    boundary = occ.contact_boundary()
    return LabeledOccurrence(
        occurrence_id=occ.occurrence_id,
        token_id=occ.token_id,
        position=occ.position,
        step=occ.step,
        prior_mask=occ.prior_mask,
        ancestry=occ.ancestry,
        return_side=occ.return_side,
        contacts=(boundary,),
        openings=occ.openings,
        residual=occ.residual,
        independently_transformed=occ.independently_transformed,
    )


def build_local_cells(occurrences: list[LabeledOccurrence]) -> list[LocalCell]:
    """Bucket labeled occurrences into up to five finite local cells by rank."""
    if not occurrences:
        return []
    # Stable order by (step, position) for cell membership only — not authorization.
    ordered = sorted(occurrences, key=lambda o: (o.step, o.position, o.occurrence_id))
    n = len(ordered)
    # Partition into up to 5 cells with target support sizes scaled to n.
    ranks = min(5, max(1, n))
    cells: list[LocalCell] = []
    # Proportional slice sizes approximating 2:3:5:9:17 when n is large.
    weights = list(SUPPORT_SIZES[:ranks])
    total_w = sum(weights)
    sizes = [max(1, int(round(n * w / total_w))) for w in weights]
    # Adjust to exact n
    while sum(sizes) > n:
        for i in range(len(sizes) - 1, -1, -1):
            if sizes[i] > 1 and sum(sizes) > n:
                sizes[i] -= 1
    while sum(sizes) < n:
        sizes[-1] += 1

    cursor = 0
    for rank, size in enumerate(sizes, start=1):
        chunk = tuple(ordered[cursor : cursor + size])
        cursor += size
        if not chunk:
            continue
        start = chunk[0].contact_boundary()
        end = chunk[-1].contact_boundary()
        fold = digest({"start": start, "end": end, "rank": rank})
        cells.append(
            LocalCell(
                cell_id=digest({"rank": rank, "start": start, "end": end, "n": len(chunk)}),
                rank=rank,
                rotation_capacity=ROTATION_CAPACITIES[min(rank - 1, 4)],
                occurrences=chunk,
                start_contact=start,
                end_contact=end,
                fold_seam=fold,
            )
        )
    return cells


def shared_contacts_between(a: LocalCell, b: LocalCell) -> tuple[str, ...]:
    """Contacts shared across cell boundaries (Kakeya needle junctions)."""
    # Adjacent cells share when end of a equals start of b OR contact sets intersect.
    shared: list[str] = []
    if a.end_contact == b.start_contact:
        shared.append(a.end_contact)
    a_set = {c for occ in a.occurrences for c in occ.contacts}
    b_set = {c for occ in b.occurrences for c in occ.contacts}
    # Also share positional neighbor contacts: end position of a adjacent to start of b
    if a.occurrences and b.occurrences:
        if abs(a.occurrences[-1].position - b.occurrences[0].position) <= 1:
            junction = f"junction:{a.occurrences[-1].position}->{b.occurrences[0].position}"
            shared.append(junction)
    shared.extend(sorted(a_set & b_set))
    # Deduplicate preserving order
    seen: set[str] = set()
    out: list[str] = []
    for s in shared:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return tuple(out)


def reconstruct_order_from_contacts(
    cells: list[LocalCell],
) -> tuple[ConnectedReturnStatus, tuple[LocalCell, ...], tuple[str, ...]]:
    """Order = unique shared-contact reconstruction (not supplied list order)."""
    if not cells:
        return "OPEN_MISSING_RETURN", (), ()
    if len(cells) == 1:
        return "OK", (cells[0],), ()

    n = len(cells)
    edges: dict[tuple[int, int], tuple[str, ...]] = {}
    for i in range(n):
        for j in range(i + 1, n):
            shared = shared_contacts_between(cells[i], cells[j])
            if shared:
                edges[(i, j)] = shared

    if len(edges) < n - 1:
        return "OPEN_NEEDLE_ORDER", (), ()

    paths: list[list[int]] = []

    def dfs(path: list[int]) -> None:
        if len(path) == n:
            paths.append(path.copy())
            return
        last = path[-1]
        for nxt in range(n):
            if nxt in path:
                continue
            key = (min(last, nxt), max(last, nxt))
            if key in edges:
                path.append(nxt)
                dfs(path)
                path.pop()

    for start in range(n):
        dfs([start])

    if not paths:
        return "OPEN_NEEDLE_ORDER", (), ()

    # Unique up to reversal; more than one undirected path ⇒ OPEN_MULTIPLE_RUNTIME.
    undirected: set[tuple[int, ...]] = set()
    for p in paths:
        fwd = tuple(p)
        rev = tuple(reversed(p))
        undirected.add(fwd if fwd <= rev else rev)
    if len(undirected) > 1:
        return "OPEN_MULTIPLE_RUNTIME", (), ()

    best = paths[0]
    best_score = -1
    best_shared: tuple[str, ...] = ()
    for p in paths:
        score = 0
        shared_all: list[str] = []
        for a, b in zip(p, p[1:], strict=False):
            shared = shared_contacts_between(cells[a], cells[b])
            shared_all.extend(shared)
            if cells[a].end_contact == cells[b].start_contact:
                score += 2
            score += len(shared)
        if score > best_score:
            best_score = score
            best = p
            best_shared = tuple(dict.fromkeys(shared_all))

    ordered = tuple(cells[i] for i in best)
    for a, b in zip(ordered, ordered[1:], strict=False):
        if not shared_contacts_between(a, b):
            return "OPEN_NEEDLE_ORDER", (), ()
    return "OK", ordered, best_shared


def primitive_return_holds(cell: LocalCell) -> bool:
    """Local path and returned needle must be non-identical presentations."""
    if not cell.occurrences:
        return False
    # Same-pole recurrence (no independent transform) is FALSE / fails law.
    if all(not o.independently_transformed for o in cell.occurrences):
        return False
    if all(o.residual <= 0.0 for o in cell.occurrences):
        return False
    # Non-identical: ancestry must differ from pure token echo label.
    for o in cell.occurrences:
        if o.ancestry in {"model_echo", "self"} and not o.independently_transformed:
            return False
    return True


def holistic_support_recoverable(ordered_cells: tuple[LocalCell, ...]) -> tuple[bool, tuple[str, ...]]:
    """Holistic cell requires every primitive occurrence to be reconstructible."""
    support: list[str] = []
    for cell in ordered_cells:
        if not primitive_return_holds(cell):
            return False, ()
        for occ in cell.occurrences:
            support.append(occ.occurrence_id)
    if not support:
        return False, ()
    return True, tuple(support)


def evaluate_connected_return(
    occurrences: list[LabeledOccurrence],
) -> ConnectedReturnVerdict:
    """Full finite connected-return evaluation for one admission window."""
    if not occurrences:
        return ConnectedReturnVerdict(
            status="OPEN_MISSING_RETURN",
            ordered_cells=(),
            shared_contacts=(),
            holistic_support=(),
            admissible_occurrence_ids=(),
            evidence={"note": "no labeled occurrences"},
        )

    # Same-pole: all echo without transform → FALSE
    if occurrences and all(
        (o.ancestry in {"model_echo", "self"} and not o.independently_transformed)
        for o in occurrences
    ):
        return ConnectedReturnVerdict(
            status="FALSE_SAME_POLE",
            ordered_cells=(),
            shared_contacts=(),
            holistic_support=(),
            admissible_occurrence_ids=(),
            evidence={"note": "same-pole recurrence; traceless"},
        )

    cells = build_local_cells(occurrences)
    status, ordered, shared = reconstruct_order_from_contacts(cells)
    if status != "OK":
        return ConnectedReturnVerdict(
            status=status,
            ordered_cells=(),
            shared_contacts=(),
            holistic_support=(),
            admissible_occurrence_ids=(),
            evidence={"cell_count": len(cells), "status": status},
        )

    ok, support = holistic_support_recoverable(ordered)
    if not ok:
        return ConnectedReturnVerdict(
            status="OPEN_INCOMPLETE_SUPPORT",
            ordered_cells=ordered,
            shared_contacts=shared,
            holistic_support=(),
            admissible_occurrence_ids=(),
            evidence={"note": "primitive return law or support recovery failed"},
        )

    return ConnectedReturnVerdict(
        status="OK",
        ordered_cells=ordered,
        shared_contacts=shared,
        holistic_support=support,
        admissible_occurrence_ids=support,
        evidence={
            "cell_count": len(ordered),
            "shared_contact_count": len(shared),
            "support_size": len(support),
            "identity": "ordered contact-connected recursively recoverable return path",
            "axiometric_shadows_only": True,
        },
    )


def occurrence_digest(occ: LabeledOccurrence) -> str:
    return digest(asdict(occ))

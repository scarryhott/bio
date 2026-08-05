from __future__ import annotations

from closure.ivi_structure import (
    ivi_ladder,
    ownership_declaration,
    predual_pairs,
    spine_digest,
    thesis_statement,
)


def test_structure_map_loads_ivi_ladder() -> None:
    ladder = ivi_ladder()
    ids = [level.level_id for level in ladder]
    assert ids[:4] == ["ivi0", "ivi1", "ivi2", "ivi3"]
    assert "generator/operator" in thesis_statement().lower() or "generator" in thesis_statement().lower()


def test_predual_is_our_kakeya_chaitin_not_rnd1() -> None:
    pairs = predual_pairs()
    assert "kakeya_i" in pairs
    assert "chaitin_r" in pairs
    own = ownership_declaration()
    assert own["rnd1_is_our_model"] is False
    assert own["radical_numerics_role"] == "external_architecture_comparator_only"
    assert "our" in own["local_kakeya_owner"]


def test_spine_digest_lists_core_structures() -> None:
    spine = spine_digest()
    assert "closure_operator" in spine["core_structure_ids"]
    assert "nrr" in spine["core_structure_ids"]
    assert "predual" in spine["core_structure_ids"]
    assert spine["ownership"]["rnd1_is_our_model"] is False

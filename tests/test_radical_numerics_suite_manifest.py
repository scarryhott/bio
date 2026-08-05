from __future__ import annotations

from benchmarks.plan_radical_numerics_suite import build_plan, load_manifest


def test_manifest_separates_open_and_reported_only_systems() -> None:
    data = load_manifest()
    systems = {row["id"]: row for row in data["systems"]}
    assert systems["evo2-7b"]["runnable"] is True
    assert systems["evo2-40b"]["open_weights"] is True
    assert systems["omnii"]["runnable"] is False
    assert systems["omnii"]["availability"] == "early-access-reported-only"
    assert systems["bio-closure-independent"]["ownership"] == "scarryhott-bio-transcript-thesis"
    assert systems["rnd1-base-0910"]["ownership"] == "radical-numerics"
    assert "EXTERNAL" in systems["rnd1-base-0910"]["epistemic_status"]


def test_default_plan_is_biological_and_runnable() -> None:
    data = load_manifest()
    plan = build_plan(data)
    assert plan
    assert all(arm.runnable for arm in plan)
    assert all(arm.biological_native for arm in plan)
    assert not any(arm.system_id == "omnii" for arm in plan)
    assert not any(arm.system_id == "rnd1-base-0910" for arm in plan)


def test_reported_omnii_can_be_listed_but_not_misclassified() -> None:
    data = load_manifest()
    plan = build_plan(data, include_reported=True)
    omnii = [arm for arm in plan if arm.system_id == "omnii"]
    assert omnii
    assert all(not arm.runnable for arm in omnii)


def test_language_arms_remain_separate_from_biological_default() -> None:
    data = load_manifest()
    plan = build_plan(data, include_nonbiological=True)
    ids = {arm.system_id for arm in plan}
    assert "rnd1-base-0910" not in ids  # no biological benchmark declares it compatible
    assert "rnd1-plus-closure" not in ids


def test_full_open_suite_contains_closure_and_evo2() -> None:
    data = load_manifest()
    plan = build_plan(data)
    ids = {arm.system_id for arm in plan}
    assert "bio-closure-independent" in ids
    assert "evo2-7b" in ids
    assert "evo2-20b" in ids
    assert "evo2-40b" in ids

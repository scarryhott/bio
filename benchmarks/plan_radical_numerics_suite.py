"""Plan and validate the full open Radical Numerics-associated comparison suite.

This module does not download weights or claim model execution. It turns the
suite manifest into an auditable run plan and refuses to schedule reported-only
systems such as Omnii as if they were reproducible local baselines.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MANIFEST_PATH = Path(__file__).with_name("radical_numerics_suite_manifest.json")


@dataclass(frozen=True)
class PlannedArm:
    system_id: str
    benchmark_id: str
    runnable: bool
    biological_native: bool
    availability: str
    status: str


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    validate_manifest(data)
    return data


def validate_manifest(data: dict[str, Any]) -> None:
    systems = data.get("systems")
    benchmarks = data.get("benchmark_families")
    if not isinstance(systems, list) or not systems:
        raise ValueError("manifest must contain a non-empty systems list")
    if not isinstance(benchmarks, list) or not benchmarks:
        raise ValueError("manifest must contain a non-empty benchmark_families list")

    ids = [row.get("id") for row in systems]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("system ids must be present and unique")

    known = set(ids)
    for benchmark in benchmarks:
        benchmark_id = benchmark.get("id")
        if not benchmark_id:
            raise ValueError("every benchmark family requires an id")
        unknown = set(benchmark.get("compatible_systems", [])) - known
        if unknown:
            raise ValueError(f"{benchmark_id} references unknown systems: {sorted(unknown)}")

    for system in systems:
        if system.get("runnable") and system.get("availability") == "early-access-reported-only":
            raise ValueError(f"reported-only system cannot be runnable: {system['id']}")


def build_plan(
    data: dict[str, Any],
    *,
    benchmark_ids: set[str] | None = None,
    include_nonbiological: bool = False,
    include_reported: bool = False,
) -> list[PlannedArm]:
    systems = {row["id"]: row for row in data["systems"]}
    plan: list[PlannedArm] = []
    for benchmark in data["benchmark_families"]:
        if benchmark_ids and benchmark["id"] not in benchmark_ids:
            continue
        for system_id in benchmark.get("compatible_systems", []):
            system = systems[system_id]
            if not include_nonbiological and not system.get("biological_native", False):
                continue
            if not include_reported and not system.get("runnable", False):
                continue
            plan.append(
                PlannedArm(
                    system_id=system_id,
                    benchmark_id=benchmark["id"],
                    runnable=bool(system.get("runnable")),
                    biological_native=bool(system.get("biological_native")),
                    availability=str(system.get("availability")),
                    status=str(system.get("epistemic_status")),
                )
            )
    return plan


def summarize(data: dict[str, Any], plan: list[PlannedArm]) -> dict[str, Any]:
    runnable = [arm for arm in plan if arm.runnable]
    reported = [arm for arm in plan if not arm.runnable]
    return {
        "manifest_status_date": data["status_date"],
        "planned_arms": len(plan),
        "runnable_arms": len(runnable),
        "reported_only_arms": len(reported),
        "systems": sorted({arm.system_id for arm in plan}),
        "benchmarks": sorted({arm.benchmark_id for arm in plan}),
        "framework_verdict": data["verdict"]["framework"],
        "execution_verdict": data["verdict"]["execution"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--benchmark", action="append", default=[])
    parser.add_argument("--include-nonbiological", action="store_true")
    parser.add_argument("--include-reported", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    data = load_manifest(args.manifest)
    plan = build_plan(
        data,
        benchmark_ids=set(args.benchmark) or None,
        include_nonbiological=args.include_nonbiological,
        include_reported=args.include_reported,
    )
    result = summarize(data, plan)
    if args.json:
        print(json.dumps({"summary": result, "plan": [arm.__dict__ for arm in plan]}, indent=2))
        return

    print(result["framework_verdict"])
    print(result["execution_verdict"])
    for arm in plan:
        print(
            f"{arm.benchmark_id:24} {arm.system_id:24} "
            f"runnable={str(arm.runnable).lower():5} {arm.status}"
        )


if __name__ == "__main__":
    main()

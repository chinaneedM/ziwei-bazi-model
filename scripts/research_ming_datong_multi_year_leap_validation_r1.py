from __future__ import annotations

import importlib.util
import json
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 50

ROOT = Path(__file__).resolve().parents[1]
OX_SCRIPT = ROOT / "scripts" / "research_ming_datong_d1_precision_profile_sensitivity_r1.py"

spec = importlib.util.spec_from_file_location("d1_profiles", OX_SCRIPT)
assert spec and spec.loader
d1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d1)

LEAP_LIMIT = Decimal("186552.09")
ZHONGQI_STEP = Decimal("304368.75")
DAY = Decimal("10000")


def _source_context(ctx: dict[str, Any], year: int) -> dict[str, Decimal]:
    c = ctx["constants"]
    distance = Decimal(year) - c["epoch_year"]
    middle = distance * c["year_source_units"]
    winter = (middle + c["qi_response_source_units"]) % c["ji_fa_source_units"]
    run = (middle + c["run_response_source_units"]) % c["shuo_source_units"]
    return {"middle": middle, "winter": winter, "run": run}


def _new_moon(ctx: dict[str, Any], year: int, k: int, profile: str) -> dict[str, Decimal | int]:
    source = _source_context(ctx, year)
    calc = d1.conjunction_for_sequence(ctx, year, k - 1, profile)
    correction = calc["correction_source_units"]
    assert isinstance(correction, Decimal)
    mean_relative = -source["run"] + Decimal(k) * ctx["constants"]["shuo_source_units"]
    absolute_source = source["winter"] + mean_relative + correction
    return {"k": k, "source": absolute_source, "day": int(absolute_source // DAY)}


def _month_sequence(ctx: dict[str, Any], year: int, profile: str, exact_time: bool = False) -> dict[str, Any]:
    source = _source_context(ctx, year)
    # Expand far enough to find two regular month-1 anchors. A pre-year
    # intercalation can shift civil New Year away from a fixed sequence k.
    new_moons = [_new_moon(ctx, year, k, profile) for k in range(20)]
    rows: list[dict[str, Any]] = []
    previous_month: int | None = None

    for k in range(19):
        start = new_moons[k]
        end = new_moons[k + 1]
        zhongqi: list[dict[str, Any]] = []
        for z in range(-2, 21):
            event = source["winter"] + Decimal(z) * ZHONGQI_STEP
            if exact_time:
                inside = start["source"] <= event < end["source"]
            else:
                event_day = int(event // DAY)
                inside = int(start["day"]) <= event_day < int(end["day"])
            if inside:
                zhongqi.append({"z": z, "source": event, "day": int(event // DAY)})

        if zhongqi:
            month = ((zhongqi[0]["z"] + 10) % 12) + 1
            previous_month = month
            is_leap = False
        else:
            if previous_month is None:
                raise AssertionError("month-11 anchor lost before first no-Zhongqi interval")
            month = previous_month
            is_leap = True

        rows.append({
            "k": k, "month": month, "is_leap": is_leap,
            "start_source": start["source"], "start_day": start["day"],
            "next_start_source": end["source"], "next_start_day": end["day"],
            "zhongqi": zhongqi,
        })

    regular_month_one_indices = [
        index for index, row in enumerate(rows)
        if row["month"] == 1 and not row["is_leap"]
    ]
    if len(regular_month_one_indices) < 2:
        raise AssertionError("civil-year ownership boundary requires two regular month-1 anchors")
    start_index, end_index = regular_month_one_indices[:2]
    calendar_rows = rows[start_index:end_index]
    calendar_year = [
        {"month": row["month"], "is_leap": row["is_leap"]}
        for row in calendar_rows
    ]

    leap_months = [row["month"] for row in calendar_year if row["is_leap"]]
    return {
        "run": source["run"],
        "has_leap_by_run": source["run"] >= LEAP_LIMIT,
        "calendar_year": calendar_year,
        "leap_months": leap_months,
        "civil_year_start_k": rows[start_index]["k"],
        "civil_year_end_k_exclusive": rows[end_index]["k"],
        "civil_year_boundary_rule": "FIRST_REGULAR_MONTH_1_TO_BEFORE_NEXT_REGULAR_MONTH_1",
        "fixed_k2_anchor_used": False,
        "raw_rows": rows,
    }


def _prefix_matches(actual: list[dict[str, Any]], expected: list[dict[str, Any]] | None) -> bool:
    if expected is None:
        return True
    return len(actual) >= len(expected) and actual[: len(expected)] == expected


def run(root: Path = ROOT) -> dict[str, Any]:
    ctx = d1._load(root)
    oracle = json.loads((root / "docs/research/MING-DATONG-MULTI-YEAR-LEAP-SAMPLE-ORACLE-R1.json").read_text(encoding="utf-8"))
    controls: list[dict[str, Any]] = []

    for control in oracle["controls"]:
        year = int(control["year"])
        for profile in d1.PROFILES:
            result = _month_sequence(ctx, year, profile)
            leap_month = result["leap_months"][0] if result["leap_months"] else None
            controls.append({
                "year": year,
                "profile": profile,
                "has_leap_match": result["has_leap_by_run"] is bool(control["expected_has_leap"]),
                "leap_month_match": leap_month == control["expected_leap_month"],
                "prefix_match": _prefix_matches(result["calendar_year"], control["expected_prefix"]),
                "generated_leap_month": leap_month,
            })

    day_level = _month_sequence(ctx, 1596, d1.PROFILE_FULL)
    exact = _month_sequence(ctx, 1596, d1.PROFILE_FULL, exact_time=True)
    leap8_row = next(row for row in day_level["raw_rows"] if row["k"] >= 2 and row["month"] == 8 and row["is_leap"])
    next_row = next(row for row in day_level["raw_rows"] if row["k"] == leap8_row["k"] + 1)
    z10_source = _source_context(ctx, 1596)["winter"] + Decimal("10") * ZHONGQI_STEP
    exact_gap = next_row["start_source"] - z10_source

    matched = sum(1 for item in controls if item["has_leap_match"] and item["leap_month_match"] and item["prefix_match"])
    return {
        "profile_count": len(d1.PROFILES),
        "sample_year_count": len(oracle["controls"]),
        "profile_year_control_count": len(controls),
        "matched_profile_year_controls": matched,
        "all_profile_year_controls_match": matched == len(controls),
        "controls": controls,
        "1596_day_level_leap_month": day_level["leap_months"][0],
        "1596_exact_time_counterfactual_leap_month": exact["leap_months"][0],
        "1596_zhongqi10_and_next_conjunction_same_day": int(z10_source // DAY) == int(next_row["start_day"]),
        "1596_zhongqi10_precedes_next_conjunction_source_units": str(exact_gap),
        "1596_zhongqi10_precedes_next_conjunction_hours": str(exact_gap / DAY * Decimal("24")),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

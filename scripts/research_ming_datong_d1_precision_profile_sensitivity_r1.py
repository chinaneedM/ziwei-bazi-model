from __future__ import annotations

import json
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 50

PROFILE_FULL = "FULL_DECIMAL_UNTIL_FINAL_OUTPUT"
PROFILE_LOCAL = "1596_LOCAL_CHIJI6_D1CORR2_TRUNCATE"
PROFILE_HALF_UP = "HALF_UP_AT_1596_LOCAL_WIDTHS"
PROFILE_STORED = "STORED_TABLE_WIDTH_TRUNCATION_ONLY"
PROFILE_1578_REFERENCE = "REPO_1578_REFERENCE"
PROFILES = (PROFILE_FULL, PROFILE_LOCAL, PROFILE_HALF_UP, PROFILE_STORED)


def _q(value: Decimal, quantum: str, rounding: str) -> Decimal:
    return value.quantize(Decimal(quantum), rounding=rounding)


def _load(root: Path) -> dict[str, Any]:
    def read(rel: str) -> Any:
        return json.loads((root / rel).read_text(encoding="utf-8"))

    solar = read("docs/research/MING-DATONG-1569-YINGSUO-FULL-NUMERIC-RECONSTRUCTION-R1.json")
    lunar = read("docs/research/MING-DATONG-1569-CHIJI-FULL-NUMERIC-RECONSTRUCTION-R1.json")
    replay = read("docs/research/MING-DATONG-1578-D1-SOURCE-REPLAY-R1.json")
    fixture = read("docs/research/MING-DATONG-D1-56-CONJUNCTION-VALIDATION-R1.json")

    solar_rows = {
        family["family_id"]: {int(row["day_index"]): row for row in family["rows"]}
        for family in solar["families"]
    }
    lunar_rows = {int(row["limit"]): row for row in lunar["rows"]}
    c = replay["source_constants"]
    constants = {
        key: Decimal(str(value))
        for key, value in c.items()
        if not isinstance(value, dict)
    }
    cutoffs = {
        "a": Decimal(c["yingsuo_cutoffs"]["ying_initial_suo_terminal"]),
        "b": Decimal(c["yingsuo_cutoffs"]["suo_initial_ying_terminal"]),
    }
    return {
        "solar_rows": solar_rows,
        "lunar_rows": lunar_rows,
        "replay": replay,
        "fixture": fixture,
        "constants": constants,
        "cutoffs": cutoffs,
    }


def _solar_difference(ctx: dict[str, Any], state: str, history: Decimal) -> Decimal:
    c = ctx["constants"]
    cut = ctx["cutoffs"]
    half = c["half_year_source_units"]
    if state == "盈":
        family = "YING_INITIAL_SUO_TERMINAL" if history <= cut["a"] else "SUO_INITIAL_YING_TERMINAL"
        x = history if history <= cut["a"] else half - history
    else:
        family = "SUO_INITIAL_YING_TERMINAL" if history <= cut["b"] else "YING_INITIAL_SUO_TERMINAL"
        x = history if history <= cut["b"] else half - history
    day = int(x // Decimal("10000"))
    rem = x - Decimal(day) * Decimal("10000")
    row = ctx["solar_rows"][family][day]
    accumulated = Decimal(row["accumulated_degree"] or "0")
    add = Decimal(row["add_degree"])
    return accumulated + rem / Decimal("10000") * add


def _lunar_difference(ctx: dict[str, Any], state: str, history: Decimal) -> tuple[Decimal, Decimal]:
    rows = ctx["lunar_rows"]
    selected = 0
    for limit in range(1, 169):
        rate = rows[limit]["day_rate_total_source_units"]
        if rate is not None and Decimal(str(rate)) <= history:
            selected = limit
        else:
            break
    row = rows[selected]
    rate = Decimal(str(row["day_rate_total_source_units"] or 0))
    rem = history - rate
    accumulated = Decimal(row["accumulated_chiji_degree"] or "0")
    loss_gain = Decimal(row["loss_gain_degree"])
    if row["loss_gain_sign"] == "益":
        difference = accumulated + rem * loss_gain / Decimal("820")
    else:
        difference = accumulated - rem * loss_gain / Decimal("820")
    divisor = Decimal(row["chi_xingdu_degree"] if state == "迟" else row["ji_xingdu_degree"])
    return difference, divisor


def _apply_profile(profile: str, solar: Decimal, lunar: Decimal, correction: Decimal | None = None) -> tuple[Decimal, Decimal] | Decimal:
    if correction is None:
        if profile == PROFILE_LOCAL:
            return solar, _q(lunar, "0.000001", ROUND_DOWN)
        if profile == PROFILE_HALF_UP:
            return solar, _q(lunar, "0.000001", ROUND_HALF_UP)
        if profile == PROFILE_STORED:
            return _q(solar, "0.00000001", ROUND_DOWN), _q(lunar, "0.00000001", ROUND_DOWN)
        return solar, lunar

    if profile in (PROFILE_LOCAL, PROFILE_1578_REFERENCE):
        return _q(correction, "0.01", ROUND_DOWN)
    if profile == PROFILE_HALF_UP:
        return _q(correction, "0.01", ROUND_HALF_UP)
    return correction


def conjunction_for_sequence(ctx: dict[str, Any], year: int, sequence_index: int, profile: str) -> dict[str, Decimal | str]:
    c = ctx["constants"]
    distance = Decimal(year) - c["epoch_year"]
    middle = distance * c["year_source_units"]
    winter = (middle + c["qi_response_source_units"]) % c["ji_fa_source_units"]
    run = (middle + c["run_response_source_units"]) % c["shuo_source_units"]
    tianzheng_mean = (winter - run) % c["ji_fa_source_units"]
    suo = c["half_year_source_units"] - run
    zraw = (middle + c["zhuan_response_source_units"] - run) % c["zhuan_end_source_units"]

    k = Decimal(sequence_index + 1)
    mean = (tianzheng_mean + k * c["shuo_source_units"]) % c["ji_fa_source_units"]

    solar_phase = (suo + k * c["shuo_source_units"]) % c["year_source_units"]
    if solar_phase > c["half_year_source_units"]:
        solar_state = "盈"
        solar_history = solar_phase - c["half_year_source_units"]
    else:
        solar_state = "缩"
        solar_history = solar_phase

    lunar_phase = (zraw + k * c["shuo_zhuan_difference_source_units"]) % c["zhuan_end_source_units"]
    if lunar_phase > c["zhuan_half_source_units"]:
        lunar_state = "迟"
        lunar_history = lunar_phase - c["zhuan_half_source_units"]
    else:
        lunar_state = "疾"
        lunar_history = lunar_phase

    solar_raw = _solar_difference(ctx, solar_state, solar_history)
    lunar_raw, divisor = _lunar_difference(ctx, lunar_state, lunar_history)
    solar_used, lunar_used = _apply_profile(profile, solar_raw, lunar_raw)

    signed = (solar_used if solar_state == "盈" else -solar_used) + (
        lunar_used if lunar_state == "迟" else -lunar_used
    )
    correction_raw = signed * Decimal("820") / divisor
    correction_used = _apply_profile(profile, solar_raw, lunar_raw, correction_raw)
    true_units = (mean + correction_used) % c["ji_fa_source_units"]
    return {
        "mean_source_units": mean,
        "solar_state": solar_state,
        "solar_difference_degree": solar_used,
        "lunar_state": lunar_state,
        "lunar_difference_degree": lunar_used,
        "d1_divisor": divisor,
        "correction_source_units": correction_used,
        "true_source_units": true_units,
        "day_index": true_units / Decimal("10000"),
    }


def validate_1578_reference(ctx: dict[str, Any]) -> int:
    matched = 0
    for item in ctx["replay"]["months"]:
        got = conjunction_for_sequence(
            ctx,
            1578,
            int(item["ordinal"]),
            PROFILE_1578_REFERENCE,
        )
        if got["true_source_units"] == Decimal(item["true_conjunction"]):
            matched += 1
    return matched


def run(root: Path) -> dict[str, Any]:
    ctx = _load(root)
    rows = ctx["fixture"]["rows"]
    counters: dict[int, int] = {}
    detail: list[dict[str, Any]] = []
    per_profile = {profile: {"in_bin": 0, "out_of_bin": 0} for profile in PROFILES}

    for row in rows:
        year = int(row["year"])
        counters[year] = counters.get(year, 0) + 1
        sequence_index = counters[year]
        lower = Decimal(str(row["lower_day_index"]))
        upper = Decimal(str(row["upper_day_index"]))
        values: dict[str, Decimal] = {}
        all_in = True
        for profile in PROFILES:
            value = conjunction_for_sequence(ctx, year, sequence_index, profile)["day_index"]
            assert isinstance(value, Decimal)
            values[profile] = value
            inside = lower <= value <= upper
            per_profile[profile]["in_bin" if inside else "out_of_bin"] += 1
            all_in = all_in and inside

        spread = max(values.values()) - min(values.values())
        edge_margin = min(min(value - lower, upper - value) for value in values.values())
        detail.append({
            "year": year,
            "month": row["month"],
            "all_profiles_in_bin": all_in,
            "spread_day": spread,
            "edge_margin_day": edge_margin,
            "values": values,
        })

    max_spread = max(detail, key=lambda item: item["spread_day"])
    min_margin = min(detail, key=lambda item: item["edge_margin_day"])
    ratio = min_margin["edge_margin_day"] / max_spread["spread_day"]

    return {
        "profile_counts": per_profile,
        "all_profiles_in_all_bins": sum(1 for item in detail if item["all_profiles_in_bin"]),
        "max_profile_spread": {
            "year": max_spread["year"],
            "month": max_spread["month"],
            "day": str(max_spread["spread_day"]),
            "seconds": str(max_spread["spread_day"] * Decimal("86400")),
        },
        "minimum_edge_margin": {
            "year": min_margin["year"],
            "month": min_margin["month"],
            "day": str(min_margin["edge_margin_day"]),
            "seconds": str(min_margin["edge_margin_day"] * Decimal("86400")),
        },
        "edge_margin_to_profile_spread_ratio": str(ratio),
        "reference_1578_exact_matches": validate_1578_reference(ctx),
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(run(root), ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

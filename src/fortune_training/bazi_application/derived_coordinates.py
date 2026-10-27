from __future__ import annotations

from typing import Any

from fortune_training.bazi_chart.registries import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    sexagenary_index,
    validate_branch,
    validate_stem,
)


DERIVED_COORDINATE_PROFILE_ID = "BAZI-DERIVED-COORDINATES-YHZP-R1"
DERIVED_COORDINATE_PROFILE_VERSION = "1.0.0"

TAIYUAN_RULE_ID = "YHZP-MONTH-STEM-PLUS-1-BRANCH-PLUS-3-R1"
TAIYUAN_SOURCE_REFS = (
    "S11:YHZP-ROOT-020-0003",
    "S11:YHZP-ROOT-020-0004",
)
TAIYUAN_ALTERNATIVE_PROFILES = (
    {
        "profile_id": "SMTH-CONCEPTION-DATE-MINUS-300-DAYS-R1",
        "status": "PRESERVED_NOT_SELECTED",
        "source_refs": ["S12:SMTH-SEG-01138"],
        "reason": "requires a separately selected conception-date doctrine",
    },
)

MINGGONG_RULE_ID = "SMTH-ZI-MONTH-REVERSE-HOUR-TO-MAO-R1"
MINGGONG_SOURCE_REFS = (
    "S12:SMTH-SEG-01154",
    "S12:SMTH-SEG-01155",
    "S11:YHZP-ROOT-023-0003",
)

SHENGONG_RULE_ID = "SHFTK-ZI-MONTH-REVERSE-HOUR-TO-YOU-R1"
SHENGONG_SOURCE_REFS = (
    "S11:SHFTK-CL-001-原-001-001",
    "S11:SHFTK-CL-001-原-001-003",
    "S11:SHFTK-CL-001-原-001-006",
)


def _ganzhi_identity(
    coordinate_type: str,
    stem: str,
    branch: str,
    *,
    rule_id: str,
    source_refs: tuple[str, ...],
    basis: dict[str, Any],
) -> dict[str, Any]:
    ganzhi = stem + branch
    return {
        "coordinate_type": coordinate_type,
        "ganzhi": ganzhi,
        "sexagenary_index": sexagenary_index(ganzhi),
        "stem": stem,
        "branch": branch,
        "rule_id": rule_id,
        "source_refs": list(source_refs),
        "basis": basis,
        "semantic_scope": "DERIVED_COORDINATE_IDENTITY_ONLY_NO_INTERPRETATION",
    }


def taiyuan_from_month_pillar(month_ganzhi: str) -> dict[str, Any]:
    if not isinstance(month_ganzhi, str) or len(month_ganzhi) != 2:
        raise ValueError("month_ganzhi must be one stem plus one branch")
    month_stem = validate_stem(month_ganzhi[0])
    month_branch = validate_branch(month_ganzhi[1])
    stem = HEAVENLY_STEMS[(HEAVENLY_STEMS.index(month_stem) + 1) % 10]
    branch = EARTHLY_BRANCHES[(EARTHLY_BRANCHES.index(month_branch) + 3) % 12]
    row = _ganzhi_identity(
        "TAIYUAN",
        stem,
        branch,
        rule_id=TAIYUAN_RULE_ID,
        source_refs=TAIYUAN_SOURCE_REFS,
        basis={
            "month_ganzhi": month_ganzhi,
            "stem_offset": 1,
            "branch_offset": 3,
        },
    )
    row["alternative_profiles"] = [dict(item) for item in TAIYUAN_ALTERNATIVE_PROFILES]
    return row


def _month_number_from_bazi_branch(month_branch: str) -> int:
    """Return 寅=1 ... 丑=12 for the Jie-based Bazi month branch."""

    validate_branch(month_branch)
    return ((EARTHLY_BRANCHES.index(month_branch) - EARTHLY_BRANCHES.index("寅")) % 12) + 1


def _palace_stem(year_stem: str, palace_branch: str) -> str:
    validate_stem(year_stem)
    validate_branch(palace_branch)
    tiger_start = (HEAVENLY_STEMS.index(year_stem) * 2 + 2) % 10
    branch_offset = (
        EARTHLY_BRANCHES.index(palace_branch) - EARTHLY_BRANCHES.index("寅")
    ) % 12
    return HEAVENLY_STEMS[(tiger_start + branch_offset) % 10]


def _birth_month_hour_palace(
    *,
    coordinate_type: str,
    year_stem: str,
    month_branch: str,
    hour_branch: str,
    target_branch: str,
    rule_id: str,
    source_refs: tuple[str, ...],
) -> dict[str, Any]:
    validate_stem(year_stem)
    validate_branch(month_branch)
    validate_branch(hour_branch)
    validate_branch(target_branch)
    month_number = _month_number_from_bazi_branch(month_branch)
    # 子上起正月，逆数至出生月。
    month_anchor_index = (-(month_number - 1)) % 12
    # 将出生时支落在月位，顺数至目标支；卯安命、酉安身。
    target_offset = (
        EARTHLY_BRANCHES.index(target_branch) - EARTHLY_BRANCHES.index(hour_branch)
    ) % 12
    palace_branch = EARTHLY_BRANCHES[(month_anchor_index + target_offset) % 12]
    palace_stem = _palace_stem(year_stem, palace_branch)
    return _ganzhi_identity(
        coordinate_type,
        palace_stem,
        palace_branch,
        rule_id=rule_id,
        source_refs=source_refs,
        basis={
            "year_stem": year_stem,
            "month_branch": month_branch,
            "month_number": month_number,
            "hour_branch": hour_branch,
            "target_branch": target_branch,
            "month_anchor_branch": EARTHLY_BRANCHES[month_anchor_index],
        },
    )


def minggong_from_pillars(
    year_ganzhi: str,
    month_ganzhi: str,
    hour_ganzhi: str,
) -> dict[str, Any]:
    sexagenary_index(year_ganzhi)
    sexagenary_index(month_ganzhi)
    sexagenary_index(hour_ganzhi)
    return _birth_month_hour_palace(
        coordinate_type="MINGGONG",
        year_stem=year_ganzhi[0],
        month_branch=month_ganzhi[1],
        hour_branch=hour_ganzhi[1],
        target_branch="卯",
        rule_id=MINGGONG_RULE_ID,
        source_refs=MINGGONG_SOURCE_REFS,
    )


def shengong_from_pillars(
    year_ganzhi: str,
    month_ganzhi: str,
    hour_ganzhi: str,
) -> dict[str, Any]:
    sexagenary_index(year_ganzhi)
    sexagenary_index(month_ganzhi)
    sexagenary_index(hour_ganzhi)
    return _birth_month_hour_palace(
        coordinate_type="SHENGONG",
        year_stem=year_ganzhi[0],
        month_branch=month_ganzhi[1],
        hour_branch=hour_ganzhi[1],
        target_branch="酉",
        rule_id=SHENGONG_RULE_ID,
        source_refs=SHENGONG_SOURCE_REFS,
    )


def derived_coordinates_for_pillars(
    year_ganzhi: str,
    month_ganzhi: str,
    hour_ganzhi: str,
) -> dict[str, Any]:
    return {
        "profile_id": DERIVED_COORDINATE_PROFILE_ID,
        "profile_version": DERIVED_COORDINATE_PROFILE_VERSION,
        "taiyuan": taiyuan_from_month_pillar(month_ganzhi),
        "minggong": minggong_from_pillars(year_ganzhi, month_ganzhi, hour_ganzhi),
        "shengong": shengong_from_pillars(year_ganzhi, month_ganzhi, hour_ganzhi),
        "semantic_scope": "DERIVED_COORDINATES_ONLY_NO_INTERPRETATION",
    }


def validate_derived_coordinate_profile() -> None:
    if taiyuan_from_month_pillar("己巳")["ganzhi"] != "庚申":
        raise ValueError("Taiyuan source example replay mismatch")
    example = derived_coordinates_for_pillars("甲子", "丙辰", "甲戌")
    if example["minggong"]["branch"] != "卯":
        raise ValueError("Minggong source example replay mismatch")
    if example["shengong"]["basis"]["target_branch"] != "酉":
        raise ValueError("Shengong target rule mismatch")


validate_derived_coordinate_profile()

from __future__ import annotations

from typing import Any

from fortune_training.bazi_chart.registries import (
    SEXAGENARY_CYCLE,
    STEM_POLARITY,
    sexagenary_index,
)
from fortune_training.bazi_temporal import BaziSex


XIAOYUN_CANDIDATE_SET_ID = "BAZI-XIAOYUN-CLASSICAL-CANDIDATES-R1"
XIAOYUN_CANDIDATE_SET_VERSION = "1.0.0"
XIAOYUN_SEMANTIC_SCOPE = "ANNUAL_COORDINATE_ONLY_NO_INTERPRETATION"

HOUR_PILLAR_PROFILE_ID = "SMTH-HOUR-PILLAR-YEAR-YINYANG-DIRECTION-R1"
HOUR_PILLAR_SOURCE_REFS = (
    "S12:SMTH-SEG-01200",
    "S12:YHZP-USR-S03778",
)

FIXED_SEX_PROFILE_ID = "SMTH-MALE-BINGYIN-FEMALE-RENSHEN-R1"
FIXED_SEX_SOURCE_REFS = ("S12:SMTH-SEG-01199",)


def _frames(start_index: int, direction: int, count: int) -> list[dict[str, Any]]:
    if count <= 0:
        raise ValueError("xiaoyun count must be positive")
    return [
        {
            "nominal_age": age,
            "ganzhi": SEXAGENARY_CYCLE[(start_index + direction * (age - 1)) % 60],
            "sexagenary_index": (start_index + direction * (age - 1)) % 60,
            "semantic_scope": XIAOYUN_SEMANTIC_SCOPE,
        }
        for age in range(1, count + 1)
    ]


def hour_pillar_xiaoyun(
    year_ganzhi: str,
    hour_ganzhi: str,
    sex: BaziSex,
    *,
    count: int,
) -> dict[str, Any]:
    sexagenary_index(year_ganzhi)
    hour_index = sexagenary_index(hour_ganzhi)
    sex = sex if isinstance(sex, BaziSex) else BaziSex(sex)
    year_is_yang = STEM_POLARITY[year_ganzhi[0]] == "YANG"
    forward = (year_is_yang and sex is BaziSex.MALE) or (
        (not year_is_yang) and sex is BaziSex.FEMALE
    )
    direction = 1 if forward else -1
    # The source example starts age one at the next/previous Ganzhi after birth.
    start_index = (hour_index + direction) % 60
    return {
        "profile_id": HOUR_PILLAR_PROFILE_ID,
        "status": "CANDIDATE_NOT_ARBITRATED",
        "direction": "FORWARD" if forward else "REVERSE",
        "basis": {
            "year_ganzhi": year_ganzhi,
            "year_stem_polarity": STEM_POLARITY[year_ganzhi[0]],
            "hour_ganzhi": hour_ganzhi,
            "sex": sex.value,
        },
        "source_refs": list(HOUR_PILLAR_SOURCE_REFS),
        "frames": _frames(start_index, direction, count),
        "semantic_scope": XIAOYUN_SEMANTIC_SCOPE,
    }


def fixed_sex_xiaoyun(
    sex: BaziSex,
    *,
    count: int,
) -> dict[str, Any]:
    sex = sex if isinstance(sex, BaziSex) else BaziSex(sex)
    if sex is BaziSex.MALE:
        start_ganzhi, direction = "丙寅", 1
    else:
        start_ganzhi, direction = "壬申", -1
    return {
        "profile_id": FIXED_SEX_PROFILE_ID,
        "status": "CANDIDATE_NOT_ARBITRATED",
        "direction": "FORWARD" if direction == 1 else "REVERSE",
        "basis": {"sex": sex.value, "age_one_ganzhi": start_ganzhi},
        "source_refs": list(FIXED_SEX_SOURCE_REFS),
        "frames": _frames(sexagenary_index(start_ganzhi), direction, count),
        "semantic_scope": XIAOYUN_SEMANTIC_SCOPE,
    }


def xiaoyun_candidates(
    year_ganzhi: str,
    hour_ganzhi: str,
    sex: BaziSex,
    *,
    count: int = 120,
) -> dict[str, Any]:
    return {
        "candidate_set_id": XIAOYUN_CANDIDATE_SET_ID,
        "candidate_set_version": XIAOYUN_CANDIDATE_SET_VERSION,
        "selection_status": "UNRESOLVED_CLASSICAL_ALTERNATIVES",
        "candidates": [
            hour_pillar_xiaoyun(year_ganzhi, hour_ganzhi, sex, count=count),
            fixed_sex_xiaoyun(sex, count=count),
        ],
        "semantic_scope": XIAOYUN_SEMANTIC_SCOPE,
    }


def validate_xiaoyun_profiles() -> None:
    hour = hour_pillar_xiaoyun("甲子", "甲子", BaziSex.MALE, count=2)
    if [row["ganzhi"] for row in hour["frames"]] != ["乙丑", "丙寅"]:
        raise ValueError("hour-pillar Xiaoyun source example replay mismatch")
    male = fixed_sex_xiaoyun(BaziSex.MALE, count=2)
    female = fixed_sex_xiaoyun(BaziSex.FEMALE, count=2)
    if [row["ganzhi"] for row in male["frames"]] != ["丙寅", "丁卯"]:
        raise ValueError("fixed male Xiaoyun source replay mismatch")
    if [row["ganzhi"] for row in female["frames"]] != ["壬申", "辛未"]:
        raise ValueError("fixed female Xiaoyun source replay mismatch")


validate_xiaoyun_profiles()

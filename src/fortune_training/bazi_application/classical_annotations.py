from __future__ import annotations

from typing import Any

from fortune_training.bazi_chart.registries import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    SEXAGENARY_CYCLE,
    STEM_POLARITY,
    sexagenary_index,
    validate_branch,
    validate_stem,
)


XUNKONG_PROFILE_ID = "BAZI-XUNKONG-YHZP-R1"
XUNKONG_PROFILE_VERSION = "1.0.0"
XUNKONG_SOURCE_REFS = ("S14:YHZP-CH-047", "S14:7.7")

TWELVE_GROWTH_PROFILE_ID = "BAZI-TWELVE-GROWTH-YIN-YANG-R1"
TWELVE_GROWTH_PROFILE_VERSION = "1.0.0"
TWELVE_GROWTH_SOURCE_REFS = (
    "S12:YHZP-CH-016",
    "S12:ZPZQ-CH-05",
    "S12:ZPZQ-R-0006",
)

TWELVE_GROWTH_PHASES = (
    "长生",
    "沐浴",
    "冠带",
    "临官",
    "帝旺",
    "衰",
    "病",
    "死",
    "墓",
    "绝",
    "胎",
    "养",
)

TWELVE_GROWTH_START_BRANCH = {
    "甲": "亥",
    "乙": "午",
    "丙": "寅",
    "丁": "酉",
    "戊": "寅",
    "己": "酉",
    "庚": "巳",
    "辛": "子",
    "壬": "申",
    "癸": "卯",
}


def xunkong_for_sexagenary_index(index: int) -> dict[str, Any]:
    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < 60:
        raise ValueError("sexagenary index must be an integer in [0, 59]")
    xun_start_index = (index // 10) * 10
    xun_start_ganzhi = SEXAGENARY_CYCLE[xun_start_index]
    start_branch_index = xun_start_index % 12
    void_branches = (
        EARTHLY_BRANCHES[(start_branch_index + 10) % 12],
        EARTHLY_BRANCHES[(start_branch_index + 11) % 12],
    )
    return {
        "profile_id": XUNKONG_PROFILE_ID,
        "profile_version": XUNKONG_PROFILE_VERSION,
        "xun_index": index // 10,
        "xun_start_ganzhi": xun_start_ganzhi,
        "void_branches": list(void_branches),
        "display_name": "".join(void_branches),
        "source_refs": list(XUNKONG_SOURCE_REFS),
        "semantic_scope": "IDENTITY_ONLY_NO_AUSPICIOUSNESS",
    }


def xunkong_for_ganzhi(ganzhi: str) -> dict[str, Any]:
    return xunkong_for_sexagenary_index(sexagenary_index(ganzhi))


def twelve_growth_for(stem: str, branch: str) -> dict[str, Any]:
    validate_stem(stem)
    validate_branch(branch)
    start = TWELVE_GROWTH_START_BRANCH[stem]
    direction = 1 if STEM_POLARITY[stem] == "YANG" else -1
    offset = (
        (EARTHLY_BRANCHES.index(branch) - EARTHLY_BRANCHES.index(start)) * direction
    ) % 12
    return {
        "profile_id": TWELVE_GROWTH_PROFILE_ID,
        "profile_version": TWELVE_GROWTH_PROFILE_VERSION,
        "source_stem": stem,
        "target_branch": branch,
        "stem_polarity": STEM_POLARITY[stem],
        "direction": "FORWARD" if direction == 1 else "REVERSE",
        "growth_start_branch": start,
        "phase_ordinal": offset,
        "phase": TWELVE_GROWTH_PHASES[offset],
        "source_refs": list(TWELVE_GROWTH_SOURCE_REFS),
        "semantic_scope": "PHASE_IDENTITY_ONLY_NO_STRENGTH_CONCLUSION",
    }


def validate_classical_annotation_registries() -> None:
    if tuple(TWELVE_GROWTH_START_BRANCH) != HEAVENLY_STEMS:
        raise ValueError("twelve-growth registry must cover ten stems in canonical order")
    if len(TWELVE_GROWTH_PHASES) != 12 or len(set(TWELVE_GROWTH_PHASES)) != 12:
        raise ValueError("twelve-growth phase registry must contain 12 unique phases")
    xunkong_pairs = {
        tuple(xunkong_for_sexagenary_index(index)["void_branches"])
        for index in range(0, 60, 10)
    }
    if xunkong_pairs != {
        ("戌", "亥"),
        ("申", "酉"),
        ("午", "未"),
        ("辰", "巳"),
        ("寅", "卯"),
        ("子", "丑"),
    }:
        raise ValueError("six-Xun void-branch registry mismatch")


validate_classical_annotation_registries()

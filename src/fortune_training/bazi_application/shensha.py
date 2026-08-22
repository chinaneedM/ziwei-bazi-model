from __future__ import annotations

from typing import Any, Mapping

from fortune_training.bazi_chart.registries import validate_branch, validate_stem


SHENSHA_PROFILE_ID = "BAZI-CLASSICAL-SHENSHA-FACTS-R1"
SHENSHA_PROFILE_VERSION = "1.0.0"
SHENSHA_CANDIDATE_SET_ID = "BAZI-SHENSHA-ANCHOR-CANDIDATES-R1"

TIANYI_BY_STEM = {
    "甲": ("丑", "未"), "乙": ("子", "申"), "丙": ("亥", "酉"),
    "丁": ("亥", "酉"), "戊": ("丑", "未"), "己": ("子", "申"),
    "庚": ("午", "寅"), "辛": ("午", "寅"), "壬": ("卯", "巳"),
    "癸": ("卯", "巳"),
}

LU_BY_STEM = {
    "甲": ("寅",), "乙": ("卯",), "丙": ("巳",), "丁": ("午",),
    "戊": ("巳",), "己": ("午",), "庚": ("申",), "辛": ("酉",),
    "壬": ("亥",), "癸": ("子",),
}

YIMA_BY_BRANCH = {
    "申": ("寅",), "子": ("寅",), "辰": ("寅",),
    "寅": ("申",), "午": ("申",), "戌": ("申",),
    "巳": ("亥",), "酉": ("亥",), "丑": ("亥",),
    "亥": ("巳",), "卯": ("巳",), "未": ("巳",),
}

HUAGAI_BY_BRANCH = {
    "寅": ("戌",), "午": ("戌",), "戌": ("戌",),
    "巳": ("丑",), "酉": ("丑",), "丑": ("丑",),
    "申": ("辰",), "子": ("辰",), "辰": ("辰",),
    "亥": ("未",), "卯": ("未",), "未": ("未",),
}

SOURCE_REFS = {
    "TIANYI": ("S11:YHZP-USR-S00235", "S11:YHZP-CH-024"),
    "LU": ("S11:YHZP-USR-S00278", "S11:YHZP-CH-034"),
    "YIMA": ("S11:YHZP-USR-S00285", "S11:YHZP-CH-035"),
    "HUAGAI": ("S11:YHZP-USR-S00296", "S11:YHZP-CH-037"),
}


def _pillar_parts(pillar_ganzhi: Mapping[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    if set(pillar_ganzhi) != {"YEAR", "MONTH", "DAY", "HOUR"}:
        raise ValueError("pillar_ganzhi must contain YEAR, MONTH, DAY and HOUR")
    stems: dict[str, str] = {}
    branches: dict[str, str] = {}
    for position in ("YEAR", "MONTH", "DAY", "HOUR"):
        ganzhi = pillar_ganzhi[position]
        if not isinstance(ganzhi, str) or len(ganzhi) != 2:
            raise ValueError(f"invalid pillar Ganzhi: {position}")
        validate_stem(ganzhi[0])
        validate_branch(ganzhi[1])
        stems[position] = ganzhi[0]
        branches[position] = ganzhi[1]
    return stems, branches


def _candidate(
    shensha_id: str,
    display_name: str,
    anchor_basis: str,
    anchor_value: str,
    target_branches: tuple[str, ...],
    pillar_ganzhi: Mapping[str, str],
) -> dict[str, Any]:
    occurrences = [
        {
            "pillar_position": position,
            "pillar_ganzhi": pillar_ganzhi[position],
            "matched_branch": pillar_ganzhi[position][1],
        }
        for position in ("YEAR", "MONTH", "DAY", "HOUR")
        if pillar_ganzhi[position][1] in target_branches
    ]
    return {
        "candidate_id": f"{shensha_id}:{anchor_basis}:{anchor_value}",
        "shensha_id": shensha_id,
        "display_name": display_name,
        "anchor_basis": anchor_basis,
        "anchor_value": anchor_value,
        "target_branches": list(target_branches),
        "occurrences": occurrences,
        "present": bool(occurrences),
        "selection_status": "CANDIDATE_NOT_ARBITRATED",
        "source_refs": list(SOURCE_REFS[shensha_id]),
        "semantic_scope": "IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS",
    }


def classical_shensha_for_pillars(pillar_ganzhi: Mapping[str, str]) -> dict[str, Any]:
    """Return source-bound ShenSha matches while preserving anchor alternatives."""

    stems, branches = _pillar_parts(pillar_ganzhi)
    definitions = (
        ("TIANYI", "天乙贵人", "STEM", TIANYI_BY_STEM, ("DAY_STEM", "YEAR_STEM")),
        ("LU", "禄神", "STEM", LU_BY_STEM, ("DAY_STEM", "YEAR_STEM")),
        ("YIMA", "驿马", "BRANCH", YIMA_BY_BRANCH, ("DAY_BRANCH", "YEAR_BRANCH")),
        ("HUAGAI", "华盖", "BRANCH", HUAGAI_BY_BRANCH, ("DAY_BRANCH", "YEAR_BRANCH")),
    )
    candidates: list[dict[str, Any]] = []
    for shensha_id, display_name, kind, registry, bases in definitions:
        for basis in bases:
            position = basis.split("_")[0]
            anchor = stems[position] if kind == "STEM" else branches[position]
            candidates.append(
                _candidate(
                    shensha_id,
                    display_name,
                    basis,
                    anchor,
                    registry[anchor],
                    pillar_ganzhi,
                )
            )
    return {
        "profile_id": SHENSHA_PROFILE_ID,
        "profile_version": SHENSHA_PROFILE_VERSION,
        "candidate_set_id": SHENSHA_CANDIDATE_SET_ID,
        "resolution_status": "UNRESOLVED_CLASSICAL_ANCHOR_ALTERNATIVES",
        "candidates": candidates,
        "selection_semantics": "NO_WINNER_NO_IMPLICIT_MERGE",
        "semantic_scope": "FACTS_ONLY_NO_INTERPRETATION",
    }


def validate_shensha_registries() -> None:
    if set(TIANYI_BY_STEM) != set(LU_BY_STEM) or len(TIANYI_BY_STEM) != 10:
        raise ValueError("stem ShenSha registries must cover ten stems")
    if set(YIMA_BY_BRANCH) != set(HUAGAI_BY_BRANCH) or len(YIMA_BY_BRANCH) != 12:
        raise ValueError("branch ShenSha registries must cover twelve branches")
    for registry in (TIANYI_BY_STEM, LU_BY_STEM, YIMA_BY_BRANCH, HUAGAI_BY_BRANCH):
        for targets in registry.values():
            if not targets:
                raise ValueError("ShenSha target registry must not be empty")
            for target in targets:
                validate_branch(target)


validate_shensha_registries()

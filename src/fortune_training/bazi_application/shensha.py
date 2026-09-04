from __future__ import annotations

from typing import Any, Mapping, Sequence

from fortune_training.bazi_chart.registries import (
    EARTHLY_BRANCHES,
    SEXAGENARY_CYCLE,
    validate_branch,
    validate_stem,
)

from .classical_annotations import twelve_growth_for


SHENSHA_PROFILE_ID = "BAZI-CLASSICAL-SHENSHA-FACTS-R1"
SHENSHA_PROFILE_VERSION = "1.7.0"
SHENSHA_CANDIDATE_SET_ID = "BAZI-SHENSHA-ANCHOR-CANDIDATES-R1"
POSITIONS = ("YEAR", "MONTH", "DAY", "HOUR")

TIANYI_BY_STEM = {
    "甲": ("丑", "未"), "乙": ("子", "申"), "丙": ("亥", "酉"),
    "丁": ("亥", "酉"), "戊": ("丑", "未"), "己": ("子", "申"),
    "庚": ("午", "寅"), "辛": ("午", "寅"), "壬": ("卯", "巳"),
    "癸": ("卯", "巳"),
}
# S11:YHZP-CH-025 explicitly says to anchor this rule on the birth-year stem.
TIANGUAN_BY_YEAR_STEM = {
    "甲": ("未",), "乙": ("辰",), "丙": ("巳",), "丁": ("酉",),
    "戊": ("戌",), "己": ("卯",), "庚": ("亥",), "辛": ("申",),
    "壬": ("寅",), "癸": ("午",),
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
YUEDE_BY_MONTH_BRANCH = {
    "寅": ("丙",), "午": ("丙",), "戌": ("丙",),
    "申": ("壬",), "子": ("壬",), "辰": ("壬",),
    "亥": ("甲",), "卯": ("甲",), "未": ("甲",),
    "巳": ("庚",), "酉": ("庚",), "丑": ("庚",),
}
YUEDEHE_BY_MONTH_BRANCH = {
    "寅": ("辛",), "午": ("辛",), "戌": ("辛",),
    "申": ("丁",), "子": ("丁",), "辰": ("丁",),
    "亥": ("己",), "卯": ("己",), "未": ("己",),
    "巳": ("乙",), "酉": ("乙",), "丑": ("乙",),
}
# The verse alternates a heavenly stem and an earthly branch by lunar month.
TIANDE_BY_MONTH_BRANCH = {
    "寅": ("STEM", "丁"), "卯": ("BRANCH", "申"),
    "辰": ("STEM", "壬"), "巳": ("STEM", "辛"),
    "午": ("BRANCH", "亥"), "未": ("STEM", "甲"),
    "申": ("STEM", "癸"), "酉": ("BRANCH", "寅"),
    "戌": ("STEM", "丙"), "亥": ("STEM", "乙"),
    "子": ("BRANCH", "巳"), "丑": ("STEM", "庚"),
}
# Zodiac-palace wording in S11 resolves to the food-god's Lu branch.
TIANCHU_BY_STEM = {
    "甲": ("巳",), "乙": ("午",), "丙": ("巳",), "丁": ("午",),
    "戊": ("申",), "己": ("酉",), "庚": ("亥",), "辛": ("子",),
    "壬": ("寅",), "癸": ("卯",),
}
FUXING_BY_STEM = {
    "甲": ("寅", "子"), "乙": ("丑", "卯"),
    "丙": ("寅", "子", "戌"), "丁": ("亥", "酉"),
    "戊": ("申",), "己": ("未",), "庚": ("午",),
    "辛": ("巳",), "壬": ("辰",), "癸": ("丑", "卯"),
}
TAIJI_BY_YEAR_STEM = {
    "甲": ("子", "午"), "乙": ("子", "午"),
    "丙": ("酉", "卯"), "丁": ("酉", "卯"),
    "戊": ("辰", "戌", "丑", "未"), "己": ("辰", "戌", "丑", "未"),
    "庚": ("寅", "亥"), "辛": ("寅", "亥"),
    "壬": ("巳", "申"), "癸": ("巳", "申"),
}
SANQI_STEM_SEQUENCES = {
    "HEAVEN": ("甲", "戊", "庚"),
    "EARTH": ("乙", "丙", "丁"),
    "HUMAN": ("壬", "癸", "辛"),
}
TIANSHE_BY_MONTH_BRANCH = {
    "寅": "戊寅", "卯": "戊寅", "辰": "戊寅",
    "巳": "甲午", "午": "甲午", "未": "甲午",
    "申": "戊申", "酉": "戊申", "戌": "戊申",
    "亥": "甲子", "子": "甲子", "丑": "甲子",
}
XUETANG_BY_NAYIN_ELEMENT = {
    "金": ("巳", "辛巳"), "木": ("亥", "己亥"),
    "水": ("申", "甲申"), "土": ("申", "戊申"),
    "火": ("寅", "丙寅"),
}
NAYIN_ELEMENTS_BY_PAIR = (
    "金", "火", "木", "土", "金", "火", "水", "土", "金", "木",
    "水", "土", "火", "木", "水", "金", "火", "木", "土", "金",
    "火", "水", "土", "金", "木", "水", "土", "火", "木", "水",
)
NAYIN_ELEMENT_BY_GANZHI = {
    ganzhi: NAYIN_ELEMENTS_BY_PAIR[index // 2]
    for index, ganzhi in enumerate(SEXAGENARY_CYCLE)
}
JINYU_BY_STEM = {
    stem: (EARTHLY_BRANCHES[(EARTHLY_BRANCHES.index(branches[0]) + 2) % 12],)
    for stem, branches in LU_BY_STEM.items()
}
# S14's YHZP-CH-007 relation fact table preserves the exact six Liuhe pairs.
LIUHE_PAIRS = (
    ("子", "丑"), ("寅", "亥"), ("卯", "戌"),
    ("辰", "酉"), ("巳", "申"), ("午", "未"),
)
LIUHE_PARTNER_BY_BRANCH = {
    branch: partner
    for left, right in LIUHE_PAIRS
    for branch, partner in ((left, right), (right, left))
}
# S11:YHZP-CH-043 gives Jia/Yi examples and explicitly says "其余仿此".
# The base identity is the Liuhe partner of the source-bound Lu branch.
ANLU_BY_STEM = {
    stem: (LIUHE_PARTNER_BY_BRANCH[branches[0]],)
    for stem, branches in LU_BY_STEM.items()
}
# S11:YHZP-CH-044 gives Jia/Yi examples and explicitly says "其他仿此".
# The pair is therefore generated mechanically from the two cyclic neighbours
# of each stem's source-bound Lu branch; no auspiciousness semantics are added.
JIALU_BY_STEM = {
    stem: (
        EARTHLY_BRANCHES[(EARTHLY_BRANCHES.index(branches[0]) - 1) % 12],
        EARTHLY_BRANCHES[(EARTHLY_BRANCHES.index(branches[0]) + 1) % 12],
    )
    for stem, branches in LU_BY_STEM.items()
}
# S11:YHZP-CH-041 explicitly closes this set: only these four reciprocal cases.
GONGLU_BY_GANZHI = {
    "戊辰": ("丙午",),
    "丙午": ("戊辰",),
    "丁巳": ("己未",),
    "己未": ("丁巳",),
}
# S11 identifies Yangren as the Yang stem's blade and supplies these examples.
YANGREN_BY_STEM = {
    "甲": ("卯",), "丙": ("午",), "戊": ("午",),
    "庚": ("酉",), "壬": ("子",),
}
# S11:YHZP-USR-S00378..S00388 explicitly enumerates Feiren for all ten stems.
# Keep this table independent from Yangren runtime derivation so its provenance
# and future candidate evolution remain isolated.
FEIREN_BRANCH_BY_STEM = {
    "甲": ("酉",), "乙": ("戌",), "丙": ("子",), "丁": ("丑",),
    "戊": ("子",), "己": ("丑",), "庚": ("卯",), "辛": ("辰",),
    "壬": ("午",), "癸": ("未",),
}

SOURCE_REFS = {
    "TIANYI": ("S11:YHZP-USR-S00235", "S11:YHZP-CH-024"),
    "TIANGUAN": ("S11:YHZP-USR-S00240", "S11:YHZP-CH-025"),
    "LU": ("S11:YHZP-USR-S00278", "S11:YHZP-CH-034"),
    "YIMA": ("S11:YHZP-USR-S00285", "S11:YHZP-CH-035"),
    "HUAGAI": ("S11:YHZP-USR-S00296", "S11:YHZP-CH-037"),
    "YUEDE": ("S11:YHZP-USR-S00255", "S11:YHZP-USR-S00256", "S11:YHZP-CH-028"),
    "YUEDEHE": ("S11:YHZP-USR-S00262", "S11:YHZP-CH-029"),
    "TIANDE": ("S11:YHZP-USR-S00264", "S11:YHZP-USR-S00265", "S11:YHZP-CH-030"),
    "TIANCHU": ("S11:YHZP-USR-S00268", "S11:YHZP-USR-S00304", "S11:YHZP-CH-031"),
    "FUXING": ("S11:YHZP-USR-S00272", "S11:YHZP-CH-032"),
    "TAIJI": ("S11:YHZP-USR-S00243", "S11:YHZP-USR-S00244", "S11:YHZP-CH-026"),
    "SANQI": ("S11:YHZP-USR-S00248", "S11:YHZP-USR-S00249", "S11:YHZP-USR-S00251", "S11:YHZP-CH-027"),
    "TIANSHE": ("S11:YHZP-USR-S00293", "S11:YHZP-CH-036"),
    "XUETANG": ("S11:YHZP-USR-S00301", "S11:YHZP-CH-014", "S11:YHZP-CH-038"),
    "JINYU": ("S11:YHZP-USR-S00312", "S11:YHZP-USR-S00278", "S11:YHZP-CH-040"),
    "ANLU": (
        "S11:YHZP-USR-S00324", "S11:YHZP-USR-S00278",
        "S11:YHZP-CH-043", "S11:YHZP-CH-034", "S14:YHZP-CH-007",
    ),
    "JIALU": (
        "S11:YHZP-USR-S00327", "S11:YHZP-USR-S00278",
        "S11:YHZP-CH-044", "S11:YHZP-CH-034",
    ),
    "GONGLU": (
        "S11:YHZP-USR-S00315", "S11:YHZP-USR-S00316",
        "S11:YHZP-USR-S00317", "S11:YHZP-CH-041",
    ),
    "YUANCHENG": (
        "S11:YHZP-USR-S00330", "S11:YHZP-CH-045",
        "S12:YHZP-CH-016", "S11:YHZP-USR-S00285", "S14:YHZP-CH-007",
    ),
    "YANGREN": ("S11:YHZP-USR-S00282", "S11:YHZP-USR-S02740", "S11:YHZP-CH-224"),
    "FEIREN": (
        "S11:YHZP-USR-S00378", "S11:YHZP-USR-S00379", "S11:YHZP-USR-S00380",
        "S11:YHZP-USR-S00381", "S11:YHZP-USR-S00382", "S11:YHZP-USR-S00383",
        "S11:YHZP-USR-S00384", "S11:YHZP-USR-S00385", "S11:YHZP-USR-S00386",
        "S11:YHZP-USR-S00387", "S11:YHZP-USR-S00388",
    ),
}


def _pillar_parts(pillar_ganzhi: Mapping[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    if set(pillar_ganzhi) != set(POSITIONS):
        raise ValueError("pillar_ganzhi must contain YEAR, MONTH, DAY and HOUR")
    stems: dict[str, str] = {}
    branches: dict[str, str] = {}
    for position in POSITIONS:
        ganzhi = pillar_ganzhi[position]
        if not isinstance(ganzhi, str) or len(ganzhi) != 2:
            raise ValueError(f"invalid pillar Ganzhi: {position}")
        validate_stem(ganzhi[0])
        validate_branch(ganzhi[1])
        if ganzhi not in NAYIN_ELEMENT_BY_GANZHI:
            raise ValueError(f"invalid sexagenary pillar Ganzhi: {position}")
        stems[position] = ganzhi[0]
        branches[position] = ganzhi[1]
    return stems, branches


def _positions_for_scope(scope: str) -> tuple[str, ...]:
    if scope == "ALL_PILLARS":
        return POSITIONS
    if scope.startswith("ONLY_") and scope[5:] in POSITIONS:
        return (scope[5:],)
    raise ValueError(f"unsupported ShenSha match scope: {scope}")


def _candidate(
    shensha_id: str,
    display_name: str,
    anchor_basis: str,
    anchor_value: str,
    target_kind: str,
    target_values: Sequence[str],
    pillar_ganzhi: Mapping[str, str],
    *,
    match_scope: str = "ALL_PILLARS",
    selection_status: str = "SOURCE_EXPLICIT",
    qualification_status: str = "NOT_APPLICABLE",
) -> dict[str, Any]:
    occurrences: list[dict[str, Any]] = []
    for position in _positions_for_scope(match_scope):
        ganzhi = pillar_ganzhi[position]
        value = (
            ganzhi[0] if target_kind == "STEM"
            else ganzhi[1] if target_kind == "BRANCH"
            else ganzhi
        )
        if value in target_values:
            row = {
                "pillar_position": position,
                "pillar_ganzhi": ganzhi,
                "matched_value": value,
            }
            if target_kind == "BRANCH":
                row["matched_branch"] = value
            occurrences.append(row)
    return {
        "candidate_id": f"{shensha_id}:{anchor_basis}:{anchor_value}:{match_scope}",
        "shensha_id": shensha_id,
        "display_name": display_name,
        "anchor_basis": anchor_basis,
        "anchor_value": anchor_value,
        "target_kind": target_kind,
        "target_values": list(target_values),
        "target_branches": list(target_values) if target_kind == "BRANCH" else [],
        "match_scope": match_scope,
        "occurrences": occurrences,
        "present": bool(occurrences),
        "selection_status": selection_status,
        "qualification_status": qualification_status,
        "source_refs": list(SOURCE_REFS[shensha_id]),
        "semantic_scope": "IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS",
    }


def _branch_pair_candidate(
    shensha_id: str,
    display_name: str,
    anchor_basis: str,
    anchor_value: str,
    target_branches: Sequence[str],
    pillar_ganzhi: Mapping[str, str],
    *,
    selection_status: str = "CANDIDATE_NOT_ARBITRATED",
) -> dict[str, Any]:
    required = tuple(target_branches)
    if len(required) != 2 or len(set(required)) != 2:
        raise ValueError("branch-pair ShenSha requires two distinct target branches")
    for branch in required:
        validate_branch(branch)

    matched_positions = [
        position for position in POSITIONS
        if pillar_ganzhi[position][1] in required
    ]
    matched_branches = {pillar_ganzhi[position][1] for position in matched_positions}
    present = matched_branches == set(required)
    occurrences: list[dict[str, Any]] = []
    if present:
        occurrences.append({
            "pillar_positions": matched_positions,
            "pillar_ganzhi": [pillar_ganzhi[position] for position in matched_positions],
            "matched_value": "".join(required),
            "matched_branches": list(required),
        })
    return {
        "candidate_id": f"{shensha_id}:{anchor_basis}:{anchor_value}:ALL_PILLARS",
        "shensha_id": shensha_id,
        "display_name": display_name,
        "anchor_basis": anchor_basis,
        "anchor_value": anchor_value,
        "target_kind": "BRANCH_PAIR",
        "target_values": list(required),
        "target_branches": list(required),
        "match_scope": "ALL_PILLARS",
        "occurrences": occurrences,
        "present": present,
        "selection_status": selection_status,
        "qualification_status": "BOTH_TARGET_BRANCHES_REQUIRED",
        "source_refs": list(SOURCE_REFS[shensha_id]),
        "semantic_scope": "IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS",
    }


def _stem_anchor_candidates(
    shensha_id: str,
    display_name: str,
    registry: Mapping[str, Sequence[str]],
    stems: Mapping[str, str],
    pillar_ganzhi: Mapping[str, str],
) -> list[dict[str, Any]]:
    rows = []
    for basis in ("DAY_STEM", "YEAR_STEM"):
        position = basis.split("_")[0]
        anchor = stems[position]
        rows.append(
            _candidate(
                shensha_id, display_name, basis, anchor, "BRANCH",
                registry.get(anchor, ()), pillar_ganzhi,
                selection_status="CANDIDATE_NOT_ARBITRATED",
            )
        )
    return rows


def _anlu_candidates(
    stems: Mapping[str, str],
    pillar_ganzhi: Mapping[str, str],
) -> list[dict[str, Any]]:
    visible_branches = {pillar_ganzhi[position][1] for position in POSITIONS}
    rows: list[dict[str, Any]] = []
    for basis in ("DAY_STEM", "YEAR_STEM"):
        position = basis.split("_")[0]
        anchor = stems[position]
        direct_lu_branch = LU_BY_STEM[anchor][0]
        qualification_status = (
            "COMMENTARY_NO_VISIBLE_ANCHOR_LU:SATISFIED"
            if direct_lu_branch not in visible_branches
            else "COMMENTARY_NO_VISIBLE_ANCHOR_LU:NOT_SATISFIED"
        )
        rows.append(
            _candidate(
                "ANLU", "暗禄", basis, anchor, "BRANCH", ANLU_BY_STEM[anchor],
                pillar_ganzhi,
                selection_status="CANDIDATE_NOT_ARBITRATED",
                qualification_status=qualification_status,
            )
        )
    return rows


def _stem_pair_anchor_candidates(
    shensha_id: str,
    display_name: str,
    registry: Mapping[str, Sequence[str]],
    stems: Mapping[str, str],
    pillar_ganzhi: Mapping[str, str],
) -> list[dict[str, Any]]:
    rows = []
    for basis in ("DAY_STEM", "YEAR_STEM"):
        position = basis.split("_")[0]
        anchor = stems[position]
        rows.append(
            _branch_pair_candidate(
                shensha_id, display_name, basis, anchor,
                registry[anchor], pillar_ganzhi,
            )
        )
    return rows


def _branch_anchor_candidates(
    shensha_id: str,
    display_name: str,
    registry: Mapping[str, Sequence[str]],
    branches: Mapping[str, str],
    pillar_ganzhi: Mapping[str, str],
) -> list[dict[str, Any]]:
    rows = []
    for basis in ("DAY_BRANCH", "YEAR_BRANCH"):
        position = basis.split("_")[0]
        anchor = branches[position]
        rows.append(
            _candidate(
                shensha_id, display_name, basis, anchor, "BRANCH", registry[anchor],
                pillar_ganzhi, selection_status="CANDIDATE_NOT_ARBITRATED",
            )
        )
    return rows


def _ganzhi_anchor_candidates(
    shensha_id: str,
    display_name: str,
    registry: Mapping[str, Sequence[str]],
    pillar_ganzhi: Mapping[str, str],
) -> list[dict[str, Any]]:
    rows = []
    for basis in ("DAY_GANZHI", "YEAR_GANZHI"):
        position = basis.split("_")[0]
        anchor = pillar_ganzhi[position]
        rows.append(
            _candidate(
                shensha_id, display_name, basis, anchor, "GANZHI",
                registry.get(anchor, ()), pillar_ganzhi,
                selection_status="CANDIDATE_NOT_ARBITRATED",
            )
        )
    return rows


def _yuancheng_candidate(
    stems: Mapping[str, str],
    branches: Mapping[str, str],
    pillar_ganzhi: Mapping[str, str],
) -> dict[str, Any]:
    day_stem = stems["DAY"]
    day_branch = branches["DAY"]
    hour_branch = branches["HOUR"]
    growth = twelve_growth_for(day_stem, hour_branch)
    growth_branch = str(growth["growth_start_branch"])
    yima_branch = YIMA_BY_BRANCH[day_branch][0]
    liuhe_partner = LIUHE_PARTNER_BY_BRANCH[hour_branch]
    present = growth["phase"] == "长生" and liuhe_partner == yima_branch
    occurrences: list[dict[str, Any]] = []
    if present:
        occurrences.append({
            "pillar_position": "HOUR",
            "pillar_ganzhi": pillar_ganzhi["HOUR"],
            "matched_value": hour_branch,
            "matched_branch": hour_branch,
            "day_stem_growth_start_branch": growth_branch,
            "day_branch_yima_branch": yima_branch,
            "liuhe_pair": [hour_branch, yima_branch],
        })
    return {
        "candidate_id": f"YUANCHENG:DAY_GANZHI:{pillar_ganzhi['DAY']}:ONLY_HOUR",
        "shensha_id": "YUANCHENG",
        "display_name": "垣城",
        "anchor_basis": "DAY_GANZHI",
        "anchor_value": pillar_ganzhi["DAY"],
        "target_kind": "HOUR_BRANCH_LONGSHENG_LIUHE_YIMA",
        "target_values": [growth_branch, yima_branch],
        "target_branches": [growth_branch, yima_branch],
        "match_scope": "ONLY_HOUR_WITH_DERIVED_LIUHE",
        "occurrences": occurrences,
        "present": present,
        "selection_status": "SOURCE_EXPLICIT",
        "qualification_status": "BASE_IDENTITY_ONLY_INTERPRETATION_EXCLUDED",
        "source_refs": list(SOURCE_REFS["YUANCHENG"]),
        "semantic_scope": "IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS",
    }


def _sanqi_candidates(stems: Mapping[str, str], pillar_ganzhi: Mapping[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    windows = (("YEAR", "MONTH", "DAY"), ("MONTH", "DAY", "HOUR"))
    for family, sequence in SANQI_STEM_SEQUENCES.items():
        occurrences = []
        for positions in windows:
            values = tuple(stems[position] for position in positions)
            if values == sequence:
                occurrences.append({
                    "pillar_positions": list(positions),
                    "pillar_ganzhi": [pillar_ganzhi[position] for position in positions],
                    "matched_value": "".join(values),
                })
        rows.append({
            "candidate_id": f"SANQI:PILLAR_STEM_SEQUENCE:{family}",
            "shensha_id": "SANQI",
            "display_name": "三奇贵人",
            "anchor_basis": "PILLAR_STEM_SEQUENCE",
            "anchor_value": family,
            "target_kind": "STEM_SEQUENCE",
            "target_values": ["".join(sequence)],
            "target_branches": [],
            "match_scope": "CONSECUTIVE_THREE_PILLARS",
            "occurrences": occurrences,
            "present": bool(occurrences),
            "selection_status": "SOURCE_EXPLICIT",
            "qualification_status": "BASE_SEQUENCE_ONLY_AUXILIARY_CONDITIONS_NOT_ARBITRATED",
            "source_refs": list(SOURCE_REFS["SANQI"]),
            "semantic_scope": "IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS",
        })
    return rows


def classical_shensha_for_pillars(pillar_ganzhi: Mapping[str, str]) -> dict[str, Any]:
    """Return source-bound ShenSha matches while preserving rule alternatives."""

    stems, branches = _pillar_parts(pillar_ganzhi)
    candidates: list[dict[str, Any]] = []
    candidates.extend(_stem_anchor_candidates("TIANYI", "天乙贵人", TIANYI_BY_STEM, stems, pillar_ganzhi))
    candidates.append(_candidate(
        "TIANGUAN", "天官贵人", "YEAR_STEM", stems["YEAR"], "BRANCH",
        TIANGUAN_BY_YEAR_STEM[stems["YEAR"]], pillar_ganzhi,
    ))
    candidates.extend(_stem_anchor_candidates("LU", "禄神", LU_BY_STEM, stems, pillar_ganzhi))
    candidates.extend(_branch_anchor_candidates("YIMA", "驿马", YIMA_BY_BRANCH, branches, pillar_ganzhi))
    candidates.extend(_branch_anchor_candidates("HUAGAI", "华盖", HUAGAI_BY_BRANCH, branches, pillar_ganzhi))

    month_branch = branches["MONTH"]
    candidates.append(_candidate(
        "YUEDE", "月德贵人", "MONTH_BRANCH", month_branch, "STEM",
        YUEDE_BY_MONTH_BRANCH[month_branch], pillar_ganzhi, match_scope="ONLY_DAY",
    ))
    # 月德合原文未限定落柱，日干法与四干扫描法分列，禁止合并。
    for scope in ("ONLY_DAY", "ALL_PILLARS"):
        candidates.append(_candidate(
            "YUEDEHE", "月德合", "MONTH_BRANCH", month_branch, "STEM",
            YUEDEHE_BY_MONTH_BRANCH[month_branch], pillar_ganzhi,
            match_scope=scope, selection_status="CANDIDATE_NOT_ARBITRATED",
        ))
    tiande_kind, tiande_value = TIANDE_BY_MONTH_BRANCH[month_branch]
    candidates.append(_candidate(
        "TIANDE", "天德贵人", "MONTH_BRANCH", month_branch, tiande_kind,
        (tiande_value,), pillar_ganzhi,
    ))
    candidates.extend(_stem_anchor_candidates("TIANCHU", "天厨贵人", TIANCHU_BY_STEM, stems, pillar_ganzhi))
    candidates.extend(_stem_anchor_candidates("FUXING", "福星贵人", FUXING_BY_STEM, stems, pillar_ganzhi))
    candidates.append(_candidate(
        "TAIJI", "太极贵人", "YEAR_STEM", stems["YEAR"], "BRANCH",
        TAIJI_BY_YEAR_STEM[stems["YEAR"]], pillar_ganzhi,
    ))
    candidates.extend(_sanqi_candidates(stems, pillar_ganzhi))
    candidates.append(_candidate(
        "TIANSHE", "天赦", "MONTH_BRANCH_SEASON", month_branch, "GANZHI",
        (TIANSHE_BY_MONTH_BRANCH[month_branch],), pillar_ganzhi, match_scope="ONLY_DAY",
    ))
    for position in ("YEAR", "DAY"):
        ganzhi = pillar_ganzhi[position]
        nayin_element = NAYIN_ELEMENT_BY_GANZHI[ganzhi]
        target_branch, exact_ganzhi = XUETANG_BY_NAYIN_ELEMENT[nayin_element]
        candidates.append(_candidate(
            "XUETANG", "十干学堂", f"{position}_NAYIN_ELEMENT", nayin_element,
            "BRANCH", (target_branch,), pillar_ganzhi,
            selection_status="CANDIDATE_NOT_ARBITRATED",
            qualification_status=f"ORTHODOX_GANZHI:{exact_ganzhi}",
        ))
    candidates.extend(_stem_anchor_candidates("JINYU", "金舆禄", JINYU_BY_STEM, stems, pillar_ganzhi))
    candidates.extend(_anlu_candidates(stems, pillar_ganzhi))
    candidates.extend(_stem_pair_anchor_candidates("JIALU", "夹禄", JIALU_BY_STEM, stems, pillar_ganzhi))
    candidates.extend(_ganzhi_anchor_candidates("GONGLU", "拱禄", GONGLU_BY_GANZHI, pillar_ganzhi))
    candidates.append(_yuancheng_candidate(stems, branches, pillar_ganzhi))
    candidates.extend(_stem_anchor_candidates("YANGREN", "羊刃", YANGREN_BY_STEM, stems, pillar_ganzhi))
    candidates.extend(_stem_anchor_candidates("FEIREN", "飞刃", FEIREN_BRANCH_BY_STEM, stems, pillar_ganzhi))

    return {
        "profile_id": SHENSHA_PROFILE_ID,
        "profile_version": SHENSHA_PROFILE_VERSION,
        "candidate_set_id": SHENSHA_CANDIDATE_SET_ID,
        "resolution_status": "UNRESOLVED_CLASSICAL_ANCHOR_ALTERNATIVES",
        "candidates": candidates,
        "selection_semantics": "NO_WINNER_NO_IMPLICIT_MERGE",
        "semantic_scope": "FACTS_ONLY_NO_INTERPRETATION",
    }


def _validate_registry(
    registry: Mapping[str, Sequence[str]], keys: set[str], target_kind: str
) -> None:
    if set(registry) != keys:
        raise ValueError(f"{target_kind} ShenSha registry coverage mismatch")
    validator = validate_stem if target_kind == "stem" else validate_branch
    for targets in registry.values():
        if not targets:
            raise ValueError("ShenSha target registry must not be empty")
        for target in targets:
            validator(target)


def validate_shensha_registries() -> None:
    stems = set("甲乙丙丁戊己庚辛壬癸")
    branches = set(EARTHLY_BRANCHES)
    for registry in (
        TIANYI_BY_STEM, TIANGUAN_BY_YEAR_STEM, LU_BY_STEM, TIANCHU_BY_STEM,
        FUXING_BY_STEM, TAIJI_BY_YEAR_STEM, JINYU_BY_STEM, ANLU_BY_STEM,
        JIALU_BY_STEM, FEIREN_BRANCH_BY_STEM,
    ):
        _validate_registry(registry, stems, "branch")
    if set(LIUHE_PARTNER_BY_BRANCH) != branches:
        raise ValueError("Liuhe partner registry must cover all twelve branches")
    for branch, partner in LIUHE_PARTNER_BY_BRANCH.items():
        validate_branch(partner)
        if partner == branch or LIUHE_PARTNER_BY_BRANCH.get(partner) != branch:
            raise ValueError("Liuhe partner registry must be reciprocal without self-pairs")
    if {
        frozenset((branch, partner))
        for branch, partner in LIUHE_PARTNER_BY_BRANCH.items()
    } != {frozenset(pair) for pair in LIUHE_PAIRS}:
        raise ValueError("Liuhe partner registry must preserve the six source pairs")
    for stem, lu_targets in LU_BY_STEM.items():
        if len(lu_targets) != 1:
            raise ValueError("Lu registry must remain single-branch per stem")
        expected_anlu = (LIUHE_PARTNER_BY_BRANCH[lu_targets[0]],)
        if ANLU_BY_STEM.get(stem) != expected_anlu:
            raise ValueError("Anlu registry must be the Liuhe partner of Lu")
        lu_index = EARTHLY_BRANCHES.index(lu_targets[0])
        expected_pair = (
            EARTHLY_BRANCHES[(lu_index - 1) % 12],
            EARTHLY_BRANCHES[(lu_index + 1) % 12],
        )
        if JIALU_BY_STEM.get(stem) != expected_pair:
            raise ValueError("Jialu registry must be the two cyclic neighbours of Lu")
        if len(set(JIALU_BY_STEM[stem])) != 2:
            raise ValueError("Jialu registry must contain two distinct branches")
    _validate_registry(YANGREN_BY_STEM, set("甲丙戊庚壬"), "branch")
    for registry in (YIMA_BY_BRANCH, HUAGAI_BY_BRANCH):
        _validate_registry(registry, branches, "branch")
    for registry in (YUEDE_BY_MONTH_BRANCH, YUEDEHE_BY_MONTH_BRANCH):
        _validate_registry(registry, branches, "stem")
    if set(TIANDE_BY_MONTH_BRANCH) != branches or set(TIANSHE_BY_MONTH_BRANCH) != branches:
        raise ValueError("month ShenSha registries must cover twelve branches")
    if set(NAYIN_ELEMENT_BY_GANZHI) != set(SEXAGENARY_CYCLE):
        raise ValueError("Nayin registry must cover the sexagenary cycle")
    if set(XUETANG_BY_NAYIN_ELEMENT) != set("金木水火土"):
        raise ValueError("Xuetang registry must cover five Nayin elements")
    for kind, value in TIANDE_BY_MONTH_BRANCH.values():
        (validate_stem if kind == "STEM" else validate_branch)(value)
    for ganzhi in TIANSHE_BY_MONTH_BRANCH.values():
        if ganzhi not in NAYIN_ELEMENT_BY_GANZHI:
            raise ValueError(f"invalid Tianshe Ganzhi: {ganzhi}")
    expected_gonglu = {"戊辰", "丙午", "丁巳", "己未"}
    if set(GONGLU_BY_GANZHI) != expected_gonglu:
        raise ValueError("Gonglu registry must preserve the four source-explicit cases")
    for anchor, targets in GONGLU_BY_GANZHI.items():
        if anchor not in NAYIN_ELEMENT_BY_GANZHI or len(targets) != 1:
            raise ValueError("invalid Gonglu anchor or target cardinality")
        target = targets[0]
        if target not in NAYIN_ELEMENT_BY_GANZHI or GONGLU_BY_GANZHI.get(target) != (anchor,):
            raise ValueError("Gonglu registry must be reciprocal and sexagenary-valid")


validate_shensha_registries()
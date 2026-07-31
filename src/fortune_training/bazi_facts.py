from __future__ import annotations

from itertools import combinations
from typing import Any

from .util import TrainingError, object_sha256


PILLAR_POSITIONS = ("YEAR", "MONTH", "DAY", "HOUR")
HEAVENLY_STEMS = "甲乙丙丁戊己庚辛壬癸"
EARTHLY_BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

STEM_ELEMENTS = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水",
}
STEM_POLARITY = {
    "甲": "YANG",
    "乙": "YIN",
    "丙": "YANG",
    "丁": "YIN",
    "戊": "YANG",
    "己": "YIN",
    "庚": "YANG",
    "辛": "YIN",
    "壬": "YANG",
    "癸": "YIN",
}
BRANCH_ELEMENTS = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}
HIDDEN_STEMS = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "戊", "庚"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

STEM_COMBINATIONS = {
    frozenset(("甲", "己")): "土",
    frozenset(("乙", "庚")): "金",
    frozenset(("丙", "辛")): "水",
    frozenset(("丁", "壬")): "木",
    frozenset(("戊", "癸")): "火",
}

BRANCH_PAIR_RELATIONS = {
    "六合": {
        frozenset(pair)
        for pair in (("子", "丑"), ("寅", "亥"), ("卯", "戌"), ("辰", "酉"), ("巳", "申"), ("午", "未"))
    },
    "冲": {
        frozenset(pair)
        for pair in (("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"), ("辰", "戌"), ("巳", "亥"))
    },
    "害": {
        frozenset(pair)
        for pair in (("子", "未"), ("丑", "午"), ("寅", "巳"), ("卯", "辰"), ("申", "亥"), ("酉", "戌"))
    },
    "破": {
        frozenset(pair)
        for pair in (("子", "酉"), ("午", "卯"), ("辰", "丑"), ("戌", "未"), ("寅", "亥"), ("巳", "申"))
    },
}
BRANCH_PUNISHMENT_PAIRS = {
    frozenset(pair)
    for pair in (
        ("子", "卯"),
        ("寅", "巳"),
        ("巳", "申"),
        ("申", "寅"),
        ("丑", "戌"),
        ("戌", "未"),
        ("未", "丑"),
    )
}
SELF_PUNISHMENT_BRANCHES = {"辰", "午", "酉", "亥"}
BRANCH_GROUP_RELATIONS = {
    "三合": [frozenset(group) for group in (("申", "子", "辰"), ("亥", "卯", "未"), ("寅", "午", "戌"), ("巳", "酉", "丑"))],
    "三会": [frozenset(group) for group in (("亥", "子", "丑"), ("寅", "卯", "辰"), ("巳", "午", "未"), ("申", "酉", "戌"))],
}

ROOT_GRADES = ("MAIN_QI_ROOT", "MIDDLE_QI_ROOT", "RESIDUAL_QI_ROOT")


def _validate_four_pillars(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != set(PILLAR_POSITIONS):
        raise TrainingError("Bazi four_pillars must contain YEAR, MONTH, DAY, HOUR")
    pillars: dict[str, str] = {}
    for position in PILLAR_POSITIONS:
        pillar = value[position]
        if (
            not isinstance(pillar, str)
            or len(pillar) != 2
            or pillar[0] not in HEAVENLY_STEMS
            or pillar[1] not in EARTHLY_BRANCHES
        ):
            raise TrainingError(f"invalid Bazi pillar: {position}")
        pillars[position] = pillar
    return pillars


def _ten_god(day_master: str, other_stem: str) -> str:
    day_element = STEM_ELEMENTS[day_master]
    other_element = STEM_ELEMENTS[other_stem]
    same_polarity = STEM_POLARITY[day_master] == STEM_POLARITY[other_stem]
    if other_element == day_element:
        return "比肩" if same_polarity else "劫财"
    if GENERATES[other_element] == day_element:
        return "偏印" if same_polarity else "正印"
    if GENERATES[day_element] == other_element:
        return "食神" if same_polarity else "伤官"
    if CONTROLS[day_element] == other_element:
        return "偏财" if same_polarity else "正财"
    if CONTROLS[other_element] == day_element:
        return "七杀" if same_polarity else "正官"
    raise TrainingError("unreachable ten-god relationship")


def _element_role(day_master: str, element: str) -> str:
    day_element = STEM_ELEMENTS[day_master]
    if element == day_element:
        return "PEER"
    if GENERATES[element] == day_element:
        return "RESOURCE"
    if GENERATES[day_element] == element:
        return "OUTPUT"
    if CONTROLS[day_element] == element:
        return "WEALTH"
    if CONTROLS[element] == day_element:
        return "OFFICER"
    raise TrainingError("unreachable five-element role")


def _relation_rows(pillars: dict[str, str]) -> tuple[list[str], list[str]]:
    stems = {position: pillars[position][0] for position in PILLAR_POSITIONS}
    branches = {position: pillars[position][1] for position in PILLAR_POSITIONS}
    stem_rows: list[str] = []
    branch_rows: list[str] = []
    for left, right in combinations(PILLAR_POSITIONS, 2):
        left_stem = stems[left]
        right_stem = stems[right]
        result = STEM_COMBINATIONS.get(frozenset((left_stem, right_stem)))
        if result:
            stem_rows.append(
                f"{left}_STEM+{right}_STEM:{left_stem}{right_stem}合{result}"
            )

        left_branch = branches[left]
        right_branch = branches[right]
        pair = frozenset((left_branch, right_branch))
        for relation, pairs in BRANCH_PAIR_RELATIONS.items():
            if pair in pairs:
                branch_rows.append(
                    f"{relation}:{left}_BRANCH+{right}_BRANCH:{left_branch}{right_branch}"
                )
        if (
            pair in BRANCH_PUNISHMENT_PAIRS
            or left_branch == right_branch
            and left_branch in SELF_PUNISHMENT_BRANCHES
        ):
            branch_rows.append(
                f"刑:{left}_BRANCH+{right}_BRANCH:{left_branch}{right_branch}"
            )

    for positions in combinations(PILLAR_POSITIONS, 3):
        group = frozenset(branches[position] for position in positions)
        if len(group) != 3:
            continue
        for relation, relation_groups in BRANCH_GROUP_RELATIONS.items():
            if group in relation_groups:
                ids = "+".join(f"{position}_BRANCH" for position in positions)
                chars = "".join(branches[position] for position in positions)
                branch_rows.append(f"{relation}:{ids}:{chars}")
    return sorted(stem_rows), sorted(branch_rows)


def build_bazi_atomic_fact_ledger(four_pillars: dict[str, str]) -> dict[str, Any]:
    """Derive option-blind Bazi atoms under one declared, reproducible convention."""

    pillars = _validate_four_pillars(four_pillars)
    day_master = pillars["DAY"][0]
    hidden_stems: dict[str, list[str]] = {}
    five_elements: dict[str, str] = {}
    ten_gods: dict[str, str] = {}
    for position in PILLAR_POSITIONS:
        stem, branch = pillars[position]
        stem_id = f"{position}_STEM"
        branch_id = f"{position}_BRANCH"
        five_elements[stem_id] = STEM_ELEMENTS[stem]
        five_elements[branch_id] = BRANCH_ELEMENTS[branch]
        ten_gods[stem_id] = _ten_god(day_master, stem)
        hidden_stems[position] = list(HIDDEN_STEMS[branch])
        for index, hidden_stem in enumerate(hidden_stems[position], 1):
            fact_id = f"{position}_HIDDEN_{index}"
            five_elements[fact_id] = STEM_ELEMENTS[hidden_stem]
            ten_gods[fact_id] = _ten_god(day_master, hidden_stem)

    element_roles = {
        fact_id: _element_role(day_master, element)
        for fact_id, element in five_elements.items()
    }
    visible_stem_roots: dict[str, list[str]] = {}
    for stem_position in PILLAR_POSITIONS:
        stem_id = f"{stem_position}_STEM"
        stem_element = five_elements[stem_id]
        roots: list[str] = []
        for branch_position in PILLAR_POSITIONS:
            branch_hidden = hidden_stems[branch_position]
            matching_indexes = [
                index
                for index, hidden_stem in enumerate(branch_hidden)
                if STEM_ELEMENTS[hidden_stem] == stem_element
            ]
            if matching_indexes:
                grade = ROOT_GRADES[min(matching_indexes)]
                roots.append(f"{stem_id}@{branch_position}_BRANCH:{grade}")
        visible_stem_roots[stem_id] = roots

    stem_relations, branch_relations = _relation_rows(pillars)
    return {
        "schema": "BAZI-ATOMIC-FACT-LEDGER-V1",
        "convention": "ZIPING_ATOMIC_RELATIONS_V1",
        "scope": "NATAL_ONLY",
        "four_pillars": pillars,
        "day_master": day_master,
        "hidden_stems": hidden_stems,
        "five_elements": five_elements,
        "element_roles": element_roles,
        "ten_gods": ten_gods,
        "visible_stem_roots": visible_stem_roots,
        "heavenly_stem_combinations": stem_relations,
        "earthly_branch_relations": branch_relations,
        "verification_status": "MECHANICALLY_DERIVED",
    }


def validate_bazi_atomic_fact_ledger(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TrainingError("Bazi atomic fact ledger must be an object")
    four_pillars = value.get("four_pillars")
    expected = build_bazi_atomic_fact_ledger(four_pillars)
    if value != expected:
        raise TrainingError("Bazi atomic fact ledger does not match mechanical derivation")
    return value


def validate_bazi_strength_chain(
    ledger: dict[str, Any],
    value: Any,
) -> dict[str, Any]:
    required = {
        "schema",
        "ledger_sha256",
        "seasonal_command_fact_id",
        "root_fact_ids",
        "supporting_fact_ids",
        "draining_fact_ids",
        "controlling_fact_ids",
        "relation_fact_ids",
        "strength_candidates",
        "selected_strength_candidate",
        "pattern_candidates",
        "selected_pattern_candidate",
        "favorability_candidates",
        "selected_favorability_candidate",
        "method_competition",
        "unresolved_conflicts",
        "reasoning_summary",
        "option_blind_frozen",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise TrainingError("Bazi strength/structure/favorability chain is incomplete")
    if value["schema"] != "BAZI-STRENGTH-STRUCTURE-FAVORABILITY-CHAIN-V1":
        raise TrainingError("wrong Bazi strength-chain schema")
    if value["ledger_sha256"] != object_sha256(ledger):
        raise TrainingError("Bazi strength chain is not bound to its atomic ledger")
    if value["seasonal_command_fact_id"] != "MONTH_BRANCH":
        raise TrainingError("Bazi strength chain must bind the month command")

    roles = ledger["element_roles"]
    expected_support = sorted(
        fact_id for fact_id, role in roles.items() if role in {"PEER", "RESOURCE"}
    )
    expected_drain = sorted(
        fact_id for fact_id, role in roles.items() if role in {"OUTPUT", "WEALTH"}
    )
    expected_control = sorted(
        fact_id for fact_id, role in roles.items() if role == "OFFICER"
    )
    expected_roots = ledger["visible_stem_roots"]["DAY_STEM"]
    expected_relations = sorted(
        ledger["heavenly_stem_combinations"]
        + ledger["earthly_branch_relations"]
    )
    expected_lists = {
        "root_fact_ids": expected_roots,
        "supporting_fact_ids": expected_support,
        "draining_fact_ids": expected_drain,
        "controlling_fact_ids": expected_control,
        "relation_fact_ids": expected_relations,
    }
    for field, expected in expected_lists.items():
        if value[field] != expected:
            raise TrainingError(f"Bazi strength chain has incomplete {field}")

    for candidates_field, selected_field in (
        ("strength_candidates", "selected_strength_candidate"),
        ("pattern_candidates", "selected_pattern_candidate"),
        ("favorability_candidates", "selected_favorability_candidate"),
    ):
        candidates = value[candidates_field]
        if (
            not isinstance(candidates, list)
            or not candidates
            or any(not isinstance(item, str) or not item.strip() for item in candidates)
            or len(candidates) != len(set(candidates))
            or value[selected_field] not in candidates
        ):
            raise TrainingError(f"invalid Bazi candidate chain: {candidates_field}")
    for field in ("method_competition", "unresolved_conflicts"):
        rows = value[field]
        if (
            not isinstance(rows, list)
            or any(not isinstance(item, str) or not item.strip() for item in rows)
            or len(rows) != len(set(rows))
        ):
            raise TrainingError(f"invalid Bazi strength-chain field: {field}")
    if not value["method_competition"]:
        raise TrainingError("Bazi strength chain must disclose method competition")
    if not isinstance(value["reasoning_summary"], str) or not value["reasoning_summary"].strip():
        raise TrainingError("Bazi strength chain needs a reasoning summary")
    if value["option_blind_frozen"] is not True:
        raise TrainingError("Bazi strength, pattern and favorability must be option-blind frozen")
    return value

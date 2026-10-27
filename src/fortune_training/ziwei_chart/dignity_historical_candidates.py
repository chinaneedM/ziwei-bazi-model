from __future__ import annotations

from fortune_training.util import object_sha256


JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID = (
    "ZIWEI-JIELAN-1581-DIGNITY-LEXEME-CANDIDATES-R1"
)
JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION = "1.0.0"
JIELAN_1581_DIGNITY_LEXEME_RESOLVER_ID = (
    "ZIWEI-JIELAN-1581-DIGNITY-LEXEME-RUNTIME-R1"
)
JIELAN_1581_DIGNITY_LEXEME_RESOLVER_VERSION = "1.0.0"
JIELAN_1581_DIGNITY_SELECTION_STATUS = "PRESERVED_NOT_SELECTED"
JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID = "JIELAN-1581-DIGNITY-CH70-SOURCE-LEXEME-R1"
JIELAN_1581_DIGNITY_SOURCE_ID = "EXT-ZIWEI-JIELAN-1581"
JIELAN_1581_DIGNITY_PRIMARY_SOURCE_REF = (
    "EXT-ZIWEI-JIELAN-1581:CH70"
)
JIELAN_1581_DIGNITY_PARALLEL_SOURCE_REF = (
    "EXT-ZIWEI-JIELAN-1581:CH69"
)
JIELAN_1581_DIGNITY_PARALLEL_STATUS = (
    "PRESENT_REQUIRES_CELL_LEVEL_CROSS_COLLATION"
)
JIELAN_1581_DIGNITY_NORMALIZATION_STATUS = (
    "SOURCE_LEXEME_ONLY_NO_PRODUCTION_GRADE_COERCION"
)

BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")

# Only source-explicit gloss relationships are recorded. They are not converted
# into OPERATIONAL-ZIWEI-DIGNITY-R4 grade/status values.
JIELAN_1581_DIGNITY_EXPLICIT_GLOSSES = {
    "旺": {"gloss_target": "庙", "relation": "SOURCE_EXPLICIT_EQUIVALENT"},
    "利": {"gloss_target": "旺", "relation": "SOURCE_EXPLICIT_EQUIVALENT"},
    "平": {"gloss_target": "闲", "relation": "SOURCE_EXPLICIT_EQUIVALENT"},
    "得地": {"gloss_target": "旺", "relation": "SOURCE_EXPLICIT_EQUIVALENT"},
    "嗔": {"gloss_target": "陷", "relation": "SOURCE_EXPLICIT_EQUIVALENT"},
    "地": {"gloss_target": "得地", "relation": "SOURCE_EXPLICIT_EQUIVALENT"},
    "局": {"gloss_target": "得地", "relation": "SOURCE_EXPLICIT_EQUIVALENT"},
    "庭": {"gloss_target": "庙", "relation": "SOURCE_EXPLICIT_EQUIVALENT"},
    "旺地": {"gloss_target": "旺", "relation": "SOURCE_EXPLICIT_COMMENTARY"},
}

# Chapter 70 is star-oriented and therefore used as the deterministic raw-lexeme
# candidate basis. A branch may have multiple lexemes or none; both conditions are
# preserved rather than silently adjudicated.
_GROUPS: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
    "紫微": (
        ("旺", tuple("卯酉巳亥")), ("庙", tuple("丑午未")), ("利", tuple("寅申")),
        ("陷", tuple("辰戌")), ("平", tuple("子午")),
    ),
    "天机": (
        ("庙", tuple("卯辰戌亥")), ("得地", tuple("子午")),
        ("陷", tuple("寅申丑未酉")),
    ),
    "太阳": (
        ("庙", tuple("寅卯辰巳午未")), ("陷", tuple("戌亥子")),
        ("平", tuple("丑申酉")),
    ),
    "武曲": (
        ("庙", tuple("辰戌丑未")), ("得地", tuple("卯酉巳亥")),
        ("陷", tuple("子午")), ("平", tuple("寅申")),
    ),
    "天同": (
        ("庙", tuple("子寅卯")), ("得地", tuple("丑未申")),
        ("嗔", tuple("辰戌午酉巳亥")),
    ),
    "廉贞": (
        ("旺", tuple("子午卯酉")), ("庙", tuple("未申")),
        ("陷", tuple("巳亥")), ("地", tuple("丑寅辰戌")),
    ),
    "天府": (
        ("陷", tuple("巳亥")), ("庙", tuple("辰戌丑未卯酉")),
        ("地", tuple("寅申子午")),
    ),
    "太阴": (
        ("庙", tuple("酉戌亥子丑")), ("陷", tuple("卯辰巳午")),
        ("平", tuple("寅申未")),
    ),
    "贪狼": (
        ("庙", tuple("辰戌丑未")), ("得地", tuple("子卯酉")),
        ("陷", tuple("巳午亥")), ("平", tuple("寅申")),
    ),
    "巨门": (
        ("局", tuple("子丑卯")), ("庭", tuple("寅申")), ("地", ("午",)),
        ("陷", tuple("未酉丑")), ("平", tuple("辰巳戌亥")),
    ),
    "天相": (
        ("庙", tuple("子辰巳亥")), ("陷", tuple("卯酉")),
        ("旺地", tuple("丑寅午未申戌")),
    ),
    "天梁": (
        ("庭", tuple("子午寅卯辰戌")), ("得地", tuple("酉丑")),
        ("陷", tuple("未申巳亥")),
    ),
    "七杀": (
        ("庙", tuple("寅申子午")), ("得地", tuple("辰戌丑未")),
        ("陷", tuple("卯酉")), ("平", tuple("巳亥")),
    ),
    "破军": (
        ("庙", tuple("寅申子午")), ("闲", tuple("巳亥")),
        ("地", tuple("丑未")), ("陷", tuple("卯酉辰戌")),
    ),
    "左辅": (
        ("庙", tuple("寅午戌")), ("陷", tuple("子辰申")),
        ("平", tuple("卯酉巳亥丑未")),
    ),
    "右弼": (
        ("庙", tuple("寅午戌")), ("陷", tuple("子辰申")),
        ("平", tuple("卯酉巳亥丑未")),
    ),
    "文曲": (
        ("旺", tuple("亥卯未")), ("庭", tuple("巳酉")), ("地", tuple("子辰丑")),
        ("利", ("申",)), ("陷", tuple("寅午戌")),
    ),
    "文昌": (
        ("庙", tuple("巳酉丑未")), ("陷", tuple("寅午戌")),
        ("得地", tuple("子卯辰申亥")),
    ),
    "禄存": (
        ("庙", tuple("子午卯酉")), ("旺", tuple("丑寅辰巳未申戌亥")),
    ),
    "擎羊": (
        ("庙", tuple("辰戌丑未")), ("闲", tuple("寅申巳亥")),
        ("陷", tuple("子午卯酉")),
    ),
    "陀罗": (
        ("庙", tuple("辰戌丑未")), ("闲", tuple("寅申巳亥")),
        ("陷", tuple("子午卯酉")),
    ),
    "火星": (
        ("庙", tuple("寅卯午戌")), ("得地", tuple("辰巳未申")),
        ("陷", tuple("子丑酉亥")),
    ),
    "铃星": (
        ("庙", tuple("寅卯午戌")), ("得地", tuple("辰巳未申")),
        ("陷", tuple("子丑酉亥")),
    ),
    "地劫": (
        ("庙", tuple("辰戌丑未")), ("不利", tuple("子寅卯巳午申酉亥")),
    ),
    "地空": (
        ("庙", tuple("辰戌丑未")), ("不利", tuple("子寅卯巳午申酉亥")),
    ),
}


def _cell_lexemes(display_name: str, branch: str) -> tuple[str, ...]:
    return tuple(
        lexeme
        for lexeme, branches in _GROUPS[display_name]
        if branch in branches
    )


def jielan_1581_dignity_lexeme_registry_payload() -> dict[str, object]:
    cells = tuple(
        {
            "display_name": display_name,
            "branch": branch,
            "source_lexemes": _cell_lexemes(display_name, branch),
            "attestation_status": (
                "ATTESTED"
                if _cell_lexemes(display_name, branch)
                else "UNSTATED_IN_CH70_STAR_VERSE"
            ),
            "source_conflict": len(_cell_lexemes(display_name, branch)) > 1,
        }
        for display_name in _GROUPS
        for branch in BRANCHES
    )
    return {
        "registry_id": JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID,
        "registry_version": JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION,
        "selection_status": JIELAN_1581_DIGNITY_SELECTION_STATUS,
        "candidate_id": JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID,
        "source_id": JIELAN_1581_DIGNITY_SOURCE_ID,
        "primary_source_ref": JIELAN_1581_DIGNITY_PRIMARY_SOURCE_REF,
        "parallel_source_ref": JIELAN_1581_DIGNITY_PARALLEL_SOURCE_REF,
        "parallel_source_status": JIELAN_1581_DIGNITY_PARALLEL_STATUS,
        "normalization_status": JIELAN_1581_DIGNITY_NORMALIZATION_STATUS,
        "explicit_glosses": JIELAN_1581_DIGNITY_EXPLICIT_GLOSSES,
        "entity_count": len(_GROUPS),
        "cell_count": len(cells),
        "cells": cells,
        "production_grade_mapping_present": False,
    }


def jielan_1581_dignity_lexeme_registry_hash() -> str:
    return object_sha256(jielan_1581_dignity_lexeme_registry_payload())


def resolve_jielan_1581_dignity_lexeme_candidate(
    *,
    display_name: str | None = None,
) -> dict[str, object]:
    if display_name is not None and display_name not in _GROUPS:
        raise ValueError(f"unsupported Jielan dignity entity: {display_name}")

    names = (display_name,) if display_name is not None else tuple(_GROUPS)
    rows = tuple(
        {
            "display_name": name,
            "branch": branch,
            "source_lexemes": _cell_lexemes(name, branch),
            "attestation_status": (
                "ATTESTED"
                if _cell_lexemes(name, branch)
                else "UNSTATED_IN_CH70_STAR_VERSE"
            ),
            "source_conflict": len(_cell_lexemes(name, branch)) > 1,
            "explicit_glosses": tuple(
                {
                    "lexeme": lexeme,
                    **JIELAN_1581_DIGNITY_EXPLICIT_GLOSSES[lexeme],
                }
                for lexeme in _cell_lexemes(name, branch)
                if lexeme in JIELAN_1581_DIGNITY_EXPLICIT_GLOSSES
            ),
        }
        for name in names
        for branch in BRANCHES
    )
    payload: dict[str, object] = {
        "schema": JIELAN_1581_DIGNITY_LEXEME_RESOLVER_ID,
        "runtime_resolver_id": JIELAN_1581_DIGNITY_LEXEME_RESOLVER_ID,
        "runtime_resolver_version": JIELAN_1581_DIGNITY_LEXEME_RESOLVER_VERSION,
        "registry_id": JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID,
        "registry_version": JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION,
        "registry_hash": jielan_1581_dignity_lexeme_registry_hash(),
        "selection_status": JIELAN_1581_DIGNITY_SELECTION_STATUS,
        "candidate_id": JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID,
        "source_id": JIELAN_1581_DIGNITY_SOURCE_ID,
        "primary_source_ref": JIELAN_1581_DIGNITY_PRIMARY_SOURCE_REF,
        "parallel_source_ref": JIELAN_1581_DIGNITY_PARALLEL_SOURCE_REF,
        "parallel_source_status": JIELAN_1581_DIGNITY_PARALLEL_STATUS,
        "normalization_status": JIELAN_1581_DIGNITY_NORMALIZATION_STATUS,
        "display_name_filter": display_name,
        "rows": rows,
        "production_grade_mapping_present": False,
    }
    payload["runtime_hash"] = object_sha256(payload)
    return payload

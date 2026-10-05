from __future__ import annotations

from collections import Counter

from fortune_training.util import object_sha256

from .dignity_historical_candidates import (
    BRANCHES,
    JIELAN_1581_DIGNITY_EXPLICIT_GLOSSES,
    JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID,
    JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID,
    JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION,
    JIELAN_1581_DIGNITY_SELECTION_STATUS,
    jielan_1581_dignity_lexeme_registry_payload,
)


JIELAN_1581_DIGNITY_CROSS_COLLATION_ID = (
    "ZIWEI-JIELAN-1581-DIGNITY-CH69-CH70-CROSS-COLLATION-R1"
)
JIELAN_1581_DIGNITY_CROSS_COLLATION_VERSION = "1.0.0"
JIELAN_1581_DIGNITY_CH69_SOURCE_REF = "EXT-ZIWEI-JIELAN-1581:CH69"
JIELAN_1581_DIGNITY_CH70_SOURCE_REF = "EXT-ZIWEI-JIELAN-1581:CH70"
JIELAN_1581_DIGNITY_CROSS_COLLATION_STATUS = (
    "CELL_LEVEL_CROSS_COLLATION_COMPLETE_NO_GRADE_COERCION"
)

# Chapter 69 is palace-oriented. Only cells whose star token and category scope
# are sufficiently explicit are materialized below. Ambiguous/truncated tokens
# are kept in _CH69_UNRESOLVED_CELLS rather than guessed.
_CH69_GROUPS: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
    "子": (
        ("得地", ("七杀", "太阴", "天梁")),
        ("祥", ("天相", "破军", "贪狼", "紫微", "天府")),
        ("陷", ("火星", "铃星", "陀罗", "天机", "左辅", "右弼")),
        ("闲", ("天同", "廉贞", "巨门", "武曲")),
    ),
    "丑": (
        ("庙", ("紫微", "贪狼", "武曲", "天府", "天同", "天梁")),
        ("闲", ("七杀", "天相", "廉贞", "铃星", "左辅", "右弼")),
        ("陷", ("巨门", "天机")),
    ),
    "寅": (
        ("庙", ("紫微", "天同", "巨门", "天梁", "火星", "铃星", "七杀", "贪狼")),
        ("闲", ("廉贞", "天府", "天相", "破军", "武曲")),
        ("陷", ("天机", "文曲")),
    ),
    "卯": (
        ("庙", ("武曲", "天机", "天同", "贪狼", "天府", "巨门", "火星", "铃星")),
        ("闲", ("紫微", "左辅", "右弼", "廉贞", "天梁")),
        ("陷", ("天相", "擎羊", "陀罗", "七杀", "破军")),
    ),
    "辰": (
        ("庙", ("擎羊", "陀罗", "七杀", "天机", "天府", "天梁", "天相", "廉贞")),
        ("陷", ("火星", "铃星", "巨门", "破军", "贪狼", "天同", "左辅", "右弼", "紫微")),
    ),
    "巳": (
        ("兴", ("天机", "天相", "火星", "铃星")),
        ("闲", ("巨门", "擎羊", "陀罗", "七杀", "破军", "左辅", "右弼", "紫微")),
        ("陷", ("天同", "天梁", "天府", "武曲", "贪狼", "廉贞")),
    ),
    "午": (
        ("庙", ("左辅", "右弼", "火星", "铃星", "紫微", "天府", "天相", "天梁", "破军")),
        ("闲", ("廉贞", "天机")),
        ("陷", ("擎羊", "陀罗")),
        ("低", ("文昌", "文曲", "贪狼", "天同", "武曲", "巨门")),
    ),
    "未": (
        ("庙", ("擎羊", "陀罗", "紫微", "天府", "廉贞", "火星", "铃星", "贪狼", "破军")),
        ("闲", ("天同", "左辅", "右弼", "天梁", "天相", "七杀")),
        ("陷", ("天机", "武曲", "巨门")),
    ),
    "申": (
        ("庙", ("紫微", "七杀", "巨门", "廉贞")),
        ("闲", ("天府", "擎羊", "陀罗", "天相", "破军")),
        ("陷", ("武曲", "火星", "铃星", "贪狼", "左辅", "右弼", "天机", "天梁", "天同")),
    ),
    "酉": (
        ("宜", ("天府", "擎羊")),
        ("闲", ("廉贞", "天梁", "左辅", "右弼", "铃星")),
        ("陷", ("武曲", "破军", "贪狼", "天机", "巨门", "天相", "火星", "天同", "陀罗", "七杀", "紫微")),
    ),
    "戌": (
        ("庙", ("天府", "天机", "天梁", "武曲", "七杀", "铃星", "擎羊", "陀罗", "左辅", "右弼", "贪狼")),
        ("闲", ("廉贞", "天相")),
        ("陷", ("破军", "天同", "文昌", "文曲", "紫微", "巨门")),
    ),
    "亥": (
        ("庙", ("天机", "铃星", "天相", "巨门")),
        ("闲", ("武曲", "破军", "七杀", "紫微", "擎羊", "陀罗", "左辅", "右弼")),
        ("陷", ("天府", "天同", "天梁", "贪狼", "火星", "廉贞")),
    ),
}

# Cells where CH69 contains a token or group whose exact identity/scope cannot be
# safely projected into the CH70 25-entity grid. These remain unresolved.
_CH69_UNRESOLVED_CELLS = {
    ("文昌", "子"): "CH69 uses singular 文 in 子宫; cannot safely choose 文昌 vs 文曲.",
    ("文曲", "子"): "CH69 uses singular 文 in 子宫; cannot safely choose 文昌 vs 文曲.",
    ("擎羊", "丑"): "CH69 phrase 天哭羊陀火破祥 has unclear category scope against the following 上六星皆庙 note.",
    ("陀罗", "丑"): "CH69 phrase 天哭羊陀火破祥 has unclear category scope against the following 上六星皆庙 note.",
    ("火星", "丑"): "CH69 phrase 天哭羊陀火破祥 has unclear category scope against the following 上六星皆庙 note.",
    ("破军", "丑"): "CH69 phrase 天哭羊陀火破祥 has unclear category scope against the following 上六星皆庙 note.",
    ("太阳", "辰"): "CH69 transcription has 辰午... where a star token may be corrupt; no silent 午->日 repair.",
    ("文昌", "寅"): "CH69 寅宫 line ends 曲与 and is textually truncated; 文昌 is not inferred from 文曲.",
}

# Chapter 69's own explicit/local glosses. These are source-lexical relations,
# never production R4 grade conversions.
_CH69_DIRECT_GLOSS_TARGETS = {
    "得地": frozenset(("庙", "旺")),
    "祥": frozenset(("庙",)),
    "兴": frozenset(("庙",)),
    "低": frozenset(("陷",)),
    "宜": frozenset(("庙",)),
}

# A coarse source-local polarity is used only to flag obvious CH69/CH70 semantic
# direction clashes. It is not a grade scale and is never exported as a selected
# production dignity value.
_SOURCE_LOCAL_POLARITY = {
    "庙": "FAVORABLE_SOURCE_LEXEME",
    "旺": "FAVORABLE_SOURCE_LEXEME",
    "利": "FAVORABLE_SOURCE_LEXEME",
    "得地": "FAVORABLE_SOURCE_LEXEME",
    "地": "FAVORABLE_SOURCE_LEXEME",
    "局": "FAVORABLE_SOURCE_LEXEME",
    "庭": "FAVORABLE_SOURCE_LEXEME",
    "旺地": "FAVORABLE_SOURCE_LEXEME",
    "祥": "FAVORABLE_SOURCE_LEXEME",
    "兴": "FAVORABLE_SOURCE_LEXEME",
    "宜": "FAVORABLE_SOURCE_LEXEME",
    "闲": "IDLE_SOURCE_LEXEME",
    "平": "IDLE_SOURCE_LEXEME",
    "陷": "FALLEN_SOURCE_LEXEME",
    "嗔": "FALLEN_SOURCE_LEXEME",
    "低": "FALLEN_SOURCE_LEXEME",
    "不利": "UNFAVORABLE_UNSPECIFIED_SOURCE_LEXEME",
}


def _ch69_cell_lexemes(display_name: str, branch: str) -> tuple[str, ...]:
    return tuple(
        lexeme
        for lexeme, display_names in _CH69_GROUPS[branch]
        if display_name in display_names
    )


def _direct_source_gloss_equivalent(
    ch69_lexemes: tuple[str, ...],
    ch70_lexemes: tuple[str, ...],
) -> bool:
    for lexeme in ch69_lexemes:
        if any(
            target in ch70_lexemes
            for target in _CH69_DIRECT_GLOSS_TARGETS.get(lexeme, ())
        ):
            return True
    for lexeme in ch70_lexemes:
        gloss = JIELAN_1581_DIGNITY_EXPLICIT_GLOSSES.get(lexeme)
        if gloss and gloss["gloss_target"] in ch69_lexemes:
            return True
    return False


def _source_local_polarities(lexemes: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                _SOURCE_LOCAL_POLARITY[lexeme]
                for lexeme in lexemes
                if lexeme in _SOURCE_LOCAL_POLARITY
            }
        )
    )


def _relation(
    *,
    display_name: str,
    branch: str,
    ch69_lexemes: tuple[str, ...],
    ch70_lexemes: tuple[str, ...],
) -> str:
    if not ch69_lexemes and (display_name, branch) in _CH69_UNRESOLVED_CELLS:
        return "CH69_TEXT_UNRESOLVED"
    if not ch69_lexemes:
        return "CH69_UNSTATED"
    if not ch70_lexemes:
        return "CH70_UNSTATED"
    if set(ch69_lexemes) & set(ch70_lexemes):
        return "EXACT_LEXEME_OVERLAP"
    if _direct_source_gloss_equivalent(ch69_lexemes, ch70_lexemes):
        return "SOURCE_EXPLICIT_EQUIVALENT"

    ch69_polarities = set(_source_local_polarities(ch69_lexemes))
    ch70_polarities = set(_source_local_polarities(ch70_lexemes))
    comparable = {
        "FAVORABLE_SOURCE_LEXEME",
        "IDLE_SOURCE_LEXEME",
        "FALLEN_SOURCE_LEXEME",
    }
    if (
        ch69_polarities
        and ch70_polarities
        and ch69_polarities <= comparable
        and ch70_polarities <= comparable
        and ch69_polarities.isdisjoint(ch70_polarities)
    ):
        return "SOURCE_LOCAL_POLARITY_CONFLICT"
    return "ATTESTED_NON_EQUIVALENT_NO_DIRECT_GLOSS"


def jielan_1581_dignity_ch69_ch70_cross_collation_payload() -> dict[str, object]:
    ch70_registry = jielan_1581_dignity_lexeme_registry_payload()
    ch70_by_key = {
        (row["display_name"], row["branch"]): row
        for row in ch70_registry["cells"]
    }
    rows = []
    for display_name in tuple(dict.fromkeys(row["display_name"] for row in ch70_registry["cells"])):
        for branch in BRANCHES:
            ch69_lexemes = _ch69_cell_lexemes(display_name, branch)
            ch70 = ch70_by_key[(display_name, branch)]
            ch70_lexemes = tuple(ch70["source_lexemes"])
            unresolved_note = _CH69_UNRESOLVED_CELLS.get((display_name, branch))
            relation = _relation(
                display_name=display_name,
                branch=branch,
                ch69_lexemes=ch69_lexemes,
                ch70_lexemes=ch70_lexemes,
            )
            rows.append(
                {
                    "display_name": display_name,
                    "branch": branch,
                    "ch69_source_lexemes": ch69_lexemes,
                    "ch69_attestation_status": (
                        "ATTESTED"
                        if ch69_lexemes
                        else (
                            "UNRESOLVED_TEXT_SCOPE"
                            if unresolved_note
                            else "UNSTATED_IN_CH69_PALACE_VERSE"
                        )
                    ),
                    "ch69_unresolved_note": unresolved_note,
                    "ch70_source_lexemes": ch70_lexemes,
                    "ch70_attestation_status": ch70["attestation_status"],
                    "ch70_source_conflict": ch70["source_conflict"],
                    "relation": relation,
                    "ch69_source_local_polarities": _source_local_polarities(ch69_lexemes),
                    "ch70_source_local_polarities": _source_local_polarities(ch70_lexemes),
                    "production_grade_mapping_present": False,
                }
            )

    relation_counts = dict(Counter(row["relation"] for row in rows))
    payload: dict[str, object] = {
        "schema": JIELAN_1581_DIGNITY_CROSS_COLLATION_ID,
        "cross_collation_id": JIELAN_1581_DIGNITY_CROSS_COLLATION_ID,
        "cross_collation_version": JIELAN_1581_DIGNITY_CROSS_COLLATION_VERSION,
        "cross_collation_status": JIELAN_1581_DIGNITY_CROSS_COLLATION_STATUS,
        "registry_id": JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID,
        "registry_version": JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION,
        "candidate_id": JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID,
        "selection_status": JIELAN_1581_DIGNITY_SELECTION_STATUS,
        "ch69_source_ref": JIELAN_1581_DIGNITY_CH69_SOURCE_REF,
        "ch70_source_ref": JIELAN_1581_DIGNITY_CH70_SOURCE_REF,
        "entity_count": ch70_registry["entity_count"],
        "cell_count": len(rows),
        "relation_counts": relation_counts,
        "rows": tuple(rows),
        "ch69_unresolved_cell_count": len(_CH69_UNRESOLVED_CELLS),
        "ch70_source_conflict_cell_count": sum(
            1 for row in rows if row["ch70_source_conflict"]
        ),
        "ch70_unstated_cell_count": sum(
            1
            for row in rows
            if row["ch70_attestation_status"] == "UNSTATED_IN_CH70_STAR_VERSE"
        ),
        "ch69_used_to_fill_ch70": False,
        "ch70_used_to_overwrite_ch69": False,
        "production_grade_mapping_present": False,
        "production_dignity_registry_changed": False,
        "winner_selected": False,
    }
    payload["cross_collation_hash"] = object_sha256(payload)
    return payload


def resolve_jielan_1581_dignity_ch69_ch70_cross_collation(
    *,
    display_name: str | None = None,
) -> dict[str, object]:
    payload = jielan_1581_dignity_ch69_ch70_cross_collation_payload()
    if display_name is None:
        return payload
    names = {row["display_name"] for row in payload["rows"]}
    if display_name not in names:
        raise ValueError(f"unsupported Jielan dignity entity: {display_name}")
    filtered = {
        **payload,
        "display_name_filter": display_name,
        "rows": tuple(
            row for row in payload["rows"] if row["display_name"] == display_name
        ),
    }
    filtered["cross_collation_hash"] = object_sha256(
        {
            key: value
            for key, value in filtered.items()
            if key != "cross_collation_hash"
        }
    )
    return filtered

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

from .source_access import DERIVED_ACCESS_ROOT
from .source_access_validator import validate_source_access
from .util import TrainingError, atomic_write_bytes, atomic_write_json, load_json


AUDIT_ID = "BAZI-CLASSICAL-RELATION-LIFECYCLE-EVIDENCE-MATRIX-R1"
AUDIT_ROOT = Path("audits/bazi-classical-relation-lifecycle-evidence-r1")
MATRIX_PATH = AUDIT_ROOT / "matrix.json"
COVERAGE_PATH = AUDIT_ROOT / "coverage-manifest.json"
REPORT_PATH = AUDIT_ROOT / "dependency-gap-report.md"
MATRIX_SCHEMA_PATH = Path(
    "schemas/bazi-classical-relation-lifecycle-evidence-matrix-r1.schema.json"
)
COVERAGE_SCHEMA_PATH = Path(
    "schemas/bazi-classical-relation-lifecycle-evidence-coverage-r1.schema.json"
)

SOURCE_ID = "S14"
EXPECTED_SOURCE_PATH = "sources/canonical/S14_八字合冲刑害墓库与结构变化库.txt"
EXPECTED_SOURCE_BYTES = 3354845
EXPECTED_SOURCE_SHA256 = "b225e64fcf7238b27a634e653a6904403d518335aeca59372b32e02f4a560407"
EXPECTED_SEGMENT_COUNT = 52

CURRENT_RELATION_FAMILIES = (
    "STEM_FIVE_COMBINATION",
    "BRANCH_LIUHE",
    "BRANCH_CHONG",
    "BRANCH_CHUAN",
    "BRANCH_SANHE_COMPLETE",
    "BRANCH_ZIMAO_PUNISHMENT",
    "BRANCH_DIRECTIONAL_PUNISHMENT",
    "BRANCH_SELF_PUNISHMENT",
)
RUNTIME_GAP_FAMILIES = (
    "BRANCH_HARM",
    "BRANCH_BREAK",
    "BRANCH_PARTIAL_TRINE",
    "BRANCH_DIRECTIONAL_TRIAD",
    "HIDDEN_COMBINATION",
    "OTHER_UNRELEASED_RELATION",
)
AUDIT_META_RELATION_FAMILIES = ("CROSS_FAMILY_RELATION_LIFECYCLE",)
STATEMENT_CLASSES = (
    "DEFINITION_OR_NOMINAL_RELATION",
    "ELIGIBILITY_CONDITION",
    "TRANSFORMATION_CONDITION",
    "NON_TRANSFORMATION_OR_BINDING_CONDITION",
    "SEASONAL_OR_MONTH_COMMAND_DEPENDENCY",
    "ROOT_OR_SUPPORT_DEPENDENCY",
    "EXPOSURE_OR_HIDDEN_STEM_DEPENDENCY",
    "MULTIPLICITY_OR_COMPETITION",
    "COEXISTING_RELATION_DEPENDENCY",
    "CLASH_OR_RELEASE_DEPENDENCY",
    "PUNISHMENT_DEPENDENCY",
    "ORDER_OR_PROXIMITY_DEPENDENCY",
    "TEMPORAL_CONTEXT_HINT",
    "RESULT_OR_EFFECT_STATEMENT",
    "EXCEPTION_OR_LIMIT",
    "CONTRADICTORY_OR_ALTERNATIVE_STATEMENT",
    "EXAMPLE_ONLY",
    "COMMENTARY_OR_EXPLANATION",
    "AMBIGUOUS",
    "RUNTIME_RELATION_GAP",
)
RUNTIME_STATUSES = (
    "AVAILABLE_EXACTLY",
    "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
    "PARTIALLY_AVAILABLE",
    "MISSING_PRIMITIVE",
    "OUTSIDE_CURRENT_RELATION_REGISTRY",
    "SOURCE_SEMANTICS_AMBIGUOUS",
)
REVIEW_STATUSES = (
    "REVIEWED_R1",
    "CONFLICT_REQUIRES_REVIEW",
    "SOURCE_SEMANTICS_AMBIGUOUS",
    "RUNTIME_RELATION_GAP_DEFERRED",
)

TEXT_KEYS = (
    "RAW_CLAUSE_TEXT",
    "T",
    "RAW_TEXT",
    "RAW_BLOCK_TEXT",
    "ASSERTION",
    "RULE",
    "RAW_TEXT_FRAGMENT",
    "OTHER_SOURCE_POSITION",
    "SHFTK_POSITION",
    "COUNTEREVIDENCE_OR_DISQUALIFIER",
    "RAW_RESULT_TERM",
    "RAW_TERM",
    "TERM",
    "W",
    "TITLE",
    "SOURCE_CHAPTER_TITLE",
    "CHAPTER_TITLE",
)

DISCOVERY_CONTROL_ROLE = "TECHNICAL_TERM"
DISCOVERY_CONTROL_FIELD = "RAW_TERM"
DISCOVERY_RELATION_MORPHEMES = tuple("合冲刑害破会化绊局")
DISCOVERY_TERM_PATTERN = re.compile(r"^[\u3400-\u9fff]{2,8}$")
CONFLICT_SOURCE_SIDE_FIELDS = (
    "OTHER_SOURCE_POSITION",
    "SHFTK_POSITION",
    "COUNTEREVIDENCE_OR_DISQUALIFIER",
)

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
GANZHI = re.compile(f"[{STEMS}][{BRANCHES}]")


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def _extract_text(line: str) -> tuple[str, str, dict[str, Any]]:
    stripped = line.rstrip("\r\n")
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        value = None
    if isinstance(value, dict):
        for key in TEXT_KEYS:
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.strip():
                return candidate, f"JSON:{key}", value
        strings = [
            item
            for item in value.values()
            if isinstance(item, str) and re.search(r"[\u3400-\u9fff]", item)
        ]
        if strings:
            return max(strings, key=len), "JSON:CJK_FALLBACK", value
        return "", "JSON:NO_SOURCE_TEXT", value
    if "\t" in stripped:
        fields = [
            field
            for field in stripped.split("\t")
            if re.search(r"[\u3400-\u9fff]", field)
        ]
        return (max(fields, key=len), "TSV:CJK_FIELD", {}) if fields else (
            "",
            "TSV:NO_SOURCE_TEXT",
            {},
        )
    return stripped, "PLAIN_TEXT", {}


def _source_views(line: str) -> list[tuple[str, str, dict[str, Any], str | None]]:
    text, record_type, metadata = _extract_text(line)
    conflict_id = metadata.get("CONFLICT_ID")
    if isinstance(conflict_id, str) and conflict_id:
        explicit_sides = [
            (value, f"JSON:{key}", metadata, key)
            for key in CONFLICT_SOURCE_SIDE_FIELDS
            if isinstance((value := metadata.get(key)), str) and value.strip()
        ]
        if len(explicit_sides) >= 2:
            return explicit_sides
        pairing_role = (
            record_type.removeprefix("JSON:")
            if record_type.startswith("JSON:")
            else None
        )
        return [(text, record_type, metadata, pairing_role)]
    return [(text, record_type, metadata, None)]


def _discover_control_term(metadata: dict[str, Any]) -> str | None:
    if not isinstance(metadata.get("SOURCE_TERM_OCCURRENCE_ID"), str):
        return None
    if metadata.get("RESULT_OCCURRENCE_ROLE") != DISCOVERY_CONTROL_ROLE:
        return None
    term = metadata.get(DISCOVERY_CONTROL_FIELD)
    if not isinstance(term, str):
        return None
    term = term.strip()
    if not DISCOVERY_TERM_PATTERN.fullmatch(term):
        return None
    if not _contains_any(term, DISCOVERY_RELATION_MORPHEMES):
        return None
    return term


def _vocabulary_closure_sha256(terms: Iterable[str]) -> str:
    payload = json.dumps(
        sorted(set(terms)), ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return _sha256(payload)


def _relation_families(text: str, heading: str) -> tuple[list[str], list[str]]:
    scope = f"{heading}\n{text}"
    current: set[str] = set()
    gaps: set[str] = set()

    stem_signal = _contains_any(
        scope,
        (
            "天干五合",
            "十干配合",
            "十干合",
            "干合",
            "甲己",
            "乙庚",
            "丙辛",
            "丁壬",
            "戊癸",
            "化气",
        ),
    )
    if stem_signal and _contains_any(text, ("合", "化", "争", "妒", "配")):
        current.add("STEM_FIVE_COMBINATION")

    if _contains_any(
        text,
        ("地支六合", "六合", "子丑合", "寅亥合", "卯戌合", "辰酉合", "巳申合", "午未合"),
    ) or ("十二支六合" in heading and "合" in text):
        current.add("BRANCH_LIUHE")
    if _contains_any(text, ("六冲", "相冲", "冲")) and (
        "地支" in scope
        or len(GANZHI.findall(text)) >= 1
        or _contains_any(text, ("子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥"))
    ):
        current.add("BRANCH_CHONG")
    if _contains_any(
        text,
        ("三合", "三合局", "申子辰", "亥卯未", "寅午戌", "巳酉丑"),
    ) and not _contains_any(text, ("半合", "拱合", "拱局")):
        current.add("BRANCH_SANHE_COMPLETE")
    if "刑" in text and _contains_any(text, ("子卯", "无礼之刑")):
        current.add("BRANCH_ZIMAO_PUNISHMENT")
    if "刑" in text and _contains_any(
        text,
        ("寅巳申", "丑戌未", "恃势之刑", "无恩之刑", "三刑"),
    ):
        current.add("BRANCH_DIRECTIONAL_PUNISHMENT")
    if _contains_any(text, ("自刑", "辰辰", "午午", "酉酉", "亥亥")):
        current.add("BRANCH_SELF_PUNISHMENT")

    if "相穿" in text:
        current.add("BRANCH_CHUAN")

    if _contains_any(text, ("六害", "相害", "穿害")):
        gaps.add("BRANCH_HARM")
    if _contains_any(text, ("六破", "相破")):
        gaps.add("BRANCH_BREAK")
    if _contains_any(text, ("半合", "拱合", "拱局", "生地半合", "墓地半合")):
        gaps.add("BRANCH_PARTIAL_TRINE")
    if _contains_any(text, ("三会", "会方", "方局")):
        gaps.add("BRANCH_DIRECTIONAL_TRIAD")
    if _contains_any(text, ("暗冲", "暗会")):
        gaps.add("OTHER_UNRELEASED_RELATION")
    generic_relation = (
        _contains_any(
            text,
            (
                "合不等于化",
                "合而不化",
                "合而不合",
                "合化",
                "争合",
                "妒合",
                "相冲",
                "六冲",
                "冲破",
                "冲开",
                "冲散",
                "解冲",
                "刑冲",
                "刑合",
                "相刑",
                "三刑",
                "自刑",
                "带刑",
            ),
        )
        or bool(re.search(r"冲(?!突)", text))
    )
    if generic_relation and not current and not gaps:
        current.add("CROSS_FAMILY_RELATION_LIFECYCLE")
    return sorted(current), sorted(gaps)


DEPENDENCY_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("MONTH_COMMAND_OR_SEASON", ("月令", "司令", "当令", "得令", "失令", "季节", "旺月")),
    ("ROOT_OR_SUPPORT", ("通根", "根气", "有根", "无根", "得根", "扎根", "根深")),
    ("EXPOSURE_OR_HIDDEN_STEM", ("透干", "透出", "透露", "藏干", "藏支", "藏于", "伏藏")),
    ("MULTIPLICITY_OR_COMPETITION", ("争合", "妒合", "两干合一", "一干合两", "多合", "重合", "竞合")),
    ("COEXISTING_RELATION", ("贪合忘冲", "合冲并见", "冲合", "刑冲合害", "刑合", "并见", "并存")),
    ("CLASH_OR_RELEASE", ("解冲", "冲开", "冲散", "冲破", "破合", "冲去", "解除", "解合")),
    ("ORDER_OR_PROXIMITY", ("紧贴", "贴近", "相邻", "隔位", "远近", "次序", "顺序", "先合", "先冲", "年上", "月上", "日干", "时上")),
    ("TEMPORAL_CONTEXT", ("岁运", "大运", "流年", "流月", "岁来", "运来", "行运", "太岁")),
    ("STRENGTH_GRADE", ("旺衰", "身旺", "身弱", "强弱", "有力", "无力", "得势", "失势")),
)


def _dependency_tags(text: str, families: list[str], gaps: list[str]) -> list[str]:
    tags = [name for name, terms in DEPENDENCY_PATTERNS if _contains_any(text, terms)]
    if "干支暗合" in text:
        tags.append("SOURCE_TERM_GANZHI_ANHE_UNRESOLVED")
    elif "暗合" in text:
        tags.append("SOURCE_MODIFIER_ANHE_UNRESOLVED")
    if _contains_any(text, ("合化", "化神", "化气", "化成", "成化", "化局")):
        tags.append("TRANSFORMATION")
    if _contains_any(text, ("合而不化", "不化", "合绊", "羁绊", "合去", "合住", "不以合论", "合而不合")):
        tags.append("NON_TRANSFORMATION_OR_BINDING")
    if any("PUNISHMENT" in family for family in families) or "刑" in text:
        tags.append("PUNISHMENT")
    if gaps:
        tags.append("RUNTIME_RELATION_GAP")
    return sorted(set(tags))


def _source_role(metadata: dict[str, Any], record_type: str) -> str:
    for key in ("CLAUSE_ROLE", "SOURCE_LAYER", "RESULT_OCCURRENCE_ROLE", "SOURCE_AUTHOR_COORDINATE"):
        value = metadata.get(key)
        if isinstance(value, str) and value:
            return f"{key}:{value}"
    return record_type


def _statement_classes(
    text: str,
    metadata: dict[str, Any],
    families: list[str],
    gaps: list[str],
    tags: list[str],
    record_type: str,
) -> tuple[str, list[str], str, list[str]]:
    classes: set[str] = set()
    role = " ".join(
        str(metadata.get(key, ""))
        for key in ("CLAUSE_ROLE", "SOURCE_LAYER", "LOGICAL_OPERATOR_TAGS", "STATUS")
    )
    example = (
        _contains_any(text[:12], ("例如", "比如", "又如", "如：", "命例", "譬如", "假如"))
        or len(GANZHI.findall(text)) >= 4
        or "EXAMPLE" in role
        or "CASE_FACT" in role
    )
    conflict = bool(metadata.get("CONFLICT_ID")) or _contains_any(
        text + role,
        (
            "异说",
            "异版",
            "另一说",
            "一说",
            "两说",
            "或谓",
            "有谓",
            "不同版本",
            "来源冲突",
            "CONFLICT",
            "ALTERNATIVE_SOURCE",
        ),
    )
    ambiguous = _contains_any(
        text + role,
        ("待考", "未详", "不明", "未定", "存疑", "疑字", "OCR", "UNKNOWN", "AMBIGUOUS"),
    )
    if gaps:
        classes.add("RUNTIME_RELATION_GAP")
    if example:
        classes.add("EXAMPLE_ONLY")
    if conflict:
        classes.add("CONTRADICTORY_OR_ALTERNATIVE_STATEMENT")
    if ambiguous:
        classes.add("AMBIGUOUS")
    if "NON_TRANSFORMATION_OR_BINDING" in tags:
        classes.add("NON_TRANSFORMATION_OR_BINDING_CONDITION")
    if "TRANSFORMATION" in tags:
        classes.add("TRANSFORMATION_CONDITION")
    if "MONTH_COMMAND_OR_SEASON" in tags:
        classes.add("SEASONAL_OR_MONTH_COMMAND_DEPENDENCY")
    if "ROOT_OR_SUPPORT" in tags:
        classes.add("ROOT_OR_SUPPORT_DEPENDENCY")
    if "EXPOSURE_OR_HIDDEN_STEM" in tags:
        classes.add("EXPOSURE_OR_HIDDEN_STEM_DEPENDENCY")
    if "MULTIPLICITY_OR_COMPETITION" in tags:
        classes.add("MULTIPLICITY_OR_COMPETITION")
    if "COEXISTING_RELATION" in tags:
        classes.add("COEXISTING_RELATION_DEPENDENCY")
    if "CLASH_OR_RELEASE" in tags:
        classes.add("CLASH_OR_RELEASE_DEPENDENCY")
    if "PUNISHMENT" in tags:
        classes.add("PUNISHMENT_DEPENDENCY")
    if "ORDER_OR_PROXIMITY" in tags:
        classes.add("ORDER_OR_PROXIMITY_DEPENDENCY")
    if "TEMPORAL_CONTEXT" in tags:
        classes.add("TEMPORAL_CONTEXT_HINT")
    if _contains_any(text, ("若", "须", "必须", "方能", "乃能", "才", "条件", "逢", "见")):
        classes.add("ELIGIBILITY_CONDITION")
    if _contains_any(text, ("但", "惟", "唯", "除", "否则", "不可", "不能", "不宜", "非真", "不作")):
        classes.add("EXCEPTION_OR_LIMIT")
    if _contains_any(text, ("故", "所以", "因此", "则", "遂", "使", "成为", "结果", "主")):
        classes.add("RESULT_OR_EFFECT_STATEMENT")
    if "COMMENTARY" in role or record_type.startswith("PLAIN") and not metadata:
        classes.add("COMMENTARY_OR_EXPLANATION")
    if not classes:
        classes.add("DEFINITION_OR_NOMINAL_RELATION")

    priority = (
        "RUNTIME_RELATION_GAP",
        "CONTRADICTORY_OR_ALTERNATIVE_STATEMENT",
        "AMBIGUOUS",
        "EXAMPLE_ONLY",
        "NON_TRANSFORMATION_OR_BINDING_CONDITION",
        "TRANSFORMATION_CONDITION",
        "MULTIPLICITY_OR_COMPETITION",
        "CLASH_OR_RELEASE_DEPENDENCY",
        "SEASONAL_OR_MONTH_COMMAND_DEPENDENCY",
        "ROOT_OR_SUPPORT_DEPENDENCY",
        "EXPOSURE_OR_HIDDEN_STEM_DEPENDENCY",
        "COEXISTING_RELATION_DEPENDENCY",
        "PUNISHMENT_DEPENDENCY",
        "ORDER_OR_PROXIMITY_DEPENDENCY",
        "TEMPORAL_CONTEXT_HINT",
        "EXCEPTION_OR_LIMIT",
        "ELIGIBILITY_CONDITION",
        "RESULT_OR_EFFECT_STATEMENT",
        "COMMENTARY_OR_EXPLANATION",
        "DEFINITION_OR_NOMINAL_RELATION",
    )
    primary = next(item for item in priority if item in classes)
    review = "REVIEWED_R1"
    labels: list[str] = []
    if conflict:
        review = "CONFLICT_REQUIRES_REVIEW"
        labels = ["ALTERNATIVE_SOURCE_STATEMENT", "PROFILE_CANDIDATE", "CONFLICT_REQUIRES_REVIEW"]
    elif ambiguous:
        review = "SOURCE_SEMANTICS_AMBIGUOUS"
    elif gaps:
        review = "RUNTIME_RELATION_GAP_DEFERRED"
    return primary, sorted(classes - {primary}), review, labels


def _runtime_dependency_map(
    families: list[str], gaps: list[str], tags: list[str], text: str
) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    missing: set[str] = set()

    def add(primitive: str, status: str, rationale: str) -> None:
        if not any(row["primitive"] == primitive for row in rows):
            rows.append({"primitive": primitive, "status": status, "rationale": rationale})

    released_families = [family for family in families if family in CURRENT_RELATION_FAMILIES]
    if released_families:
        add(
            "EXACT_RAW_RELATION_OCCURRENCES",
            "AVAILABLE_EXACTLY",
            "Released Natal and Structural relation occurrences preserve exact relation and participant IDs.",
        )
        add(
            "EXACT_STEM_BRANCH_OCCURRENCE_IDS",
            "AVAILABLE_EXACTLY",
            "Occurrence-scoped StemInstance and BranchInstance identities are released.",
        )
    if "CROSS_FAMILY_RELATION_LIFECYCLE" in families:
        add(
            "CROSS_FAMILY_RELATION_CONTEXT",
            "PARTIALLY_AVAILABLE",
            "The passage is relation-lifecycle relevant but does not identify one released exact relation family.",
        )
    for gap in gaps:
        add(
            f"RELATION_REGISTRY:{gap}",
            "OUTSIDE_CURRENT_RELATION_REGISTRY",
            "The source relation family is recorded for audit only and is not released by the current registry.",
        )

    if "MONTH_COMMAND_OR_SEASON" in tags:
        if "流月" in text or _contains_any(text, ("当前月", "行运月", "岁运月")):
            add(
                "ACTIVE_FLOW_SOLAR_MONTH",
                "AVAILABLE_EXACTLY",
                "The active Flow solar month is separately typed and does not replace Natal month command.",
            )
        elif "月令" in text:
            add(
                "NATAL_MONTH_COMMAND",
                "AVAILABLE_EXACTLY",
                "The fixed Natal month-command branch occurrence is released.",
            )
        else:
            add(
                "SEASONAL_ROLE_SELECTION",
                "SOURCE_SEMANTICS_AMBIGUOUS",
                "The passage does not identify whether the seasonal role is Natal or active Flow context.",
            )
    if "ROOT_OR_SUPPORT" in tags:
        add(
            "EXACT_HIDDEN_STEM_MATCH",
            "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
            "Exact hidden-stem membership/support is neutral evidence, not a root verdict or grade.",
        )
        add(
            "SAME_ELEMENT_HIDDEN_SUPPORT",
            "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
            "Same-element support is neutral evidence and cannot establish strength.",
        )
        missing.add("ROOT_OR_SUPPORT_GRADE")
    if "EXPOSURE_OR_HIDDEN_STEM" in tags:
        add(
            "HIDDEN_STEM_MEMBERSHIP_AND_EXPOSURE",
            "AVAILABLE_EXACTLY",
            "Hidden-stem membership and exact exposure links are released without weights.",
        )
    if "MULTIPLICITY_OR_COMPETITION" in tags:
        add(
            "RELATION_INCIDENCE_EXACT_TOPOLOGY",
            "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
            "Degree and SHARED_PARTICIPANT/DISJOINT are exact topology, not competition or dominance.",
        )
        missing.add("CLASSICAL_COMPETITION_SEMANTICS")
    if "COEXISTING_RELATION" in tags:
        add(
            "RELATION_INCIDENCE_EXACT_TOPOLOGY",
            "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
            "Coexisting exact relation sets and pair topology exist without interaction precedence.",
        )
        missing.add("COEXISTING_RELATION_PRECEDENCE")
    if "CLASH_OR_RELEASE" in tags:
        add(
            "RELATION_TRANSITION_BEFORE_AFTER",
            "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
            "PERSISTING/ENTERED/EXITED are exact set changes and are not release or cancellation verdicts.",
        )
        missing.add("CLASH_RELEASE_OR_CANCELLATION_SEMANTICS")
    if "ORDER_OR_PROXIMITY" in tags:
        add(
            "PARTICIPANT_POSITION_LINEAGE",
            "PARTIALLY_AVAILABLE",
            "Occurrence IDs retain pillar/frame positions but no Classical proximity/ordering primitive is released.",
        )
        missing.add("CLASSICAL_ORDER_OR_PROXIMITY")
    if "TEMPORAL_CONTEXT" in tags:
        add(
            "DAYUN_ANNUAL_MONTHLY_FRAME_CONTEXT",
            "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
            "Typed active frames and neutral frame-change evidence exist without temporal priority.",
        )
        missing.add("TEMPORAL_LAYER_PRIORITY_SEMANTICS")
    if "STRENGTH_GRADE" in tags:
        add(
            "STRENGTH_OR_WANGSHUAI_GRADE",
            "MISSING_PRIMITIVE",
            "No strength, Wangshuai, or Day-Master-strength evaluator is released.",
        )
        missing.add("STRENGTH_OR_WANGSHUAI_GRADE")
    if "TRANSFORMATION" in tags:
        add(
            "TRANSFORMATION_SUCCESS",
            "MISSING_PRIMITIVE",
            "Nominal transformation metadata does not establish successful transformation.",
        )
        missing.add("TRANSFORMATION_SUCCESS")
    if "NON_TRANSFORMATION_OR_BINDING" in tags:
        add(
            "BINDING_OR_NON_TRANSFORMATION_OUTCOME",
            "MISSING_PRIMITIVE",
            "The current runtime publishes no binding or failed-transformation evaluator.",
        )
        missing.add("BINDING_OR_NON_TRANSFORMATION_OUTCOME")
    if "PUNISHMENT" in tags and families:
        add(
            "RAW_PUNISHMENT_OCCURRENCE",
            "AVAILABLE_EXACTLY",
            "Released punishment occurrence IDs preserve participant identity and direction where applicable.",
        )
        missing.add("PUNISHMENT_INTERACTION_OR_PRECEDENCE")
    if "SOURCE_MODIFIER_ANHE_UNRESOLVED" in tags:
        add(
            "SOURCE_MODIFIER:ANHE_UNRESOLVED",
            "SOURCE_SEMANTICS_AMBIGUOUS",
            "The literal 暗 modifier is retained for source audit without inferring a hidden-stem participant or HIDDEN_COMBINATION runtime relation.",
        )
        missing.add("SOURCE_MODIFIER:ANHE_UNRESOLVED")
    if "SOURCE_TERM_GANZHI_ANHE_UNRESOLVED" in tags:
        add(
            "SOURCE_TERM:GANZHI_ANHE_UNRESOLVED",
            "SOURCE_SEMANTICS_AMBIGUOUS",
            "The explicit 干支暗合 term is retained separately for future source research and does not inherit the bare 暗合 rule.",
        )
        missing.add("SOURCE_TERM:GANZHI_ANHE_UNRESOLVED")
    return sorted(rows, key=lambda row: row["primitive"]), sorted(missing)


def _is_candidate(
    text: str,
    heading: str,
    families: list[str],
    gaps: list[str],
    tags: list[str],
    discovered_vocabulary: Iterable[str] = (),
) -> bool:
    if not text or text.startswith("#") or text in {"```", "```text", "```json", "```jsonl"}:
        return False
    relation_signal = _contains_any(
        text,
        (
            "五合", "六合", "六冲", "三合", "相合", "暗合", "相冲", "相穿", "冲破", "冲开", "冲散", "解冲", "刑冲", "刑合", "相刑", "三刑", "自刑", "带刑", "合化",
            "合而", "争合", "妒合", "甲己", "乙庚", "丙辛", "丁壬", "戊癸",
            "子丑", "寅亥", "卯戌", "辰酉", "巳申", "午未",
        ),
    ) or bool(re.search(r"冲(?!突)", text))
    contextual = bool(families or gaps) and bool(tags) and len(text.strip()) >= 3
    discovered_signal = _contains_any(text, discovered_vocabulary)
    return relation_signal or contextual or discovered_signal


def _participant_kind(families: list[str], gaps: list[str]) -> str:
    all_families = families + gaps
    has_stem = "STEM_FIVE_COMBINATION" in all_families
    has_branch = any(item.startswith("BRANCH_") for item in all_families)
    if has_stem and has_branch:
        return "MIXED"
    if has_stem:
        return "STEM"
    if has_branch:
        return "BRANCH"
    return "OTHER"


def _excerpt(text: str, limit: int = 240) -> str:
    return text if len(text) <= limit else text[:limit]


def _heading_path(headings: dict[int, str]) -> str:
    return " / ".join(headings[level] for level in sorted(headings))


def _build_records(
    root: Path, index: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    line_rows: list[dict[str, Any]] = []
    segment_states: dict[str, dict[str, Any]] = {}
    headings: dict[int, str] = {}
    discovered: set[str] = set()

    # Pass 1: consume every indexed line, retain exact locators, and derive a
    # closed vocabulary only from explicitly typed source term-control rows.
    for segment in index["segments"]:
        payload = (root / segment["path"]).read_bytes()
        lines = payload.decode("utf-8", errors="strict").splitlines(keepends=True)
        local_offset = 0
        segment_discoveries: list[str] = []
        for local_line_number, line in enumerate(lines, start=1):
            line_bytes = line.encode("utf-8")
            canonical_line = segment["line_start"] + local_line_number - 1
            canonical_byte_start = segment["byte_start"] + local_offset
            canonical_byte_end = canonical_byte_start + len(line_bytes)
            local_offset += len(line_bytes)

            stripped = line.rstrip("\r\n")
            heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
            if heading_match:
                level = len(heading_match.group(1))
                headings[level] = heading_match.group(2)
                for deeper in tuple(key for key in headings if key > level):
                    del headings[deeper]

            _, _, metadata = _extract_text(line)
            heading = _heading_path(headings)
            term = _discover_control_term(metadata)
            if term is not None and term not in discovered:
                discovered.add(term)
                segment_discoveries.append(term)
            line_rows.append(
                {
                    "segment": segment,
                    "line": line,
                    "line_bytes": line_bytes,
                    "heading": heading,
                    "local_line_number": local_line_number,
                    "canonical_line": canonical_line,
                    "canonical_byte_start": canonical_byte_start,
                    "canonical_byte_end": canonical_byte_end,
                }
            )

        if local_offset != len(payload):
            raise TrainingError(f"evidence audit segment byte replay failed: {segment['segment_id']}")
        segment_states[segment["segment_id"]] = {
            "segment": segment,
            "line_count": len(lines),
            "byte_count": len(payload),
            "candidate_count": 0,
            "families": set(),
            "discoveries": sorted(set(segment_discoveries)),
        }

    vocabulary = tuple(sorted(discovered))
    records: list[dict[str, Any]] = []
    vocabulary_only_count = 0

    # Pass 2: replay all retained lines in the same index order and expand the
    # seed candidate predicate with the complete pass-1 vocabulary closure.
    for row in line_rows:
        segment = row["segment"]
        state = segment_states[segment["segment_id"]]
        source_views = _source_views(row["line"])
        for view_index, (text, record_type, metadata, pairing_role) in enumerate(
            source_views
        ):
            analysis_text = text
            if metadata.get("CONFLICT_ID"):
                analysis_text = " ".join(
                    [text]
                    + [
                        value
                        for value in metadata.values()
                        if isinstance(value, str) and re.search(r"[\u3400-\u9fff]", value)
                    ]
                )
            families, gaps = _relation_families(analysis_text, row["heading"])
            tags = _dependency_tags(analysis_text, families, gaps)
            forced_conflict_candidate = bool(metadata.get("CONFLICT_ID"))
            seed_candidate = forced_conflict_candidate or _is_candidate(
                analysis_text, row["heading"], families, gaps, tags
            )
            expanded_candidate = forced_conflict_candidate or _is_candidate(
                analysis_text,
                row["heading"],
                families,
                gaps,
                tags,
                vocabulary,
            )
            if not expanded_candidate:
                continue
            if not seed_candidate:
                vocabulary_only_count += 1
            if not families and not gaps:
                families = ["CROSS_FAMILY_RELATION_LIFECYCLE"]
            state["families"].update(families)
            state["families"].update(gaps)
            state["candidate_count"] += 1

            primary, secondary, review, profile_labels = _statement_classes(
                analysis_text, metadata, families, gaps, tags, record_type
            )
            dependencies, missing = _runtime_dependency_map(
                families, gaps, tags, analysis_text
            )
            passage_hash = _sha256(row["line_bytes"])
            evidence_suffix = passage_hash[:12]
            if view_index:
                evidence_suffix = _sha256(
                    row["line_bytes"] + b"\0" + record_type.encode("utf-8")
                )[:12]
            evidence_id = (
                f"S14-EV-L{row['canonical_line']:05d}-{evidence_suffix}"
            )
            conflict_id = metadata.get("CONFLICT_ID")
            records.append(
                {
                    "evidence_id": evidence_id,
                    "source_id": SOURCE_ID,
                    "canonical_source_path": index["source"]["canonical_path"],
                    "canonical_source_sha256": index["source"]["canonical_sha256"],
                    "access_segment_id": segment["segment_id"],
                    "access_segment_path": segment["path"],
                    "access_segment_sha256": segment["sha256"],
                    "canonical_line_start": row["canonical_line"],
                    "canonical_line_end": row["canonical_line"],
                    "segment_local_line_start": row["local_line_number"],
                    "segment_local_line_end": row["local_line_number"],
                    "canonical_byte_start": row["canonical_byte_start"],
                    "canonical_byte_end_exclusive": row["canonical_byte_end"],
                    "passage_includes_line_ending": row["line"].endswith(("\n", "\r")),
                    "passage_sha256": passage_hash,
                    "source_heading_path": row["heading"],
                    "source_record_type": record_type,
                    "source_role": _source_role(metadata, record_type),
                    "source_conflict_id": (
                        conflict_id if isinstance(conflict_id, str) and conflict_id else None
                    ),
                    "source_pairing_role": pairing_role,
                    "exact_excerpt": _excerpt(text),
                    "excerpt_is_complete_source_record_text": len(text) <= 240,
                    "relation_families": families + gaps,
                    "participant_kind": _participant_kind(families, gaps),
                    "statement_class": primary,
                    "secondary_statement_classes": secondary,
                    "condition_dependency_tags": tags,
                    "conflict_group_ids": [],
                    "alternative_profile_labels": profile_labels,
                    "runtime_dependency_map": dependencies,
                    "runtime_gap_tags": sorted(set(gaps + missing)),
                    "review_status": review,
                    "audit_notes": "Source bytes are authoritative; classifications are audit metadata only.",
                }
            )

    coverage: list[dict[str, Any]] = []
    for segment in index["segments"]:
        state = segment_states[segment["segment_id"]]
        coverage.append(
            {
                "segment_id": segment["segment_id"],
                "segment_path": segment["path"],
                "segment_sha256": segment["sha256"],
                "sequence": segment["sequence"],
                "canonical_line_start": segment["line_start"],
                "canonical_line_end": segment["line_end_inclusive"],
                "scanned_line_count": state["line_count"],
                "scanned_byte_count": state["byte_count"],
                "candidate_passage_count": state["candidate_count"],
                "relation_family_terms_encountered": sorted(state["families"]),
                "new_vocabulary_discovered": state["discoveries"],
                "scan_status": "COMPLETE",
                "review_completion_state": "COMPLETE_R1",
            }
        )
    discovery = {
        "seed_candidate_rule_id": "S14_RELATION_SIGNAL_AND_TYPED_DEPENDENCY_R1",
        "pass1_control_derivation_rule_id": "S14_TYPED_TECHNICAL_TERM_RELATION_MORPHEME_R1",
        "pass1_control_field": DISCOVERY_CONTROL_FIELD,
        "pass1_control_role": DISCOVERY_CONTROL_ROLE,
        "pass1_relation_morphemes": list(DISCOVERY_RELATION_MORPHEMES),
        "pass1_discovered_terms": list(vocabulary),
        "vocabulary_closure_sha256": _vocabulary_closure_sha256(vocabulary),
        "pass2_vocabulary_only_record_count": vocabulary_only_count,
    }
    return records, coverage, discovery


def _bind_conflict_groups(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_source_conflict_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        source_conflict_id = record.get("source_conflict_id")
        if (
            isinstance(source_conflict_id, str)
            and source_conflict_id
            and record["review_status"] == "CONFLICT_REQUIRES_REVIEW"
        ):
            by_source_conflict_id[source_conflict_id].append(record)
    groups: list[dict[str, Any]] = []
    for source_conflict_id, linked in sorted(by_source_conflict_id.items()):
        pairing_roles = {
            record.get("source_pairing_role")
            for record in linked
            if record.get("source_pairing_role")
        }
        if len(linked) < 2 or len(pairing_roles) < 2:
            continue
        common_families = set(linked[0]["relation_families"])
        for record in linked[1:]:
            common_families.intersection_update(record["relation_families"])
        relation_family = (
            sorted(common_families)[0]
            if common_families
            else "CROSS_FAMILY_RELATION_LIFECYCLE"
        )
        safe_source_id = re.sub(r"[^A-Za-z0-9._-]", "-", source_conflict_id)
        group_id = f"S14-CONFLICT-{safe_source_id}"
        evidence_ids = sorted({record["evidence_id"] for record in linked})
        groups.append(
            {
                "conflict_group_id": group_id,
                "source_conflict_id": source_conflict_id,
                "linkage_basis": "SHARED_EXPLICIT_SOURCE_CONFLICT_ID_AND_DISTINCT_SOURCE_ROLES",
                "relation_family": relation_family,
                "evidence_ids": evidence_ids,
                "resolution_status": "UNRESOLVED_PROFILE_REVIEW_REQUIRED",
            }
        )
        for record in linked:
            record["conflict_group_ids"].append(group_id)
    return groups


def _counter(records: list[dict[str, Any]], field: str) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for record in records:
        value = record[field]
        if isinstance(value, list):
            counter.update(value)
        else:
            counter[value] += 1
    return dict(sorted(counter.items()))


def _build_report(matrix: dict[str, Any], coverage: dict[str, Any]) -> str:
    summary = matrix["summary"]
    lines = [
        "# Bazi Classical Relation Lifecycle Evidence Matrix R1 — Dependency / Gap Report",
        "",
        "Status: source-grounded audit artifact; no Classical lifecycle semantic evaluator is released.",
        "",
        "## Authority and coverage",
        "",
        f"- Source: `S14` / `{matrix['authority']['canonical_source_sha256']}`",
        f"- Canonical bytes: `{matrix['authority']['canonical_source_bytes']}`",
        f"- Access segments reviewed in index order: `{coverage['summary']['terminal_segment_count']}/{coverage['summary']['segment_count']}`",
        f"- Evidence records: `{summary['evidence_record_count']}`",
        f"- Conflict groups: `{summary['source_conflict_group_count']}`",
        f"- Unresolved one-sided conflict records: `{summary['unresolved_one_sided_conflict_record_count']}`",
        f"- Profile-candidate records: `{summary['profile_candidate_record_count']}`",
        f"- Pass-1 vocabulary closure: `{', '.join(matrix['method']['vocabulary_expansion']['pass1_discovered_terms'])}`",
        f"- Pass-2 vocabulary-only records: `{matrix['method']['vocabulary_expansion']['pass2_vocabulary_only_record_count']}`",
        "- Coverage claim: exhaustive for the declared R1 scan method and target relation/lifecycle scope, not for every Bazi doctrine.",
        "",
        "## Evidence distribution",
        "",
        "### Primary statement classes",
        "",
        "| Statement class | Records |",
        "|---|---:|",
    ]
    for statement_class, count in summary["statement_class_counts"].items():
        lines.append(f"| `{statement_class}` | {count} |")
    lines.extend(
        [
            "",
            "### Relation families",
            "",
            "| Relation family | Records |",
            "|---|---:|",
        ]
    )
    for family, count in summary["relation_family_counts"].items():
        lines.append(f"| `{family}` | {count} |")
    lines.extend(
        [
        "",
        "## Dependency findings",
        "",
        "| Candidate family | Current exact input | Neutral-only input | Missing / unresolved | Recommended next slice |",
        "|---|---|---|---|---|",
        "| Stem combination eligibility / transformation | Stem occurrence IDs and raw Five-Combination occurrences | Month/support/exposure references | transformation success, binding, competition, profile choice | profile-explicit eligibility candidates without outcome verdicts |",
        "| Branch harmony / complete trine | Exact Liuhe and complete-Sanhe occurrences | seasonal/support context | successful state change and precedence | candidate-preserving harmony eligibility schema |",
        "| Clash interaction | Exact clash occurrences and BEFORE/AFTER sets | `PERSISTING/ENTERED/EXITED` frame-change evidence | release/cancellation/rescue semantics | separate clash-interaction evidence issue |",
        "| Punishment interaction | Exact Zi-Mao, directed, and self-punishment occurrences | coexisting relation topology | precedence, suppression, result semantics | punishment-specific profile audit |",
        "| Multiplicity / shared participant | exact incidence degree and `SHARED_PARTICIPANT/DISJOINT` | topology is neutral | competition/dominance/winner semantics | source-profile competition candidates |",
        "| Month / season | `NATAL_MONTH_COMMAND` and separate `ACTIVE_FLOW_SOLAR_MONTH` | support-touch references | seasonal strength and role ambiguity | retain typed roles; add no score |",
        "| Root / support / exposure | hidden-stem membership and exact exposure | `EXACT_HIDDEN_STEM_MATCH`, `SAME_ELEMENT_HIDDEN_SUPPORT` | root/strength grades | independent root semantics issue |",
        "| Temporal layer | Dayun/Annual/Monthly frame identities | neutral frame-change evidence | automatic layer priority | profile-explicit temporal interaction issue |",
        "| Unreleased relation families | none in current registry | none | Harm, Break, partial trine, directional triad, hidden combination | separate registry-governance issues only |",
        "| Literal `暗合` modifier | ordinary released relation identity where independently explicit | exact source text | meaning of `暗`; no hidden-stem participant inference | source-semantics review only |",
        "",
        "## Missing primitives",
        "",
        ]
    )
    for primitive, count in summary["runtime_gap_tag_counts"].items():
        lines.append(f"- `{primitive}`: {count} evidence record(s)")
    lines.extend(
        [
            "",
            "## Source conflicts and profile candidates",
            "",
            "Alternative and contradictory statements are linked only when a shared explicit source conflict identifier and distinct source-side roles prove the pairing. One-sided conflict markers remain `CONFLICT_REQUIRES_REVIEW` without an invented counterpart. No majority vote, chronology guess, or universal default is selected. Records marked `PROFILE_CANDIDATE` require a later CHAT design decision.",
            "",
            "## Semantic boundary",
            "",
            "This audit does not rename neutral runtime facts. In particular, source-faithful `相穿` is `BRANCH_CHUAN`, not an inferred `BRANCH_HARM`; bare `暗合` retains an unresolved literal source modifier and does not prove hidden-stem participants; participant degree is not strength; `SHARED_PARTICIPANT` is not competition; `ENTERED` is not activation; `EXITED` is not release or cancellation; and active Flow month never replaces Natal month command.",
            "",
            "No canonical source, model-learning, training state, prediction control, relation registry, or existing Natal/Temporal/Flow/Structural/Support/Incidence/Transition semantic contract is changed by this artifact.",
            "",
        ]
    )
    return "\n".join(lines)


def build_classical_relation_evidence(root: Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    root = root.resolve()
    access = validate_source_access(root, require_source_commit=False)
    if (
        access["status"] != "PASS"
        or access["source_id"] != SOURCE_ID
        or access["canonical_bytes"] != EXPECTED_SOURCE_BYTES
        or access["canonical_sha256"] != EXPECTED_SOURCE_SHA256
        or access["segment_count"] != EXPECTED_SEGMENT_COUNT
        or access["round_trip_exact"] is not True
    ):
        raise TrainingError("classical relation evidence audit source-access gate failed")
    index = load_json(root / DERIVED_ACCESS_ROOT / SOURCE_ID / "index.json")
    if index["source"]["canonical_path"] != EXPECTED_SOURCE_PATH:
        raise TrainingError("classical relation evidence audit canonical path mismatch")
    records, segment_rows, discovery = _build_records(root, index)
    conflict_groups = _bind_conflict_groups(records)
    if not records:
        raise TrainingError("classical relation evidence audit found no target evidence")

    summary = {
        "evidence_record_count": len(records),
        "statement_class_counts": _counter(records, "statement_class"),
        "relation_family_counts": _counter(records, "relation_families"),
        "review_status_counts": _counter(records, "review_status"),
        "runtime_gap_tag_counts": _counter(records, "runtime_gap_tags"),
        "source_conflict_group_count": len(conflict_groups),
        "unresolved_one_sided_conflict_record_count": sum(
            record["review_status"] == "CONFLICT_REQUIRES_REVIEW"
            and not record["conflict_group_ids"]
            for record in records
        ),
        "profile_candidate_record_count": sum(
            "PROFILE_CANDIDATE" in record["alternative_profile_labels"]
            for record in records
        ),
    }
    matrix = {
        "schema": AUDIT_ID,
        "audit_id": AUDIT_ID,
        "authority": {
            "source_id": SOURCE_ID,
            "canonical_source_path": EXPECTED_SOURCE_PATH,
            "canonical_source_bytes": EXPECTED_SOURCE_BYTES,
            "canonical_source_sha256": EXPECTED_SOURCE_SHA256,
            "source_access_index_path": f"sources/derived-access/{SOURCE_ID}/index.json",
            "source_access_index_sha256": _sha256(
                (root / DERIVED_ACCESS_ROOT / SOURCE_ID / "index.json").read_bytes()
            ),
            "canonical_source_is_sole_authority": True,
            "prediction_source_selection_allowed": False,
        },
        "scope": {
            "artifact_role": "SOURCE_GROUNDED_EVIDENCE_AND_DEPENDENCY_AUDIT_ONLY",
            "semantic_evaluator_released": False,
            "current_runtime_relation_families": list(CURRENT_RELATION_FAMILIES),
            "runtime_gap_families": list(RUNTIME_GAP_FAMILIES),
            "audit_meta_relation_families": list(AUDIT_META_RELATION_FAMILIES),
        },
        "method": {
            "algorithm_id": "S14_INDEX_ORDER_FULL_LINE_TWO_PASS_AUDIT_R1",
            "all_indexed_segments_processed": True,
            "all_lines_considered": True,
            "format_support": ["MARKDOWN", "PLAIN_TEXT", "JSONL", "TSV", "CONTROL_ROWS"],
            "vocabulary_expansion": discovery,
            "coverage_claim_limit": "TARGET_RELATION_AND_LIFECYCLE_SCOPE_ONLY",
        },
        "closed_vocabularies": {
            "statement_classes": list(STATEMENT_CLASSES),
            "runtime_dependency_statuses": list(RUNTIME_STATUSES),
            "review_statuses": list(REVIEW_STATUSES),
        },
        "conflict_groups": conflict_groups,
        "records": records,
        "summary": summary,
    }
    coverage = {
        "schema": "BAZI-CLASSICAL-RELATION-LIFECYCLE-EVIDENCE-COVERAGE-R1",
        "audit_id": AUDIT_ID,
        "source_id": SOURCE_ID,
        "canonical_source_sha256": EXPECTED_SOURCE_SHA256,
        "index_path": f"sources/derived-access/{SOURCE_ID}/index.json",
        "segments": segment_rows,
        "summary": {
            "segment_count": len(segment_rows),
            "terminal_segment_count": sum(
                row["scan_status"] == "COMPLETE"
                and row["review_completion_state"] == "COMPLETE_R1"
                for row in segment_rows
            ),
            "total_scanned_lines": sum(row["scanned_line_count"] for row in segment_rows),
            "total_scanned_bytes": sum(row["scanned_byte_count"] for row in segment_rows),
            "total_candidate_passages": sum(
                row["candidate_passage_count"] for row in segment_rows
            ),
            "all_segments_terminal": all(
                row["scan_status"] == "COMPLETE"
                and row["review_completion_state"] == "COMPLETE_R1"
                for row in segment_rows
            ),
        },
    }
    return matrix, coverage, _build_report(matrix, coverage)


def write_classical_relation_evidence(root: Path) -> dict[str, Any]:
    matrix, coverage, report = build_classical_relation_evidence(root)
    atomic_write_json(root / MATRIX_PATH, matrix)
    atomic_write_json(root / COVERAGE_PATH, coverage)
    atomic_write_bytes(root / REPORT_PATH, report.encode("utf-8"))
    return {
        "status": "BUILT",
        "audit_id": AUDIT_ID,
        "matrix_path": MATRIX_PATH.as_posix(),
        "coverage_path": COVERAGE_PATH.as_posix(),
        "report_path": REPORT_PATH.as_posix(),
        **matrix["summary"],
        "segment_count": coverage["summary"]["segment_count"],
        "all_segments_terminal": coverage["summary"]["all_segments_terminal"],
    }


def _validate_schema(root: Path, schema_path: Path, value: dict[str, Any]) -> None:
    schema = load_json(root / schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(item) for item in error.path) or "<root>"
        raise TrainingError(f"classical relation evidence schema failed at {location}: {error.message}")


def validate_classical_relation_evidence(root: Path) -> dict[str, Any]:
    root = root.resolve()
    expected_matrix, expected_coverage, expected_report = build_classical_relation_evidence(root)
    matrix = load_json(root / MATRIX_PATH)
    coverage = load_json(root / COVERAGE_PATH)
    try:
        report = (root / REPORT_PATH).read_text(encoding="utf-8")
    except OSError as exc:
        raise TrainingError("missing classical relation evidence dependency report") from exc
    _validate_schema(root, MATRIX_SCHEMA_PATH, matrix)
    _validate_schema(root, COVERAGE_SCHEMA_PATH, coverage)
    if matrix != expected_matrix or coverage != expected_coverage or report != expected_report:
        raise TrainingError("classical relation evidence artifacts are stale or non-deterministic")

    discovery = matrix["method"]["vocabulary_expansion"]
    coverage_vocabulary = sorted(
        {
            term
            for segment in coverage["segments"]
            for term in segment["new_vocabulary_discovered"]
        }
    )
    if (
        discovery["pass1_discovered_terms"] != coverage_vocabulary
        or discovery["vocabulary_closure_sha256"]
        != _vocabulary_closure_sha256(coverage_vocabulary)
    ):
        raise TrainingError("two-pass vocabulary closure replay failed")

    ids = {record["evidence_id"] for record in matrix["records"]}
    if len(ids) != len(matrix["records"]):
        raise TrainingError("duplicate classical relation evidence ID")
    groups = {group["conflict_group_id"]: group for group in matrix["conflict_groups"]}
    records_by_id = {record["evidence_id"]: record for record in matrix["records"]}
    for record in matrix["records"]:
        if any(group_id not in groups for group_id in record["conflict_group_ids"]):
            raise TrainingError("evidence record references an absent conflict group")
        payload = (root / record["canonical_source_path"]).read_bytes()[
            record["canonical_byte_start"] : record["canonical_byte_end_exclusive"]
        ]
        if _sha256(payload) != record["passage_sha256"]:
            raise TrainingError(f"evidence passage hash replay failed: {record['evidence_id']}")
        if record["canonical_source_sha256"] != EXPECTED_SOURCE_SHA256:
            raise TrainingError("evidence record canonical source binding mismatch")
        if any(
            row["status"] not in RUNTIME_STATUSES
            for row in record["runtime_dependency_map"]
        ):
            raise TrainingError("evidence record uses an open runtime status")
    for group in groups.values():
        if len(group["evidence_ids"]) < 2 or not set(group["evidence_ids"]).issubset(ids):
            raise TrainingError("conflict group evidence linkage is invalid")
        linked = [records_by_id[evidence_id] for evidence_id in group["evidence_ids"]]
        if (
            group["linkage_basis"]
            != "SHARED_EXPLICIT_SOURCE_CONFLICT_ID_AND_DISTINCT_SOURCE_ROLES"
            or {record["source_conflict_id"] for record in linked}
            != {group["source_conflict_id"]}
            or len({record["source_pairing_role"] for record in linked}) < 2
        ):
            raise TrainingError("conflict group source-side proof is invalid")
    if coverage["summary"] != {
        "segment_count": EXPECTED_SEGMENT_COUNT,
        "terminal_segment_count": EXPECTED_SEGMENT_COUNT,
        "total_scanned_lines": 15442,
        "total_scanned_bytes": EXPECTED_SOURCE_BYTES,
        "total_candidate_passages": len(matrix["records"]),
        "all_segments_terminal": True,
    }:
        raise TrainingError("classical relation evidence coverage is incomplete")
    if len({row["segment_id"] for row in coverage["segments"]}) != EXPECTED_SEGMENT_COUNT:
        raise TrainingError("classical relation evidence segment coverage is not exact")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "source_id": SOURCE_ID,
        "canonical_source_sha256": EXPECTED_SOURCE_SHA256,
        "segment_count": EXPECTED_SEGMENT_COUNT,
        "all_segments_terminal": True,
        **matrix["summary"],
    }

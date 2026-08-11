from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .source_access import DERIVED_ACCESS_ROOT
from .source_access_validator import validate_source_access
from .util import (
    TrainingError,
    atomic_write_bytes,
    atomic_write_json,
    load_json,
    object_sha256,
    sha256_file,
)


AUDIT_ID = "BAZI-CLASSICAL-RELATION-INTERACTION-ASSERTION-MATRIX-R1"
AUDIT_ROOT = Path("audits/bazi-classical-relation-interaction-assertion-matrix-r1")
MATRIX_PATH = AUDIT_ROOT / "matrix.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path(
    "schemas/bazi-classical-relation-interaction-assertion-matrix-r1.schema.json"
)

SOURCE_ID = "S14"
EXPECTED_SOURCE_PATH = "sources/canonical/S14_八字合冲刑害墓库与结构变化库.txt"
EXPECTED_SOURCE_BYTES = 3354845
EXPECTED_SOURCE_SHA256 = "b225e64fcf7238b27a634e653a6904403d518335aeca59372b32e02f4a560407"
SOURCE_ACCESS_INDEX_PATH = DERIVED_ACCESS_ROOT / SOURCE_ID / "index.json"

MANDATORY_SHEN_BLOCK_COUNTS = {
    "ZPZQ-B-09-003": 11,
    "ZPZQ-B-09-005": 2,
    "ZPZQ-B-09-007": 4,
    "ZPZQ-B-09-009": 5,
}
MANDATORY_SHEN_SOURCE_OCCURRENCE_IDS = tuple(
    source_occurrence_id
    for block_suffix, count in (("003", 11), ("005", 2), ("007", 4), ("009", 5))
    for source_occurrence_id in (
        f"ZPZQ-CL-09-{block_suffix}-{index:03d}" for index in range(1, count + 1)
    )
)
QTBJ_EXPLICIT_RELEASE_SOURCE_OCCURRENCE_IDS = (
    "QTBJ-CL-05347",
    "QTBJ-CL-05370",
)
MANDATORY_SOURCE_OCCURRENCE_IDS = (
    *MANDATORY_SHEN_SOURCE_OCCURRENCE_IDS,
    *QTBJ_EXPLICIT_RELEASE_SOURCE_OCCURRENCE_IDS,
)

ASSERTION_CLASSES = (
    "RESOLUTION_ASSERTION",
    "REVERSAL_OR_REAPPEARANCE_ASSERTION",
    "RESOLUTION_FAILURE_ASSERTION",
    "ATTENUATION_ASSERTION",
    "PARTICIPANT_ALLOCATION_ASSERTION",
    "PARTICIPANT_MEDIATED_RELEASE_ASSERTION",
)
SOURCE_ASSERTION_ROLES = (
    "CONTEXTUAL_QUESTION",
    "GENERAL_SOURCE_ASSERTION",
    "EXEMPLIFYING_SOURCE_ASSERTION",
    "SUMMARY_SOURCE_ASSERTION",
)
ACTOR_REFERENCE_KINDS = (
    "RELATION_PATTERN_ACTOR",
    "PARTICIPANT_OR_CONTEXT_ACTOR",
    "UNRESOLVED_ACTOR",
)
TARGET_REFERENCE_KINDS = (
    "SOURCE_NAMED_RELATION_OR_EFFECT_TARGET",
    "UNRESOLVED_TARGET",
)
MULTIPLICITY_SIGNALS = (
    "NONE",
    "EXPLICIT_SOURCE_MULTIPLICITY_AND_UNRESOLVED_ALLOCATION",
)
ALTERNATIVE_PATH_SIGNALS = (
    "NONE",
    "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS",
)
UNRESOLVED_SEMANTIC_REQUIREMENTS = (
    "CLASSICAL_RESOLUTION_SEMANTICS",
    "CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",
    "CLASSICAL_RESOLUTION_FAILURE_SEMANTICS",
    "CLASSICAL_ATTENUATION_GRADE",
    "CLASSICAL_PARTICIPANT_ALLOCATION",
    "CLASSICAL_PARTICIPANT_MEDIATED_RELEASE_SEMANTICS",
    "CLASSICAL_INTERACTION_CHAIN_RESOLUTION",
    "SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING",
    "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION",
)
NEUTRAL_RUNTIME_PRIMITIVES = (
    "EXACT_RAW_RELATION_OCCURRENCE_IDENTITY",
    "EXACT_PARTICIPANT_INSTANCE_IDENTITY",
    "RELATION_INCIDENCE_DEGREE",
    "RELATION_PAIR_TOPOLOGY",
    "EXACT_TEMPORAL_LAYER_FRAME",
    "RELATION_TRANSITION_SET_CHANGE",
)

NEUTRAL_RUNTIME_DEPENDENCY_REGISTRY: dict[str, dict[str, Any]] = {
    "EXACT_RAW_RELATION_OCCURRENCE_IDENTITY": {
        "contract_refs": [
            "src/fortune_training/bazi_chart/models.py:RelationCandidate.relation_id",
            "src/fortune_training/bazi_structural/models.py:DynamicRelationOccurrence.relation_id",
        ],
        "semantic_boundary": (
            "An immutable released raw relation identity is neutral evidence; its presence is not a "
            "Classical operative-effect verdict."
        ),
    },
    "EXACT_PARTICIPANT_INSTANCE_IDENTITY": {
        "contract_refs": [
            "src/fortune_training/bazi_chart/models.py:RelationCandidate.participant_instance_ids",
            "src/fortune_training/bazi_structural/models.py:DynamicRelationOccurrence.participant_instance_ids",
        ],
        "semantic_boundary": (
            "Exact participant identities permit future path enumeration but do not select an actor, "
            "target, allocation, or winner."
        ),
    },
    "RELATION_INCIDENCE_DEGREE": {
        "contract_refs": [
            "src/fortune_training/bazi_relation_incidence/models.py:ParticipantRelationIncidenceFact.relation_count",
        ],
        "semantic_boundary": (
            "Incidence degree preserves multiplicity only; it is not competition, dominance, or allocation."
        ),
    },
    "RELATION_PAIR_TOPOLOGY": {
        "contract_refs": [
            "src/fortune_training/bazi_relation_incidence/models.py:RelationPairTopologyFact.topology_kind",
            "src/fortune_training/bazi_relation_incidence/models.py:RelationPairTopologyFact.shared_participant_instance_ids",
        ],
        "semantic_boundary": (
            "SHARED_PARTICIPANT and DISJOINT are exact topology only; neither implies competition or a winner."
        ),
    },
    "EXACT_TEMPORAL_LAYER_FRAME": {
        "contract_refs": [
            "src/fortune_training/bazi_relation_incidence/models.py:RelationOccurrenceReference.participant_layers",
            "src/fortune_training/bazi_relation_incidence/models.py:IncidenceParticipantReference.source_frame_id",
        ],
        "semantic_boundary": (
            "A typed layer or frame is source-binding evidence and does not activate or suppress a relation."
        ),
    },
    "RELATION_TRANSITION_SET_CHANGE": {
        "contract_refs": [
            "src/fortune_training/bazi_relation_transition/models.py:RawRelationTransitionFact.transition_state",
        ],
        "semantic_boundary": (
            "PERSISTING, ENTERED, and EXITED replay raw set change only; EXITED is not Classical resolution."
        ),
    },
}


def _spec(
    *,
    role: str,
    primary: str,
    fragments: tuple[str, ...],
    participants: tuple[str, ...] = (),
    actor: str = "RELATION_PATTERN_ACTOR",
    target: str = "SOURCE_NAMED_RELATION_OR_EFFECT_TARGET",
    secondary: tuple[str, ...] = (),
    unresolved: tuple[str, ...] = (),
    temporal: bool = False,
) -> dict[str, Any]:
    return {
        "source_assertion_role": role,
        "primary_assertion_class": primary,
        "secondary_assertion_classes": secondary,
        "source_assertion_fragments": fragments,
        "source_named_participant_patterns": participants,
        "source_named_relation_or_effect_patterns": fragments,
        "actor_reference_kind": actor,
        "target_reference_kind": target,
        "unresolved_semantic_requirements": unresolved,
        "requires_exact_temporal_layer_frame": temporal,
    }


_RESOLUTION_GAPS = (
    "CLASSICAL_RESOLUTION_SEMANTICS",
    "SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING",
)
_FAILURE_GAPS = (
    "CLASSICAL_RESOLUTION_FAILURE_SEMANTICS",
    "CLASSICAL_INTERACTION_CHAIN_RESOLUTION",
    "SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING",
)

NORMALIZATION_SPECS: dict[str, dict[str, Any]] = {
    "ZPZQ-CL-09-003-001": _spec(
        role="GENERAL_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("刑冲", "三合六合", "可以解之"), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-003-002": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("卯则冲", "卯与戌合而不冲"), participants=("甲", "酉", "卯", "戌"),
        unresolved=_RESOLUTION_GAPS, temporal=True,
    ),
    "ZPZQ-CL-09-003-003": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("酉与辰合而不冲",), participants=("辰", "酉"), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-003-004": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("卯与亥未会而不冲",), participants=("亥", "未", "卯"), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-003-005": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("酉与巳丑会而不冲",), participants=("巳", "丑", "酉"), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-003-006": _spec(
        role="SUMMARY_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("会合可以解冲",), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-003-007": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("逢卯则刑", "与戌合而不刑"), participants=("丙", "子", "卯", "戌"),
        unresolved=_RESOLUTION_GAPS, temporal=True,
    ),
    "ZPZQ-CL-09-003-008": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("子与丑合而不刑",), participants=("丑", "子"), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-003-009": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("卯与亥未会而不刑",), participants=("亥", "未", "卯"), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-003-010": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("子与申辰会而不刑",), participants=("申", "辰", "子"), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-003-011": _spec(
        role="SUMMARY_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("会合可以解刑",), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-005-001": _spec(
        role="CONTEXTUAL_QUESTION", primary="REVERSAL_OR_REAPPEARANCE_ASSERTION",
        fragments=("因解而反得刑冲",), actor="UNRESOLVED_ACTOR", target="UNRESOLVED_TARGET",
        unresolved=("CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",),
    ),
    "ZPZQ-CL-09-005-002": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="REVERSAL_OR_REAPPEARANCE_ASSERTION",
        secondary=("PARTICIPANT_ALLOCATION_ASSERTION", "RESOLUTION_ASSERTION"),
        fragments=("二卯相并", "二卯不刑一子", "戌与卯合", "本为解刑", "合去其一", "一合而一刑", "因解而反得刑冲"),
        participants=("甲", "子", "卯", "戌"),
        unresolved=(
            "CLASSICAL_RESOLUTION_SEMANTICS",
            "CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",
            "CLASSICAL_PARTICIPANT_ALLOCATION",
            "SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING",
            "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION",
        ), temporal=True,
    ),
    "ZPZQ-CL-09-007-001": _spec(
        role="CONTEXTUAL_QUESTION", primary="RESOLUTION_FAILURE_ASSERTION",
        fragments=("刑冲而会合不能解",), unresolved=_FAILURE_GAPS,
    ),
    "ZPZQ-CL-09-007-002": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_FAILURE_ASSERTION",
        secondary=("RESOLUTION_ASSERTION", "REVERSAL_OR_REAPPEARANCE_ASSERTION"),
        fragments=("丑与子合", "可以解冲", "丑与巳酉会", "子复冲午"),
        participants=("子", "午", "丑", "巳", "酉"),
        unresolved=(*_FAILURE_GAPS, "CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS"), temporal=True,
    ),
    "ZPZQ-CL-09-007-003": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_FAILURE_ASSERTION",
        secondary=("RESOLUTION_ASSERTION", "REVERSAL_OR_REAPPEARANCE_ASSERTION"),
        fragments=("戌与卯合", "可以解刑", "戌与寅午会", "卯复刑子"),
        participants=("子", "卯", "戌", "寅", "午"),
        unresolved=(*_FAILURE_GAPS, "CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS"), temporal=True,
    ),
    "ZPZQ-CL-09-007-004": _spec(
        role="SUMMARY_SOURCE_ASSERTION", primary="RESOLUTION_FAILURE_ASSERTION",
        fragments=("会合而不能解刑冲",), unresolved=_FAILURE_GAPS,
    ),
    "ZPZQ-CL-09-009-001": _spec(
        role="CONTEXTUAL_QUESTION", primary="RESOLUTION_ASSERTION",
        fragments=("刑冲而可以解刑",), unresolved=_RESOLUTION_GAPS,
    ),
    "ZPZQ-CL-09-009-002": _spec(
        role="GENERAL_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("以另位之刑冲", "解月令之刑冲"), unresolved=_RESOLUTION_GAPS, temporal=True,
    ),
    "ZPZQ-CL-09-009-003": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("卯以刑子", "与酉冲不刑月令之官"), participants=("丙", "子", "卯", "酉"),
        unresolved=_RESOLUTION_GAPS, temporal=True,
    ),
    "ZPZQ-CL-09-009-004": _spec(
        role="EXEMPLIFYING_SOURCE_ASSERTION", primary="ATTENUATION_ASSERTION",
        fragments=("卯日冲之", "卯与子刑", "冲之无力", "月官犹在"), participants=("甲", "酉", "卯", "子"),
        unresolved=("CLASSICAL_ATTENUATION_GRADE", "SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING"), temporal=True,
    ),
    "ZPZQ-CL-09-009-005": _spec(
        role="SUMMARY_SOURCE_ASSERTION", primary="RESOLUTION_ASSERTION",
        fragments=("以刑冲而解刑冲",), unresolved=_RESOLUTION_GAPS,
    ),
    "QTBJ-CL-05347": _spec(
        role="GENERAL_SOURCE_ASSERTION", primary="PARTICIPANT_MEDIATED_RELEASE_ASSERTION",
        fragments=("癸水通源", "破丙解合"), participants=("亥", "子", "申", "癸", "丙"),
        actor="PARTICIPANT_OR_CONTEXT_ACTOR",
        unresolved=("CLASSICAL_PARTICIPANT_MEDIATED_RELEASE_SEMANTICS", "SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING"),
    ),
    "QTBJ-CL-05370": _spec(
        role="GENERAL_SOURCE_ASSERTION", primary="PARTICIPANT_MEDIATED_RELEASE_ASSERTION",
        fragments=("癸水破丙解合", "癸水有力"), participants=("丙", "癸", "亥", "子", "丑", "甲", "戊"),
        actor="PARTICIPANT_OR_CONTEXT_ACTOR",
        unresolved=("CLASSICAL_PARTICIPANT_MEDIATED_RELEASE_SEMANTICS", "SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING"),
    ),
}


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _parse_source_row(line: str) -> dict[str, Any] | None:
    stripped = line.rstrip("\r\n")
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        value = None
    if isinstance(value, dict):
        source_occurrence_id = value.get("SOURCE_OCCURRENCE_ID")
        source_text = value.get("RAW_CLAUSE_TEXT")
        if isinstance(source_occurrence_id, str) and isinstance(source_text, str) and source_text:
            return {
                "source_occurrence_id": source_occurrence_id,
                "parent_source_block_id": value.get("SOURCE_BLOCK_ID"),
                "parent_source_segment_id": None,
                "source_chapter_id": value.get("SOURCE_CHAPTER_ID"),
                "source_chapter_title": value.get("SOURCE_CHAPTER_TITLE"),
                "source_layer": value.get("SOURCE_LAYER"),
                "source_record_role": value.get("CLAUSE_ROLE"),
                "source_record_format": "JSONL_SOURCE_CLAUSE",
                "source_text_sha256": value.get("RAW_CLAUSE_SHA256"),
                "exact_source_text": source_text,
            }
        return None
    fields = stripped.split("\t")
    if len(fields) == 11 and fields[0].startswith("QTBJ-CL-"):
        return {
            "source_occurrence_id": fields[0],
            "parent_source_block_id": None,
            "parent_source_segment_id": fields[1],
            "source_chapter_id": None,
            "source_chapter_title": None,
            "source_layer": fields[4],
            "source_record_role": fields[6],
            "source_record_format": "QTBJ_SOURCE_CLAUSE_TSV",
            "source_text_sha256": fields[9],
            "exact_source_text": fields[10],
        }
    return None


def _collect_source_rows(root: Path, index: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    wanted = set(MANDATORY_SOURCE_OCCURRENCE_IDS)
    matches: dict[str, list[dict[str, Any]]] = {source_id: [] for source_id in wanted}
    qtbj_explicit_release_ids: list[str] = []
    for segment in index["segments"]:
        segment_path = root / segment["path"]
        payload = segment_path.read_bytes()
        local_offset = 0
        for local_line_number, line_bytes in enumerate(payload.splitlines(keepends=True), start=1):
            line = line_bytes.decode("utf-8", errors="strict")
            parsed = _parse_source_row(line)
            if parsed is not None:
                source_occurrence_id = parsed["source_occurrence_id"]
                if source_occurrence_id.startswith("QTBJ-CL-") and "解合" in parsed["exact_source_text"]:
                    qtbj_explicit_release_ids.append(source_occurrence_id)
                if source_occurrence_id in wanted:
                    canonical_byte_start = segment["byte_start"] + local_offset
                    matches[source_occurrence_id].append(
                        {
                            **parsed,
                            "access_segment_id": segment["segment_id"],
                            "access_segment_path": segment["path"],
                            "access_segment_sha256": segment["sha256"],
                            "segment_local_line": local_line_number,
                            "canonical_line": segment["line_start"] + local_line_number - 1,
                            "canonical_byte_start": canonical_byte_start,
                            "canonical_byte_end_exclusive": canonical_byte_start + len(line_bytes),
                            "source_record_sha256": _sha256(line_bytes),
                        }
                    )
            local_offset += len(line_bytes)
        if local_offset != len(payload):
            raise TrainingError(f"interaction assertion segment replay failed: {segment['segment_id']}")

    duplicated_or_missing = {
        source_id: len(rows) for source_id, rows in matches.items() if len(rows) != 1
    }
    if duplicated_or_missing:
        raise TrainingError(
            f"interaction assertion source rows are missing or duplicated: {duplicated_or_missing}"
        )
    exact_qtbj_ids = sorted(set(qtbj_explicit_release_ids))
    if exact_qtbj_ids != sorted(QTBJ_EXPLICIT_RELEASE_SOURCE_OCCURRENCE_IDS):
        raise TrainingError(
            "QTBJ exact-lexeme 解合 inventory changed; exact-ID normalization review is required"
        )
    return {source_id: rows[0] for source_id, rows in matches.items()}, exact_qtbj_ids


def _dependencies(spec: dict[str, Any]) -> list[dict[str, str]]:
    primitives = {
        "EXACT_RAW_RELATION_OCCURRENCE_IDENTITY",
        "EXACT_PARTICIPANT_INSTANCE_IDENTITY",
    }
    if spec["actor_reference_kind"] == "RELATION_PATTERN_ACTOR":
        primitives.add("RELATION_PAIR_TOPOLOGY")
    if spec["requires_exact_temporal_layer_frame"]:
        primitives.add("EXACT_TEMPORAL_LAYER_FRAME")
    if "PARTICIPANT_ALLOCATION_ASSERTION" in (
        spec["primary_assertion_class"], *spec["secondary_assertion_classes"]
    ):
        primitives.add("RELATION_INCIDENCE_DEGREE")
        primitives.add("RELATION_PAIR_TOPOLOGY")
    return [
        {
            "primitive": primitive,
            "binding_status": "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
            "semantic_boundary": NEUTRAL_RUNTIME_DEPENDENCY_REGISTRY[primitive]["semantic_boundary"],
        }
        for primitive in sorted(primitives)
    ]


def _multiplicity(source_occurrence_id: str) -> dict[str, Any]:
    if source_occurrence_id == "ZPZQ-CL-09-005-002":
        return {
            "signal": "EXPLICIT_SOURCE_MULTIPLICITY_AND_UNRESOLVED_ALLOCATION",
            "source_named_multiplicity": [{"participant_lexeme": "卯", "count": 2}],
            "allocation_lexemes": ["合去其一", "一合而一刑"],
            "exact_instance_selection": "NOT_SELECTED",
            "alternative_path_signal": "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS",
        }
    return {
        "signal": "NONE",
        "source_named_multiplicity": [],
        "allocation_lexemes": [],
        "exact_instance_selection": "NOT_APPLICABLE",
        "alternative_path_signal": "NONE",
    }


def _build_record(source_row: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    source_occurrence_id = source_row["source_occurrence_id"]
    exact_text = source_row["exact_source_text"]
    if source_row["source_text_sha256"] != _sha256(exact_text.encode("utf-8")):
        raise TrainingError(f"source text hash mismatch: {source_occurrence_id}")
    missing_fragments = [
        fragment for fragment in spec["source_assertion_fragments"] if fragment not in exact_text
    ]
    if missing_fragments:
        raise TrainingError(
            f"interaction assertion fragments do not replay: {source_occurrence_id}:{missing_fragments}"
        )
    missing_participants = [
        participant
        for participant in spec["source_named_participant_patterns"]
        if participant not in exact_text
    ]
    if missing_participants:
        raise TrainingError(
            f"interaction participant patterns do not replay: {source_occurrence_id}:{missing_participants}"
        )
    if spec["primary_assertion_class"] in spec["secondary_assertion_classes"]:
        raise TrainingError(
            f"interaction assertion primary class is duplicated: {source_occurrence_id}"
        )
    record = {
        "interaction_assertion_id": f"BCRIA-R1-{source_occurrence_id}",
        "source_id": SOURCE_ID,
        "source_occurrence_id": source_occurrence_id,
        "parent_source_block_id": source_row["parent_source_block_id"],
        "parent_source_segment_id": source_row["parent_source_segment_id"],
        "source_chapter_id": source_row["source_chapter_id"],
        "source_chapter_title": source_row["source_chapter_title"],
        "source_layer": source_row["source_layer"],
        "source_record_role": source_row["source_record_role"],
        "source_record_format": source_row["source_record_format"],
        "canonical_source_path": EXPECTED_SOURCE_PATH,
        "canonical_source_sha256": EXPECTED_SOURCE_SHA256,
        "access_segment_id": source_row["access_segment_id"],
        "access_segment_path": source_row["access_segment_path"],
        "access_segment_sha256": source_row["access_segment_sha256"],
        "segment_local_line": source_row["segment_local_line"],
        "canonical_line": source_row["canonical_line"],
        "canonical_byte_start": source_row["canonical_byte_start"],
        "canonical_byte_end_exclusive": source_row["canonical_byte_end_exclusive"],
        "source_record_sha256": source_row["source_record_sha256"],
        "source_text_sha256": source_row["source_text_sha256"],
        "exact_source_text": exact_text,
        "source_assertion_fragments": list(spec["source_assertion_fragments"]),
        "source_assertion_role": spec["source_assertion_role"],
        "primary_assertion_class": spec["primary_assertion_class"],
        "secondary_assertion_classes": sorted(spec["secondary_assertion_classes"]),
        "actor_reference_kind": spec["actor_reference_kind"],
        "target_reference_kind": spec["target_reference_kind"],
        "source_named_participant_patterns": sorted(spec["source_named_participant_patterns"]),
        "source_named_relation_or_effect_patterns": list(
            spec["source_named_relation_or_effect_patterns"]
        ),
        "multiplicity_and_alternative_path": _multiplicity(source_occurrence_id),
        "neutral_runtime_dependency_map": _dependencies(spec),
        "unresolved_semantic_requirements": sorted(spec["unresolved_semantic_requirements"]),
        "runtime_semantic_boundary": {
            "raw_relation_mutation_allowed": False,
            "relation_presence_verdict": "NOT_EMITTED",
            "classical_operability_verdict": "NOT_EMITTED",
            "exact_winner_selection": "NOT_EMITTED",
        },
    }
    record["record_sha256"] = object_sha256(record)
    return record


def _counts(records: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(record[field] for record in records).items()))


def _summary(records: list[dict[str, Any]], qtbj_ids: list[str]) -> dict[str, Any]:
    assertion_counts: Counter[str] = Counter()
    for record in records:
        assertion_counts.update(
            [record["primary_assertion_class"], *record["secondary_assertion_classes"]]
        )
    shen_counts = Counter(
        record["parent_source_block_id"]
        for record in records
        if record["source_layer"] == "SHEN_CLASSICAL_SOURCE"
    )
    return {
        "record_count": len(records),
        "shen_record_count": sum(shen_counts.values()),
        "qtbj_explicit_release_record_count": len(qtbj_ids),
        "shen_block_counts": dict(sorted(shen_counts.items())),
        "assertion_class_occurrence_counts": dict(sorted(assertion_counts.items())),
        "source_assertion_role_counts": _counts(records, "source_assertion_role"),
        "actor_reference_kind_counts": _counts(records, "actor_reference_kind"),
        "target_reference_kind_counts": _counts(records, "target_reference_kind"),
        "source_layer_counts": _counts(records, "source_layer"),
        "explicit_multiplicity_record_count": sum(
            record["multiplicity_and_alternative_path"]["signal"] != "NONE"
            for record in records
        ),
        "qtbj_exact_lexeme_review_source_occurrence_ids": qtbj_ids,
    }


def build_classical_relation_interaction_assertion_matrix(
    root: Path,
) -> tuple[dict[str, Any], str]:
    root = root.resolve()
    access = validate_source_access(root, require_source_commit=False)
    if (
        access["status"] != "PASS"
        or access["source_id"] != SOURCE_ID
        or access["canonical_sha256"] != EXPECTED_SOURCE_SHA256
        or access["round_trip_exact"] is not True
    ):
        raise TrainingError("interaction assertion source-access gate failed")
    if set(NORMALIZATION_SPECS) != set(MANDATORY_SOURCE_OCCURRENCE_IDS):
        raise TrainingError("interaction assertion normalization inventory is incomplete")

    index = load_json(root / SOURCE_ACCESS_INDEX_PATH)
    source_rows, qtbj_ids = _collect_source_rows(root, index)
    records = [
        _build_record(source_rows[source_occurrence_id], NORMALIZATION_SPECS[source_occurrence_id])
        for source_occurrence_id in MANDATORY_SOURCE_OCCURRENCE_IDS
    ]
    summary = _summary(records, qtbj_ids)
    artifact: dict[str, Any] = {
        "schema": AUDIT_ID,
        "audit_id": AUDIT_ID,
        "authority": {
            "source_id": SOURCE_ID,
            "canonical_source_path": EXPECTED_SOURCE_PATH,
            "canonical_source_bytes": EXPECTED_SOURCE_BYTES,
            "canonical_source_sha256": EXPECTED_SOURCE_SHA256,
            "source_access_index_path": SOURCE_ACCESS_INDEX_PATH.as_posix(),
            "source_access_index_sha256": sha256_file(root / SOURCE_ACCESS_INDEX_PATH),
            "canonical_source_is_sole_authority": True,
            "derived_access_is_read_only_lossless_view": True,
            "prediction_source_selection_allowed": False,
        },
        "scope": {
            "artifact_role": "STATIC_SOURCE_INTERACTION_ASSERTION_EVIDENCE_ONLY",
            "chart_specific_runtime_verdicts_released": False,
            "classical_operability_evaluator_released": False,
            "graph_or_fixpoint_resolver_released": False,
            "global_relation_precedence_released": False,
            "winner_selection_released": False,
            "participant_auto_allocation_released": False,
            "raw_relation_mutation_released": False,
            "activation_suppression_or_cancellation_runtime_released": False,
            "three_meeting_or_six_break_runtime_tables_released": False,
            "hidden_combination_or_hidden_stem_relation_ontology_released": False,
            "five_combination_outcome_semantics_released": False,
        },
        "method": {
            "algorithm_id": "S14_EXACT_SOURCE_ID_INTERACTION_ASSERTION_NORMALIZATION_R1",
            "algorithm_version": "1.0.0",
            "source_selection": "CLOSED_EXACT_SOURCE_OCCURRENCE_ID_UNIVERSE",
            "source_row_selection": "AUTHORITATIVE_CLAUSE_ROW_WITH_EXACT_SOURCE_TEXT",
            "qtbj_extension_review": "QTBJ_SOURCE_CLAUSE_ID_PLUS_EXACT_LEXEME_JIEHE_ONLY",
            "keyword_to_runtime_ontology_compilation_used": False,
            "record_order": "MANDATORY_SOURCE_UNIVERSE_ORDER",
            "multi_assertion_representation": "PRIMARY_PLUS_SORTED_SECONDARY",
        },
        "mandatory_source_universe": {
            "shen_chapter_id": "ZPZQ-CH-09",
            "shen_chapter_title": "论刑冲会合解法",
            "shen_block_counts": MANDATORY_SHEN_BLOCK_COUNTS,
            "shen_source_occurrence_ids": list(MANDATORY_SHEN_SOURCE_OCCURRENCE_IDS),
            "qtbj_explicit_release_source_occurrence_ids": list(
                QTBJ_EXPLICIT_RELEASE_SOURCE_OCCURRENCE_IDS
            ),
        },
        "closed_vocabularies": {
            "assertion_classes": list(ASSERTION_CLASSES),
            "source_assertion_roles": list(SOURCE_ASSERTION_ROLES),
            "actor_reference_kinds": list(ACTOR_REFERENCE_KINDS),
            "target_reference_kinds": list(TARGET_REFERENCE_KINDS),
            "multiplicity_signals": list(MULTIPLICITY_SIGNALS),
            "alternative_path_signals": list(ALTERNATIVE_PATH_SIGNALS),
            "neutral_runtime_primitives": list(NEUTRAL_RUNTIME_PRIMITIVES),
            "unresolved_semantic_requirements": list(UNRESOLVED_SEMANTIC_REQUIREMENTS),
        },
        "neutral_runtime_dependency_registry": NEUTRAL_RUNTIME_DEPENDENCY_REGISTRY,
        "records": records,
        "summary": summary,
    }
    artifact["determinism"] = {
        "source_inventory_sha256": object_sha256(
            [record["source_occurrence_id"] for record in records]
        ),
        "record_hash_chain_sha256": object_sha256(
            [record["record_sha256"] for record in records]
        ),
        "records_semantics_sha256": object_sha256(records),
        "closed_registry_sha256": object_sha256(
            {
                "closed_vocabularies": artifact["closed_vocabularies"],
                "neutral_runtime_dependency_registry": NEUTRAL_RUNTIME_DEPENDENCY_REGISTRY,
            }
        ),
        "artifact_semantics_sha256": object_sha256(artifact),
    }
    return artifact, _build_report(artifact)


def _build_report(artifact: dict[str, Any]) -> str:
    summary = artifact["summary"]
    lines = [
        "# Bazi Classical Relation Interaction Assertion Matrix R1 — Coverage Report",
        "",
        "Status: static, exact-source interaction assertion evidence only.",
        "",
        "## Mandatory source coverage",
        "",
        f"- Shen `ZPZQ-CH-09` source occurrences: `{summary['shen_record_count']}` (exactly once).",
        f"- QTBJ explicit `解合` source occurrences: `{summary['qtbj_explicit_release_record_count']}` (exactly once).",
        f"- Total records: `{summary['record_count']}`.",
        "",
        "| Source occurrence | Source role | Primary assertion | Secondary assertions | Actor kind | Target kind |",
        "|---|---|---|---|---|---|",
    ]
    for record in artifact["records"]:
        secondary = ", ".join(record["secondary_assertion_classes"]) or "—"
        lines.append(
            f"| `{record['source_occurrence_id']}` | `{record['source_assertion_role']}` | "
            f"`{record['primary_assertion_class']}` | {secondary} | "
            f"`{record['actor_reference_kind']}` | `{record['target_reference_kind']}` |"
        )
    lines.extend(
        [
            "",
            "## Semantic boundary",
            "",
            "- Source assertion classes are not chart-specific runtime outcomes.",
            "- `SHARED_PARTICIPANT` is topology, not competition or winner selection.",
            "- Transition `EXITED` is raw set-change evidence and is not `解`.",
            "- `RELATION_PRESENT` is not a Classical operative-effect verdict.",
            "- `不冲` / `不刑` source language does not delete or mutate an immutable raw relation occurrence.",
            "- `冲之无力` is preserved as attenuation language and never normalized to relation absence.",
            "- `合去其一` preserves all compatible future exact-instance allocation paths and selects no winner.",
            "- QTBJ `破丙解合` records use a participant/context actor and create no generic stem-control relation.",
            "- No global family precedence, operability evaluator, graph/fixpoint resolver, activation, suppression, or final relation outcome is released.",
            "",
            "## Determinism",
            "",
            f"- Source inventory SHA-256: `{artifact['determinism']['source_inventory_sha256']}`",
            f"- Record hash chain SHA-256: `{artifact['determinism']['record_hash_chain_sha256']}`",
            f"- Records semantics SHA-256: `{artifact['determinism']['records_semantics_sha256']}`",
            f"- Closed registry SHA-256: `{artifact['determinism']['closed_registry_sha256']}`",
            f"- Artifact semantics SHA-256: `{artifact['determinism']['artifact_semantics_sha256']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_classical_relation_interaction_assertion_matrix(root: Path) -> dict[str, Any]:
    artifact, report = build_classical_relation_interaction_assertion_matrix(root)
    atomic_write_json(root / MATRIX_PATH, artifact)
    atomic_write_bytes(root / REPORT_PATH, report.encode("utf-8"))
    return {
        "status": "BUILT",
        "audit_id": AUDIT_ID,
        "matrix_path": MATRIX_PATH.as_posix(),
        "report_path": REPORT_PATH.as_posix(),
        **artifact["summary"],
        **artifact["determinism"],
    }


def _validate_schema(root: Path, artifact: dict[str, Any]) -> None:
    schema = load_json(root / SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(artifact),
        key=lambda error: list(error.path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(item) for item in error.path) or "<root>"
        raise TrainingError(
            f"interaction assertion schema failed at {location}: {error.message}"
        )


def _validate_contract_refs(root: Path) -> None:
    for primitive, spec in NEUTRAL_RUNTIME_DEPENDENCY_REGISTRY.items():
        for contract_ref in spec["contract_refs"]:
            path_value, symbol = contract_ref.split(":", 1)
            payload = (root / path_value).read_text(encoding="utf-8")
            class_name, field_name = symbol.split(".", 1)
            if f"class {class_name}" not in payload or field_name not in payload:
                raise TrainingError(
                    f"neutral runtime contract reference is unresolved: {primitive}:{contract_ref}"
                )


def _validate_record_replay(root: Path, record: dict[str, Any]) -> None:
    segment_path = root / record["access_segment_path"]
    if sha256_file(segment_path) != record["access_segment_sha256"]:
        raise TrainingError(f"interaction source segment hash mismatch: {record['source_occurrence_id']}")
    canonical_payload = (root / record["canonical_source_path"]).read_bytes()
    passage = canonical_payload[
        record["canonical_byte_start"] : record["canonical_byte_end_exclusive"]
    ]
    if _sha256(passage) != record["source_record_sha256"]:
        raise TrainingError(f"interaction canonical locator replay failed: {record['source_occurrence_id']}")
    index = load_json(root / SOURCE_ACCESS_INDEX_PATH)
    segment = next(
        row for row in index["segments"] if row["segment_id"] == record["access_segment_id"]
    )
    local_start = record["canonical_byte_start"] - segment["byte_start"]
    local_end = record["canonical_byte_end_exclusive"] - segment["byte_start"]
    if segment_path.read_bytes()[local_start:local_end] != passage:
        raise TrainingError(f"interaction derived-access replay failed: {record['source_occurrence_id']}")
    parsed = _parse_source_row(passage.decode("utf-8", errors="strict"))
    if (
        parsed is None
        or parsed["source_occurrence_id"] != record["source_occurrence_id"]
        or parsed["exact_source_text"] != record["exact_source_text"]
    ):
        raise TrainingError(f"interaction source row parse replay failed: {record['source_occurrence_id']}")
    if record["record_sha256"] != object_sha256(
        {key: value for key, value in record.items() if key != "record_sha256"}
    ):
        raise TrainingError(f"interaction record hash mismatch: {record['source_occurrence_id']}")


def validate_classical_relation_interaction_assertion_matrix_value(
    root: Path, artifact: dict[str, Any]
) -> dict[str, Any]:
    root = root.resolve()
    expected, expected_report = build_classical_relation_interaction_assertion_matrix(root)
    _validate_schema(root, artifact)
    if artifact != expected:
        raise TrainingError("interaction assertion matrix is stale, tampered, or non-deterministic")
    _validate_contract_refs(root)

    records = artifact["records"]
    occurrence_ids = [record["source_occurrence_id"] for record in records]
    if occurrence_ids != list(MANDATORY_SOURCE_OCCURRENCE_IDS) or len(set(occurrence_ids)) != len(records):
        raise TrainingError("interaction assertion mandatory source universe is not exactly once")
    if artifact["summary"]["shen_block_counts"] != MANDATORY_SHEN_BLOCK_COUNTS:
        raise TrainingError("interaction assertion Shen block coverage changed")
    for record in records:
        _validate_record_replay(root, record)
        classes = {record["primary_assertion_class"], *record["secondary_assertion_classes"]}
        if not classes.issubset(ASSERTION_CLASSES):
            raise TrainingError("interaction assertion class escaped the closed vocabulary")
        if any(fragment not in record["exact_source_text"] for fragment in record["source_assertion_fragments"]):
            raise TrainingError("interaction assertion fragment does not replay")
        if any(
            participant not in record["exact_source_text"]
            for participant in record["source_named_participant_patterns"]
        ):
            raise TrainingError("interaction participant pattern does not replay")
        if any(
            dependency["primitive"] not in NEUTRAL_RUNTIME_PRIMITIVES
            for dependency in record["neutral_runtime_dependency_map"]
        ):
            raise TrainingError("interaction assertion emitted a non-neutral runtime dependency")
        if record["runtime_semantic_boundary"] != {
            "raw_relation_mutation_allowed": False,
            "relation_presence_verdict": "NOT_EMITTED",
            "classical_operability_verdict": "NOT_EMITTED",
            "exact_winner_selection": "NOT_EMITTED",
        }:
            raise TrainingError("interaction assertion crossed the runtime semantic boundary")

    by_id = {record["source_occurrence_id"]: record for record in records}
    for source_occurrence_id in QTBJ_EXPLICIT_RELEASE_SOURCE_OCCURRENCE_IDS:
        qtbj = by_id[source_occurrence_id]
        if (
            qtbj["actor_reference_kind"] != "PARTICIPANT_OR_CONTEXT_ACTOR"
            or qtbj["primary_assertion_class"] != "PARTICIPANT_MEDIATED_RELEASE_ASSERTION"
        ):
            raise TrainingError("QTBJ participant-mediated release was converted to a relation actor")
    allocation = by_id["ZPZQ-CL-09-005-002"]["multiplicity_and_alternative_path"]
    if allocation != {
        "signal": "EXPLICIT_SOURCE_MULTIPLICITY_AND_UNRESOLVED_ALLOCATION",
        "source_named_multiplicity": [{"participant_lexeme": "卯", "count": 2}],
        "allocation_lexemes": ["合去其一", "一合而一刑"],
        "exact_instance_selection": "NOT_SELECTED",
        "alternative_path_signal": "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS",
    }:
        raise TrainingError("合去其一 exact-instance alternative paths were not preserved")
    attenuation = by_id["ZPZQ-CL-09-009-004"]
    if (
        attenuation["primary_assertion_class"] != "ATTENUATION_ASSERTION"
        or attenuation["runtime_semantic_boundary"]["relation_presence_verdict"] != "NOT_EMITTED"
    ):
        raise TrainingError("冲之无力 was converted to relation absence")
    if any(value is True for key, value in artifact["scope"].items() if key.endswith("_released")):
        raise TrainingError("interaction assertion artifact released excluded runtime semantics")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        **artifact["summary"],
        **artifact["determinism"],
        "mandatory_source_exactly_once": True,
        "source_locator_replay": True,
        "neutral_contract_refs_resolved": True,
        "deterministic_rebuild": True,
        "report_sha256": _sha256(expected_report.encode("utf-8")),
    }


def validate_classical_relation_interaction_assertion_matrix(root: Path) -> dict[str, Any]:
    root = root.resolve()
    artifact = load_json(root / MATRIX_PATH)
    report = (root / REPORT_PATH).read_text(encoding="utf-8")
    result = validate_classical_relation_interaction_assertion_matrix_value(root, artifact)
    _, expected_report = build_classical_relation_interaction_assertion_matrix(root)
    if report != expected_report:
        raise TrainingError("interaction assertion coverage report is stale or tampered")
    return result

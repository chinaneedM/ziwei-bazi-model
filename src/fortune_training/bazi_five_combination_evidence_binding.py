from __future__ import annotations

import hashlib
import importlib
from collections import Counter
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

from .classical_relation_evidence import (
    MATRIX_PATH,
    validate_classical_relation_evidence,
)
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


AUDIT_ID = "BAZI-STEM-FIVE-COMBINATION-ELIGIBILITY-EVIDENCE-BINDING-R1"
AUDIT_ROOT = Path("audits/bazi-stem-five-combination-eligibility-evidence-binding-r1")
BINDINGS_PATH = AUDIT_ROOT / "bindings.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-stem-five-combination-eligibility-evidence-binding-r1.schema.json")

SOURCE_FAMILY = "STEM_FIVE_COMBINATION"
EXPECTED_EVIDENCE_COUNT = 215
SOURCE_ID = "S14"
EXPECTED_SOURCE_SHA256 = "b225e64fcf7238b27a634e653a6904403d518335aeca59372b32e02f4a560407"

BINDING_DISPOSITIONS = (
    "EXACT_NEUTRAL_BINDING",
    "RELATED_NEUTRAL_EVIDENCE_ONLY",
    "PARTIAL_BINDING",
    "NO_BINDING_MISSING_PRIMITIVE",
    "NO_BINDING_SOURCE_SEMANTICS_AMBIGUOUS",
    "PROFILE_ALTERNATIVE_UNRESOLVED",
    "NON_CONDITION_RECORD",
)
BINDING_ASSERTION_STRENGTHS = (
    "EXACT_IDENTITY_BINDING",
    "RELATED_NEUTRAL_EVIDENCE",
)
NEUTRAL_PREDICATE_KINDS = (
    "RELATION_OCCURRENCE_IDENTITY",
    "NOMINAL_TRANSFORMATION_ELEMENT_IDENTITY",
    "PARTICIPANT_STEM_IDENTITY",
    "PARTICIPANT_ELEMENT_IDENTITY",
    "PARTICIPANT_POLARITY_IDENTITY",
    "PARTICIPANT_LAYER_IDENTITY",
    "TEMPORAL_FRAME_IDENTITY",
    "NATAL_POSITION_DOMAIN",
    "NATAL_PILLAR_ORDINALS",
    "NATAL_ORDINAL_DISTANCE",
    "NATAL_INTERVENING_VISIBLE_STEM_IDS",
    "INTERVENER_STEM_IDENTITY",
    "NATAL_DAY_MASTER_PARTICIPATION",
    "PARTICIPANT_RELATION_DEGREE",
    "RELATION_PAIR_SHARED_PARTICIPANT_TOPOLOGY",
    "NATAL_MONTH_COMMAND_REFERENCE",
    "ACTIVE_FLOW_SOLAR_MONTH_REFERENCE",
    "EXACT_HIDDEN_STEM_MATCH_REFERENCE",
    "SAME_ELEMENT_HIDDEN_SUPPORT_REFERENCE",
    "SUPPORT_TOUCH_REFERENCE",
    "EXPOSURE_LINK_REFERENCE",
    "RELATION_TRANSITION_SET_MEMBERSHIP",
)

REQUIRED_UNRESOLVED_PRIMITIVES = (
    "TRANSFORMATION_SUCCESS",
    "BINDING_OR_NON_TRANSFORMATION_OUTCOME",
    "CLASSICAL_COMPETITION_SEMANTICS",
    "CLASSICAL_ORDER_OR_PROXIMITY",
    "COEXISTING_RELATION_PRECEDENCE",
    "ROOT_OR_SUPPORT_GRADE",
    "STRENGTH_OR_WANGSHUAI_GRADE",
    "TEMPORAL_LAYER_PRIORITY_SEMANTICS",
    "CLASH_RELEASE_OR_CANCELLATION_SEMANTICS",
)

NON_CONDITION_STATEMENT_CLASSES = frozenset(
    {
        "COMMENTARY_OR_EXPLANATION",
        "EXAMPLE_ONLY",
        "RESULT_OR_EFFECT_STATEMENT",
    }
)
UNMAPPED_SOURCE_CONDITION_CLASSES = frozenset(
    {"ELIGIBILITY_CONDITION", "EXCEPTION_OR_LIMIT"}
)


def _spec(contract: str, *paths: str) -> dict[str, Any]:
    return {"runtime_contract": contract, "runtime_fact_or_field_paths": list(paths)}


PREDICATE_SPECS: dict[str, dict[str, Any]] = {
    "RELATION_OCCURRENCE_IDENTITY": _spec(
        "Bazi Relation Incidence Foundation R1",
        "fortune_training.bazi_relation_incidence.models:RelationOccurrenceReference.reference_id",
        "fortune_training.bazi_relation_incidence.models:RelationOccurrenceReference.relation_id",
        "fortune_training.bazi_relation_incidence.models:RelationOccurrenceReference.semantic_relation_id",
        "fortune_training.bazi_relation_incidence.models:RelationOccurrenceReference.relation_family",
    ),
    "NOMINAL_TRANSFORMATION_ELEMENT_IDENTITY": _spec(
        "Bazi Relation Incidence Foundation R1",
        "fortune_training.bazi_relation_incidence.models:RelationOccurrenceReference.nominal_transformation_element",
        "fortune_training.bazi_relation_incidence.models:RelationOccurrenceReference.nominal_transformation_semantics",
    ),
    "PARTICIPANT_STEM_IDENTITY": _spec(
        "Bazi Relation Incidence Foundation R1",
        "fortune_training.bazi_relation_incidence.models:RelationOccurrenceReference.participant_instance_ids",
        "fortune_training.bazi_relation_incidence.models:IncidenceParticipantReference.value",
        "fortune_training.bazi_relation_incidence.models:IncidenceParticipantReference.participant_kind",
    ),
    "PARTICIPANT_ELEMENT_IDENTITY": _spec(
        "Stem Relation Positional Context Foundation R1",
        "fortune_training.bazi_stem_relation_positional.models:StemParticipantPositionReference.element",
    ),
    "PARTICIPANT_POLARITY_IDENTITY": _spec(
        "Stem Relation Positional Context Foundation R1",
        "fortune_training.bazi_stem_relation_positional.models:StemParticipantPositionReference.polarity",
    ),
    "PARTICIPANT_LAYER_IDENTITY": _spec(
        "Bazi Relation Incidence Foundation R1",
        "fortune_training.bazi_relation_incidence.models:IncidenceParticipantReference.participant_layer",
    ),
    "TEMPORAL_FRAME_IDENTITY": _spec(
        "Bazi Relation Incidence Foundation R1",
        "fortune_training.bazi_relation_incidence.models:IncidenceParticipantReference.source_frame_id",
    ),
    "NATAL_POSITION_DOMAIN": _spec(
        "Stem Relation Positional Context Foundation R1",
        "fortune_training.bazi_stem_relation_positional.models:StemParticipantPositionReference.position_domain",
        "fortune_training.bazi_stem_relation_positional.models:StemPairPositionalFact.position_domain_pair",
    ),
    "NATAL_PILLAR_ORDINALS": _spec(
        "Stem Relation Positional Context Foundation R1",
        "fortune_training.bazi_stem_relation_positional.models:StemParticipantPositionReference.natal_pillar_ordinal",
        "fortune_training.bazi_stem_relation_positional.models:StemPairPositionalFact.natal_pillar_ordinals",
    ),
    "NATAL_ORDINAL_DISTANCE": _spec(
        "Stem Relation Positional Context Foundation R1",
        "fortune_training.bazi_stem_relation_positional.models:StemPairPositionalFact.natal_ordinal_distance",
    ),
    "NATAL_INTERVENING_VISIBLE_STEM_IDS": _spec(
        "Stem Relation Positional Context Foundation R1",
        "fortune_training.bazi_stem_relation_positional.models:StemPairPositionalFact.intervening_natal_visible_stem_instance_ids",
    ),
    "INTERVENER_STEM_IDENTITY": _spec(
        "Bazi Natal Foundation",
        "fortune_training.bazi_chart.models:BaziNatalState.stems",
        "fortune_training.bazi_chart.models:StemInstance.instance_id",
        "fortune_training.bazi_chart.models:StemInstance.stem",
    ),
    "NATAL_DAY_MASTER_PARTICIPATION": _spec(
        "Stem Relation Positional Context Foundation R1",
        "fortune_training.bazi_stem_relation_positional.models:StemParticipantPositionReference.is_natal_day_master_participant",
        "fortune_training.bazi_stem_relation_positional.models:StemPairPositionalFact.contains_natal_day_master_participant",
        "fortune_training.bazi_stem_relation_positional.models:StemPairPositionalFact.natal_day_master_participant_instance_ids",
    ),
    "PARTICIPANT_RELATION_DEGREE": _spec(
        "Bazi Relation Incidence Foundation R1",
        "fortune_training.bazi_relation_incidence.models:ParticipantRelationIncidenceFact.relation_ids",
        "fortune_training.bazi_relation_incidence.models:ParticipantRelationIncidenceFact.relation_count",
    ),
    "RELATION_PAIR_SHARED_PARTICIPANT_TOPOLOGY": _spec(
        "Bazi Relation Incidence Foundation R1",
        "fortune_training.bazi_relation_incidence.models:RelationPairTopologyFact.topology_kind",
        "fortune_training.bazi_relation_incidence.models:RelationPairTopologyFact.shared_participant_instance_ids",
    ),
    "NATAL_MONTH_COMMAND_REFERENCE": _spec(
        "Bazi Structural Support Foundation R1",
        "fortune_training.bazi_structural_support.models:BaziStructuralSupportContext.natal_month_command",
        "fortune_training.bazi_structural_support.models:NatalMonthCommandReference.role_id",
        "fortune_training.bazi_structural_support.models:NatalMonthCommandReference.source_branch_instance_id",
    ),
    "ACTIVE_FLOW_SOLAR_MONTH_REFERENCE": _spec(
        "Bazi Structural Support Foundation R1",
        "fortune_training.bazi_structural_support.models:BaziStructuralSupportContext.active_flow_solar_month",
        "fortune_training.bazi_structural_support.models:ActiveFlowSolarMonthReference.role_id",
        "fortune_training.bazi_structural_support.models:ActiveFlowSolarMonthReference.source_monthly_frame_id",
    ),
    "EXACT_HIDDEN_STEM_MATCH_REFERENCE": _spec(
        "Bazi Structural Support Foundation R1",
        "fortune_training.bazi_structural_support.models:SupportEvidenceCandidate.matching_hidden_stem_instance_ids",
        "fortune_training.bazi_structural_support.models:SupportEvidenceCandidate.evidence_class",
    ),
    "SAME_ELEMENT_HIDDEN_SUPPORT_REFERENCE": _spec(
        "Bazi Structural Support Foundation R1",
        "fortune_training.bazi_structural_support.models:SupportEvidenceCandidate.matching_hidden_stem_instance_ids",
        "fortune_training.bazi_structural_support.models:SupportEvidenceCandidate.evidence_class",
    ),
    "SUPPORT_TOUCH_REFERENCE": _spec(
        "Bazi Relation Incidence Foundation R1",
        "fortune_training.bazi_relation_incidence.models:ParticipantRelationIncidenceFact.support_evidence_candidate_ids",
        "fortune_training.bazi_relation_incidence.models:ParticipantRelationIncidenceFact.seasonal_role_reference_ids",
    ),
    "EXPOSURE_LINK_REFERENCE": _spec(
        "Bazi Natal Foundation / Structural Context R1",
        "fortune_training.bazi_chart.models:HiddenStemExposureLink.link_id",
        "fortune_training.bazi_chart.models:HiddenStemExposureLink.hidden_stem_instance_id",
        "fortune_training.bazi_chart.models:HiddenStemExposureLink.visible_stem_instance_id",
    ),
    "RELATION_TRANSITION_SET_MEMBERSHIP": _spec(
        "Bazi Relation Transition Foundation R1",
        "fortune_training.bazi_relation_transition.models:RawRelationTransitionFact.relation_id",
        "fortune_training.bazi_relation_transition.models:RawRelationTransitionFact.transition_state",
        "fortune_training.bazi_relation_transition.models:RawRelationTransitionFact.before_snapshot_id",
        "fortune_training.bazi_relation_transition.models:RawRelationTransitionFact.after_snapshot_id",
    ),
}


PRIMITIVE_BINDINGS: dict[str, tuple[tuple[str, str], ...]] = {
    "EXACT_RAW_RELATION_OCCURRENCES": (
        ("RELATION_OCCURRENCE_IDENTITY", "EXACT_IDENTITY_BINDING"),
    ),
    "EXACT_STEM_BRANCH_OCCURRENCE_IDS": (
        ("PARTICIPANT_STEM_IDENTITY", "EXACT_IDENTITY_BINDING"),
    ),
    "NATAL_MONTH_COMMAND": (
        ("NATAL_MONTH_COMMAND_REFERENCE", "EXACT_IDENTITY_BINDING"),
    ),
    "ACTIVE_FLOW_SOLAR_MONTH": (
        ("ACTIVE_FLOW_SOLAR_MONTH_REFERENCE", "EXACT_IDENTITY_BINDING"),
    ),
    "EXACT_HIDDEN_STEM_MATCH": (
        ("EXACT_HIDDEN_STEM_MATCH_REFERENCE", "RELATED_NEUTRAL_EVIDENCE"),
        ("SUPPORT_TOUCH_REFERENCE", "RELATED_NEUTRAL_EVIDENCE"),
    ),
    "SAME_ELEMENT_HIDDEN_SUPPORT": (
        ("SAME_ELEMENT_HIDDEN_SUPPORT_REFERENCE", "RELATED_NEUTRAL_EVIDENCE"),
        ("SUPPORT_TOUCH_REFERENCE", "RELATED_NEUTRAL_EVIDENCE"),
    ),
    "HIDDEN_STEM_MEMBERSHIP_AND_EXPOSURE": (
        ("EXACT_HIDDEN_STEM_MATCH_REFERENCE", "EXACT_IDENTITY_BINDING"),
        ("EXPOSURE_LINK_REFERENCE", "EXACT_IDENTITY_BINDING"),
    ),
    "RELATION_INCIDENCE_EXACT_TOPOLOGY": (
        ("PARTICIPANT_RELATION_DEGREE", "RELATED_NEUTRAL_EVIDENCE"),
        ("RELATION_PAIR_SHARED_PARTICIPANT_TOPOLOGY", "RELATED_NEUTRAL_EVIDENCE"),
    ),
    "PARTICIPANT_POSITION_LINEAGE": (
        ("NATAL_POSITION_DOMAIN", "RELATED_NEUTRAL_EVIDENCE"),
        ("NATAL_PILLAR_ORDINALS", "RELATED_NEUTRAL_EVIDENCE"),
        ("NATAL_ORDINAL_DISTANCE", "RELATED_NEUTRAL_EVIDENCE"),
        ("NATAL_INTERVENING_VISIBLE_STEM_IDS", "RELATED_NEUTRAL_EVIDENCE"),
        ("INTERVENER_STEM_IDENTITY", "RELATED_NEUTRAL_EVIDENCE"),
        ("NATAL_DAY_MASTER_PARTICIPATION", "RELATED_NEUTRAL_EVIDENCE"),
    ),
    "DAYUN_ANNUAL_MONTHLY_FRAME_CONTEXT": (
        ("PARTICIPANT_LAYER_IDENTITY", "RELATED_NEUTRAL_EVIDENCE"),
        ("TEMPORAL_FRAME_IDENTITY", "RELATED_NEUTRAL_EVIDENCE"),
    ),
    "RELATION_TRANSITION_BEFORE_AFTER": (
        ("RELATION_TRANSITION_SET_MEMBERSHIP", "RELATED_NEUTRAL_EVIDENCE"),
    ),
}

RATIONALES = {
    "RELATION_OCCURRENCE_IDENTITY": "The released occurrence reference preserves the exact relation and participant-scoped identity named by the source dependency.",
    "NOMINAL_TRANSFORMATION_ELEMENT_IDENTITY": "The released relation occurrence preserves only its nominal element identity; it does not publish a Classical result.",
    "PARTICIPANT_STEM_IDENTITY": "Released occurrence provenance preserves exact visible-stem instance and stem identities.",
    "PARTICIPANT_ELEMENT_IDENTITY": "The positional participant reference preserves the participant element identity.",
    "PARTICIPANT_POLARITY_IDENTITY": "The positional participant reference preserves the participant polarity identity.",
    "PARTICIPANT_LAYER_IDENTITY": "Released participant provenance preserves the typed Natal, Dayun, Annual, or Monthly layer.",
    "TEMPORAL_FRAME_IDENTITY": "Released participant provenance preserves the exact source frame identity when a temporal participant exists.",
    "NATAL_POSITION_DOMAIN": "The positional contract states whether the participant belongs to the Natal-pillar coordinate domain.",
    "NATAL_PILLAR_ORDINALS": "The positional contract preserves exact zero-based Natal pillar coordinates without Classical interpretation.",
    "NATAL_ORDINAL_DISTANCE": "The positional contract preserves arithmetic coordinate distance only.",
    "NATAL_INTERVENING_VISIBLE_STEM_IDS": "The positional contract preserves exact intervening visible-stem instance identities only.",
    "INTERVENER_STEM_IDENTITY": "Natal stem instances resolve each intervening instance ID to its exact stem identity.",
    "NATAL_DAY_MASTER_PARTICIPATION": "The positional contract preserves exact DAY.STEM participation identity only.",
    "PARTICIPANT_RELATION_DEGREE": "Incidence preserves exact relation membership and degree as neutral topology.",
    "RELATION_PAIR_SHARED_PARTICIPANT_TOPOLOGY": "Incidence preserves exact shared-participant topology only.",
    "NATAL_MONTH_COMMAND_REFERENCE": "Support R1 preserves the fixed typed Natal month-command reference.",
    "ACTIVE_FLOW_SOLAR_MONTH_REFERENCE": "Support R1 preserves the separately typed active Flow solar-month reference.",
    "EXACT_HIDDEN_STEM_MATCH_REFERENCE": "Support R1 preserves exact hidden-stem membership as neutral evidence.",
    "SAME_ELEMENT_HIDDEN_SUPPORT_REFERENCE": "Support R1 preserves same-element hidden support as related neutral evidence only.",
    "SUPPORT_TOUCH_REFERENCE": "Incidence preserves exact support-evidence reference IDs touching a participant.",
    "EXPOSURE_LINK_REFERENCE": "Natal and Structural contracts preserve exact hidden-to-visible exposure links.",
    "RELATION_TRANSITION_SET_MEMBERSHIP": "Transition R1 preserves exact before/after relation-set membership only.",
}


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _counter(records: Iterable[dict[str, Any]], field: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for record in records:
        value = record[field]
        counts.update(value if isinstance(value, list) else [value])
    return dict(sorted(counts.items()))


def _runtime_contract_manifest(root: Path) -> dict[str, str]:
    paths = sorted(
        {
            "src/" + path.split(":", 1)[0].replace(".", "/") + ".py"
            for spec in PREDICATE_SPECS.values()
            for path in spec["runtime_fact_or_field_paths"]
        }
        | {
            "schemas/bazi-chart-foundation-v1.schema.json",
            "schemas/bazi-structural-context-r1.schema.json",
            "schemas/bazi-structural-support-foundation-r1.schema.json",
            "schemas/bazi-relation-incidence-foundation-r1.schema.json",
            "schemas/bazi-relation-transition-foundation-r1.schema.json",
            "schemas/bazi-stem-relation-positional-context-foundation-r1.schema.json",
        }
    )
    return {path: sha256_file(root / path) for path in paths}


def _binding_id(evidence_id: str) -> str:
    return f"S14-FIVE-COMBINATION-BINDING:{_sha256((AUDIT_ID + ':' + evidence_id).encode('utf-8'))}"


def _binding_entry(predicate_kind: str, strength: str) -> dict[str, Any]:
    spec = PREDICATE_SPECS[predicate_kind]
    return {
        "predicate_kind": predicate_kind,
        "binding_assertion_strength": strength,
        "runtime_contract": spec["runtime_contract"],
        "runtime_fact_or_field_paths": spec["runtime_fact_or_field_paths"],
        "source_applicability_scope": "EXACT_EVIDENCE_RECORD_DEPENDENCY",
        "rationale": RATIONALES[predicate_kind],
    }


def _bindings_for(record: dict[str, Any]) -> list[dict[str, Any]]:
    by_kind: dict[str, dict[str, Any]] = {}
    for dependency in record["runtime_dependency_map"]:
        for predicate_kind, strength in PRIMITIVE_BINDINGS.get(dependency["primitive"], ()):
            candidate = _binding_entry(predicate_kind, strength)
            previous = by_kind.get(predicate_kind)
            if previous is None or (
                previous["binding_assertion_strength"] == "RELATED_NEUTRAL_EVIDENCE"
                and strength == "EXACT_IDENTITY_BINDING"
            ):
                by_kind[predicate_kind] = candidate
    if "TRANSFORMATION" in record["condition_dependency_tags"]:
        by_kind["NOMINAL_TRANSFORMATION_ELEMENT_IDENTITY"] = _binding_entry(
            "NOMINAL_TRANSFORMATION_ELEMENT_IDENTITY", "EXACT_IDENTITY_BINDING"
        )
    return [by_kind[key] for key in sorted(by_kind)]


def _unresolved_for(record: dict[str, Any]) -> list[str]:
    unresolved = set(record["runtime_gap_tags"])
    unresolved.update(
        dependency["primitive"]
        for dependency in record["runtime_dependency_map"]
        if dependency["status"] == "SOURCE_SEMANTICS_AMBIGUOUS"
    )
    return sorted(unresolved)


def _decision(record: dict[str, Any]) -> tuple[str, list[dict[str, Any]], list[str], bool, bool, str]:
    unresolved = _unresolved_for(record)
    profile_required = bool(record["conflict_group_ids"] or record["alternative_profile_labels"])
    source_ambiguous = record["review_status"] == "SOURCE_SEMANTICS_AMBIGUOUS" or any(
        dependency["status"] == "SOURCE_SEMANTICS_AMBIGUOUS"
        for dependency in record["runtime_dependency_map"]
    )

    if record["statement_class"] in NON_CONDITION_STATEMENT_CLASSES:
        return (
            "NON_CONDITION_RECORD",
            [],
            unresolved,
            source_ambiguous,
            profile_required,
            "Retained for exactly-once coverage; the source record is not compiled into a condition binding.",
        )
    if profile_required or record["review_status"] == "CONFLICT_REQUIRES_REVIEW":
        return (
            "PROFILE_ALTERNATIVE_UNRESOLVED",
            [],
            unresolved,
            source_ambiguous,
            True,
            "Source alternative metadata is preserved without selecting a profile.",
        )
    if source_ambiguous or record["statement_class"] in UNMAPPED_SOURCE_CONDITION_CLASSES:
        if record["statement_class"] in UNMAPPED_SOURCE_CONDITION_CLASSES:
            unresolved = sorted(set(unresolved) | {"SOURCE_CONDITION_SEMANTICS"})
        return (
            "NO_BINDING_SOURCE_SEMANTICS_AMBIGUOUS",
            [],
            unresolved,
            True,
            False,
            "No deterministic mapping to the closed neutral predicate registry is asserted.",
        )

    bindings = _bindings_for(record)
    if bindings and unresolved:
        disposition = "PARTIAL_BINDING"
    elif bindings and any(
        binding["binding_assertion_strength"] == "RELATED_NEUTRAL_EVIDENCE"
        for binding in bindings
    ):
        disposition = "RELATED_NEUTRAL_EVIDENCE_ONLY"
    elif bindings:
        disposition = "EXACT_NEUTRAL_BINDING"
    else:
        disposition = "NO_BINDING_MISSING_PRIMITIVE"
    note = {
        "PARTIAL_BINDING": "Released neutral facts cover only part of the source dependency; unresolved primitives remain explicit.",
        "RELATED_NEUTRAL_EVIDENCE_ONLY": "The catalog exposes related neutral facts without claiming doctrinal equivalence.",
        "EXACT_NEUTRAL_BINDING": "The source dependency is limited to identities represented by released neutral facts.",
        "NO_BINDING_MISSING_PRIMITIVE": "No released neutral predicate represents the source dependency.",
    }[disposition]
    return disposition, bindings, unresolved, source_ambiguous, False, note


def _build_record(record: dict[str, Any]) -> dict[str, Any]:
    disposition, bindings, unresolved, ambiguous, profile_required, note = _decision(record)
    return {
        "binding_id": _binding_id(record["evidence_id"]),
        "source_evidence_id": record["evidence_id"],
        "source_id": record["source_id"],
        "canonical_source_path": record["canonical_source_path"],
        "canonical_source_sha256": record["canonical_source_sha256"],
        "access_segment_id": record["access_segment_id"],
        "access_segment_path": record["access_segment_path"],
        "access_segment_sha256": record["access_segment_sha256"],
        "canonical_line_start": record["canonical_line_start"],
        "canonical_line_end": record["canonical_line_end"],
        "segment_local_line_start": record["segment_local_line_start"],
        "segment_local_line_end": record["segment_local_line_end"],
        "canonical_byte_start": record["canonical_byte_start"],
        "canonical_byte_end_exclusive": record["canonical_byte_end_exclusive"],
        "passage_sha256": record["passage_sha256"],
        "source_statement_class": record["statement_class"],
        "source_secondary_statement_classes": record["secondary_statement_classes"],
        "source_condition_dependency_tags": record["condition_dependency_tags"],
        "source_review_status": record["review_status"],
        "source_conflict_group_ids": record["conflict_group_ids"],
        "source_alternative_profile_labels": record["alternative_profile_labels"],
        "source_runtime_dependency_map": record["runtime_dependency_map"],
        "binding_disposition": disposition,
        "neutral_predicate_bindings": bindings,
        "unresolved_runtime_primitives": unresolved,
        "source_semantics_ambiguous": ambiguous,
        "profile_selection_required": profile_required,
        "binding_notes": note,
    }


def _summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    ambiguous = [
        record["source_evidence_id"]
        for record in records
        if record["source_semantics_ambiguous"]
    ]
    unbound = [
        record["source_evidence_id"]
        for record in records
        if not record["neutral_predicate_bindings"]
    ]
    conflict_groups = sorted(
        {
            group_id
            for record in records
            for group_id in record["source_conflict_group_ids"]
        }
    )
    profile_labels = sorted(
        {
            label
            for record in records
            for label in record["source_alternative_profile_labels"]
        }
    )
    predicate_counts: Counter[str] = Counter()
    missing_counts: Counter[str] = Counter()
    for record in records:
        predicate_counts.update(
            binding["predicate_kind"]
            for binding in record["neutral_predicate_bindings"]
        )
        missing_counts.update(record["unresolved_runtime_primitives"])
    return {
        "five_combination_evidence_count": len(records),
        "statement_class_counts": _counter(records, "source_statement_class"),
        "binding_disposition_counts": _counter(records, "binding_disposition"),
        "neutral_predicate_counts": dict(sorted(predicate_counts.items())),
        "missing_primitive_counts": dict(sorted(missing_counts.items())),
        "relevant_conflict_group_count": len(conflict_groups),
        "relevant_conflict_group_ids": conflict_groups,
        "relevant_profile_label_count": len(profile_labels),
        "relevant_profile_labels": profile_labels,
        "source_semantics_ambiguous_count": len(ambiguous),
        "source_semantics_ambiguous_evidence_ids": ambiguous,
        "unbound_record_count": len(unbound),
        "unbound_evidence_ids": unbound,
    }


def build_five_combination_evidence_bindings(root: Path) -> tuple[dict[str, Any], str]:
    root = root.resolve()
    access = validate_source_access(root, require_source_commit=False)
    evidence_report = validate_classical_relation_evidence(root)
    if (
        access["status"] != "PASS"
        or access["source_id"] != SOURCE_ID
        or access["canonical_sha256"] != EXPECTED_SOURCE_SHA256
        or access["round_trip_exact"] is not True
        or evidence_report["status"] != "PASS"
    ):
        raise TrainingError("Five-Combination evidence binding upstream gate failed")

    matrix = load_json(root / MATRIX_PATH)
    source_records = sorted(
        (
            record
            for record in matrix["records"]
            if SOURCE_FAMILY in record["relation_families"]
        ),
        key=lambda record: record["evidence_id"],
    )
    if len(source_records) != EXPECTED_EVIDENCE_COUNT:
        raise TrainingError(
            f"Five-Combination evidence regression count changed: {len(source_records)}"
        )
    records = [_build_record(record) for record in source_records]
    summary = _summary(records)
    contract_manifest = _runtime_contract_manifest(root)
    catalog = {
        "schema": AUDIT_ID,
        "audit_id": AUDIT_ID,
        "authority": {
            "source_id": SOURCE_ID,
            "canonical_source_sha256": EXPECTED_SOURCE_SHA256,
            "source_access_index_path": matrix["authority"]["source_access_index_path"],
            "source_access_index_sha256": matrix["authority"]["source_access_index_sha256"],
            "source_matrix_path": MATRIX_PATH.as_posix(),
            "source_matrix_sha256": sha256_file(root / MATRIX_PATH),
            "source_matrix_audit_id": matrix["audit_id"],
            "runtime_contract_file_sha256": contract_manifest,
            "runtime_contract_manifest_sha256": object_sha256(contract_manifest),
        },
        "scope": {
            "artifact_role": "STATIC_SOURCE_TO_RELEASED_NEUTRAL_RUNTIME_BINDING_ONLY",
            "source_relation_family": SOURCE_FAMILY,
            "per_chart_runtime_evaluator_released": False,
            "classical_outcome_semantics_released": False,
            "free_text_semantic_compiler_used": False,
            "profile_default_selected": False,
        },
        "method": {
            "algorithm_id": "S14_FIVE_COMBINATION_MATRIX_METADATA_BINDING_R1",
            "algorithm_version": "1.0.0",
            "source_selection": "MATRIX_RELATION_FAMILY_EXACT_MEMBERSHIP",
            "binding_input": "REVIEWED_MATRIX_METADATA_NOT_SOURCE_FREE_TEXT",
            "ordering": "SOURCE_EVIDENCE_ID_ASCENDING",
            "expected_regression_count": EXPECTED_EVIDENCE_COUNT,
        },
        "closed_vocabularies": {
            "binding_dispositions": list(BINDING_DISPOSITIONS),
            "binding_assertion_strengths": list(BINDING_ASSERTION_STRENGTHS),
            "neutral_predicate_kinds": list(NEUTRAL_PREDICATE_KINDS),
            "required_unresolved_primitives": list(REQUIRED_UNRESOLVED_PRIMITIVES),
        },
        "runtime_predicate_registry": PREDICATE_SPECS,
        "records": records,
        "summary": summary,
        "determinism": {
            "records_semantics_sha256": object_sha256(records),
            "closed_registry_sha256": object_sha256(PREDICATE_SPECS),
            "catalog_semantics_sha256": object_sha256(
                {
                    "records": records,
                    "summary": summary,
                    "runtime_predicate_registry": PREDICATE_SPECS,
                    "runtime_contract_manifest_sha256": object_sha256(contract_manifest),
                }
            ),
        },
    }
    return catalog, _build_report(catalog)


def _table(lines: list[str], title: str, values: dict[str, int]) -> None:
    lines.extend([f"## {title}", "", "| Value | Count |", "|---|---:|"])
    for key, count in values.items():
        lines.append(f"| `{key}` | {count} |")
    lines.append("")


def _build_report(catalog: dict[str, Any]) -> str:
    summary = catalog["summary"]
    lines = [
        "# Bazi Stem Five-Combination Eligibility Evidence Binding R1 — Coverage Report",
        "",
        "Status: static source-to-released-neutral-runtime evidence binding only.",
        "",
        "## Coverage",
        "",
        f"- Current `STEM_FIVE_COMBINATION` evidence records: `{summary['five_combination_evidence_count']}`",
        "- Coverage: exactly once by source evidence ID.",
        f"- Source-semantics ambiguous records: `{summary['source_semantics_ambiguous_count']}`",
        f"- Records with no neutral predicate binding: `{summary['unbound_record_count']}`",
        f"- Relevant conflict groups: `{summary['relevant_conflict_group_count']}`",
        f"- Relevant alternative profile labels: `{summary['relevant_profile_label_count']}`",
        "",
    ]
    _table(lines, "Primary source statement classes", summary["statement_class_counts"])
    _table(lines, "Binding dispositions", summary["binding_disposition_counts"])
    _table(lines, "Neutral predicate kinds", summary["neutral_predicate_counts"])
    _table(lines, "Unresolved primitives", summary["missing_primitive_counts"])
    lines.extend(["## Conflict and profile metadata", ""])
    if summary["relevant_conflict_group_ids"]:
        lines.extend(f"- Conflict group: `{value}`" for value in summary["relevant_conflict_group_ids"])
    else:
        lines.append("- No Five-Combination record in the current matrix carries a conflict group.")
    if summary["relevant_profile_labels"]:
        lines.extend(f"- Profile label: `{value}`" for value in summary["relevant_profile_labels"])
    else:
        lines.append("- No Five-Combination record in the current matrix carries an alternative profile label.")
    lines.extend(["", "## Source-semantics ambiguous evidence", ""])
    if summary["source_semantics_ambiguous_evidence_ids"]:
        lines.extend(f"- `{value}`" for value in summary["source_semantics_ambiguous_evidence_ids"])
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Semantic boundary",
            "",
            "Coordinates, intervening stem identities, Day-Master identity, incidence degree, shared-participant topology, support references, typed month roles, and transition-set membership remain neutral facts. The catalog does not attach Classical effect, ordering, dominance, strength, or outcome meaning to them.",
            "",
            "Natal month command and active Flow solar month remain distinct typed references and are never substituted.",
            "",
            "No per-chart Five-Combination condition evaluator or Classical relation outcome evaluator is released.",
            "",
            "## Determinism",
            "",
            f"- Records semantics SHA-256: `{catalog['determinism']['records_semantics_sha256']}`",
            f"- Closed registry SHA-256: `{catalog['determinism']['closed_registry_sha256']}`",
            f"- Catalog semantics SHA-256: `{catalog['determinism']['catalog_semantics_sha256']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_five_combination_evidence_bindings(root: Path) -> dict[str, Any]:
    catalog, report = build_five_combination_evidence_bindings(root)
    atomic_write_json(root / BINDINGS_PATH, catalog)
    atomic_write_bytes(root / REPORT_PATH, report.encode("utf-8"))
    return {
        "status": "BUILT",
        "audit_id": AUDIT_ID,
        "bindings_path": BINDINGS_PATH.as_posix(),
        "report_path": REPORT_PATH.as_posix(),
        **catalog["summary"],
        **catalog["determinism"],
    }


def _validate_schema(root: Path, catalog: dict[str, Any]) -> None:
    schema = load_json(root / SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(catalog),
        key=lambda error: list(error.path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(item) for item in error.path) or "<root>"
        raise TrainingError(f"Five-Combination binding schema failed at {location}: {error.message}")


def _validate_runtime_field_path(path: str) -> None:
    try:
        module_name, target = path.split(":", 1)
        class_name, field_name = target.split(".", 1)
        value = getattr(importlib.import_module(module_name), class_name)
    except (ValueError, ImportError, AttributeError) as exc:
        raise TrainingError(f"unresolved runtime contract path: {path}") from exc
    if not is_dataclass(value) or field_name not in {field.name for field in fields(value)}:
        raise TrainingError(f"unresolved runtime contract field: {path}")


def _validate_locator_replay(root: Path, binding: dict[str, Any], source: dict[str, Any]) -> None:
    for field in (
        "source_evidence_id",
        "source_id",
        "canonical_source_path",
        "canonical_source_sha256",
        "access_segment_id",
        "access_segment_path",
        "access_segment_sha256",
        "canonical_line_start",
        "canonical_line_end",
        "segment_local_line_start",
        "segment_local_line_end",
        "canonical_byte_start",
        "canonical_byte_end_exclusive",
        "passage_sha256",
    ):
        source_field = "evidence_id" if field == "source_evidence_id" else field
        if binding[field] != source[source_field]:
            raise TrainingError(f"source binding metadata mismatch: {binding['source_evidence_id']}:{field}")
    segment_path = root / binding["access_segment_path"]
    if sha256_file(segment_path) != binding["access_segment_sha256"]:
        raise TrainingError(f"access segment hash replay failed: {binding['source_evidence_id']}")
    canonical_payload = (root / binding["canonical_source_path"]).read_bytes()
    passage = canonical_payload[
        binding["canonical_byte_start"] : binding["canonical_byte_end_exclusive"]
    ]
    if _sha256(passage) != binding["passage_sha256"]:
        raise TrainingError(f"canonical passage hash replay failed: {binding['source_evidence_id']}")
    index = load_json(root / DERIVED_ACCESS_ROOT / SOURCE_ID / "index.json")
    segment = next(
        item for item in index["segments"] if item["segment_id"] == binding["access_segment_id"]
    )
    local_start = binding["canonical_byte_start"] - segment["byte_start"]
    local_end = binding["canonical_byte_end_exclusive"] - segment["byte_start"]
    if segment_path.read_bytes()[local_start:local_end] != passage:
        raise TrainingError(f"segment passage replay failed: {binding['source_evidence_id']}")


def validate_five_combination_evidence_binding_value(
    root: Path, catalog: dict[str, Any]
) -> dict[str, Any]:
    root = root.resolve()
    expected, expected_report = build_five_combination_evidence_bindings(root)
    _validate_schema(root, catalog)
    if catalog != expected:
        raise TrainingError("Five-Combination binding catalog is stale, tampered, or non-deterministic")

    matrix = load_json(root / MATRIX_PATH)
    source_records = {
        record["evidence_id"]: record
        for record in matrix["records"]
        if SOURCE_FAMILY in record["relation_families"]
    }
    evidence_ids = [record["source_evidence_id"] for record in catalog["records"]]
    if len(evidence_ids) != EXPECTED_EVIDENCE_COUNT or len(set(evidence_ids)) != len(evidence_ids):
        raise TrainingError("Five-Combination evidence coverage is not exactly once")
    if set(evidence_ids) != set(source_records):
        raise TrainingError("Five-Combination binding evidence inventory mismatch")

    for binding in catalog["records"]:
        source = source_records[binding["source_evidence_id"]]
        _validate_locator_replay(root, binding, source)
        if binding["source_conflict_group_ids"] != source["conflict_group_ids"]:
            raise TrainingError("source conflict metadata was not preserved")
        if binding["source_alternative_profile_labels"] != source["alternative_profile_labels"]:
            raise TrainingError("source profile metadata was not preserved")
        for predicate in binding["neutral_predicate_bindings"]:
            kind = predicate["predicate_kind"]
            if kind not in NEUTRAL_PREDICATE_KINDS or kind not in PREDICATE_SPECS:
                raise TrainingError(f"predicate is outside the closed registry: {kind}")
            if predicate["binding_assertion_strength"] not in BINDING_ASSERTION_STRENGTHS:
                raise TrainingError("binding assertion strength is outside the closed registry")
            for path in predicate["runtime_fact_or_field_paths"]:
                _validate_runtime_field_path(path)

    positional_kinds = {
        "NATAL_POSITION_DOMAIN",
        "NATAL_PILLAR_ORDINALS",
        "NATAL_ORDINAL_DISTANCE",
        "NATAL_INTERVENING_VISIBLE_STEM_IDS",
        "INTERVENER_STEM_IDENTITY",
        "NATAL_DAY_MASTER_PARTICIPATION",
    }
    support_kinds = {
        "EXACT_HIDDEN_STEM_MATCH_REFERENCE",
        "SAME_ELEMENT_HIDDEN_SUPPORT_REFERENCE",
    }
    for binding in catalog["records"]:
        by_kind = {
            row["predicate_kind"]: row for row in binding["neutral_predicate_bindings"]
        }
        if any(
            by_kind[kind]["binding_assertion_strength"] != "RELATED_NEUTRAL_EVIDENCE"
            for kind in positional_kinds & set(by_kind)
        ):
            raise TrainingError("positional coordinates were upgraded beyond neutral evidence")
        if any(
            by_kind[kind]["binding_assertion_strength"] != "RELATED_NEUTRAL_EVIDENCE"
            for kind in support_kinds & set(by_kind)
            if "ROOT_OR_SUPPORT" in binding["source_condition_dependency_tags"]
        ):
            raise TrainingError("support evidence was upgraded beyond neutral evidence")
        shared = by_kind.get("RELATION_PAIR_SHARED_PARTICIPANT_TOPOLOGY")
        if shared and shared["binding_assertion_strength"] != "RELATED_NEUTRAL_EVIDENCE":
            raise TrainingError("shared-participant topology was upgraded beyond neutral evidence")

    if PREDICATE_SPECS["NATAL_MONTH_COMMAND_REFERENCE"] == PREDICATE_SPECS["ACTIVE_FLOW_SOLAR_MONTH_REFERENCE"]:
        raise TrainingError("Natal and active Flow month roles were merged")
    for primitive in REQUIRED_UNRESOLVED_PRIMITIVES:
        relevant = [
            source
            for source in source_records.values()
            if primitive in source["runtime_gap_tags"]
        ]
        if relevant and any(
            primitive not in expected_record["unresolved_runtime_primitives"]
            for source in relevant
            for expected_record in [
                next(row for row in catalog["records"] if row["source_evidence_id"] == source["evidence_id"])
            ]
        ):
            raise TrainingError(f"required unresolved primitive was lost: {primitive}")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        **catalog["summary"],
        **catalog["determinism"],
        "source_locator_replay": True,
        "runtime_field_path_resolution": True,
        "deterministic_rebuild": True,
        "report_sha256": _sha256(expected_report.encode("utf-8")),
    }


def validate_five_combination_evidence_bindings(root: Path) -> dict[str, Any]:
    root = root.resolve()
    catalog = load_json(root / BINDINGS_PATH)
    report = (root / REPORT_PATH).read_text(encoding="utf-8")
    result = validate_five_combination_evidence_binding_value(root, catalog)
    _, expected_report = build_five_combination_evidence_bindings(root)
    if report != expected_report:
        raise TrainingError("Five-Combination coverage report is stale or tampered")
    return result

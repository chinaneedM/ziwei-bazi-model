from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

from .bazi_facts import (
    validate_bazi_atomic_fact_ledger,
    validate_bazi_strength_chain,
)
from .util import TrainingError, object_sha256


PREDICTION_SCHEMA = "PREDICTION-WORKBOOK-V2"
FROZEN_SCHEMA = "FROZEN-PREDICTION-V2"
CONFIDENCE_COMPONENTS = (
    "input_confidence",
    "natal_structure_confidence",
    "subject_confidence",
    "mechanism_confidence",
    "timing_confidence",
    "reality_endpoint_confidence",
    "cross_track_agreement",
    "top1_top2_separation",
    "overall_confidence",
)
ROOT_CAUSES = {
    "INPUT_RECOGNITION",
    "QUESTION_SEMANTICS",
    "NATAL_STRUCTURE",
    "ZIWEI_REASONING",
    "BAZI_REASONING",
    "PERIOD_TIMING",
    "SUBJECT_ROUTING",
    "EVENT_MECHANISM",
    "REALITY_TRANSLATION",
    "OPTION_COMPARISON",
    "EVIDENCE_WEIGHTING",
    "CONFIDENCE_CALIBRATION",
    "EXECUTION_OMISSION",
    "SYSTEM_SCHEMA",
    "DATA_OR_ANSWER_AMBIGUITY",
}
REMEDIATION_TYPES = {
    "EXECUTION_GATE",
    "MEASUREMENT_CHANGE",
    "CALIBRATION_CHANGE",
    "RULE_WEIGHT_CHANGE",
    "RULE_SCOPE_CHANGE",
    "RULE_MERGE",
    "RULE_RETIREMENT",
    "TEST_ADDITION",
    "HYPOTHESIS_ONLY",
    "NEW_GENERAL_RULE",
}
EVIDENCE_FIELDS = {
    "evidence_id",
    "track",
    "layer",
    "chart_fact",
    "source_route",
    "knowledge_point",
    "applicability_conditions",
    "conditions_satisfied",
    "supports_option_atoms",
    "contradicts_option_atoms",
    "alternative_explanation",
    "evidence_family_id",
    "independence_status",
    "reliability",
    "capability_ceiling",
    "decision_impact",
    "limitations",
}
EVIDENCE_SCOPE_FIELDS = {
    "axis_distance",
    "transmission_path",
    "temporal_role",
    "scope_id",
}

_TIME_WINDOW_ATOM = re.compile(
    r"^(?:约|大约|第)?\d{1,4}(?:\s*(?:-|–|—|~|～|至|到)\s*\d{1,4})?"
    r"\s*(?:岁|年|年代|月|日|周|天|时|点|季度|季)"
    r"(?:以前|以后|前|后|间|内|左右|上下)?$"
)


def _object(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise TrainingError(f"{label} must contain exactly: {', '.join(sorted(fields))}")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TrainingError(f"{label} must be a non-empty string")
    return value.strip()


def _texts(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    if (
        not isinstance(value, list)
        or (not allow_empty and not value)
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise TrainingError(f"{label} must be a list of non-empty strings")
    normalized = [item.strip() for item in value]
    if len(normalized) != len(set(normalized)):
        raise TrainingError(f"{label} must not contain duplicates")
    return normalized


def _ranking(value: Any, option_ids: list[str], label: str) -> list[str]:
    if not isinstance(value, list) or value != list(dict.fromkeys(value)):
        raise TrainingError(f"{label} must be a unique option ranking")
    if set(value) != set(option_ids) or len(value) != len(option_ids):
        raise TrainingError(f"{label} must rank every option exactly once")
    return value


def _confidence(value: Any, label: str) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value < 0
        or value > 100
    ):
        raise TrainingError(f"{label} must be an integer from 0 to 100")
    return value


def _walk_forbidden(value: Any, label: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if "answer" in lowered or lowered in {"correct_option", "expected_result"}:
                raise TrainingError(f"answer-bearing field is forbidden in reasoning: {label}.{key}")
            _walk_forbidden(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden(child, f"{label}[{index}]")


def validate_blind_chart_model(case: dict[str, Any], value: Any) -> dict[str, Any]:
    model = _object(
        value,
        {
            "schema",
            "input_reliability",
            "ziwei_static_model",
            "bazi_static_model",
            "shared_life_structure",
        },
        "blind_chart_model",
    )
    if model["schema"] not in {"BLIND-CHART-MODEL-V1", "BLIND-CHART-MODEL-V2"}:
        raise TrainingError("blind_chart_model has an unsupported schema")
    _walk_forbidden(model, "$.blind_chart_model")
    reliability = _object(
        model["input_reliability"],
        {
            "gender",
            "calendar",
            "birth_time",
            "birth_place",
            "four_pillars",
            "ziwei_coordinates",
            "major_periods",
            "missing_fields",
            "conflicting_fields",
            "unreliable_fields",
            "forbidden_inferences",
        },
        "blind_chart_model.input_reliability",
    )
    for field in (
        "gender",
        "calendar",
        "birth_time",
        "birth_place",
        "four_pillars",
        "ziwei_coordinates",
        "major_periods",
    ):
        _text(reliability[field], f"input_reliability.{field}")
    for field in (
        "missing_fields",
        "conflicting_fields",
        "unreliable_fields",
        "forbidden_inferences",
    ):
        _texts(reliability[field], f"input_reliability.{field}")

    ziwei = _object(
        model["ziwei_static_model"],
        {
            "chart_facts",
            "palace_and_star_structures",
            "transformations_and_lines",
            "advanced_method_applicability",
            "structural_conflicts",
            "limitations",
        },
        "blind_chart_model.ziwei_static_model",
    )
    bazi_fields = {
        "chart_facts",
        "seasonal_strength_candidates",
        "pattern_candidates",
        "method_competition",
        "relations_and_structural_changes",
        "useful_harmful_candidates",
        "unresolved_disputes",
        "limitations",
    }
    if model["schema"] == "BLIND-CHART-MODEL-V2":
        bazi_fields |= {
            "immutable_atomic_fact_ledger",
            "strength_structure_favorability_chain",
        }
    bazi = _object(
        model["bazi_static_model"],
        bazi_fields,
        "blind_chart_model.bazi_static_model",
    )
    if model["schema"] == "BLIND-CHART-MODEL-V2":
        atomic_ledger = validate_bazi_atomic_fact_ledger(
            bazi["immutable_atomic_fact_ledger"]
        )
        validate_bazi_strength_chain(
            atomic_ledger,
            bazi["strength_structure_favorability_chain"],
        )
    shared = _object(
        model["shared_life_structure"],
        {
            "personality_and_behavior",
            "family_roles",
            "marriage_capacity",
            "children_axis",
            "career_and_wealth",
            "health_capacity",
            "migration_assets_social",
            "period_themes",
            "major_conflicts",
            "unknowns",
        },
        "blind_chart_model.shared_life_structure",
    )
    for label, section in (
        ("ziwei_static_model", ziwei),
        ("bazi_static_model", bazi),
        ("shared_life_structure", shared),
    ):
        for field, field_value in section.items():
            if field in {
                "immutable_atomic_fact_ledger",
                "strength_structure_favorability_chain",
            }:
                continue
            _texts(field_value, f"{label}.{field}", allow_empty=field in {"structural_conflicts", "unresolved_disputes", "major_conflicts", "unknowns"})

    serialized = json.dumps(model, ensure_ascii=False)
    for question in case["questions"]["parsed"]:
        for option in question["options"]:
            option_text = " ".join(str(option.get("text", "")).split())
            if len(option_text) >= 8 and option_text in serialized:
                raise TrainingError("blind_chart_model may not copy option text")
    return model


def _validate_semantics(value: Any, option_ids: list[str], question_id: str) -> dict[str, Any]:
    model = _object(
        value,
        {
            "target",
            "subject",
            "time_range",
            "action_subject",
            "reality_object",
            "event_process",
            "completion_endpoint",
            "magnitude",
            "is_composite_narrative",
            "option_atoms",
            "shared_non_discriminating_atoms",
            "ambiguities",
        },
        f"{question_id}.question_semantic_model",
    )
    for field in (
        "target",
        "subject",
        "time_range",
        "action_subject",
        "reality_object",
        "event_process",
        "completion_endpoint",
        "magnitude",
    ):
        _text(model[field], f"{question_id}.question_semantic_model.{field}")
    if not isinstance(model["is_composite_narrative"], bool):
        raise TrainingError(f"{question_id}.is_composite_narrative must be boolean")
    atoms = model["option_atoms"]
    if not isinstance(atoms, dict) or set(atoms) != set(option_ids):
        raise TrainingError(f"{question_id}.option_atoms must cover every option")
    for option_id, atom_model in atoms.items():
        atom_model = _object(
            atom_model,
            {
                "required_atoms",
                "distinctive_atoms",
                "severe_irreversible_or_high_precision_atoms",
            },
            f"{question_id}.option_atoms.{option_id}",
        )
        _texts(atom_model["required_atoms"], f"{question_id}.{option_id}.required_atoms", allow_empty=False)
        _texts(atom_model["distinctive_atoms"], f"{question_id}.{option_id}.distinctive_atoms", allow_empty=False)
        _texts(
            atom_model["severe_irreversible_or_high_precision_atoms"],
            f"{question_id}.{option_id}.severe_atoms",
        )
    _texts(model["shared_non_discriminating_atoms"], f"{question_id}.shared_atoms")
    _texts(model["ambiguities"], f"{question_id}.ambiguities")
    return model


def _is_pure_time_window_comparison(semantics: dict[str, Any]) -> bool:
    """Return true only when option differences are explicit time windows."""

    if semantics["is_composite_narrative"]:
        return False
    atoms = semantics.get("option_atoms")
    if not isinstance(atoms, dict) or len(atoms) < 2:
        return False

    windows: list[str] = []
    shared_required_atoms: set[str] | None = None
    for atom_model in atoms.values():
        if not isinstance(atom_model, dict):
            return False
        required_atoms = atom_model.get("required_atoms")
        distinctive_atoms = atom_model.get("distinctive_atoms")
        if (
            not isinstance(required_atoms, list)
            or not isinstance(distinctive_atoms, list)
            or len(distinctive_atoms) != 1
        ):
            return False
        window = distinctive_atoms[0].strip()
        if not _TIME_WINDOW_ATOM.fullmatch(window) or window not in required_atoms:
            return False
        windows.append(window)
        option_shared_atoms = set(required_atoms) - {window}
        if shared_required_atoms is None:
            shared_required_atoms = option_shared_atoms
        elif option_shared_atoms != shared_required_atoms:
            return False

    return len(windows) == len(set(windows))


def _validate_evidence(
    value: Any,
    *,
    option_ids: list[str],
    source_routes: list[str],
    question_id: str,
    allow_timing_only: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if not isinstance(value, list) or not value:
        raise TrainingError(f"{question_id}.evidence_ledger must be non-empty")
    rows: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    fact_families: dict[str, str] = {}
    for raw in value:
        if not isinstance(raw, dict):
            raise TrainingError(f"{question_id}.evidence must be an object")
        raw_fields = frozenset(raw)
        scoped = raw_fields == frozenset(EVIDENCE_FIELDS | EVIDENCE_SCOPE_FIELDS)
        if raw_fields not in {
            frozenset(EVIDENCE_FIELDS),
            frozenset(EVIDENCE_FIELDS | EVIDENCE_SCOPE_FIELDS),
        }:
            raise TrainingError(f"{question_id}.evidence has invalid fields")
        row = raw
        evidence_id = _text(row["evidence_id"], f"{question_id}.evidence_id")
        if evidence_id in by_id:
            raise TrainingError(f"{question_id} has duplicate evidence_id: {evidence_id}")
        if row["track"] not in {"ZIWEI", "BAZI", "REALITY"}:
            raise TrainingError(f"{question_id}.{evidence_id} has invalid track")
        if row["layer"] not in {"NATAL", "PERIOD", "YEAR", "MONTH", "REALITY"}:
            raise TrainingError(f"{question_id}.{evidence_id} has invalid layer")
        _text(row["chart_fact"], f"{question_id}.{evidence_id}.chart_fact")
        if row["source_route"] not in source_routes:
            raise TrainingError(f"{question_id}.{evidence_id} source_route is not declared")
        _text(row["knowledge_point"], f"{question_id}.{evidence_id}.knowledge_point")
        _texts(row["applicability_conditions"], f"{question_id}.{evidence_id}.applicability_conditions", allow_empty=False)
        _texts(row["conditions_satisfied"], f"{question_id}.{evidence_id}.conditions_satisfied", allow_empty=False)
        for field in ("supports_option_atoms", "contradicts_option_atoms"):
            refs = _texts(row[field], f"{question_id}.{evidence_id}.{field}")
            if any(ref.split(":", 1)[0] not in option_ids or ":" not in ref for ref in refs):
                raise TrainingError(f"{question_id}.{evidence_id}.{field} has an invalid option-atom reference")
        _text(row["alternative_explanation"], f"{question_id}.{evidence_id}.alternative_explanation")
        family = _text(row["evidence_family_id"], f"{question_id}.{evidence_id}.evidence_family_id")
        if row["independence_status"] not in {"INDEPENDENT", "SAME_FAMILY", "NEUTRAL_BACKGROUND"}:
            raise TrainingError(f"{question_id}.{evidence_id} has invalid independence_status")
        if row["reliability"] not in {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}:
            raise TrainingError(f"{question_id}.{evidence_id} has invalid reliability")
        if row["decision_impact"] not in {"DECISIVE", "SUPPORTING", "COUNTEREVIDENCE", "NEUTRAL"}:
            raise TrainingError(f"{question_id}.{evidence_id} has invalid decision_impact")
        if scoped:
            distance = row["axis_distance"]
            path = _texts(
                row["transmission_path"],
                f"{question_id}.{evidence_id}.transmission_path",
            )
            expected_path_length = {
                "DIRECT_SAME_AXIS": 0,
                "ONE_HOP": 1,
            }
            if distance in expected_path_length and len(path) != expected_path_length[distance]:
                raise TrainingError(
                    f"{question_id}.{evidence_id} evidence distance/path mismatch"
                )
            if distance == "MULTI_HOP" and len(path) < 2:
                raise TrainingError(
                    f"{question_id}.{evidence_id} multi-hop evidence needs every intermediate link"
                )
            if distance not in {"DIRECT_SAME_AXIS", "ONE_HOP", "MULTI_HOP"}:
                raise TrainingError(f"{question_id}.{evidence_id} has invalid axis_distance")
            temporal_role = row["temporal_role"]
            if temporal_role not in {
                "NATAL_STATIC",
                "PERIOD_CONTEXT",
                "ACTIVE_QUERY_OBJECT",
                "HISTORICAL_VALIDATION_ANCHOR",
                "REALITY_ENDPOINT",
            }:
                raise TrainingError(f"{question_id}.{evidence_id} has invalid temporal_role")
            _text(row["scope_id"], f"{question_id}.{evidence_id}.scope_id")
            allowed_layers = {
                "NATAL_STATIC": {"NATAL"},
                "PERIOD_CONTEXT": {"PERIOD"},
                "ACTIVE_QUERY_OBJECT": {"PERIOD", "YEAR", "MONTH"},
                "HISTORICAL_VALIDATION_ANCHOR": {"YEAR", "MONTH", "REALITY"},
                "REALITY_ENDPOINT": {"REALITY"},
            }
            if row["layer"] not in allowed_layers[temporal_role]:
                raise TrainingError(
                    f"{question_id}.{evidence_id} temporal role/layer mismatch"
                )
            if temporal_role == "HISTORICAL_VALIDATION_ANCHOR" and (
                row["decision_impact"] != "NEUTRAL"
                or row["independence_status"] != "NEUTRAL_BACKGROUND"
            ):
                raise TrainingError(
                    f"{question_id}.{evidence_id} historical anchor may not become an active decision object"
                )
        if row["independence_status"] == "NEUTRAL_BACKGROUND":
            if row["decision_impact"] != "NEUTRAL":
                raise TrainingError(
                    f"{question_id}.{evidence_id} neutral background must have NEUTRAL decision_impact"
                )
            if row["contradicts_option_atoms"]:
                raise TrainingError(
                    f"{question_id}.{evidence_id} neutral background may not contradict option atoms"
                )
        for field in ("capability_ceiling", "limitations"):
            _text(row[field], f"{question_id}.{evidence_id}.{field}")
        normalized_fact = " ".join(row["chart_fact"].split()).casefold()
        previous_family = fact_families.setdefault(normalized_fact, family)
        if previous_family != family:
            raise TrainingError(f"{question_id} repeats one chart fact across different evidence families")
        rows.append(row)
        by_id[evidence_id] = row
    if not {"ZIWEI", "BAZI"}.issubset({row["track"] for row in rows}):
        raise TrainingError(f"{question_id} needs concrete evidence from both Ziwei and Bazi")
    if not allow_timing_only and not any(
        row["layer"] in {"NATAL", "REALITY"}
        and row["decision_impact"] != "NEUTRAL"
        for row in rows
    ):
        raise TrainingError(
            f"{question_id} may not use timing signals alone to close the decision"
        )
    return rows, by_id


def _validate_bazi_dynamic_relation_scope(value: Any, question_id: str) -> dict[str, Any]:
    scope = _object(
        value,
        {
            "query_scope_id",
            "active_dynamic_object_ids",
            "historical_anchor_ids",
            "cross_time_reactivation",
        },
        f"{question_id}.bazi_dynamic_relation_scope",
    )
    _text(scope["query_scope_id"], f"{question_id}.bazi_dynamic_relation_scope.query_scope_id")
    active = _texts(
        scope["active_dynamic_object_ids"],
        f"{question_id}.bazi_dynamic_relation_scope.active_dynamic_object_ids",
    )
    historical = _texts(
        scope["historical_anchor_ids"],
        f"{question_id}.bazi_dynamic_relation_scope.historical_anchor_ids",
    )
    reactivation = _object(
        scope["cross_time_reactivation"],
        {"status", "method", "source_route", "bounded_object_ids"},
        f"{question_id}.bazi_dynamic_relation_scope.cross_time_reactivation",
    )
    bounded = _texts(
        reactivation["bounded_object_ids"],
        f"{question_id}.bazi_dynamic_relation_scope.bounded_object_ids",
    )
    overlap = set(active) & set(historical)
    if reactivation["status"] == "NOT_USED":
        if (
            reactivation["method"] != "NOT_APPLICABLE"
            or reactivation["source_route"] != "NOT_APPLICABLE"
            or bounded
            or overlap
        ):
            raise TrainingError(
                f"{question_id} silently reactivates a historical Bazi object"
            )
    elif reactivation["status"] == "DECLARED_METHOD":
        _text(reactivation["method"], f"{question_id}.bazi_dynamic_relation_scope.method")
        if reactivation["method"] == "NOT_APPLICABLE":
            raise TrainingError(f"{question_id} lacks a declared cross-time method")
        if not re.fullmatch(r"S(?:0[0-9]|1[0-9])", str(reactivation["source_route"])):
            raise TrainingError(f"{question_id} has an invalid cross-time source route")
        if not bounded or not set(bounded).issubset(set(active) | set(historical)):
            raise TrainingError(f"{question_id} cross-time method is not object-bounded")
    else:
        raise TrainingError(f"{question_id} has invalid cross-time reactivation status")
    return scope


def _validate_track(
    value: Any,
    *,
    track: str,
    option_ids: list[str],
    evidence_by_id: dict[str, dict[str, Any]],
    question_id: str,
) -> dict[str, Any]:
    analysis_fields = (
        {"core_structure", "dynamic_trigger"}
        if track == "ZIWEI"
        else {"strength_and_pattern", "method_competition", "luck_timing"}
    )
    seal_fields = {
        "top1",
        "top2",
        "ranking",
        *analysis_fields,
        "endpoint_chain",
        "supporting_evidence_ids",
        "contradicting_evidence_ids",
        "alternative_explanations",
        "unresolved_links",
        "capability_ceiling",
        "confidence",
    }
    if track == "BAZI" and isinstance(value, dict) and "dynamic_relation_scope" in value:
        seal_fields.add("dynamic_relation_scope")
    seal = _object(
        value,
        seal_fields,
        f"{question_id}.{track.lower()}_track_seal",
    )
    if seal["top1"] not in option_ids or seal["top2"] not in option_ids or seal["top1"] == seal["top2"]:
        raise TrainingError(f"{question_id}.{track} track has invalid Top1/Top2")
    ranking = _ranking(seal["ranking"], option_ids, f"{question_id}.{track}.ranking")
    if ranking[:2] != [seal["top1"], seal["top2"]]:
        raise TrainingError(f"{question_id}.{track} ranking does not match Top1/Top2")
    for field in analysis_fields:
        _text(seal[field], f"{question_id}.{track}.{field}")
    chain = _object(
        seal["endpoint_chain"],
        {"subject", "action", "object", "endpoint"},
        f"{question_id}.{track}.endpoint_chain",
    )
    for field, text in chain.items():
        _text(text, f"{question_id}.{track}.endpoint_chain.{field}")
    used_ids: list[str] = []
    for field in ("supporting_evidence_ids", "contradicting_evidence_ids"):
        ids = _texts(seal[field], f"{question_id}.{track}.{field}", allow_empty=field == "contradicting_evidence_ids")
        for evidence_id in ids:
            evidence = evidence_by_id.get(evidence_id)
            if evidence is None or evidence["track"] != track:
                raise TrainingError(f"{question_id}.{track} references evidence from another track")
            if field == "contradicting_evidence_ids" and (
                evidence["decision_impact"] == "NEUTRAL"
                or evidence["independence_status"] == "NEUTRAL_BACKGROUND"
            ):
                raise TrainingError(
                    f"{question_id}.{track} contradicting evidence must be non-neutral"
                )
        used_ids.extend(ids)
    if len(used_ids) != len(set(used_ids)):
        raise TrainingError(f"{question_id}.{track} support and counterevidence must be disjoint")
    _texts(seal["alternative_explanations"], f"{question_id}.{track}.alternative_explanations", allow_empty=False)
    _texts(seal["unresolved_links"], f"{question_id}.{track}.unresolved_links")
    if track == "BAZI" and "dynamic_relation_scope" in seal:
        _validate_bazi_dynamic_relation_scope(
            seal["dynamic_relation_scope"],
            question_id,
        )
    _text(seal["capability_ceiling"], f"{question_id}.{track}.capability_ceiling")
    _confidence(seal["confidence"], f"{question_id}.{track}.confidence")
    return seal


def _validate_arbitration(value: Any, question_id: str) -> dict[str, Any]:
    result = _object(
        value,
        {
            "agreement_layers",
            "conflict_layers",
            "conflict_origin",
            "shared_reality_assumption_risk",
            "stronger_track_for_topic",
            "decision",
            "confidence_reduction_required",
        },
        f"{question_id}.cross_track_arbitration",
    )
    _texts(result["agreement_layers"], f"{question_id}.agreement_layers")
    _texts(result["conflict_layers"], f"{question_id}.conflict_layers")
    for field in ("conflict_origin", "shared_reality_assumption_risk", "decision"):
        _text(result[field], f"{question_id}.{field}")
    if result["stronger_track_for_topic"] not in {"ZIWEI", "BAZI", "EQUAL", "UNRESOLVED"}:
        raise TrainingError(f"{question_id}.stronger_track_for_topic is invalid")
    if not isinstance(result["confidence_reduction_required"], bool):
        raise TrainingError(f"{question_id}.confidence_reduction_required must be boolean")
    return result


def _validate_matrix(
    value: Any,
    *,
    option_ids: list[str],
    evidence_by_id: dict[str, dict[str, Any]],
    final_ranking: list[str],
    question_id: str,
) -> dict[str, Any]:
    matrix = _object(value, {"options", "pairwise"}, f"{question_id}.option_comparison_matrix")
    rows = matrix["options"]
    if not isinstance(rows, dict) or set(rows) != set(option_ids):
        raise TrainingError(f"{question_id}.option_comparison_matrix must cover all options")
    observed_ranks: dict[int, str] = {}
    for option_id, raw in rows.items():
        row = _object(
            raw,
            {
                "required_atom_completion",
                "distinctive_atom_completion",
                "severe_atoms_have_independent_evidence",
                "ziwei_support_evidence_ids",
                "bazi_support_evidence_ids",
                "reality_closure",
                "timing_closure",
                "direct_counterevidence_ids",
                "unknown_atoms",
                "shared_background_zeroed",
                "final_rank",
                "final_rank_reason",
            },
            f"{question_id}.option_matrix.{option_id}",
        )
        for field in ("required_atom_completion", "distinctive_atom_completion", "unknown_atoms"):
            _texts(row[field], f"{question_id}.{option_id}.{field}")
        if not isinstance(row["severe_atoms_have_independent_evidence"], bool):
            raise TrainingError(f"{question_id}.{option_id}.severe_atoms evidence flag must be boolean")
        for field, track in (
            ("ziwei_support_evidence_ids", "ZIWEI"),
            ("bazi_support_evidence_ids", "BAZI"),
        ):
            for evidence_id in _texts(row[field], f"{question_id}.{option_id}.{field}"):
                if evidence_id not in evidence_by_id or evidence_by_id[evidence_id]["track"] != track:
                    raise TrainingError(f"{question_id}.{option_id}.{field} references invalid evidence")
        for evidence_id in _texts(row["direct_counterevidence_ids"], f"{question_id}.{option_id}.counterevidence"):
            evidence = evidence_by_id.get(evidence_id)
            if evidence is None:
                raise TrainingError(f"{question_id}.{option_id} references unknown counterevidence")
            if (
                evidence["decision_impact"] == "NEUTRAL"
                or evidence["independence_status"] == "NEUTRAL_BACKGROUND"
            ):
                raise TrainingError(
                    f"{question_id}.{option_id} direct counterevidence must be non-neutral"
                )
        for field in ("reality_closure", "timing_closure", "final_rank_reason"):
            _text(row[field], f"{question_id}.{option_id}.{field}")
        if not isinstance(row["shared_background_zeroed"], bool):
            raise TrainingError(f"{question_id}.{option_id}.shared_background_zeroed must be boolean")
        rank = row["final_rank"]
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1 or rank > len(option_ids) or rank in observed_ranks:
            raise TrainingError(f"{question_id}.{option_id}.final_rank is invalid")
        observed_ranks[rank] = option_id
    if [observed_ranks[index] for index in range(1, len(option_ids) + 1)] != final_ranking:
        raise TrainingError(f"{question_id} matrix ranks do not match final ranking")

    pairs = matrix["pairwise"]
    expected_pairs = {
        tuple(sorted((left, right)))
        for index, left in enumerate(option_ids)
        for right in option_ids[index + 1 :]
    }
    observed_pairs: set[tuple[str, str]] = set()
    if not isinstance(pairs, list):
        raise TrainingError(f"{question_id}.pairwise must be a list")
    for raw in pairs:
        pair = _object(raw, {"left", "right", "winner", "reason"}, f"{question_id}.pairwise")
        left, right = pair["left"], pair["right"]
        key = tuple(sorted((left, right)))
        if key not in expected_pairs or key in observed_pairs or pair["winner"] not in {left, right}:
            raise TrainingError(f"{question_id} has invalid or duplicate pairwise comparison")
        _text(pair["reason"], f"{question_id}.pairwise.reason")
        observed_pairs.add(key)
    if observed_pairs != expected_pairs:
        raise TrainingError(f"{question_id} must compare every option pair")
    return matrix


def _validate_adversarial(
    value: Any,
    *,
    option_ids: list[str],
    evidence_by_id: dict[str, dict[str, Any]],
    top1: str,
    top2: str,
    question_id: str,
) -> dict[str, Any]:
    review = _object(
        value,
        {
            "top1_weakest_required_atom",
            "strongest_competitor",
            "strongest_reversal_evidence_ids",
            "ignored_alternative_explanations",
            "option_wording_inducement",
            "annual_signal_overweighting",
            "bazi_posthoc_agreement",
            "duplicate_evidence_stacking",
            "background_as_endpoint",
            "participation_as_action",
            "valence_as_mechanism",
            "known_rule_execution_omissions",
            "precision_beyond_capability",
            "reversal_test",
        },
        f"{question_id}.adversarial_review",
    )
    _text(review["top1_weakest_required_atom"], f"{question_id}.top1_weakest_required_atom")
    if review["strongest_competitor"] != top2:
        raise TrainingError(f"{question_id}.strongest_competitor must equal Top2")
    reversal_ids = _texts(
        review["strongest_reversal_evidence_ids"],
        f"{question_id}.strongest_reversal_evidence_ids",
        allow_empty=False,
    )
    if any(evidence_id not in evidence_by_id for evidence_id in reversal_ids):
        raise TrainingError(f"{question_id} reversal evidence is unknown")
    _texts(review["ignored_alternative_explanations"], f"{question_id}.ignored_alternatives", allow_empty=False)
    for field in (
        "option_wording_inducement",
        "annual_signal_overweighting",
        "bazi_posthoc_agreement",
        "duplicate_evidence_stacking",
        "background_as_endpoint",
        "participation_as_action",
        "valence_as_mechanism",
        "known_rule_execution_omissions",
        "precision_beyond_capability",
    ):
        _text(review[field], f"{question_id}.adversarial_review.{field}")
    test = _object(
        review["reversal_test"],
        {
            "removed_evidence_ids",
            "ranking_before",
            "ranking_after_removal",
            "top2_best_explanation",
            "top1_survives",
            "reason",
        },
        f"{question_id}.reversal_test",
    )
    removed = _texts(test["removed_evidence_ids"], f"{question_id}.removed_evidence_ids", allow_empty=False)
    if any(evidence_id not in evidence_by_id for evidence_id in removed):
        raise TrainingError(f"{question_id} reversal test removes unknown evidence")
    before = _ranking(test["ranking_before"], option_ids, f"{question_id}.ranking_before")
    _ranking(test["ranking_after_removal"], option_ids, f"{question_id}.ranking_after_removal")
    if before[0] != top1:
        raise TrainingError(f"{question_id} reversal test does not start from Top1")
    _text(test["top2_best_explanation"], f"{question_id}.top2_best_explanation")
    if not isinstance(test["top1_survives"], bool):
        raise TrainingError(f"{question_id}.top1_survives must be boolean")
    _text(test["reason"], f"{question_id}.reversal_test.reason")
    return review


def _validate_confidence(value: Any, question_id: str) -> dict[str, int]:
    components = _object(value, set(CONFIDENCE_COMPONENTS), f"{question_id}.confidence_components")
    normalized = {
        field: _confidence(components[field], f"{question_id}.confidence_components.{field}")
        for field in CONFIDENCE_COMPONENTS
    }
    critical = [normalized[field] for field in CONFIDENCE_COMPONENTS[:-1]]
    if normalized["overall_confidence"] > min(critical):
        raise TrainingError(f"{question_id} overall confidence exceeds its weakest component")
    return normalized


def _validate_counterfactuals(
    value: Any,
    *,
    option_ids: list[str],
    decisive_rule_ids: list[str],
    question_id: str,
) -> dict[str, Any]:
    analysis = _object(
        value,
        {
            "full_model_ranking",
            "canonical_only_ranking",
            "ziwei_only_ranking",
            "bazi_only_ranking",
            "fused_ranking",
            "decisive_rule_ablations",
        },
        f"{question_id}.counterfactual_analysis",
    )
    for field in (
        "full_model_ranking",
        "canonical_only_ranking",
        "ziwei_only_ranking",
        "bazi_only_ranking",
        "fused_ranking",
    ):
        _ranking(analysis[field], option_ids, f"{question_id}.{field}")
    rows = analysis["decisive_rule_ablations"]
    if not isinstance(rows, list):
        raise TrainingError(f"{question_id}.decisive_rule_ablations must be a list")
    seen: set[str] = set()
    for raw in rows:
        row = _object(
            raw,
            {"rule_id", "ranking_without_rule", "changes_top1", "reason"},
            f"{question_id}.rule_ablation",
        )
        if row["rule_id"] not in decisive_rule_ids or row["rule_id"] in seen:
            raise TrainingError(f"{question_id} has invalid decisive rule ablation")
        ranking = _ranking(row["ranking_without_rule"], option_ids, f"{question_id}.ranking_without_rule")
        if row["changes_top1"] is not True or ranking[0] == analysis["full_model_ranking"][0]:
            raise TrainingError(f"{question_id} decisive rule must change Top1 when removed")
        _text(row["reason"], f"{question_id}.rule_ablation.reason")
        seen.add(row["rule_id"])
    if seen != set(decisive_rule_ids):
        raise TrainingError(f"{question_id} must ablate every decisive rule")
    return analysis


def validate_prediction_reasoning(
    *,
    case: dict[str, Any],
    payload: dict[str, Any],
    predictions: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if payload.get("schema") != PREDICTION_SCHEMA:
        raise TrainingError(f"prediction schema must be {PREDICTION_SCHEMA}")
    blind = validate_blind_chart_model(case, payload.get("blind_chart_model"))
    consistency = _object(
        payload.get("cross_question_consistency"),
        {"checks", "unresolved_conflicts"},
        "cross_question_consistency",
    )
    question_ids = [row["question_id"] for row in predictions]
    checks = consistency["checks"]
    if not isinstance(checks, list) or {row.get("question_id") for row in checks if isinstance(row, dict)} != set(question_ids):
        raise TrainingError("cross_question_consistency must check every question")
    for raw in checks:
        row = _object(raw, {"question_id", "consistent", "conflicts", "resolution"}, "cross_question_consistency.check")
        if not isinstance(row["consistent"], bool):
            raise TrainingError("cross-question consistency flag must be boolean")
        _texts(row["conflicts"], "cross_question_consistency.conflicts")
        _text(row["resolution"], "cross_question_consistency.resolution")
        if not row["consistent"] and not row["conflicts"]:
            raise TrainingError("an inconsistent question must disclose conflicts")
    _texts(consistency["unresolved_conflicts"], "cross_question_consistency.unresolved_conflicts")
    _walk_forbidden(payload)
    return blind, consistency


def validate_question_reasoning(
    *,
    row: dict[str, Any],
    option_ids: list[str],
    source_routes: list[str],
    top1: str,
    top2: str,
    decisive_rule_ids: list[str],
) -> dict[str, Any]:
    question_id = row["question_id"]
    semantics = _validate_semantics(row.get("question_semantic_model"), option_ids, question_id)
    profile = row.get("question_profile")
    allow_timing_only = (
        semantics["is_composite_narrative"] is False
        and (
            (
                isinstance(profile, dict)
                and profile.get("time_scope_tags") == ["SPECIFIC_YEAR"]
            )
            or _is_pure_time_window_comparison(semantics)
        )
    )
    evidence, evidence_by_id = _validate_evidence(
        row.get("evidence_ledger"),
        option_ids=option_ids,
        source_routes=source_routes,
        question_id=question_id,
        allow_timing_only=allow_timing_only,
    )
    ziwei = _validate_track(
        row.get("ziwei_track_seal"),
        track="ZIWEI",
        option_ids=option_ids,
        evidence_by_id=evidence_by_id,
        question_id=question_id,
    )
    bazi = _validate_track(
        row.get("bazi_track_seal"),
        track="BAZI",
        option_ids=option_ids,
        evidence_by_id=evidence_by_id,
        question_id=question_id,
    )
    arbitration = _validate_arbitration(row.get("cross_track_arbitration"), question_id)
    final_ranking = _ranking(row.get("final_ranking"), option_ids, f"{question_id}.final_ranking")
    if final_ranking[:2] != [top1, top2]:
        raise TrainingError(f"{question_id}.final_ranking does not match Top1/Top2")
    matrix = _validate_matrix(
        row.get("option_comparison_matrix"),
        option_ids=option_ids,
        evidence_by_id=evidence_by_id,
        final_ranking=final_ranking,
        question_id=question_id,
    )
    top1_atoms = semantics["option_atoms"][top1]
    severe_atoms = top1_atoms["severe_irreversible_or_high_precision_atoms"]
    if severe_atoms:
        option_row = matrix["options"][top1]
        required_refs = {
            " ".join(f"{top1}:{atom}".split()).casefold()
            for atom in severe_atoms
        }
        supported_refs = {
            " ".join(atom_ref.split()).casefold()
            for evidence_row in evidence
            if evidence_row["independence_status"] == "INDEPENDENT"
            for atom_ref in evidence_row["supports_option_atoms"]
        }
        if (
            not option_row["severe_atoms_have_independent_evidence"]
            or not required_refs.issubset(supported_refs)
        ):
            raise TrainingError(
                f"{question_id}.{top1} each high-precision Top1 atom needs "
                "an exact independent evidence binding"
            )
    adversarial = _validate_adversarial(
        row.get("adversarial_review"),
        option_ids=option_ids,
        evidence_by_id=evidence_by_id,
        top1=top1,
        top2=top2,
        question_id=question_id,
    )
    confidence = _validate_confidence(row.get("confidence_components"), question_id)
    counterfactuals = _validate_counterfactuals(
        row.get("counterfactual_analysis"),
        option_ids=option_ids,
        decisive_rule_ids=decisive_rule_ids,
        question_id=question_id,
    )
    return {
        "question_semantic_model": semantics,
        "ziwei_track_seal": ziwei,
        "bazi_track_seal": bazi,
        "cross_track_arbitration": arbitration,
        "evidence_ledger": evidence,
        "final_ranking": final_ranking,
        "option_comparison_matrix": matrix,
        "adversarial_review": adversarial,
        "confidence_components": confidence,
        "counterfactual_analysis": counterfactuals,
    }


def validate_replay_remediation(value: Any, *, required: bool) -> dict[str, Any] | None:
    if value is None and not required:
        return None
    report = _object(
        value,
        {
            "original_root_causes",
            "remediation_type",
            "new_idea_executed",
            "changed_steps",
            "predicted_mechanism_of_improvement",
            "new_error_risks",
        },
        "replay_remediation",
    )
    roots = _texts(report["original_root_causes"], "replay_remediation.original_root_causes", allow_empty=False)
    if not set(roots).issubset(ROOT_CAUSES):
        raise TrainingError("replay_remediation contains an invalid root cause")
    if report["remediation_type"] not in REMEDIATION_TYPES:
        raise TrainingError("replay_remediation has an invalid remediation type")
    for field in ("new_idea_executed", "predicted_mechanism_of_improvement"):
        _text(report[field], f"replay_remediation.{field}")
    _texts(report["changed_steps"], "replay_remediation.changed_steps", allow_empty=False)
    _texts(report["new_error_risks"], "replay_remediation.new_error_risks")
    return report


def build_completeness_report(
    blind_chart_model: dict[str, Any],
    predictions: list[dict[str, Any]],
    consistency: dict[str, Any],
) -> dict[str, Any]:
    evidence_rows = [
        evidence
        for prediction in predictions
        for evidence in prediction["evidence_ledger"]
    ]
    families = {row["evidence_family_id"] for row in evidence_rows}
    decision_evidence = [
        row for row in evidence_rows if row["decision_impact"] != "NEUTRAL"
    ]
    return {
        "schema": "REASONING-COMPLETENESS-REPORT-V1",
        "blind_chart_model_sha256": object_sha256(blind_chart_model),
        "blind_chart_model_complete": True,
        "ziwei_track_seals_complete": True,
        "bazi_track_seals_complete": True,
        "cross_track_conflicts_preserved": all(
            isinstance(row["cross_track_arbitration"]["conflict_layers"], list)
            for row in predictions
        ),
        "valid_evidence_entries": len(evidence_rows),
        "decision_impact_evidence_entries": len(decision_evidence),
        "independent_evidence_families": len(families),
        "source_only_invalid_evidence_entries": 0,
        "all_option_comparisons_complete": True,
        "reversal_tests_complete": True,
        "decisive_rules_with_real_top1_change": sum(
            len(row["counterfactual_analysis"]["decisive_rule_ablations"])
            for row in predictions
        ),
        "high_confidence_with_unclosed_critical_link": sum(
            1
            for row in predictions
            if row["confidence_components"]["overall_confidence"] >= 75
            and (
                row["ziwei_track_seal"]["unresolved_links"]
                or row["bazi_track_seal"]["unresolved_links"]
            )
        ),
        "cross_question_unresolved_conflicts": len(consistency["unresolved_conflicts"]),
        "reasoning_framework": {
            "dimensions": ["STRUCTURE", "MECHANISM", "TIMING", "REALITY", "ADVERSARIAL", "REFLECTION"],
            "status": "WORKING_HYPOTHESIS_NOT_FIXED_DOGMA",
            "evidence_quota": None,
        },
        "evidence_family_sizes": dict(
            sorted(Counter(row["evidence_family_id"] for row in evidence_rows).items())
        ),
    }


def frozen_content_hash(frozen: dict[str, Any]) -> str:
    if frozen.get("schema") == "FROZEN-PREDICTION-V1":
        return object_sha256(frozen["predictions"])
    return object_sha256(
        {
            "blind_chart_model": frozen["blind_chart_model"],
            "cross_question_consistency": frozen["cross_question_consistency"],
            "replay_remediation": frozen.get("replay_remediation"),
            "predictions": frozen["predictions"],
        }
    )

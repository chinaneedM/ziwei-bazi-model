from __future__ import annotations

import copy
import json
import re
from collections import Counter
from typing import Any

from .bazi_facts import (
    EARTHLY_BRANCHES,
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
    "branch_id",
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

ZIWEI_NAMESPACE_TYPES = {
    "NATAL",
    "ZIWEI_MAJOR_PERIOD",
    "YEAR",
    "SUBJECT_TAIJI",
}
UPSTREAM_FACT_TYPES = {
    "ZIWEI_COORDINATE",
    "ZIWEI_TRANSFORMATION",
    "BAZI_ATOMIC",
    "PERIOD_OBJECT",
    "EXTERNAL_FACT",
}


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


def _bazi_atomic_source_ids(ledger: dict[str, Any]) -> set[str]:
    ids = set(ledger["five_elements"])
    ids.update(f"{position}_PILLAR" for position in ledger["four_pillars"])
    ids.update(
        root
        for roots in ledger["visible_stem_roots"].values()
        for root in roots
    )
    ids.update(ledger["heavenly_stem_combinations"])
    ids.update(ledger["earthly_branch_relations"])
    return ids


def _validate_ziwei_coordinate_truth_table(
    value: Any,
    *,
    label: str,
) -> dict[str, set[str]]:
    table = _object(
        value,
        {
            "schema",
            "required_namespace_ids",
            "namespaces",
            "transformations",
            "verification_status",
        },
        label,
    )
    if table["schema"] != "ZIWEI-COORDINATE-TRUTH-TABLE-V1":
        raise TrainingError(f"{label} has the wrong schema")
    required_namespace_ids = _texts(
        table["required_namespace_ids"],
        f"{label}.required_namespace_ids",
        allow_empty=False,
    )
    namespaces = table["namespaces"]
    if not isinstance(namespaces, list) or not namespaces:
        raise TrainingError(f"{label}.namespaces must be non-empty")
    namespace_ids: set[str] = set()
    namespace_types: set[str] = set()
    coordinate_ids: set[str] = set()
    for raw_namespace in namespaces:
        namespace = _object(
            raw_namespace,
            {"namespace_id", "namespace_type", "coordinates"},
            f"{label}.namespace",
        )
        namespace_id = _text(namespace["namespace_id"], f"{label}.namespace_id")
        if namespace_id in namespace_ids:
            raise TrainingError(f"{label} has duplicate namespace_id: {namespace_id}")
        namespace_ids.add(namespace_id)
        namespace_type = namespace["namespace_type"]
        if namespace_type not in ZIWEI_NAMESPACE_TYPES:
            raise TrainingError(f"{label}.{namespace_id} has invalid namespace_type")
        namespace_types.add(namespace_type)
        coordinates = namespace["coordinates"]
        if not isinstance(coordinates, list) or len(coordinates) != 12:
            raise TrainingError(f"{label}.{namespace_id} must contain exactly twelve coordinates")
        palace_names: set[str] = set()
        earthly_branches: set[str] = set()
        local_coordinate_ids: set[str] = set()
        for raw_coordinate in coordinates:
            if not isinstance(raw_coordinate, list) or len(raw_coordinate) != 3:
                raise TrainingError(
                    f"{label}.{namespace_id}.coordinate must be [id, palace, branch]"
                )
            coordinate_id, palace_name, earthly_branch = raw_coordinate
            coordinate_id = _text(
                coordinate_id,
                f"{label}.{namespace_id}.coordinate_id",
            )
            palace_name = _text(
                palace_name,
                f"{label}.{namespace_id}.palace_name",
            )
            if earthly_branch not in EARTHLY_BRANCHES:
                raise TrainingError(
                    f"{label}.{namespace_id} has invalid earthly_branch"
                )
            if (
                coordinate_id in coordinate_ids
                or coordinate_id in local_coordinate_ids
                or palace_name in palace_names
                or earthly_branch in earthly_branches
            ):
                raise TrainingError(
                    f"{label}.{namespace_id} has duplicate coordinate, palace, or branch"
                )
            local_coordinate_ids.add(coordinate_id)
            palace_names.add(palace_name)
            earthly_branches.add(earthly_branch)
        if earthly_branches != set(EARTHLY_BRANCHES):
            raise TrainingError(
                f"{label}.{namespace_id} does not cover all twelve earthly branches"
            )
        coordinate_ids.update(local_coordinate_ids)
    if namespace_ids != set(required_namespace_ids):
        raise TrainingError(f"{label} required namespaces do not match materialized namespaces")
    if not {"NATAL", "ZIWEI_MAJOR_PERIOD", "YEAR"}.issubset(namespace_types):
        raise TrainingError(
            f"{label} must include natal, Ziwei-major-period, and year namespaces"
        )

    transformations = table["transformations"]
    if not isinstance(transformations, list):
        raise TrainingError(f"{label}.transformations must be a list")
    transformation_ids: set[str] = set()
    for raw_transformation in transformations:
        transformation = _object(
            raw_transformation,
            {
                "fact_id",
                "origin_layer",
                "heavenly_stem",
                "transformed_star",
                "destination_coordinate_id",
                "verification_status",
            },
            f"{label}.transformation",
        )
        fact_id = _text(transformation["fact_id"], f"{label}.transformation.fact_id")
        if fact_id in transformation_ids:
            raise TrainingError(f"{label} has duplicate transformation fact_id")
        transformation_ids.add(fact_id)
        for field in ("origin_layer", "heavenly_stem", "transformed_star"):
            _text(transformation[field], f"{label}.transformation.{field}")
        if transformation["destination_coordinate_id"] not in coordinate_ids:
            raise TrainingError(f"{label} transformation has an unknown destination")
        if transformation["verification_status"] != "VERIFIED":
            raise TrainingError(f"{label} transformation provenance was not verified")
    if table["verification_status"] != "VERIFIED":
        raise TrainingError(f"{label} coordinate truth table was not verified")
    return {
        "ZIWEI_COORDINATE": coordinate_ids,
        "ZIWEI_TRANSFORMATION": transformation_ids,
    }


def _validate_chart_branch_model(value: Any) -> dict[str, Any]:
    model = _object(
        value,
        {
            "schema",
            "boundary_status",
            "boundary_kinds",
            "branches",
            "calibration",
        },
        "blind_chart_model.chart_branch_model",
    )
    if model["schema"] != "TIME-BOUNDARY-CHART-BRANCHES-V1":
        raise TrainingError("chart_branch_model has the wrong schema")
    boundary_status = model["boundary_status"]
    if boundary_status not in {"UNAMBIGUOUS", "MULTIPLE_LEGAL_CANDIDATES"}:
        raise TrainingError("chart_branch_model has an invalid boundary_status")
    boundary_kinds = _texts(
        model["boundary_kinds"],
        "chart_branch_model.boundary_kinds",
        allow_empty=False,
    )
    branches = model["branches"]
    if not isinstance(branches, dict) or not branches:
        raise TrainingError("chart_branch_model.branches must be non-empty")
    if boundary_status == "UNAMBIGUOUS" and len(branches) != 1:
        raise TrainingError("an unambiguous input must have exactly one chart branch")
    if boundary_status == "MULTIPLE_LEGAL_CANDIDATES" and len(branches) < 2:
        raise TrainingError("a boundary ambiguity must preserve at least two legal branches")
    if boundary_status == "UNAMBIGUOUS" and boundary_kinds != ["NONE"]:
        raise TrainingError("an unambiguous input must declare boundary_kinds as NONE")
    if boundary_status == "MULTIPLE_LEGAL_CANDIDATES" and "NONE" in boundary_kinds:
        raise TrainingError("ambiguous time branches may not use the NONE boundary kind")

    branch_sources: dict[str, dict[str, set[str]]] = {}
    for branch_id, raw_branch in branches.items():
        _text(branch_id, "chart_branch_model.branch_id")
        branch = _object(
            raw_branch,
            {
                "derivation_basis",
                "option_blind_frozen",
                "ziwei_coordinate_truth_table",
                "bazi_atomic_fact_ledger",
                "bazi_strength_structure_favorability_chain",
                "period_objects",
                "verification_status",
            },
            f"chart_branch_model.branches.{branch_id}",
        )
        _text(branch["derivation_basis"], f"chart_branch_model.{branch_id}.derivation_basis")
        if branch["option_blind_frozen"] is not True:
            raise TrainingError(f"{branch_id} must be frozen before option ranking")
        sources = _validate_ziwei_coordinate_truth_table(
            branch["ziwei_coordinate_truth_table"],
            label=f"chart_branch_model.{branch_id}.ziwei_coordinate_truth_table",
        )
        ledger = validate_bazi_atomic_fact_ledger(branch["bazi_atomic_fact_ledger"])
        validate_bazi_strength_chain(
            ledger,
            branch["bazi_strength_structure_favorability_chain"],
        )
        sources["BAZI_ATOMIC"] = _bazi_atomic_source_ids(ledger)
        period_objects = branch["period_objects"]
        if not isinstance(period_objects, list) or not period_objects:
            raise TrainingError(f"{branch_id} must materialize period objects")
        period_ids: set[str] = set()
        period_namespaces: set[str] = set()
        for raw_period in period_objects:
            period = _object(
                raw_period,
                {
                    "fact_id",
                    "namespace",
                    "start_marker",
                    "end_marker",
                    "query_membership_verified",
                    "recomputation_status",
                },
                f"chart_branch_model.{branch_id}.period_object",
            )
            fact_id = _text(period["fact_id"], f"{branch_id}.period_object.fact_id")
            if fact_id in period_ids:
                raise TrainingError(f"{branch_id} has duplicate period fact_id")
            period_ids.add(fact_id)
            if period["namespace"] not in {
                "ZIWEI_MAJOR_PERIOD",
                "BAZI_LUCK_CYCLE",
                "YEAR",
                "MONTH",
            }:
                raise TrainingError(f"{branch_id} has an invalid period namespace")
            period_namespaces.add(period["namespace"])
            _text(period["start_marker"], f"{branch_id}.period_object.start_marker")
            _text(period["end_marker"], f"{branch_id}.period_object.end_marker")
            if period["query_membership_verified"] is not True:
                raise TrainingError(f"{branch_id} period membership is unverified")
            if period["recomputation_status"] != "VERIFIED":
                raise TrainingError(f"{branch_id} period object failed recomputation")
        if not {"ZIWEI_MAJOR_PERIOD", "BAZI_LUCK_CYCLE"}.issubset(period_namespaces):
            raise TrainingError(
                f"{branch_id} must keep Ziwei major periods and Bazi luck cycles separate"
            )
        sources["PERIOD_OBJECT"] = period_ids
        sources["EXTERNAL_FACT"] = set()
        if branch["verification_status"] != "VERIFIED":
            raise TrainingError(f"{branch_id} branch verification failed")
        branch_sources[branch_id] = sources

    calibration = _object(
        model["calibration"],
        {
            "status",
            "selected_branch_id",
            "independent_external_fact_ids",
            "option_atoms_used",
            "rationale",
        },
        "chart_branch_model.calibration",
    )
    external_fact_ids = _texts(
        calibration["independent_external_fact_ids"],
        "chart_branch_model.calibration.independent_external_fact_ids",
    )
    if calibration["option_atoms_used"] is not False:
        raise TrainingError("option atoms may not participate in time calibration")
    _text(calibration["rationale"], "chart_branch_model.calibration.rationale")
    if boundary_status == "UNAMBIGUOUS":
        only_branch = next(iter(branches))
        if (
            calibration["status"] != "NOT_REQUIRED"
            or calibration["selected_branch_id"] != only_branch
            or external_fact_ids
        ):
            raise TrainingError("unambiguous input has an invalid calibration record")
    elif calibration["status"] == "UNRESOLVED":
        if calibration["selected_branch_id"] is not None:
            raise TrainingError("an unresolved boundary may not select a chart branch")
    elif calibration["status"] == "RESOLVED_BY_EXTERNAL_FACT":
        if (
            calibration["selected_branch_id"] not in branches
            or not external_fact_ids
        ):
            raise TrainingError(
                "resolved time calibration needs a selected branch and independent external facts"
            )
    else:
        raise TrainingError("ambiguous input has an invalid calibration status")
    for sources in branch_sources.values():
        sources["EXTERNAL_FACT"].update(external_fact_ids)
    return {
        "model": model,
        "branch_ids": list(branches),
        "branch_sources": branch_sources,
        "boundary_status": boundary_status,
        "calibration": calibration,
    }


def validate_blind_chart_model(case: dict[str, Any], value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TrainingError("blind_chart_model must be an object")
    schema = value.get("schema")
    model_fields = {
        "schema",
        "input_reliability",
        "ziwei_static_model",
        "bazi_static_model",
        "shared_life_structure",
    }
    if schema == "BLIND-CHART-MODEL-V3":
        model_fields.add("chart_branch_model")
    model = _object(
        value,
        model_fields,
        "blind_chart_model",
    )
    if model["schema"] not in {
        "BLIND-CHART-MODEL-V1",
        "BLIND-CHART-MODEL-V2",
        "BLIND-CHART-MODEL-V3",
    }:
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
    if model["schema"] == "BLIND-CHART-MODEL-V3":
        _validate_chart_branch_model(model["chart_branch_model"])
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
        required_atoms = _texts(
            atom_model["required_atoms"],
            f"{question_id}.{option_id}.required_atoms",
            allow_empty=False,
        )
        distinctive_atoms = _texts(
            atom_model["distinctive_atoms"],
            f"{question_id}.{option_id}.distinctive_atoms",
            allow_empty=False,
        )
        severe_atoms = _texts(
            atom_model["severe_irreversible_or_high_precision_atoms"],
            f"{question_id}.{option_id}.severe_atoms",
        )
        if not set(distinctive_atoms).issubset(required_atoms):
            raise TrainingError(
                f"{question_id}.{option_id} distinctive atoms must be required atoms"
            )
        if not set(severe_atoms).issubset(required_atoms):
            raise TrainingError(
                f"{question_id}.{option_id} severe atoms must be required atoms"
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


def _validate_upstream_fact_dependencies(
    value: Any,
    *,
    evidence_rows: Any,
    branch_context: dict[str, Any],
    question_id: str,
) -> tuple[dict[str, Any], set[str]]:
    graph = _object(
        value,
        {
            "facts",
            "evidence_dependencies",
            "invalidated_evidence_ids",
            "ranking_recomputed_after_invalidation",
        },
        f"{question_id}.upstream_fact_dependencies",
    )
    if not isinstance(evidence_rows, list) or not evidence_rows:
        raise TrainingError(f"{question_id}.evidence_ledger must be non-empty")
    evidence_by_id = {
        row.get("evidence_id"): row
        for row in evidence_rows
        if isinstance(row, dict) and isinstance(row.get("evidence_id"), str)
    }
    if len(evidence_by_id) != len(evidence_rows):
        raise TrainingError(f"{question_id} has invalid or duplicate evidence identifiers")

    facts = graph["facts"]
    if not isinstance(facts, list) or not facts:
        raise TrainingError(f"{question_id}.upstream facts must be non-empty")
    fact_by_id: dict[str, dict[str, Any]] = {}
    for raw_fact in facts:
        fact = _object(
            raw_fact,
            {
                "fact_id",
                "branch_id",
                "fact_type",
                "source_object_id",
                "recomputation_status",
            },
            f"{question_id}.upstream_fact",
        )
        fact_id = _text(fact["fact_id"], f"{question_id}.upstream_fact.fact_id")
        if fact_id in fact_by_id:
            raise TrainingError(f"{question_id} has duplicate upstream fact_id")
        branch_id = fact["branch_id"]
        if branch_id not in branch_context["branch_ids"]:
            raise TrainingError(f"{question_id}.{fact_id} has an unknown branch_id")
        fact_type = fact["fact_type"]
        if fact_type not in UPSTREAM_FACT_TYPES:
            raise TrainingError(f"{question_id}.{fact_id} has an invalid fact_type")
        source_object_id = _text(
            fact["source_object_id"],
            f"{question_id}.{fact_id}.source_object_id",
        )
        allowed_sources = branch_context["branch_sources"][branch_id][fact_type]
        if fact_type != "EXTERNAL_FACT" and source_object_id not in allowed_sources:
            raise TrainingError(
                f"{question_id}.{fact_id} does not resolve to the declared branch source"
            )
        if fact_type == "EXTERNAL_FACT" and allowed_sources and source_object_id not in allowed_sources:
            raise TrainingError(
                f"{question_id}.{fact_id} is not an independent calibration fact"
            )
        if fact["recomputation_status"] not in {"VERIFIED", "FAILED"}:
            raise TrainingError(f"{question_id}.{fact_id} has invalid recomputation_status")
        fact_by_id[fact_id] = fact

    dependencies = graph["evidence_dependencies"]
    if not isinstance(dependencies, list):
        raise TrainingError(f"{question_id}.evidence_dependencies must be a list")
    dependency_by_evidence: dict[str, dict[str, Any]] = {}
    invalidated: set[str] = set()
    for raw_dependency in dependencies:
        dependency = _object(
            raw_dependency,
            {"evidence_id", "branch_id", "upstream_fact_ids", "dependency_signature"},
            f"{question_id}.evidence_dependency",
        )
        evidence_id = dependency["evidence_id"]
        if evidence_id not in evidence_by_id or evidence_id in dependency_by_evidence:
            raise TrainingError(f"{question_id} has an invalid evidence dependency row")
        branch_id = dependency["branch_id"]
        evidence = evidence_by_id[evidence_id]
        if branch_id != evidence.get("branch_id") or branch_id not in branch_context["branch_ids"]:
            raise TrainingError(f"{question_id}.{evidence_id} dependency branch mismatch")
        upstream_fact_ids = _texts(
            dependency["upstream_fact_ids"],
            f"{question_id}.{evidence_id}.upstream_fact_ids",
            allow_empty=False,
        )
        upstream_facts = []
        for fact_id in upstream_fact_ids:
            fact = fact_by_id.get(fact_id)
            if fact is None or fact["branch_id"] != branch_id:
                raise TrainingError(
                    f"{question_id}.{evidence_id} depends on an unknown or cross-branch fact"
                )
            upstream_facts.append(fact)
        fact_types = {fact["fact_type"] for fact in upstream_facts}
        if evidence.get("track") == "ZIWEI" and not fact_types.intersection(
            {"ZIWEI_COORDINATE", "ZIWEI_TRANSFORMATION"}
        ):
            raise TrainingError(f"{question_id}.{evidence_id} lacks a Ziwei coordinate dependency")
        if evidence.get("track") == "BAZI" and "BAZI_ATOMIC" not in fact_types:
            raise TrainingError(f"{question_id}.{evidence_id} lacks a Bazi atomic dependency")
        if evidence.get("layer") in {"PERIOD", "YEAR", "MONTH"} and "PERIOD_OBJECT" not in fact_types:
            raise TrainingError(f"{question_id}.{evidence_id} lacks a period-object dependency")
        expected_signature = object_sha256(
            {
                "branch_id": branch_id,
                "upstream_fact_ids": sorted(upstream_fact_ids),
            }
        )
        if dependency["dependency_signature"] != expected_signature:
            raise TrainingError(
                f"{question_id}.{evidence_id} dependency signature mismatch"
            )
        if any(fact["recomputation_status"] == "FAILED" for fact in upstream_facts):
            invalidated.add(evidence_id)
        dependency_by_evidence[evidence_id] = dependency
    if set(dependency_by_evidence) != set(evidence_by_id):
        raise TrainingError(f"{question_id} must bind every evidence row to upstream facts")
    declared_invalidated = _texts(
        graph["invalidated_evidence_ids"],
        f"{question_id}.invalidated_evidence_ids",
    )
    if set(declared_invalidated) != invalidated:
        raise TrainingError(
            f"{question_id} invalidated evidence does not match failed upstream dependencies"
        )
    if invalidated and graph["ranking_recomputed_after_invalidation"] is not True:
        raise TrainingError(
            f"{question_id} must recompute ranking after upstream dependency failure"
        )
    if not isinstance(graph["ranking_recomputed_after_invalidation"], bool):
        raise TrainingError(
            f"{question_id}.ranking_recomputed_after_invalidation must be boolean"
        )
    return graph, invalidated


def _validate_evidence(
    value: Any,
    *,
    option_ids: list[str],
    option_atoms: dict[str, dict[str, Any]],
    source_routes: list[str],
    question_id: str,
    branch_ids: set[str],
    invalidated_evidence_ids: set[str],
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
        row = copy.deepcopy(raw)
        evidence_id = _text(row["evidence_id"], f"{question_id}.evidence_id")
        if evidence_id in by_id:
            raise TrainingError(f"{question_id} has duplicate evidence_id: {evidence_id}")
        if row["branch_id"] not in branch_ids:
            raise TrainingError(f"{question_id}.{evidence_id} has an invalid branch_id")
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
            valid_refs = {
                f"{option_id}:{atom}"
                for option_id, atom_model in option_atoms.items()
                for atom in atom_model["required_atoms"]
            }
            if any(ref not in valid_refs for ref in refs):
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
        if evidence_id in invalidated_evidence_ids:
            row["supports_option_atoms"] = []
            row["contradicts_option_atoms"] = []
            row["independence_status"] = "NEUTRAL_BACKGROUND"
            row["reliability"] = "UNKNOWN"
            row["decision_impact"] = "NEUTRAL"
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
            if field == "supporting_evidence_ids" and (
                evidence["decision_impact"] == "NEUTRAL"
                or evidence["independence_status"] == "NEUTRAL_BACKGROUND"
            ):
                raise TrainingError(
                    f"{question_id}.{track} may not use invalidated or neutral evidence"
                )
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
    option_atoms: dict[str, dict[str, Any]],
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
                "directly_refuted_atoms",
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
        for field in (
            "required_atom_completion",
            "directly_refuted_atoms",
            "distinctive_atom_completion",
            "unknown_atoms",
        ):
            _texts(row[field], f"{question_id}.{option_id}.{field}")
        if not isinstance(row["severe_atoms_have_independent_evidence"], bool):
            raise TrainingError(f"{question_id}.{option_id}.severe_atoms evidence flag must be boolean")
        support_ids: list[str] = []
        for field, track in (
            ("ziwei_support_evidence_ids", "ZIWEI"),
            ("bazi_support_evidence_ids", "BAZI"),
        ):
            for evidence_id in _texts(row[field], f"{question_id}.{option_id}.{field}"):
                if evidence_id not in evidence_by_id or evidence_by_id[evidence_id]["track"] != track:
                    raise TrainingError(f"{question_id}.{option_id}.{field} references invalid evidence")
                evidence = evidence_by_id[evidence_id]
                if (
                    evidence["decision_impact"] == "NEUTRAL"
                    or evidence["independence_status"] == "NEUTRAL_BACKGROUND"
                ):
                    raise TrainingError(
                        f"{question_id}.{option_id}.{field} uses invalidated or neutral evidence"
                    )
                support_ids.append(evidence_id)
        counter_ids = _texts(
            row["direct_counterevidence_ids"],
            f"{question_id}.{option_id}.counterevidence",
        )
        for evidence_id in counter_ids:
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
            if evidence.get("axis_distance") != "DIRECT_SAME_AXIS":
                raise TrainingError(
                    f"{question_id}.{option_id} counterevidence must be direct same-axis evidence"
                )

        required_atoms = set(option_atoms[option_id]["required_atoms"])
        completed_atoms = set(row["required_atom_completion"])
        refuted_atoms = set(row["directly_refuted_atoms"])
        unknown_atoms = set(row["unknown_atoms"])
        if any(
            not atoms.issubset(required_atoms)
            for atoms in (completed_atoms, refuted_atoms, unknown_atoms)
        ):
            raise TrainingError(
                f"{question_id}.{option_id} atom closure references a non-required atom"
            )
        if (
            completed_atoms & refuted_atoms
            or completed_atoms & unknown_atoms
            or refuted_atoms & unknown_atoms
            or completed_atoms | refuted_atoms | unknown_atoms != required_atoms
        ):
            raise TrainingError(
                f"{question_id}.{option_id} required atoms need one complete, disjoint closure partition"
            )
        independently_supported_atoms = {
            ref.split(":", 1)[1]
            for evidence_id in support_ids
            for evidence in [evidence_by_id[evidence_id]]
            if evidence["independence_status"] == "INDEPENDENT"
            for ref in evidence["supports_option_atoms"]
            if ref.startswith(f"{option_id}:")
        }
        directly_contradicted_atoms = {
            ref.split(":", 1)[1]
            for evidence_id in counter_ids
            for ref in evidence_by_id[evidence_id]["contradicts_option_atoms"]
            if ref.startswith(f"{option_id}:")
        }
        if not completed_atoms.issubset(independently_supported_atoms):
            raise TrainingError(
                f"{question_id}.{option_id} completed atoms lack independent evidence"
            )
        if not refuted_atoms.issubset(directly_contradicted_atoms):
            raise TrainingError(
                f"{question_id}.{option_id} refuted atoms lack direct counterevidence"
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


def _validate_branch_analysis(
    value: Any,
    *,
    branch_context: dict[str, Any],
    option_ids: list[str],
    evidence_by_id: dict[str, dict[str, Any]],
    final_ranking: list[str],
    question_id: str,
) -> tuple[dict[str, Any], bool]:
    analysis = _object(
        value,
        {
            "branch_rankings",
            "consensus_status",
            "selected_branch_id",
            "top1_uncertainty_preserved",
        },
        f"{question_id}.branch_analysis",
    )
    rankings = analysis["branch_rankings"]
    branch_ids = branch_context["branch_ids"]
    if not isinstance(rankings, dict) or set(rankings) != set(branch_ids):
        raise TrainingError(f"{question_id}.branch_rankings must cover every chart branch")
    branch_top1: dict[str, str] = {}
    for branch_id, raw_ranking in rankings.items():
        branch_ranking = _object(
            raw_ranking,
            {
                "top1",
                "top2",
                "ranking",
                "supporting_evidence_ids",
                "contradicting_evidence_ids",
                "confidence",
            },
            f"{question_id}.branch_rankings.{branch_id}",
        )
        ranking = _ranking(
            branch_ranking["ranking"],
            option_ids,
            f"{question_id}.branch_rankings.{branch_id}.ranking",
        )
        if ranking[:2] != [branch_ranking["top1"], branch_ranking["top2"]]:
            raise TrainingError(f"{question_id}.{branch_id} branch Top1/Top2 mismatch")
        used_ids: list[str] = []
        for field in ("supporting_evidence_ids", "contradicting_evidence_ids"):
            evidence_ids = _texts(
                branch_ranking[field],
                f"{question_id}.{branch_id}.{field}",
                allow_empty=field == "contradicting_evidence_ids",
            )
            for evidence_id in evidence_ids:
                evidence = evidence_by_id.get(evidence_id)
                if (
                    evidence is None
                    or evidence["branch_id"] != branch_id
                    or evidence["decision_impact"] == "NEUTRAL"
                    or evidence["independence_status"] == "NEUTRAL_BACKGROUND"
                ):
                    raise TrainingError(
                        f"{question_id}.{branch_id} ranking uses cross-branch or invalid evidence"
                    )
            used_ids.extend(evidence_ids)
        if len(used_ids) != len(set(used_ids)):
            raise TrainingError(f"{question_id}.{branch_id} branch evidence must be disjoint")
        supporting_tracks = {
            evidence_by_id[evidence_id]["track"]
            for evidence_id in branch_ranking["supporting_evidence_ids"]
        }
        if not {"ZIWEI", "BAZI"}.issubset(supporting_tracks):
            raise TrainingError(
                f"{question_id}.{branch_id} needs independent Ziwei and Bazi branch evidence"
            )
        _confidence(
            branch_ranking["confidence"],
            f"{question_id}.branch_rankings.{branch_id}.confidence",
        )
        branch_top1[branch_id] = branch_ranking["top1"]

    distinct_top1 = set(branch_top1.values())
    calibration = branch_context["calibration"]
    requires_confidence_reduction = False
    if len(distinct_top1) == 1:
        if (
            analysis["consensus_status"] != "CONSISTENT"
            or analysis["selected_branch_id"] is not None
            or analysis["top1_uncertainty_preserved"] is not False
            or final_ranking[0] not in distinct_top1
        ):
            raise TrainingError(f"{question_id} has an invalid consistent branch result")
    elif calibration["status"] == "RESOLVED_BY_EXTERNAL_FACT":
        selected_branch_id = calibration["selected_branch_id"]
        if (
            analysis["consensus_status"] != "RESOLVED_BY_EXTERNAL_FACT"
            or analysis["selected_branch_id"] != selected_branch_id
            or analysis["top1_uncertainty_preserved"] is not False
            or final_ranking[0] != branch_top1[selected_branch_id]
        ):
            raise TrainingError(
                f"{question_id} does not follow independently resolved time calibration"
            )
    else:
        if (
            analysis["consensus_status"] != "DIVERGENT_UNRESOLVED"
            or analysis["selected_branch_id"] is not None
            or analysis["top1_uncertainty_preserved"] is not True
            or final_ranking[0] not in distinct_top1
        ):
            raise TrainingError(
                f"{question_id} must preserve divergent chart-branch uncertainty"
            )
        requires_confidence_reduction = True
    return analysis, requires_confidence_reduction


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
    if any(
        evidence_id not in evidence_by_id
        or evidence_by_id[evidence_id]["decision_impact"] == "NEUTRAL"
        for evidence_id in reversal_ids
    ):
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
    if any(
        evidence_id not in evidence_by_id
        or evidence_by_id[evidence_id]["decision_impact"] == "NEUTRAL"
        for evidence_id in removed
    ):
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
    if blind["schema"] != "BLIND-CHART-MODEL-V3":
        raise TrainingError(
            "prediction freeze requires the branch-aware BLIND-CHART-MODEL-V3"
        )
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
    chart_branch_model: dict[str, Any],
) -> dict[str, Any]:
    question_id = row["question_id"]
    branch_context = _validate_chart_branch_model(chart_branch_model)
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
    upstream_dependencies, invalidated_evidence_ids = _validate_upstream_fact_dependencies(
        row.get("upstream_fact_dependencies"),
        evidence_rows=row.get("evidence_ledger"),
        branch_context=branch_context,
        question_id=question_id,
    )
    evidence, evidence_by_id = _validate_evidence(
        row.get("evidence_ledger"),
        option_ids=option_ids,
        option_atoms=semantics["option_atoms"],
        source_routes=source_routes,
        question_id=question_id,
        branch_ids=set(branch_context["branch_ids"]),
        invalidated_evidence_ids=invalidated_evidence_ids,
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
        option_atoms=semantics["option_atoms"],
        evidence_by_id=evidence_by_id,
        final_ranking=final_ranking,
        question_id=question_id,
    )
    branch_analysis, branch_confidence_reduction = _validate_branch_analysis(
        row.get("branch_analysis"),
        branch_context=branch_context,
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
    top1_required_atoms = set(top1_atoms["required_atoms"])
    top1_completed_atoms = set(
        matrix["options"][top1]["required_atom_completion"]
    )
    atom_closure_reduction = top1_completed_atoms != top1_required_atoms
    if atom_closure_reduction or branch_confidence_reduction:
        non_overall_minimum = min(
            confidence[field] for field in CONFIDENCE_COMPONENTS[:-1]
        )
        if confidence["overall_confidence"] >= non_overall_minimum:
            raise TrainingError(
                f"{question_id} unresolved required atoms or chart branches must reduce overall confidence"
            )
        if arbitration["confidence_reduction_required"] is not True:
            raise TrainingError(
                f"{question_id} must disclose the required confidence reduction"
            )
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
        "upstream_fact_dependencies": upstream_dependencies,
        "final_ranking": final_ranking,
        "option_comparison_matrix": matrix,
        "branch_analysis": branch_analysis,
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
        "source_only_invalid_evidence_entries": sum(
            len(
                row.get("upstream_fact_dependencies", {}).get(
                    "invalidated_evidence_ids", []
                )
            )
            for row in predictions
        ),
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
        "unresolved_chart_branch_rankings": sum(
            row.get("branch_analysis", {}).get("consensus_status")
            == "DIVERGENT_UNRESOLVED"
            for row in predictions
        ),
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

from __future__ import annotations

from pathlib import Path
from typing import Any

from .policy import (
    RULE_MIN_DISTINCT_FUTURE_CASES,
    RULE_MIN_SUPPORT_RATIO,
    RULE_MIN_SUPPORTING_APPLICATIONS,
)
from .util import TrainingError, atomic_write_json, load_json, object_sha256


TAXONOMY_RELATIVE_PATH = Path("config/question-taxonomy.json")
LEDGER_RELATIVE_PATH = Path("training/learning-ledger.json")
PROFILE_FIELDS = {
    "topic_tags",
    "subject_tags",
    "time_scope_tags",
    "endpoint_tags",
    "reasoning_skill_tags",
    "source_routes",
    "applied_rule_ids",
}
RULE_FIELDS = {
    "rule_id",
    "topic_tags",
    "reasoning_skill_tags",
    "source_routes",
    "statement",
    "applicability",
    "limits",
    "counterexamples",
    "capability_ceiling",
    "source_basis",
    "trigger_conditions",
    "decision_procedure",
    "stop_conditions",
}


def load_taxonomy(root: Path) -> dict[str, Any]:
    taxonomy = load_json(root / TAXONOMY_RELATIVE_PATH)
    if taxonomy.get("schema") != "QUESTION-REASONING-TAXONOMY-V1":
        raise TrainingError("wrong question taxonomy schema")
    for key in (
        "topic_tags",
        "subject_tags",
        "time_scope_tags",
        "endpoint_tags",
        "reasoning_skill_tags",
        "source_routes",
        "rule_statuses",
    ):
        values = taxonomy.get(key)
        if not isinstance(values, list) or not values or any(not isinstance(item, str) for item in values):
            raise TrainingError(f"taxonomy {key} must be a non-empty string array")
        if len(values) != len(set(values)):
            raise TrainingError(f"taxonomy {key} contains duplicates")
    if set(taxonomy["source_routes"]) != {f"S{index:02d}" for index in range(20)}:
        raise TrainingError("taxonomy source routes must be exactly S00-S19")
    return taxonomy


def _normalize_tags(
    values: Any,
    allowed: list[str],
    field: str,
    *,
    allow_empty: bool = False,
) -> list[str]:
    if not isinstance(values, list) or (not values and not allow_empty):
        raise TrainingError(f"{field} must be a {'possibly empty' if allow_empty else 'non-empty'} array")
    if any(not isinstance(item, str) or item not in allowed for item in values):
        raise TrainingError(f"{field} contains an unknown value")
    if len(values) != len(set(values)):
        raise TrainingError(f"{field} contains duplicates")
    rank = {value: index for index, value in enumerate(allowed)}
    return sorted(values, key=rank.__getitem__)


def load_rule_catalog(root: Path, release: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    if release is None:
        state = load_json(root / "training" / "state.json")
        release = load_json(
            root / "model-learning" / "releases" / f"{state['current_model_release']}.json"
        )
    catalog: dict[str, dict[str, Any]] = {}
    for relative_path in release.get("patches", []):
        patch = load_json(root / relative_path)
        if patch.get("schema") != "MODEL-LEARNING-PATCH-V2":
            continue
        for rule in patch.get("content", {}).get("rules", []):
            rule_id = rule.get("rule_id")
            if rule_id in catalog:
                raise TrainingError(f"duplicate learning rule id: {rule_id}")
            catalog[rule_id] = rule
    return catalog


def validate_question_profile(
    root: Path,
    profile: Any,
    *,
    known_rule_ids: set[str] | None = None,
) -> dict[str, Any]:
    if not isinstance(profile, dict) or set(profile) != PROFILE_FIELDS:
        raise TrainingError("question_profile must contain exactly the required taxonomy fields")
    taxonomy = load_taxonomy(root)
    if known_rule_ids is None:
        known_rule_ids = set(load_rule_catalog(root))
    normalized = {
        "topic_tags": _normalize_tags(profile["topic_tags"], taxonomy["topic_tags"], "topic_tags"),
        "subject_tags": _normalize_tags(profile["subject_tags"], taxonomy["subject_tags"], "subject_tags"),
        "time_scope_tags": _normalize_tags(
            profile["time_scope_tags"], taxonomy["time_scope_tags"], "time_scope_tags"
        ),
        "endpoint_tags": _normalize_tags(
            profile["endpoint_tags"], taxonomy["endpoint_tags"], "endpoint_tags"
        ),
        "reasoning_skill_tags": _normalize_tags(
            profile["reasoning_skill_tags"],
            taxonomy["reasoning_skill_tags"],
            "reasoning_skill_tags",
        ),
        "source_routes": _normalize_tags(
            profile["source_routes"], taxonomy["source_routes"], "source_routes"
        ),
    }
    applied = profile["applied_rule_ids"]
    if not isinstance(applied, list) or any(
        not isinstance(rule_id, str) or rule_id not in known_rule_ids for rule_id in applied
    ):
        raise TrainingError("applied_rule_ids contains an unknown rule")
    if len(applied) != len(set(applied)):
        raise TrainingError("applied_rule_ids contains duplicates")
    normalized["applied_rule_ids"] = sorted(applied)
    return normalized


def validate_rule(root: Path, rule: Any) -> dict[str, Any]:
    if not isinstance(rule, dict) or set(rule) != RULE_FIELDS:
        raise TrainingError("every learning rule must contain exactly the required fields")
    rule_id = rule.get("rule_id")
    if not isinstance(rule_id, str) or not rule_id.startswith("RULE-"):
        raise TrainingError("learning rule_id must start with RULE-")
    if not all(character.isupper() or character.isdigit() or character == "-" for character in rule_id):
        raise TrainingError("learning rule_id must use uppercase letters, digits, and hyphens")
    taxonomy = load_taxonomy(root)
    normalized = dict(rule)
    normalized["topic_tags"] = _normalize_tags(
        rule["topic_tags"], taxonomy["topic_tags"], "rule.topic_tags"
    )
    normalized["reasoning_skill_tags"] = _normalize_tags(
        rule["reasoning_skill_tags"],
        taxonomy["reasoning_skill_tags"],
        "rule.reasoning_skill_tags",
    )
    normalized["source_routes"] = _normalize_tags(
        rule["source_routes"], taxonomy["source_routes"], "rule.source_routes"
    )
    for field in RULE_FIELDS - {
        "rule_id",
        "topic_tags",
        "reasoning_skill_tags",
        "source_routes",
    }:
        if not isinstance(rule[field], str) or not rule[field].strip():
            raise TrainingError(f"learning rule {rule_id} has an empty {field}")
        normalized[field] = rule[field].strip()
    return normalized


def validate_learning_patch_v2(root: Path, payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != {"learning_type", "rules"}:
        raise TrainingError("V2 learning patch must contain learning_type and rules")
    if payload["learning_type"] not in {
        "REASONING_STRATEGY",
        "EXECUTION_PROCEDURE",
        "MODEL_HYPOTHESIS",
    }:
        raise TrainingError("invalid V2 learning_type")
    rules = payload["rules"]
    if not isinstance(rules, list) or not rules:
        raise TrainingError("failed first-blind round needs at least one candidate rule")
    normalized_rules = [validate_rule(root, rule) for rule in rules]
    ids = [rule["rule_id"] for rule in normalized_rules]
    if len(ids) != len(set(ids)):
        raise TrainingError("V2 learning patch contains duplicate rule ids")
    existing = set(load_rule_catalog(root))
    collision = existing.intersection(ids)
    if collision:
        raise TrainingError(f"learning rule already exists: {', '.join(sorted(collision))}")
    return {"learning_type": payload["learning_type"], "rules": normalized_rules}


def empty_learning_ledger(root: Path) -> dict[str, Any]:
    taxonomy = load_taxonomy(root)
    return {
        "schema": "QUESTION-LEARNING-LEDGER-V1",
        "taxonomy_sha256": object_sha256(taxonomy),
        "first_blind_totals": {
            "cases": 0,
            "questions": 0,
            "top1_correct": 0,
            "top2_covered": 0,
        },
        "topic_metrics": {},
        "reasoning_skill_metrics": {},
        "source_route_metrics": {},
        "rule_evidence": {},
        "legacy_unclassified": {
            "first_blind_cases": 0,
            "first_blind_questions": 0,
            "replay_rounds_excluded": 0,
        },
    }


def load_learning_ledger(root: Path) -> dict[str, Any]:
    return load_json(root / LEDGER_RELATIVE_PATH)


def write_learning_ledger(root: Path, ledger: dict[str, Any]) -> None:
    atomic_write_json(root / LEDGER_RELATIVE_PATH, ledger)


def _metric_row() -> dict[str, int]:
    return {"questions": 0, "top1_correct": 0, "top2_covered": 0}


def _update_metric(container: dict[str, Any], tag: str, is_correct: bool, top2_hit: bool) -> None:
    row = container.setdefault(tag, _metric_row())
    row["questions"] += 1
    row["top1_correct"] += int(is_correct)
    row["top2_covered"] += int(top2_hit)


def _rule_status(evidence: dict[str, Any]) -> str:
    applications = evidence["applications"]
    supporting = evidence["supporting_applications"]
    distinct = len(evidence["distinct_application_cases"])
    if applications == 0:
        return "CANDIDATE"
    ratio = supporting / applications
    if (
        supporting >= RULE_MIN_SUPPORTING_APPLICATIONS
        and distinct >= RULE_MIN_DISTINCT_FUTURE_CASES
        and ratio >= RULE_MIN_SUPPORT_RATIO
    ):
        return "VALIDATED"
    if applications >= RULE_MIN_SUPPORTING_APPLICATIONS and ratio < RULE_MIN_SUPPORT_RATIO:
        return "CHALLENGED"
    return "PROVISIONAL"


def register_rules(ledger: dict[str, Any], rules: list[dict[str, Any]]) -> None:
    for rule in rules:
        rule_id = rule["rule_id"]
        if rule_id in ledger["rule_evidence"]:
            raise TrainingError(f"rule evidence already exists: {rule_id}")
        ledger["rule_evidence"][rule_id] = {
            "applications": 0,
            "supporting_applications": 0,
            "contradicting_applications": 0,
            "distinct_application_cases": [],
            "distinct_support_cases": [],
            "status": "CANDIDATE",
        }


def record_first_blind_results(
    ledger: dict[str, Any],
    *,
    case_id: str,
    predictions: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
) -> None:
    review_map = {row["question_id"]: row for row in review_rows}
    totals = ledger["first_blind_totals"]
    totals["cases"] += 1
    for prediction in predictions:
        review = review_map[prediction["question_id"]]
        is_correct = review["is_correct"]
        top2_hit = prediction.get("top2") == review["correct_option"]
        totals["questions"] += 1
        totals["top1_correct"] += int(is_correct)
        totals["top2_covered"] += int(is_correct or top2_hit)
        profile = prediction["question_profile"]
        for tag in profile["topic_tags"]:
            _update_metric(ledger["topic_metrics"], tag, is_correct, is_correct or top2_hit)
        for tag in profile["reasoning_skill_tags"]:
            _update_metric(
                ledger["reasoning_skill_metrics"], tag, is_correct, is_correct or top2_hit
            )
        for tag in profile["source_routes"]:
            _update_metric(ledger["source_route_metrics"], tag, is_correct, is_correct or top2_hit)
        for rule_id in profile["applied_rule_ids"]:
            evidence = ledger["rule_evidence"].get(rule_id)
            if evidence is None:
                raise TrainingError(f"missing evidence ledger entry for applied rule: {rule_id}")
            evidence["applications"] += 1
            evidence["supporting_applications"] += int(is_correct)
            evidence["contradicting_applications"] += int(not is_correct)
            if case_id not in evidence["distinct_application_cases"]:
                evidence["distinct_application_cases"].append(case_id)
            if is_correct and case_id not in evidence["distinct_support_cases"]:
                evidence["distinct_support_cases"].append(case_id)
            evidence["status"] = _rule_status(evidence)


def safe_active_rules(root: Path, release: dict[str, Any]) -> list[dict[str, Any]]:
    catalog = load_rule_catalog(root, release)
    ledger = load_learning_ledger(root)
    rows = []
    for rule_id in sorted(catalog):
        evidence = ledger["rule_evidence"].get(rule_id)
        if evidence is None:
            raise TrainingError(f"learning ledger is missing rule: {rule_id}")
        if evidence["status"] == "RETIRED":
            continue
        rows.append({**catalog[rule_id], "validation_status": evidence["status"]})
    return rows


def public_learning_summary(root: Path) -> dict[str, Any]:
    """Return answer-free aggregate progress for post-reveal reporting only."""
    ledger = load_learning_ledger(root)
    totals = ledger["first_blind_totals"]

    def metric_summary(rows: dict[str, Any]) -> dict[str, Any]:
        return {
            tag: {
                **row,
                "top1_accuracy": row["top1_correct"] / row["questions"],
                "top2_coverage": row["top2_covered"] / row["questions"],
            }
            for tag, row in sorted(rows.items())
        }

    status_counts: dict[str, int] = {}
    for evidence in ledger["rule_evidence"].values():
        status = evidence["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "first_blind_totals": {
            **totals,
            "top1_accuracy": (
                totals["top1_correct"] / totals["questions"] if totals["questions"] else None
            ),
            "top2_coverage": (
                totals["top2_covered"] / totals["questions"] if totals["questions"] else None
            ),
        },
        "topic_metrics": metric_summary(ledger["topic_metrics"]),
        "reasoning_skill_metrics": metric_summary(ledger["reasoning_skill_metrics"]),
        "rule_status_counts": dict(sorted(status_counts.items())),
        "legacy_unclassified": ledger["legacy_unclassified"],
        "overall_maturity_claim": "NOT_DERIVED_FROM_A_SINGLE_CASE_OR_GLOBAL_STREAK",
    }


def validate_learning_ledger(root: Path, ledger: dict[str, Any], release: dict[str, Any]) -> None:
    taxonomy = load_taxonomy(root)
    if ledger.get("schema") != "QUESTION-LEARNING-LEDGER-V1":
        raise TrainingError("wrong learning-ledger schema")
    if ledger.get("taxonomy_sha256") != object_sha256(taxonomy):
        raise TrainingError("learning ledger taxonomy hash mismatch")
    totals = ledger.get("first_blind_totals")
    if not isinstance(totals, dict) or set(totals) != {
        "cases",
        "questions",
        "top1_correct",
        "top2_covered",
    }:
        raise TrainingError("invalid first-blind totals")
    if any(not isinstance(value, int) or value < 0 for value in totals.values()):
        raise TrainingError("first-blind totals must be non-negative integers")
    if not (totals["top1_correct"] <= totals["top2_covered"] <= totals["questions"]):
        raise TrainingError("first-blind totals do not balance")
    legacy = ledger.get("legacy_unclassified")
    if not isinstance(legacy, dict) or set(legacy) != {
        "first_blind_cases",
        "first_blind_questions",
        "replay_rounds_excluded",
    }:
        raise TrainingError("invalid legacy-unclassified counters")
    if any(not isinstance(value, int) or value < 0 for value in legacy.values()):
        raise TrainingError("legacy-unclassified counters must be non-negative integers")
    catalog = load_rule_catalog(root, release)
    if set(ledger.get("rule_evidence", {})) != set(catalog):
        raise TrainingError("learning ledger rule set does not match current model release")
    for rule_id, evidence in ledger["rule_evidence"].items():
        for key in ("applications", "supporting_applications", "contradicting_applications"):
            if not isinstance(evidence.get(key), int) or evidence[key] < 0:
                raise TrainingError(f"invalid evidence count for {rule_id}/{key}")
        if evidence["supporting_applications"] + evidence["contradicting_applications"] != evidence["applications"]:
            raise TrainingError(f"rule evidence totals do not balance for {rule_id}")
        for key in ("distinct_application_cases", "distinct_support_cases"):
            values = evidence.get(key)
            if not isinstance(values, list) or len(values) != len(set(values)):
                raise TrainingError(f"invalid distinct-case evidence for {rule_id}/{key}")
        if not set(evidence["distinct_support_cases"]).issubset(
            evidence["distinct_application_cases"]
        ):
            raise TrainingError(f"support cases are not application cases for {rule_id}")
        if evidence.get("status") != _rule_status(evidence):
            raise TrainingError(f"stale rule status for {rule_id}")
    for key, allowed_tags in (
        ("topic_metrics", taxonomy["topic_tags"]),
        ("reasoning_skill_metrics", taxonomy["reasoning_skill_tags"]),
        ("source_route_metrics", taxonomy["source_routes"]),
    ):
        rows = ledger.get(key)
        if not isinstance(rows, dict) or not set(rows).issubset(allowed_tags):
            raise TrainingError(f"invalid learning-ledger metric keys: {key}")
        for tag, row in rows.items():
            if set(row) != {"questions", "top1_correct", "top2_covered"}:
                raise TrainingError(f"invalid metric row for {key}/{tag}")
            if any(not isinstance(value, int) or value < 0 for value in row.values()):
                raise TrainingError(f"invalid metric count for {key}/{tag}")
            if not (row["top1_correct"] <= row["top2_covered"] <= row["questions"]):
                raise TrainingError(f"metric counts do not balance for {key}/{tag}")

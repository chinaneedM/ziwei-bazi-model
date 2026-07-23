from __future__ import annotations

from pathlib import Path
from typing import Any

from .policy import (
    MAX_APPLIED_RULES_PER_QUESTION,
    RULE_MIN_DISTINCT_FUTURE_CASES,
    RULE_MIN_SUPPORT_RATIO,
    RULE_MIN_SUPPORTING_APPLICATIONS,
)
from .util import TrainingError, atomic_write_json, load_json, object_sha256


TAXONOMY_RELATIVE_PATH = Path("config/question-taxonomy.json")
LEDGER_RELATIVE_PATH = Path("training/learning-ledger.json")
RUNTIME_GOVERNANCE_RELATIVE_PATH = Path("model-learning/runtime-governance.json")
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
RULE_ATTRIBUTION_FIELDS = {
    "decisive_rule_ids",
    "supporting_rule_ids",
    "counterevidence_rule_ids",
    "decision_changed",
}
CONFIDENCE_BINS = (
    (0, 49, "00-49"),
    (50, 59, "50-59"),
    (60, 69, "60-69"),
    (70, 79, "70-79"),
    (80, 89, "80-89"),
    (90, 100, "90-100"),
)


def load_taxonomy(root: Path) -> dict[str, Any]:
    taxonomy = load_json(root / TAXONOMY_RELATIVE_PATH)
    if taxonomy.get("schema") != "QUESTION-REASONING-TAXONOMY-V2":
        raise TrainingError("wrong question taxonomy schema")
    for key in (
        "topic_tags",
        "subject_tags",
        "time_scope_tags",
        "endpoint_tags",
        "reasoning_skill_tags",
        "source_routes",
        "governance_tags",
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


def load_runtime_governance(root: Path) -> dict[str, Any]:
    path = root / RUNTIME_GOVERNANCE_RELATIVE_PATH
    if not path.is_file():
        return {
            "schema": "MODEL-RUNTIME-GOVERNANCE-V1",
            "authority": "AUTOMATED_TRAINING_MAINTENANCE",
            "canonical_sources_mutated": False,
            "suppressed_rules": [],
        }
    return load_json(path)


def suppressed_rule_ids(root: Path) -> set[str]:
    governance = load_runtime_governance(root)
    rows = governance.get("suppressed_rules", [])
    return {
        row["rule_id"]
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("rule_id"), str)
    }


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


def validate_rule_attribution(
    root: Path,
    attribution: Any,
    *,
    profile: dict[str, Any],
    catalog: dict[str, dict[str, Any]] | None = None,
    ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(attribution, dict) or set(attribution) != RULE_ATTRIBUTION_FIELDS:
        raise TrainingError("rule_attribution must contain exactly the required fields")
    if catalog is None:
        catalog = load_rule_catalog(root)
    if ledger is None:
        ledger = load_learning_ledger(root)
    normalized: dict[str, Any] = {}
    combined: list[str] = []
    for field in (
        "decisive_rule_ids",
        "supporting_rule_ids",
        "counterevidence_rule_ids",
    ):
        values = attribution[field]
        if (
            not isinstance(values, list)
            or any(not isinstance(rule_id, str) or rule_id not in catalog for rule_id in values)
            or len(values) != len(set(values))
        ):
            raise TrainingError(f"{field} contains an unknown or duplicate rule")
        normalized[field] = sorted(values)
        combined.extend(values)
    if len(combined) != len(set(combined)):
        raise TrainingError("rule_attribution roles must be disjoint")
    if sorted(combined) != profile["applied_rule_ids"]:
        raise TrainingError("rule_attribution must classify every applied_rule_id exactly once")
    if len(combined) > MAX_APPLIED_RULES_PER_QUESTION:
        raise TrainingError(
            f"a question may apply at most {MAX_APPLIED_RULES_PER_QUESTION} rules"
        )
    if len(normalized["decisive_rule_ids"]) > 2:
        raise TrainingError("at most two rules may be decisive for one Top1 decision")
    decision_changed = attribution["decision_changed"]
    if not isinstance(decision_changed, bool):
        raise TrainingError("rule_attribution decision_changed must be boolean")
    if decision_changed != bool(normalized["decisive_rule_ids"]):
        raise TrainingError(
            "decision_changed must be true exactly when decisive_rule_ids is non-empty"
        )
    suppressed = suppressed_rule_ids(root)
    for rule_id in combined:
        if rule_id in suppressed:
            raise TrainingError(f"suppressed rule may not be applied: {rule_id}")
        rule = catalog[rule_id]
        if not (
            set(rule["topic_tags"]).intersection(profile["topic_tags"])
            or set(rule["reasoning_skill_tags"]).intersection(
                profile["reasoning_skill_tags"]
            )
        ):
            raise TrainingError(f"applied rule is outside the question scope: {rule_id}")
    for rule_id in (
        normalized["decisive_rule_ids"] + normalized["supporting_rule_ids"]
    ):
        evidence = ledger["rule_evidence"].get(rule_id)
        attributed_evidence = ledger.get("attributed_rule_evidence", {}).get(rule_id)
        if (
            evidence is not None
            and evidence.get("status") == "CHALLENGED"
        ) or (
            attributed_evidence is not None
            and attributed_evidence.get("status") == "CHALLENGED"
        ):
            raise TrainingError(
                f"challenged rule may only be counterevidence: {rule_id}"
            )
    normalized["decision_changed"] = decision_changed
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
        raise TrainingError("failed round needs at least one generic model-learning rule")
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
        "attributed_rule_evidence": {},
        "confidence_calibration": {
            "started_after_first_blind_questions": 0,
            "questions": 0,
            "correct": 0,
            "confidence_sum": 0,
            "brier_sum": 0.0,
            "bins": {},
        },
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


def ensure_learning_extensions(
    ledger: dict[str, Any],
    *,
    rule_ids: set[str] | None = None,
) -> None:
    if rule_ids is None:
        rule_ids = set(ledger.get("rule_evidence", {}))
    attributed = ledger.setdefault("attributed_rule_evidence", {})
    for rule_id in sorted(rule_ids):
        attributed.setdefault(
            rule_id,
            {
                "decisive_applications": 0,
                "decisive_supporting_applications": 0,
                "decisive_contradicting_applications": 0,
                "decision_change_applications": 0,
                "supporting_mentions": 0,
                "counterevidence_mentions": 0,
                "distinct_decisive_cases": [],
                "distinct_decisive_support_cases": [],
                "status": "CANDIDATE",
            },
        )
    ledger.setdefault(
        "confidence_calibration",
        {
            "started_after_first_blind_questions": ledger["first_blind_totals"][
                "questions"
            ],
            "questions": 0,
            "correct": 0,
            "confidence_sum": 0,
            "brier_sum": 0.0,
            "bins": {},
        },
    )


def register_rules(ledger: dict[str, Any], rules: list[dict[str, Any]]) -> None:
    ensure_learning_extensions(ledger)
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
        ensure_learning_extensions(ledger, rule_ids={rule_id})


def _confidence_bin(confidence: int) -> str:
    for minimum, maximum, label in CONFIDENCE_BINS:
        if minimum <= confidence <= maximum:
            return label
    raise TrainingError("confidence is outside the supported calibration range")


def _record_confidence(
    calibration: dict[str, Any],
    *,
    confidence: int,
    is_correct: bool,
) -> None:
    probability = confidence / 100
    calibration["questions"] += 1
    calibration["correct"] += int(is_correct)
    calibration["confidence_sum"] += confidence
    calibration["brier_sum"] += (probability - int(is_correct)) ** 2
    row = calibration["bins"].setdefault(
        _confidence_bin(confidence),
        {"questions": 0, "correct": 0, "confidence_sum": 0},
    )
    row["questions"] += 1
    row["correct"] += int(is_correct)
    row["confidence_sum"] += confidence


def _record_attribution(
    ledger: dict[str, Any],
    *,
    case_id: str,
    attribution: dict[str, Any],
    is_correct: bool,
) -> None:
    attributed = ledger["attributed_rule_evidence"]
    for rule_id in attribution["decisive_rule_ids"]:
        row = attributed[rule_id]
        row["decisive_applications"] += 1
        row["decisive_supporting_applications"] += int(is_correct)
        row["decisive_contradicting_applications"] += int(not is_correct)
        row["decision_change_applications"] += int(attribution["decision_changed"])
        if case_id not in row["distinct_decisive_cases"]:
            row["distinct_decisive_cases"].append(case_id)
        if is_correct and case_id not in row["distinct_decisive_support_cases"]:
            row["distinct_decisive_support_cases"].append(case_id)
        row["status"] = _rule_status(
            {
                "applications": row["decisive_applications"],
                "supporting_applications": row[
                    "decisive_supporting_applications"
                ],
                "distinct_application_cases": row["distinct_decisive_cases"],
            }
        )
    for rule_id in attribution["supporting_rule_ids"]:
        attributed[rule_id]["supporting_mentions"] += 1
    for rule_id in attribution["counterevidence_rule_ids"]:
        attributed[rule_id]["counterevidence_mentions"] += 1


def record_first_blind_results(
    ledger: dict[str, Any],
    *,
    case_id: str,
    predictions: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
) -> None:
    ensure_learning_extensions(
        ledger,
        rule_ids=set(ledger.get("rule_evidence", {})),
    )
    review_map = {row["question_id"]: row for row in review_rows}
    totals = ledger["first_blind_totals"]
    totals["cases"] += 1
    for prediction in predictions:
        review = review_map[prediction["question_id"]]
        if review.get("is_scored", True) is False:
            continue
        is_correct = review["is_correct"]
        top2_hit = prediction.get("top2") == review["correct_option"]
        totals["questions"] += 1
        totals["top1_correct"] += int(is_correct)
        totals["top2_covered"] += int(is_correct or top2_hit)
        profile = prediction["question_profile"]
        attribution = prediction["rule_attribution"]
        _record_confidence(
            ledger["confidence_calibration"],
            confidence=prediction["confidence"],
            is_correct=is_correct,
        )
        for tag in profile["topic_tags"]:
            _update_metric(ledger["topic_metrics"], tag, is_correct, is_correct or top2_hit)
        for tag in profile["reasoning_skill_tags"]:
            _update_metric(
                ledger["reasoning_skill_metrics"], tag, is_correct, is_correct or top2_hit
            )
        for tag in profile["source_routes"]:
            _update_metric(ledger["source_route_metrics"], tag, is_correct, is_correct or top2_hit)
        _record_attribution(
            ledger,
            case_id=case_id,
            attribution=attribution,
            is_correct=is_correct,
        )
        for rule_id in attribution["decisive_rule_ids"]:
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
    ensure_learning_extensions(ledger, rule_ids=set(catalog))
    suppressed = suppressed_rule_ids(root)
    rows = []
    for rule_id in sorted(catalog):
        evidence = ledger["rule_evidence"].get(rule_id)
        if evidence is None:
            raise TrainingError(f"learning ledger is missing rule: {rule_id}")
        if evidence["status"] == "RETIRED" or rule_id in suppressed:
            continue
        attributed = ledger["attributed_rule_evidence"][rule_id]
        rows.append(
            {
                **catalog[rule_id],
                "validation_status": evidence["status"],
                "attributed_validation_status": attributed["status"],
                "runtime_role": (
                    "COUNTEREVIDENCE_ONLY"
                    if evidence["status"] == "CHALLENGED"
                    else "DECISIVE_OR_SUPPORTING_CANDIDATE"
                ),
            }
        )
    return rows


def build_rule_router(root: Path, release: dict[str, Any]) -> dict[str, Any]:
    rules = safe_active_rules(root, release)
    rank = {"VALIDATED": 0, "PROVISIONAL": 1, "CANDIDATE": 2, "CHALLENGED": 3}

    def sort_key(rule: dict[str, Any]) -> tuple[Any, ...]:
        return (
            rank.get(rule["validation_status"], 9),
            len(rule["topic_tags"]),
            rule["rule_id"],
        )

    taxonomy = load_taxonomy(root)
    routes: dict[str, Any] = {}
    for topic in taxonomy["topic_tags"]:
        matching = [rule for rule in rules if topic in rule["topic_tags"]]
        decisive = sorted(
            (
                rule
                for rule in matching
                if rule["runtime_role"] == "DECISIVE_OR_SUPPORTING_CANDIDATE"
            ),
            key=sort_key,
        )
        counter = sorted(
            (
                rule
                for rule in matching
                if rule["runtime_role"] == "COUNTEREVIDENCE_ONLY"
            ),
            key=sort_key,
        )
        routes[topic] = {
            "decisive_or_supporting_rule_ids": [
                rule["rule_id"]
                for rule in decisive[:MAX_APPLIED_RULES_PER_QUESTION]
            ],
            "counterevidence_rule_ids": [
                rule["rule_id"]
                for rule in counter[:MAX_APPLIED_RULES_PER_QUESTION]
            ],
        }
    return {
        "schema": "TOPIC-RULE-ROUTER-V1",
        "max_applied_rules_per_question": MAX_APPLIED_RULES_PER_QUESTION,
        "selection_order": (
            "TAG_QUESTION_FIRST_THEN_SELECT_SCOPE_MATCHED_RULES; "
            "CHALLENGED_RULES_COUNTEREVIDENCE_ONLY"
        ),
        "topics": routes,
    }


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
    attributed_status_counts: dict[str, int] = {}
    for evidence in ledger["attributed_rule_evidence"].values():
        status = evidence["status"]
        attributed_status_counts[status] = attributed_status_counts.get(status, 0) + 1
    calibration = ledger["confidence_calibration"]
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
        "attributed_rule_status_counts": dict(sorted(attributed_status_counts.items())),
        "confidence_calibration": {
            **calibration,
            "mean_confidence": (
                calibration["confidence_sum"] / calibration["questions"] / 100
                if calibration["questions"]
                else None
            ),
            "accuracy": (
                calibration["correct"] / calibration["questions"]
                if calibration["questions"]
                else None
            ),
            "brier_score": (
                calibration["brier_sum"] / calibration["questions"]
                if calibration["questions"]
                else None
            ),
        },
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
    attributed = ledger.get("attributed_rule_evidence")
    if not isinstance(attributed, dict) or set(attributed) != set(catalog):
        raise TrainingError(
            "attributed rule evidence must match the current model release"
        )
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
        if (
            evidence.get("status") != "RETIRED"
            and evidence.get("status") != _rule_status(evidence)
        ):
            raise TrainingError(f"stale rule status for {rule_id}")
    for rule_id, evidence in attributed.items():
        integer_fields = (
            "decisive_applications",
            "decisive_supporting_applications",
            "decisive_contradicting_applications",
            "decision_change_applications",
            "supporting_mentions",
            "counterevidence_mentions",
        )
        if any(
            not isinstance(evidence.get(key), int) or evidence[key] < 0
            for key in integer_fields
        ):
            raise TrainingError(f"invalid attributed evidence counts for {rule_id}")
        if (
            evidence["decisive_supporting_applications"]
            + evidence["decisive_contradicting_applications"]
            != evidence["decisive_applications"]
        ):
            raise TrainingError(
                f"attributed decisive evidence does not balance for {rule_id}"
            )
        if evidence["decision_change_applications"] > evidence["decisive_applications"]:
            raise TrainingError(
                f"decision-change count exceeds decisive applications for {rule_id}"
            )
        for key in ("distinct_decisive_cases", "distinct_decisive_support_cases"):
            values = evidence.get(key)
            if not isinstance(values, list) or len(values) != len(set(values)):
                raise TrainingError(
                    f"invalid attributed distinct-case evidence for {rule_id}/{key}"
                )
        if not set(evidence["distinct_decisive_support_cases"]).issubset(
            evidence["distinct_decisive_cases"]
        ):
            raise TrainingError(
                f"attributed support cases are not decisive cases for {rule_id}"
            )
        derived = _rule_status(
            {
                "applications": evidence["decisive_applications"],
                "supporting_applications": evidence[
                    "decisive_supporting_applications"
                ],
                "distinct_application_cases": evidence["distinct_decisive_cases"],
            }
        )
        if evidence.get("status") != derived:
            raise TrainingError(f"stale attributed rule status for {rule_id}")
    calibration = ledger.get("confidence_calibration")
    if not isinstance(calibration, dict) or set(calibration) != {
        "started_after_first_blind_questions",
        "questions",
        "correct",
        "confidence_sum",
        "brier_sum",
        "bins",
    }:
        raise TrainingError("invalid confidence calibration ledger")
    for key in (
        "started_after_first_blind_questions",
        "questions",
        "correct",
        "confidence_sum",
    ):
        if not isinstance(calibration[key], int) or calibration[key] < 0:
            raise TrainingError(f"invalid confidence calibration field: {key}")
    if (
        not isinstance(calibration["brier_sum"], (int, float))
        or isinstance(calibration["brier_sum"], bool)
        or calibration["brier_sum"] < 0
        or calibration["correct"] > calibration["questions"]
        or calibration["confidence_sum"] > calibration["questions"] * 100
    ):
        raise TrainingError("confidence calibration totals do not balance")
    if not isinstance(calibration["bins"], dict) or not set(
        calibration["bins"]
    ).issubset({label for _, _, label in CONFIDENCE_BINS}):
        raise TrainingError("invalid confidence calibration bins")
    bin_questions = bin_correct = bin_confidence = 0
    for label, row in calibration["bins"].items():
        if not isinstance(row, dict) or set(row) != {
            "questions",
            "correct",
            "confidence_sum",
        }:
            raise TrainingError(f"invalid confidence calibration bin: {label}")
        if any(not isinstance(value, int) or value < 0 for value in row.values()):
            raise TrainingError(f"invalid confidence calibration counts: {label}")
        if row["correct"] > row["questions"] or row["confidence_sum"] > row["questions"] * 100:
            raise TrainingError(f"confidence calibration bin does not balance: {label}")
        bin_questions += row["questions"]
        bin_correct += row["correct"]
        bin_confidence += row["confidence_sum"]
    if (
        bin_questions != calibration["questions"]
        or bin_correct != calibration["correct"]
        or bin_confidence != calibration["confidence_sum"]
    ):
        raise TrainingError("confidence calibration bins do not match totals")
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

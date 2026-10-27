from __future__ import annotations

from pathlib import Path
from typing import Any

from .learning import (
    ensure_learning_extensions,
    load_learning_ledger,
    load_rule_catalog,
    load_runtime_governance,
    safe_active_rules,
    write_learning_ledger,
)
from .policy import (
    MAINTENANCE_ANOMALY_COOLDOWN_QUESTIONS,
    MAINTENANCE_RECENT_WINDOW_QUESTIONS,
    MEDIUM_MAINTENANCE_INTERVAL_QUESTIONS,
    SHORT_MAINTENANCE_INTERVAL_QUESTIONS,
)
from .util import (
    TrainingError,
    atomic_write_json,
    exclusive_write_json,
    load_json,
    object_sha256,
    utc_now,
)


MAINTENANCE_STATE_PATH = Path("training/maintenance-state.json")
MAINTENANCE_REPORT_DIR = Path("training/maintenance-reports")
REPLAY_EFFECTIVENESS_PATH = Path("training/replay-effectiveness.json")
OPERATIONAL_EVENTS_PATH = Path("training/maintenance-events.json")


def _default_state() -> dict[str, Any]:
    return {
        "schema": "TRAINING-MAINTENANCE-STATE-V1",
        "short_interval_first_blind_questions": SHORT_MAINTENANCE_INTERVAL_QUESTIONS,
        "medium_interval_first_blind_questions": MEDIUM_MAINTENANCE_INTERVAL_QUESTIONS,
        "last_short_milestone_questions": 0,
        "last_medium_milestone_questions": 0,
        "last_anomaly_maintenance_questions": None,
        "next_maintenance_index": 1,
        "history": [],
    }


def load_maintenance_state(root: Path) -> dict[str, Any]:
    path = root / MAINTENANCE_STATE_PATH
    return load_json(path) if path.is_file() else _default_state()


def _round_rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score_path in (root / "training" / "runs").glob("*/score.json"):
        score = load_json(score_path)
        if score.get("evaluation_kind") not in {"FIRST_BLIND", "SPACED_REPLAY"}:
            continue
        round_dir = score_path.parent
        frozen_path = round_dir / "prediction-freeze.json"
        frozen = load_json(frozen_path) if frozen_path.is_file() else {"predictions": []}
        confidences = [
            (
                prediction["confidence_components"]["overall_confidence"]
                if isinstance(prediction.get("confidence_components"), dict)
                else prediction.get("confidence")
            )
            for prediction in frozen.get("predictions", [])
            if isinstance(
                (
                    prediction["confidence_components"].get("overall_confidence")
                    if isinstance(prediction.get("confidence_components"), dict)
                    else prediction.get("confidence")
                ),
                int,
            )
        ]
        rows.append(
            {
                "round_id": score["round_id"],
                "case_id": score["case_id"],
                "evaluation_kind": score["evaluation_kind"],
                "correct_count": score["correct_count"],
                "scoreable_question_count": score.get(
                    "scoreable_question_count", score["question_count"]
                ),
                "top2_covered_count": score.get("top2_covered_count", 0),
                "passed": score["passed"],
                "mean_confidence": (
                    sum(confidences) / len(confidences) / 100
                    if confidences
                    else None
                ),
                "scored_at": score.get("scored_at", ""),
            }
        )
    rows.sort(key=lambda row: (row["scored_at"], row["round_id"]))
    return rows


def _reasoning_quality_metrics(root: Path) -> dict[str, Any]:
    freezes = [
        load_json(path)
        for path in sorted((root / "training" / "runs").glob("*/prediction-freeze.json"))
    ]
    new_freezes = [
        freeze for freeze in freezes if freeze.get("schema") == "FROZEN-PREDICTION-V2"
    ]
    predictions = [
        prediction
        for freeze in new_freezes
        for prediction in freeze.get("predictions", [])
    ]
    reports = [
        freeze["reasoning_completeness_report"]
        for freeze in new_freezes
        if isinstance(freeze.get("reasoning_completeness_report"), dict)
    ]
    questions = len(predictions)
    evidence_rows = [
        evidence
        for prediction in predictions
        for evidence in prediction["evidence_ledger"]
    ]
    family_count = len(
        {
            (prediction["question_id"], evidence["evidence_family_id"])
            for prediction in predictions
            for evidence in prediction["evidence_ledger"]
        }
    )
    decisive_ablations = sum(
        len(prediction["counterfactual_analysis"]["decisive_rule_ablations"])
        for prediction in predictions
    )
    high_unclosed = sum(
        report["high_confidence_with_unclosed_critical_link"] for report in reports
    )
    cross_conflicts = sum(
        report["cross_question_unresolved_conflicts"] for report in reports
    )
    source_only_invalid = sum(
        report["source_only_invalid_evidence_entries"] for report in reports
    )
    topics: dict[str, int] = {}
    option_counts: dict[str, int] = {}
    precision_questions = composite_questions = 0
    for prediction in predictions:
        for topic in prediction["question_profile"]["topic_tags"]:
            topics[topic] = topics.get(topic, 0) + 1
        option_count = len(prediction["final_ranking"])
        option_counts[str(option_count)] = option_counts.get(str(option_count), 0) + 1
        semantic = prediction["question_semantic_model"]
        composite_questions += int(semantic["is_composite_narrative"])
        precision_questions += int(
            any(
                atoms["severe_irreversible_or_high_precision_atoms"]
                for atoms in semantic["option_atoms"].values()
            )
        )
    low_sample_threshold = 30
    return {
        "schema": "REASONING-DEGRADATION-METRICS-V1",
        "legacy_freezes_excluded": len(freezes) - len(new_freezes),
        "v2_freezes": len(new_freezes),
        "v2_questions": questions,
        "sample_status": (
            "INSUFFICIENT_SAMPLE"
            if questions < low_sample_threshold
            else "OBSERVED"
        ),
        "low_sample_threshold_questions": low_sample_threshold,
        "blind_chart_model_completion_rate": (
            len(reports) / len(new_freezes) if new_freezes else None
        ),
        "ziwei_independent_seal_completion_rate": (
            sum(
                "ziwei_track_seal" in prediction for prediction in predictions
            )
            / questions
            if questions
            else None
        ),
        "bazi_independent_seal_completion_rate": (
            sum("bazi_track_seal" in prediction for prediction in predictions)
            / questions
            if questions
            else None
        ),
        "cross_track_conflict_preservation_rate": (
            sum(
                isinstance(
                    prediction["cross_track_arbitration"]["conflict_layers"],
                    list,
                )
                for prediction in predictions
            )
            / questions
            if questions
            else None
        ),
        "valid_evidence_entries": len(evidence_rows),
        "independent_evidence_families": family_count,
        "source_only_invalid_evidence_entries": source_only_invalid,
        "all_option_comparison_coverage": (
            sum("option_comparison_matrix" in row for row in predictions)
            / questions
            if questions
            else None
        ),
        "reversal_test_completion_rate": (
            sum("adversarial_review" in row for row in predictions) / questions
            if questions
            else None
        ),
        "decisive_rules_with_recorded_top1_change": decisive_ablations,
        "high_confidence_unclosed_critical_links": high_unclosed,
        "cross_question_unresolved_conflicts": cross_conflicts,
        "known_rule_execution_omissions": sum(
            prediction["adversarial_review"]["known_rule_execution_omissions"]
            not in {"NONE", "无", "无遗漏"}
            for prediction in predictions
        ),
        "label_to_evidence_mismatch": sum(
            len(prediction["question_profile"]["source_routes"])
            > len(
                {
                    evidence["source_route"]
                    for evidence in prediction["evidence_ledger"]
                }
            )
            for prediction in predictions
        ),
        "template_or_compression_check": (
            "STRUCTURAL_VALIDATION_ACTIVE"
            if questions
            else "INSUFFICIENT_SAMPLE"
        ),
        "question_distribution_monitoring": {
            "topics": dict(sorted(topics.items())),
            "option_counts": dict(sorted(option_counts.items())),
            "composite_questions": composite_questions,
            "high_precision_endpoint_questions": precision_questions,
            "overlapping_topic_counts_are_not_independent": True,
            "automatic_reordering_or_reweighting": False,
            "automatic_model_change": False,
            "sample_status": (
                "INSUFFICIENT_SAMPLE"
                if questions < low_sample_threshold
                else "OBSERVED"
            ),
        },
    }


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    questions = sum(row["scoreable_question_count"] for row in rows)
    correct = sum(row["correct_count"] for row in rows)
    top2 = sum(row["top2_covered_count"] for row in rows)
    confidence_weight = sum(
        row["mean_confidence"] * row["scoreable_question_count"]
        for row in rows
        if row["mean_confidence"] is not None
    )
    confidence_questions = sum(
        row["scoreable_question_count"]
        for row in rows
        if row["mean_confidence"] is not None
    )
    accuracy = correct / questions if questions else None
    mean_confidence = (
        confidence_weight / confidence_questions if confidence_questions else None
    )
    return {
        "rounds": len(rows),
        "questions": questions,
        "top1_correct": correct,
        "top2_covered": top2,
        "top1_accuracy": accuracy,
        "top2_coverage": top2 / questions if questions else None,
        "mean_confidence": mean_confidence,
        "confidence_accuracy_gap": (
            mean_confidence - accuracy
            if mean_confidence is not None and accuracy is not None
            else None
        ),
        "round_ids": [row["round_id"] for row in rows],
        "case_ids": [row["case_id"] for row in rows],
    }


def _take_question_window(
    rows: list[dict[str, Any]],
    question_limit: int,
    *,
    from_end: int = 0,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    skipped = 0
    questions = 0
    for row in reversed(rows):
        if skipped < from_end:
            skipped += row["scoreable_question_count"]
            continue
        if questions >= question_limit:
            break
        selected.append(row)
        questions += row["scoreable_question_count"]
    return list(reversed(selected))


def build_replay_effectiveness(root: Path) -> dict[str, Any]:
    rows = _round_rows(root)
    first_blind = {
        row["case_id"]: row for row in rows if row["evaluation_kind"] == "FIRST_BLIND"
    }
    cases: dict[str, Any] = {}
    for row in rows:
        if row["evaluation_kind"] != "SPACED_REPLAY" or row["case_id"] not in first_blind:
            continue
        base = first_blind[row["case_id"]]
        case = cases.setdefault(
            row["case_id"],
            {
                "first_blind_round_id": base["round_id"],
                "first_blind_correct": base["correct_count"],
                "replays": [],
            },
        )
        case["replays"].append(
            {
                "round_id": row["round_id"],
                "correct_count": row["correct_count"],
                "delta_from_first_blind": row["correct_count"]
                - base["correct_count"],
                "passed": row["passed"],
            }
        )
    improved = unchanged = regressed = 0
    for case in cases.values():
        for replay in case["replays"]:
            delta = replay["delta_from_first_blind"]
            improved += int(delta > 0)
            unchanged += int(delta == 0)
            regressed += int(delta < 0)
    return {
        "schema": "SPACED-REPLAY-EFFECTIVENESS-V1",
        "generated_at": utc_now(),
        "cases": cases,
        "summary": {
            "replay_rounds": improved + unchanged + regressed,
            "improved": improved,
            "unchanged": unchanged,
            "regressed": regressed,
        },
        "counts_as_first_blind_evidence": False,
    }


def _duplicate_candidates(
    catalog: dict[str, dict[str, Any]],
    suppressed: set[str],
) -> list[dict[str, Any]]:
    active_ids = sorted(set(catalog) - suppressed)
    candidates: list[dict[str, Any]] = []
    for index, left_id in enumerate(active_ids):
        left = catalog[left_id]
        for right_id in active_ids[index + 1 :]:
            right = catalog[right_id]
            left_topics = set(left["topic_tags"])
            right_topics = set(right["topic_tags"])
            left_skills = set(left["reasoning_skill_tags"])
            right_skills = set(right["reasoning_skill_tags"])
            topic_union = left_topics | right_topics
            skill_union = left_skills | right_skills
            topic_similarity = (
                len(left_topics & right_topics) / len(topic_union)
                if topic_union
                else 0
            )
            skill_similarity = (
                len(left_skills & right_skills) / len(skill_union)
                if skill_union
                else 0
            )
            combined = (topic_similarity + skill_similarity) / 2
            if combined >= 0.72:
                candidates.append(
                    {
                        "left_rule_id": left_id,
                        "right_rule_id": right_id,
                        "topic_jaccard": round(topic_similarity, 4),
                        "skill_jaccard": round(skill_similarity, 4),
                        "combined_similarity": round(combined, 4),
                        "action": "REVIEW_FOR_FUTURE_SUPERSESSION_NOT_AUTO_MERGED",
                    }
                )
    candidates.sort(
        key=lambda row: (
            -row["combined_similarity"],
            row["left_rule_id"],
            row["right_rule_id"],
        )
    )
    return candidates[:20]


def _operational_events(root: Path) -> list[dict[str, Any]]:
    path = root / OPERATIONAL_EVENTS_PATH
    if not path.is_file():
        return []
    payload = load_json(path)
    rows = payload.get("events")
    return rows if isinstance(rows, list) else []


def record_operational_event(
    root: Path,
    *,
    kind: str,
    round_count: int,
    detail: str,
) -> dict[str, Any]:
    if kind not in {"HANDOFF", "HASH_BINDING", "CONTROLLER", "WORKFLOW"}:
        raise TrainingError("unsupported maintenance operational event kind")
    if not isinstance(round_count, int) or round_count < 0:
        raise TrainingError("operational event round_count must be non-negative")
    path = root / OPERATIONAL_EVENTS_PATH
    payload = (
        load_json(path)
        if path.is_file()
        else {"schema": "TRAINING-OPERATIONAL-EVENTS-V1", "events": []}
    )
    event = {
        "kind": kind,
        "round_count": round_count,
        "detail": detail.strip(),
        "recorded_at": utc_now(),
    }
    if not event["detail"]:
        raise TrainingError("operational event needs a detail")
    payload["events"].append(event)
    atomic_write_json(path, payload)
    return event


def _anomalies(
    root: Path,
    *,
    first_blind_rows: list[dict[str, Any]],
    replay_effectiveness: dict[str, Any],
    active_rule_count: int,
    current_round_count: int,
) -> list[dict[str, Any]]:
    policy = load_json(root / "config" / "training-policy.json")[
        "maintenance_policy"
    ]["anomaly_triggers"]
    recent_rows = _take_question_window(
        first_blind_rows, MAINTENANCE_RECENT_WINDOW_QUESTIONS
    )
    recent = _aggregate(recent_rows)
    previous_rows = _take_question_window(
        first_blind_rows,
        MAINTENANCE_RECENT_WINDOW_QUESTIONS,
        from_end=recent["questions"],
    )
    previous = _aggregate(previous_rows)
    anomalies: list[dict[str, Any]] = []
    required_low = policy["consecutive_low_first_blind_cases"]
    low_threshold = policy["maximum_correct_for_low_five_question_case"]
    tail = first_blind_rows[-required_low:]
    if len(tail) == required_low and all(
        row["scoreable_question_count"] == 5
        and row["correct_count"] <= low_threshold
        for row in tail
    ):
        anomalies.append(
            {
                "code": "CONSECUTIVE_LOW_FIRST_BLIND_CASES",
                "observed": [
                    {
                        "case_id": row["case_id"],
                        "correct_count": row["correct_count"],
                    }
                    for row in tail
                ],
                "threshold": required_low,
            }
        )
    if (
        recent["questions"] >= MAINTENANCE_RECENT_WINDOW_QUESTIONS
        and previous["questions"] >= MAINTENANCE_RECENT_WINDOW_QUESTIONS
        and previous["top1_accuracy"] - recent["top1_accuracy"]
        >= policy["accuracy_drop_percentage_points"] / 100
    ):
        anomalies.append(
            {
                "code": "RECENT_ACCURACY_DROP",
                "observed": previous["top1_accuracy"] - recent["top1_accuracy"],
                "threshold": policy["accuracy_drop_percentage_points"] / 100,
            }
        )
    if (
        recent["questions"] >= MAINTENANCE_RECENT_WINDOW_QUESTIONS
        and recent["top2_coverage"] < policy["minimum_recent_top2_coverage"]
    ):
        anomalies.append(
            {
                "code": "LOW_RECENT_TOP2_COVERAGE",
                "observed": recent["top2_coverage"],
                "threshold": policy["minimum_recent_top2_coverage"],
            }
        )
    if (
        recent["questions"] >= MAINTENANCE_RECENT_WINDOW_QUESTIONS
        and recent["confidence_accuracy_gap"] is not None
        and recent["confidence_accuracy_gap"]
        > policy["maximum_confidence_accuracy_gap"]
    ):
        anomalies.append(
            {
                "code": "OVERCONFIDENCE",
                "observed": recent["confidence_accuracy_gap"],
                "threshold": policy["maximum_confidence_accuracy_gap"],
            }
        )
    if active_rule_count > policy["active_rule_limit"]:
        anomalies.append(
            {
                "code": "ACTIVE_RULE_LIMIT_EXCEEDED",
                "observed": active_rule_count,
                "threshold": policy["active_rule_limit"],
            }
        )
    no_improvement_limit = policy["same_replay_no_improvement_limit"]
    for case_id, case in replay_effectiveness["cases"].items():
        if len(case["replays"]) >= no_improvement_limit and all(
            replay["delta_from_first_blind"] <= 0
            for replay in case["replays"][-no_improvement_limit:]
        ):
            anomalies.append(
                {
                    "code": "REPEATED_REPLAY_NO_IMPROVEMENT",
                    "case_id": case_id,
                    "observed": [
                        replay["delta_from_first_blind"]
                        for replay in case["replays"][-no_improvement_limit:]
                    ],
                    "threshold": no_improvement_limit,
                }
            )
    recent_operational = [
        event
        for event in _operational_events(root)
        if event.get("round_count", -1) >= current_round_count - 4
    ]
    if (
        len(recent_operational)
        >= policy["operational_failures_in_recent_five_rounds"]
    ):
        anomalies.append(
            {
                "code": "REPEATED_OPERATIONAL_FAILURES",
                "observed": len(recent_operational),
                "threshold": policy[
                    "operational_failures_in_recent_five_rounds"
                ],
            }
        )
    return anomalies


def maintenance_due(root: Path) -> dict[str, Any]:
    maintenance_state = load_maintenance_state(root)
    training_state = load_json(root / "training" / "state.json")
    ledger = load_learning_ledger(root)
    questions = ledger["first_blind_totals"]["questions"]
    release = load_json(
        root
        / "model-learning"
        / "releases"
        / f"{training_state['current_model_release']}.json"
    )
    active_rule_count = len(safe_active_rules(root, release))
    rows = _round_rows(root)
    first_blind_rows = [
        row for row in rows if row["evaluation_kind"] == "FIRST_BLIND"
    ]
    replay_effectiveness = build_replay_effectiveness(root)
    anomalies = _anomalies(
        root,
        first_blind_rows=first_blind_rows,
        replay_effectiveness=replay_effectiveness,
        active_rule_count=active_rule_count,
        current_round_count=training_state["round_count"],
    )
    short_milestone = (
        questions // SHORT_MAINTENANCE_INTERVAL_QUESTIONS
    ) * SHORT_MAINTENANCE_INTERVAL_QUESTIONS
    medium_milestone = (
        questions // MEDIUM_MAINTENANCE_INTERVAL_QUESTIONS
    ) * MEDIUM_MAINTENANCE_INTERVAL_QUESTIONS
    short_due = short_milestone > maintenance_state["last_short_milestone_questions"]
    medium_due = (
        medium_milestone > maintenance_state["last_medium_milestone_questions"]
    )
    last_anomaly = maintenance_state["last_anomaly_maintenance_questions"]
    anomaly_due = bool(anomalies) and (
        last_anomaly is None
        or questions - last_anomaly >= MAINTENANCE_ANOMALY_COOLDOWN_QUESTIONS
    )
    return {
        "due": short_due or medium_due or anomaly_due,
        "maintenance_type": (
            "MEDIUM"
            if medium_due
            else "SHORT"
            if short_due
            else "ANOMALY"
            if anomaly_due
            else None
        ),
        "first_blind_questions": questions,
        "short_milestone": short_milestone,
        "medium_milestone": medium_milestone,
        "short_due": short_due,
        "medium_due": medium_due,
        "anomaly_due": anomaly_due,
        "anomalies": anomalies,
        "first_blind_rows": first_blind_rows,
        "replay_effectiveness": replay_effectiveness,
        "active_rule_count": active_rule_count,
    }


def run_maintenance(root: Path, *, force: bool = False) -> dict[str, Any]:
    root = root.resolve()
    training_state = load_json(root / "training" / "state.json")
    if training_state.get("active_round_id") is not None or training_state.get(
        "status"
    ) not in {
        "READY_FOR_ROUND",
        "GROUP_COMPLETE",
        "FIRST_BLIND_COMPLETE_REPLAY_PENDING",
    }:
        raise TrainingError("maintenance may run only between closed rounds")
    due = maintenance_due(root)
    if not due["due"] and not force:
        return {
            "performed": False,
            "reason": "NO_MAINTENANCE_DUE",
            "first_blind_questions": due["first_blind_questions"],
        }
    state = load_maintenance_state(root)
    maintenance_id = f"MAINTENANCE-{state['next_maintenance_index']:03d}"
    maintenance_type = due["maintenance_type"] or "MANUAL"
    ledger = load_learning_ledger(root)
    recent_rows = _take_question_window(
        due["first_blind_rows"], MAINTENANCE_RECENT_WINDOW_QUESTIONS
    )
    previous_rows = _take_question_window(
        due["first_blind_rows"],
        MAINTENANCE_RECENT_WINDOW_QUESTIONS,
        from_end=sum(row["scoreable_question_count"] for row in recent_rows),
    )
    release = load_json(
        root
        / "model-learning"
        / "releases"
        / f"{training_state['current_model_release']}.json"
    )
    catalog = load_rule_catalog(root, release)
    ensure_learning_extensions(ledger, rule_ids=set(catalog))
    write_learning_ledger(root, ledger)
    governance = load_runtime_governance(root)
    suppressed = {
        row["rule_id"] for row in governance.get("suppressed_rules", [])
    }
    rule_status_counts: dict[str, int] = {}
    for evidence in ledger["rule_evidence"].values():
        status = evidence["status"]
        rule_status_counts[status] = rule_status_counts.get(status, 0) + 1
    remediation_type_counts: dict[str, int] = {}
    for relative_path in release.get("patches", []):
        patch = load_json(root / relative_path)
        if patch.get("schema") != "MODEL-LEARNING-PATCH-V3":
            continue
        remediation_type = patch["content"]["remediation_type"]
        remediation_type_counts[remediation_type] = (
            remediation_type_counts.get(remediation_type, 0) + 1
        )
    report = {
        "schema": "TRAINING-MAINTENANCE-REPORT-V2",
        "maintenance_id": maintenance_id,
        "maintenance_type": maintenance_type,
        "performed_at": utc_now(),
        "trigger": {
            key: due[key]
            for key in (
                "first_blind_questions",
                "short_milestone",
                "medium_milestone",
                "short_due",
                "medium_due",
                "anomaly_due",
                "anomalies",
            )
        },
        "training_statistics_unchanged": True,
        "counts_as_training_evidence": False,
        "canonical_sources_mutated": False,
        "metrics": {
            "all_first_blind": _aggregate(due["first_blind_rows"]),
            "recent_window": _aggregate(recent_rows),
            "previous_window": _aggregate(previous_rows),
            "ledger_totals": ledger["first_blind_totals"],
        },
        "rule_governance": {
            "catalog_rules": len(catalog),
            "status_counts": dict(sorted(rule_status_counts.items())),
            "suppressed_rule_count": len(suppressed),
            "suppressed_rules": governance.get("suppressed_rules", []),
            "runtime_active_rule_count": due["active_rule_count"],
            "duplicate_candidates": _duplicate_candidates(catalog, suppressed),
            "rule_selection": "TOPIC_ROUTER_MAXIMUM_SIX_MODEL_LEARNING_RULES_PER_QUESTION",
            "canonical_evidence_quota": None,
            "attribution": "DECISIVE_SUPPORTING_COUNTEREVIDENCE_WITH_DECISION_CHANGE",
            "remediation_type_counts": dict(
                sorted(remediation_type_counts.items())
            ),
            "only_new_general_rule_increases_catalog": True,
        },
        "confidence_calibration": {
            "historical_round_level_gap": _aggregate(due["first_blind_rows"])[
                "confidence_accuracy_gap"
            ],
            "future_question_level_ledger": ledger["confidence_calibration"],
            "unresolved_actor_time_or_endpoint_confidence_cap": 0.65,
        },
        "replay_effectiveness": due["replay_effectiveness"],
        "reasoning_degradation": _reasoning_quality_metrics(root),
        "operational_events_recent": _operational_events(root),
        "handoff_hardening": {
            "machine_generated_payload_template": True,
            "binding_values_copied_from_current_bundle": True,
            "prediction_rows_require_rule_attribution": True,
        },
        "next_due": {
            "short_at_first_blind_questions": (
                (due["first_blind_questions"] // SHORT_MAINTENANCE_INTERVAL_QUESTIONS)
                + 1
            )
            * SHORT_MAINTENANCE_INTERVAL_QUESTIONS,
            "medium_at_first_blind_questions": (
                (due["first_blind_questions"] // MEDIUM_MAINTENANCE_INTERVAL_QUESTIONS)
                + 1
            )
            * MEDIUM_MAINTENANCE_INTERVAL_QUESTIONS,
            "anomaly_monitoring": "AFTER_EVERY_CLOSED_ROUND_WITH_COOLDOWN",
        },
    }
    report_path = root / MAINTENANCE_REPORT_DIR / f"{maintenance_id}.json"
    exclusive_write_json(report_path, report)
    replay_effectiveness = due["replay_effectiveness"]
    atomic_write_json(root / REPLAY_EFFECTIVENESS_PATH, replay_effectiveness)
    if due["short_due"]:
        state["last_short_milestone_questions"] = due["short_milestone"]
    if due["medium_due"]:
        state["last_medium_milestone_questions"] = due["medium_milestone"]
        state["last_short_milestone_questions"] = max(
            state["last_short_milestone_questions"],
            due["medium_milestone"],
        )
    if due["anomaly_due"]:
        state["last_anomaly_maintenance_questions"] = due[
            "first_blind_questions"
        ]
    state["history"].append(
        {
            "maintenance_id": maintenance_id,
            "maintenance_type": maintenance_type,
            "first_blind_questions": due["first_blind_questions"],
            "report_path": report_path.relative_to(root).as_posix(),
            "report_sha256": object_sha256(report),
        }
    )
    state["next_maintenance_index"] += 1
    atomic_write_json(root / MAINTENANCE_STATE_PATH, state)
    return {
        "performed": True,
        "maintenance_id": maintenance_id,
        "maintenance_type": maintenance_type,
        "report_path": report_path.relative_to(root).as_posix(),
        "first_blind_questions": due["first_blind_questions"],
        "anomaly_codes": [row["code"] for row in due["anomalies"]],
        "runtime_active_rule_count": due["active_rule_count"],
        "suppressed_rule_count": len(suppressed),
    }


def validate_maintenance(root: Path, catalog: dict[str, dict[str, Any]]) -> dict[str, Any]:
    governance = load_runtime_governance(root)
    if (
        governance.get("schema") != "MODEL-RUNTIME-GOVERNANCE-V1"
        or governance.get("authority") != "AUTOMATED_TRAINING_MAINTENANCE"
        or governance.get("canonical_sources_mutated") is not False
    ):
        raise TrainingError("invalid model runtime governance")
    suppressed_rows = governance.get("suppressed_rules")
    if not isinstance(suppressed_rows, list):
        raise TrainingError("suppressed_rules must be a list")
    suppressed_ids: list[str] = []
    active_suppressed_ids: list[str] = []
    for row in suppressed_rows:
        if not isinstance(row, dict) or set(row) != {
            "rule_id",
            "replaced_by",
            "reason",
            "applied_in_maintenance",
        }:
            raise TrainingError("invalid suppressed rule record")
        if (
            row["rule_id"] == row["replaced_by"]
            or not isinstance(row["reason"], str)
            or not row["reason"].strip()
        ):
            raise TrainingError("invalid suppressed rule replacement")
        suppressed_ids.append(row["rule_id"])
        if row["rule_id"] in catalog and row["replaced_by"] in catalog:
            active_suppressed_ids.append(row["rule_id"])
    if len(suppressed_ids) != len(set(suppressed_ids)):
        raise TrainingError("duplicate suppressed rule")
    if set(active_suppressed_ids).intersection(
        row["replaced_by"]
        for row in suppressed_rows
        if row["replaced_by"] in catalog
    ):
        raise TrainingError("a replacement rule may not itself be suppressed")
    state = load_maintenance_state(root)
    if state.get("schema") != "TRAINING-MAINTENANCE-STATE-V1":
        raise TrainingError("invalid maintenance state schema")
    if (
        state.get("short_interval_first_blind_questions")
        != SHORT_MAINTENANCE_INTERVAL_QUESTIONS
        or state.get("medium_interval_first_blind_questions")
        != MEDIUM_MAINTENANCE_INTERVAL_QUESTIONS
    ):
        raise TrainingError("maintenance state interval mismatch")
    history = state.get("history")
    if not isinstance(history, list):
        raise TrainingError("maintenance history must be a list")
    for index, row in enumerate(history, start=1):
        if row.get("maintenance_id") != f"MAINTENANCE-{index:03d}":
            raise TrainingError("maintenance ids must be contiguous")
        report_path = root / row["report_path"]
        report = load_json(report_path)
        if (
            report.get("maintenance_id") != row["maintenance_id"]
            or object_sha256(report) != row["report_sha256"]
            or report.get("counts_as_training_evidence") is not False
            or report.get("canonical_sources_mutated") is not False
        ):
            raise TrainingError("maintenance report binding mismatch")
    if state.get("next_maintenance_index") != len(history) + 1:
        raise TrainingError("maintenance next index mismatch")
    return {
        "status": "PASS",
        "maintenance_runs": len(history),
        "suppressed_rule_count": len(active_suppressed_ids),
        "next_short_milestone": (
            state["last_short_milestone_questions"]
            + SHORT_MAINTENANCE_INTERVAL_QUESTIONS
        ),
        "next_medium_milestone": (
            state["last_medium_milestone_questions"]
            + MEDIUM_MAINTENANCE_INTERVAL_QUESTIONS
        ),
    }

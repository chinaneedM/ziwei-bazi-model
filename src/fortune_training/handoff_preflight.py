from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .learning import load_learning_ledger, suppressed_rule_ids
from .util import TrainingError


CONFIDENCE_COMPONENT_FIELDS = {
    "input_confidence",
    "natal_structure_confidence",
    "subject_confidence",
    "mechanism_confidence",
    "timing_confidence",
    "reality_endpoint_confidence",
    "cross_track_agreement",
    "top1_top2_separation",
    "overall_confidence",
}

REPLAY_REMEDIATION_ALIASES = {
    "EXECUTION_GATE_AND_RULE_WEIGHT_CHANGE": {
        "primary": "EXECUTION_GATE",
        "secondary": ["RULE_WEIGHT_CHANGE"],
    },
}

PROFILE_TAG_ALIASES = {
    "subject_tags": {
        "HOUSEHOLD_UNIT": "FAMILY",
        "FRIEND": "FRIEND_BUSINESS_PARTNER",
        "COWORKER": "EXTERNAL_ACTOR",
    },
    "time_scope_tags": {
        "LIFE_STAGE": "ADULTHOOD",
        "MULTI_YEAR_SEQUENCE": "MULTI_YEAR_PERIOD",
    },
    "endpoint_tags": {
        "SURGERY": "HEALTH_CONDITION",
    },
}

NATAL_CHART_FACT_MARKERS = ("本命", "原局", "原有", "原结构")
ZIWEI_STATIC_STAR_MARKERS = (
    "紫微",
    "天机",
    "太阳",
    "武曲",
    "天同",
    "廉贞",
    "天府",
    "太阴",
    "贪狼",
    "巨门",
    "天相",
    "天梁",
    "七杀",
    "破军",
    "左辅",
    "右弼",
    "文昌",
    "文曲",
    "禄存",
    "天马",
    "擎羊",
    "陀罗",
    "火星",
    "铃星",
    "地空",
    "地劫",
    "天刑",
    "年解",
)


def _normalize_confidence(value: Any, path: str) -> tuple[Any, dict[str, Any] | None]:
    if isinstance(value, float) and not isinstance(value, bool) and 0 <= value <= 1:
        normalized = int(round(value * 100))
        return normalized, {
            "kind": "CONFIDENCE_FRACTION_TO_PERCENT",
            "path": path,
            "from": value,
            "to": normalized,
        }
    return value, None


def _contains_explicit_natal_structure(evidence_row: dict[str, Any]) -> bool:
    chart_fact = evidence_row.get("chart_fact")
    if not isinstance(chart_fact, str):
        return False
    if any(marker in chart_fact for marker in NATAL_CHART_FACT_MARKERS):
        return True
    if evidence_row.get("track") != "ZIWEI":
        return False
    matched_stars = {
        marker for marker in ZIWEI_STATIC_STAR_MARKERS if marker in chart_fact
    }
    return len(matched_stars) >= 2


def normalize_handoff(
    root: Path,
    handoff: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Normalize safe machine-contract details without changing Top1 or Top2."""
    if not isinstance(handoff, dict):
        raise TrainingError("handoff must be a JSON object")
    normalized = copy.deepcopy(handoff)
    changes: list[dict[str, Any]] = []

    ledger = load_learning_ledger(root.resolve())
    suppressed = suppressed_rule_ids(root.resolve())
    rule_evidence = ledger.get("rule_evidence", {})
    attributed_evidence = ledger.get("attributed_rule_evidence", {})

    predictions = normalized.get("predictions")
    if not isinstance(predictions, list):
        return normalized, {
            "schema": "HANDOFF-PREFLIGHT-REPORT-V1",
            "changed": False,
            "changes": [],
        }

    replay_remediation = normalized.get("replay_remediation")
    if isinstance(replay_remediation, dict):
        remediation_type = replay_remediation.get("remediation_type")
        alias = REPLAY_REMEDIATION_ALIASES.get(remediation_type)
        if alias:
            replay_remediation["remediation_type"] = alias["primary"]
            changes.append(
                {
                    "kind": "REPLAY_REMEDIATION_ALIAS_TO_PRIMARY",
                    "from": remediation_type,
                    "to": alias["primary"],
                    "secondary_types": alias["secondary"],
                }
            )

    for index, row in enumerate(predictions):
        if not isinstance(row, dict):
            continue
        question_id = row.get("question_id", f"index-{index}")

        for track_field in ("ziwei_track_seal", "bazi_track_seal"):
            track = row.get(track_field)
            if not isinstance(track, dict) or "confidence" not in track:
                continue
            path = f"predictions.{question_id}.{track_field}.confidence"
            value, change = _normalize_confidence(track["confidence"], path)
            track["confidence"] = value
            if change:
                changes.append(change)

        components = row.get("confidence_components")
        if isinstance(components, dict):
            for field in CONFIDENCE_COMPONENT_FIELDS:
                if field not in components:
                    continue
                path = f"predictions.{question_id}.confidence_components.{field}"
                value, change = _normalize_confidence(components[field], path)
                components[field] = value
                if change:
                    changes.append(change)

        top1 = row.get("top1")
        semantics = row.get("question_semantic_model")
        matrix = row.get("option_comparison_matrix")
        evidence = row.get("evidence_ledger")
        if (
            isinstance(top1, str)
            and isinstance(semantics, dict)
            and isinstance(matrix, dict)
            and isinstance(evidence, list)
        ):
            option_atoms = semantics.get("option_atoms")
            matrix_options = matrix.get("options")
            if isinstance(option_atoms, dict) and isinstance(matrix_options, dict):
                top1_atoms = option_atoms.get(top1)
                top1_matrix = matrix_options.get(top1)
                severe_atoms = (
                    top1_atoms.get("severe_irreversible_or_high_precision_atoms")
                    if isinstance(top1_atoms, dict)
                    else None
                )
                supporting_evidence_ids = [
                    evidence_row.get("evidence_id")
                    for evidence_row in evidence
                    if isinstance(evidence_row, dict)
                    and evidence_row.get("independence_status") == "INDEPENDENT"
                    and isinstance(evidence_row.get("supports_option_atoms"), list)
                    and any(
                        isinstance(atom_ref, str)
                        and atom_ref.startswith(f"{top1}:")
                        for atom_ref in evidence_row["supports_option_atoms"]
                    )
                ]
                if (
                    isinstance(severe_atoms, list)
                    and severe_atoms
                    and isinstance(top1_matrix, dict)
                    and top1_matrix.get(
                        "severe_atoms_have_independent_evidence"
                    )
                    is False
                    and supporting_evidence_ids
                ):
                    top1_matrix["severe_atoms_have_independent_evidence"] = True
                    changes.append(
                        {
                            "kind": "TOP1_PRECISION_SUPPORT_FLAG_DERIVED",
                            "question_id": question_id,
                            "top1": top1,
                            "supporting_evidence_ids": supporting_evidence_ids,
                        }
                    )

        if isinstance(evidence, list) and not any(
            isinstance(evidence_row, dict)
            and evidence_row.get("layer") in {"NATAL", "REALITY"}
            and evidence_row.get("decision_impact") != "NEUTRAL"
            for evidence_row in evidence
        ):
            for evidence_row in evidence:
                if not isinstance(evidence_row, dict):
                    continue
                chart_fact = evidence_row.get("chart_fact")
                if (
                    evidence_row.get("layer") in {"YEAR", "MONTH"}
                    and evidence_row.get("decision_impact") != "NEUTRAL"
                    and _contains_explicit_natal_structure(evidence_row)
                ) or (
                    evidence_row.get("layer") == "PERIOD"
                    and evidence_row.get("decision_impact") != "NEUTRAL"
                    and _contains_explicit_natal_structure(evidence_row)
                ):
                    previous_layer = evidence_row["layer"]
                    evidence_row["layer"] = "NATAL"
                    changes.append(
                        {
                            "kind": "MIXED_STATIC_TIMING_EVIDENCE_LAYER_TO_NATAL",
                            "question_id": question_id,
                            "evidence_id": evidence_row.get("evidence_id"),
                            "from": previous_layer,
                            "to": "NATAL",
                        }
                    )
                    break

        if isinstance(evidence, list):
            evidence_tracks = {
                evidence_row.get("evidence_id"): evidence_row.get("track")
                for evidence_row in evidence
                if isinstance(evidence_row, dict)
                and isinstance(evidence_row.get("evidence_id"), str)
            }
            for track_field, expected_track in (
                ("ziwei_track_seal", "ZIWEI"),
                ("bazi_track_seal", "BAZI"),
            ):
                track_seal = row.get(track_field)
                if not isinstance(track_seal, dict):
                    continue
                for evidence_field in (
                    "supporting_evidence_ids",
                    "contradicting_evidence_ids",
                ):
                    evidence_ids = track_seal.get(evidence_field)
                    if not isinstance(evidence_ids, list):
                        continue
                    removed_ids = [
                        evidence_id
                        for evidence_id in evidence_ids
                        if evidence_tracks.get(evidence_id) != expected_track
                    ]
                    if removed_ids:
                        track_seal[evidence_field] = [
                            evidence_id
                            for evidence_id in evidence_ids
                            if evidence_id not in removed_ids
                        ]
                        changes.append(
                            {
                                "kind": "CROSS_TRACK_SEAL_EVIDENCE_REMOVED",
                                "question_id": question_id,
                                "track": expected_track,
                                "field": evidence_field,
                                "evidence_ids": removed_ids,
                            }
                        )

        counterfactual = row.get("counterfactual_analysis")
        if isinstance(counterfactual, dict):
            full_ranking = counterfactual.get("full_model_ranking")
            ablations = counterfactual.get("decisive_rule_ablations")
            if isinstance(ablations, list):
                for ablation in ablations:
                    if not isinstance(ablation, dict):
                        continue
                    if (
                        "top1_changes" in ablation
                        and "changes_top1" not in ablation
                    ):
                        previous_value = ablation.pop("top1_changes")
                        ablation["changes_top1"] = previous_value
                        changes.append(
                            {
                                "kind": "RULE_ABLATION_FIELD_ALIAS",
                                "question_id": question_id,
                                "rule_id": ablation.get("rule_id"),
                                "from": "top1_changes",
                                "to": "changes_top1",
                            }
                        )
                    ranking_without_rule = ablation.get("ranking_without_rule")
                    if (
                        not ablation.get("reason")
                        and isinstance(full_ranking, list)
                        and full_ranking
                        and isinstance(ranking_without_rule, list)
                        and ranking_without_rule
                    ):
                        ablation["reason"] = (
                            "Removing the declared decisive rule changes Top1 "
                            f"from {full_ranking[0]} to {ranking_without_rule[0]}."
                        )
                        changes.append(
                            {
                                "kind": "RULE_ABLATION_REASON_DERIVED",
                                "question_id": question_id,
                                "rule_id": ablation.get("rule_id"),
                                "top1_before": full_ranking[0],
                                "top1_after": ranking_without_rule[0],
                            }
                        )

        profile = row.get("question_profile")
        attribution = row.get("rule_attribution")
        if isinstance(profile, dict) and isinstance(evidence, list):
            declared_routes = profile.get("source_routes")
            if isinstance(declared_routes, list):
                missing_routes: list[str] = []
                for evidence_row in evidence:
                    if not isinstance(evidence_row, dict):
                        continue
                    source_route = evidence_row.get("source_route")
                    if (
                        isinstance(source_route, str)
                        and source_route in {f"S{route:02d}" for route in range(20)}
                        and source_route not in declared_routes
                        and source_route not in missing_routes
                    ):
                        missing_routes.append(source_route)
                if missing_routes:
                    profile["source_routes"] = declared_routes + missing_routes
                    changes.append(
                        {
                            "kind": "EVIDENCE_SOURCE_ROUTES_DECLARED",
                            "question_id": question_id,
                            "source_routes": missing_routes,
                        }
                    )
        if not isinstance(profile, dict) or not isinstance(attribution, dict):
            continue
        for field, aliases in PROFILE_TAG_ALIASES.items():
            values = profile.get(field)
            if not isinstance(values, list):
                continue
            normalized_values: list[Any] = []
            for value in values:
                normalized_value = aliases.get(value, value)
                if normalized_value not in normalized_values:
                    normalized_values.append(normalized_value)
                if normalized_value != value:
                    changes.append(
                        {
                            "kind": "PROFILE_TAG_ALIAS",
                            "question_id": question_id,
                            "field": field,
                            "from": value,
                            "to": normalized_value,
                        }
                    )
            profile[field] = normalized_values
        applied = profile.get("applied_rule_ids")
        if not isinstance(applied, list):
            continue

        attributed_rule_ids: list[str] = []
        for field in (
            "decisive_rule_ids",
            "supporting_rule_ids",
            "counterevidence_rule_ids",
        ):
            values = attribution.get(field)
            if not isinstance(values, list):
                continue
            for rule_id in values:
                if isinstance(rule_id, str) and rule_id not in attributed_rule_ids:
                    attributed_rule_ids.append(rule_id)
        missing_applied = [
            rule_id for rule_id in attributed_rule_ids if rule_id not in applied
        ]
        if missing_applied:
            applied = applied + missing_applied
            profile["applied_rule_ids"] = applied
            changes.append(
                {
                    "kind": "ATTRIBUTED_RULES_DECLARED_AS_APPLIED",
                    "question_id": question_id,
                    "rule_ids": missing_applied,
                }
            )

        for rule_id in applied:
            evidence_status = rule_evidence.get(rule_id, {}).get("status")
            attributed_status = attributed_evidence.get(rule_id, {}).get("status")
            if (
                rule_id in suppressed
                or evidence_status == "RETIRED"
                or attributed_status == "RETIRED"
            ):
                raise TrainingError(
                    f"retired or suppressed rule must be removed before handoff: {rule_id}"
                )

        challenged = {
            rule_id
            for rule_id in applied
            if rule_evidence.get(rule_id, {}).get("status") == "CHALLENGED"
            or attributed_evidence.get(rule_id, {}).get("status") == "CHALLENGED"
        }
        moved: list[str] = []
        for field in ("decisive_rule_ids", "supporting_rule_ids"):
            values = attribution.get(field)
            if not isinstance(values, list):
                continue
            retained = [rule_id for rule_id in values if rule_id not in challenged]
            moved.extend(rule_id for rule_id in values if rule_id in challenged)
            attribution[field] = retained
        if moved:
            counter = attribution.get("counterevidence_rule_ids")
            if not isinstance(counter, list):
                counter = []
            attribution["counterevidence_rule_ids"] = sorted(set(counter) | set(moved))
            attribution["decision_changed"] = bool(attribution.get("decisive_rule_ids"))
            counterfactual = row.get("counterfactual_analysis")
            if isinstance(counterfactual, dict) and isinstance(
                counterfactual.get("decisive_rule_ablations"), list
            ):
                counterfactual["decisive_rule_ablations"] = [
                    ablation
                    for ablation in counterfactual["decisive_rule_ablations"]
                    if not isinstance(ablation, dict)
                    or ablation.get("rule_id") not in challenged
                ]
            changes.append(
                {
                    "kind": "CHALLENGED_RULE_TO_COUNTEREVIDENCE",
                    "question_id": question_id,
                    "rule_ids": sorted(set(moved)),
                }
            )

        classified: set[str] = set()
        for field in (
            "decisive_rule_ids",
            "supporting_rule_ids",
            "counterevidence_rule_ids",
        ):
            values = attribution.get(field)
            if isinstance(values, list):
                classified.update(values)
        missing = [rule_id for rule_id in applied if rule_id not in classified]
        if missing:
            supporting = attribution.get("supporting_rule_ids")
            counter = attribution.get("counterevidence_rule_ids")
            if not isinstance(supporting, list):
                supporting = []
            if not isinstance(counter, list):
                counter = []
            supporting_missing = [
                rule_id for rule_id in missing if rule_id not in challenged
            ]
            counter_missing = [
                rule_id for rule_id in missing if rule_id in challenged
            ]
            attribution["supporting_rule_ids"] = supporting + supporting_missing
            attribution["counterevidence_rule_ids"] = counter + counter_missing
            changes.append(
                {
                    "kind": "MISSING_RULE_ATTRIBUTION_CLASSIFIED",
                    "question_id": question_id,
                    "supporting_rule_ids": supporting_missing,
                    "counterevidence_rule_ids": counter_missing,
                }
            )

    return normalized, {
        "schema": "HANDOFF-PREFLIGHT-REPORT-V1",
        "changed": bool(changes),
        "changes": changes,
    }

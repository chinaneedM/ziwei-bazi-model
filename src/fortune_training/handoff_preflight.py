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

        profile = row.get("question_profile")
        attribution = row.get("rule_attribution")
        if not isinstance(profile, dict) or not isinstance(attribution, dict):
            continue
        applied = profile.get("applied_rule_ids")
        if not isinstance(applied, list):
            continue

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

    return normalized, {
        "schema": "HANDOFF-PREFLIGHT-REPORT-V1",
        "changed": bool(changes),
        "changes": changes,
    }

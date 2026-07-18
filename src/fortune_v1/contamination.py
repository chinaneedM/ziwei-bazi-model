from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .util import (
    FortuneError,
    atomic_write_json,
    canonical_bytes,
    read_json,
    sha256_bytes,
    sha256_file,
    utc_now,
)

CONTAMINATION_POLICY_SCHEMA = "FORTUNE-RUNTIME-CONTAMINATION-POLICY-V1"
CONTAMINATION_INVENTORY_SCHEMA = "FORTUNE-LEGACY-CONTAMINATION-INVENTORY-V1"
CONTAMINATION_VALIDATION_SCHEMA = "FORTUNE-RUNTIME-CONTAMINATION-VALIDATION-V1"

LIFECYCLE_STATUSES = {
    "ACTIVE",
    "DEPRECATED",
    "QUARANTINED",
    "HISTORICAL_AUDIT_ONLY",
    "RESEARCH_ONLY",
    "ANSWER_CONTAMINATED",
    "SUPERSEDED",
    "REJECTED",
}

_ALLOWED_KNOWLEDGE = re.compile(r"(?:^|/)knowledge/(?:base|candidates|releases)(?:/|$)", re.I)
_ALLOWED_METHOD = re.compile(r"(?:^|/)method/(?:base|candidates|releases)(?:/|$)", re.I)
_ALLOWED_MODEL = re.compile(r"(?:^|/)model/(?:base|candidates|releases)(?:/|$)", re.I)

# These are repository/runtime path classes, not semantic keyword scans. Historical
# material is preserved, but a reference to it is ineligible in a prediction packet.
_FORBIDDEN_RULES: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    ("PROJECT_UPLOAD_REFERENCE", "ANSWER_CONTAMINATED", re.compile(r"(?:^|/)mnt/data(?:/|$)|file_[0-9a-f]{16,}|project[_ -]?upload", re.I)),
    ("ANSWER_VAULT_REFERENCE", "ANSWER_CONTAMINATED", re.compile(r"(?:^|/)(?:answer-vault|answer_vault|ground-truth|ground_truth)(?:/|$)", re.I)),
    ("SHADOW_REBUILD_REFERENCE", "QUARANTINED", re.compile(r"(?:^|/)(?:shadow-rebuild|shadow_rebuild)(?:/|$)", re.I)),
    ("POSTREVEAL_REFERENCE", "HISTORICAL_AUDIT_ONLY", re.compile(r"(?:^|/)[^/]*(?:postreveal|post-reveal|revealed-case|revealed_case)[^/]*(?:/|$)", re.I)),
    ("HISTORICAL_REPORT_REFERENCE", "HISTORICAL_AUDIT_ONLY", re.compile(r"(?:^|/)reports(?:/|$)", re.I)),
    ("TRAINING_STATE_REFERENCE", "HISTORICAL_AUDIT_ONLY", re.compile(r"(?:^|/)data/training(?:/|$)", re.I)),
    ("RESEARCH_HYPOTHESIS_REFERENCE", "RESEARCH_ONLY", re.compile(r"(?:^|/)research/fortune-hypothesis-library(?:/|$)", re.I)),
)


def _normalize(value: str | Path) -> str:
    return str(value).replace("\\", "/").strip()


def _object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    return sha256_bytes(canonical_bytes(body))


def classify_repository_path(value: str | Path) -> dict[str, Any]:
    normalized = _normalize(value)
    lowered = normalized.lower()
    for rule_id, lifecycle_status, pattern in _FORBIDDEN_RULES:
        if pattern.search(lowered):
            return {
                "path": normalized,
                "classification": rule_id,
                "lifecycle_status": lifecycle_status,
                "runtime_eligibility": "PROHIBITED",
                "packet_eligibility": "PROHIBITED",
                "score_eligibility": "PROHIBITED",
            }
    if _ALLOWED_KNOWLEDGE.search(lowered):
        classification = "VERSIONED_KNOWLEDGE_OBJECT"
    elif _ALLOWED_METHOD.search(lowered):
        classification = "VERSIONED_METHOD_OBJECT"
    elif _ALLOWED_MODEL.search(lowered):
        classification = "VERSIONED_MODEL_OBJECT"
    else:
        classification = "CONTROL_PLANE_OR_UNCLASSIFIED_OBJECT"
    return {
        "path": normalized,
        "classification": classification,
        "lifecycle_status": "ACTIVE" if classification.startswith("VERSIONED_") else "DEPRECATED",
        "runtime_eligibility": "ELIGIBLE_WHEN_FROZEN_AND_HASH_BOUND" if classification.startswith("VERSIONED_") else "CONTROL_PLANE_ONLY",
        "packet_eligibility": "ELIGIBLE_WHEN_FROZEN_AND_HASH_BOUND" if classification.startswith("VERSIONED_") else "NOT_A_KNOWLEDGE_OR_METHOD_SOURCE",
        "score_eligibility": "CONDITIONAL" if classification.startswith("VERSIONED_") else "NO_DIRECT_SCORE_ROLE",
    }


def assert_knowledge_source_path(value: str | Path) -> None:
    classification = classify_repository_path(value)
    normalized = _normalize(value)
    if classification["runtime_eligibility"] == "PROHIBITED":
        raise FortuneError(
            f"knowledge source path is quarantined: {normalized}",
            status="KNOWLEDGE_SOURCE_PATH_QUARANTINED",
        )
    if not _ALLOWED_KNOWLEDGE.search(normalized.lower()):
        raise FortuneError(
            f"knowledge source path is outside versioned knowledge roots: {normalized}",
            status="KNOWLEDGE_SOURCE_PATH_INELIGIBLE",
        )


def runtime_reference_violations(value: Any, path: str = "$") -> list[dict[str, str]]:
    violations: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            violations.extend(runtime_reference_violations(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            violations.extend(runtime_reference_violations(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        normalized = _normalize(value)
        lowered = normalized.lower()
        looks_like_reference = "/" in normalized or "\\" in normalized or lowered.startswith("file_")
        if not looks_like_reference:
            return violations
        for rule_id, lifecycle_status, pattern in _FORBIDDEN_RULES:
            if pattern.search(lowered):
                violations.append({
                    "object_path": path,
                    "value": normalized,
                    "rule_id": rule_id,
                    "lifecycle_status": lifecycle_status,
                })
                break
    return violations


def validate_runtime_object(input_path: str | Path, output: str | Path | None = None) -> dict[str, Any]:
    body = read_json(input_path)
    violations = runtime_reference_violations(body)
    receipt = {
        "schema": CONTAMINATION_VALIDATION_SCHEMA,
        "input_path": Path(input_path).as_posix(),
        "input_sha256": sha256_file(input_path),
        "status": "PASS" if not violations else "FAIL_CLOSED",
        "runtime_eligibility": "ELIGIBLE" if not violations else "PROHIBITED",
        "score_eligibility": "CONDITIONAL" if not violations else "PROHIBITED",
        "violation_count": len(violations),
        "violations": violations,
        "validated_at": utc_now(),
    }
    receipt["object_hash"] = _object_hash(receipt)
    if output:
        atomic_write_json(output, receipt, overwrite=True)
    return receipt


def build_contamination_inventory(repository_root: str | Path, output: str | Path) -> dict[str, Any]:
    root = Path(repository_root)
    rows: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for file_path in sorted(path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts):
        relative = file_path.relative_to(root).as_posix()
        classification = classify_repository_path(relative)
        row = {
            "path": relative,
            "sha256": sha256_file(file_path),
            "size_bytes": file_path.stat().st_size,
            **{key: value for key, value in classification.items() if key != "path"},
        }
        rows.append(row)
        counts[row["lifecycle_status"]] = counts.get(row["lifecycle_status"], 0) + 1
    body = {
        "schema": CONTAMINATION_INVENTORY_SCHEMA,
        "repository_root": root.as_posix(),
        "file_count": len(rows),
        "status_counts": counts,
        "rows": rows,
        "policy": {
            "historical_deletion_required": False,
            "historical_mutation_permission": "NO",
            "activity_removal_rule": "PROHIBITED_OBJECTS_MUST_BE_ABSENT_FROM_PACKETS_AND_RUNTIME_REFERENCES",
            "physical_separation_rule": "ANSWER_AND_POSTREVEAL_MATERIAL_MUST_NOT_BE_VISIBLE_TO_BLIND_RUNTIME",
        },
        "created_at": utc_now(),
    }
    body["object_hash"] = _object_hash(body)
    atomic_write_json(output, body, overwrite=True)
    return body

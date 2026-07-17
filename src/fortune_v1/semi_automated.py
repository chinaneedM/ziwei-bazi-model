from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

CHAT_PACKET_SCHEMA = "CHAT-PROFESSIONAL-PACKET-V1"
CHAT_OUTPUT_SCHEMA = "CHAT-PROFESSIONAL-OUTPUT-V1"
VALIDATION_SCHEMA = "CHAT-OUTPUT-VALIDATION-V1"

NODE_IDS = (
    "01_INPUT_FREEZE",
    "02_QUESTION_SEMANTICS",
    "03_ZIWEI_BLIND_MODEL",
    "04_BAZI_BLIND_MODEL",
    "05_SOURCE_CALL_LEDGER",
    "06_REALITY_CHAIN",
    "07_DIRECTION_MATRIX",
    "08_PAIRWISE_SELECTION",
    "09_LOCAL_SEAL_AND_FUSION",
)

FORBIDDEN_CASE_KEYS = {
    "answers",
    "answer",
    "correct_answer",
    "answer_key",
    "reveal",
    "grading",
    "diagnosis",
    "shadow_rebuild",
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str
    severity: str = "REPAIRABLE_FAILURE"

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "path": self.path,
            "message": self.message,
            "severity": self.severity,
        }


def _assert_no_forbidden_keys(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower()
            if normalized in FORBIDDEN_CASE_KEYS:
                raise FortuneError(
                    f"forbidden answer-bearing key at {path}.{key}",
                    status="CHAT_PACKET_ANSWER_ISOLATION_FAILED",
                )
            _assert_no_forbidden_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_forbidden_keys(child, f"{path}[{index}]")


def _exact_allowed_paths(clean_start: dict[str, Any]) -> set[str]:
    policy = clean_start.get("retrieval_policy", {})
    if policy.get("mode") != "EXACT_PATH_ONLY":
        raise FortuneError("clean start is not exact-path-only", status="CLEAN_START_POLICY_INVALID")
    if policy.get("repository_search_allowed") is not False:
        raise FortuneError("repository search must be disabled", status="CLEAN_START_POLICY_INVALID")
    if policy.get("history_navigation_allowed") is not False:
        raise FortuneError("history navigation must be disabled", status="CLEAN_START_POLICY_INVALID")
    return {str(Path(row)) for row in policy.get("exact_allowed_paths", [])}


def _professional_output_template(case: dict[str, Any]) -> dict[str, Any]:
    questions = []
    for question in case["questions"]["parsed"]:
        option_ids = [row["option_id"] for row in question["options"]]
        questions.append(
            {
                "question_id": question["question_id"],
                "option_ids": option_ids,
                "option_order": [],
                "top1": None,
                "top2": None,
                "confidence": None,
                "blind_core": None,
                "public_evidence": [],
                "strongest_competitor_reason": None,
                "most_important_unverified_atom": None,
                "formal_exact_assertion": None,
                "ziwei": {
                    "blind_model": None,
                    "support": [],
                    "counterevidence": [],
                    "limits": [],
                    "unknowns": [],
                    "native_parent_ids": [],
                },
                "bazi": {
                    "blind_model": None,
                    "support": [],
                    "counterevidence": [],
                    "limits": [],
                    "unknowns": [],
                    "native_parent_ids": [],
                    "variant_status": None,
                },
                "evidence_ledger": [],
                "direction_matrix": {option_id: [] for option_id in option_ids},
                "compound_coverage": {option_id: {} for option_id in option_ids},
            }
        )
    return {
        "schema": CHAT_OUTPUT_SCHEMA,
        "case_id": case["case_id"],
        "questions": questions,
        "status": "INCOMPLETE_CHAT_PROFESSIONAL_OUTPUT",
    }


def prepare_chat_packets(clean_start_path: str | Path, output_root: str | Path) -> dict[str, Any]:
    clean_start_file = Path(clean_start_path)
    clean = read_json(clean_start_file)
    if clean.get("schema") != "GROUP-CLEAN-START-V1":
        raise FortuneError("wrong clean-start schema", status="CLEAN_START_SCHEMA_INVALID")
    if clean.get("status") != "READY_FOR_CLEAN_GROUP_PREDICTION":
        raise FortuneError("group is not ready for prediction", status="GROUP_NOT_READY")
    if clean.get("answer_data_available") is not False:
        raise FortuneError("answer data is available", status="GROUP_ANSWER_ISOLATION_FAILED")

    allowed = _exact_allowed_paths(clean)
    output_dir = Path(output_root) / slug(clean["group_run_id"])
    if output_dir.exists():
        raise FortuneError("chat packet output already exists", status="CHAT_PACKET_NONOVERWRITE_FAILED")
    output_dir.mkdir(parents=True, exist_ok=False)

    rows: list[dict[str, Any]] = []
    for case_row in clean["cases"]:
        case_path = str(Path(case_row["input_path"]))
        if case_path not in allowed:
            raise FortuneError("case input is outside exact whitelist", status="CHAT_PACKET_PATH_NOT_ALLOWED")
        case_file = Path(case_path)
        if sha256_file(case_file) != case_row["input_sha256"]:
            raise FortuneError("case input hash mismatch", status="CHAT_PACKET_INPUT_HASH_MISMATCH")
        case = read_json(case_file)
        if case.get("answer_isolation", {}).get("answer_payload_present") is not False:
            raise FortuneError("case answer isolation failed", status="CASE_ANSWER_ISOLATION_FAILED")
        _assert_no_forbidden_keys(case)

        packet = {
            "schema": CHAT_PACKET_SCHEMA,
            "group_id": clean["group_id"],
            "group_run_id": clean["group_run_id"],
            "case_id": case["case_id"],
            "cold_start": True,
            "answer_data_available": False,
            "input_snapshot": {
                "path": case_path,
                "sha256": case_row["input_sha256"],
            },
            "binding": case["binding"],
            "case_payload": case,
            "professional_output_template": _professional_output_template(case),
            "execution_contract": {
                "model_role": "PROFESSIONAL_REASONING_ONLY",
                "repository_search_allowed": False,
                "history_navigation_allowed": False,
                "answer_access_allowed": False,
                "mechanical_hashing_by_model_required": False,
                "mechanical_pairwise_generation_by_model_required": False,
                "node_order": list(NODE_IDS),
            },
            "created_at": utc_now(),
        }
        packet_path = output_dir / f"{case['case_id']}.chat-packet.json"
        atomic_write_json(packet_path, packet)
        rows.append(
            {
                "case_id": case["case_id"],
                "packet_path": str(packet_path),
                "packet_sha256": sha256_file(packet_path),
            }
        )

    manifest = {
        "schema": "CHAT-PROFESSIONAL-PACKET-MANIFEST-V1",
        "group_id": clean["group_id"],
        "group_run_id": clean["group_run_id"],
        "clean_start_path": str(clean_start_file),
        "clean_start_sha256": sha256_file(clean_start_file),
        "case_count": len(rows),
        "packets": rows,
        "status": "READY_FOR_CHAT_PROFESSIONAL_REASONING",
        "created_at": utc_now(),
    }
    manifest_path = output_dir / "manifest.json"
    atomic_write_json(manifest_path, manifest)
    return {**manifest, "manifest_path": str(manifest_path), "manifest_sha256": sha256_file(manifest_path)}


def classify_visibility_event(
    *,
    operation_attempted: bool,
    returned_payload_visible: bool,
    forbidden_content_visible: bool,
    answer_bearing_content_visible: bool,
) -> dict[str, Any]:
    if answer_bearing_content_visible:
        status = "FAIL_CLOSED_CONTAMINATED"
        severity = "ANSWER_BEARING_CONTENT_VISIBLE"
    elif forbidden_content_visible:
        status = "FAIL_CLOSED_CONTAMINATED"
        severity = "FORBIDDEN_CONTENT_VISIBLE"
    elif returned_payload_visible:
        status = "POLICY_VIOLATION_REPAIRABLE"
        severity = "NONANSWER_PAYLOAD_VISIBLE"
    elif operation_attempted:
        status = "OPERATION_ATTEMPT_RECORDED_NO_CONTAMINATION"
        severity = "NO_CONTENT_VISIBLE"
    else:
        status = "NO_EVENT"
        severity = "NONE"
    return {
        "schema": "VISIBILITY-EVENT-CLASSIFICATION-V1",
        "operation_attempted": operation_attempted,
        "returned_payload_visible": returned_payload_visible,
        "forbidden_content_visible": forbidden_content_visible,
        "answer_bearing_content_visible": answer_bearing_content_visible,
        "status": status,
        "visibility_class": severity,
        "restart_required": status == "FAIL_CLOSED_CONTAMINATED",
    }


def _pairwise_rows(option_order: list[str]) -> list[dict[str, Any]]:
    rank = {option_id: index for index, option_id in enumerate(option_order)}
    rows = []
    for left_index, left in enumerate(option_order):
        for right in option_order[left_index + 1 :]:
            rows.append(
                {
                    "left": left,
                    "right": right,
                    "winner": left if rank[left] < rank[right] else right,
                    "decision_basis": "MECHANICALLY_DERIVED_FROM_COMPLETE_OPTION_ORDER",
                }
            )
    return rows


def _validate_question(expected: dict[str, Any], actual: dict[str, Any], path: str) -> tuple[list[ValidationIssue], dict[str, Any]]:
    issues: list[ValidationIssue] = []
    expected_options = [row["option_id"] for row in expected["options"]]
    option_order = actual.get("option_order")
    if not isinstance(option_order, list) or sorted(option_order) != sorted(expected_options):
        issues.append(ValidationIssue("OPTION_ORDER_INVALID", f"{path}.option_order", "must contain every option exactly once"))
        option_order = []
    if option_order:
        if actual.get("top1") != option_order[0]:
            issues.append(ValidationIssue("TOP1_ORDER_MISMATCH", f"{path}.top1", "top1 must equal option_order[0]"))
        if len(option_order) > 1 and actual.get("top2") != option_order[1]:
            issues.append(ValidationIssue("TOP2_ORDER_MISMATCH", f"{path}.top2", "top2 must equal option_order[1]"))
    if not actual.get("blind_core"):
        issues.append(ValidationIssue("BLIND_CORE_MISSING", f"{path}.blind_core", "blind core is required"))
    if not actual.get("strongest_competitor_reason"):
        issues.append(ValidationIssue("STRONGEST_COMPETITOR_MISSING", f"{path}.strongest_competitor_reason", "strongest competitor reason is required"))
    if not actual.get("most_important_unverified_atom"):
        issues.append(ValidationIssue("UNVERIFIED_ATOM_MISSING", f"{path}.most_important_unverified_atom", "most important unverified atom is required"))

    public_evidence = actual.get("public_evidence", [])
    if not isinstance(public_evidence, list) or len(public_evidence) < 3:
        issues.append(ValidationIssue("PUBLIC_EVIDENCE_MINIMUM_NOT_MET", f"{path}.public_evidence", "at least three non-duplicate public evidence components are required"))

    for track_name, native_prefixes in (("ziwei", ("S05", "S06", "S07", "S08", "S09", "S10")), ("bazi", ("S11", "S12", "S13", "S14", "S15", "S16"))):
        track = actual.get(track_name, {})
        if not track.get("blind_model"):
            issues.append(ValidationIssue("TRACK_BLIND_MODEL_MISSING", f"{path}.{track_name}.blind_model", "track blind model is required"))
        parents = track.get("native_parent_ids", [])
        if not isinstance(parents, list) or not parents:
            issues.append(ValidationIssue("TRACK_NATIVE_PARENT_MISSING", f"{path}.{track_name}.native_parent_ids", "at least one native parent is required"))
        elif any(not str(parent).startswith(native_prefixes) for parent in parents):
            issues.append(ValidationIssue("FOREIGN_TRACK_PARENT", f"{path}.{track_name}.native_parent_ids", "parent namespace does not belong to this track"))

    matrix = actual.get("direction_matrix", {})
    if set(matrix) != set(expected_options):
        issues.append(ValidationIssue("DIRECTION_MATRIX_OPTION_SET_INVALID", f"{path}.direction_matrix", "matrix must contain every option"))
    coverage = actual.get("compound_coverage", {})
    if set(coverage) != set(expected_options):
        issues.append(ValidationIssue("COMPOUND_COVERAGE_OPTION_SET_INVALID", f"{path}.compound_coverage", "coverage must contain every option"))

    materialized = dict(actual)
    materialized["pairwise_rows"] = _pairwise_rows(option_order) if option_order else []
    materialized["pairwise_row_count_expected"] = len(expected_options) * (len(expected_options) - 1) // 2
    materialized["pairwise_row_count_actual"] = len(materialized["pairwise_rows"])
    return issues, materialized


def validate_chat_output(packet_path: str | Path, output_path: str | Path, validated_output_path: str | Path) -> dict[str, Any]:
    packet_file = Path(packet_path)
    output_file = Path(output_path)
    packet = read_json(packet_file)
    output = read_json(output_file)
    if packet.get("schema") != CHAT_PACKET_SCHEMA:
        raise FortuneError("wrong packet schema", status="CHAT_PACKET_SCHEMA_INVALID")
    if output.get("schema") != CHAT_OUTPUT_SCHEMA:
        raise FortuneError("wrong chat output schema", status="CHAT_OUTPUT_SCHEMA_INVALID")
    if output.get("case_id") != packet.get("case_id"):
        raise FortuneError("case id mismatch", status="CHAT_OUTPUT_CASE_MISMATCH")

    expected_questions = {row["question_id"]: row for row in packet["case_payload"]["questions"]["parsed"]}
    actual_questions = {row.get("question_id"): row for row in output.get("questions", [])}
    issues: list[ValidationIssue] = []
    materialized_questions = []
    for question_id, expected in expected_questions.items():
        actual = actual_questions.get(question_id)
        if actual is None:
            issues.append(ValidationIssue("QUESTION_OUTPUT_MISSING", f"$.questions[{question_id}]", "question output is missing"))
            continue
        question_issues, materialized = _validate_question(expected, actual, f"$.questions[{question_id}]")
        issues.extend(question_issues)
        materialized_questions.append(materialized)
    unknown_ids = sorted(set(actual_questions) - set(expected_questions))
    for question_id in unknown_ids:
        issues.append(ValidationIssue("UNKNOWN_QUESTION_OUTPUT", f"$.questions[{question_id}]", "question is not in packet"))

    fail_closed = any(issue.severity == "FAIL_CLOSED_CONTAMINATED" for issue in issues)
    if fail_closed:
        status = "FAIL_CLOSED_CONTAMINATED"
    elif issues:
        status = "REPAIRABLE_FAILURE"
    else:
        status = "PASS_READY_FOR_PREDICTION_FREEZE"

    validated = {
        "schema": "VALIDATED-CHAT-PROFESSIONAL-OUTPUT-V1",
        "case_id": packet["case_id"],
        "group_run_id": packet["group_run_id"],
        "packet_path": str(packet_file),
        "packet_sha256": sha256_file(packet_file),
        "chat_output_path": str(output_file),
        "chat_output_sha256": sha256_file(output_file),
        "questions": materialized_questions,
        "answer_data_available": False,
        "status": status,
        "validated_at": utc_now(),
    }
    atomic_write_json(validated_output_path, validated)
    report = {
        "schema": VALIDATION_SCHEMA,
        "case_id": packet["case_id"],
        "status": status,
        "issue_count": len(issues),
        "issues": [issue.as_dict() for issue in issues],
        "validated_output_path": str(validated_output_path),
        "validated_output_sha256": sha256_file(validated_output_path),
        "restart_required": fail_closed,
        "generated_at": utc_now(),
    }
    return report

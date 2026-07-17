from __future__ import annotations

import pytest

from fortune_v1.cli import parser
from fortune_v1.group_runner import GROUP_RUN_SCHEMA, _validate_manifest
from fortune_v1.util import FortuneError


def group() -> dict:
    return {
        "group_id": "DEV-GROUP-002",
        "case_ids": [f"DEV-EXAMPLE-00{i}" for i in range(1, 6)],
        "frozen_binding": {"main_prompt_runtime_id": "R16"},
    }


def manifest() -> dict:
    return {
        "schema": GROUP_RUN_SCHEMA,
        "group_id": "DEV-GROUP-002",
        "group_run_id": "GROUP-RUN-001",
        "session_id": "SESSION-001",
        "session_mode": "CHAT_ONLY",
        "answer_data_available": False,
        "case_runs": [
            {
                "case_id": f"DEV-EXAMPLE-00{i}",
                "run_id": f"CASE-RUN-00{i}",
                "run_path": f"case-{i}.json",
                "contract_path": f"contract-{i}.json",
                "prior_case_object_refs": [],
            }
            for i in range(1, 6)
        ],
    }


def test_cli_exposes_group_single_session_commands() -> None:
    p = parser()
    args = p.parse_args([
        "group-chat-work-run",
        "--manifest", "group.json",
        "--group-root", "groups/DEV-GROUP-002",
        "--output-root", "runs",
        "--mode", "CHAT_ONLY",
        "--session-id", "SESSION-001",
        "--group-run-id", "GROUP-RUN-001",
    ])
    assert args.command == "group-chat-work-run"

    verify = p.parse_args([
        "group-verify-freeze",
        "--group-freeze", "group-freeze.json",
        "--group-run-id", "GROUP-RUN-001",
        "--output", "validation.json",
    ])
    assert verify.command == "group-verify-freeze"


def test_complete_ordered_manifest_passes() -> None:
    rows = _validate_manifest(
        manifest(), group(), "GROUP-RUN-001", "SESSION-001", "CHAT_ONLY"
    )
    assert len(rows) == 5


def test_partial_group_submission_fails_closed() -> None:
    data = manifest()
    data["case_runs"] = data["case_runs"][:-1]
    with pytest.raises(FortuneError) as exc:
        _validate_manifest(data, group(), "GROUP-RUN-001", "SESSION-001", "CHAT_ONLY")
    assert exc.value.status == "PARTIAL_GROUP_SUBMISSION"


def test_duplicate_case_id_fails_closed() -> None:
    data = manifest()
    data["case_runs"][4]["case_id"] = data["case_runs"][3]["case_id"]
    with pytest.raises(FortuneError) as exc:
        _validate_manifest(data, group(), "GROUP-RUN-001", "SESSION-001", "CHAT_ONLY")
    assert exc.value.status in {"GROUP_CASE_ORDER_MISMATCH", "DUPLICATE_CASE_ID"}


def test_duplicate_case_run_id_fails_closed() -> None:
    data = manifest()
    data["case_runs"][4]["run_id"] = data["case_runs"][3]["run_id"]
    with pytest.raises(FortuneError) as exc:
        _validate_manifest(data, group(), "GROUP-RUN-001", "SESSION-001", "CHAT_ONLY")
    assert exc.value.status == "DUPLICATE_CASE_RUN_ID"


def test_group_answer_isolation_is_mandatory() -> None:
    data = manifest()
    data["answer_data_available"] = True
    with pytest.raises(FortuneError) as exc:
        _validate_manifest(data, group(), "GROUP-RUN-001", "SESSION-001", "CHAT_ONLY")
    assert exc.value.status == "GROUP_ANSWER_ISOLATION_FAILED"


def test_session_identity_and_mode_are_bound() -> None:
    with pytest.raises(FortuneError) as exc:
        _validate_manifest(manifest(), group(), "GROUP-RUN-001", "OTHER", "CHAT_ONLY")
    assert exc.value.status == "GROUP_SESSION_ID_MISMATCH"

    with pytest.raises(FortuneError) as exc:
        _validate_manifest(manifest(), group(), "GROUP-RUN-001", "SESSION-001", "WORK")
    assert exc.value.status == "GROUP_SESSION_MODE_MISMATCH"

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_valid_plain_json_case_materializes_with_registered_logical_hash(tmp_path: Path) -> None:
    receipt = tmp_path / "case005-receipt.json"
    result = run(
        "scripts/materialize-training-case.py",
        "training-data/DEV-GROUP-001/cases/DEV-EXAMPLE-005.json",
        "--expected-stored-bytes",
        "32806",
        "--expected-stored-sha256",
        "6c01997de6d6b4dcad111b65b0c5e350c28168d06a0fa95a4171296f17bf8450",
        "--expected-logical-sha256",
        "5292c94c69263d6aacf934e0078b1d5f2e90a29d0b731df482da6b293a541e45",
        "--receipt",
        str(receipt),
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(receipt.read_text(encoding="utf-8"))["status"] == "PASS"


def test_corrupt_legacy_case_is_rejected(tmp_path: Path) -> None:
    receipt = tmp_path / "case001-receipt.json"
    result = run(
        "scripts/materialize-training-case.py",
        "training-data/DEV-GROUP-001/cases/DEV-EXAMPLE-001.json.gz.b64",
        "--receipt",
        str(receipt),
    )
    assert result.returncode != 0
    body = json.loads(receipt.read_text(encoding="utf-8"))
    assert body["status"] == "FAIL"
    assert "gzip integrity check failed" in body["error"]


def test_group_hold_is_machine_valid_and_not_ready(tmp_path: Path) -> None:
    receipt = tmp_path / "group-receipt.json"
    result = run(
        "scripts/validate-training-group.py",
        "training-data/DEV-GROUP-001",
        "--allow-hold",
        "--receipt",
        str(receipt),
    )
    assert result.returncode == 0, result.stderr
    body = json.loads(receipt.read_text(encoding="utf-8"))
    assert body["status"] == "PASS_HOLD_FAIL_CLOSED"
    assert body["fully_valid_case_count"] == 1
    assert body["failed_case_ids"] == [
        "DEV-EXAMPLE-001",
        "DEV-EXAMPLE-002",
        "DEV-EXAMPLE-003",
        "DEV-EXAMPLE-004",
    ]


def test_group_cannot_enter_ready_training() -> None:
    result = run(
        "scripts/validate-training-group.py",
        "training-data/DEV-GROUP-001",
        "--require-ready",
    )
    assert result.returncode != 0
    assert "GROUP_NOT_READY" in result.stdout

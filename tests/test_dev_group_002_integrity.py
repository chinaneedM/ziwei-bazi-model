from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False)


def test_dev_group_002_all_plain_cases_materialize(tmp_path: Path) -> None:
    manifest = json.loads((ROOT / "training-data/DEV-GROUP-002/manifest.json").read_text(encoding="utf-8"))
    assert manifest["storage_format"] == "PLAIN_CANONICAL_JSON"
    assert manifest["answer_payload_present"] is False
    assert manifest["case_count"] == 5
    assert manifest["question_count_total"] == 25
    for row in manifest["cases"]:
        assert row["path"].endswith(".json")
        receipt = tmp_path / f"{row['case_id']}.json"
        result = run(
            "scripts/materialize-training-case.py",
            row["path"],
            "--expected-stored-bytes", str(row["stored_bytes"]),
            "--expected-stored-sha256", row["stored_sha256"],
            "--expected-logical-sha256", row["logical_json_sha256"],
            "--receipt", str(receipt),
        )
        assert result.returncode == 0, result.stderr
        assert json.loads(receipt.read_text(encoding="utf-8"))["status"] == "PASS"


def test_dev_group_002_is_pass_ready(tmp_path: Path) -> None:
    receipt = tmp_path / "group.json"
    result = run(
        "scripts/validate-training-group.py",
        "training-data/DEV-GROUP-002",
        "--require-ready",
        "--receipt", str(receipt),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    body = json.loads(receipt.read_text(encoding="utf-8"))
    assert body["status"] == "PASS_READY"
    assert body["fully_valid_case_count"] == 5
    assert body["failed_case_ids"] == []

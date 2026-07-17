#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GROUP_ID = "DEV-GROUP-002"
GROUP_ROOT = ROOT / "training-data" / GROUP_ID
CASES_ROOT = GROUP_ROOT / "cases"
OUTPUT_ROOT = GROUP_ROOT / "readable"
FORBIDDEN_KEYS = {
    "answer", "answers", "correct", "correct_option", "correct_answer",
    "literal_answer_vector", "answer_vector",
}
FORBIDDEN_TEXT = ("正确答案：", "正确答案:", "literal_answer_vector", "answer_vector")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def scan(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text.lower() in FORBIDDEN_KEYS or ("答案" in key_text and key_text != "answer_isolation"):
                findings.append(f"{path}.{key_text}:FORBIDDEN_KEY")
            findings.extend(scan(child, f"{path}.{key_text}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(scan(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        for token in FORBIDDEN_TEXT:
            if token in value:
                findings.append(f"{path}:FORBIDDEN_TEXT:{token}")
    return findings


def write(path: Path, data: bytes) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }


def main() -> None:
    manifest = json.loads((GROUP_ROOT / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("group_id") != GROUP_ID or manifest.get("status") not in {"READY_FOR_BASELINE_PREDICTION", "PASS_READY"}:
        raise SystemExit("group manifest is not eligible")
    if manifest.get("answer_payload_present") is not False or manifest.get("runtime_answer_scan") != "PASS":
        raise SystemExit("group answer-isolation gate failed")

    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True)

    case_rows: list[dict[str, Any]] = []
    for row in manifest["cases"]:
        case_path = ROOT / row["path"]
        case = json.loads(case_path.read_text(encoding="utf-8"))
        findings = scan(case)
        if findings:
            raise SystemExit(f"{case_path}: answer scan failed: {findings}")
        if case["answer_isolation"] != {
            "answer_payload_present": False,
            "answer_reference_disclosed": False,
            "status": "PROGRAMMATICALLY_ISOLATED",
        }:
            raise SystemExit(f"{case_path}: isolation receipt mismatch")

        case_id = case["case_id"]
        case_out = OUTPUT_ROOT / case_id
        ziwei_bytes = case["ziwei"]["text"].encode("utf-8")
        questions_bytes = case["questions"]["original_text"].encode("utf-8")
        bazi_bytes = canonical_bytes(case["bazi"])
        input_index = {
            "schema": "READABLE-PREDICTION-INPUT-V1",
            "group_id": GROUP_ID,
            "case_id": case_id,
            "answer_isolation": case["answer_isolation"],
            "binding": case["binding"],
            "cold_start_required": case["cold_start_required"],
            "source_case_path": row["path"],
            "source_case_sha256": row["stored_sha256"],
            "ziwei_path": f"training-data/{GROUP_ID}/readable/{case_id}/ziwei.txt",
            "questions_path": f"training-data/{GROUP_ID}/readable/{case_id}/questions.txt",
            "bazi_path": f"training-data/{GROUP_ID}/readable/{case_id}/bazi.json",
            "question_count": case["questions"]["question_count"],
            "status": "READY_FOR_BASELINE_PREDICTION",
        }
        files = {
            "ziwei": write(case_out / "ziwei.txt", ziwei_bytes),
            "questions": write(case_out / "questions.txt", questions_bytes),
            "bazi": write(case_out / "bazi.json", bazi_bytes),
        }
        index_bytes = canonical_bytes({**input_index, "files": files})
        index_receipt = write(case_out / "input-index.json", index_bytes)
        case_rows.append({
            "case_id": case_id,
            "question_count": case["questions"]["question_count"],
            "source_case_path": row["path"],
            "source_case_sha256": row["stored_sha256"],
            "files": files,
            "input_index": index_receipt,
            "answer_scan": "PASS",
            "status": "PASS_READABLE_TRANSPORT",
        })

    readable_manifest = {
        "schema": "DEV-GROUP-READABLE-TRANSPORT-V1",
        "group_id": GROUP_ID,
        "case_count": len(case_rows),
        "question_count_total": sum(row["question_count"] for row in case_rows),
        "answer_payload_present": False,
        "answer_reference_disclosed": False,
        "source_manifest_path": f"training-data/{GROUP_ID}/manifest.json",
        "transport_mode": "INDEPENDENT_UTF8_SIDECARS",
        "cases": case_rows,
        "status": "PASS_READY_FOR_COMPLETE_CHAT_READBACK",
    }
    manifest_bytes = canonical_bytes(readable_manifest)
    write(OUTPUT_ROOT / "manifest.json", manifest_bytes)
    print(manifest_bytes.decode("utf-8"), end="")


if __name__ == "__main__":
    main()

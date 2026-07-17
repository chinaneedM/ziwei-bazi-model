#!/usr/bin/env python3
"""Materialize answer-free, line-readable runtime views for training cases.

The canonical case bundle remains immutable. This tool extracts only fields already
present in the answer-isolated runtime case and writes deterministic sidecar files
that GitHub and CHAT/WORK connectors can read without truncating long JSON strings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "TRAINING-CASE-RUNTIME-VIEW-V1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def normalize_text(text: str) -> bytes:
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def materialize(case_path: Path, output_root: Path) -> Path:
    raw = case_path.read_bytes()
    case = json.loads(raw.decode("utf-8"))

    isolation = case.get("answer_isolation", {})
    if isolation.get("answer_payload_present") is not False:
        raise ValueError(f"answer payload is not isolated: {case_path}")
    if isolation.get("answer_reference_disclosed") is not False:
        raise ValueError(f"answer reference is disclosed: {case_path}")

    case_id = case["case_id"]
    out_dir = output_root / case_id
    if out_dir.exists():
        raise FileExistsError(f"runtime view already exists: {out_dir}")
    out_dir.mkdir(parents=True)

    ziwei = normalize_text(case["ziwei"]["text"])
    questions = normalize_text(case["questions"]["original_text"])
    bazi = canonical_json_bytes(case["bazi"]["transcription"])
    parsed_questions = canonical_json_bytes(case["questions"]["parsed"])

    files = {
        "ziwei.txt": ziwei,
        "questions.txt": questions,
        "bazi-transcription.json": bazi,
        "questions-parsed.json": parsed_questions,
    }
    for name, payload in files.items():
        (out_dir / name).write_bytes(payload)

    manifest = {
        "schema": SCHEMA,
        "case_id": case_id,
        "source_case_path": case_path.as_posix(),
        "source_case_sha256": sha256_bytes(raw),
        "answer_isolation_status": isolation.get("status"),
        "answer_payload_present": False,
        "answer_reference_disclosed": False,
        "files": {
            name: {"sha256": sha256_bytes(payload), "bytes": len(payload)}
            for name, payload in sorted(files.items())
        },
    }
    (out_dir / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()

    for case_path in args.case:
        materialize(case_path, args.output_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

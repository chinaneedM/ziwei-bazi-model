#!/usr/bin/env python3
"""Reparse answer-free question files after expanding intake support to option E."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_case_bank import (
    classify_question,
    coverage,
    object_sha256,
    parse_questions,
    sha256_file,
    write_json,
)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _assert_safe_reparse(
    case_id: str,
    existing: list[dict[str, Any]],
    reparsed: list[dict[str, Any]],
) -> None:
    if len(existing) != len(reparsed):
        raise ValueError(f"{case_id}: question count changed during option repair")
    for old, new in zip(existing, reparsed, strict=True):
        if old["question_id"] != new["question_id"] or old["stem"] != new["stem"]:
            raise ValueError(f"{case_id}: question identity or stem changed")
        old_options = {row["option_id"]: row["text"] for row in old["options"]}
        new_options = {row["option_id"]: row["text"] for row in new["options"]}
        if not set(old_options).issubset(new_options):
            raise ValueError(f"{case_id}/{old['question_id']}: existing option ids changed")
        for option_id in ("A", "B", "C"):
            if option_id in old_options and old_options[option_id] != new_options[option_id]:
                raise ValueError(
                    f"{case_id}/{old['question_id']}: stable option {option_id} changed"
                )
        if "E" not in new_options and old_options != new_options:
            raise ValueError(f"{case_id}/{old['question_id']}: four-option text changed")
        if "E" in new_options and not old_options["D"].startswith(new_options["D"]):
            raise ValueError(f"{case_id}/{old['question_id']}: D/E split is not lossless")


def repair(root: Path) -> dict[str, Any]:
    case_dir = root / "case-bank" / "cases"
    cases: list[dict[str, Any]] = []
    changed_cases: list[str] = []
    changed_questions: list[str] = []
    five_option_questions = 0
    for case_path in sorted(case_dir.glob("CASE-*.json")):
        case = _load_json(case_path)
        source_path = case.get("questions", {}).get("source_path")
        if isinstance(source_path, str):
            raw_path = root / source_path
            if sha256_file(raw_path) != case["questions"]["source_sha256"]:
                raise ValueError(f"{case['case_id']}: raw question hash mismatch")
            reparsed, issues = parse_questions(raw_path.read_text(encoding="utf-8-sig"))
            blocking = [row for row in issues if row.get("severity") == "BLOCKING"]
            if blocking:
                raise ValueError(f"{case['case_id']}: reparsing produced {blocking}")
            for question in reparsed:
                question["preblind_profile"] = classify_question(question)
            existing = case["questions"]["parsed"]
            _assert_safe_reparse(case["case_id"], existing, reparsed)
            for old, new in zip(existing, reparsed, strict=True):
                if old != new:
                    changed_questions.append(f"{case['case_id']}/{old['question_id']}")
            if existing != reparsed:
                changed_cases.append(case["case_id"])
                case["questions"]["parsed"] = reparsed
                write_json(case_path, case)
        five_option_questions += sum(
            len(question["options"]) == 5
            for question in case["questions"]["parsed"]
        )
        cases.append(case)

    manifest_path = root / "case-bank" / "manifest.json"
    manifest = _load_json(manifest_path)
    if manifest["question_count"] != sum(
        case["questions"]["question_count"] for case in cases
    ):
        raise ValueError("question count changed during option repair")
    manifest["coverage"] = coverage(cases)
    manifest["case_hashes"] = {
        case["case_id"]: object_sha256(case) for case in cases
    }
    write_json(manifest_path, manifest)

    split_to_file = {
        "DEVELOPMENT": "development.json",
        "STAGE_VALIDATION": "stage-validation.json",
        "FINAL_HOLDOUT": "final-holdout.json",
    }
    by_id = {case["case_id"]: case for case in cases}
    for split, filename in split_to_file.items():
        path = root / "case-bank" / "partitions" / filename
        partition = _load_json(path)
        partition["coverage"] = coverage(
            [by_id[case_id] for case_id in partition["case_order"]]
        )
        write_json(path, partition)

    return {
        "status": "CASE_BANK_OPTION_REPAIR_COMPLETE",
        "changed_case_count": len(changed_cases),
        "changed_question_count": len(changed_questions),
        "five_option_question_count": five_option_questions,
        "changed_cases": changed_cases,
        "answer_material_read": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(repair(args.repo.resolve()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

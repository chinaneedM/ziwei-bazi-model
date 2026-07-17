#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image

CASE_SCHEMA = "TRAINING-CASE-BUNDLE-V2"
GROUP_SCHEMA = "DEV-GROUP-V2"
MANIFEST_SCHEMA = "TRAINING-DATASET-MANIFEST-V2"
SOURCE_BASELINE_TAG = "source-baseline-S00-S19-R16"
MAIN_PROMPT_RUNTIME_ID = "MP-PROFESSIONAL-REASONING-20260715-R16"

FORBIDDEN_RUNTIME_KEYS = {
    "answer", "answers", "correct", "correct_option", "correct_answer",
    "literal_answer_vector", "answer_vector", "source_text"
}
FORBIDDEN_RUNTIME_TEXT = ("正确答案：", "正确答案:", "literal_answer_vector", "answer_vector")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(obj: Any, *, pretty: bool) -> bytes:
    if pretty:
        text = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, separators=(",", ": ")) + "\n"
    else:
        text = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return text.encode("utf-8")


def logical_hash(obj: Any) -> str:
    # Repository validator defines logical JSON as the same sorted, indented UTF-8 form.
    return sha256_bytes(canonical_bytes(obj, pretty=True))


def classify(name: str) -> str:
    if "答案" in name:
        return "answer"
    if "选择" in name or "题目" in name:
        return "questions"
    if "紫微" in name:
        return "ziwei"
    if "八字" in name:
        return "bazi_image"
    raise ValueError(f"unclassified archive member: {name}")


def parse_questions(text: str) -> list[dict[str, Any]]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    q_re = re.compile(r"^\s*(?:问题|题目)\s*(\d+)\s*[：:]\s*(.*)$")
    o_re = re.compile(r"^\s*([A-D])\s*(.*)$")
    questions: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in normalized.split("\n"):
        qm = q_re.match(line)
        if qm:
            if current is not None:
                questions.append(current)
            current = {"question_id": f"Q{int(qm.group(1))}", "stem": qm.group(2).strip(), "options": []}
            continue
        om = o_re.match(line)
        if om and current is not None:
            current["options"].append({"option_id": om.group(1), "text": om.group(2).strip()})
            continue
        if line.strip() and current is not None:
            if current["options"]:
                current["options"][-1]["text"] += "\n" + line.strip()
            else:
                current["stem"] += "\n" + line.strip()
    if current is not None:
        questions.append(current)
    if len(questions) != 5:
        raise ValueError(f"expected 5 questions, got {len(questions)}")
    for q in questions:
        ids = [o["option_id"] for o in q["options"]]
        if ids != ["A", "B", "C", "D"]:
            raise ValueError(f"{q['question_id']} option ids invalid: {ids}")
    return questions


def parse_answer_vector_without_disclosure(data: bytes, question_count: int) -> dict[str, Any]:
    text = data.decode("utf-8").strip()
    vectors = re.findall(r"(?<![A-Z])([A-D]{%d})(?![A-Z])" % question_count, text)
    if len(vectors) != 1:
        raise ValueError("answer vector parse failed")
    vector = vectors[0]
    return {
        "vector": vector,
        "question_count": len(vector),
        "source_bytes": len(data),
        "source_sha256": sha256_bytes(data),
    }


def recursive_answer_scan(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if (str(key).lower() in FORBIDDEN_RUNTIME_KEYS or "答案" in str(key)) and str(key) != "answer_isolation":
                findings.append(f"{path}.{key}:FORBIDDEN_KEY")
            findings.extend(recursive_answer_scan(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            findings.extend(recursive_answer_scan(child, f"{path}[{i}]"))
    elif isinstance(value, str):
        for token in FORBIDDEN_RUNTIME_TEXT:
            if token in value:
                findings.append(f"{path}:FORBIDDEN_TEXT:{token}")
    return findings


def extract_archive(extractor: Path, archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    subprocess.run([str(extractor), str(archive), str(destination)], check=True)


def build_case(case_index: int, archive: Path, extractor: Path, transcription_map: dict[str, Any], work_root: Path, output_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    case_id = f"DEV-EXAMPLE-{case_index:03d}"
    with tempfile.TemporaryDirectory(prefix=f"{case_id}-", dir=work_root) as td:
        extracted = Path(td) / "members"
        extract_archive(extractor, archive, extracted)
        roles: dict[str, Path] = {}
        member_receipts: list[dict[str, Any]] = []
        for member in sorted(p for p in extracted.iterdir() if p.is_file()):
            role = classify(member.name)
            if role in roles:
                raise ValueError(f"duplicate role {role} in {archive.name}")
            roles[role] = member
            data = member.read_bytes()
            member_receipts.append({"name": member.name, "role": role, "bytes": len(data), "sha256": sha256_bytes(data)})
        if set(roles) != {"answer", "questions", "ziwei", "bazi_image"}:
            raise ValueError(f"role set invalid for {archive.name}: {sorted(roles)}")

        question_bytes = roles["questions"].read_bytes()
        question_text = question_bytes.decode("utf-8")
        parsed = parse_questions(question_text)
        private_answer = parse_answer_vector_without_disclosure(roles["answer"].read_bytes(), len(parsed))

        image_bytes = roles["bazi_image"].read_bytes()
        image_sha = sha256_bytes(image_bytes)
        if image_sha not in transcription_map:
            raise ValueError(f"no verified transcription for image {image_sha}")
        with Image.open(roles["bazi_image"]) as im:
            width, height = im.size

        ziwei_bytes = roles["ziwei"].read_bytes()
        ziwei_text = ziwei_bytes.decode("utf-8")
        archive_bytes = archive.read_bytes()
        case_obj: dict[str, Any] = {
            "schema": CASE_SCHEMA,
            "case_id": case_id,
            "group_id": "DEV-GROUP-002",
            "dataset_type": "DEV",
            "source_label": f"例题{case_index}",
            "binding": {
                "main_prompt_runtime_id": MAIN_PROMPT_RUNTIME_ID,
                "source_baseline_tag": SOURCE_BASELINE_TAG,
            },
            "source_archive": {
                "original_name": archive.name,
                "bytes": len(archive_bytes),
                "sha256": sha256_bytes(archive_bytes),
            },
            "ziwei": {
                "original_name": roles["ziwei"].name,
                "bytes": len(ziwei_bytes),
                "sha256": sha256_bytes(ziwei_bytes),
                "text": ziwei_text,
            },
            "bazi": {
                "source_image": {
                    "original_name": roles["bazi_image"].name,
                    "bytes": len(image_bytes),
                    "sha256": image_sha,
                    "width": width,
                    "height": height,
                },
                "transcription": transcription_map[image_sha],
                "transcription_status": "VERIFIED_BY_IMAGE_SHA_BOUND_SIDECAR",
            },
            "questions": {
                "original_name": roles["questions"].name,
                "bytes": len(question_bytes),
                "sha256": sha256_bytes(question_bytes),
                "original_text": question_text,
                "question_count": len(parsed),
                "parsed": parsed,
            },
            "answer_isolation": {
                "answer_payload_present": False,
                "answer_reference_disclosed": False,
                "status": "PROGRAMMATICALLY_ISOLATED",
            },
            "cold_start_required": True,
        }
        findings = recursive_answer_scan(case_obj)
        if findings:
            raise ValueError(f"runtime answer isolation failed for {case_id}: {findings}")
        case_path = output_root / "cases" / f"{case_id}.json"
        case_path.parent.mkdir(parents=True, exist_ok=True)
        case_bytes = canonical_bytes(case_obj, pretty=True)
        case_path.write_bytes(case_bytes)
        receipt = {
            "case_id": case_id,
            "path": f"training-data/DEV-GROUP-002/cases/{case_id}.json",
            "storage_format": "PLAIN_CANONICAL_JSON",
            "stored_bytes": len(case_bytes),
            "stored_sha256": sha256_bytes(case_bytes),
            "logical_json_sha256": logical_hash(case_obj),
            "question_count": len(parsed),
            "runtime_answer_scan": "PASS",
            "integrity_status": "PASS",
            "source_archive_sha256": sha256_bytes(archive_bytes),
            "source_members": [m for m in member_receipts if m["role"] != "answer"],
            "bazi_image_sha256": image_sha,
        }
        private_receipt = {
            "case_id": case_id,
            "question_count": private_answer["question_count"],
            "answer_member_bytes": private_answer["source_bytes"],
            "answer_member_sha256": private_answer["source_sha256"],
        }
        # Private vector remains only in a local file for deterministic vault handling and is never printed.
        private_dir = output_root.parent / "private-vault-staging"
        private_dir.mkdir(parents=True, exist_ok=True)
        private_obj = {
            "schema": "PRIVATE-ANSWER-SOURCE-V2",
            "group_id": "DEV-GROUP-002",
            "case_id": case_id,
            "question_count": private_answer["question_count"],
            "literal_answer_vector": private_answer["vector"],
            "source_bytes": private_answer["source_bytes"],
            "source_sha256": private_answer["source_sha256"],
            "reveal_authorized": False,
            "status": "PRIVATE_STAGED_NOT_REVEALED",
        }
        (private_dir / f"{case_id}.json").write_bytes(canonical_bytes(private_obj, pretty=True))
        return receipt, private_receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extractor", required=True, type=Path)
    parser.add_argument("--transcriptions", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("archives", nargs=5, type=Path)
    args = parser.parse_args()

    map_obj = json.loads(args.transcriptions.read_text(encoding="utf-8"))
    transcription_map = map_obj["entries"]
    out = args.output_root
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    work_root = out.parent / "work"
    work_root.mkdir(parents=True, exist_ok=True)

    case_receipts: list[dict[str, Any]] = []
    private_receipts: list[dict[str, Any]] = []
    for idx, archive in enumerate(args.archives, 1):
        receipt, private = build_case(idx, archive, args.extractor, transcription_map, work_root, out)
        case_receipts.append(receipt)
        private_receipts.append(private)

    group_revision = {
        "schema": GROUP_SCHEMA,
        "group_id": "DEV-GROUP-002",
        "revision": 1,
        "status": "READY_FOR_BASELINE_PREDICTION",
        "case_ids": [r["case_id"] for r in case_receipts],
        "case_count": len(case_receipts),
        "question_count_total": sum(r["question_count"] for r in case_receipts),
        "storage_format": "PLAIN_CANONICAL_JSON",
        "binding": {
            "main_prompt_runtime_id": MAIN_PROMPT_RUNTIME_ID,
            "source_baseline_tag": SOURCE_BASELINE_TAG,
        },
        "baseline_freezes": {},
        "reveal_authorized": False,
        "cases": case_receipts,
    }
    rev_path = out / "revisions" / "0001.json"
    rev_path.parent.mkdir(parents=True, exist_ok=True)
    rev_path.write_bytes(canonical_bytes(group_revision, pretty=True))
    head = {"revision": 1, "path": "training-data/DEV-GROUP-002/revisions/0001.json", "status": "READY_FOR_BASELINE_PREDICTION"}
    (out / "HEAD.json").write_bytes(canonical_bytes(head, pretty=True))
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "group_id": "DEV-GROUP-002",
        "status": "READY_FOR_BASELINE_PREDICTION",
        "answer_payload_present": False,
        "case_count": len(case_receipts),
        "question_count_total": sum(r["question_count"] for r in case_receipts),
        "storage_format": "PLAIN_CANONICAL_JSON",
        "runtime_answer_scan": "PASS",
        "cases": case_receipts,
        "group_head": "training-data/DEV-GROUP-002/HEAD.json",
    }
    (out / "manifest.json").write_bytes(canonical_bytes(manifest, pretty=True))
    private_manifest = {
        "schema": "PRIVATE-TRAINING-IMPORT-MANIFEST-V2",
        "group_id": "DEV-GROUP-002",
        "status": "PRIVATE_STAGED_NOT_REVEALED",
        "reveal_authorized": False,
        "case_count": len(private_receipts),
        "question_count_total": sum(x["question_count"] for x in private_receipts),
        "answers": private_receipts,
    }
    (out.parent / "private-vault-staging" / "manifest.json").write_bytes(canonical_bytes(private_manifest, pretty=True))
    # Only non-sensitive receipt is printed.
    print(json.dumps({
        "group_id": "DEV-GROUP-002",
        "case_count": len(case_receipts),
        "question_count_total": sum(r["question_count"] for r in case_receipts),
        "status": "READY_FOR_BASELINE_PREDICTION",
        "case_receipts": [{k: r[k] for k in ("case_id", "stored_bytes", "stored_sha256", "logical_json_sha256", "question_count", "runtime_answer_scan")} for r in case_receipts],
    }, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()

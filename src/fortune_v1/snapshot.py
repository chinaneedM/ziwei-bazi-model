from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, sha256_file, slug, utc_now

ANSWER_PATTERNS = [
    re.compile(r"(?:正确答案|标准答案|参考答案|答案)\s*[:：=]\s*[A-H]", re.I),
    re.compile(r"\b(?:answer[_ -]?key|correct[_ -]?answer)\b", re.I),
]
ANSWER_KEYS = {"answer", "answers", "answer_key", "correct_answer", "correct_answers", "gold", "label"}


def _contains_forbidden(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in ANSWER_KEYS:
                findings.append(f"{path}.{key}:FORBIDDEN_KEY")
            findings.extend(_contains_forbidden(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for i, child in enumerate(value): findings.extend(_contains_forbidden(child, f"{path}[{i}]"))
    elif isinstance(value, str):
        for pattern in ANSWER_PATTERNS:
            if pattern.search(value): findings.append(f"{path}:FORBIDDEN_TEXT")
    return findings


def scan_file_for_answers(path: Path) -> list[str]:
    findings = []
    if any(token in path.name.lower() for token in ("answer", "答案", "gold", "label")):
        findings.append(f"{path}:FORBIDDEN_FILENAME")
    if path.suffix.lower() in {".txt", ".md", ".json", ".csv", ".tsv"}:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return findings + [f"{path}:INVALID_UTF8_TEXT"]
        for pattern in ANSWER_PATTERNS:
            if pattern.search(text): findings.append(f"{path}:FORBIDDEN_TEXT")
    return findings


def parse_questions(text: str) -> list[dict[str, Any]]:
    starts = list(re.finditer(r"(?m)^\s*(?:题目|问题|Q)\s*(\d+)\s*[.、:：)]?", text, re.I))
    if not starts:
        raise FortuneError("question headings not recognized", status="QUESTION_PARSE_FAILED")
    questions = []
    for index, start in enumerate(starts):
        block = text[start.start(): starts[index + 1].start() if index + 1 < len(starts) else len(text)]
        option_matches = list(re.finditer(r"(?m)^\s*([A-H])\s*[.、:：)]?\s+(.+?)\s*$", block))
        if len(option_matches) < 2:
            raise FortuneError(f"question {start.group(1)} has fewer than two options", status="QUESTION_PARSE_FAILED")
        options = [{"option_id": m.group(1), "text": m.group(2)} for m in option_matches]
        stem_end = option_matches[0].start()
        stem = block[start.end() - start.start():stem_end].strip()
        questions.append({"question_id": f"Q{int(start.group(1))}", "original_heading": start.group(0).strip(), "stem": stem, "options": options})
    ids = [q["question_id"] for q in questions]
    if len(ids) != len(set(ids)):
        raise FortuneError("duplicate question ids", status="QUESTION_PARSE_FAILED")
    return questions


def generate_prediction_snapshot(normalized_case_path: str | Path, output_root: str | Path,
                                 bazi_transcription_path: str | Path | None = None) -> dict[str, Any]:
    case = read_json(normalized_case_path)
    if case["status"] != "NORMALIZED" or case["answer_isolation"]["status"] != "PROGRAMMATICALLY_ISOLATED":
        raise FortuneError("case is not normalized and answer-isolated", status="PREDICTION_SNAPSHOT_BLOCKED")
    snapshot_id_seed = {"case": case, "bazi": sha256_file(bazi_transcription_path) if bazi_transcription_path else None}
    snapshot_id = f"SNAP-{slug(case['case_id'])}-{sha256_bytes(canonical_bytes(snapshot_id_seed))[:16]}"
    root = Path(output_root) / snapshot_id
    if root.exists():
        raise FortuneError("snapshot already exists", status="IMMUTABLE_OBJECT_EXISTS")
    copied, findings, question_source = [], [], None
    for item in case["files"]:
        source = Path(item["path"])
        if sha256_file(source) != item["sha256"]:
            raise FortuneError(f"normalized input hash mismatch: {source}", status="CASE_INPUT_HASH_MISMATCH")
        findings.extend(scan_file_for_answers(source))
        target = root / "input" / item["logical_type"].lower() / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target); target.chmod(0o444)
        copied.append({"logical_type": item["logical_type"], "path": str(target), "sha256": item["sha256"], "bytes": item["bytes"]})
        if item["logical_type"] == "QUESTIONS": question_source = source
    if findings:
        shutil.rmtree(root, ignore_errors=True)
        raise FortuneError("answer signature found in prediction input", status="ANSWER_LEAK_DETECTED")
    if question_source is None:
        raise FortuneError("questions file missing", status="QUESTION_PARSE_FAILED")
    questions = parse_questions(question_source.read_text(encoding="utf-8"))
    atomic_write_json(root / "questions.json", {"schema": "QUESTION-SET-V1", "questions": questions})
    bazi_receipt = None
    if bazi_transcription_path:
        bazi = read_json(bazi_transcription_path)
        bazi_findings = _contains_forbidden(bazi)
        if bazi_findings:
            shutil.rmtree(root, ignore_errors=True)
            raise FortuneError("answer key found in bazi transcription", status="ANSWER_LEAK_DETECTED")
        target = root / "bazi-transcription.json"
        shutil.copyfile(bazi_transcription_path, target); target.chmod(0o444)
        bazi_receipt = {"path": str(target), "sha256": sha256_file(target)}
    case_input_hash = sha256_bytes(canonical_bytes({"files": copied, "questions": questions, "bazi": bazi_receipt}))
    manifest = {
        "schema": "PREDICTION-INPUT-SNAPSHOT-V1", "snapshot_id": snapshot_id, "case_id": case["case_id"],
        "dataset_type": case["dataset_type"], "case_input_hash": case_input_hash,
        "files": copied, "questions_path": str(root / "questions.json"), "bazi_transcription": bazi_receipt,
        "answer_scan": {"status": "PASS", "findings": []}, "created_at": utc_now(),
    }
    atomic_write_json(root / "manifest.json", manifest)
    for path in root.rglob("*"):
        if path.is_file(): path.chmod(0o444)
    return manifest


def static_cache_key(case_input_hash: str, binding_hash: str, schema_version: str) -> str:
    return sha256_bytes(canonical_bytes({"case_input_hash": case_input_hash, "binding_hash": binding_hash, "schema_version": schema_version}))


def freeze_static_cache(snapshot_manifest_path: str | Path, static_object_path: str | Path,
                        binding_hash: str, schema_version: str, cache_root: str | Path) -> dict[str, Any]:
    manifest, obj = read_json(snapshot_manifest_path), read_json(static_object_path)
    required_ziwei = {"twelve_palaces", "base_chart_id", "sixty_star_system", "borrowed_stars", "opposite_and_trines", "stable_natures", "birth_transformations", "palace_stem_transformations", "self_transformations_and_lines", "person_coordinates"}
    required_bazi = {"solar_term_versions", "hidden_stems_ten_gods", "month_command_roots_qi", "relation_graph", "method_competition", "luck_coordinates"}
    missing = sorted((required_ziwei - set(obj.get("ziwei", {}))) | (required_bazi - set(obj.get("bazi", {}))))
    if missing:
        raise FortuneError(f"static cache missing fields: {missing}", status="STATIC_CACHE_INCOMPLETE")
    key = static_cache_key(manifest["case_input_hash"], binding_hash, schema_version)
    result = {"schema": "CASE-STATIC-CACHE-V1", "cache_key": key, "case_id": manifest["case_id"],
              "case_input_hash": manifest["case_input_hash"], "binding_hash": binding_hash,
              "schema_version": schema_version, "ziwei": obj["ziwei"], "bazi": obj["bazi"], "frozen_at": utc_now()}
    target = Path(cache_root) / f"{key}.json"
    atomic_write_json(target, result); target.chmod(0o444)
    return result


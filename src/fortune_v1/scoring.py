from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

SEPARATORS = {" ", "\t", "\r", "\n", ",", "，", "、", "/", "|", "-", ";", "；"}


def _extract_answer_payload(answer_path: str | Path, expected_run_id: str | None = None) -> str:
    path = Path(answer_path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        obj = read_json(path)
        if set(obj) - {"schema", "answers", "authorized_run_id"}:
            raise FortuneError("answer JSON contains unsupported fields", status="ANSWER_OBJECT_INVALID")
        if not isinstance(obj.get("answers"), str):
            raise FortuneError("answer JSON answers must be a string", status="ANSWER_OBJECT_INVALID")
        if obj.get("schema") != "FORTUNE-ANSWER-OBJECT-V1":
            raise FortuneError("answer JSON Schema invalid", status="ANSWER_OBJECT_INVALID")
        if expected_run_id is not None and obj.get("authorized_run_id") != slug(expected_run_id):
            raise FortuneError("answer object RUN_ID mismatch", status="ANSWER_OBJECT_RUN_ID_MISMATCH")
        return obj["answers"]
    return text


def literal_replay(answer_path: str | Path, legal_options: list[list[str]],
                   expected_run_id: str | None = None) -> dict[str, Any]:
    original = _extract_answer_payload(answer_path, expected_run_id)
    trimmed = original.strip()
    # Parser A: split only on an explicit separator set; no case conversion or semantic guessing.
    tokens_a = [token for token in re.split(r"[\s,，、/|;；-]+", trimmed) if token]
    if len(tokens_a) == 1 and len(tokens_a[0]) > 1:
        vector_a = list(tokens_a[0])
    else:
        if any(len(token) != 1 for token in tokens_a):
            raise FortuneError("answer contains non-literal tokens", status="ANSWER_LITERAL_REPLAY_FAIL")
        vector_a = tokens_a
    # Parser B: codepoint walk removing exactly the same explicit separators.
    vector_b, offsets = [], []
    for offset, char in enumerate(original):
        if char in SEPARATORS: continue
        vector_b.append(char); offsets.append(offset)
    if vector_a != vector_b:
        raise FortuneError("independent answer parsers disagree", status="ANSWER_LITERAL_REPLAY_FAIL")
    if len(vector_a) != len(legal_options):
        raise FortuneError(f"answer length {len(vector_a)} != question count {len(legal_options)}", status="ANSWER_LITERAL_REPLAY_FAIL")
    mapping = []
    for i, (answer, legal) in enumerate(zip(vector_a, legal_options), 1):
        if answer not in legal:
            raise FortuneError(f"answer {answer!r} is illegal for question {i}", status="ANSWER_LITERAL_REPLAY_FAIL")
        mapping.append({"question_index": i, "answer": answer, "char_offset": offsets[i - 1], "legal_options": legal})
    return {
        "schema": "ANSWER-VECTOR-LITERAL-REPLAY-V1", "original_string": original,
        "unicode_codepoints": [f"U+{ord(c):04X}" for c in original],
        "character_offsets": [{"offset": i, "char": c} for i, c in enumerate(original)],
        "question_count": len(legal_options), "parser_a": vector_a, "parser_b": vector_b,
        "mapping": mapping, "status": "PASS",
    }


def minimum_correct(question_count: int) -> int:
    if question_count <= 4: return question_count
    if question_count == 5: return 4
    return math.ceil(question_count * 0.8)


def validate_freeze_receipt(freeze_receipt_path: str | Path,
                            expected_run_id: str | None = None) -> dict[str, Any]:
    receipt = read_json(freeze_receipt_path)
    if receipt.get("schema") != "PREDICTION-FREEZE-RECEIPT-V1":
        raise FortuneError("freeze receipt Schema invalid", status="GRADING_BEFORE_FREEZE_BLOCKED")
    if receipt.get("immutable") is not True or receipt.get("non_overwrite") is not True:
        raise FortuneError("immutable freeze receipt required", status="GRADING_BEFORE_FREEZE_BLOCKED")
    if receipt.get("freeze_status") != "PREDICTION_FROZEN":
        raise FortuneError("prediction is not frozen", status="GRADING_BEFORE_FREEZE_BLOCKED")
    if expected_run_id is not None and receipt.get("run_id") != slug(expected_run_id):
        raise FortuneError("freeze receipt RUN_ID mismatch", status="FREEZE_RUN_ID_MISMATCH")
    if receipt.get("runtime_validation", {}).get("status") != "PASS":
        raise FortuneError("freeze runtime validation failed", status="GRADING_BEFORE_FREEZE_BLOCKED")
    required = {"prediction_path", "prediction_sha256", "contract_path", "contract_sha256", "run_id"}
    if not required.issubset(receipt):
        raise FortuneError("valid freeze receipt required", status="GRADING_BEFORE_FREEZE_BLOCKED")
    prediction_path = Path(receipt["prediction_path"])
    if not prediction_path.is_file() or sha256_file(prediction_path) != receipt["prediction_sha256"]:
        raise FortuneError("frozen prediction changed or missing", status="FROZEN_PREDICTION_HASH_MISMATCH")
    contract_path = Path(receipt["contract_path"])
    if not contract_path.is_file() or sha256_file(contract_path) != receipt["contract_sha256"]:
        raise FortuneError("frozen contract changed or missing", status="FROZEN_CONTRACT_HASH_MISMATCH")
    run = read_json(prediction_path)
    if slug(run.get("run_id", "")) != receipt["run_id"]:
        raise FortuneError("prediction RUN_ID differs from freeze receipt", status="FREEZE_RUN_ID_MISMATCH")
    return {"schema": "FREEZE-VALIDATION-RECEIPT-V1", "run_id": receipt["run_id"],
            "freeze_receipt_path": str(Path(freeze_receipt_path)),
            "freeze_receipt_sha256": sha256_file(freeze_receipt_path),
            "prediction_path": str(prediction_path), "prediction_sha256": receipt["prediction_sha256"],
            "contract_path": str(contract_path), "contract_sha256": receipt["contract_sha256"],
            "freeze_status": receipt["freeze_status"], "immutable": True, "status": "PASS"}


def grade_frozen_prediction(freeze_receipt_path: str | Path, answer_path: str | Path,
                            output_path: str | Path, gates: dict[str, bool] | None = None,
                            expected_run_id: str | None = None) -> dict[str, Any]:
    validation = validate_freeze_receipt(freeze_receipt_path, expected_run_id)
    receipt = read_json(freeze_receipt_path)
    prediction_path = Path(receipt["prediction_path"])
    run = read_json(prediction_path)
    legal = [q["option_ids"] for q in run["questions"]]
    # This is the first answer-object access. Every freeze check above has already passed.
    replay = literal_replay(answer_path, legal, expected_run_id or receipt["run_id"])
    rows, top1_hits, top2_hits = [], 0, 0
    for question, answer_row in zip(run["questions"], replay["mapping"]):
        answer = answer_row["answer"]
        top1_hit = question["top1"] == answer
        top2_hit = answer in {question["top1"], question["top2"]}
        top1_hits += int(top1_hit); top2_hits += int(top2_hit)
        rows.append({"question_id": question["question_id"], "frozen_top1": question["top1"],
                     "frozen_top2": question["top2"], "literal_answer": answer,
                     "top1_scored_correct": top1_hit, "top2_diagnostic_hit": top2_hit})
    threshold = minimum_correct(len(rows)); accuracy_pass = top1_hits >= threshold
    required_gates = ["answer_isolation", "cold_start", "runtime_object_complete", "dual_track_independent", "patch_leak_free", "historical_regression_no_damage"]
    gate_values = gates or {}
    gates_pass = all(gate_values.get(key) is True for key in required_gates)
    runtime_pass = receipt["runtime_validation"].get("status") == "PASS"
    if accuracy_pass and not runtime_pass:
        status = "ACCURACY_PASS_RUNTIME_FAIL"
    elif accuracy_pass and runtime_pass and gates_pass:
        status = "CASE_PASS"
    elif accuracy_pass:
        status = "ACCURACY_PASS_PENDING_REQUIRED_GATES"
    else:
        status = "CASE_FAIL"
    result = {
        "schema": "REVEAL-AND-DIAGNOSIS-V1", "reveal_id": f"REVEAL-{slug(run['run_id'])}", "run_id": run["run_id"],
        "freeze_receipt_sha256": sha256_file(freeze_receipt_path), "literal_replay": replay,
        "pre_answer_freeze_validation": validation,
        "score": {"question_count": len(rows), "top1_correct": top1_hits, "top1_required": threshold,
                  "top1_accuracy": top1_hits / len(rows), "top2_diagnostic_hits": top2_hits,
                  "top2_is_formal_score": False, "accuracy_pass": accuracy_pass, "rows": rows},
        "gates": {"required": required_gates, "values": gate_values, "all_pass": gates_pass},
        "diagnosis": {"status": "PENDING_ERROR_CLASSIFICATION"}, "status": status, "created_at": utc_now(),
    }
    atomic_write_json(output_path, result)
    return result

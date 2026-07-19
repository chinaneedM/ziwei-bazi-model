from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from .runtime import (
    _validate_learning_patch,
    apply_learning,
    freeze_prediction,
    score_round,
    start_round,
    status,
)
from .util import TrainingError, atomic_write_json, require_safe_id
from .verify import verify_repository


PACKET_START = "<!-- TRAINING_PACKET_START -->"
PACKET_END = "<!-- TRAINING_PACKET_END -->"
PACKET_SCHEMA = "TRAINING-ISSUE-PACKET-V1"
EXPECTED_RESULTS = {"PASS", "FAIL"}


def extract_packet(issue_body: str) -> dict[str, Any]:
    start_count = issue_body.count(PACKET_START)
    end_count = issue_body.count(PACKET_END)
    if start_count or end_count:
        if start_count != 1 or end_count != 1:
            raise TrainingError("issue must contain exactly one training packet marker pair")
        start = issue_body.index(PACKET_START) + len(PACKET_START)
        end = issue_body.index(PACKET_END, start)
        raw = issue_body[start:end].strip()
    else:
        # Low-friction mode: the owner may replace the whole Issue body with the
        # JSON copied from Chat. Legacy marker-wrapped submissions remain valid.
        raw = issue_body.strip()
    if raw.startswith("```json"):
        raw = raw[len("```json") :].strip()
    elif raw.startswith("```"):
        raw = raw[3:].strip()
    if raw.endswith("```"):
        raw = raw[:-3].strip()
    if not raw or raw in {"PASTE_CHAT_PACKET_HERE", "PASTE_COMPLETE_JSON_HERE"}:
        raise TrainingError("training packet is empty")
    try:
        packet = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TrainingError(f"training packet is not valid JSON: {exc.msg}") from exc
    if not isinstance(packet, dict):
        raise TrainingError("training packet must be a JSON object")
    return packet


def _validate_packet(root: Path, packet: dict[str, Any]) -> dict[str, Any]:
    if packet.get("schema") != PACKET_SCHEMA:
        raise TrainingError(f"packet schema must be {PACKET_SCHEMA}")
    allowed_keys = {
        "schema",
        "round_id",
        "case_id",
        "predictions",
        "expected_result",
        "learning_release_id",
        "learning_patch",
    }
    unknown = set(packet) - allowed_keys
    if unknown:
        raise TrainingError(f"unknown packet fields: {', '.join(sorted(unknown))}")
    round_id = packet.get("round_id")
    release_id = packet.get("learning_release_id")
    require_safe_id(round_id, "round_id")
    expected = packet.get("expected_result")
    if expected not in EXPECTED_RESULTS:
        raise TrainingError("expected_result must be PASS or FAIL")
    current = status(root)
    if packet.get("case_id") != current["current_case_id"]:
        raise TrainingError("packet case_id is not the current training case")
    if current["status"] not in {"READY_FOR_ROUND", "CONFIRMATION_REQUIRED"}:
        raise TrainingError(f"cannot process a new round while state is {current['status']}")
    predictions = packet.get("predictions")
    if not isinstance(predictions, list) or not predictions:
        raise TrainingError("packet needs predictions for every question")
    if expected == "FAIL":
        require_safe_id(release_id, "learning_release_id")
        _validate_learning_patch(root, packet.get("learning_patch"))
    elif release_id is not None or packet.get("learning_patch") is not None:
        raise TrainingError("a PASS packet must not contain a learning patch or release id")
    return packet


def process_packet(root: Path, packet: dict[str, Any], key: str | bytes | None) -> dict[str, Any]:
    root = root.resolve()
    verify_repository(root, require_answers=True)
    packet = _validate_packet(root, packet)
    round_id = packet["round_id"]

    with tempfile.TemporaryDirectory(prefix="fortune-training-relay-") as temporary:
        work = Path(temporary)
        prediction_file = work / "prediction.json"
        review_file = work / "review.json"
        patch_file = work / "learning-patch.json"
        atomic_write_json(
            prediction_file,
            {
                "case_id": packet["case_id"],
                "round_id": round_id,
                "predictions": packet["predictions"],
            },
        )

        start_round(root, round_id)
        freeze_prediction(root, round_id, prediction_file)
        score = score_round(root, round_id, review_file, key=key)
        actual_result = "PASS" if score["passed"] else "FAIL"
        if actual_result != packet["expected_result"]:
            raise TrainingError(
                f"packet expected {packet['expected_result']} but encrypted-answer scoring produced {actual_result}"
            )

        learning_release = None
        if not score["passed"]:
            atomic_write_json(patch_file, packet["learning_patch"])
            release = apply_learning(root, round_id, patch_file, packet["learning_release_id"])
            learning_release = release["release_id"]

        verification = verify_repository(root, require_answers=True)
        new_status = status(root)
        result = {
            "schema": "TRAINING-ISSUE-RESULT-V1",
            "round_id": round_id,
            "case_id": packet["case_id"],
            "correct_count": score["correct_count"],
            "question_count": score["question_count"],
            "required_correct": score["required_correct"],
            "accuracy": score["accuracy"],
            "passed": score["passed"],
            "consecutive_passes": score["consecutive_passes_after"],
            "learning_release": learning_release,
            "next_case_id": new_status["current_case_id"],
            "next_status": new_status["status"],
            "answers_published": False,
            "verification": verification["status"],
        }
        result_path = root / "training" / "relay-results" / f"{round_id}.json"
        atomic_write_json(result_path, result)
        return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process one owner-submitted GitHub training issue")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--issue-body-file", type=Path, required=True)
    parser.add_argument("--result-file", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        issue_body = args.issue_body_file.read_text(encoding="utf-8")
        packet = extract_packet(issue_body)
        result = process_packet(args.root, packet, os.environ.get("FORTUNE_ANSWER_KEY"))
        atomic_write_json(args.result_file, result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    except (OSError, TrainingError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from .chat_input import CHAT_INPUT_RELATIVE_PATH
from .issue_relay import extract_packet
from .runtime import _validate_prediction, freeze_prediction, score_round, start_round
from .util import TrainingError, atomic_write_json, canonical_bytes, load_json, sha256_bytes
from .verify import verify_repository


HANDOFF_SCHEMA = "CHAT-WORK-PREDICTION-HANDOFF-V2"
REQUEST_PREFIX = "/score-review "
SEALED_SCHEMA = "WORK-PRIVATE-ROUND-REVIEW-V1"
FORBIDDEN_HANDOFF_KEYS = {
    "answer",
    "answers",
    "answer_key",
    "correct_answer",
    "correct_option",
    "expected_result",
    "is_correct",
    "learning_patch",
    "learning_release_id",
    "passed",
    "review",
    "score",
    "secret",
}


def _walk_forbidden_keys(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_HANDOFF_KEYS:
                raise TrainingError(f"answer, score, or learning field in handoff: {path}.{key}")
            _walk_forbidden_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden_keys(child, f"{path}[{index}]")


def parse_review_request(request: str) -> str:
    request = request.strip()
    if not request.startswith(REQUEST_PREFIX):
        raise TrainingError(f"review request must start with {REQUEST_PREFIX!r}")
    encoded = request[len(REQUEST_PREFIX) :].strip()
    try:
        der = base64.b64decode(encoded, validate=True)
        key = serialization.load_der_public_key(der)
    except (ValueError, TypeError) as exc:
        raise TrainingError("review request public key is invalid") from exc
    if not isinstance(key, rsa.RSAPublicKey) or key.key_size < 3072:
        raise TrainingError("review request requires an RSA public key of at least 3072 bits")
    return encoded


def validate_handoff(
    root: Path,
    *,
    issue_title: str,
    issue_body: str,
) -> dict[str, Any]:
    root = root.resolve()
    bundle = load_json(root / CHAT_INPUT_RELATIVE_PATH)
    contract = bundle.get("chat_work_handoff_contract")
    if not isinstance(contract, dict):
        raise TrainingError("current Chat bundle has no handoff contract")
    expected_title = contract.get("issue_title")
    if not expected_title or issue_title != expected_title:
        raise TrainingError("handoff Issue title does not match the current Chat bundle")
    if bundle.get("state_summary", {}).get("prediction_allowed") is not True:
        raise TrainingError("current Chat bundle does not allow a prediction round")

    handoff = extract_packet(issue_body)
    if handoff.get("schema") != HANDOFF_SCHEMA:
        raise TrainingError(f"handoff schema must be {HANDOFF_SCHEMA}")
    if set(handoff) != {
        "schema",
        "binding",
        "blind_chart_model",
        "cross_question_consistency",
        "replay_remediation",
        "predictions",
    }:
        raise TrainingError("handoff must contain the complete V2 reasoning workbook")
    if handoff.get("binding") != contract.get("binding"):
        raise TrainingError("handoff binding does not match the current Chat bundle")
    predictions = handoff.get("predictions")
    if not isinstance(predictions, list) or not predictions:
        raise TrainingError("handoff predictions must be a non-empty array")
    _walk_forbidden_keys(handoff)
    _validate_prediction(
        root,
        bundle["current_case"],
        {
            "case_id": contract["binding"]["case_id"],
            "round_id": contract["binding"]["round_id"],
            "evaluation_kind": contract["binding"]["evaluation_kind"],
        },
        {
            "schema": "PREDICTION-WORKBOOK-V2",
            "case_id": contract["binding"]["case_id"],
            "round_id": contract["binding"]["round_id"],
            "blind_chart_model": handoff["blind_chart_model"],
            "cross_question_consistency": handoff[
                "cross_question_consistency"
            ],
            "replay_remediation": handoff["replay_remediation"],
            "predictions": predictions,
        },
    )
    return handoff


def seal_private_review(payload: dict[str, Any], encoded_public_key: str) -> dict[str, Any]:
    public_key = serialization.load_der_public_key(base64.b64decode(encoded_public_key))
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TrainingError("review request key is not RSA")
    data_key = Fernet.generate_key()
    ciphertext = Fernet(data_key).encrypt(canonical_bytes(payload)).decode("ascii")
    wrapped_key = public_key.encrypt(
        data_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    public_der = public_key.public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return {
        "schema": SEALED_SCHEMA,
        "algorithm": "RSA-OAEP-SHA256+FERNET",
        "public_key_sha256": sha256_bytes(public_der),
        "wrapped_key": base64.b64encode(wrapped_key).decode("ascii"),
        "ciphertext": ciphertext,
    }


def unseal_private_review(
    envelope: dict[str, Any],
    private_key: rsa.RSAPrivateKey,
) -> dict[str, Any]:
    if envelope.get("schema") != SEALED_SCHEMA:
        raise TrainingError(f"sealed review schema must be {SEALED_SCHEMA}")
    public_der = private_key.public_key().public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    if envelope.get("public_key_sha256") != sha256_bytes(public_der):
        raise TrainingError("sealed review was encrypted for a different Work session")
    try:
        data_key = private_key.decrypt(
            base64.b64decode(envelope["wrapped_key"], validate=True),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        plaintext = Fernet(data_key).decrypt(envelope["ciphertext"].encode("ascii"))
        payload = json.loads(plaintext.decode("utf-8"))
    except (KeyError, TypeError, ValueError) as exc:
        raise TrainingError("sealed review envelope is invalid") from exc
    if not isinstance(payload, dict):
        raise TrainingError("unsealed review payload is invalid")
    return payload


def process_handoff_probe(
    root: Path,
    *,
    issue_title: str,
    issue_body: str,
    encoded_public_key: str,
    key: str | bytes | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root.resolve()
    verify_repository(root, require_answers=True)
    handoff = validate_handoff(root, issue_title=issue_title, issue_body=issue_body)
    binding = handoff["binding"]
    round_id = binding["round_id"]

    with tempfile.TemporaryDirectory(prefix="fortune-handoff-probe-") as temporary:
        work = Path(temporary)
        prediction_path = work / "prediction.json"
        review_path = work / "review.json"
        atomic_write_json(
            prediction_path,
            {
                "schema": "PREDICTION-WORKBOOK-V2",
                "case_id": binding["case_id"],
                "round_id": round_id,
                "blind_chart_model": handoff["blind_chart_model"],
                "cross_question_consistency": handoff[
                    "cross_question_consistency"
                ],
                "replay_remediation": handoff["replay_remediation"],
                "predictions": handoff["predictions"],
            },
        )
        start_round(root, round_id)
        frozen = freeze_prediction(root, round_id, prediction_path)
        score = score_round(root, round_id, review_path, key=key)
        detailed_review = load_json(review_path)

    private_payload = {
        "schema": "WORK-ROUND-REVIEW-PLAINTEXT-V1",
        "binding": binding,
        "prediction_sha256": frozen["prediction_sha256"],
        "score": score,
        "detailed_review": detailed_review,
    }
    summary = {
        "schema": "HANDOFF-SCORE-PROBE-RESULT-V1",
        "round_id": round_id,
        "case_id": binding["case_id"],
        "correct_count": score["correct_count"],
        "scoreable_question_count": score["scoreable_question_count"],
        "required_correct": score["required_correct"],
        "passed": score["passed"],
        "answers_published": False,
        "repository_mutated": False,
    }
    return summary, seal_private_review(private_payload, encoded_public_key)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Privately score one machine-bound Chat-to-Work handoff without committing state"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--issue-title", required=True)
    parser.add_argument("--issue-body-file", type=Path, required=True)
    parser.add_argument("--request-file", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--sealed-output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        encoded_public_key = parse_review_request(
            args.request_file.read_text(encoding="utf-8")
        )
        summary, sealed = process_handoff_probe(
            args.root,
            issue_title=args.issue_title,
            issue_body=args.issue_body_file.read_text(encoding="utf-8"),
            encoded_public_key=encoded_public_key,
            key=os.environ.get("FORTUNE_ANSWER_KEY"),
        )
        atomic_write_json(args.summary_output, summary)
        atomic_write_json(args.sealed_output, sealed)
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    except (OSError, TrainingError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

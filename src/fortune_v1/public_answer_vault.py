from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, sha256_file, utc_now

ENVELOPE_SCHEMA = "PUBLIC-ENCRYPTED-ANSWER-VECTOR-V1"
ANSWER_SCHEMA = "GROUP-ANSWER-VECTOR-V1"
ALGORITHM = "FERNET-AES128-CBC-HMAC-SHA256"


def _require(condition: bool, message: str, status: str) -> None:
    if not condition:
        raise FortuneError(message, status=status)


def _key_bytes(value: str | bytes) -> bytes:
    raw = value.encode("ascii") if isinstance(value, str) else value
    try:
        Fernet(raw)
    except Exception as exc:  # pragma: no cover - cryptography owns exact exception type
        raise FortuneError("invalid public answer vault key", status="PUBLIC_ANSWER_KEY_INVALID") from exc
    return raw


def _with_hash(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("object_hash", None)
    result["object_hash"] = sha256_bytes(canonical_bytes(result))
    return result


def generate_key() -> str:
    return Fernet.generate_key().decode("ascii")


def encrypt_answer_vector(
    answer_vector_path: str | Path,
    envelope_path: str | Path,
    key: str | bytes,
    *,
    key_id: str = "FORTUNE_PUBLIC_ANSWER_KEY_V1",
) -> dict[str, Any]:
    answer_path = Path(answer_vector_path)
    answer = read_json(answer_path)
    _require(answer.get("schema") == ANSWER_SCHEMA, "answer vector schema invalid", "ANSWER_VECTOR_SCHEMA_INVALID")
    _require(answer.get("status") == "REVEALED_FOR_TRAINING_AFTER_FREEZE", "answer vector status invalid", "ANSWER_VECTOR_STATUS_INVALID")
    group_run_id = answer.get("group_run_id")
    _require(isinstance(group_run_id, str) and bool(group_run_id), "group run id missing", "ANSWER_VECTOR_IDENTITY_INVALID")
    rows = answer.get("rows")
    _require(isinstance(rows, list) and bool(rows), "answer rows missing", "ANSWER_VECTOR_ROWS_MISSING")

    plaintext = canonical_bytes(answer)
    token = Fernet(_key_bytes(key)).encrypt(plaintext)
    envelope = _with_hash({
        "schema": ENVELOPE_SCHEMA,
        "status": "ENCRYPTED_PUBLIC_STORAGE_READY",
        "group_run_id": group_run_id,
        "algorithm": ALGORITHM,
        "key_id": key_id,
        "ciphertext": token.decode("ascii"),
        "ciphertext_sha256": sha256_bytes(token),
        "plaintext_not_stored_in_repository": True,
        "created_at": utc_now(),
    })
    atomic_write_json(envelope_path, envelope)
    return envelope


def decrypt_answer_envelope(
    envelope_path: str | Path,
    output_path: str | Path,
    key: str | bytes,
    *,
    repository_root: str | Path | None = None,
) -> dict[str, Any]:
    envelope_file = Path(envelope_path)
    envelope = read_json(envelope_file)
    _require(envelope.get("schema") == ENVELOPE_SCHEMA, "answer envelope schema invalid", "PUBLIC_ANSWER_ENVELOPE_SCHEMA_INVALID")
    _require(envelope.get("status") == "ENCRYPTED_PUBLIC_STORAGE_READY", "answer envelope status invalid", "PUBLIC_ANSWER_ENVELOPE_STATUS_INVALID")
    _require(envelope.get("algorithm") == ALGORITHM, "answer envelope algorithm invalid", "PUBLIC_ANSWER_ENVELOPE_ALGORITHM_INVALID")
    token_text = envelope.get("ciphertext")
    _require(isinstance(token_text, str) and bool(token_text), "ciphertext missing", "PUBLIC_ANSWER_CIPHERTEXT_MISSING")
    token = token_text.encode("ascii")
    _require(sha256_bytes(token) == envelope.get("ciphertext_sha256"), "ciphertext hash mismatch", "PUBLIC_ANSWER_CIPHERTEXT_HASH_MISMATCH")

    target = Path(output_path).resolve()
    root = Path(repository_root or Path.cwd()).resolve()
    _require(root != target and root not in target.parents, "decrypted answer output must remain outside repository", "DECRYPTED_ANSWER_REPOSITORY_WRITE_FORBIDDEN")
    try:
        plaintext = Fernet(_key_bytes(key)).decrypt(token)
    except InvalidToken as exc:
        raise FortuneError("answer envelope decryption failed", status="PUBLIC_ANSWER_DECRYPTION_FAILED") from exc
    try:
        answer = json.loads(plaintext.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FortuneError("decrypted answer payload invalid", status="PUBLIC_ANSWER_PAYLOAD_INVALID") from exc

    _require(answer.get("schema") == ANSWER_SCHEMA, "decrypted answer schema invalid", "ANSWER_VECTOR_SCHEMA_INVALID")
    _require(answer.get("group_run_id") == envelope.get("group_run_id"), "decrypted answer identity mismatch", "ANSWER_VECTOR_IDENTITY_INVALID")
    atomic_write_json(target, answer)
    return _with_hash({
        "schema": "PUBLIC-ANSWER-DECRYPTION-RECEIPT-V1",
        "status": "PASS",
        "group_run_id": envelope["group_run_id"],
        "encrypted_envelope_path": str(envelope_file),
        "encrypted_envelope_sha256": sha256_file(envelope_file),
        "decrypted_answer_sha256": sha256_file(target),
        "decrypted_output_location": "TRANSIENT_OUTSIDE_REPOSITORY",
        "plaintext_committed_to_repository": False,
        "decrypted_at": utc_now(),
    })


def _key_from_env(name: str) -> str:
    value = os.environ.get(name)
    _require(bool(value), f"missing environment secret: {name}", "PUBLIC_ANSWER_KEY_MISSING")
    return str(value)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fortune-public-answer-vault")
    sub = p.add_subparsers(dest="command", required=True)

    key = sub.add_parser("generate-key")
    key.add_argument("--output")

    encrypt = sub.add_parser("encrypt")
    encrypt.add_argument("--answer", required=True)
    encrypt.add_argument("--envelope", required=True)
    encrypt.add_argument("--key-env", default="FORTUNE_PUBLIC_ANSWER_KEY")
    encrypt.add_argument("--key-id", default="FORTUNE_PUBLIC_ANSWER_KEY_V1")

    decrypt = sub.add_parser("decrypt")
    decrypt.add_argument("--envelope", required=True)
    decrypt.add_argument("--output", required=True)
    decrypt.add_argument("--key-env", default="FORTUNE_PUBLIC_ANSWER_KEY")
    decrypt.add_argument("--repository-root", default=".")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "generate-key":
            value = generate_key()
            if args.output:
                target = Path(args.output)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(value + "\n", encoding="ascii")
                print(json.dumps({"status": "KEY_WRITTEN", "path": str(target)}, sort_keys=True))
            else:
                print(value)
            return 0
        if args.command == "encrypt":
            result = encrypt_answer_vector(args.answer, args.envelope, _key_from_env(args.key_env), key_id=args.key_id)
        else:
            result = decrypt_answer_envelope(
                args.envelope,
                args.output,
                _key_from_env(args.key_env),
                repository_root=args.repository_root,
            )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

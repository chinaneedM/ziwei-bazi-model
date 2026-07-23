from __future__ import annotations

import base64
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .formal import (
    activate_formal_controller,
    import_answer_batch,
    rehearse_formal_no_reveal,
)
from .runtime import _fernet_from_key
from .util import (
    TrainingError,
    atomic_write_json,
    require_outside,
)


TRANSPORT_DIR = Path("answer-vault/import-transport")
PUBLIC_KEY_PATH = TRANSPORT_DIR / "public-key.pem"
PRIVATE_KEY_ENVELOPE_PATH = TRANSPORT_DIR / "private-key.pem.fernet"
SEALED_BATCH_PATH = TRANSPORT_DIR / "answer-batch.sealed.json"


def bootstrap_answer_transport(
    root: Path,
    key: str | bytes | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    destination = root / TRANSPORT_DIR
    if destination.exists():
        raise TrainingError("answer-import transport already exists")
    fernet = _fernet_from_key(key)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    destination.mkdir(parents=True)
    try:
        with (root / PUBLIC_KEY_PATH).open("xb") as handle:
            handle.write(public_pem)
        with (root / PRIVATE_KEY_ENVELOPE_PATH).open("xb") as handle:
            handle.write(fernet.encrypt(private_pem) + b"\n")
    except Exception:
        shutil.rmtree(destination)
        raise
    return {
        "status": "ANSWER_IMPORT_TRANSPORT_READY",
        "public_key_path": PUBLIC_KEY_PATH.as_posix(),
        "private_key_encrypted": True,
        "plaintext_answer_key_disclosed": False,
    }


def seal_answer_batch(
    root: Path,
    public_key_path: Path,
    plaintext_batch: Path,
    output_path: Path,
) -> dict[str, Any]:
    root = root.resolve()
    require_outside(root, plaintext_batch, "plaintext answer batch")
    require_outside(root, output_path, "sealed answer-batch output")
    if output_path.exists():
        raise TrainingError(f"sealed output already exists: {output_path}")
    try:
        public_key = serialization.load_pem_public_key(public_key_path.read_bytes())
    except (OSError, ValueError, TypeError) as exc:
        raise TrainingError("answer-import public key is invalid") from exc
    plaintext = plaintext_batch.read_bytes()
    content_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    ciphertext = AESGCM(content_key).encrypt(nonce, plaintext, None)
    try:
        wrapped_key = public_key.encrypt(
            content_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except (AttributeError, TypeError, ValueError) as exc:
        raise TrainingError("answer-import public key cannot wrap the batch key") from exc
    payload = {
        "schema": "FORMAL-ANSWER-TRANSPORT-V1",
        "key_wrap": "RSA-OAEP-SHA256",
        "content_cipher": "AES-256-GCM",
        "wrapped_key": base64.b64encode(wrapped_key).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
        "plaintext_stored_in_repository": False,
    }
    atomic_write_json(output_path, payload)
    return {
        "status": "ANSWER_BATCH_SEALED",
        "sealed_path": str(output_path),
        "plaintext_stored_in_repository": False,
    }


def _decrypt_transport_batch(
    root: Path,
    key: str | bytes | None,
) -> bytes:
    transport = load_transport_payload(root / SEALED_BATCH_PATH)
    fernet = _fernet_from_key(key)
    try:
        private_pem = fernet.decrypt(
            (root / PRIVATE_KEY_ENVELOPE_PATH).read_bytes().strip()
        )
        private_key = serialization.load_pem_private_key(private_pem, password=None)
        content_key = private_key.decrypt(
            base64.b64decode(transport["wrapped_key"], validate=True),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return AESGCM(content_key).decrypt(
            base64.b64decode(transport["nonce"], validate=True),
            base64.b64decode(transport["ciphertext"], validate=True),
            None,
        )
    except Exception as exc:
        raise TrainingError("sealed answer batch failed authenticated decryption") from exc


def load_transport_payload(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TrainingError("sealed answer-batch transport is missing or invalid") from exc
    if not isinstance(payload, dict) or set(payload) != {
        "schema",
        "key_wrap",
        "content_cipher",
        "wrapped_key",
        "nonce",
        "ciphertext",
        "plaintext_stored_in_repository",
    }:
        raise TrainingError("sealed answer-batch transport has unexpected fields")
    if (
        payload.get("schema") != "FORMAL-ANSWER-TRANSPORT-V1"
        or payload.get("key_wrap") != "RSA-OAEP-SHA256"
        or payload.get("content_cipher") != "AES-256-GCM"
        or payload.get("plaintext_stored_in_repository") is not False
    ):
        raise TrainingError("sealed answer-batch transport policy mismatch")
    return payload


def finalize_answer_transport(
    root: Path,
    key: str | bytes | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    plaintext = _decrypt_transport_batch(root, key)
    with tempfile.TemporaryDirectory(prefix="fortune-formal-answer-finalize-") as temporary:
        batch_path = Path(temporary) / "trusted-answer-batch.json"
        batch_path.write_bytes(plaintext)
        imported = import_answer_batch(root, batch_path, key)
    activated = activate_formal_controller(root, key)
    rehearsal = rehearse_formal_no_reveal(root)
    shutil.rmtree(root / TRANSPORT_DIR)
    return {
        "status": "FORMAL_ANSWER_IMPORT_FINALIZED",
        "answer_envelopes": imported["answer_envelopes"],
        "controller": activated["status"],
        "current_case_id": rehearsal["current_case_id"],
        "recommended_round_id": rehearsal["recommended_round_id"],
        "no_reveal_rehearsal": rehearsal["status"],
        "answers_disclosed": False,
        "transport_material_removed": True,
    }

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cryptography.fernet import Fernet

from fortune_v1.public_answer_vault import decrypt_answer_envelope, encrypt_answer_vector
from fortune_v1.util import FortuneError, read_json


class PublicAnswerVaultTests(unittest.TestCase):
    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    def answer(self, path: Path) -> None:
        self.write_json(path, {
            "schema": "GROUP-ANSWER-VECTOR-V1",
            "status": "REVEALED_FOR_TRAINING_AFTER_FREEZE",
            "group_run_id": "RUN-PUBLIC-1",
            "raw_answer_string": "A,B",
            "delimiter": ",",
            "rows": [
                {"case_id": "CASE-1", "question_id": "Q1", "answer_option_id": "A"},
                {"case_id": "CASE-1", "question_id": "Q2", "answer_option_id": "B"},
            ],
        })

    def test_round_trip_uses_public_envelope_and_transient_plaintext(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = root / "repo"
            transient = root / "transient"
            answer = root / "source-answer.json"
            envelope = repository / "public-answer-vault/encrypted/RUN-PUBLIC-1.json.fernet"
            decrypted = transient / "RUN-PUBLIC-1.json"
            self.answer(answer)
            key = Fernet.generate_key()

            encrypted = encrypt_answer_vector(answer, envelope, key)
            self.assertEqual(encrypted["status"], "ENCRYPTED_PUBLIC_STORAGE_READY")
            self.assertNotIn("A,B", envelope.read_text(encoding="utf-8"))

            receipt = decrypt_answer_envelope(envelope, decrypted, key, repository_root=repository)
            self.assertEqual(receipt["status"], "PASS")
            self.assertFalse(receipt["plaintext_committed_to_repository"])
            self.assertEqual(read_json(decrypted)["raw_answer_string"], "A,B")

    def test_wrong_key_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = root / "repo"
            answer = root / "source-answer.json"
            envelope = repository / "public-answer-vault/encrypted/RUN-PUBLIC-1.json.fernet"
            self.answer(answer)
            encrypt_answer_vector(answer, envelope, Fernet.generate_key())
            with self.assertRaises(FortuneError) as caught:
                decrypt_answer_envelope(envelope, root / "transient/answer.json", Fernet.generate_key(), repository_root=repository)
            self.assertEqual(caught.exception.status, "PUBLIC_ANSWER_DECRYPTION_FAILED")

    def test_plaintext_repository_output_is_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = root / "repo"
            answer = root / "source-answer.json"
            envelope = repository / "public-answer-vault/encrypted/RUN-PUBLIC-1.json.fernet"
            key = Fernet.generate_key()
            self.answer(answer)
            encrypt_answer_vector(answer, envelope, key)
            with self.assertRaises(FortuneError) as caught:
                decrypt_answer_envelope(envelope, repository / "plaintext.json", key, repository_root=repository)
            self.assertEqual(caught.exception.status, "DECRYPTED_ANSWER_REPOSITORY_WRITE_FORBIDDEN")


if __name__ == "__main__":
    unittest.main()

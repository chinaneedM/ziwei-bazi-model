from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cryptography.fernet import Fernet

import tests.test_end_to_end_pipeline as e2e_fixture
from fortune_v1.end_to_end import freeze_group_predictions, release_group_postblind, reveal_and_start_training
from fortune_v1.public_answer_vault import decrypt_answer_envelope, encrypt_answer_vector


class PublicEnvelopeEndToEndTests(unittest.TestCase):
    def test_public_envelope_reaches_learning_active_after_group_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            helper = e2e_fixture.EndToEndPipelineTests(methodName="runTest")
            run_root, _, release_request = helper.fixture(root)

            access = release_group_postblind(release_request)
            prediction = helper.prediction_bundle(run_root / "postblind-predictions/CASE-1.json")
            freeze_request = root / "runtime/group-freeze-requests/RUN-1.json"
            helper.write_json(freeze_request, {
                "schema": "GROUP-PREDICTION-FREEZE-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": "RUN-1",
                "group_postblind_access_path": access["output_path"],
                "output_root": str(run_root),
                "case_prediction_bundles": [
                    {"case_id": "CASE-1", "prediction_bundle_path": str(prediction)}
                ],
            })
            freeze = freeze_group_predictions(freeze_request)
            self.assertEqual(freeze["status"], "GROUP_PREDICTION_FREEZE_PASS")

            secure_local = root / "secure-local"
            plaintext_answer = secure_local / "RUN-1.json"
            helper.write_json(plaintext_answer, {
                "schema": "GROUP-ANSWER-VECTOR-V1",
                "status": "REVEALED_FOR_TRAINING_AFTER_FREEZE",
                "group_run_id": "RUN-1",
                "raw_answer_string": "A",
                "delimiter": ",",
                "unicode_codepoints": [65],
                "character_offsets": [{"index": 0, "character": "A", "codepoint": 65}],
                "rows": [
                    {"case_id": "CASE-1", "question_id": "Q1", "answer_option_id": "A"}
                ],
            })

            repository_root = root / "public-repository"
            envelope = repository_root / "public-answer-vault/encrypted/RUN-1.json.fernet"
            transient_root = root / "transient-answers"
            transient_answer = transient_root / "RUN-1.json"
            key = Fernet.generate_key()

            encrypted = encrypt_answer_vector(plaintext_answer, envelope, key)
            self.assertEqual(encrypted["status"], "ENCRYPTED_PUBLIC_STORAGE_READY")
            self.assertNotIn('"raw_answer_string":"A"', envelope.read_text(encoding="utf-8"))

            decryption = decrypt_answer_envelope(
                envelope,
                transient_answer,
                key,
                repository_root=repository_root,
            )
            self.assertEqual(decryption["status"], "PASS")
            self.assertFalse(decryption["plaintext_committed_to_repository"])

            reveal_request = root / "runtime/group-reveal-requests/RUN-1.json"
            helper.write_json(reveal_request, {
                "schema": "GROUP-REVEAL-TRAINING-REQUEST-V1",
                "status": "REQUESTED",
                "group_run_id": "RUN-1",
                "group_prediction_freeze_path": freeze["output_path"],
                "answer_vector_path": "RUN-1.json",
                "answer_vector_transport": "TRANSIENT_DECRYPTED_FROM_PUBLIC_ENVELOPE_AFTER_GROUP_FREEZE",
                "output_root": str(run_root / "training"),
                "cycle_id": "CYCLE-PUBLIC-RUN-1",
            })
            intake = reveal_and_start_training(reveal_request, answer_root=transient_root)
            self.assertEqual(intake["status"], "LEARNING_ACTIVE")
            self.assertEqual(intake["training_unit_count"], 1)


if __name__ == "__main__":
    unittest.main()

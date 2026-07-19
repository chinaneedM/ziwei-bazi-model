from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from fortune_v1.scoring import grade_frozen_prediction
from fortune_v1.topology import scan_runtime_workflows
from fortune_v1.util import FortuneError, sha256_file


class ReverseGradingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = Path(__file__).resolve().parents[1]

    def tearDown(self):
        self.tmp.cleanup()

    def _write_json(self, path: Path, value) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _valid_freeze(self, run_id: str = "RUN-TEST-001") -> tuple[Path, Path, Path]:
        prediction = self._write_json(self.root / "prediction-run.json", {
            "run_id": run_id,
            "questions": [
                {"question_id": "Q1", "option_ids": ["A", "B", "C", "D"], "top1": "A", "top2": "B"},
                {"question_id": "Q2", "option_ids": ["A", "B", "C", "D"], "top1": "C", "top2": "D"},
            ],
        })
        contract = self._write_json(self.root / "contract.json", {"schema": "PREDICTION-RUN-CONTRACT-V1"})
        receipt = self._write_json(self.root / "freeze-receipt.json", {
            "schema": "PREDICTION-FREEZE-RECEIPT-V1", "run_id": run_id,
            "prediction_path": str(prediction), "prediction_sha256": sha256_file(prediction),
            "contract_path": str(contract), "contract_sha256": sha256_file(contract),
            "runtime_validation": {"status": "PASS"}, "freeze_status": "PREDICTION_FROZEN",
            "immutable": True, "non_overwrite": True,
        })
        answer = self._write_json(self.root / "answer.json", {
            "schema": "FORTUNE-ANSWER-OBJECT-V1", "authorized_run_id": run_id, "answers": "A,C"})
        return receipt, prediction, answer

    def test_active_runtime_has_no_private_vault_path(self):
        result = scan_runtime_workflows(self.repo)
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["runtime_repository_vault_credential"], "NONE")

        verifier = subprocess.run(
            [
                sys.executable,
                str(self.repo / "scripts/verify-public-only-repository.py"),
                "--root",
                str(self.repo),
                "--visibility",
                "public",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(verifier.returncode, 0, verifier.stdout + verifier.stderr)
        receipt = json.loads(verifier.stdout)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["legacy_quarantine_status"], "PASS")
        self.assertFalse((self.repo / ".github/workflows/grade-frozen.yml").exists())

    def test_public_reveal_workflow_order_and_secret_boundary(self):
        path = self.repo / ".github/workflows/repository-group-reveal-training.yml"
        text = path.read_text(encoding="utf-8")
        markers = [
            "Verify group freeze and public encrypted answer paths",
            "Require public encrypted answer key",
            "Decrypt public envelopes only after freeze PASS",
            "Literal replay and start learning cycle",
            "Destroy transient answer plaintext",
        ]
        order = [text.index(marker) for marker in markers]
        self.assertEqual(order, sorted(order))
        self.assertNotIn("pull_request:", text)
        self.assertIn("secrets.FORTUNE_PUBLIC_ANSWER_KEY", text)
        self.assertIn("/tmp/fortune-public-answer-vault", text)
        self.assertIn("public-answer-vault/encrypted", text)

    def test_public_answer_repository_accepts_encrypted_envelopes_only(self):
        ignore = (self.repo / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("public-answer-vault/**", ignore)
        self.assertIn("!public-answer-vault/encrypted/*.json.fernet", ignore)
        self.assertIn("*.decrypted-answer.json", ignore)
        readme = (self.repo / "public-answer-vault/README.md").read_text(encoding="utf-8")
        self.assertIn("encrypted", readme.lower())
        self.assertNotIn("FORTUNE_PUBLIC_ANSWER_KEY=", readme)

    def test_missing_or_invalid_freeze_does_not_read_answer(self):
        fake = self._write_json(self.root / "invalid-freeze.json", {"schema": "wrong"})
        with mock.patch("fortune_v1.scoring.literal_replay") as replay:
            with self.assertRaises(FortuneError):
                grade_frozen_prediction(fake, self.root / "must-not-read.json", self.root / "out.json", expected_run_id="RUN-X")
            replay.assert_not_called()
        receipt, prediction, _ = self._valid_freeze()
        prediction.write_text("changed", encoding="utf-8")
        with mock.patch("fortune_v1.scoring.literal_replay") as replay:
            with self.assertRaises(FortuneError):
                grade_frozen_prediction(receipt, self.root / "must-not-read.json", self.root / "out2.json", expected_run_id="RUN-TEST-001")
            replay.assert_not_called()

    def test_valid_freeze_allows_grade_top1_formal_top2_diagnostic_and_immutable_prediction(self):
        receipt, prediction, answer = self._valid_freeze()
        before = sha256_file(prediction)
        output = self.root / "reveal.json"
        result = grade_frozen_prediction(receipt, answer, output, expected_run_id="RUN-TEST-001")
        self.assertEqual(result["pre_answer_freeze_validation"]["status"], "PASS")
        self.assertEqual(result["score"]["top1_correct"], 2)
        self.assertFalse(result["score"]["top2_is_formal_score"])
        self.assertEqual(result["literal_replay"]["parser_a"], result["literal_replay"]["parser_b"])
        self.assertEqual(before, sha256_file(prediction))
        with self.assertRaises(FortuneError):
            grade_frozen_prediction(receipt, answer, output, expected_run_id="RUN-TEST-001")

    def test_answer_run_id_mismatch_is_rejected(self):
        receipt, _, answer = self._valid_freeze()
        obj = json.loads(answer.read_text(encoding="utf-8"))
        obj["authorized_run_id"] = "RUN-WRONG"
        answer.write_text(json.dumps(obj), encoding="utf-8")
        with self.assertRaises(FortuneError) as ctx:
            grade_frozen_prediction(receipt, answer, self.root / "out.json", expected_run_id="RUN-TEST-001")
        self.assertEqual(ctx.exception.status, "ANSWER_OBJECT_RUN_ID_MISMATCH")


if __name__ == "__main__":
    unittest.main()

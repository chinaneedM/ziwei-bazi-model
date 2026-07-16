from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from fortune_v1.scoring import grade_frozen_prediction
from fortune_v1.topology import scan_runtime_workflows, verify_topology
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

    def test_runtime_workflows_have_no_vault_path(self):
        result = scan_runtime_workflows(self.repo)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["runtime_repository_vault_credential"], "NONE")
        all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in self.repo.rglob("*")
                             if path.is_file() and ".git" not in path.parts and "templates" not in path.parts
                             and "__pycache__" not in path.parts)
        self.assertNotIn("ANSWER_" + "VAULT_TOKEN", all_text)
        self.assertFalse((self.repo / ".github/workflows/grade-frozen.yml").exists())

    def test_vault_workflow_order_and_write_allowlist(self):
        path = self.repo / "templates/answer-vault/.github/workflows/grade-frozen-prediction.yml"
        text = path.read_text(encoding="utf-8")
        order = [text.index(marker) for marker in ["Checkout runtime repository", "Validate immutable freeze before any answer access",
                                                    "Checkout current answer vault only after freeze validation",
                                                    "Grade frozen prediction", "Remove answer worktree and caches before commit",
                                                    "Commit only the new reveal"]]
        self.assertEqual(order, sorted(order))
        self.assertIn("secrets.RUNTIME_REPO_TOKEN", text)
        self.assertIn('test "$(git diff --cached --name-only)" = "$reveal"', text)
        self.assertIn("Reject reveal overwrite", text)

    def test_token_scope_probe_requires_runtime_allow_and_vault_denial(self):
        config = self.repo / "config/github-topology.json"
        statuses = {
            ("chinaneedM/ziwei-bazi-model", "runtime-secret"): (200, {"private": True}),
            ("chinaneedM/fortune-answer-vault", "runtime-secret"): (404, None),
            ("chinaneedM/fortune-answer-vault", "vault-self"): (200, {"private": True}),
            ("chinaneedM/ziwei-bazi-model", "vault-self"): (404, None),
        }
        with mock.patch.dict(os.environ, {"RUNTIME_REPO_TOKEN": "runtime-secret", "VAULT_SELF_TOKEN": "vault-self"}), \
             mock.patch("fortune_v1.topology._github_get", side_effect=lambda repo, token: statuses[(repo, token)]):
            result = verify_topology(config, self.root / "topology.json")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checks"]["TOKEN_REPOSITORY_SCOPE"], "PASS")
        self.assertEqual(result["checks"]["RUNTIME_VAULT_ACCESS_DENIAL"], "PASS")
        self.assertEqual(result["checks"]["FREE_PLAN_CONTROL_LIMITATION"], "RECORDED")

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
        obj = json.loads(answer.read_text(encoding="utf-8")); obj["authorized_run_id"] = "RUN-WRONG"
        answer.write_text(json.dumps(obj), encoding="utf-8")
        with self.assertRaises(FortuneError) as ctx:
            grade_frozen_prediction(receipt, answer, self.root / "out.json", expected_run_id="RUN-TEST-001")
        self.assertEqual(ctx.exception.status, "ANSWER_OBJECT_RUN_ID_MISMATCH")

    def test_initialization_template_contains_no_real_answer_token_zip_rar_or_shadow(self):
        root = self.repo / "templates/answer-vault"
        payload = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in root.rglob("*") if path.is_file())
        self.assertNotIn("ghp_", payload)
        self.assertNotIn("github_pat_", payload)
        self.assertFalse(any(path.suffix.lower() in {".zip", ".rar"} for path in root.rglob("*")))
        self.assertFalse(any("shadow_rebuild" in path.name.lower() for path in root.rglob("*")))


if __name__ == "__main__":
    unittest.main()

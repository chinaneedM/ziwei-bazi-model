import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.group import authorize_group_reveal, create_dev_group, register_baseline_freeze
from fortune_v1.util import FortuneError, sha256_file


class GroupFreezeValidationTests(unittest.TestCase):
    def _write_valid_freeze(self, root: Path, binding: dict) -> Path:
        prediction = root / "prediction.json"
        contract = root / "contract.json"
        prediction.write_text(json.dumps({
            "schema": "PREDICTION-RUN-V1",
            "run_id": "RUN-CASE-001",
            "case_id": "CASE-001",
            "binding": binding,
            "questions": [],
        }), encoding="utf-8")
        contract.write_text(json.dumps({"schema": "PREDICTION-RUN-CONTRACT-V1"}), encoding="utf-8")
        receipt = root / "freeze-receipt.json"
        receipt.write_text(json.dumps({
            "schema": "PREDICTION-FREEZE-RECEIPT-V1",
            "case_id": "CASE-001",
            "run_id": "RUN-CASE-001",
            "prediction_path": str(prediction),
            "prediction_sha256": sha256_file(prediction),
            "contract_path": str(contract),
            "contract_sha256": sha256_file(contract),
            "freeze_status": "PREDICTION_FROZEN",
            "runtime_validation": {"status": "PASS"},
            "immutable": True,
            "non_overwrite": True,
        }), encoding="utf-8")
        return receipt

    def test_register_rejects_unvalidated_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group_root = root / "groups"
            create_dev_group("GROUP-001", ["CASE-001"], {"version": "R1"}, group_root, expected_size=1)
            bad = root / "bad.json"
            bad.write_text(json.dumps({"case_id": "CASE-001", "run_id": "RUN-CASE-001"}), encoding="utf-8")
            with self.assertRaises(FortuneError):
                register_baseline_freeze(group_root / "GROUP-001", bad)

    def test_authorize_replays_freeze_validation_and_detects_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            binding = {"version": "R1"}
            group_root = root / "groups"
            create_dev_group("GROUP-001", ["CASE-001"], binding, group_root, expected_size=1)
            receipt = self._write_valid_freeze(root, binding)
            registered = register_baseline_freeze(group_root / "GROUP-001", receipt)
            self.assertEqual(registered["status"], "BASELINE_GROUP_FROZEN")
            prediction = root / "prediction.json"
            prediction.write_text(prediction.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            with self.assertRaises(FortuneError):
                authorize_group_reveal(group_root / "GROUP-001")


if __name__ == "__main__":
    unittest.main()

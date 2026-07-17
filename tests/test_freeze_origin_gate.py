from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.external_runner import (
    freeze_chat_work_prediction,
    import_chat_work_prediction,
)
from fortune_v1.util import FortuneError
from test_external_runner import ChatWorkRunnerTests


class FreezeOriginGateTests(unittest.TestCase):
    def test_valid_handoff_can_freeze(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = ChatWorkRunnerTests()
            run_path, contract_path, _, _ = fixture._fixtures(root)
            imported = root / "prediction-run.json"
            handoff = root / "handoff-receipt.json"
            import_chat_work_prediction(
                run_path,
                contract_path,
                imported,
                handoff,
                "CHAT_ONLY",
                "SESSION-1",
            )
            receipt = freeze_chat_work_prediction(
                imported,
                contract_path,
                handoff,
                root / "frozen",
            )
            self.assertEqual(receipt["freeze_status"], "PREDICTION_FROZEN")
            self.assertEqual(receipt["prediction_origin"], "CHAT_WORK_HANDOFF_VERIFIED")
            self.assertEqual(receipt["origin_validation"]["status"], "PASS")

    def test_missing_handoff_receipt_blocks_freeze(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = ChatWorkRunnerTests()
            run_path, contract_path, _, _ = fixture._fixtures(root)
            with self.assertRaises(FortuneError) as ctx:
                freeze_chat_work_prediction(
                    run_path,
                    contract_path,
                    root / "missing.json",
                    root / "frozen",
                )
            self.assertEqual(ctx.exception.status, "HANDOFF_RECEIPT_MISSING")
            self.assertFalse((root / "frozen").exists())

    def test_prediction_tamper_after_handoff_blocks_freeze(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = ChatWorkRunnerTests()
            run_path, contract_path, _, _ = fixture._fixtures(root)
            imported = root / "prediction-run.json"
            handoff = root / "handoff-receipt.json"
            import_chat_work_prediction(
                run_path,
                contract_path,
                imported,
                handoff,
                "CHAT_ONLY",
                "SESSION-1",
            )
            payload = json.loads(imported.read_text(encoding="utf-8"))
            payload["questions"][0]["confidence"] = 0.7
            imported.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(FortuneError) as ctx:
                freeze_chat_work_prediction(
                    imported,
                    contract_path,
                    handoff,
                    root / "frozen",
                )
            self.assertEqual(ctx.exception.status, "HANDOFF_RECEIPT_INVALID")
            self.assertFalse((root / "frozen").exists())


if __name__ == "__main__":
    unittest.main()

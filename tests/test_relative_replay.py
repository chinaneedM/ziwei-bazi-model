import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.relative_replay import freeze_relative_replay, validate_relative_replay
from fortune_v1.util import FortuneError


def valid_object():
    return {
        "schema": "RELATIVE-PREDICTION-REPLAY-V1",
        "run_id": "RELATIVE-TEST-001",
        "case_id": "CASE-001",
        "dataset_type": "DEV",
        "cold_start": True,
        "answer_access_performed": False,
        "retrospective_replay": True,
        "formal_validity": "INVALID_UNSEALED",
        "formal_prediction_frozen": False,
        "s03_formal_fusion_performed": False,
        "input_reference": {"kind": "ANSWER_ISOLATED_SOURCE_CASE", "path": "case.json", "sha256": "abc"},
        "top1_vector": "A",
        "top2_vector": "B",
        "questions": [
            {
                "question_id": "Q1",
                "option_ids": ["A", "B"],
                "top1": "A",
                "top2": "B",
                "confidence": 0.5,
                "pairwise_rows": [
                    {
                        "left": "A",
                        "right": "B",
                        "winner": "A",
                        "decision_basis": "A has better relative coverage",
                        "distinctive_atom_comparison": {"A": "supported", "B": "limited"},
                    }
                ],
                "track_replay_status": {"ziwei": "UNSEALED_REPLAY_ONLY", "bazi": "UNSEALED_REPLAY_ONLY"},
                "strongest_competitor_reason": "B is the only competitor.",
                "most_important_unverified_atom": "Exact endpoint.",
                "formal_exact_assertion": None,
            }
        ],
    }


class RelativeReplayTests(unittest.TestCase):
    def test_valid_relative_replay_passes(self):
        result = validate_relative_replay(valid_object())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["errors"], [])

    def test_formal_assertion_is_rejected(self):
        obj = valid_object()
        obj["questions"][0]["formal_exact_assertion"] = "not allowed"
        result = validate_relative_replay(obj)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Q1:FORMAL_EXACT_ASSERTION_MUST_BE_NULL", result["errors"])

    def test_answer_access_is_rejected(self):
        obj = valid_object()
        obj["answer_access_performed"] = True
        result = validate_relative_replay(obj)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("ANSWER_ACCESS_ATTESTATION_INVALID", result["errors"])

    def test_freeze_is_non_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            obj_path = root / "candidate.json"
            obj_path.write_text(json.dumps(valid_object()), encoding="utf-8")
            receipt = freeze_relative_replay(obj_path, root / "frozen")
            self.assertEqual(receipt["freeze_status"], "RELATIVE_REPLAY_FROZEN")
            self.assertFalse(receipt["formal_prediction_frozen"])
            with self.assertRaises(FortuneError):
                freeze_relative_replay(obj_path, root / "frozen")


if __name__ == "__main__":
    unittest.main()

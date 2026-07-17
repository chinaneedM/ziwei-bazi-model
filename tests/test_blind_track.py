import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.blind_track import create_local_track_seal, seal_blind_track_model, validate_blind_track_model
from fortune_v1.util import FortuneError


def blind_candidate(track="ZIWEI"):
    return {
        "schema": "BLIND-TRACK-MODEL-V1",
        "case_id": "CASE-NEW-001",
        "track": track,
        "phase": "PRE_OPTION",
        "option_visibility": False,
        "other_track_visibility": False,
        "answer_access_performed": False,
        "parent_libraries": ["S05", "S06", "S17"] if track == "ZIWEI" else ["S11", "S12", "S17"],
        "blind_model": {
            "structural_seed": "independent sealed structural summary",
            "supporting_mechanisms": ["mechanism one"],
            "limitations": ["no exact real-world endpoint"],
        },
    }


class BlindTrackTests(unittest.TestCase):
    def test_pre_option_blind_model_passes(self):
        result = validate_blind_track_model(blind_candidate())
        self.assertEqual(result["status"], "PASS")

    def test_option_key_is_rejected(self):
        obj = blind_candidate()
        obj["blind_model"]["top1"] = "A"
        result = validate_blind_track_model(obj)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("OPTION_OR_ADJUDICATION_KEY_DETECTED", result["errors"])

    def test_cross_track_parent_is_rejected(self):
        obj = blind_candidate("ZIWEI")
        obj["parent_libraries"].append("S12")
        result = validate_blind_track_model(obj)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("CROSS_TRACK_PARENT_CONTAMINATION", result["errors"])

    def test_two_stage_seal_produces_validator_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate_path = root / "blind.json"
            candidate_path.write_text(json.dumps(blind_candidate()), encoding="utf-8")
            receipt = seal_blind_track_model(candidate_path, root / "blind-frozen")
            self.assertEqual(receipt["validation_status"], "PASS")
            self.assertTrue(receipt["blind_model_hash"])

            receipt_path = Path(receipt["frozen_path"]).parent / "blind-track-seal-receipt.json"
            adjudication = {
                "schema": "TRACK-LOCAL-ADJUDICATION-V1",
                "case_id": "CASE-NEW-001",
                "question_id": "Q1",
                "track": "ZIWEI",
                "blind_model_hash": receipt["blind_model_hash"],
                "s18_local_adjudication_object_id": "S18-Q1-ZIWEI-001",
                "parent_object_ids": ["COVERAGE-Q1-ZIWEI", "PAIRWISE-Q1-ZIWEI"],
                "answer_access_performed": False,
                "other_track_visibility": False,
                "adjudication_body": {"relative_top1": "A", "relative_top2": "B"},
            }
            adjudication_path = root / "adjudication.json"
            adjudication_path.write_text(json.dumps(adjudication), encoding="utf-8")
            seal = create_local_track_seal(adjudication_path, receipt_path, root / "local-seal.json")
            for field in (
                "seal_id", "canonical_hash", "body_hash", "machine_validation_report_id",
                "validation_status", "s18_local_adjudication_object_id", "parent_object_ids",
            ):
                self.assertIn(field, seal)
            self.assertEqual(seal["validation_status"], "PASS")

    def test_blind_seal_is_non_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate_path = root / "blind.json"
            candidate_path.write_text(json.dumps(blind_candidate()), encoding="utf-8")
            seal_blind_track_model(candidate_path, root / "blind-frozen")
            with self.assertRaises(FortuneError):
                seal_blind_track_model(candidate_path, root / "blind-frozen")


if __name__ == "__main__":
    unittest.main()

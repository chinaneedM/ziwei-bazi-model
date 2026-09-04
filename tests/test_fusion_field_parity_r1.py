from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "config" / "fusion-field-parity-r1.json"

ALLOWED_CLASSIFICATIONS = {
    "ALREADY_RELEASED_AND_VISIBLE",
    "ALREADY_RELEASED_NOT_YET_VISIBLE",
    "DETERMINISTIC_RUNTIME_MISSING",
    "SOURCE_PROFILE_OR_SCHOOL_CONFLICT",
    "REFERENCE_PRODUCT_ONLY",
    "INTERPRETIVE_OR_PREDICTIVE_OUT_OF_SCOPE",
}


class FusionFieldParityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))

    def test_matrix_identity_and_authority_boundary_are_explicit(self) -> None:
        self.assertEqual("FUSION-CHART-FIELD-PARITY-R1", self.matrix["schema"])
        self.assertEqual(
            "FUSION-CHART-FIELD-CLOSURE-AUDIT-R1",
            self.matrix["audit_id"],
        )
        authority = self.matrix["authority_policy"]
        self.assertEqual("REFERENCE_COMPATIBILITY_ONLY", authority["wenmo_tianji"])
        self.assertEqual("REFERENCE_COMPATIBILITY_ONLY", authority["wenzhen_bazi"])
        self.assertTrue(authority["no_reference_product_may_override_source_profile"])

    def test_classification_vocabulary_is_closed_and_rows_are_unique(self) -> None:
        self.assertEqual(
            ALLOWED_CLASSIFICATIONS,
            set(self.matrix["classification_vocabulary"]),
        )
        rows = self.matrix["rows"]
        field_ids = [row["field_id"] for row in rows]
        self.assertEqual(len(field_ids), len(set(field_ids)))
        self.assertGreaterEqual(len(rows), 25)
        for row in rows:
            with self.subTest(field_id=row["field_id"]):
                self.assertIn(row["classification"], ALLOWED_CLASSIFICATIONS)
                self.assertIn(row["system"], {"FUSION", "BAZI", "ZIWEI"})
                self.assertTrue(row["display_name"].strip())
                self.assertIsInstance(row["runtime_evidence"], list)
                self.assertIsInstance(row["reference_evidence"], list)
                self.assertTrue(row["next_action"].strip())

    def test_priority_queue_contains_only_open_charting_work(self) -> None:
        rows = {row["field_id"]: row for row in self.matrix["rows"]}
        queue = self.matrix["priority_queue"]
        self.assertEqual(len(queue), len(set(queue)))
        for field_id in queue:
            with self.subTest(field_id=field_id):
                self.assertIn(field_id, rows)
                self.assertIn(
                    rows[field_id]["classification"],
                    {
                        "ALREADY_RELEASED_NOT_YET_VISIBLE",
                        "DETERMINISTIC_RUNTIME_MISSING",
                        "SOURCE_PROFILE_OR_SCHOOL_CONFLICT",
                    },
                )
        self.assertNotIn("PREDICTION_INTERPRETATION", queue)

    def test_shared_time_and_r2_fusion_remain_released_visible_baselines(self) -> None:
        rows = {row["field_id"]: row for row in self.matrix["rows"]}
        self.assertEqual(
            "ALREADY_RELEASED_AND_VISIBLE",
            rows["SHARED_TIME_CREDENTIAL"]["classification"],
        )
        self.assertEqual(
            "ALREADY_RELEASED_AND_VISIBLE",
            rows["SHARED_TARGET_FUSION_R2"]["classification"],
        )
        self.assertEqual(
            "SOURCE_PROFILE_OR_SCHOOL_CONFLICT",
            rows["BAZI_XIAOYUN"]["classification"],
        )

    def test_closed_ziwei_basic_and_overlap_fields_are_visible(self) -> None:
        rows = {row["field_id"]: row for row in self.matrix["rows"]}
        for field_id in (
            "ZIWEI_ROLE_BINDINGS",
            "ZIWEI_FIVE_ELEMENT_BUREAU",
            "ZIWEI_BODY_PALACE",
            "ZIWEI_LIMIT_FLOW_OVERLAP_LABEL",
        ):
            with self.subTest(field_id=field_id):
                self.assertEqual(
                    "ALREADY_RELEASED_AND_VISIBLE",
                    rows[field_id]["classification"],
                )
                self.assertTrue(
                    any(
                        "ziwei_basic_info_assets.py" in evidence
                        for evidence in rows[field_id]["runtime_evidence"]
                    )
                )
        self.assertEqual(
            "DETERMINISTIC_RUNTIME_MISSING",
            rows["ZIWEI_SELF_TRANSFORMATION"]["classification"],
        )
        self.assertEqual(["ZIWEI_SELF_TRANSFORMATION"], self.matrix["priority_queue"])

    def test_reference_only_differences_cannot_enter_runtime_as_authority(self) -> None:
        for row in self.matrix["rows"]:
            with self.subTest(field_id=row["field_id"]):
                for evidence in row["reference_evidence"]:
                    if evidence.startswith("WENMO:") or evidence.startswith("WENZHEN:"):
                        self.assertNotEqual(
                            "REFERENCE_PRODUCT_ONLY",
                            self.matrix["authority_policy"]["repository_runtime_contracts"],
                        )
        self.assertEqual(
            "DO_NOT_IMPLEMENT_IN_CHARTING_PHASE",
            next(
                row for row in self.matrix["rows"]
                if row["field_id"] == "PREDICTION_INTERPRETATION"
            )["next_action"],
        )


if __name__ == "__main__":
    unittest.main()

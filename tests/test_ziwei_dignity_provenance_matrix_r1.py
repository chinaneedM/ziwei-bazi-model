from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
RELEASE_DOC = ROOT / "docs" / "ZIWEI-DIGNITY-ANNOTATION-PROVENANCE-R1.md"
FEATURE_COMMIT = "17989e8769bfdb9f20c11ba227b86966d261f373"


class ZiweiDignityProvenanceMatrixR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in cls.matrix["fields"]}
        cls.release_doc = RELEASE_DOC.read_text(encoding="utf-8")

    def test_matrix_baseline_and_released_row(self) -> None:
        self.assertEqual(self.matrix["evidence_baseline_commit"], FEATURE_COMMIT)
        row = self.rows["ZIWEI_DIGNITY_ANNOTATION_PROVENANCE"]
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertEqual(row["system"], "ZIWEI")
        self.assertIn("dignity_provenance.py", row["backend_evidence"]["path"])
        self.assertIn("ziwei_dignity_provenance_local_app.py", row["api_evidence"]["path"])
        self.assertIn("ziwei_dignity_provenance_assets.py", row["workbench_evidence"]["path"])

    def test_matrix_preserves_operational_vs_s01_boundary(self) -> None:
        row = self.rows["ZIWEI_DIGNITY_ANNOTATION_PROVENANCE"]
        text = json.dumps(row, ensure_ascii=False)
        self.assertIn("PROJECT_OPERATIONAL_REGISTRY", text)
        self.assertIn("NOT_CLAIMED", text)
        self.assertIn("S01", text)
        self.assertIn("provenance", text.lower())
        self.assertNotIn("canonical S01 brightness", text)
        self.assertNotIn("吉星", text)
        self.assertNotIn("煞星", text)

    def test_self_inward_direction_remains_not_formalized(self) -> None:
        row = self.rows["ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION"]
        self.assertEqual(row["status"], "NOT_YET_FORMALIZED")
        self.assertIn("must not be promoted", row["notes"])

    def test_release_doc_locks_exact_semantic_boundary(self) -> None:
        self.assertIn(
            "EXISTING_DIGNITY_ANNOTATION_PROVENANCE_ONLY_NOT_S01_FROZEN_BRIGHTNESS_"
            "NO_AUSPICIOUSNESS_STRENGTH_OR_PREDICTION",
            self.release_doc,
        )
        self.assertIn("authority_class = PROJECT_OPERATIONAL_REGISTRY", self.release_doc)
        self.assertIn("s01_brightness_authority = NOT_CLAIMED", self.release_doc)
        self.assertIn("S01_RECALCULATE_BRIGHTNESS_PERMISSION=NO", self.release_doc)
        self.assertIn("SOURCE_BRIGHTNESS_REFERENCE_CAN_OVERWRITE=NO", self.release_doc)


if __name__ == "__main__":
    unittest.main()

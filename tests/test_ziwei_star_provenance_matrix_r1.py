from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
RELEASE = ROOT / "docs" / "ZIWEI-STAR-PLACEMENT-PROVENANCE-R1.md"


class ZiweiStarProvenanceMatrixR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        payload = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.payload = payload
        cls.rows = {row["field_id"]: row for row in payload["fields"]}
        cls.release = RELEASE.read_text(encoding="utf-8")

    def test_matrix_registers_green_feature_baseline(self) -> None:
        self.assertEqual(
            self.payload["evidence_baseline_commit"],
            "17989e8769bfdb9f20c11ba227b86966d261f373",
        )
        row = self.rows["ZIWEI_STAR_PLACEMENT_PROVENANCE"]
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertIn("generator_id", row["backend_evidence"]["claim"])
        self.assertIn("source_refs", row["backend_evidence"]["claim"])
        self.assertIn("no auspiciousness", row["notes"].lower())
        self.assertIn("no doctrinal", row["notes"].lower())

    def test_release_boundary_is_provenance_only(self) -> None:
        for expected in (
            "ZIWEI-STAR-PLACEMENT-PROVENANCE-SIDECAR-R1",
            "PLACEMENT_GENERATOR_PROVENANCE_ONLY_NO_AUSPICIOUSNESS_OR_DOCTRINAL_STAR_CLASSIFICATION",
            "GENERATOR_IDENTITY_AND_RELEASED_MAIN_STAR_SOURCE_REFS_ONLY",
            "FOURTEEN_MAIN_STARS",
            "CORE_AUXILIARY",
            "DERIVED_AUXILIARY",
            "OPERATIONAL_MINOR_STARS",
            "ZIWEI_SYSTEM",
            "TIANFU_SYSTEM",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.release)

    def test_self_inward_direction_remains_unformalized(self) -> None:
        row = self.rows["ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION"]
        self.assertEqual(row["status"], "NOT_YET_FORMALIZED")
        self.assertIn("must not be promoted by geometry alone", row["notes"])


if __name__ == "__main__":
    unittest.main()

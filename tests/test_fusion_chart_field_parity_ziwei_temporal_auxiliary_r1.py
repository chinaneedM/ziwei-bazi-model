from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads((ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json").read_text(encoding="utf-8"))
RINGS = (ROOT / "src" / "fortune_training" / "ziwei_chart" / "rings.py").read_text(encoding="utf-8")
TEMPORAL_AUX = (ROOT / "src" / "fortune_training" / "ziwei_chart" / "temporal_auxiliary.py").read_text(encoding="utf-8")
VIEW = (ROOT / "src" / "fortune_training" / "ziwei_chart" / "view.py").read_text(encoding="utf-8")
SVG = (ROOT / "src" / "fortune_training" / "ziwei_application" / "svg.py").read_text(encoding="utf-8")


class FusionChartFieldParityZiweiTemporalAuxiliaryR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = {row["field_id"]: row for row in MATRIX["fields"]}

    def test_four_released_ring_families_are_registered_visible(self) -> None:
        expected = {
            "ZIWEI_RING_CHANGSHENG12": "RING.CHANGSHENG12",
            "ZIWEI_RING_TAISUI12": "RING.TAISUI12",
            "ZIWEI_RING_JIANGQIAN12": "RING.JIANGQIAN12",
            "ZIWEI_RING_BOSHI12": "RING.BOSHI12",
        }
        for field_id, ring_id in expected.items():
            with self.subTest(field_id=field_id):
                row = self.rows[field_id]
                self.assertEqual("ZIWEI", row["system"])
                self.assertEqual("ALREADY_VISIBLE", row["status"])
                self.assertEqual("src/fortune_training/ziwei_chart/rings.py", row["backend_evidence"]["path"])
                self.assertEqual("src/fortune_training/ziwei_application/svg.py", row["workbench_evidence"]["path"])
                self.assertIn(ring_id, RINGS)
        for label in ("长生十二神", "岁前十二神", "将前十二神", "博士十二神"):
            self.assertIn(label, RINGS)
        self.assertIn("环: ", SVG)

    def test_dynamic_auxiliary_surface_stays_candidate_only_after_visibility_closure(self) -> None:
        row = self.rows["ZIWEI_TEMPORAL_AUXILIARY_CANDIDATES"]
        self.assertEqual("ZIWEI", row["system"])
        self.assertEqual("DISPUTED_CANDIDATE_ONLY", row["status"])
        self.assertEqual("src/fortune_training/ziwei_chart/temporal_auxiliary.py", row["backend_evidence"]["path"])
        self.assertEqual("src/fortune_training/ziwei_application/svg.py", row["workbench_evidence"]["path"])
        self.assertIn("ViewTemporalAuxiliaryCandidate", row["api_evidence"]["symbol"])
        for field_name in (
            "candidate_set_id",
            "candidate_id",
            "frame_type",
            "frame_id",
            "entity_id",
            "method_id",
            "authority_status",
        ):
            self.assertIn(field_name, row["api_evidence"]["claim"])
        self.assertIn("fact hash", row["api_evidence"]["claim"])
        self.assertIn("candidate_set_hash", row["api_evidence"]["claim"])
        self.assertIn("star_id", row["api_evidence"]["claim"])
        self.assertIn('KUI_YUE_SELECTION_STATUS = "CANDIDATES_PRESERVED_NO_SELECTION"', TEMPORAL_AUX)
        self.assertIn('STRICT_KUI_YUE_METHOD_ID = "S01-QS-STRICT-KUI-YUE-R1"', TEMPORAL_AUX)
        self.assertIn('WENMO_KUI_YUE_METHOD_ID = "COMPAT-WENMO-KUI-YUE-R1"', TEMPORAL_AUX)
        self.assertIn('LIMIT_TIANMA_METHOD_ID = "S10-LIMIT-PALACE-BRANCH-TIANMA-CASE-R1"', TEMPORAL_AUX)
        self.assertIn('ANNUAL_TIANMA_METHOD_ID = "S10-ANNUAL-BRANCH-TIANMA-CASE-R1"', TEMPORAL_AUX)
        self.assertIn('TIANMA_SELECTION_STATUS = "CASE_METHOD_CANDIDATE_PRESERVED_NO_SELECTION"', TEMPORAL_AUX)
        self.assertIn("class ViewTemporalAuxiliaryCandidate:", VIEW)
        self.assertIn("    frame_id: str", VIEW)
        self.assertIn("    entity_id: str", VIEW)
        self.assertIn("    candidate_fact_hash: str", VIEW)
        self.assertIn('class="temporal-auxiliary-candidate"', SVG)
        self.assertIn('data-frame-id=', SVG)
        self.assertIn('data-entity-id=', SVG)
        self.assertIn('data-method-id=', SVG)
        self.assertIn('data-authority-status=', SVG)
        self.assertNotIn('data-candidate-set-hash=', SVG)
        self.assertNotIn('data-star-id=', SVG)
        self.assertNotIn('data-selected=', SVG)
        self.assertNotIn('data-winner=', SVG)
        self.assertNotIn('data-rank=', SVG)


if __name__ == "__main__":
    unittest.main()

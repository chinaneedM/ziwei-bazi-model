from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.bazi_pillar_metadata_assets import (
    BAZI_PILLAR_METADATA_JS,
)
from fortune_training.combined_chart_application.target_flow_ziwei_projection_assets import (
    TARGET_FLOW_ZIWEI_PROJECTION_JS,
)
from fortune_training.combined_chart_application.ziwei_basic_info_assets import (
    ZIWEI_BASIC_INFO_JS,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
SCHEMA_PATH = ROOT / "schemas" / "fusion-chart-field-parity-matrix-r1.schema.json"
BAZI_SERVICE_PATH = ROOT / "src" / "fortune_training" / "bazi_application" / "service.py"


class FusionChartFieldParityMatrixR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in cls.matrix["fields"]}
        cls.bazi_service = BAZI_SERVICE_PATH.read_text(encoding="utf-8")

    def test_matrix_contract_and_field_ids_are_stable(self) -> None:
        self.assertEqual(self.matrix["schema"], "FUSION-CHART-FIELD-PARITY-MATRIX-R1")
        self.assertEqual(self.matrix["version"], "1.0.0")
        self.assertEqual(len(self.rows), len(self.matrix["fields"]))
        self.assertEqual(
            set(self.matrix["status_definitions"]),
            {
                "ALREADY_VISIBLE",
                "ALREADY_RELEASED_NOT_YET_VISIBLE",
                "NOT_YET_FORMALIZED",
                "DISPUTED_CANDIDATE_ONLY",
            },
        )
        self.assertEqual(
            self.schema["properties"]["schema"]["const"],
            "FUSION-CHART-FIELD-PARITY-MATRIX-R1",
        )

    def test_every_evidence_path_exists(self) -> None:
        for row in self.matrix["fields"]:
            for key in ("backend_evidence", "api_evidence", "workbench_evidence"):
                with self.subTest(field_id=row["field_id"], evidence=key):
                    self.assertTrue((ROOT / row[key]["path"]).exists(), row[key]["path"])

    def test_current_visible_bazi_fields_are_not_misclassified_as_missing(self) -> None:
        expected_visible = {
            "BAZI_PILLAR_GANZHI",
            "BAZI_VISIBLE_TEN_GOD",
            "BAZI_HIDDEN_STEMS",
            "BAZI_XUNKONG",
            "BAZI_TWELVE_GROWTH",
            "BAZI_DERIVED_COORDINATES",
            "BAZI_XIAOYUN_CANDIDATES",
            "BAZI_SHENSHA_FACT_CANDIDATES",
            "BAZI_NAYIN",
            "BAZI_DAYUN",
            "BAZI_STEM_ELEMENT",
            "BAZI_STEM_POLARITY",
            "BAZI_BRANCH_ELEMENT_AFFILIATION",
            "SHARED_TIME_CREDENTIAL",
        }
        for field_id in expected_visible:
            with self.subTest(field_id=field_id):
                self.assertEqual(self.rows[field_id]["status"], "ALREADY_VISIBLE")

    def test_released_bazi_pillar_metadata_is_now_visible_read_only(self) -> None:
        fields = {
            "BAZI_STEM_ELEMENT": "stem_element",
            "BAZI_STEM_POLARITY": "stem_polarity",
            "BAZI_BRANCH_ELEMENT_AFFILIATION": "branch_element_affiliation",
        }
        for field_id, key in fields.items():
            with self.subTest(field_id=field_id):
                row = self.rows[field_id]
                self.assertEqual(row["status"], "ALREADY_VISIBLE")
                self.assertEqual(row["priority"], "REFERENCE")
                self.assertEqual(
                    row["workbench_evidence"]["path"],
                    "src/fortune_training/combined_chart_application/bazi_pillar_metadata_assets.py",
                )
                self.assertIn(f'"{key}"', self.bazi_service)
                self.assertIn(f"source.{key}", BAZI_PILLAR_METADATA_JS)

        self.assertIn("response?.combined_resolution?.bazi_bundle", BAZI_PILLAR_METADATA_JS)
        self.assertIn("selectedApplicationCandidateIndex()", BAZI_PILLAR_METADATA_JS)
        self.assertIn("source.position !== expectedPositions[index]", BAZI_PILLAR_METADATA_JS)
        self.assertIn("renderedGanzhi !== source.ganzhi", BAZI_PILLAR_METADATA_JS)
        self.assertNotIn("五行强弱", BAZI_PILLAR_METADATA_JS)
        self.assertNotIn("旺衰", BAZI_PILLAR_METADATA_JS)
        self.assertNotIn("喜用神", BAZI_PILLAR_METADATA_JS)

    def test_ziwei_daily_is_visible_but_hourly_remains_candidate_only(self) -> None:
        self.assertEqual(
            self.rows["ZIWEI_TARGET_DAILY_PROJECTION"]["status"],
            "ALREADY_VISIBLE",
        )
        self.assertEqual(
            self.rows["ZIWEI_TARGET_HOURLY_CANDIDATES"]["status"],
            "DISPUTED_CANDIDATE_ONLY",
        )
        self.assertIn("紫微流日（条文规则）", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn(
            "紫微流时候选（案例方法；未作流派裁决）",
            TARGET_FLOW_ZIWEI_PROJECTION_JS,
        )
        self.assertIn(
            "hourlyCandidates.forEach((hourlyCandidate) =>",
            TARGET_FLOW_ZIWEI_PROJECTION_JS,
        )

    def test_released_ziwei_bureau_metadata_is_visible_read_only(self) -> None:
        fields = {
            "ZIWEI_LIFE_PALACE_GANZHI": ("bureau.life_palace_ganzhi", "命宫干支"),
            "ZIWEI_BUREAU_NAYIN": ("bureau.nayin_name", "局纳音"),
        }
        for field_id, (source_key, label) in fields.items():
            with self.subTest(field_id=field_id):
                row = self.rows[field_id]
                self.assertEqual(row["status"], "ALREADY_VISIBLE")
                self.assertEqual(row["system"], "ZIWEI")
                self.assertEqual(
                    row["workbench_evidence"]["path"],
                    "src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py",
                )
                self.assertIn(source_key, ZIWEI_BASIC_INFO_JS)
                self.assertIn(f"item('{label}'", ZIWEI_BASIC_INFO_JS)

        self.assertIn("response.clone()", ZIWEI_BASIC_INFO_JS)
        self.assertNotIn("NayinRegistry", ZIWEI_BASIC_INFO_JS)
        self.assertNotIn("NatalStructureGenerator", ZIWEI_BASIC_INFO_JS)

    def test_closed_p1_metadata_rows_leave_no_stale_ui_gap_claim(self) -> None:
        closed_ids = {
            "BAZI_STEM_ELEMENT",
            "BAZI_STEM_POLARITY",
            "BAZI_BRANCH_ELEMENT_AFFILIATION",
            "ZIWEI_LIFE_PALACE_GANZHI",
            "ZIWEI_BUREAU_NAYIN",
        }
        stale = {
            row["field_id"]
            for row in self.matrix["fields"]
            if row["status"] == "ALREADY_RELEASED_NOT_YET_VISIBLE"
        }
        self.assertTrue(closed_ids.isdisjoint(stale))
        for field_id in closed_ids:
            self.assertNotIn("UI-only closure candidate", self.rows[field_id]["notes"])


if __name__ == "__main__":
    unittest.main()
from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app_assets import APP_JS
from fortune_training.combined_chart_application.target_flow_ziwei_projection_assets import (
    TARGET_FLOW_ZIWEI_PROJECTION_JS,
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
            "SHARED_TIME_CREDENTIAL",
        }
        for field_id in expected_visible:
            with self.subTest(field_id=field_id):
                self.assertEqual(self.rows[field_id]["status"], "ALREADY_VISIBLE")

    def test_released_bazi_pillar_metadata_is_a_real_workbench_gap(self) -> None:
        gaps = {
            "BAZI_STEM_ELEMENT": "stem_element",
            "BAZI_STEM_POLARITY": "stem_polarity",
            "BAZI_BRANCH_ELEMENT_AFFILIATION": "branch_element_affiliation",
        }
        for field_id, key in gaps.items():
            with self.subTest(field_id=field_id):
                self.assertEqual(
                    self.rows[field_id]["status"],
                    "ALREADY_RELEASED_NOT_YET_VISIBLE",
                )
                self.assertIn(f'"{key}"', self.bazi_service)
                self.assertNotIn(f"p.{key}", APP_JS)

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

    def test_missing_ui_is_not_treated_as_missing_core(self) -> None:
        statuses = {row["status"] for row in self.matrix["fields"]}
        self.assertIn("ALREADY_RELEASED_NOT_YET_VISIBLE", statuses)
        for field_id in (
            "BAZI_STEM_ELEMENT",
            "BAZI_STEM_POLARITY",
            "BAZI_BRANCH_ELEMENT_AFFILIATION",
        ):
            self.assertEqual(self.rows[field_id]["priority"], "P1")
            self.assertIn("UI-only", self.rows[field_id]["notes"])


if __name__ == "__main__":
    unittest.main()

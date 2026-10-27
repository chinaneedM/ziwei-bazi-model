from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
SVG_PATH = ROOT / "src" / "fortune_training" / "ziwei_application" / "svg.py"
MODELS_PATH = ROOT / "src" / "fortune_training" / "ziwei_chart" / "models.py"


class FusionChartFieldParityZiweiNatalVisibleR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}
        cls.svg_source = SVG_PATH.read_text(encoding="utf-8")
        cls.models_source = MODELS_PATH.read_text(encoding="utf-8")

    def test_visible_ziwei_natal_inventory_rows_are_registered(self) -> None:
        expected = {
            "ZIWEI_FIVE_ELEMENT_BUREAU",
            "ZIWEI_MINGZHU_SHENZHU",
            "ZIWEI_LIFE_BODY_PALACE_BRANCHES",
            "ZIWEI_NATAL_LUNAR_COORDINATES",
            "ZIWEI_TWELVE_PALACE_GANZHI",
            "ZIWEI_STAR_PLACEMENTS_DIGNITY",
            "ZIWEI_TRANSFORMATION_BADGES",
        }
        for field_id in expected:
            with self.subTest(field_id=field_id):
                row = self.rows[field_id]
                self.assertEqual(row["system"], "ZIWEI")
                self.assertEqual(row["status"], "ALREADY_VISIBLE")
                self.assertEqual(row["priority"], "REFERENCE")

    def test_basic_info_rows_consume_released_natal_payload_read_only(self) -> None:
        self.assertIn("bureau.number", ZIWEI_BASIC_INFO_JS)
        self.assertIn("bureau.element", ZIWEI_BASIC_INFO_JS)
        self.assertIn("role(chart, 'ROLE.MINGZHU')", ZIWEI_BASIC_INFO_JS)
        self.assertIn("role(chart, 'ROLE.SHENZHU')", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.life_address?.branch", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.body_address?.branch", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.ziwei_birth_year_stem", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.ziwei_birth_year_branch", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.natal_month_coordinate", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.lunar_birth_day", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.birth_hour_branch?.branch", ZIWEI_BASIC_INFO_JS)
        self.assertNotIn("ZiweiChartFoundation", ZIWEI_BASIC_INFO_JS)
        self.assertNotIn("resolve_bazi", ZIWEI_BASIC_INFO_JS)

    def test_twelve_palace_svg_already_renders_ganzhi_dignity_and_transformations(self) -> None:
        self.assertIn("cell.stem", self.svg_source)
        self.assertIn("cell.branch", self.svg_source)
        self.assertIn("row.dignity_grade", self.svg_source)
        self.assertIn("row.dignity_status", self.svg_source)
        self.assertIn("row.transformation_badges", self.svg_source)
        self.assertIn("_placement_label", self.svg_source)
        self.assertIn("class Placement", self.models_source)
        self.assertIn("class DignityAnnotation", self.models_source)
        self.assertIn("class TransformationActivation", self.models_source)

    def test_inventory_closure_does_not_create_a_false_ui_gap(self) -> None:
        for field_id in (
            "ZIWEI_FIVE_ELEMENT_BUREAU",
            "ZIWEI_MINGZHU_SHENZHU",
            "ZIWEI_LIFE_BODY_PALACE_BRANCHES",
            "ZIWEI_NATAL_LUNAR_COORDINATES",
            "ZIWEI_TWELVE_PALACE_GANZHI",
            "ZIWEI_STAR_PLACEMENTS_DIGNITY",
            "ZIWEI_TRANSFORMATION_BADGES",
        ):
            self.assertNotEqual(
                self.rows[field_id]["status"],
                "ALREADY_RELEASED_NOT_YET_VISIBLE",
            )


if __name__ == "__main__":
    unittest.main()

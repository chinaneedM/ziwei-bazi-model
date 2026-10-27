from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.bazi_pillar_metadata_assets import (
    BAZI_PILLAR_METADATA_JS,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class BaziJiaoyunSymbolicAgeParityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}

    def test_symbolic_age_is_registered_as_already_visible(self) -> None:
        row = self.rows["BAZI_JIAOYUN_SYMBOLIC_AGE"]
        self.assertEqual(row["system"], "BAZI")
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertEqual(row["priority"], "REFERENCE")
        self.assertEqual(
            row["backend_evidence"]["path"],
            "src/fortune_training/bazi_temporal/models.py",
        )
        self.assertEqual(row["backend_evidence"]["symbol"], "SymbolicLuckAge")
        self.assertEqual(
            row["api_evidence"]["path"],
            "src/fortune_training/bazi_application/service.py",
        )
        self.assertEqual(
            row["workbench_evidence"]["path"],
            "src/fortune_training/combined_chart_application/bazi_pillar_metadata_assets.py",
        )
        for evidence_key in (
            "backend_evidence",
            "api_evidence",
            "workbench_evidence",
        ):
            self.assertTrue((ROOT / row[evidence_key]["path"]).exists())

    def test_workbench_copy_projects_released_symbolic_age_units(self) -> None:
        for expected in (
            "renderJiaoyunSymbolicAge",
            "jiaoyun?.symbolic_age",
            "symbolic.years_360",
            "symbolic.months_30",
            "symbolic.days",
            "symbolic.residual_microseconds",
            "起运岁数（符号年龄；360日年 / 30日月）",
            "原始符号年龄余量",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, BAZI_PILLAR_METADATA_JS)

    def test_browser_does_not_recompute_symbolic_age_from_raw_interval(self) -> None:
        for forbidden in (
            "raw_interval_microseconds",
            "JiaoyunEngine",
            "THREE_DAYS_ONE_YEAR",
            "BAZI-THREE-DAYS-ONE-YEAR-360D-R1",
            "MICROSECONDS_PER_SYMBOLIC_YEAR",
            "MICROSECONDS_PER_SYMBOLIC_MONTH",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, BAZI_PILLAR_METADATA_JS)

    def test_inventory_boundary_remains_non_interpretive(self) -> None:
        row = self.rows["BAZI_JIAOYUN_SYMBOLIC_AGE"]
        self.assertIn("no browser recomputation", row["notes"])
        self.assertIn("360-day year / 30-day month", row["notes"])
        for forbidden in ("旺衰", "喜用神", "吉凶", "prediction"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, BAZI_PILLAR_METADATA_JS)


if __name__ == "__main__":
    unittest.main()

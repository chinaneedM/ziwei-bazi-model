from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app_assets import APP_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
BAZI_APPLICATION_SERVICE_PATH = (
    ROOT / "src" / "fortune_training" / "bazi_application" / "service.py"
)


class BaziDayMasterStemProductClosureR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}
        cls.application_source = BAZI_APPLICATION_SERVICE_PATH.read_text(
            encoding="utf-8"
        )
        render_tail = APP_JS.split("function renderBazi", 1)[1]
        cls.render_bazi = render_tail.split("function renderSharedTime", 1)[0]

    def test_day_master_stem_is_registered_as_already_visible(self) -> None:
        row = self.rows["BAZI_DAY_MASTER_STEM"]
        self.assertEqual(row["system"], "BAZI")
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertEqual(row["priority"], "REFERENCE")
        self.assertEqual(
            row["backend_evidence"]["path"],
            "src/fortune_training/bazi_application/service.py",
        )
        self.assertEqual(
            row["backend_evidence"]["symbol"], "BaziChartService._build_view"
        )
        self.assertEqual(
            row["api_evidence"]["path"],
            "src/fortune_training/combined_chart_application/service.py",
        )
        self.assertEqual(
            row["workbench_evidence"]["path"],
            "src/fortune_training/combined_chart_application/local_app_assets.py",
        )
        self.assertEqual(row["workbench_evidence"]["symbol"], "renderBazi")
        for evidence_key in (
            "backend_evidence",
            "api_evidence",
            "workbench_evidence",
        ):
            with self.subTest(evidence_key=evidence_key):
                self.assertTrue((ROOT / row[evidence_key]["path"]).exists())

    def test_application_copy_projects_released_day_master_stem(self) -> None:
        self.assertIn(
            '"day_master_stem": chart.day_master_stem,',
            self.application_source,
        )

    def test_workbench_directly_consumes_released_day_master_stem(self) -> None:
        self.assertIn("view.day_master_stem", self.render_bazi)
        self.assertIn("日主：${view.day_master_stem}", self.render_bazi)

    def test_browser_does_not_rederive_day_master_from_day_pillar(self) -> None:
        for forbidden in (
            "position==='DAY'",
            'position==="DAY"',
            "position === 'DAY'",
            'position === "DAY"',
            "chart.day_master_stem",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.render_bazi)

    def test_inventory_boundary_remains_non_interpretive(self) -> None:
        notes = self.rows["BAZI_DAY_MASTER_STEM"]["notes"]
        self.assertIn("no browser derivation", notes)
        for expected in (
            "strength",
            "favorable-element",
            "auspiciousness",
            "prediction",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, notes)
        for forbidden in ("旺衰", "喜用神", "吉凶", "prediction"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.render_bazi)


if __name__ == "__main__":
    unittest.main()

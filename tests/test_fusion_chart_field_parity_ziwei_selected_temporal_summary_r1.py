from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads((ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json").read_text(encoding="utf-8"))
TEMPORAL = (ROOT / "src" / "fortune_training" / "ziwei_chart" / "temporal.py").read_text(encoding="utf-8")
VIEW = (ROOT / "src" / "fortune_training" / "ziwei_chart" / "view.py").read_text(encoding="utf-8")
SVG = (ROOT / "src" / "fortune_training" / "ziwei_application" / "svg.py").read_text(encoding="utf-8")
LOCAL_APP = (ROOT / "src" / "fortune_training" / "combined_chart_application" / "local_app_assets.py").read_text(encoding="utf-8")
VIEW_SCHEMA = json.loads((ROOT / "schemas" / "ziwei-chart-view-v1.schema.json").read_text(encoding="utf-8"))


def _class_section(source: str, class_name: str) -> str:
    return source.split(f"class {class_name}:", 1)[1].split("\n\n\n@dataclass", 1)[0]


class FusionChartFieldParityZiweiSelectedTemporalSummaryR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = {row["field_id"]: row for row in MATRIX["fields"]}

    def test_selected_temporal_summary_rows_are_registered_visible(self) -> None:
        expected = {
            "ZIWEI_SELECTED_DAXIAN_FRAME_SUMMARY": "ViewDaxianFrameSummary",
            "ZIWEI_SELECTED_ANNUAL_FRAME_SUMMARY": "ViewAnnualFrameSummary",
            "ZIWEI_SELECTED_MONTHLY_FRAME_SUMMARY": "ViewMonthlyFrameSummary",
            "ZIWEI_SELECTED_MINOR_LIMIT_FRAME_SUMMARY": "ViewMinorLimitFrameSummary",
        }
        for field_id, symbol in expected.items():
            with self.subTest(field_id=field_id):
                row = self.rows[field_id]
                self.assertEqual("ZIWEI", row["system"])
                self.assertEqual("ALREADY_VISIBLE", row["status"])
                self.assertEqual(
                    "src/fortune_training/ziwei_chart/temporal.py",
                    row["backend_evidence"]["path"],
                )
                self.assertEqual(
                    "src/fortune_training/ziwei_chart/view.py",
                    row["api_evidence"]["path"],
                )
                self.assertIn(symbol, row["api_evidence"]["symbol"])
                self.assertEqual(
                    "src/fortune_training/ziwei_application/svg.py",
                    row["workbench_evidence"]["path"],
                )
                self.assertIn("server ziwei_svg", row["workbench_evidence"]["claim"])

    def test_released_summary_contract_copies_only_canonical_frame_fields(self) -> None:
        self.assertIn('VIEW_PROJECTION_ALGORITHM_VERSION = "1.2.0"', VIEW)
        self.assertIn("class ViewSelectedTemporalFrameSummary:", VIEW)
        self.assertIn("selected_temporal_frame_summary=selected_summary", VIEW)
        self.assertIn("selected_summary = self._selected_temporal_summary(daxian, annual, monthly, minor)", VIEW)

        daxian = _class_section(VIEW, "ViewDaxianFrameSummary")
        for field in (
            "frame_id",
            "index",
            "nominal_age_start",
            "nominal_age_end",
            "absolute_year_start",
            "absolute_year_end",
            "active_address_index",
            "active_branch",
            "active_palace_ganzhi",
        ):
            self.assertIn(field, daxian)

        annual = _class_section(VIEW, "ViewAnnualFrameSummary")
        for field in (
            "frame_id",
            "absolute_year",
            "nominal_age",
            "year_stem",
            "year_branch",
            "active_address_index",
            "active_branch",
            "active_palace_ganzhi",
        ):
            self.assertIn(field, annual)

        monthly = _class_section(VIEW, "ViewMonthlyFrameSummary")
        for field in (
            "frame_id",
            "absolute_year",
            "lunar_month",
            "month_stem",
            "month_branch",
            "month_ganzhi",
            "active_address_index",
            "active_branch",
            "calendar_scope",
            "leap_month_policy_status",
        ):
            self.assertIn(field, monthly)
        for forbidden in ("active_palace_ganzhi", "year_stem", "year_branch"):
            self.assertNotIn(forbidden, monthly)

        minor = _class_section(VIEW, "ViewMinorLimitFrameSummary")
        for field in ("frame_id", "nominal_age", "active_address_index", "active_branch"):
            self.assertIn(field, minor)
        for forbidden in ("direction", "daxian_direction", "step_count", "start_address"):
            self.assertNotIn(forbidden, minor)

        monthly_source = _class_section(TEMPORAL, "MonthlyFrame")
        self.assertNotIn("active_palace_ganzhi", monthly_source)
        minor_source = _class_section(TEMPORAL, "MinorLimitFrame")
        self.assertNotIn("direction", minor_source)

    def test_schema_and_svg_expose_summary_without_browser_recalculation(self) -> None:
        self.assertIn("selected_temporal_frame_summary", VIEW_SCHEMA["required"])
        selected = VIEW_SCHEMA["$defs"]["selectedTemporalFrameSummary"]
        self.assertEqual(
            {"daxian", "annual", "monthly", "minor_limit"},
            set(selected["required"]),
        )
        monthly = VIEW_SCHEMA["$defs"]["monthlyFrameSummary"]["properties"]
        self.assertNotIn("active_palace_ganzhi", monthly)
        self.assertNotIn("year_stem", monthly)
        self.assertNotIn("year_branch", monthly)
        minor = VIEW_SCHEMA["$defs"]["minorLimitFrameSummary"]["properties"]
        self.assertNotIn("direction", minor)

        self.assertIn('SVG_RENDERER_VERSION = "1.4.0"', SVG)
        self.assertIn("view.selected_temporal_frame_summary", SVG)
        self.assertIn("_selected_temporal_summary_lines", SVG)
        self.assertIn("月历: ", SVG)
        self.assertIn("闰月策略: ", SVG)
        self.assertIn("zroot.innerHTML=d.ziwei_svg", LOCAL_APP)
        self.assertNotIn("selected_temporal_frame_summary", LOCAL_APP)


if __name__ == "__main__":
    unittest.main()

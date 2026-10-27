from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class CombinedWorkbenchZiweiMonthlySequenceR1Tests(unittest.TestCase):
    @staticmethod
    def _resolve_payload(*, lunar_month: int | None = None) -> dict[str, object]:
        app = LocalCombinedChartApplication(ROOT)
        return app.resolve_payload(
            {
                "birth_datetime": "1994-05-17T14:30",
                "birth_place": "Beijing",
                "latitude": 39.9042,
                "longitude": 116.4074,
                "timezone_id": "Asia/Shanghai",
                "sex": "MALE",
                "precision": "EXACT_SECOND",
                "uncertainty_seconds": 0,
                "ziwei_daxian_count": 12,
                "ziwei_daxian_frame_id": None,
                "ziwei_annual_year": 2025,
                "ziwei_lunar_month": lunar_month,
                "ziwei_minor_limit_age": None,
                "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
                "bazi_dayun_count": 12,
                "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
            }
        )

    def test_released_selected_year_exposes_twelve_monthly_frames(self) -> None:
        response = self._resolve_payload()
        temporal_state = response["combined_resolution"]["ziwei_bundle"]["temporal_state"]
        rows = temporal_state["monthly_frames"]
        self.assertEqual(12, len(rows))
        self.assertEqual(list(range(1, 13)), [row["lunar_month"] for row in rows])
        self.assertEqual(12, len({row["frame_id"] for row in rows}))
        self.assertEqual({2025}, {row["absolute_year"] for row in rows})
        self.assertEqual(1, len({row["parent_annual_frame_id"] for row in rows}))
        self.assertEqual({"REGULAR_LUNAR_MONTH_COORDINATE"}, {row["calendar_scope"] for row in rows})
        self.assertEqual({"UNRESOLVED_NOT_GENERATED"}, {row["leap_month_policy_status"] for row in rows})
        for row in rows:
            with self.subTest(frame_id=row["frame_id"]):
                self.assertTrue(row["month_stem"])
                self.assertTrue(row["month_branch"])
                self.assertEqual(row["month_stem"] + row["month_branch"], row["month_ganzhi"])
                self.assertIsInstance(row["active_address"]["index"], int)
                self.assertTrue(row["active_address"]["branch"])
                self.assertTrue(row["parent_annual_frame_id"])
                self.assertTrue(row["monthly_rule_id"])
                self.assertTrue(row["month_ganzhi_rule_id"])
                self.assertTrue(row["source_refs"])

    def test_browser_copy_projects_only_released_monthly_sequence(self) -> None:
        self.assertIn("function monthlySequence(temporalState)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("temporalState?.monthly_frames", ZIWEI_BASIC_INFO_JS)
        for released_field in (
            "row?.frame_id",
            "row?.absolute_year",
            "row?.lunar_month",
            "row?.month_stem",
            "row?.month_branch",
            "row?.month_ganzhi",
            "row?.active_address?.index",
            "row?.active_address?.branch",
            "row?.parent_annual_frame_id",
            "row?.monthly_rule_id",
            "row?.month_ganzhi_rule_id",
            "row?.calendar_scope",
            "row?.leap_month_policy_status",
            "row?.source_refs",
        ):
            with self.subTest(released_field=released_field):
                self.assertIn(released_field, ZIWEI_BASIC_INFO_JS)
        self.assertIn("frameIds.has(row.frame_id)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("lunarMonths.has(row.lunar_month)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("function renderMonthlySequence(temporalState, selectedMonthly)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("renderMonthlySequence(", ZIWEI_BASIC_INFO_JS)
        self.assertIn("完整流月序列", ZIWEI_BASIC_INFO_JS)
        self.assertIn("UNRESOLVED_NOT_GENERATED", self._resolve_payload()["combined_resolution"]["ziwei_bundle"]["temporal_state"]["monthly_frames"][0]["leap_month_policy_status"])

    def test_month_click_copies_released_lunar_month_without_submit_or_cross_selection(self) -> None:
        start = ZIWEI_BASIC_INFO_JS.index("function fillMonthlyTarget(lunarMonth)")
        end = ZIWEI_BASIC_INFO_JS.index("function renderMonthlySequence", start)
        helper = ZIWEI_BASIC_INFO_JS[start:end]
        self.assertIn("$('ziwei-lunar-month')", helper)
        self.assertIn("target.value = String(lunarMonth)", helper)
        self.assertIn("dispatchEvent(new Event('input'", helper)
        self.assertIn("dispatchEvent(new Event('change'", helper)
        self.assertNotIn("ziwei-annual-year", helper)
        self.assertNotIn("ziwei-daxian-frame-id", helper)
        self.assertNotIn("ziwei-minor-limit-age", helper)
        self.assertNotIn("requestSubmit", helper)
        self.assertNotIn(".submit(", helper)
        self.assertIn("fillMonthlyTarget(row.lunarMonth)", ZIWEI_BASIC_INFO_JS)

    def test_selected_month_row_uses_released_selected_summary_identity(self) -> None:
        response = self._resolve_payload(lunar_month=5)
        ziwei_bundle = response["combined_resolution"]["ziwei_bundle"]
        selected = ziwei_bundle["view_model"]["selected_temporal_frame_summary"]["monthly"]
        rows = ziwei_bundle["temporal_state"]["monthly_frames"]
        released = next(row for row in rows if row["lunar_month"] == 5)
        self.assertEqual(released["frame_id"], selected["frame_id"])
        self.assertEqual(released["absolute_year"], selected["absolute_year"])
        self.assertEqual(released["lunar_month"], selected["lunar_month"])
        self.assertIn("selectedMonthly?.frame_id === row.frameId", ZIWEI_BASIC_INFO_JS)
        self.assertIn("selectedMonthly?.absolute_year === row.absoluteYear", ZIWEI_BASIC_INFO_JS)
        self.assertIn("selectedMonthly?.lunar_month === row.lunarMonth", ZIWEI_BASIC_INFO_JS)

    def test_browser_does_not_reimplement_month_generation_rules(self) -> None:
        start = ZIWEI_BASIC_INFO_JS.index("function monthlySequence(temporalState)")
        end = ZIWEI_BASIC_INFO_JS.index("function minorLimitSequence", start)
        monthly_projection = ZIWEI_BASIC_INFO_JS[start:end]
        for forbidden in (
            "YEAR_STEM_TO_YIN_START_STEM",
            "stem_index(",
            "branch_index(",
            "sexagenary_for_year",
            "MONTH:${",
            "MonthlyFrame(",
            "doujun_address.index +",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, monthly_projection)

    def test_field_parity_separates_full_sequence_from_selected_summary(self) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}
        selected = rows["ZIWEI_SELECTED_MONTHLY_FRAME_SUMMARY"]
        sequence = rows["ZIWEI_MONTHLY_SEQUENCE_FRAMES"]
        self.assertEqual("ALREADY_VISIBLE", selected["status"])
        self.assertEqual("ALREADY_VISIBLE", sequence["status"])
        self.assertEqual("ZIWEI", sequence["system"])
        self.assertEqual("REFERENCE", sequence["priority"])
        self.assertIn("ZiweiTemporalState.monthly_frames", sequence["backend_evidence"]["symbol"])
        self.assertIn("ApplicationChartBundle.temporal_state", sequence["api_evidence"]["symbol"])
        self.assertIn("monthlySequence", sequence["workbench_evidence"]["symbol"])
        self.assertIn("does not derive", sequence["notes"])
        self.assertIn("lunar_month", sequence["notes"])
        self.assertIn("leap", sequence["notes"].lower())
        self.assertNotEqual(selected["display_name"], sequence["display_name"])


if __name__ == "__main__":
    unittest.main()

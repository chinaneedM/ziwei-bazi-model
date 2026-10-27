from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class CombinedWorkbenchZiweiAnnualSequenceR1Tests(unittest.TestCase):
    @staticmethod
    def _resolve_temporal_state() -> dict[str, object]:
        app = LocalCombinedChartApplication(ROOT)
        response = app.resolve_payload(
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
                "ziwei_annual_year": None,
                "ziwei_lunar_month": None,
                "ziwei_minor_limit_age": None,
                "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
                "bazi_dayun_count": 12,
                "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
            }
        )
        return response["combined_resolution"]["ziwei_bundle"]["temporal_state"]

    def test_released_annual_sequence_exposes_full_frame_identity(self) -> None:
        temporal_state = self._resolve_temporal_state()
        rows = temporal_state["annual_frames"]
        daxian_ids = {row["frame_id"] for row in temporal_state["daxian_frames"]}
        self.assertGreater(len(rows), 1)
        self.assertEqual(len(rows), len({row["frame_id"] for row in rows}))
        self.assertEqual(len(rows), len({row["absolute_year"] for row in rows}))
        self.assertEqual(1994, rows[0]["absolute_year"])
        for row in rows:
            with self.subTest(frame_id=row["frame_id"]):
                self.assertTrue(row["frame_id"])
                self.assertIsInstance(row["absolute_year"], int)
                self.assertIsInstance(row["nominal_age"], int)
                self.assertGreaterEqual(row["nominal_age"], 1)
                self.assertTrue(row["year_stem"])
                self.assertTrue(row["year_branch"])
                self.assertIsInstance(row["active_address"]["index"], int)
                self.assertTrue(row["active_address"]["branch"])
                self.assertTrue(row["active_palace_ganzhi"])
                self.assertIsInstance(row["doujun_address"]["index"], int)
                self.assertTrue(row["doujun_address"]["branch"])
                self.assertTrue(row["doujun_rule_id"])
                parent = row["parent_daxian_frame_id"]
                if parent is not None:
                    self.assertIn(parent, daxian_ids)

    def test_browser_copy_projects_released_annual_sequence_only(self) -> None:
        self.assertIn("function annualSequence(temporalState)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("temporalState?.annual_frames", ZIWEI_BASIC_INFO_JS)
        for released_field in (
            "row?.frame_id",
            "row?.absolute_year",
            "row?.nominal_age",
            "row?.year_stem",
            "row?.year_branch",
            "row?.active_address?.index",
            "row?.active_address?.branch",
            "row?.active_palace_ganzhi",
            "row?.doujun_address?.index",
            "row?.doujun_address?.branch",
            "row?.doujun_rule_id",
            "row?.parent_daxian_frame_id",
        ):
            with self.subTest(released_field=released_field):
                self.assertIn(released_field, ZIWEI_BASIC_INFO_JS)
        self.assertIn("frameIds.has(row.frame_id)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("years.has(row.absolute_year)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("function renderAnnualSequence(temporalState)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("renderAnnualSequence(ziweiBundle?.temporal_state)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("完整流年序列", ZIWEI_BASIC_INFO_JS)

    def test_annual_click_copies_released_year_without_submit_or_cross_selection(self) -> None:
        start = ZIWEI_BASIC_INFO_JS.index("function fillAnnualTarget(absoluteYear)")
        end = ZIWEI_BASIC_INFO_JS.index("function renderAnnualSequence", start)
        helper = ZIWEI_BASIC_INFO_JS[start:end]
        self.assertIn("$('ziwei-annual-year')", helper)
        self.assertIn("target.value = String(absoluteYear)", helper)
        self.assertIn("dispatchEvent(new Event('input'", helper)
        self.assertIn("dispatchEvent(new Event('change'", helper)
        self.assertNotIn("ziwei-daxian-frame-id", helper)
        self.assertNotIn("requestSubmit", helper)
        self.assertNotIn(".submit(", helper)
        self.assertIn("fillAnnualTarget(row.absoluteYear)", ZIWEI_BASIC_INFO_JS)

    def test_browser_does_not_reimplement_annual_generation_formula(self) -> None:
        for forbidden in (
            "absolute_year - context.ziwei_birth_year + 1",
            "sexagenary_for_year",
            "branch_index(year_branch)",
            "ANNUAL:${",
            "_parent_daxian",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_BASIC_INFO_JS)

    def test_field_parity_separates_full_sequence_from_selected_summary(self) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}
        selected = rows["ZIWEI_SELECTED_ANNUAL_FRAME_SUMMARY"]
        sequence = rows["ZIWEI_ANNUAL_SEQUENCE_FRAMES"]
        self.assertEqual("ALREADY_VISIBLE", selected["status"])
        self.assertEqual("ALREADY_VISIBLE", sequence["status"])
        self.assertEqual("ZIWEI", sequence["system"])
        self.assertEqual("REFERENCE", sequence["priority"])
        self.assertIn("ZiweiTemporalState.annual_frames", sequence["backend_evidence"]["symbol"])
        self.assertIn("ApplicationChartBundle.temporal_state", sequence["api_evidence"]["symbol"])
        self.assertIn("annualSequence", sequence["workbench_evidence"]["symbol"])
        self.assertIn("does not derive", sequence["notes"])
        self.assertIn("absolute_year", sequence["notes"])
        self.assertNotEqual(selected["display_name"], sequence["display_name"])


if __name__ == "__main__":
    unittest.main()

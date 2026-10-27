from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class CombinedWorkbenchZiweiMinorLimitSequenceR1Tests(unittest.TestCase):
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

    def test_released_minor_limit_sequence_exposes_full_frame_identity(self) -> None:
        rows = self._resolve_temporal_state()["minor_limit_frames"]
        self.assertGreater(len(rows), 1)
        self.assertEqual(1, rows[0]["nominal_age"])
        self.assertEqual(len(rows), len({row["frame_id"] for row in rows}))
        self.assertEqual(len(rows), len({row["nominal_age"] for row in rows}))
        for row in rows:
            with self.subTest(frame_id=row["frame_id"]):
                self.assertTrue(row["frame_id"])
                self.assertIsInstance(row["nominal_age"], int)
                self.assertGreaterEqual(row["nominal_age"], 1)
                self.assertIsInstance(row["active_address"]["index"], int)
                self.assertTrue(row["active_address"]["branch"])
                self.assertTrue(row["source_refs"])
                self.assertTrue(all(isinstance(ref, str) and ref for ref in row["source_refs"]))

    def test_browser_copy_projects_released_minor_limit_sequence_only(self) -> None:
        self.assertIn("function minorLimitSequence(temporalState)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("temporalState?.minor_limit_frames", ZIWEI_BASIC_INFO_JS)
        for released_field in (
            "row?.frame_id",
            "row?.nominal_age",
            "row?.active_address?.index",
            "row?.active_address?.branch",
            "row?.source_refs",
        ):
            with self.subTest(released_field=released_field):
                self.assertIn(released_field, ZIWEI_BASIC_INFO_JS)
        self.assertIn("frameIds.has(row.frame_id)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("ages.has(row.nominal_age)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("function renderMinorLimitSequence(temporalState, selectedMinorLimit)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("renderMinorLimitSequence(", ZIWEI_BASIC_INFO_JS)
        self.assertIn("ziweiBundle?.temporal_state", ZIWEI_BASIC_INFO_JS)
        self.assertIn("selected_temporal_frame_summary?.minor_limit", ZIWEI_BASIC_INFO_JS)
        self.assertIn("完整小限序列", ZIWEI_BASIC_INFO_JS)

    def test_minor_limit_click_copies_released_age_without_submit_or_cross_selection(self) -> None:
        start = ZIWEI_BASIC_INFO_JS.index("function fillMinorLimitTarget(nominalAge)")
        end = ZIWEI_BASIC_INFO_JS.index("function renderMinorLimitSequence", start)
        helper = ZIWEI_BASIC_INFO_JS[start:end]
        self.assertIn("$('ziwei-minor-limit-age')", helper)
        self.assertIn("target.value = String(nominalAge)", helper)
        self.assertIn("dispatchEvent(new Event('input'", helper)
        self.assertIn("dispatchEvent(new Event('change'", helper)
        self.assertNotIn("ziwei-daxian-frame-id", helper)
        self.assertNotIn("ziwei-annual-year", helper)
        self.assertNotIn("requestSubmit", helper)
        self.assertNotIn(".submit(", helper)
        self.assertIn("fillMinorLimitTarget(row.nominalAge)", ZIWEI_BASIC_INFO_JS)

    def test_selected_minor_limit_row_uses_released_summary_identity(self) -> None:
        self.assertIn("selectedMinorLimit?.frame_id === row.frameId", ZIWEI_BASIC_INFO_JS)
        self.assertIn("selectedMinorLimit?.nominal_age === row.nominalAge", ZIWEI_BASIC_INFO_JS)
        self.assertIn("box.dataset.selected = 'true'", ZIWEI_BASIC_INFO_JS)
        self.assertIn("box.setAttribute('aria-current', 'true')", ZIWEI_BASIC_INFO_JS)

    def test_browser_does_not_reimplement_minor_limit_generation_formula(self) -> None:
        for forbidden in (
            "MINOR_AGE_ONE_START_BY_YEAR_BRANCH",
            "branch_index(start_branch)",
            "context.sex",
            "MINOR:age=${",
            "daxian_direction",
            "MinorLimitFrame",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_BASIC_INFO_JS)

    def test_field_parity_separates_full_sequence_from_selected_summary(self) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}
        selected = rows["ZIWEI_SELECTED_MINOR_LIMIT_FRAME_SUMMARY"]
        sequence = rows["ZIWEI_MINOR_LIMIT_SEQUENCE_FRAMES"]
        self.assertEqual("ALREADY_VISIBLE", selected["status"])
        self.assertEqual("ALREADY_VISIBLE", sequence["status"])
        self.assertEqual("ZIWEI", sequence["system"])
        self.assertEqual("REFERENCE", sequence["priority"])
        self.assertIn("ZiweiTemporalState.minor_limit_frames", sequence["backend_evidence"]["symbol"])
        self.assertIn("ApplicationChartBundle.temporal_state", sequence["api_evidence"]["symbol"])
        self.assertIn("minorLimitSequence", sequence["workbench_evidence"]["symbol"])
        self.assertIn("does not derive", sequence["notes"])
        self.assertIn("nominal_age", sequence["notes"])
        self.assertNotEqual(selected["display_name"], sequence["display_name"])


if __name__ == "__main__":
    unittest.main()

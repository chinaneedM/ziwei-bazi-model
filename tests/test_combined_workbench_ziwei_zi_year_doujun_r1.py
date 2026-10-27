from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class CombinedWorkbenchZiweiZiYearDoujunR1Tests(unittest.TestCase):
    def test_released_zi_year_annual_frames_agree_on_doujun_branch(self) -> None:
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
        temporal_state = response["combined_resolution"]["ziwei_bundle"]["temporal_state"]
        zi_year_rows = [
            row for row in temporal_state["annual_frames"] if row["year_branch"] == "子"
        ]
        self.assertGreaterEqual(len(zi_year_rows), 1)
        identities = {
            (row["doujun_address"]["index"], row["doujun_address"]["branch"])
            for row in zi_year_rows
        }
        self.assertEqual(1, len(identities))
        self.assertEqual({"辰"}, {row["doujun_address"]["branch"] for row in zi_year_rows})
        self.assertEqual(
            {"S10-SUIJIAN-REVERSE-BIRTH-MONTH-FORWARD-BIRTH-HOUR-R1"},
            {row["doujun_rule_id"] for row in zi_year_rows},
        )

    def test_browser_reads_released_zi_year_doujun_identity_only(self) -> None:
        self.assertIn("function ziYearDoujun(temporalState)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("temporalState?.annual_frames || []", ZIWEI_BASIC_INFO_JS)
        self.assertIn("row?.year_branch === '子'", ZIWEI_BASIC_INFO_JS)
        self.assertIn("row?.doujun_address?.index", ZIWEI_BASIC_INFO_JS)
        self.assertIn("row?.doujun_address?.branch", ZIWEI_BASIC_INFO_JS)
        self.assertIn("rows.every", ZIWEI_BASIC_INFO_JS)
        self.assertIn(
            "item('子年斗君', ziYearDoujun(ziweiBundle?.temporal_state))",
            ZIWEI_BASIC_INFO_JS,
        )

    def test_browser_does_not_reimplement_doujun_formula(self) -> None:
        for forbidden in (
            "branch_index(",
            "birth_hour_branch.index",
            "natal_month_coordinate - 1",
            "S10-SUIJIAN-REVERSE-BIRTH-MONTH-FORWARD-BIRTH-HOUR-R1",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_BASIC_INFO_JS)

    def test_field_parity_inventory_registers_zi_year_doujun_visibility(self) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}
        row = rows["ZIWEI_ZI_YEAR_DOUJUN_BRANCH"]
        self.assertEqual("ZIWEI", row["system"])
        self.assertEqual("ALREADY_VISIBLE", row["status"])
        self.assertEqual("REFERENCE", row["priority"])
        self.assertIn("AnnualFrame.doujun_address", row["backend_evidence"]["symbol"])
        self.assertIn("ApplicationChartBundle.temporal_state", row["api_evidence"]["symbol"])
        self.assertIn("ziYearDoujun", row["workbench_evidence"]["symbol"])
        self.assertIn("ZZZA-PR-056", row["notes"])
        self.assertIn("source-candidate-only", row["notes"])


if __name__ == "__main__":
    unittest.main()

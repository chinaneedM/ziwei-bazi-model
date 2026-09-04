from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]


class CombinedWorkbenchZiweiBodyPalaceGanzhiR1Tests(unittest.TestCase):
    def test_released_body_palace_identity_has_exact_address_attribute(self) -> None:
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
        structure = response["combined_resolution"]["ziwei_bundle"]["candidate"]["chart"]["structure"]
        body_address = structure["body_address"]
        matches = [
            row
            for row in structure["address_attributes"]
            if row["address"]["index"] == body_address["index"]
            and row["address"]["branch"] == body_address["branch"]
        ]
        self.assertEqual(1, len(matches))
        self.assertTrue(matches[0]["stem"])
        self.assertEqual(body_address["branch"], matches[0]["address"]["branch"])

    def test_browser_renders_body_palace_ganzhi_by_released_identity_join_only(self) -> None:
        self.assertIn("function palaceGanzhi(structure, palaceAddress)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.address_attributes || []", ZIWEI_BASIC_INFO_JS)
        self.assertIn("row?.address?.index === palaceAddress.index", ZIWEI_BASIC_INFO_JS)
        self.assertIn("row?.address?.branch === palaceAddress.branch", ZIWEI_BASIC_INFO_JS)
        self.assertIn("matches.length !== 1", ZIWEI_BASIC_INFO_JS)
        self.assertIn("`${matches[0].stem}${palaceAddress.branch}`", ZIWEI_BASIC_INFO_JS)
        self.assertIn(
            "item('身宫干支', palaceGanzhi(structure, structure.body_address))",
            ZIWEI_BASIC_INFO_JS,
        )

    def test_body_palace_ganzhi_projection_does_not_introduce_a_browser_rule_engine(self) -> None:
        for forbidden in (
            "fiveTiger",
            "FiveTiger",
            "palaceStem",
            "GanZhiRegistry",
            "NatalStructureGenerator",
            "TimeCalendarFoundation",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_BASIC_INFO_JS)


if __name__ == "__main__":
    unittest.main()

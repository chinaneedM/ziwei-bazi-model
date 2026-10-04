from __future__ import annotations

import unittest
import json
import re
import shutil
import subprocess
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS
from fortune_training.ziwei_chart.natal import NatalStructureGenerator, NatalStructureInput


ROOT = Path(__file__).resolve().parents[1]


class CombinedWorkbenchZiweiBodyPalaceGanzhiR1Tests(unittest.TestCase):
    def _execute_projection(self, cases: list[dict]) -> list[str]:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node is required for the actual JavaScript projection replay")
        function = re.search(
            r"  function palaceGanzhi\(structure, palaceAddress\) \{.*?\n  \}",
            ZIWEI_BASIC_INFO_JS, re.DOTALL,
        )
        self.assertIsNotNone(function)
        script = function.group(0) + """
const cases = JSON.parse(require('fs').readFileSync(0, 'utf8'));
console.log(JSON.stringify(cases.map(c => palaceGanzhi(c.structure, c.address))));
"""
        completed = subprocess.run(
            [node, "-e", script], input=json.dumps(cases, ensure_ascii=False),
            capture_output=True, text=True, check=True, timeout=30,
        )
        return json.loads(completed.stdout)

    def test_actual_projection_joins_reordered_released_rows_for_all_natal_coordinates(self) -> None:
        cases, expected = [], []
        # Ten consecutive years cover all year stems; ordinary month/hour
        # geometry is already source-audited. This checks the consumer join,
        # including row reordering, rather than reimplementing that geometry.
        for year in range(1984, 1994):
            for month in range(1, 13):
                for hour_branch in range(12):
                    natal = NatalStructureGenerator().generate(NatalStructureInput(
                        lunar_year=year, lunar_month=month, lunar_day=1,
                        is_leap_month=False, lunar_month_length_days=30,
                        local_apparent_solar_datetime=datetime(2000, 1, 1, hour_branch * 2),
                        life_body_leap_month_policy="CURRENT_MONTH",
                    ))
                    row = next(r for r in natal.address_attributes if r.address == natal.body_address)
                    expected.append(row.stem + row.address.branch)
                    cases.append({
                        "structure": {"address_attributes": [asdict(r) for r in reversed(natal.address_attributes)]},
                        "address": asdict(natal.body_address),
                    })
        self.assertEqual(1440, len(cases))
        self.assertEqual(expected, self._execute_projection(cases))

    def test_actual_projection_rejects_ambiguous_and_malformed_released_identities(self) -> None:
        address = {"index": 2, "branch": "寅"}
        valid = {"address": address, "stem": "丙"}
        empty = {"address": address, "stem": ""}
        wrong_branch = {"address": {"index": 2, "branch": "卯"}, "stem": "丁"}
        wrong_index = {"address": {"index": 3, "branch": "寅"}, "stem": "丁"}
        cases = [
            {"structure": None, "address": address},
            {"structure": {}, "address": address},
            {"structure": {"address_attributes": {}}, "address": address},
            {"structure": {"address_attributes": []}, "address": address},
            {"structure": {"address_attributes": [valid]}, "address": None},
            {"structure": {"address_attributes": [valid]}, "address": {"index": "2", "branch": "寅"}},
            {"structure": {"address_attributes": [{"address": {"index": 12, "branch": "寅"}, "stem": "丙"}]}, "address": {"index": 12, "branch": "寅"}},
            {"structure": {"address_attributes": [{"address": {"index": -1, "branch": "寅"}, "stem": "丙"}]}, "address": {"index": -1, "branch": "寅"}},
            {"structure": {"address_attributes": [valid, valid]}, "address": address},
            {"structure": {"address_attributes": [valid, empty]}, "address": address},
            {"structure": {"address_attributes": [empty, valid]}, "address": address},
            {"structure": {"address_attributes": [empty]}, "address": address},
            {"structure": {"address_attributes": [wrong_branch, wrong_index]}, "address": address},
            {"structure": {"address_attributes": [None, wrong_branch, valid, wrong_index]}, "address": address},
        ]
        self.assertEqual(["-"] * 13 + ["丙寅"], self._execute_projection(cases))

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
        self.assertIn("Array.isArray(structure.address_attributes)", ZIWEI_BASIC_INFO_JS)
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

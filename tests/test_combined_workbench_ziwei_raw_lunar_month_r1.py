from __future__ import annotations

import threading
import unittest
from pathlib import Path
from urllib.request import urlopen

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.workbench_local_app import build_workbench_server
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS
from fortune_training.combined_chart_application.ziwei_raw_lunar_month_assets import (
    ZIWEI_RAW_LUNAR_MONTH_JS,
    ziwei_raw_lunar_month_index_html,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedWorkbenchZiweiRawLunarMonthR1Tests(unittest.TestCase):
    @staticmethod
    def _resolve_structure() -> dict[str, object]:
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
        return response["combined_resolution"]["ziwei_bundle"]["candidate"]["chart"]["structure"]

    def test_released_structure_exposes_raw_lunar_month_distinct_from_month_coordinate(self) -> None:
        structure = self._resolve_structure()
        self.assertIsInstance(structure["raw_lunar_month"], int)
        self.assertGreaterEqual(structure["raw_lunar_month"], 1)
        self.assertLessEqual(structure["raw_lunar_month"], 12)
        self.assertIn("natal_month_coordinate", structure)

    def test_asset_copy_projects_released_raw_lunar_month_only(self) -> None:
        self.assertIn("structure?.raw_lunar_month", ZIWEI_RAW_LUNAR_MONTH_JS)
        self.assertIn("Number.isInteger(rawLunarMonth)", ZIWEI_RAW_LUNAR_MONTH_JS)
        self.assertIn("label.textContent = '原始农历月'", ZIWEI_RAW_LUNAR_MONTH_JS)
        self.assertIn("content.textContent = String(rawLunarMonth)", ZIWEI_RAW_LUNAR_MONTH_JS)
        self.assertIn("ziwei-basic-info-grid", ZIWEI_RAW_LUNAR_MONTH_JS)
        self.assertIn("structure.natal_month_coordinate", ZIWEI_BASIC_INFO_JS)

    def test_asset_does_not_reimplement_calendar_or_month_coordinate_rules(self) -> None:
        for forbidden in (
            "natal_month_coordinate =",
            "raw_lunar_month =",
            "fromSolar",
            "fromLunar",
            "Lunar.from",
            "Solar.from",
            "day_boundary",
            "apparent_solar",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_RAW_LUNAR_MONTH_JS)

    def test_html_injection_is_single_and_read_only(self) -> None:
        base = "<html><head></head><body><main></main></body></html>"
        injected = ziwei_raw_lunar_month_index_html(base)
        self.assertIn('<script src="/ziwei-raw-lunar-month.js" defer></script>', injected)
        with self.assertRaisesRegex(ValueError, "already injected"):
            ziwei_raw_lunar_month_index_html(injected)

    def test_workbench_publishes_raw_lunar_month_asset_over_loopback_http(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        host, port = server.server_address[:2]
        self.assertEqual("127.0.0.1", host)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urlopen(f"http://{host}:{port}/", timeout=30) as response:
                index = response.read().decode("utf-8")
                self.assertEqual(200, response.status)
            self.assertIn("/ziwei-raw-lunar-month.js", index)
            with urlopen(f"http://{host}:{port}/ziwei-raw-lunar-month.js", timeout=30) as response:
                asset = response.read().decode("utf-8")
                self.assertEqual(200, response.status)
                self.assertIn("structure?.raw_lunar_month", asset)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

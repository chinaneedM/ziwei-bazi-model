from __future__ import annotations

import threading
import unittest
from pathlib import Path
from urllib.request import urlopen

from fortune_training.combined_chart_application.local_app import (
    LocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)
from fortune_training.combined_chart_application.ziwei_basic_info_assets import (
    ZIWEI_BASIC_INFO_JS,
    ziwei_basic_info_index_html,
)
from fortune_training.combined_chart_application.local_app_assets import INDEX_HTML


ROOT = Path(__file__).resolve().parents[1]


class CombinedWorkbenchZiweiBasicInfoR1Tests(unittest.TestCase):
    def test_released_bundle_contains_all_basic_info_sources(self) -> None:
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
        candidate = response["combined_resolution"]["ziwei_bundle"]["candidate"]
        chart = candidate["chart"]
        structure = chart["structure"]
        self.assertIn("bureau", structure)
        self.assertIn("life_address", structure)
        self.assertIn("body_address", structure)
        roles = {row["role_id"]: row for row in chart["role_bindings"]}
        self.assertIn("ROLE.MINGZHU", roles)
        self.assertIn("ROLE.SHENZHU", roles)
        self.assertTrue(roles["ROLE.MINGZHU"]["entity_display_name"])
        self.assertTrue(roles["ROLE.SHENZHU"]["entity_display_name"])

    def test_browser_projection_reads_released_fields_without_recomputation(self) -> None:
        self.assertIn("candidate?.chart", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.bureau", ZIWEI_BASIC_INFO_JS)
        self.assertIn("ROLE.MINGZHU", ZIWEI_BASIC_INFO_JS)
        self.assertIn("ROLE.SHENZHU", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.body_address", ZIWEI_BASIC_INFO_JS)
        for forbidden in (
            "NatalStructureGenerator",
            "WenmoDefaultRoleGenerator",
            "MINGZHU_BY_LIFE_BRANCH",
            "WENMO_SHENZHU_BY_YEAR_BRANCH",
            "TimeCalendarFoundation",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_BASIC_INFO_JS)

    def test_assets_are_additive_and_duplicate_guarded(self) -> None:
        html = ziwei_basic_info_index_html(INDEX_HTML)
        self.assertEqual(1, html.count('/ziwei-basic-info.css'))
        self.assertEqual(1, html.count('/ziwei-basic-info.js'))
        with self.assertRaisesRegex(ValueError, "already injected"):
            ziwei_basic_info_index_html(html)

    def test_real_workbench_serves_basic_info_assets_once(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            base = f"http://{host}:{port}"
            with urlopen(f"{base}/", timeout=10) as response:  # noqa: S310
                html = response.read().decode("utf-8")
            self.assertEqual(1, html.count('/ziwei-basic-info.css'))
            self.assertEqual(1, html.count('/ziwei-basic-info.js'))
            with urlopen(f"{base}/ziwei-basic-info.js", timeout=10) as response:  # noqa: S310
                js = response.read().decode("utf-8")
            self.assertIn("panel.id = 'ziwei-basic-info'", js)
            with urlopen(f"{base}/ziwei-basic-info.css", timeout=10) as response:  # noqa: S310
                css = response.read().decode("utf-8")
            self.assertIn(".ziwei-basic-info-grid", css)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

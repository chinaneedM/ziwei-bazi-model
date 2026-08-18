from __future__ import annotations

import threading
import unittest
import urllib.request
from pathlib import Path

from fortune_training.combined_chart_application.target_flow_guard_assets import (
    TARGET_FLOW_GUARD_JS,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedBrowserBaziTargetFlowDisplayGuardR1Tests(unittest.TestCase):
    def test_guard_freezes_source_fingerprint_when_bazi_chart_is_actually_redrawn(self) -> None:
        self.assertIn("let displayedSourceFingerprint = null", TARGET_FLOW_GUARD_JS)
        self.assertIn("function captureDisplayedSource()", TARGET_FLOW_GUARD_JS)
        self.assertIn("sourceObserver.observe(baziRoot", TARGET_FLOW_GUARD_JS)
        self.assertIn("displayedSourceFingerprint === sourceFingerprint()", TARGET_FLOW_GUARD_JS)
        for field_id in (
            "birth-datetime",
            "birth-place",
            "latitude",
            "longitude",
            "timezone-id",
            "sex",
            "precision",
            "ziwei-daxian-frame-id",
            "ziwei-annual-year",
            "ziwei-minor-limit-age",
            "bazi-natal-profile",
            "bazi-temporal-profile",
            "bazi-dayun-count",
        ):
            with self.subTest(field_id=field_id):
                self.assertIn(f"'{field_id}'", TARGET_FLOW_GUARD_JS)

    def test_guard_blocks_flow_request_against_stale_visible_bazi_chart(self) -> None:
        self.assertIn("document.addEventListener('click'", TARGET_FLOW_GUARD_JS)
        self.assertIn("event.stopImmediatePropagation()", TARGET_FLOW_GUARD_JS)
        self.assertIn("请先点击“联合排盘”", TARGET_FLOW_GUARD_JS)
        self.assertIn("setInterval(() =>", TARGET_FLOW_GUARD_JS)
        self.assertIn("已清除旧目标 flow", TARGET_FLOW_GUARD_JS)

    def test_guard_does_not_write_any_ziwei_presentation_state(self) -> None:
        for forbidden in (
            "$('ziwei-chart')",
            "$('ziwei-daxian-frame-id').value =",
            "$('ziwei-annual-year').value =",
            "$('ziwei-minor-limit-age').value =",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, TARGET_FLOW_GUARD_JS)

    def test_real_server_serves_target_flow_and_guard_as_one_asset(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with urllib.request.urlopen(
                f"http://{host}:{port}/target-flow.js", timeout=10
            ) as response:
                javascript = response.read().decode("utf-8")
            self.assertIn("/api/resolve-flow", javascript)
            self.assertIn("displayedSourceFingerprint", javascript)
            self.assertIn("stopImmediatePropagation", javascript)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

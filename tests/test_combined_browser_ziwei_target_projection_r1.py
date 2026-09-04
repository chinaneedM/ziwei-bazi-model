from __future__ import annotations

import re
import threading
import unittest
import urllib.request
from pathlib import Path

from fortune_training.combined_chart_application.target_flow_assets import TARGET_FLOW_JS
from fortune_training.combined_chart_application.target_flow_ziwei_projection_assets import (
    TARGET_FLOW_ZIWEI_PROJECTION_CSS,
    TARGET_FLOW_ZIWEI_PROJECTION_JS,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedBrowserZiweiTargetProjectionR1Tests(unittest.TestCase):
    def test_projection_binds_by_exact_target_candidate_identity(self) -> None:
        self.assertIn(
            "state.response?.shared_ziwei_selector_projection",
            TARGET_FLOW_ZIWEI_PROJECTION_JS.replace("projectionState", "state"),
        )
        self.assertIn(
            "row.source_target_candidate_id === targetCandidateId",
            TARGET_FLOW_ZIWEI_PROJECTION_JS,
        )
        self.assertIn("matches.length === 1 ? matches[0] : null", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("拒绝位置式回退", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertNotIn("projection.candidates[index]", TARGET_FLOW_ZIWEI_PROJECTION_JS)

    def test_projection_renders_daily_rule_and_all_hourly_candidates_neutrally(self) -> None:
        self.assertIn("紫微流日（条文规则）", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn(
            "紫微流时候选（案例方法；未作流派裁决）",
            TARGET_FLOW_ZIWEI_PROJECTION_JS,
        )
        self.assertIn("hourlyCandidates.forEach((hourlyCandidate) =>", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("hourlyCandidate.authority_status", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("全部候选并列展示，不自动选定任何流时", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        for forbidden in (
            "selected_hourly_candidate_id",
            "winner",
            "吉凶",
            "应验",
            "预测",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, TARGET_FLOW_ZIWEI_PROJECTION_JS)

    def test_projection_is_additive_and_missing_field_is_safe(self) -> None:
        self.assertIn(
            "if (!projection || !Array.isArray(projection.candidates))",
            TARGET_FLOW_ZIWEI_PROJECTION_JS,
        )
        self.assertIn("clearProjectionView();", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("const copy = response.clone();", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("const originalFetch = window.fetch.bind(window);", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("/api/resolve-flow", TARGET_FLOW_JS)
        self.assertNotIn("body: JSON.stringify", TARGET_FLOW_ZIWEI_PROJECTION_JS)

    def test_ziwei_selector_changes_invalidate_only_projection_view(self) -> None:
        for field_id in (
            "ziwei-daxian-count",
            "ziwei-daxian-frame-id",
            "ziwei-annual-year",
            "ziwei-minor-limit-age",
        ):
            with self.subTest(field_id=field_id):
                self.assertIn(f"'{field_id}'", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("invalidateProjectionOnly", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("observer.observe(ziweiRoot", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertNotIn("$('ziwei-chart').innerHTML", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIsNone(
            re.search(r"candidateSelect\.value\s*=(?!=)", TARGET_FLOW_ZIWEI_PROJECTION_JS),
            "read-only projection asset must not assign candidateSelect.value",
        )

    def test_projection_assets_have_independent_visual_contract(self) -> None:
        self.assertIn(".ziwei-target-projection", TARGET_FLOW_ZIWEI_PROJECTION_CSS)
        self.assertIn(".ziwei-target-hourly-candidate", TARGET_FLOW_ZIWEI_PROJECTION_CSS)
        self.assertIn("紫微目标时点投影（只读）", TARGET_FLOW_ZIWEI_PROJECTION_JS)
        self.assertIn("不改写紫微选择器", TARGET_FLOW_ZIWEI_PROJECTION_JS)

    def test_real_workbench_serves_old_and_new_target_flow_assets_together(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with urllib.request.urlopen(
                f"http://{host}:{port}/target-flow.js", timeout=10
            ) as response:
                javascript = response.read().decode("utf-8")
            with urllib.request.urlopen(
                f"http://{host}:{port}/target-flow.css", timeout=10
            ) as response:
                stylesheet = response.read().decode("utf-8")
            self.assertIn("/api/resolve-flow", javascript)
            self.assertIn("displayedSourceFingerprint", javascript)
            self.assertIn("shared_ziwei_selector_projection", javascript)
            self.assertIn("紫微流日（条文规则）", javascript)
            self.assertIn("紫微流时候选（案例方法；未作流派裁决）", javascript)
            self.assertIn(".bazi-target-flow-panel", stylesheet)
            self.assertIn(".ziwei-target-projection", stylesheet)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

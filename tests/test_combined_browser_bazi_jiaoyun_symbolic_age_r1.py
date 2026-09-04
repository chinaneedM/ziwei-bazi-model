from __future__ import annotations

import threading
import unittest
import urllib.request
from pathlib import Path

from fortune_training.combined_chart_application.bazi_pillar_metadata_assets import (
    BAZI_PILLAR_METADATA_CSS,
    BAZI_PILLAR_METADATA_JS,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedBrowserBaziJiaoyunSymbolicAgeR1Tests(unittest.TestCase):
    def test_released_symbolic_age_is_rendered_with_explicit_coordinate_semantics(self) -> None:
        self.assertIn("candidate?.view?.dayun?.jiaoyun", BAZI_PILLAR_METADATA_JS)
        self.assertIn("jiaoyun?.symbolic_age", BAZI_PILLAR_METADATA_JS)
        self.assertIn("symbolic.years_360", BAZI_PILLAR_METADATA_JS)
        self.assertIn("symbolic.months_30", BAZI_PILLAR_METADATA_JS)
        self.assertIn("symbolic.days", BAZI_PILLAR_METADATA_JS)
        self.assertIn("symbolic.residual_microseconds", BAZI_PILLAR_METADATA_JS)
        self.assertIn("起运岁数（符号年龄；360日年 / 30日月）", BAZI_PILLAR_METADATA_JS)
        self.assertIn("原始符号年龄余量", BAZI_PILLAR_METADATA_JS)

    def test_symbolic_age_uses_same_exact_rendered_candidate_binding(self) -> None:
        self.assertIn("const candidate = bundle.candidates[selectedIndex]", BAZI_PILLAR_METADATA_JS)
        self.assertIn("const bindings = validatedPillarBindings(candidate)", BAZI_PILLAR_METADATA_JS)
        self.assertIn("if (!bindings) return", BAZI_PILLAR_METADATA_JS)
        self.assertIn("renderJiaoyunSymbolicAge(candidate, selectedIndex)", BAZI_PILLAR_METADATA_JS)
        self.assertIn("row.dataset.applicationCandidateIndex = String(selectedIndex)", BAZI_PILLAR_METADATA_JS)
        self.assertNotIn("bundle.candidates[0]", BAZI_PILLAR_METADATA_JS)

    def test_presentation_is_read_only_and_does_not_recompute_jiaoyun(self) -> None:
        for forbidden in (
            "symbolic.years_360 =",
            "symbolic.months_30 =",
            "symbolic.days =",
            "first_transition_utc =",
            "selector.value =",
            "fetch('/api/bazi",
            "吉凶",
            "旺衰",
            "预测",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, BAZI_PILLAR_METADATA_JS)
        self.assertIn("const copy = response.clone();", BAZI_PILLAR_METADATA_JS)
        self.assertIn("pathname !== '/api/resolve'", BAZI_PILLAR_METADATA_JS)

    def test_visual_contract_is_additive(self) -> None:
        self.assertIn(".bazi-jiaoyun-symbolic-age", BAZI_PILLAR_METADATA_CSS)
        self.assertIn("baziRoot.insertBefore(row, dayunTable || null)", BAZI_PILLAR_METADATA_JS)

    def test_real_workbench_serves_symbolic_age_asset(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with urllib.request.urlopen(
                f"http://{host}:{port}/bazi-pillar-metadata.js", timeout=10
            ) as response:
                javascript = response.read().decode("utf-8")
            with urllib.request.urlopen(
                f"http://{host}:{port}/bazi-pillar-metadata.css", timeout=10
            ) as response:
                stylesheet = response.read().decode("utf-8")
            self.assertIn("symbolic_age", javascript)
            self.assertIn("起运岁数（符号年龄；360日年 / 30日月）", javascript)
            self.assertIn(".bazi-jiaoyun-symbolic-age", stylesheet)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

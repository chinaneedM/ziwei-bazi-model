from __future__ import annotations

import threading
import unittest
from pathlib import Path
from urllib.request import urlopen

from fortune_training.combined_chart_application.flow_fusion_assets import (
    FLOW_FUSION_JS,
    flow_fusion_index_html,
)
from fortune_training.combined_chart_application.local_app import INDEX_HTML
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedWorkbenchFlowFusionPanelR2Tests(unittest.TestCase):
    def test_asset_injection_is_additive_and_idempotency_guarded(self) -> None:
        html = flow_fusion_index_html(INDEX_HTML)
        self.assertEqual(1, html.count('/flow-fusion.css'))
        self.assertEqual(1, html.count('/flow-fusion.js'))
        with self.assertRaisesRegex(ValueError, 'already injected'):
            flow_fusion_index_html(html)

    def test_browser_panel_is_read_only_composition_without_temporal_algorithms(self) -> None:
        self.assertIn("panel.id = 'fusion-r2-panel'", FLOW_FUSION_JS)
        self.assertIn("fetch('/api/resolve-flow-fusion-r2'", FLOW_FUSION_JS)
        self.assertIn('ziwei_selector_candidate_count', FLOW_FUSION_JS)
        self.assertIn('bazi_target_flow_bundle_hash', FLOW_FUSION_JS)
        self.assertIn('target_coordinate_fact_hash', FLOW_FUSION_JS)
        for forbidden in (
            'BaziTimeResolver',
            'TargetTemporalCoordinateFoundation',
            'ZiweiTemporalEngine',
            'SharedZiweiSelectorProjectionService',
            'candidate_zero',
            'candidates[0]',
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, FLOW_FUSION_JS)

    def test_real_workbench_serves_fusion_panel_assets_once(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            base = f'http://{host}:{port}'
            with urlopen(f'{base}/', timeout=10) as response:  # noqa: S310
                html = response.read().decode('utf-8')
            self.assertEqual(1, html.count('/flow-fusion.css'))
            self.assertEqual(1, html.count('/flow-fusion.js'))

            with urlopen(f'{base}/flow-fusion.js', timeout=10) as response:  # noqa: S310
                js = response.read().decode('utf-8')
            self.assertIn("panel.id = 'fusion-r2-panel'", js)
            self.assertIn("/api/resolve-flow-fusion-r2", js)

            with urlopen(f'{base}/flow-fusion.css', timeout=10) as response:  # noqa: S310
                css = response.read().decode('utf-8')
            self.assertIn('.fusion-r2-panel', css)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()

from __future__ import annotations

import threading
import unittest
from pathlib import Path
from urllib.request import urlopen

from fortune_training.combined_chart_application.shared_apply_assets import SHARED_APPLY_JS
from fortune_training.combined_chart_application.target_flow_assets import TARGET_FLOW_JS
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]
UNSAFE_JS_JOIN_FRAGMENT = "].join('\n');"
SAFE_JS_JOIN_FRAGMENT = r"].join('\n');"


class CombinedWorkbenchBrowserPanelVisibilityR1Tests(unittest.TestCase):
    def test_embedded_browser_javascript_preserves_backslash_n_literals(self) -> None:
        # Python must not turn JS string-literal \n escapes into literal line breaks.
        self.assertNotIn(UNSAFE_JS_JOIN_FRAGMENT, TARGET_FLOW_JS)
        self.assertIn(SAFE_JS_JOIN_FRAGMENT, TARGET_FLOW_JS)
        self.assertNotIn(UNSAFE_JS_JOIN_FRAGMENT, SHARED_APPLY_JS)
        self.assertIn(SAFE_JS_JOIN_FRAGMENT, SHARED_APPLY_JS)

    def test_actual_workbench_root_and_assets_expose_both_sidecars(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            base = f"http://{host}:{port}"
            with urlopen(f"{base}/", timeout=10) as response:  # noqa: S310
                html = response.read().decode("utf-8")
            self.assertEqual(html.count('/target-flow.js'), 1)
            self.assertEqual(html.count('/shared-apply.js'), 1)
            self.assertEqual(html.count('/target-flow.css'), 1)
            self.assertEqual(html.count('/shared-apply.css'), 1)

            with urlopen(f"{base}/target-flow.js", timeout=10) as response:  # noqa: S310
                target_js = response.read().decode("utf-8")
            self.assertIn("panel.id = 'bazi-target-flow-panel'", target_js)
            self.assertIn(SAFE_JS_JOIN_FRAGMENT, target_js)
            self.assertNotIn(UNSAFE_JS_JOIN_FRAGMENT, target_js)

            with urlopen(f"{base}/shared-apply.js", timeout=10) as response:  # noqa: S310
                shared_js = response.read().decode("utf-8")
            self.assertIn("panel.id = 'shared-ziwei-apply-panel'", shared_js)
            self.assertIn(SAFE_JS_JOIN_FRAGMENT, shared_js)
            self.assertNotIn(UNSAFE_JS_JOIN_FRAGMENT, shared_js)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_fortune_chart_app_still_points_to_workbench_entrypoint(self) -> None:
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn(
            'fortune-chart-app = "fortune_training.combined_chart_application.workbench_local_app:main"',
            pyproject,
        )


if __name__ == "__main__":
    unittest.main()

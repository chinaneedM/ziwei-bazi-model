from __future__ import annotations

import threading
import unittest
from pathlib import Path
from urllib.request import urlopen

from fortune_training.combined_chart_application.product_shell_assets import (
    DESKTOP_PRODUCT_SHELL_SCHEMA,
    PRODUCT_SHELL_CSS,
    PRODUCT_SHELL_JS,
    product_shell_index_html,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class FusionChartDesktopProductShellR1Tests(unittest.TestCase):
    def test_product_shell_is_presentation_only_and_preserves_existing_mounts(self) -> None:
        source = "<html><head></head><body><main></main></body></html>"
        rendered = product_shell_index_html(source)
        self.assertEqual(rendered.count('/product-shell.css'), 1)
        self.assertEqual(rendered.count('/product-shell.js'), 1)
        self.assertEqual(rendered.count('name="fortune-chart-product-shell"'), 1)
        self.assertIn(DESKTOP_PRODUCT_SHELL_SCHEMA, rendered)
        self.assertNotIn("fetch(", PRODUCT_SHELL_JS)
        self.assertNotIn("/api/", PRODUCT_SHELL_JS)
        self.assertIn("fortune-chart-product-shell", PRODUCT_SHELL_JS)
        self.assertIn("'natal','本命总览'", PRODUCT_SHELL_JS)
        self.assertIn("'flow','时运联动'", PRODUCT_SHELL_JS)
        self.assertIn("'fusion','融合视图'", PRODUCT_SHELL_JS)
        self.assertIn("'audit','专业审计'", PRODUCT_SHELL_JS)
        self.assertIn("'product-view-' + id", PRODUCT_SHELL_JS)
        self.assertIn("product-bridge-ziwei", PRODUCT_SHELL_JS)
        self.assertIn("product-bridge-time", PRODUCT_SHELL_JS)
        self.assertIn("product-bridge-bazi", PRODUCT_SHELL_JS)
        self.assertIn('data-product-jump="fusion"', PRODUCT_SHELL_JS)
        self.assertIn("紫微斗数本命盘", PRODUCT_SHELL_JS)
        self.assertIn("四柱八字本命盘", PRODUCT_SHELL_JS)
        for mount_id in (
            "ziwei-interaction-panel",
            "bazi-target-flow-panel",
            "shared-ziwei-apply-panel",
            "fusion-r2-panel",
            "resolved-profile-lineage-panel",
            "ziwei-structural-relations-panel",
            "ziwei-star-provenance-panel",
            "ziwei-palace-stem-topology-panel",
            "ziwei-dignity-provenance-panel",
            "ziwei-transformation-provenance-panel",
        ):
            with self.subTest(mount_id=mount_id):
                self.assertIn(mount_id, PRODUCT_SHELL_JS)

    def test_product_shell_exposes_professional_workspace_structure(self) -> None:
        for expected in (
            ".product-resolution-summary",
            ".product-workspace",
            ".product-nav",
            ".product-view",
            ".product-primary-grid",
            ".product-option-details",
            ".product-fusion-bridge",
            ".product-shared-core",
            ".product-quick-actions",
            ".product-fusion-intro",
            ".product-audit-stack",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, PRODUCT_SHELL_CSS)

    def test_actual_workbench_serves_product_shell_last(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            base = f"http://{host}:{port}"
            with urlopen(f"{base}/", timeout=10) as response:  # noqa: S310
                html = response.read().decode("utf-8")
            self.assertEqual(html.count('/product-shell.css'), 1)
            self.assertEqual(html.count('/product-shell.js'), 1)
            self.assertEqual(html.count('name="fortune-chart-product-shell"'), 1)
            self.assertIn(DESKTOP_PRODUCT_SHELL_SCHEMA, html)
            self.assertGreater(
                html.rfind('/product-shell.js'),
                html.rfind('/ziwei-transformation-provenance.js'),
            )

            with urlopen(f"{base}/product-shell.css", timeout=10) as response:  # noqa: S310
                css = response.read().decode("utf-8")
            with urlopen(f"{base}/product-shell.js", timeout=10) as response:  # noqa: S310
                javascript = response.read().decode("utf-8")
            self.assertEqual(css, PRODUCT_SHELL_CSS)
            self.assertEqual(javascript, PRODUCT_SHELL_JS)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_productization_does_not_reopen_closed_deterministic_scope(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED", readme)
        self.assertIn(
            "ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED",
            readme,
        )


if __name__ == "__main__":
    unittest.main()

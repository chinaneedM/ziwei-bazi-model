from __future__ import annotations

import threading
import unittest
from pathlib import Path
from urllib.request import urlopen

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.workbench_local_app import (
    _WorkbenchHandler,
    build_workbench_server,
)
from fortune_training.combined_chart_application.ziwei_transformation_provenance_assets import (
    ZIWEI_TRANSFORMATION_PROVENANCE_CSS,
    ZIWEI_TRANSFORMATION_PROVENANCE_JS,
    ziwei_transformation_provenance_index_html,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedWorkbenchZiweiTransformationProvenanceR1Tests(unittest.TestCase):
    @staticmethod
    def _resolve_transformations() -> list[dict[str, object]]:
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
        return response["combined_resolution"]["ziwei_bundle"]["candidate"]["chart"][
            "transformations"
        ]

    def test_resolve_releases_transformation_activation_lineage(self) -> None:
        rows = self._resolve_transformations()
        self.assertGreaterEqual(len(rows), 4)
        required = {
            "activation_id",
            "transformation_type",
            "target_entity_id",
            "target_display_name",
            "target_address",
            "source_layer",
            "source_stem",
            "context_id",
            "assignment_id",
            "mechanism_id",
            "generator_id",
            "algorithm_version",
            "source_refs",
        }
        for row in rows:
            self.assertTrue(required.issubset(row))
            self.assertTrue(row["transformation_type"])
            self.assertTrue(row["target_display_name"])
            self.assertIsInstance(row["target_address"], dict)
            self.assertIsInstance(row["source_refs"], list)

    def test_asset_reads_only_canonical_resolve_transformations(self) -> None:
        self.assertIn(
            "payload?.combined_resolution?.ziwei_bundle?.candidate?.chart?.transformations",
            ZIWEI_TRANSFORMATION_PROVENANCE_JS,
        )
        for field in (
            "activation_id",
            "transformation_type",
            "target_entity_id",
            "target_display_name",
            "target_address",
            "source_layer",
            "source_stem",
            "context_id",
            "assignment_id",
            "mechanism_id",
            "generator_id",
            "algorithm_version",
            "source_refs",
        ):
            with self.subTest(field=field):
                self.assertIn(field, ZIWEI_TRANSFORMATION_PROVENANCE_JS)
        self.assertIn("path === '/api/resolve'", ZIWEI_TRANSFORMATION_PROVENANCE_JS)
        self.assertIn("Array.isArray(transformations)", ZIWEI_TRANSFORMATION_PROVENANCE_JS)
        self.assertIn("transformations.filter(validActivation)", ZIWEI_TRANSFORMATION_PROVENANCE_JS)

    def test_asset_does_not_reimplement_transformation_rules_or_direction(self) -> None:
        for forbidden in (
            "ASSIGNMENTS_BY_STEM",
            "S08_CURRENT_40_ASSIGNMENT_R1",
            "S08_TRANSFORMATION_RULE_SET",
            "TransformationGenerator",
            "transformation_type =",
            "target_entity_id =",
            "ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION",
            "SAME",
            "OPPOSITE",
            "OUTWARD",
            "INWARD",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_TRANSFORMATION_PROVENANCE_JS)

    def test_html_injection_is_single_and_external_asset_only(self) -> None:
        base = "<html><head></head><body><main></main></body></html>"
        injected = ziwei_transformation_provenance_index_html(base)
        self.assertIn(
            '<link rel="stylesheet" href="/ziwei-transformation-provenance.css">',
            injected,
        )
        self.assertIn(
            '<script src="/ziwei-transformation-provenance.js" defer></script>',
            injected,
        )
        with self.assertRaisesRegex(ValueError, "already injected"):
            ziwei_transformation_provenance_index_html(injected)

    def test_workbench_publishes_transformation_provenance_assets_without_version_bump(self) -> None:
        self.assertEqual("CombinedChartWorkbenchLocalApp/1.12", _WorkbenchHandler.server_version)
        server = build_workbench_server(ROOT, port=0)
        host, port = server.server_address[:2]
        self.assertEqual("127.0.0.1", host)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urlopen(f"http://{host}:{port}/", timeout=30) as response:
                index = response.read().decode("utf-8")
                self.assertEqual(200, response.status)
            self.assertIn("/ziwei-transformation-provenance.css", index)
            self.assertIn("/ziwei-transformation-provenance.js", index)

            with urlopen(
                f"http://{host}:{port}/ziwei-transformation-provenance.css", timeout=30
            ) as response:
                css = response.read().decode("utf-8")
                self.assertEqual(200, response.status)
                self.assertEqual(ZIWEI_TRANSFORMATION_PROVENANCE_CSS, css)

            with urlopen(
                f"http://{host}:{port}/ziwei-transformation-provenance.js", timeout=30
            ) as response:
                script = response.read().decode("utf-8")
                self.assertEqual(200, response.status)
                self.assertEqual(ZIWEI_TRANSFORMATION_PROVENANCE_JS, script)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

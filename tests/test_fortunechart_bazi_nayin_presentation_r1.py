from __future__ import annotations

import json
import threading
import unittest
import urllib.request
from pathlib import Path

from fortune_training.combined_chart_application.local_app import (
    LocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.nayin_assets import (
    NAYIN_JS,
    nayin_index_html,
)
from fortune_training.combined_chart_application.nayin_local_app import (
    NAYIN_PRESENTATION_SCHEMA,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class FortuneChartBaziNayinPresentationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.base_app = LocalCombinedChartApplication(ROOT)

    @staticmethod
    def base_payload() -> dict[str, object]:
        return {
            "birth_datetime": "1994-05-17T14:30:00",
            "birth_place": "Beijing",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone_id": "Asia/Shanghai",
            "sex": "MALE",
            "precision": "EXACT_SECOND",
            "uncertainty_seconds": 0,
            "ziwei_daxian_count": 12,
            "ziwei_daxian_frame_id": "DAXIAN:index=1",
            "ziwei_annual_year": 2025,
            "ziwei_minor_limit_age": 8,
            "bazi_natal_profile_id": "BAZI-FOUNDATION-V1-R1",
            "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "bazi_dayun_count": 12,
            "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
        }

    @classmethod
    def multi_candidate_payload(cls) -> dict[str, object]:
        return {
            **cls.base_payload(),
            "birth_datetime": "1994-05-17T23:11:00",
            "precision": "APPROXIMATE",
            "uncertainty_seconds": 120,
            "bazi_natal_profile_id": "BAZI-FOUNDATION-ZI-START-23-R1",
        }

    def test_presentation_reuses_exact_released_nayin_sidecar(self) -> None:
        response = self.app.resolve_bazi_nayin_presentation_payload(
            self.base_payload()
        )
        self.assertEqual(NAYIN_PRESENTATION_SCHEMA, response["schema"])
        self.assertTrue(response["source_combined_manifest_hash"])
        self.assertTrue(response["source_bazi_bundle_hash"])
        self.assertGreaterEqual(len(response["candidates"]), 1)

        for application_index, candidate in enumerate(response["candidates"]):
            with self.subTest(application_index=application_index):
                self.assertEqual(
                    application_index,
                    candidate["application_candidate_index"],
                )
                self.assertIsInstance(candidate["natal_candidate_index"], int)
                resolution = candidate["nayin_resolution"]
                self.assertEqual(
                    candidate["source_natal_fact_hash"],
                    resolution["source_natal_fact_hash"],
                )
                self.assertEqual(
                    candidate["source_natal_computation_hash"],
                    resolution["source_natal_computation_hash"],
                )
                annotations = resolution["annotations"]
                self.assertEqual(
                    ["YEAR", "MONTH", "DAY", "HOUR"],
                    [row["source_pillar_position"] for row in annotations],
                )
                self.assertTrue(
                    all(
                        isinstance(row["display_name"], str)
                        and row["display_name"].strip()
                        for row in annotations
                    )
                )

    def test_legacy_resolve_contract_is_unchanged(self) -> None:
        payload = self.base_payload()
        self.assertEqual(
            self.base_app.resolve_payload(dict(payload)),
            self.app.resolve_payload(dict(payload)),
        )

    def test_multi_candidate_nayin_binding_tracks_exact_natal_candidates(self) -> None:
        response = self.app.resolve_bazi_nayin_presentation_payload(
            self.multi_candidate_payload()
        )
        candidates = response["candidates"]
        self.assertGreaterEqual(len(candidates), 2)
        self.assertEqual(
            list(range(len(candidates))),
            [row["application_candidate_index"] for row in candidates],
        )
        natal_indices = {
            row["natal_candidate_index"] for row in candidates
        }
        self.assertGreaterEqual(len(natal_indices), 2)
        self.assertEqual(set(range(len(natal_indices))), natal_indices)

        exact_lineages = set()
        for candidate in candidates:
            resolution = candidate["nayin_resolution"]
            self.assertEqual(
                candidate["source_natal_fact_hash"],
                resolution["source_natal_fact_hash"],
            )
            self.assertEqual(
                candidate["source_natal_computation_hash"],
                resolution["source_natal_computation_hash"],
            )
            annotations = resolution["annotations"]
            self.assertEqual(
                ["YEAR", "MONTH", "DAY", "HOUR"],
                [row["source_pillar_position"] for row in annotations],
            )
            by_position = {
                row["source_pillar_position"]: row["source_pillar_ganzhi"]
                for row in annotations
            }
            exact_lineages.add(
                (
                    candidate["natal_candidate_index"],
                    candidate["source_natal_fact_hash"],
                    candidate["source_natal_computation_hash"],
                    by_position["DAY"],
                    by_position["HOUR"],
                )
            )
        self.assertEqual(len(natal_indices), len(exact_lineages))

    def test_browser_contract_is_candidate_bound_and_source_only(self) -> None:
        for required in (
            "/api/bazi-nayin-presentation",
            "application_candidate_index",
            "natal_candidate_index",
            "source_pillar_ganzhi",
            "display_name",
            ".bazi-candidate-select",
            "MutationObserver",
            "纳音：",
        ):
            with self.subTest(required=required):
                self.assertIn(required, NAYIN_JS)

        for forbidden in (
            "NAYIN_PAIRS",
            "nayin_name",
            "selected_candidate_index",
            "bazi-nayin-panel",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, NAYIN_JS)

    def test_nayin_asset_injection_is_additive_and_idempotent(self) -> None:
        html = nayin_index_html("<html><head></head><body></body></html>")
        self.assertEqual(1, html.count("/nayin.css"))
        self.assertEqual(1, html.count("/nayin.js"))
        with self.assertRaises(ValueError):
            nayin_index_html(html)

    def test_real_workbench_server_exposes_nayin_assets_and_endpoint(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            base_url = f"http://{host}:{port}"

            with urllib.request.urlopen(f"{base_url}/", timeout=10) as response:
                html = response.read().decode("utf-8")
            self.assertEqual(1, html.count("/nayin.css"))
            self.assertEqual(1, html.count("/nayin.js"))

            with urllib.request.urlopen(f"{base_url}/nayin.css", timeout=10) as response:
                css = response.read().decode("utf-8")
            self.assertIn(".pillar .bazi-nayin", css)

            with urllib.request.urlopen(f"{base_url}/nayin.js", timeout=10) as response:
                js = response.read().decode("utf-8")
            self.assertIn("/api/bazi-nayin-presentation", js)

            request = urllib.request.Request(
                f"{base_url}/api/bazi-nayin-presentation",
                data=json.dumps(self.base_payload()).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                presentation = json.loads(response.read().decode("utf-8"))
            self.assertEqual(
                NAYIN_PRESENTATION_SCHEMA,
                presentation["schema"],
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

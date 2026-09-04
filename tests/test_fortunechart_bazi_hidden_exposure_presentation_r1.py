from __future__ import annotations

import json
import threading
import unittest
import urllib.request
from pathlib import Path

from fortune_training.combined_chart_application.bazi_hidden_exposure_assets import (
    BAZI_HIDDEN_EXPOSURE_JS,
    bazi_hidden_exposure_index_html,
)
from fortune_training.combined_chart_application.bazi_hidden_exposure_local_app import (
    BAZI_HIDDEN_EXPOSURE_PRESENTATION_SCHEMA,
)
from fortune_training.combined_chart_application.local_app import (
    LocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class FortuneChartBaziHiddenExposurePresentationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.base_app = LocalCombinedChartApplication(ROOT)

    @staticmethod
    def base_payload() -> dict[str, object]:
        # 1974 is 甲寅 after 立春, guaranteeing at least the YEAR.寅藏甲 ↔ YEAR.甲
        # exact identity link without depending on any strength/rooting interpretation.
        return {
            "birth_datetime": "1974-05-17T14:30:00",
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
            "birth_datetime": "1974-05-17T23:11:00",
            "precision": "APPROXIMATE",
            "uncertainty_seconds": 120,
            "bazi_natal_profile_id": "BAZI-FOUNDATION-ZI-START-23-R1",
        }

    def test_presentation_is_exact_same_stem_identity_only(self) -> None:
        response = self.app.resolve_bazi_hidden_exposure_presentation_payload(
            self.base_payload()
        )
        self.assertEqual(BAZI_HIDDEN_EXPOSURE_PRESENTATION_SCHEMA, response["schema"])
        self.assertEqual("EXACT_STEM_IDENTITY_MATCH_ONLY", response["semantics"])
        self.assertTrue(response["source_combined_manifest_hash"])
        self.assertTrue(response["source_bazi_bundle_hash"])
        self.assertGreaterEqual(len(response["candidates"]), 1)

        found_year_jia = False
        for application_index, candidate in enumerate(response["candidates"]):
            with self.subTest(application_index=application_index):
                self.assertEqual(
                    application_index, candidate["application_candidate_index"]
                )
                self.assertTrue(candidate["source_natal_fact_hash"])
                self.assertTrue(candidate["source_natal_computation_hash"])
                for exposure in candidate["exposures"]:
                    self.assertEqual("EXACT_STEM", exposure["match_kind"])
                    hidden = exposure["hidden_stem"]
                    visible = exposure["visible_stem"]
                    self.assertEqual(exposure["stem"], hidden["stem"])
                    self.assertEqual(exposure["stem"], visible["stem"])
                    self.assertIn(
                        hidden["branch_position"], {"YEAR", "MONTH", "DAY", "HOUR"}
                    )
                    self.assertIn(
                        visible["position"], {"YEAR", "MONTH", "DAY", "HOUR"}
                    )
                    self.assertGreaterEqual(len(exposure["source_refs"]), 1)
                    if (
                        hidden["branch_position"] == "YEAR"
                        and visible["position"] == "YEAR"
                        and exposure["stem"] == "甲"
                    ):
                        found_year_jia = True
        self.assertTrue(found_year_jia)

    def test_legacy_resolve_contract_is_unchanged(self) -> None:
        payload = self.base_payload()
        self.assertEqual(
            self.base_app.resolve_payload(dict(payload)),
            self.app.resolve_payload(dict(payload)),
        )

    def test_multi_candidate_binding_preserves_application_rows_and_natal_reuse(self) -> None:
        response = self.app.resolve_bazi_hidden_exposure_presentation_payload(
            self.multi_candidate_payload()
        )
        candidates = response["candidates"]
        self.assertGreaterEqual(len(candidates), 2)
        self.assertEqual(
            list(range(len(candidates))),
            [row["application_candidate_index"] for row in candidates],
        )
        natal_indices = {row["natal_candidate_index"] for row in candidates}
        self.assertGreaterEqual(len(natal_indices), 2)
        self.assertEqual(set(range(len(natal_indices))), natal_indices)

        by_lineage: dict[tuple[object, object, object], list[dict[str, object]]] = {}
        for row in candidates:
            key = (
                row["natal_candidate_index"],
                row["source_natal_fact_hash"],
                row["source_natal_computation_hash"],
            )
            by_lineage.setdefault(key, []).append(row)
        for rows in by_lineage.values():
            expected = rows[0]["exposures"]
            for row in rows[1:]:
                self.assertEqual(expected, row["exposures"])

    def test_browser_contract_is_candidate_bound_and_non_judgmental(self) -> None:
        for required in (
            "/api/bazi-hidden-exposure-presentation",
            "application_candidate_index",
            "natal_candidate_index",
            ".bazi-candidate-select",
            "EXACT_STEM_IDENTITY_MATCH_ONLY",
            "EXACT_STEM",
            "本命藏干同干显干匹配",
            "不判通根、得地、旺衰、喜用或吉凶",
        ):
            with self.subTest(required=required):
                self.assertIn(required, BAZI_HIDDEN_EXPOSURE_JS)
        for forbidden in (
            "same_element_hidden_stem_instance_ids",
            "affinities",
            "喜用神",
            "winner",
            "五行强弱",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, BAZI_HIDDEN_EXPOSURE_JS)

    def test_asset_injection_adds_stable_sibling_panel_and_is_idempotent(self) -> None:
        source = (
            '<html><head></head><body><div id="bazi-chart" '
            'class="placeholder">等待排盘</div></body></html>'
        )
        html = bazi_hidden_exposure_index_html(source)
        self.assertEqual(1, html.count('id="bazi-chart"'))
        self.assertEqual(1, html.count('id="bazi-hidden-exposure"'))
        self.assertEqual(1, html.count("/bazi-hidden-exposure.css"))
        self.assertEqual(1, html.count("/bazi-hidden-exposure.js"))
        with self.assertRaises(ValueError):
            bazi_hidden_exposure_index_html(html)

    def test_parity_matrix_registers_visible_exposure_fact(self) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}
        row = rows["BAZI_NATAL_HIDDEN_STEM_EXPOSURE_MATCHES"]
        self.assertEqual("BAZI", row["system"])
        self.assertEqual("ALREADY_VISIBLE", row["status"])
        self.assertEqual(
            "src/fortune_training/bazi_chart/hidden_stems.py",
            row["backend_evidence"]["path"],
        )
        self.assertEqual(
            "src/fortune_training/combined_chart_application/bazi_hidden_exposure_local_app.py",
            row["api_evidence"]["path"],
        )
        self.assertEqual(
            "src/fortune_training/combined_chart_application/bazi_hidden_exposure_assets.py",
            row["workbench_evidence"]["path"],
        )

    def test_real_workbench_server_exposes_assets_and_endpoint(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            base_url = f"http://{host}:{port}"
            with urllib.request.urlopen(f"{base_url}/", timeout=10) as response:
                html = response.read().decode("utf-8")
            self.assertEqual(1, html.count("/bazi-hidden-exposure.css"))
            self.assertEqual(1, html.count("/bazi-hidden-exposure.js"))
            self.assertEqual(1, html.count('id="bazi-hidden-exposure"'))

            with urllib.request.urlopen(
                f"{base_url}/bazi-hidden-exposure.js", timeout=10
            ) as response:
                js = response.read().decode("utf-8")
            self.assertIn("/api/bazi-hidden-exposure-presentation", js)

            request = urllib.request.Request(
                f"{base_url}/api/bazi-hidden-exposure-presentation",
                data=json.dumps(self.base_payload()).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                presentation = json.loads(response.read().decode("utf-8"))
            self.assertEqual(
                BAZI_HIDDEN_EXPOSURE_PRESENTATION_SCHEMA,
                presentation["schema"],
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

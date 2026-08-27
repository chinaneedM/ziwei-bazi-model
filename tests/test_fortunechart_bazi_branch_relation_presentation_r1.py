from __future__ import annotations

import json
import threading
import unittest
import urllib.request
from pathlib import Path

from fortune_training.combined_chart_application.bazi_branch_relation_assets import (
    BAZI_BRANCH_RELATION_JS,
    bazi_branch_relation_index_html,
)
from fortune_training.combined_chart_application.bazi_branch_relation_local_app import (
    BAZI_BRANCH_RELATION_PRESENTATION_SCHEMA,
)
from fortune_training.combined_chart_application.local_app import (
    LocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class FortuneChartBaziBranchRelationPresentationR1Tests(unittest.TestCase):
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

    def test_presentation_is_hash_bound_branch_relation_identity_only(self) -> None:
        response = self.app.resolve_bazi_branch_relation_presentation_payload(
            self.base_payload()
        )
        self.assertEqual(BAZI_BRANCH_RELATION_PRESENTATION_SCHEMA, response["schema"])
        self.assertEqual("RELATION_IDENTITY_ONLY", response["semantics"])
        self.assertTrue(response["source_combined_manifest_hash"])
        self.assertTrue(response["source_bazi_bundle_hash"])
        self.assertGreaterEqual(len(response["candidates"]), 1)

        encoded = json.dumps(response, ensure_ascii=False)
        self.assertNotIn("nominal_transformation_element", encoded)
        for application_index, candidate in enumerate(response["candidates"]):
            with self.subTest(application_index=application_index):
                self.assertEqual(
                    application_index, candidate["application_candidate_index"]
                )
                self.assertTrue(candidate["source_natal_fact_hash"])
                self.assertTrue(candidate["source_natal_computation_hash"])
                for relation in candidate["branch_relations"]:
                    self.assertTrue(relation["relation_family"].startswith("BRANCH_"))
                    self.assertEqual(relation["arity"], len(relation["participants"]))
                    self.assertGreaterEqual(len(relation["source_refs"]), 1)
                    for participant in relation["participants"]:
                        self.assertIn(
                            participant["position"], {"YEAR", "MONTH", "DAY", "HOUR"}
                        )
                        self.assertTrue(participant["instance_id"])
                        self.assertTrue(participant["branch"])

    def test_legacy_resolve_contract_is_unchanged(self) -> None:
        payload = self.base_payload()
        self.assertEqual(
            self.base_app.resolve_payload(dict(payload)),
            self.app.resolve_payload(dict(payload)),
        )

    def test_multi_candidate_binding_tracks_exact_application_candidates(self) -> None:
        response = self.app.resolve_bazi_branch_relation_presentation_payload(
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
        lineages = {
            (
                row["natal_candidate_index"],
                row["source_natal_fact_hash"],
                row["source_natal_computation_hash"],
            )
            for row in candidates
        }
        self.assertEqual(len(candidates), len(lineages))

    def test_browser_contract_is_candidate_bound_and_non_judgmental(self) -> None:
        for required in (
            "/api/bazi-branch-relations-presentation",
            "application_candidate_index",
            "natal_candidate_index",
            ".bazi-candidate-select",
            "RELATION_IDENTITY_ONLY",
            "BRANCH_SIX_HARMONY",
            "BRANCH_TRINE",
            "BRANCH_CLASH",
            "BRANCH_CHUAN",
            "BRANCH_PUNISHMENT",
            "不判合化、成败、强弱或吉凶",
        ):
            with self.subTest(required=required):
                self.assertIn(required, BAZI_BRANCH_RELATION_JS)
        for forbidden in (
            "nominal_transformation_element",
            "喜用神",
            "五行强弱",
            "winner",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, BAZI_BRANCH_RELATION_JS)

    def test_asset_injection_adds_stable_sibling_panel_and_is_idempotent(self) -> None:
        source = (
            '<html><head></head><body><div id="bazi-chart" '
            'class="placeholder">等待排盘</div></body></html>'
        )
        html = bazi_branch_relation_index_html(source)
        self.assertEqual(1, html.count('id="bazi-chart"'))
        self.assertEqual(1, html.count('id="bazi-branch-relations"'))
        self.assertEqual(1, html.count("/bazi-branch-relations.css"))
        self.assertEqual(1, html.count("/bazi-branch-relations.js"))
        with self.assertRaises(ValueError):
            bazi_branch_relation_index_html(html)

    def test_real_workbench_server_exposes_assets_and_endpoint(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            base_url = f"http://{host}:{port}"
            with urllib.request.urlopen(f"{base_url}/", timeout=10) as response:
                html = response.read().decode("utf-8")
            self.assertEqual(1, html.count("/bazi-branch-relations.css"))
            self.assertEqual(1, html.count("/bazi-branch-relations.js"))
            self.assertEqual(1, html.count('id="bazi-branch-relations"'))

            with urllib.request.urlopen(
                f"{base_url}/bazi-branch-relations.js", timeout=10
            ) as response:
                js = response.read().decode("utf-8")
            self.assertIn("/api/bazi-branch-relations-presentation", js)

            request = urllib.request.Request(
                f"{base_url}/api/bazi-branch-relations-presentation",
                data=json.dumps(self.base_payload()).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                presentation = json.loads(response.read().decode("utf-8"))
            self.assertEqual(
                BAZI_BRANCH_RELATION_PRESENTATION_SCHEMA,
                presentation["schema"],
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()

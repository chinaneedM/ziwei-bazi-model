from __future__ import annotations

import json
import threading
import unittest
import urllib.request
from pathlib import Path

import jsonschema

from fortune_training.combined_chart_application.flow_local_app import (
    FlowLocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.interaction_local_app import (
    InteractionLocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.local_app import (
    LOCAL_APP_HEALTH_SCHEMA,
    LOCAL_APP_ID,
    LOCAL_APP_VERSION,
    LocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.target_flow_assets import (
    TARGET_FLOW_CSS,
    TARGET_FLOW_JS,
    target_flow_index_html,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedBrowserBaziTargetFlowSidecarR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.flow_app = FlowLocalCombinedChartApplication(ROOT)
        cls.interaction_app = InteractionLocalCombinedChartApplication(ROOT)
        cls.base_app = LocalCombinedChartApplication(ROOT)
        cls.flow_response_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "combined-local-target-flow-response-r1.schema.json"
            ).read_text(encoding="utf-8")
        )
        cls.flow_binding_schema = json.loads(
            (
                ROOT / "schemas" / "combined-target-flow-composition-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

    @staticmethod
    def base_payload(*, ziwei_annual_year: int | None = 2025) -> dict[str, object]:
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
            "ziwei_annual_year": ziwei_annual_year,
            "ziwei_minor_limit_age": 8,
            "bazi_natal_profile_id": "BAZI-FOUNDATION-V1-R1",
            "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "bazi_dayun_count": 12,
            "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
        }

    @classmethod
    def flow_payload(
        cls,
        *,
        target_datetime: str = "2026-06-01T12:00:00",
        target_place: str = "Greenwich",
        target_latitude: float = 51.4769,
        target_longitude: float = 0.0,
        target_timezone_id: str = "Etc/UTC",
        ziwei_annual_year: int | None = 2025,
    ) -> dict[str, object]:
        return {
            **cls.base_payload(ziwei_annual_year=ziwei_annual_year),
            "target_datetime": target_datetime,
            "target_place": target_place,
            "target_latitude": target_latitude,
            "target_longitude": target_longitude,
            "target_timezone_id": target_timezone_id,
            "target_precision": "EXACT_SECOND",
            "target_uncertainty_seconds": 0,
            "target_temporal_profile_id": (
                "BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1"
            ),
        }

    def test_workbench_reuses_exact_released_flow_payload_without_fork(self) -> None:
        payload = self.flow_payload()
        expected = self.flow_app.resolve_flow_payload(dict(payload))
        actual = self.app.resolve_flow_payload(dict(payload))
        self.assertEqual(expected, actual)
        jsonschema.Draft202012Validator(self.flow_response_schema).validate(actual)
        jsonschema.Draft202012Validator(self.flow_binding_schema).validate(
            actual["combined_target_flow_resolution"]
        )
        self.assertEqual(
            actual["combined_resolution"]["bazi_bundle"]["bundle_hash"],
            actual["bazi_target_flow_bundle"]["base_application_bundle_hash"],
        )

    def test_workbench_health_preserves_released_browser_contract(self) -> None:
        health = self.app.health()
        self.assertEqual(LOCAL_APP_HEALTH_SCHEMA, health["schema"])
        self.assertEqual(LOCAL_APP_ID, health["application_id"])
        self.assertEqual(LOCAL_APP_VERSION, health["application_version"])
        self.assertNotIn("target_flow_endpoint", health)
        self.assertEqual(self.base_app.health(), health)

    def test_legacy_resolve_and_ziwei_interaction_remain_exact(self) -> None:
        base_payload = self.base_payload()
        self.assertEqual(
            self.interaction_app.resolve_payload(dict(base_payload)),
            self.app.resolve_payload(dict(base_payload)),
        )
        interaction_payload = {
            **base_payload,
            "ziwei_origin_designation_id": "LIFE",
        }
        self.assertEqual(
            self.interaction_app.resolve_ziwei_interaction_payload(
                dict(interaction_payload)
            ),
            self.app.resolve_ziwei_interaction_payload(dict(interaction_payload)),
        )

    def test_target_year_remains_independent_from_explicit_ziwei_year(self) -> None:
        response = self.app.resolve_flow_payload(
            self.flow_payload(
                target_datetime="2026-08-18T12:00:00",
                ziwei_annual_year=2025,
            )
        )
        binding = response["combined_target_flow_resolution"]
        self.assertEqual(2025, binding["ziwei_selected_annual_year"])
        self.assertEqual(
            "2026-08-18T12:00:00",
            binding["target_input"]["reported_local_datetime"],
        )

    def test_flow_resolution_does_not_mutate_ziwei_interaction_identity(self) -> None:
        interaction_payload = {
            **self.base_payload(),
            "ziwei_origin_designation_id": "LIFE",
        }
        before = self.app.resolve_ziwei_interaction_payload(
            dict(interaction_payload)
        )
        self.app.resolve_flow_payload(self.flow_payload())
        after = self.app.resolve_ziwei_interaction_payload(
            dict(interaction_payload)
        )
        self.assertEqual(before, after)

    def test_dst_fold_preserves_two_explicit_target_candidates(self) -> None:
        response = self.app.resolve_flow_payload(
            self.flow_payload(
                target_datetime="2026-11-01T01:30:00",
                target_place="New York",
                target_latitude=40.7128,
                target_longitude=-74.006,
                target_timezone_id="America/New_York",
            )
        )
        bundle = response["bazi_target_flow_bundle"]
        self.assertEqual("MULTI_CANDIDATE", bundle["status"])
        self.assertEqual(2, len(bundle["candidates"]))
        self.assertEqual(
            {0, 1},
            {
                row["source_target_coordinate_candidate_index"]
                for row in bundle["candidates"]
            },
        )
        self.assertEqual(
            2,
            len(
                {
                    row["view"]["target"]["target_utc"]
                    for row in bundle["candidates"]
                }
            ),
        )

    def test_browser_requires_explicit_selection_for_multi_candidate_flow(self) -> None:
        self.assertIn("请选择候选", TARGET_FLOW_JS)
        self.assertIn("未自动锁定第 1 个", TARGET_FLOW_JS)
        self.assertIn("candidateSelect.value === ''", TARGET_FLOW_JS)
        self.assertIn("if (candidates.length === 1)", TARGET_FLOW_JS)
        self.assertNotIn("candidateSelect.value = '0'", TARGET_FLOW_JS)

    def test_browser_renders_both_xiaoyun_candidates_without_selecting_a_winner(self) -> None:
        self.assertIn("view.timeline.xiaoyun.candidates.forEach", TARGET_FLOW_JS)
        self.assertIn("小运候选", TARGET_FLOW_JS)
        self.assertIn("row.activation_status", TARGET_FLOW_JS)

    def test_browser_renders_temporal_classical_annotations_read_only(self) -> None:
        self.assertIn("view.timeline.classical_annotations", TARGET_FLOW_JS)
        self.assertIn("annotation.visible_ten_god.display_name", TARGET_FLOW_JS)
        self.assertIn("annotation.hidden_stems.map", TARGET_FLOW_JS)
        self.assertIn("annotation.nayin.display_name", TARGET_FLOW_JS)
        self.assertIn("annotation.xunkong.display_name", TARGET_FLOW_JS)
        self.assertIn("annotation.day_master_twelve_growth.phase", TARGET_FLOW_JS)
        self.assertIn("annotation.self_twelve_growth.phase", TARGET_FLOW_JS)
        self.assertIn("annotation_fact=${annotation.fact_hash}", TARGET_FLOW_JS)
        self.assertIn(".bazi-flow-annotation", TARGET_FLOW_CSS)
        for forbidden in ("旺衰", "格局", "用神", "喜忌", "预测"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, TARGET_FLOW_JS)

    def test_browser_renders_structural_projection_as_neutral_read_only_facts(self) -> None:
        self.assertIn("renderStructural(view.structural)", TARGET_FLOW_JS)
        self.assertIn("structural.active_temporal_stems.forEach", TARGET_FLOW_JS)
        self.assertIn("structural.temporal_hidden_stems.filter", TARGET_FLOW_JS)
        self.assertIn("structural.temporal_ten_gods.map", TARGET_FLOW_JS)
        self.assertIn("structural.dynamic_exposures.forEach", TARGET_FLOW_JS)
        self.assertIn("structural.dynamic_affinities.forEach", TARGET_FLOW_JS)
        self.assertIn("exposure.link_id", TARGET_FLOW_JS)
        self.assertIn("affinity.fact_id", TARGET_FLOW_JS)
        self.assertIn("affinity.rule_set_id", TARGET_FLOW_JS)
        self.assertIn("structural.relations.forEach", TARGET_FLOW_JS)
        self.assertIn("relation.participant_instance_ids.join", TARGET_FLOW_JS)
        self.assertIn("relation.rule_set_id", TARGET_FLOW_JS)
        self.assertIn("relation.source_refs.join", TARGET_FLOW_JS)
        self.assertIn("名义目标五行", TARGET_FLOW_JS)
        self.assertIn("非成化结论", TARGET_FLOW_JS)
        self.assertIn("不判强弱、作用或合化成败", TARGET_FLOW_JS)
        self.assertIn("structural_projection_fact", TARGET_FLOW_JS)
        self.assertIn(".bazi-flow-structural", TARGET_FLOW_CSS)
        self.assertIn(".bazi-flow-structural-layer", TARGET_FLOW_CSS)

    def test_browser_flow_never_writes_ziwei_selector_or_svg_state(self) -> None:
        for forbidden in (
            "$('ziwei-daxian-frame-id').value =",
            "$('ziwei-annual-year').value =",
            "$('ziwei-minor-limit-age').value =",
            "$('ziwei-chart').innerHTML",
            "querySelector('#ziwei-chart')",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, TARGET_FLOW_JS)
        self.assertIn("/api/resolve-flow", TARGET_FLOW_JS)
        self.assertIn("不会自动同步或改写紫微", TARGET_FLOW_JS)

    def test_browser_invalidates_flow_after_source_or_target_input_changes(self) -> None:
        self.assertIn("function invalidateFlow()", TARGET_FLOW_JS)
        self.assertIn("state.displayedFingerprint = null", TARGET_FLOW_JS)
        self.assertIn("当前目标 flow 已失效", TARGET_FLOW_JS)
        for field_id in (
            "birth-datetime",
            "timezone-id",
            "ziwei-annual-year",
            "bazi-natal-profile",
            "bazi-temporal-profile",
            "target-datetime",
            "target-longitude",
            "target-timezone-id",
        ):
            with self.subTest(field_id=field_id):
                self.assertIn(f"'{field_id}'", TARGET_FLOW_JS)

    def test_real_workbench_server_exposes_all_three_routes(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]

            with urllib.request.urlopen(
                f"http://{host}:{port}/health", timeout=10
            ) as response:
                health = json.loads(response.read().decode("utf-8"))
            self.assertEqual(LOCAL_APP_HEALTH_SCHEMA, health["schema"])

            flow_request = urllib.request.Request(
                f"http://{host}:{port}/api/resolve-flow",
                data=json.dumps(self.flow_payload()).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(flow_request, timeout=20) as response:
                flow = json.loads(response.read().decode("utf-8"))
            jsonschema.Draft202012Validator(self.flow_response_schema).validate(flow)

            interaction_request = urllib.request.Request(
                f"http://{host}:{port}/api/ziwei-interaction",
                data=json.dumps(
                    {
                        **self.base_payload(),
                        "ziwei_origin_designation_id": "LIFE",
                    }
                ).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(interaction_request, timeout=20) as response:
                interaction = json.loads(response.read().decode("utf-8"))
            self.assertEqual(
                "ZIWEI-SANHE-INTERACTION-RESOLUTION-R1",
                interaction["interaction"]["schema"],
            )

            base_request = urllib.request.Request(
                f"http://{host}:{port}/api/resolve",
                data=json.dumps(self.base_payload()).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(base_request, timeout=20) as response:
                base = json.loads(response.read().decode("utf-8"))
            self.assertEqual(
                "ZIWEI-BAZI-COMBINED-LOCAL-APP-RESOLVE-V1",
                base["schema"],
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_composed_page_injects_target_flow_assets_once(self) -> None:
        html = target_flow_index_html("<html><head></head><body></body></html>")
        self.assertEqual(1, html.count("/target-flow.css"))
        self.assertEqual(1, html.count("/target-flow.js"))
        with self.assertRaises(ValueError):
            target_flow_index_html(html)


if __name__ == "__main__":
    unittest.main()

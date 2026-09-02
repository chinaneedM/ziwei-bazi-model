from __future__ import annotations

import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from fortune_training.combined_chart_application.local_app import (
    LocalCombinedAppRequestError,
)
from fortune_training.combined_chart_application.palace_stem_topology_assets import (
    PALACE_STEM_TOPOLOGY_JS,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
)
from fortune_training.ziwei_application.structural_relations import (
    STRUCTURAL_RELATION_PROJECTIONS_SCHEMA,
    STRUCTURAL_RELATION_PROJECTIONS_SEMANTIC_SCOPE,
    validate_structural_relation_projections,
)


ROOT = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
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
        "ziwei_daxian_frame_id": None,
        "ziwei_annual_year": 2025,
        "ziwei_lunar_month": 4,
        "ziwei_minor_limit_age": None,
        "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
        "bazi_dayun_count": 12,
        "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
    }


class ZiweiStructuralRelationSidecarR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.payload = _payload()
        combined, expected_hash, bundle = cls.app._resolve_ziwei_sidecar_source(
            dict(cls.payload)
        )
        cls.combined = combined
        cls.expected_hash = expected_hash
        cls.bundle = bundle
        cls.resolution = cls.app.ziwei_structural_relation_service.resolve(bundle)
        cls.response = cls.app.resolve_ziwei_structural_relations_payload(
            dict(cls.payload)
        )
        cls.exported = cls.response["ziwei_structural_relation_projections"]

    def test_sidecar_is_bound_to_exact_released_application_bundle_and_r2(self) -> None:
        self.assertEqual(self.bundle.bundle_hash, self.expected_hash)
        self.assertEqual(self.response["source_ziwei_bundle_hash"], self.expected_hash)
        self.assertEqual(
            self.exported["source_application_bundle_hash"],
            self.expected_hash,
        )
        self.assertEqual(
            self.exported["source_r2_fact_hash"],
            self.bundle.r2_state.hashes.fact_hash,
        )
        self.assertEqual(
            self.exported["source_r2_computation_hash"],
            self.bundle.r2_state.hashes.computation_hash,
        )
        self.assertEqual(
            self.response["source_combined_manifest_hash"],
            self.combined["manifest_hash"],
        )

    def test_r6_r7_r8_are_complete_read_only_natal_projections(self) -> None:
        self.assertEqual(self.exported["schema"], STRUCTURAL_RELATION_PROJECTIONS_SCHEMA)
        self.assertEqual(self.exported["status"], "COMPLETE")
        self.assertEqual(self.exported["integrity"]["status"], "PASS")
        self.assertEqual(
            self.exported["semantic_scope"],
            STRUCTURAL_RELATION_PROJECTIONS_SEMANTIC_SCOPE,
        )
        self.assertEqual(len(self.exported["qishu"]["qishu_facts"]), 12)
        self.assertEqual(len(self.exported["one_six"]["one_six_facts"]), 12)
        self.assertEqual(
            len(self.exported["adjacent_palace"]["adjacent_palace_pairs"]),
            12,
        )
        for component in ("qishu", "one_six", "adjacent_palace"):
            with self.subTest(component=component):
                state = self.exported[component]
                self.assertEqual(state["time_layer"], "NATAL")
                self.assertEqual(state["integrity"]["status"], "PASS")
                self.assertEqual(
                    state["upstream_r2_fact_hash"],
                    self.bundle.r2_state.hashes.fact_hash,
                )
                self.assertEqual(
                    state["upstream_r2_computation_hash"],
                    self.bundle.r2_state.hashes.computation_hash,
                )

    def test_r6_reuses_frozen_qishu_geometry_without_reinterpretation(self) -> None:
        for fact in self.exported["qishu"]["qishu_facts"]:
            with self.subTest(origin=fact["origin_designation_id"]):
                self.assertEqual(fact["relative_ordinal"], 9)
                self.assertEqual(fact["clockwise_offset"], 4)

    def test_r7_r8_permission_gates_remain_closed(self) -> None:
        for fact in self.exported["one_six"]["one_six_facts"]:
            self.assertFalse(fact["direct_event_permission"])
            self.assertFalse(fact["direct_endpoint_permission"])
        for fact in self.exported["adjacent_palace"]["adjacent_palace_pairs"]:
            self.assertFalse(fact["direct_event_permission"])
            self.assertFalse(fact["direct_endpoint_permission"])
            self.assertFalse(fact["direct_score_permission"])
            self.assertFalse(fact["flank_semantics_permission"])

    def test_top_level_binding_and_hash_chain_are_tamper_evident(self) -> None:
        genuine = validate_structural_relation_projections(
            self.bundle,
            self.resolution,
        )
        self.assertEqual(genuine.status, "PASS")

        rebinding = replace(
            self.resolution,
            source_application_bundle_hash="1" * 64,
        )
        report = validate_structural_relation_projections(self.bundle, rebinding)
        self.assertEqual(report.status, "FAIL")
        self.assertIn(
            "SOURCE_APPLICATION_BUNDLE_HASH_MISMATCH",
            report.diagnostics,
        )
        self.assertIn("BUNDLE_HASH_MISMATCH", report.diagnostics)

        tampered_hash = replace(self.resolution, bundle_hash="0" * 64)
        report = validate_structural_relation_projections(self.bundle, tampered_hash)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("BUNDLE_HASH_MISMATCH", report.diagnostics)

    def test_source_unavailable_has_dedicated_diagnostic(self) -> None:
        combined = {
            "combined_resolution": {
                "ziwei_bundle": None,
                "ziwei_error": {"detail": "fixture source unavailable"},
            }
        }
        with patch.object(self.app, "resolve_payload", return_value=combined):
            with self.assertRaises(LocalCombinedAppRequestError) as raised:
                self.app.resolve_ziwei_structural_relations_payload(
                    dict(self.payload)
                )
        self.assertEqual(
            raised.exception.code,
            "LOCAL_APP_ZIWEI_STRUCTURAL_RELATIONS_SOURCE_UNAVAILABLE",
        )
        self.assertEqual(raised.exception.status, 422)

    def test_full_replay_is_stable(self) -> None:
        replay = self.app.resolve_ziwei_structural_relations_payload(
            dict(self.payload)
        )
        self.assertEqual(replay, self.response)


class ZiweiStructuralRelationWorkbenchContractR1Tests(unittest.TestCase):
    def test_browser_consumes_backend_r6_r7_r8_without_recomputing_geometry(self) -> None:
        for expected in (
            "/api/ziwei-structural-relations",
            "ziwei_structural_relation_projections",
            "renderStructuralRelations",
            "qishu_facts",
            "one_six_facts",
            "adjacent_palace_pairs",
            "relative_ordinal",
            "clockwise_offset",
            "counterclockwise_address",
            "clockwise_address",
            "source_application_bundle_hash",
            "source_r2_fact_hash",
            "source_r2_computation_hash",
            "semantic_scope",
            "integrity",
            "不成立夹宫/夹格",
            "不作事件、端点、评分或吉凶判断",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, PALACE_STEM_TOPOLOGY_JS)

        for forbidden in (
            "QISHU_RELATIVE_ORDINAL",
            "QISHU_CLOCKWISE_OFFSET",
            "ONE_SIX_RELATIVE_ORDINAL",
            "CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL",
            "COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL",
            "flank_semantics_permission = true",
            "direct_event_permission = true",
            "direct_endpoint_permission = true",
            "direct_score_permission = true",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, PALACE_STEM_TOPOLOGY_JS)


if __name__ == "__main__":
    unittest.main()

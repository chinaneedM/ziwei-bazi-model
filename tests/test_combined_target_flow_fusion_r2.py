from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

import jsonschema

from fortune_training.bazi_application import bazi_local_application_v1_profile
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_temporal import bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.calendar_foundation.models import json_value
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedTargetFlowRequest,
    CombinedTargetFlowService,
    combined_chart_application_v1_profile,
)
from fortune_training.combined_chart_application.flow_fusion_r2 import (
    CombinedTargetFlowFusionR2Service,
    combined_target_flow_fusion_r2_bundle_hash,
    combined_target_flow_fusion_r2_source_fact_hash,
    combined_target_flow_fusion_r2_view_hash,
    validate_combined_target_flow_fusion_r2_full_replay,
    validate_combined_target_flow_fusion_r2_resolution,
)
from fortune_training.ziwei_application import (
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class CombinedTargetFlowFusionR2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.birth = BirthInput(
            reported_local_datetime=datetime(1994, 5, 17, 14, 30),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.combined_request = CombinedChartApplicationRequest(
            birth=cls.birth,
            sex="MALE",
            ziwei_calculation_profile=ziwei_chart_engine_v1_profile(registry),
            ziwei_application_profile=ziwei_application_v1_profile(),
            ziwei_presentation_profile=(
                ziwei_application_default_presentation_profile()
            ),
            bazi_natal_profile=bazi_foundation_v1_profile(registry),
            bazi_temporal_profile=bazi_temporal_v1_continuous_profile(),
            bazi_application_profile=bazi_local_application_v1_profile(),
            combined_profile=combined_chart_application_v1_profile(),
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )
        cls.target_profile = bazi_target_temporal_coordinate_r1_profile()
        cls.r1_service = CombinedTargetFlowService.from_repository(ROOT)
        cls.service = CombinedTargetFlowFusionR2Service.from_repository(ROOT)
        cls.schema = json.loads(
            (
                ROOT
                / "schemas"
                / "combined-target-flow-fusion-r2.schema.json"
            ).read_text(encoding="utf-8")
        )

    @staticmethod
    def _target(
        local: datetime,
        *,
        place: str = "Beijing",
        latitude: float = 39.9042,
        longitude: float = 116.4074,
        timezone_id: str = "Asia/Shanghai",
        uncertainty_seconds: int = 0,
    ) -> TargetTemporalInput:
        return TargetTemporalInput(
            reported_local_datetime=local,
            target_place=place,
            latitude=latitude,
            longitude=longitude,
            timezone_id=timezone_id,
            uncertainty_seconds=uncertainty_seconds,
        )

    @classmethod
    def _request(cls, target: TargetTemporalInput) -> CombinedTargetFlowRequest:
        return CombinedTargetFlowRequest(
            combined_request=cls.combined_request,
            target_input=target,
            target_coordinate_profile=cls.target_profile,
        )

    def test_exact_target_binds_both_system_target_projections(self) -> None:
        request = self._request(self._target(datetime(2026, 8, 18, 12, 0)))
        base, bazi_flow, r1, target, ziwei_selector, result = (
            self.service.resolve_with_bundles(request)
        )

        self.assertEqual("RESOLVED", target.status)
        self.assertEqual("RESOLVED", bazi_flow.status)
        self.assertEqual("RESOLVED", ziwei_selector.status)
        self.assertEqual(1, len(ziwei_selector.candidates))
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual("PASS", result.integrity.status)

        self.assertEqual(base.manifest_hash, result.base_combined_manifest_hash)
        self.assertEqual(r1.bundle_hash, result.r1_target_flow_bundle_hash)
        self.assertEqual(target.hashes.fact_hash, result.target_coordinate_fact_hash)
        self.assertEqual(
            target.hashes.computation_hash,
            result.target_coordinate_computation_hash,
        )
        self.assertEqual(
            bazi_flow.bundle_hash,
            result.bazi_target_flow_bundle_hash,
        )
        self.assertEqual(
            ziwei_selector.hashes.fact_hash,
            result.ziwei_selector_fact_hash,
        )
        self.assertEqual(
            ziwei_selector.hashes.computation_hash,
            result.ziwei_selector_computation_hash,
        )
        self.assertEqual(
            target.hashes.fact_hash,
            ziwei_selector.source_target_coordinate_fact_hash,
        )
        self.assertEqual(
            target.hashes.fact_hash,
            bazi_flow.target_coordinate_fact_hash,
        )
        jsonschema.Draft202012Validator(self.schema).validate(json_value(result))

        injected = copy.deepcopy(json_value(result))
        injected["prediction"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.schema).validate(injected)

    def test_r1_remains_byte_and_hash_stable_after_r2_projection(self) -> None:
        request = self._request(self._target(datetime(2026, 8, 18, 12, 0)))
        before = self.r1_service.resolve(request)
        self.service.resolve(request)
        after = self.r1_service.resolve(request)

        self.assertEqual(before, after)
        self.assertEqual(json_value(before), json_value(after))
        self.assertEqual(before.source_fact_hash, after.source_fact_hash)
        self.assertEqual(before.view_hash, after.view_hash)
        self.assertEqual(before.bundle_hash, after.bundle_hash)

    def test_dst_fold_preserves_uncertainty_on_both_sides(self) -> None:
        request = self._request(
            self._target(
                datetime(2026, 11, 1, 1, 30),
                place="New York",
                latitude=40.7128,
                longitude=-74.006,
                timezone_id="America/New_York",
            )
        )
        _, bazi_flow, _, target, ziwei_selector, result = (
            self.service.resolve_with_bundles(request)
        )

        self.assertEqual(
            "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY",
            target.status,
        )
        self.assertEqual("MULTI_CANDIDATE", bazi_flow.status)
        self.assertEqual("RESOLVED", ziwei_selector.status)
        self.assertGreaterEqual(len(ziwei_selector.candidates), 2)
        self.assertEqual("UNCERTAINTY_PRESENT", result.status)
        self.assertEqual("PASS", result.integrity.status)

    def test_local_rehash_cannot_hide_ziwei_binding_tamper_from_full_replay(self) -> None:
        request = self._request(self._target(datetime(2026, 8, 18, 12, 0)))
        result = self.service.resolve(request)

        rewritten = replace(result, ziwei_selector_fact_hash="0" * 64)
        rewritten = replace(
            rewritten,
            source_fact_hash=combined_target_flow_fusion_r2_source_fact_hash(
                rewritten
            ),
        )
        rewritten = replace(
            rewritten,
            view_hash=combined_target_flow_fusion_r2_view_hash(rewritten),
        )
        rewritten = replace(
            rewritten,
            bundle_hash=combined_target_flow_fusion_r2_bundle_hash(rewritten),
        )
        rewritten = replace(
            rewritten,
            integrity=validate_combined_target_flow_fusion_r2_resolution(rewritten),
        )

        self.assertEqual("PASS", rewritten.integrity.status)
        replay = validate_combined_target_flow_fusion_r2_full_replay(
            self.service,
            request,
            rewritten,
        )
        self.assertEqual("FAIL", replay.status)
        self.assertIn(
            "COMBINED_TARGET_FLOW_FUSION_R2_FULL_REPLAY_MISMATCH",
            replay.diagnostics,
        )

    def test_repeated_resolution_is_deterministic(self) -> None:
        request = self._request(self._target(datetime(2026, 8, 18, 12, 0)))
        first = self.service.resolve(request)
        second = self.service.resolve(request)

        self.assertEqual(first, second)
        self.assertEqual(first.source_fact_hash, second.source_fact_hash)
        self.assertEqual(first.view_hash, second.view_hash)
        self.assertEqual(first.bundle_hash, second.bundle_hash)


if __name__ == "__main__":
    unittest.main()

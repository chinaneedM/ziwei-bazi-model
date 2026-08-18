from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import jsonschema

from fortune_training.bazi_application import BaziApplicationResolutionError
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
    CombinedChartService,
    CombinedTargetFlowRequest,
    CombinedTargetFlowService,
    combined_chart_application_v1_profile,
    combined_target_flow_bundle_hash,
    combined_target_flow_source_fact_hash,
    combined_target_flow_view_hash,
    validate_combined_target_flow_full_replay,
    validate_combined_target_flow_resolution,
)
from fortune_training.ziwei_application import (
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import ziwei_chart_engine_v1_profile
from fortune_training.bazi_application import bazi_local_application_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class CombinedTargetFlowCompositionR1Tests(unittest.TestCase):
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
            ziwei_annual_year=2025,
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )
        cls.target_profile = bazi_target_temporal_coordinate_r1_profile()
        cls.service = CombinedTargetFlowService.from_repository(ROOT)
        cls.schema = json.loads(
            (
                ROOT
                / "schemas"
                / "combined-target-flow-composition-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

    @staticmethod
    def _target(
        local: datetime,
        *,
        place: str = "Greenwich",
        latitude: float = 51.4769,
        longitude: float = 0.0,
        timezone_id: str = "Etc/UTC",
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
    def _request(cls, target, *, combined_request=None):
        return CombinedTargetFlowRequest(
            combined_request=combined_request or cls.combined_request,
            target_input=target,
            target_coordinate_profile=cls.target_profile,
        )

    def test_ordinary_exact_target_is_deterministic_and_schema_valid(self) -> None:
        request = self._request(self._target(datetime(2026, 6, 1, 12, 0)))
        base1, flow1, result1 = self.service.resolve_with_bundles(request)
        base2, flow2, result2 = self.service.resolve_with_bundles(request)
        self.assertEqual("RESOLVED", result1.status)
        self.assertEqual("PASS", result1.integrity.status)
        self.assertEqual(base1, base2)
        self.assertEqual(flow1, flow2)
        self.assertEqual(result1, result2)
        self.assertEqual(base1.manifest_hash, result1.base_combined_manifest_hash)
        self.assertEqual(base1.ziwei_bundle.bundle_hash, result1.ziwei_bundle_hash)
        self.assertEqual(base1.bazi_bundle.bundle_hash, result1.bazi_base_bundle_hash)
        self.assertEqual(flow1.bundle_hash, result1.bazi_target_flow_bundle_hash)
        jsonschema.Draft202012Validator(self.schema).validate(json_value(result1))

        injected = copy.deepcopy(json_value(result1))
        injected["prediction"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.schema).validate(injected)

    def test_existing_combined_v1_is_byte_and_hash_stable(self) -> None:
        base_service = CombinedChartService.from_repository(ROOT)
        before = base_service.resolve(self.combined_request)
        self.service.resolve(
            self._request(self._target(datetime(2026, 6, 1, 12, 0)))
        )
        after = base_service.resolve(self.combined_request)
        self.assertEqual(before, after)
        self.assertEqual(json_value(before), json_value(after))
        self.assertEqual(before.manifest_hash, after.manifest_hash)
        self.assertEqual(
            before.ziwei_bundle.bundle_hash,
            after.ziwei_bundle.bundle_hash,
        )
        self.assertEqual(
            before.bazi_bundle.bundle_hash,
            after.bazi_bundle.bundle_hash,
        )

    def test_different_target_longitude_keeps_ziwei_identity_independent(self) -> None:
        local = datetime(2026, 6, 1, 0, 30)
        left_base, left_flow, left = self.service.resolve_with_bundles(
            self._request(
                self._target(
                    local,
                    place="UTC meridian",
                    latitude=0.0,
                    longitude=0.0,
                )
            )
        )
        right_base, right_flow, right = self.service.resolve_with_bundles(
            self._request(
                self._target(
                    local,
                    place="East longitude",
                    latitude=0.0,
                    longitude=120.0,
                )
            )
        )
        self.assertEqual(
            left_base.ziwei_bundle.bundle_hash,
            right_base.ziwei_bundle.bundle_hash,
        )
        self.assertEqual(left.ziwei_bundle_hash, right.ziwei_bundle_hash)
        self.assertNotEqual(left_flow.bundle_hash, right_flow.bundle_hash)
        self.assertNotEqual(left.bundle_hash, right.bundle_hash)

    def test_explicit_ziwei_annual_change_does_not_mutate_bazi_target_flow(self) -> None:
        target = self._target(datetime(2026, 6, 1, 12, 0))
        request_2025 = self._request(target)
        request_2026 = self._request(
            target,
            combined_request=replace(self.combined_request, ziwei_annual_year=2026),
        )
        base_2025, flow_2025, result_2025 = self.service.resolve_with_bundles(
            request_2025
        )
        base_2026, flow_2026, result_2026 = self.service.resolve_with_bundles(
            request_2026
        )
        self.assertNotEqual(
            base_2025.ziwei_bundle.bundle_hash,
            base_2026.ziwei_bundle.bundle_hash,
        )
        self.assertEqual(flow_2025.bundle_hash, flow_2026.bundle_hash)
        self.assertEqual(
            result_2025.bazi_target_flow_bundle_hash,
            result_2026.bazi_target_flow_bundle_hash,
        )
        self.assertNotEqual(result_2025.bundle_hash, result_2026.bundle_hash)

    def test_target_year_does_not_override_explicit_ziwei_annual_year(self) -> None:
        target = self._target(datetime(2026, 8, 18, 12, 0))
        base, flow, result = self.service.resolve_with_bundles(self._request(target))
        self.assertEqual(2025, base.ziwei_bundle.selected_annual_year)
        self.assertEqual(2025, result.ziwei_selected_annual_year)
        self.assertEqual(
            "2026-08-18T12:00:00",
            json_value(flow.target_input)["reported_local_datetime"],
        )

    def test_dst_fold_is_preserved_as_bazi_target_flow_uncertainty(self) -> None:
        target = self._target(
            datetime(2026, 11, 1, 1, 30),
            place="New York",
            latitude=40.7128,
            longitude=-74.006,
            timezone_id="America/New_York",
        )
        _, flow, result = self.service.resolve_with_bundles(self._request(target))
        self.assertEqual("MULTI_CANDIDATE", flow.status)
        self.assertEqual("UNCERTAINTY_PRESENT", result.status)
        self.assertEqual(flow.bundle_hash, result.bazi_target_flow_bundle_hash)

    def test_dst_gap_fails_closed_with_bazi_provenance(self) -> None:
        target = self._target(
            datetime(2026, 3, 8, 2, 30),
            place="New York",
            latitude=40.7128,
            longitude=-74.006,
            timezone_id="America/New_York",
        )
        with self.assertRaises(BaziApplicationResolutionError) as error:
            self.service.resolve(self._request(target))
        self.assertEqual(
            "BAZI_APP_FLOW_TARGET_RESOLUTION_FAILED",
            error.exception.code,
        )

    def test_structural_tamper_and_full_replay_are_independent_gates(self) -> None:
        request = self._request(self._target(datetime(2026, 6, 1, 12, 0)))
        base, flow, result = self.service.resolve_with_bundles(request)
        structural = validate_combined_target_flow_resolution(result)
        self.assertEqual("PASS", structural.status)
        full = validate_combined_target_flow_full_replay(
            self.service, request, base, flow, result
        )
        self.assertEqual("PASS", full.status)

        rewritten = replace(result, ziwei_selected_annual_year=2026)
        rewritten = replace(
            rewritten,
            source_fact_hash=combined_target_flow_source_fact_hash(rewritten),
        )
        rewritten = replace(
            rewritten,
            view_hash=combined_target_flow_view_hash(rewritten),
        )
        rewritten = replace(
            rewritten,
            bundle_hash=combined_target_flow_bundle_hash(rewritten),
        )
        self.assertEqual(
            "PASS",
            validate_combined_target_flow_resolution(rewritten).status,
        )
        replay = validate_combined_target_flow_full_replay(
            self.service, request, base, flow, rewritten
        )
        self.assertEqual("FAIL", replay.status)
        self.assertIn(
            "COMBINED_TARGET_FLOW_FULL_REPLAY_MISMATCH",
            replay.diagnostics,
        )

    def test_bazi_base_object_mismatch_fails_closed(self) -> None:
        request = self._request(self._target(datetime(2026, 6, 1, 12, 0)))
        base = self.service.base_service.resolve(self.combined_request)
        real = self.service.bazi_flow_service.resolve_with_base

        def mismatched(flow_request):
            bazi_base, bazi_flow = real(flow_request)
            return replace(bazi_base, bundle_hash="0" * 64), bazi_flow

        with patch.object(
            self.service.bazi_flow_service,
            "resolve_with_base",
            side_effect=mismatched,
        ):
            with self.assertRaises(ValueError) as error:
                self.service.resolve(request)
        self.assertIn(
            "combined=",
            str(error.exception),
        )
        self.assertEqual(
            base.bazi_bundle.bundle_hash,
            self.service.base_service.resolve(self.combined_request).bazi_bundle.bundle_hash,
        )


if __name__ == "__main__":
    unittest.main()

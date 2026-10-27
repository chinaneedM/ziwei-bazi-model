from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path

import jsonschema

from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_temporal_shensha_sidecar import (
    BaziTemporalShenshaSidecarService,
    TemporalShenshaSidecarResolutionError,
    bound_source_application_candidates,
)
from fortune_training.combined_chart_application.flow_local_app import (
    FlowLocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.flow_models import (
    CombinedTargetFlowRequest,
)
from fortune_training.combined_chart_application.local_app import (
    LocalCombinedAppRequestError,
)


ROOT = Path(__file__).resolve().parents[1]


class BaziTemporalShenshaSidecarHardeningR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = FlowLocalCombinedChartApplication(ROOT)
        cls.response_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "combined-local-target-flow-response-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

    @staticmethod
    def payload() -> dict[str, object]:
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
            "target_datetime": "2026-06-01T12:00:00",
            "target_place": "Greenwich",
            "target_latitude": 51.4769,
            "target_longitude": 0.0,
            "target_timezone_id": "Etc/UTC",
            "target_precision": "EXACT_SECOND",
            "target_uncertainty_seconds": 0,
            "target_temporal_profile_id": (
                "BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1"
            ),
        }

    @classmethod
    def upstream(cls):
        payload = cls.payload()
        combined_request, _ = cls.app._combined_request_from_payload(payload)
        target_input = TargetTemporalInput(
            reported_local_datetime=cls.app._target_datetime(payload),
            target_place=str(payload["target_place"]),
            latitude=float(payload["target_latitude"]),
            longitude=float(payload["target_longitude"]),
            timezone_id=str(payload["target_timezone_id"]),
            uncertainty_seconds=int(payload["target_uncertainty_seconds"]),
        )
        request = CombinedTargetFlowRequest(
            combined_request=combined_request,
            target_input=target_input,
            target_coordinate_profile=bazi_target_temporal_coordinate_r1_profile(),
        )
        base, flow, _ = cls.app.flow_service.resolve_with_bundles(request)
        if base.bazi_bundle is None:
            raise RuntimeError("fixture requires Bazi application bundle")
        return base.bazi_bundle, flow

    def test_source_application_id_must_match_natal_temporal_coordinate(self) -> None:
        base, flow = self.upstream()
        source = base.candidates[0]
        wrong = replace(
            source,
            candidate_id=source.candidate_id + ":WRONG-LINEAGE",
            temporal_candidate_index=source.temporal_candidate_index + 1,
        )
        tampered_flow = replace(
            flow.candidates[0],
            source_application_candidate_ids=(wrong.candidate_id,),
        )
        with self.assertRaises(TemporalShenshaSidecarResolutionError) as caught:
            bound_source_application_candidates(
                (source, wrong),
                tampered_flow,
            )
        self.assertEqual(
            "BAZI_TEMPORAL_SHENSHA_SOURCE_LINEAGE_COORDINATE_MISMATCH",
            caught.exception.code,
        )

    def test_api_requires_sidecar_full_replay_before_return(self) -> None:
        class ReplayDivergentService(BaziTemporalShenshaSidecarService):
            def __init__(self) -> None:
                super().__init__()
                self.once_calls = 0

            def _resolve_once(self, base_application, bazi_target_flow):
                result = super()._resolve_once(base_application, bazi_target_flow)
                self.once_calls += 1
                if self.once_calls % 2 == 0:
                    return replace(result, bundle_hash="0" * 64)
                return result

        original = self.app.temporal_shensha_sidecar_service
        divergent = ReplayDivergentService()
        self.app.temporal_shensha_sidecar_service = divergent
        try:
            with self.assertRaises(LocalCombinedAppRequestError) as caught:
                self.app.resolve_flow_payload(self.payload())
        finally:
            self.app.temporal_shensha_sidecar_service = original
        self.assertEqual(
            "BAZI_TEMPORAL_SHENSHA_FULL_REPLAY_FAILED",
            caught.exception.code,
        )
        self.assertGreaterEqual(divergent.once_calls, 2)

    def test_dst_fold_preserves_exact_two_sidecar_candidates(self) -> None:
        payload = self.payload()
        payload.update(
            {
                "target_datetime": "2026-11-01T01:30:00",
                "target_place": "New York",
                "target_latitude": 40.7128,
                "target_longitude": -74.006,
                "target_timezone_id": "America/New_York",
            }
        )
        response = self.app.resolve_flow_payload(payload)
        flow = response["bazi_target_flow_bundle"]
        sidecar = response["bazi_temporal_shensha_projection_bundle"]
        self.assertEqual("MULTI_CANDIDATE", flow["status"])
        self.assertEqual("MULTI_CANDIDATE", sidecar["status"])
        self.assertEqual(2, len(flow["candidates"]))
        self.assertEqual(2, len(sidecar["candidates"]))
        self.assertEqual(
            [row["candidate_id"] for row in flow["candidates"]],
            [
                row["source_bazi_target_flow_candidate_id"]
                for row in sidecar["candidates"]
            ],
        )
        self.assertEqual(
            [row["target_coordinate_candidate_id"] for row in flow["candidates"]],
            [row["target_coordinate_candidate_id"] for row in sidecar["candidates"]],
        )

    def test_pre_dayun_remains_explicit_no_ganzhi_projection(self) -> None:
        payload = self.payload()
        payload.update(
            {
                "target_datetime": "1994-05-18T12:00:00",
                "target_place": "Beijing",
                "target_latitude": 39.9042,
                "target_longitude": 116.4074,
                "target_timezone_id": "Asia/Shanghai",
            }
        )
        response = self.app.resolve_flow_payload(payload)
        sidecar = response["bazi_temporal_shensha_projection_bundle"]
        self.assertGreaterEqual(len(sidecar["candidates"]), 1)
        for candidate in sidecar["candidates"]:
            slot = candidate["projection"]["dayun"]
            self.assertEqual("PRE_DAYUN_NO_GANZHI_PROJECTION", slot["status"])
            self.assertIsNone(slot["ganzhi"])
            self.assertEqual([], slot["matches"])

    def test_wrapper_schema_rejects_sidecar_top_level_injection(self) -> None:
        response = self.app.resolve_flow_payload(self.payload())
        jsonschema.Draft202012Validator(self.response_schema).validate(response)
        injected = copy.deepcopy(response)
        injected["bazi_temporal_shensha_projection_bundle"]["prediction"] = (
            "FORBIDDEN"
        )
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.response_schema).validate(injected)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

import jsonschema

from fortune_training.bazi_application import (
    BaziApplicationFlowRequest,
    BaziApplicationFlowService,
    BaziApplicationRequest,
    BaziChartService,
    bazi_local_application_v1_profile,
    validate_application_flow_full_replay,
    validate_application_flow_resolution,
)
from fortune_training.bazi_application.flow_local_app import (
    FLOW_LOCAL_APP_HEALTH_SCHEMA,
    FLOW_LOCAL_APP_ID,
    FLOW_LOCAL_APP_RESOLVE_SCHEMA,
    FLOW_LOCAL_APP_VERSION,
    FlowLocalBaziApplication,
)
from fortune_training.bazi_application.local_app import (
    LOCAL_APP_HEALTH_SCHEMA,
    LOCAL_APP_ID,
    LOCAL_APP_VERSION,
    LocalBaziApplication,
)
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziApplicationFlowLocalContractR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_service = BaziChartService.from_repository(ROOT)
        cls.flow_service = BaziApplicationFlowService(cls.base_service)
        registry = cls.base_service.chart_foundation.time_calendar.policy_registry
        cls.base_request = BaziApplicationRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(2025, 2, 7, 10, 10),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex=BaziSex.MALE,
            natal_profile=bazi_foundation_v1_profile(registry),
            temporal_profile=bazi_temporal_v1_continuous_profile(),
            application_profile=bazi_local_application_v1_profile(),
            dayun_count=6,
        )
        cls.target_input = TargetTemporalInput(
            reported_local_datetime=datetime(2026, 6, 1, 12, 0),
            target_place="Greenwich",
            latitude=51.4769,
            longitude=0.0,
            timezone_id="Etc/UTC",
        )
        cls.flow_request = BaziApplicationFlowRequest(
            application_request=cls.base_request,
            target_input=cls.target_input,
            target_coordinate_profile=bazi_target_temporal_coordinate_r1_profile(),
        )
        cls.bundle_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "bazi-application-flow-integration-r1.schema.json"
            ).read_text(encoding="utf-8")
        )
        cls.local_response_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "bazi-local-application-flow-response-r1.schema.json"
            ).read_text(encoding="utf-8")
        )
        cls.local_health_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "bazi-local-application-flow-health-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

    @staticmethod
    def _local_payload() -> dict[str, object]:
        return {
            "birth_datetime": "2025-02-07T10:10:00",
            "birth_place": "Beijing",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone_id": "Asia/Shanghai",
            "sex": "MALE",
            "precision": "EXACT_SECOND",
            "uncertainty_seconds": 0,
            "natal_profile_id": "BAZI-FOUNDATION-V1-R1",
            "temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "application_profile_id": "BAZI-LOCAL-APPLICATION-V1-R1",
            "dayun_count": 6,
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

    def test_flow_health_has_independent_closed_schema_without_mutating_legacy_health(self) -> None:
        legacy = LocalBaziApplication(ROOT).health()
        self.assertEqual(
            {
                "schema": LOCAL_APP_HEALTH_SCHEMA,
                "status": "ok",
                "application_id": LOCAL_APP_ID,
                "application_version": LOCAL_APP_VERSION,
                "bind_policy": "LOOPBACK_ONLY",
            },
            legacy,
        )

        flow_health = FlowLocalBaziApplication(ROOT).health()
        self.assertEqual(FLOW_LOCAL_APP_HEALTH_SCHEMA, flow_health["schema"])
        self.assertEqual(FLOW_LOCAL_APP_ID, flow_health["application_id"])
        self.assertEqual(FLOW_LOCAL_APP_VERSION, flow_health["application_version"])
        jsonschema.Draft202012Validator(self.local_health_schema).validate(flow_health)

        injected = dict(flow_health)
        injected["prediction"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.local_health_schema).validate(injected)

    def test_local_flow_response_wrapper_and_nested_bundle_validate_independently(self) -> None:
        response = FlowLocalBaziApplication(ROOT).resolve_flow_payload(
            self._local_payload()
        )
        self.assertEqual(FLOW_LOCAL_APP_RESOLVE_SCHEMA, response["schema"])
        jsonschema.Draft202012Validator(self.local_response_schema).validate(response)
        jsonschema.Draft202012Validator(self.bundle_schema).validate(
            response["target_flow_bundle"]
        )

        injected = dict(response)
        injected["interpretation"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.local_response_schema).validate(injected)

    def test_full_replay_detects_rewritten_metadata_even_when_structural_hashes_still_pass(self) -> None:
        resolution = self.flow_service.resolve(self.flow_request)
        structural = validate_application_flow_resolution(resolution)
        self.assertEqual("PASS", structural.status)
        full = validate_application_flow_full_replay(
            self.flow_service, self.flow_request, resolution
        )
        self.assertEqual("PASS", full.status)

        rewritten = replace(
            resolution,
            events=(*resolution.events, "SYNTHETIC_REWRITTEN_EVENT"),
        )
        rewritten_structural = validate_application_flow_resolution(rewritten)
        self.assertEqual("PASS", rewritten_structural.status)
        rewritten_full = validate_application_flow_full_replay(
            self.flow_service, self.flow_request, rewritten
        )
        self.assertEqual("FAIL", rewritten_full.status)
        self.assertEqual(("FULL_REPLAY_MISMATCH",), rewritten_full.diagnostics)


if __name__ == "__main__":
    unittest.main()

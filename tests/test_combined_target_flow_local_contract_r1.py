from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

from fortune_training.combined_chart_application.flow_local_app import (
    FLOW_LOCAL_APP_HEALTH_SCHEMA,
    FLOW_LOCAL_APP_ID,
    FLOW_LOCAL_APP_RESOLVE_SCHEMA,
    FLOW_LOCAL_APP_VERSION,
    FlowLocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.local_app import (
    LOCAL_APP_HEALTH_SCHEMA,
    LOCAL_APP_ID,
    LOCAL_APP_VERSION,
    LocalCombinedAppRequestError,
    LocalCombinedChartApplication,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedTargetFlowLocalContractR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = FlowLocalCombinedChartApplication(ROOT)
        cls.base_app = LocalCombinedChartApplication(ROOT)
        cls.flow_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "combined-target-flow-composition-r1.schema.json"
            ).read_text(encoding="utf-8")
        )
        cls.response_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "combined-local-target-flow-response-r1.schema.json"
            ).read_text(encoding="utf-8")
        )
        cls.health_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "combined-local-target-flow-health-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

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
            "ziwei_daxian_frame_id": None,
            "ziwei_annual_year": 2025,
            "ziwei_minor_limit_age": None,
            "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "bazi_dayun_count": 12,
            "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
        }

    @classmethod
    def flow_payload(cls) -> dict[str, object]:
        return {
            **cls.base_payload(),
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

    def test_flow_health_is_independent_and_legacy_health_is_unchanged(self) -> None:
        legacy = self.base_app.health()
        self.assertEqual(LOCAL_APP_HEALTH_SCHEMA, legacy["schema"])
        self.assertEqual(LOCAL_APP_ID, legacy["application_id"])
        self.assertEqual(LOCAL_APP_VERSION, legacy["application_version"])
        self.assertNotIn("target_flow_endpoint", legacy)

        flow = self.app.health()
        self.assertEqual(FLOW_LOCAL_APP_HEALTH_SCHEMA, flow["schema"])
        self.assertEqual(FLOW_LOCAL_APP_ID, flow["application_id"])
        self.assertEqual(FLOW_LOCAL_APP_VERSION, flow["application_version"])
        jsonschema.Draft202012Validator(self.health_schema).validate(flow)

        injected = dict(flow)
        injected["prediction"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.health_schema).validate(injected)

    def test_flow_response_validates_wrapper_and_binding_schemas(self) -> None:
        response = self.app.resolve_flow_payload(self.flow_payload())
        self.assertEqual(FLOW_LOCAL_APP_RESOLVE_SCHEMA, response["schema"])
        jsonschema.Draft202012Validator(self.response_schema).validate(response)
        jsonschema.Draft202012Validator(self.flow_schema).validate(
            response["combined_target_flow_resolution"]
        )
        self.assertEqual(
            response["combined_resolution"]["bazi_bundle"]["bundle_hash"],
            response["bazi_target_flow_bundle"]["base_application_bundle_hash"],
        )
        self.assertEqual(
            response["combined_resolution"]["manifest_hash"],
            response["combined_target_flow_resolution"][
                "base_combined_manifest_hash"
            ],
        )

        injected = copy.deepcopy(response)
        injected["synthesis"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.response_schema).validate(injected)

    def test_flow_server_legacy_resolve_payload_is_exactly_legacy_application(self) -> None:
        payload = self.base_payload()
        legacy = self.base_app.resolve_payload(dict(payload))
        delegated = self.app.resolve_payload(dict(payload))
        self.assertEqual(legacy, delegated)

    def test_invalid_target_timezone_and_profile_fail_at_additive_boundary(self) -> None:
        wrong_zone = self.flow_payload()
        wrong_zone["target_timezone_id"] = "Mars/Olympus"
        with self.assertRaises(LocalCombinedAppRequestError) as zone_error:
            self.app.resolve_flow_payload(wrong_zone)
        self.assertEqual(
            "LOCAL_APP_INVALID_TARGET_TIMEZONE",
            zone_error.exception.code,
        )

        wrong_profile = self.flow_payload()
        wrong_profile["target_temporal_profile_id"] = "IMPLICIT-DEFAULT"
        with self.assertRaises(LocalCombinedAppRequestError) as profile_error:
            self.app.resolve_flow_payload(wrong_profile)
        self.assertEqual(
            "LOCAL_APP_UNSUPPORTED_TARGET_TEMPORAL_PROFILE",
            profile_error.exception.code,
        )

    def test_target_year_does_not_silently_rewrite_explicit_ziwei_year(self) -> None:
        payload = self.flow_payload()
        payload["ziwei_annual_year"] = 2025
        payload["target_datetime"] = "2026-08-18T12:00:00"
        response = self.app.resolve_flow_payload(payload)
        binding = response["combined_target_flow_resolution"]
        self.assertEqual(2025, binding["ziwei_selected_annual_year"])
        self.assertEqual(
            "2026-08-18T12:00:00",
            binding["target_input"]["reported_local_datetime"],
        )


if __name__ == "__main__":
    unittest.main()

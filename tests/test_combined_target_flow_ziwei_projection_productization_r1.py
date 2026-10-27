from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import jsonschema

from fortune_training.combined_chart_application.flow_local_app import (
    FlowLocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.local_app import (
    LocalCombinedAppRequestError,
)
from fortune_training.combined_chart_application.shared_time_models import (
    SharedZiweiSelectorProjectionIntegrityReport,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedTargetFlowZiweiProjectionProductizationR1Tests(unittest.TestCase):
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
        cls.projection_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "shared-ziwei-selector-projection-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

    @staticmethod
    def payload(
        *,
        target_datetime: str = "2026-06-01T12:00:00",
        target_place: str = "Greenwich",
        target_latitude: float = 51.4769,
        target_longitude: float = 0.0,
        target_timezone_id: str = "Etc/UTC",
    ) -> dict[str, object]:
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

    def test_unified_flow_exposes_strict_shared_ziwei_projection(self) -> None:
        response = self.app.resolve_flow_payload(self.payload())
        jsonschema.Draft202012Validator(self.response_schema).validate(response)

        projection = response["shared_ziwei_selector_projection"]
        jsonschema.Draft202012Validator(self.projection_schema).validate(projection)
        self.assertEqual("RESOLVED", projection["status"])
        self.assertEqual("PASS", projection["integrity"]["status"])

        ziwei_bundle = response["combined_resolution"]["ziwei_bundle"]
        bazi_flow = response["bazi_target_flow_bundle"]
        combined_flow = response["combined_target_flow_resolution"]
        self.assertEqual(
            ziwei_bundle["bundle_hash"],
            projection["source_ziwei_application_bundle_hash"],
        )
        self.assertEqual(
            bazi_flow["target_coordinate_fact_hash"],
            projection["source_target_coordinate_fact_hash"],
        )
        self.assertEqual(
            bazi_flow["target_coordinate_computation_hash"],
            projection["source_target_coordinate_computation_hash"],
        )
        self.assertEqual(
            combined_flow["target_coordinate_fact_hash"],
            projection["source_target_coordinate_fact_hash"],
        )
        self.assertEqual(
            combined_flow["target_coordinate_computation_hash"],
            projection["source_target_coordinate_computation_hash"],
        )

        projection_target_ids = {
            row["source_target_candidate_id"] for row in projection["candidates"]
        }
        flow_target_ids = {
            row["view"]["target"]["target_coordinate_candidate_id"]
            for row in bazi_flow["candidates"]
        }
        self.assertEqual(flow_target_ids, projection_target_ids)

        for row in projection["candidates"]:
            self.assertEqual(
                "REGULAR_LUNAR_DAY_RESOLVED",
                row["daily_projection_status"],
            )
            self.assertEqual(
                "S10-FLOW-MONTH-FIRST-DAY-FORWARD-R1",
                row["daily_rule_id"],
            )
            self.assertIn("S10:ZZTERM-P-0274", row["daily_source_refs"])
            self.assertEqual(
                "CANDIDATES_PRESERVED_NO_SELECTED_FRAME",
                row["hourly_projection_status"],
            )
            self.assertEqual(2, len(row["hourly_method_candidates"]))
            self.assertEqual(
                {
                    "ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME",
                    "LOCAL_APPARENT_SOLAR_TIME",
                },
                {
                    candidate["time_standard"]
                    for candidate in row["hourly_method_candidates"]
                },
            )
            self.assertEqual(
                {"CASE_METHOD_ONLY_NOT_GLOBAL_RULE"},
                {
                    candidate["authority_status"]
                    for candidate in row["hourly_method_candidates"]
                },
            )
            self.assertNotIn("selected_hourly_candidate_id", row)

    def test_unified_response_schema_rejects_projection_prediction_injection(self) -> None:
        response = self.app.resolve_flow_payload(self.payload())
        injected = copy.deepcopy(response)
        injected["shared_ziwei_selector_projection"]["prediction"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.response_schema).validate(injected)

    def test_unified_flow_fails_closed_when_shared_ziwei_full_replay_fails(self) -> None:
        failed = SharedZiweiSelectorProjectionIntegrityReport(
            status="FAIL",
            diagnostics=("FORCED_FULL_REPLAY_FAILURE",),
        )
        with patch(
            "fortune_training.combined_chart_application.flow_local_app."
            "validate_shared_ziwei_selector_full_replay",
            return_value=failed,
        ):
            with self.assertRaises(LocalCombinedAppRequestError) as caught:
                self.app.resolve_flow_payload(self.payload())
        self.assertEqual(
            "LOCAL_APP_SHARED_ZIWEI_FULL_REPLAY_FAILED",
            caught.exception.code,
        )
        self.assertIn("FORCED_FULL_REPLAY_FAILURE", caught.exception.detail)

    def test_dst_fold_preserves_same_target_candidates_across_bazi_and_ziwei(self) -> None:
        response = self.app.resolve_flow_payload(
            self.payload(
                target_datetime="2026-11-01T01:30:00",
                target_place="New York",
                target_latitude=40.7128,
                target_longitude=-74.006,
                target_timezone_id="America/New_York",
            )
        )
        bazi_flow = response["bazi_target_flow_bundle"]
        projection = response["shared_ziwei_selector_projection"]
        self.assertEqual("MULTI_CANDIDATE", bazi_flow["status"])
        self.assertEqual(2, len(projection["candidates"]))
        self.assertEqual(
            {0, 1},
            {row["source_target_candidate_index"] for row in projection["candidates"]},
        )
        self.assertEqual(
            {
                row["view"]["target"]["target_coordinate_candidate_id"]
                for row in bazi_flow["candidates"]
            },
            {
                row["source_target_candidate_id"]
                for row in projection["candidates"]
            },
        )
        self.assertTrue(
            all(
                row["hourly_projection_status"]
                == "CANDIDATES_PRESERVED_NO_SELECTED_FRAME"
                for row in projection["candidates"]
            )
        )


if __name__ == "__main__":
    unittest.main()

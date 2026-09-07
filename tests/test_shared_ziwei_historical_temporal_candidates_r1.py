from __future__ import annotations

import copy
import json
import unittest
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from fortune_training.bazi_target_temporal import (
    TargetTemporalCoordinateFoundation,
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.calendar_foundation.models import json_value
from fortune_training.combined_chart_application.shared_time_service import (
    SharedZiweiSelectorProjectionService,
)
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    ZiweiChartService,
    ziwei_application_default_presentation_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class SharedZiweiHistoricalTemporalCandidatesR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        calculation_profile = ziwei_chart_engine_v1_profile(registry)
        application = ZiweiChartService.from_repository(ROOT)
        birth = BirthInput(
            reported_local_datetime=datetime(1994, 5, 17, 14, 30),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.ziwei_bundle = application.resolve(
            ApplicationBirthRequest(
                birth=birth,
                sex=Sex.MALE,
                calculation_profile=calculation_profile,
                presentation_profile=ziwei_application_default_presentation_profile(),
                daxian_count=12,
                max_nominal_age=120,
            )
        )
        cls.target_foundation = TargetTemporalCoordinateFoundation()
        cls.target_profile = bazi_target_temporal_coordinate_r1_profile()
        cls.service = SharedZiweiSelectorProjectionService()
        cls.schema = json.loads(
            (ROOT / "schemas" / "shared-ziwei-selector-projection-r1.schema.json").read_text(
                encoding="utf-8"
            )
        )

    @classmethod
    def _project(cls, wall: datetime):
        target = cls.target_foundation.resolve(
            TargetTemporalInput(
                reported_local_datetime=wall,
                target_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            cls.target_profile,
        )
        return cls.service.project(cls.ziwei_bundle, target, cls.target_profile)

    def test_regular_month_preserves_fixed_branch_and_jielan_families_separately(self) -> None:
        result = self._project(datetime(2026, 11, 15, 13, 15))
        row = result.candidates[0]
        self.assertEqual(2, len(row.hourly_method_candidates))
        self.assertTrue(all(
            item.active_address_branch == item.hour_branch
            for item in row.hourly_method_candidates
        ))
        self.assertEqual(
            "CANDIDATES_PRESERVED_NO_SELECTED_FRAME",
            row.historical_hourly_projection_status,
        )
        self.assertEqual(2, len(row.historical_hourly_method_candidates))
        self.assertEqual(
            {"ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME", "LOCAL_APPARENT_SOLAR_TIME"},
            {item["time_standard"] for item in row.historical_hourly_method_candidates},
        )
        self.assertTrue(all(
            item["method_id"] == "JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1"
            for item in row.historical_hourly_method_candidates
        ))
        self.assertTrue(all(
            item["selection_status"] == "PRESERVED_NOT_SELECTED"
            for item in row.historical_hourly_method_candidates
        ))
        self.assertTrue(all(
            item["parent_daily_effective_gregorian_date"]
            == item["effective_gregorian_date"]
            for item in row.historical_hourly_method_candidates
        ))
        self.assertEqual("NOT_APPLICABLE_REGULAR_MONTH", row.leap_month_candidate_status)
        self.assertEqual((), row.leap_month_method_candidates)
        Draft202012Validator(self.schema).validate(json_value(result))

    def test_leap_month_exposes_school_candidate_without_fabricating_regular_frame(self) -> None:
        result = self._project(datetime(2025, 8, 1, 12, 0))
        row = result.candidates[0]
        self.assertTrue(row.effective_lunar_is_leap_month)
        self.assertEqual("LEAP_MONTH_UNRESOLVED_NO_FRAME", row.monthly_projection_status)
        self.assertEqual("PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME", row.daily_projection_status)
        self.assertIsNone(row.monthly_frame_id)
        self.assertIsNone(row.daily_frame_id)
        self.assertEqual("CANDIDATE_PRESERVED_NO_SELECTION", row.leap_month_candidate_status)
        self.assertEqual(1, len(row.leap_month_method_candidates))
        candidate = row.leap_month_method_candidates[0]
        self.assertEqual("ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1", candidate["method_id"])
        self.assertEqual("PRESERVED_NOT_SELECTED", candidate["selection_status"])
        self.assertFalse(candidate["flow_day_continuity"]["half_split_reset"])
        self.assertFalse(candidate["flow_day_continuity"]["daily_active_address_emitted"])
        self.assertEqual(
            "NOT_CLOSED_BY_THIS_MONTH_POLICY_API",
            candidate["flow_day_continuity"]["daily_origin_semantics"],
        )
        self.assertEqual(
            "NO_SOURCE_SCOPED_PARENT_DAILY_FRAME",
            row.historical_hourly_projection_status,
        )
        self.assertEqual((), row.historical_hourly_method_candidates)
        Draft202012Validator(self.schema).validate(json_value(result))

    def test_nested_historical_candidate_schema_rejects_prediction_injection(self) -> None:
        result = self._project(datetime(2026, 11, 15, 13, 15))
        payload = copy.deepcopy(json_value(result))
        payload["candidates"][0]["historical_hourly_method_candidates"][0]["prediction"] = "FORBIDDEN"
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.schema).validate(payload)


if __name__ == "__main__":
    unittest.main()

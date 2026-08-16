from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import (
    BaziPolicySelection,
    BirthInput,
    TimeCalendarFoundation,
    TimePrecision,
)


ROOT = Path(__file__).resolve().parents[1]


class TimeCalendarApproximateSamplingR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.foundation = TimeCalendarFoundation.from_repository(ROOT)
        cls.registry = cls.foundation.policy_registry

    @staticmethod
    def beijing(
        *,
        precision: TimePrecision,
        uncertainty_seconds: int,
        local: datetime = datetime(1994, 5, 17, 23, 11),
    ) -> BirthInput:
        return BirthInput(
            reported_local_datetime=local,
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
            precision=precision,
            uncertainty_seconds=uncertainty_seconds,
        )

    def test_approximate_range_resolves_through_shared_combined_path(self):
        request = self.beijing(
            precision=TimePrecision.APPROXIMATE,
            uncertainty_seconds=120,
        )

        result = self.foundation.resolve(request)

        self.assertEqual("APPROXIMATE", result["input"]["precision"])
        self.assertEqual(120, result["input"]["uncertainty_seconds"])
        self.assertEqual(120, result["input_interval"]["uncertainty_seconds_each_side"])
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", result["status"])
        self.assertGreater(result["classification_count"], 1)
        self.assertGreater(len(result["branches"]), 1)

    def test_approximate_range_preserves_bazi_boundary_candidates(self):
        request = self.beijing(
            precision=TimePrecision.APPROXIMATE,
            uncertainty_seconds=120,
        )
        defaults = self.registry.default_bazi_selection()
        selection = BaziPolicySelection(
            bazi_day_boundary_policy="ZI_START_23",
            bazi_late_zi_hour_stem_policy="ZI_START_ROLLOVER",
            bazi_year_boundary_policy=defaults.bazi_year_boundary_policy,
            civil_ambiguous_time_policy=defaults.civil_ambiguous_time_policy,
        )

        result = self.foundation.resolve_bazi(request, selection)

        self.assertEqual("APPROXIMATE", result["input"]["precision"])
        self.assertEqual(120, result["input"]["uncertainty_seconds"])
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", result["status"])
        self.assertEqual(2, result["classification_count"])
        pillars = {
            tuple(
                branch["bazi_time"][key]
                for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")
            )
            for branch in result["branches"]
        }
        self.assertEqual(
            {
                ("甲戌", "己巳", "癸卯", "癸亥"),
                ("甲戌", "己巳", "甲辰", "甲子"),
            },
            pillars,
        )

    def test_approximate_zero_uncertainty_remains_fail_closed(self):
        with self.assertRaisesRegex(
            ValueError,
            "APPROXIMATE precision requires uncertainty_seconds > 0",
        ):
            self.beijing(
                precision=TimePrecision.APPROXIMATE,
                uncertainty_seconds=0,
            )

    def test_nearest_minute_sampling_semantics_are_unchanged(self):
        request = self.beijing(
            precision=TimePrecision.NEAREST_MINUTE,
            uncertainty_seconds=0,
            local=datetime(1994, 5, 17, 14, 30),
        )

        result = self.foundation.resolve_bazi(request)

        self.assertEqual(30, result["input_interval"]["uncertainty_seconds_each_side"])
        self.assertEqual(3, result["input_interval"]["sample_count"])
        self.assertEqual("RESOLVED_RANGE_SINGLE_CLASSIFICATION", result["status"])


if __name__ == "__main__":
    unittest.main()

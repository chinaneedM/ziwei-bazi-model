from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, TimeCalendarFoundation


ROOT = Path(__file__).resolve().parents[1]


class BaziTimeCalendarProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.foundation = TimeCalendarFoundation.from_repository(ROOT)

    @staticmethod
    def beijing(local: datetime, *, timezone_id: str = "Asia/Shanghai", **kwargs) -> BirthInput:
        return BirthInput(
            reported_local_datetime=local,
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id=timezone_id,
            **kwargs,
        )

    def test_a1_authoritative_historical_timezone_four_pillars(self):
        result = self.foundation.resolve_bazi(self.beijing(datetime(1990, 6, 15, 12, 0)))
        self.assertEqual("TIME-CALENDAR-BAZI-PROJECTION-V1", result["schema"])
        self.assertEqual("RESOLVED", result["status"])
        self.assertEqual(1, result["classification_count"])
        self.assertEqual(1, len(result["branches"]))
        branch = result["branches"][0]
        bazi = branch["bazi_time"]
        self.assertEqual(
            ("庚午", "壬午", "辛亥", "癸巳"),
            tuple(
                bazi[key]
                for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")
            ),
        )
        self.assertEqual(9 * 3600, branch["selected_civil_candidate"]["utc_offset_seconds"])
        self.assertEqual(3600, branch["selected_civil_candidate"]["daylight_saving_seconds"])
        self.assertNotIn("ziwei_calendar", branch)
        self.assertTrue(result["metadata"]["ziwei_calendar_evaluated"] is False)

    def test_a1_wenzhen_hour_is_fixed_utc8_compatibility_difference(self):
        authoritative = self.foundation.resolve_bazi(
            self.beijing(datetime(1990, 6, 15, 12, 0), timezone_id="Asia/Shanghai")
        )["branches"][0]
        fixed_utc8 = self.foundation.resolve_bazi(
            self.beijing(datetime(1990, 6, 15, 12, 0), timezone_id="Etc/GMT-8")
        )["branches"][0]
        authoritative_pillars = tuple(
            authoritative["bazi_time"][key]
            for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")
        )
        fixed_pillars = tuple(
            fixed_utc8["bazi_time"][key]
            for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")
        )
        self.assertEqual(authoritative_pillars[:3], fixed_pillars[:3])
        self.assertEqual("癸巳", authoritative_pillars[3])
        self.assertEqual("甲午", fixed_pillars[3])
        self.assertEqual(9 * 3600, authoritative["selected_civil_candidate"]["utc_offset_seconds"])
        self.assertEqual(8 * 3600, fixed_utc8["selected_civil_candidate"]["utc_offset_seconds"])
        self.assertEqual(3600, authoritative["selected_civil_candidate"]["daylight_saving_seconds"])
        self.assertEqual(0, fixed_utc8["selected_civil_candidate"]["daylight_saving_seconds"])

    def test_projection_preserves_same_pillars_as_combined_resolver(self):
        request = self.beijing(datetime(1990, 6, 15, 12, 0))
        combined = self.foundation.resolve(request)["branches"][0]["bazi_time"]
        projected = self.foundation.resolve_bazi(request)["branches"][0]["bazi_time"]
        for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
            self.assertEqual(combined[key], projected[key])

    def test_projection_is_not_limited_by_ziwei_chinese_calendar_adapter(self):
        result = self.foundation.resolve_bazi(self.beijing(datetime(2200, 6, 15, 12, 0)))
        self.assertEqual("RESOLVED", result["status"])
        self.assertEqual(1, len(result["branches"]))
        self.assertEqual(
            4,
            len(
                result["branches"][0]["bazi_time"]["year_pillar"]
                + result["branches"][0]["bazi_time"]["month_pillar"]
            ),
        )
        self.assertNotIn("ziwei_calendar", result["branches"][0])

    def test_same_bazi_classification_keeps_all_time_samples(self):
        result = self.foundation.resolve_bazi(
            self.beijing(datetime(1990, 6, 15, 12, 0), uncertainty_seconds=120)
        )
        self.assertEqual("RESOLVED_RANGE_SINGLE_CLASSIFICATION", result["status"])
        self.assertEqual(1, result["classification_count"])
        self.assertGreater(len(result["branches"]), 1)
        sampled = {branch["sample_reported_local_datetime"] for branch in result["branches"]}
        self.assertGreater(len(sampled), 1)
        self.assertTrue(all("jie_boundaries" in branch for branch in result["branches"]))

    def test_bazi_policy_projection_contains_no_ziwei_policy_fields(self):
        result = self.foundation.resolve_bazi(self.beijing(datetime(1990, 6, 15, 12, 0)))
        policies = result["selected_policies"]
        self.assertEqual(
            {
                "bazi_day_boundary_policy",
                "bazi_late_zi_hour_stem_policy",
                "bazi_year_boundary_policy",
                "civil_ambiguous_time_policy",
            },
            set(policies),
        )


if __name__ == "__main__":
    unittest.main()

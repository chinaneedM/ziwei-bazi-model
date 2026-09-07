from __future__ import annotations

from datetime import date, datetime
import unittest

from fortune_training.ziwei_chart import (
    JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_METHOD_ID,
    TEMPORAL_HISTORICAL_CANDIDATE_SELECTION_STATUS,
    ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_METHOD_ID,
    resolve_jielan_1581_day_anchored_flow_hour_candidate,
    resolve_zhongzhou_leap_month_half_split_candidate,
)


class ZiweiTemporalHistoricalCandidateApiR1Tests(unittest.TestCase):
    def test_jielan_day_anchored_hour_uses_parent_day_then_hour_ordinal(self) -> None:
        row = resolve_jielan_1581_day_anchored_flow_hour_candidate(
            parent_daily_frame_id="DAY:2026-08-18",
            parent_daily_effective_gregorian_date=date(2026, 8, 18),
            parent_daily_active_branch="辰",
            source_local_datetime=datetime(2026, 8, 18, 13, 15),
            reported_civil_date=date(2026, 8, 18),
            ziwei_calendar_date_policy="LOCAL_SOLAR_DATE_INDEXED",
            ziwei_day_boundary_policy="ZI_START_23",
            time_standard="LOCAL_APPARENT_SOLAR_TIME",
        )
        self.assertEqual(JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_METHOD_ID, row["method_id"])
        self.assertEqual(TEMPORAL_HISTORICAL_CANDIDATE_SELECTION_STATUS, row["selection_status"])
        self.assertEqual("未", row["hour_branch"])
        self.assertEqual("亥", row["active_address_branch"])
        self.assertEqual("PARENT_DAILY_ACTIVE_ADDRESS", row["mechanics"]["zi_hour_anchor"])
        self.assertEqual(64, len(row["candidate_hash"]))
        self.assertEqual(
            "NOT_APPLIED_BY_THIS_SOURCE_SCOPED_GEOMETRY_API",
            row["downstream_cross_school_projection_status"],
        )

    def test_jielan_candidate_rejects_cross_time_standard_parent_day_reuse(self) -> None:
        with self.assertRaisesRegex(ValueError, "parent daily frame date"):
            resolve_jielan_1581_day_anchored_flow_hour_candidate(
                parent_daily_frame_id="DAY:2026-08-18",
                parent_daily_effective_gregorian_date=date(2026, 8, 18),
                parent_daily_active_branch="辰",
                source_local_datetime=datetime(2026, 8, 18, 23, 30),
                reported_civil_date=date(2026, 8, 18),
                ziwei_calendar_date_policy="LOCAL_SOLAR_DATE_INDEXED",
                ziwei_day_boundary_policy="ZI_START_23",
                time_standard="ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME",
            )

    def test_jielan_candidate_keeps_time_standard_orthogonal_to_1581_authority(self) -> None:
        row = resolve_jielan_1581_day_anchored_flow_hour_candidate(
            parent_daily_frame_id="DAY:2026-11-15",
            parent_daily_effective_gregorian_date=date(2026, 11, 15),
            parent_daily_active_branch="酉",
            source_local_datetime=datetime(2026, 11, 15, 12, 44, 44),
            reported_civil_date=date(2026, 11, 15),
            ziwei_calendar_date_policy="LOCAL_SOLAR_DATE_INDEXED",
            ziwei_day_boundary_policy="ZI_START_23",
            time_standard="ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME",
        )
        self.assertEqual(
            "ORTHOGONAL_INPUT_NOT_AUTHORIZED_BY_JIELAN_1581",
            row["time_standard_authority"],
        )
        self.assertIn("EXT-ZIWEI-JIELAN-1581:CH54", row["source_refs"][0])

    @staticmethod
    def _leap(day: int):
        return resolve_zhongzhou_leap_month_half_split_candidate(
            leap_lunar_year=2025,
            leap_lunar_month=6,
            leap_lunar_day=day,
            previous_month_temporal_year=2025,
            previous_month_number=6,
            previous_month_frame_id="MONTH:2025:6",
            previous_month_ganzhi="癸未",
            previous_month_active_branch="午",
            following_month_temporal_year=2025,
            following_month_number=7,
            following_month_frame_id="MONTH:2025:7",
            following_month_ganzhi="甲申",
            following_month_active_branch="未",
        )

    def test_zhongzhou_leap_half_split_switches_only_after_day_15(self) -> None:
        day15 = self._leap(15)
        day16 = self._leap(16)
        self.assertEqual(ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_METHOD_ID, day15["method_id"])
        self.assertEqual("PREVIOUS_MONTH", day15["segment"])
        self.assertEqual("MONTH:2025:6", day15["assigned_regular_month"]["frame_id"])
        self.assertEqual("癸未", day15["assigned_regular_month"]["ganzhi"])
        self.assertEqual("FOLLOWING_MONTH", day16["segment"])
        self.assertEqual("MONTH:2025:7", day16["assigned_regular_month"]["frame_id"])
        self.assertEqual("甲申", day16["assigned_regular_month"]["ganzhi"])
        self.assertFalse(day15["flow_day_continuity"]["half_split_reset"])
        self.assertFalse(day16["flow_day_continuity"]["half_split_reset"])

    def test_zhongzhou_leap_policy_does_not_invent_daily_origin_geometry(self) -> None:
        row = self._leap(16)
        continuity = row["flow_day_continuity"]
        self.assertFalse(continuity["daily_active_address_emitted"])
        self.assertEqual("NOT_CLOSED_BY_THIS_MONTH_POLICY_API", continuity["daily_origin_semantics"])
        self.assertEqual(
            "MONTH_ASSIGNMENT_CANDIDATE_ONLY_DAILY_GEOMETRY_REMAINS_FAIL_CLOSED",
            row["downstream_projection_status"],
        )
        self.assertEqual(64, len(row["candidate_hash"]))

    def test_zhongzhou_leap_month_12_requires_next_year_month_1(self) -> None:
        row = resolve_zhongzhou_leap_month_half_split_candidate(
            leap_lunar_year=2033,
            leap_lunar_month=12,
            leap_lunar_day=20,
            previous_month_temporal_year=2033,
            previous_month_number=12,
            previous_month_frame_id="MONTH:2033:12",
            previous_month_ganzhi="乙丑",
            previous_month_active_branch="丑",
            following_month_temporal_year=2034,
            following_month_number=1,
            following_month_frame_id="MONTH:2034:1",
            following_month_ganzhi="丙寅",
            following_month_active_branch="寅",
        )
        self.assertEqual(2034, row["assigned_regular_month"]["temporal_year"])
        self.assertEqual(1, row["assigned_regular_month"]["month"])
        with self.assertRaisesRegex(ValueError, "immediate successor"):
            resolve_zhongzhou_leap_month_half_split_candidate(
                leap_lunar_year=2033,
                leap_lunar_month=12,
                leap_lunar_day=20,
                previous_month_temporal_year=2033,
                previous_month_number=12,
                previous_month_frame_id="MONTH:2033:12",
                previous_month_ganzhi="乙丑",
                previous_month_active_branch="丑",
                following_month_temporal_year=2033,
                following_month_number=1,
                following_month_frame_id="MONTH:2033:1",
                following_month_ganzhi="丙寅",
                following_month_active_branch="寅",
            )


if __name__ == "__main__":
    unittest.main()

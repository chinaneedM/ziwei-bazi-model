from __future__ import annotations

import json
import math
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from fortune_training.calendar_foundation import (
    BirthInput,
    ChineseCalendarEngine,
    CivilTimeResolver,
    InputTimeType,
    PolicyRegistry,
    SolarTermEngine,
    SolarTimeEngine,
    TimeCalendarFoundation,
)
from fortune_training.calendar_foundation.bazi import BaziTimeResolver
from fortune_training.calendar_foundation.models import CivilTimeStatus
from fortune_training.calendar_foundation.policies import PolicySelection
from fortune_training.calendar_foundation.ziwei import ZiweiCalendarResolver


ROOT = Path(__file__).resolve().parents[1]


def birth(local: datetime, place: str = "Shanghai", longitude: float = 121.4737, timezone_id: str = "Asia/Shanghai", **kwargs):
    return BirthInput(
        reported_local_datetime=local,
        birth_place=place,
        latitude=31.2304,
        longitude=longitude,
        timezone_id=timezone_id,
        **kwargs,
    )


class TimeCalendarFoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.foundation = TimeCalendarFoundation(cls.registry)
        cls.fixtures = json.loads(
            (ROOT / "tests" / "fixtures" / "time-calendar-foundation-r1.json").read_text(encoding="utf-8")
        )

    def test_standard_modern_china_civil_time(self):
        resolved = CivilTimeResolver().resolve(birth(datetime(2000, 1, 8, 12, 0)))
        self.assertEqual(CivilTimeStatus.UNIQUE, resolved.status)
        self.assertEqual("2000-01-08T04:00:00+00:00", resolved.selected_candidate.utc_instant.isoformat())
        self.assertEqual(8 * 3600, resolved.selected_candidate.utc_offset_seconds)
        self.assertEqual(0, resolved.selected_candidate.daylight_saving_seconds)

    def test_true_solar_time_crosses_hour_and_preserves_seconds(self):
        resolved = CivilTimeResolver().resolve(
            birth(datetime(2000, 1, 8, 4, 0), "Urumqi", 87.6168)
        )
        solar = SolarTimeEngine().resolve(
            resolved.selected_candidate.utc_instant,
            87.6168,
            resolved.selected_candidate.utc_offset_seconds,
        )
        self.assertEqual(1, solar.local_apparent_solar_datetime.hour)
        self.assertNotEqual(0, solar.local_apparent_solar_datetime.second)

    def test_kashgar_true_solar_cross_day_compatibility_fixture(self):
        fixture = next(row for row in self.fixtures["third_party_compatibility"] if row["id"] == "D")
        result = self.foundation.resolve(
            BirthInput(
                datetime.fromisoformat(fixture["reported_civil_datetime"]),
                fixture["place"],
                fixture["latitude"],
                fixture["longitude"],
                fixture["timezone_id"],
            )
        )
        branch = result["branches"][0]
        self.assertEqual("2000-12-25", branch["solar_time"]["local_apparent_solar_datetime"][:10])
        lunar = branch["ziwei_calendar"]["effective_ziwei_lunar_date"]
        self.assertEqual((2000, 11, 30, False), (lunar["year"], lunar["month"], lunar["day"], lunar["is_leap_month"]))
        bazi = branch["bazi_time"]
        self.assertEqual(tuple(fixture["expected_bazi"]), tuple(bazi[key] for key in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar")))
        self.assertIn("CALENDAR_DATE_DIVERGENCE", branch["ziwei_calendar"]["events"])

    def test_late_zi_policies_and_23_00_00_00_01_00_boundaries(self):
        resolver = BaziTimeResolver()
        utc = datetime(2000, 1, 7, 15, 30, tzinfo=timezone.utc)
        common = {"year_boundary_policy": "START_OF_SPRING", "day_boundary_policy": "MIDNIGHT"}
        classical = resolver.resolve(utc, datetime(2000, 1, 7, 23, 30), late_zi_hour_stem_policy="CLASSICAL_CONTINUOUS", **common)
        current = resolver.resolve(utc, datetime(2000, 1, 7, 23, 30), late_zi_hour_stem_policy="CURRENT_DAY_STEM", **common)
        rollover = resolver.resolve(
            utc,
            datetime(2000, 1, 7, 23, 30),
            year_boundary_policy="START_OF_SPRING",
            day_boundary_policy="ZI_START_23",
            late_zi_hour_stem_policy="ZI_START_ROLLOVER",
        )
        midnight = resolver.resolve(utc, datetime(2000, 1, 8, 0, 0), late_zi_hour_stem_policy="CLASSICAL_CONTINUOUS", **common)
        one_am = resolver.resolve(utc, datetime(2000, 1, 8, 1, 0), late_zi_hour_stem_policy="CLASSICAL_CONTINUOUS", **common)
        self.assertEqual("甲子", classical.day_pillar)
        self.assertEqual("丙子", classical.hour_pillar)
        self.assertEqual("甲子", current.hour_pillar)
        self.assertEqual("乙丑", rollover.day_pillar)
        self.assertEqual("乙丑", midnight.day_pillar)
        self.assertNotEqual(midnight.hour_pillar, one_am.hour_pillar)

    def test_solar_term_instant_before_and_after_uses_utc_comparison(self):
        terms = SolarTermEngine()
        spring = terms.term(2000, 315).utc_instant
        resolver = BaziTimeResolver(terms)
        before = resolver.resolve(
            spring - timedelta(microseconds=1),
            datetime(2000, 2, 4, 20, 0),
            year_boundary_policy="START_OF_SPRING",
            day_boundary_policy="MIDNIGHT",
            late_zi_hour_stem_policy="CLASSICAL_CONTINUOUS",
        )
        after = resolver.resolve(
            spring + timedelta(microseconds=1),
            datetime(2000, 2, 4, 21, 0),
            year_boundary_policy="START_OF_SPRING",
            day_boundary_policy="MIDNIGHT",
            late_zi_hour_stem_policy="CLASSICAL_CONTINUOUS",
        )
        self.assertEqual("己卯", before.year_pillar)
        self.assertEqual("庚辰", after.year_pillar)
        self.assertNotEqual(before.month_pillar, after.month_pillar)

    def test_historical_china_dst(self):
        resolved = CivilTimeResolver().resolve(birth(datetime(1988, 7, 1, 12, 0)))
        self.assertEqual(9 * 3600, resolved.selected_candidate.utc_offset_seconds)
        self.assertEqual(3600, resolved.selected_candidate.daylight_saving_seconds)

    def test_overseas_timezone(self):
        resolved = CivilTimeResolver().resolve(
            birth(datetime(2020, 1, 1, 12, 0), "New York", -74.006, "America/New_York")
        )
        self.assertEqual(-5 * 3600, resolved.selected_candidate.utc_offset_seconds)
        self.assertEqual("2020-01-01T17:00:00+00:00", resolved.selected_candidate.utc_instant.isoformat())

    def test_ambiguous_dst_time_returns_two_candidates(self):
        resolved = CivilTimeResolver().resolve(
            birth(datetime(2020, 11, 1, 1, 30), "New York", -74.006, "America/New_York")
        )
        self.assertEqual(CivilTimeStatus.AMBIGUOUS, resolved.status)
        self.assertEqual(2, len(resolved.candidates))
        self.assertIsNone(resolved.selected_candidate)
        self.assertEqual(3600, int((resolved.candidates[1].utc_instant - resolved.candidates[0].utc_instant).total_seconds()))

    def test_nonexistent_dst_time_fails_closed(self):
        resolved = CivilTimeResolver().resolve(
            birth(datetime(2020, 3, 8, 2, 30), "New York", -74.006, "America/New_York")
        )
        self.assertEqual(CivilTimeStatus.NONEXISTENT, resolved.status)
        self.assertFalse(resolved.candidates)

    def test_new_moon_date_and_hko_2000_oracle(self):
        calendar = ChineseCalendarEngine()
        before = calendar.from_gregorian_date(date(2000, 1, 6))
        after = calendar.from_gregorian_date(date(2000, 1, 7))
        self.assertEqual((1999, 11, 30), (before.year, before.month, before.day))
        self.assertEqual((1999, 12, 1), (after.year, after.month, after.day))

    def test_civil_and_true_solar_calendar_mappings_remain_separate(self):
        result = self.foundation.resolve(
            BirthInput(datetime(2000, 12, 26, 1, 40), "Kashgar", 39.4704, 75.9898, "Asia/Shanghai")
        )["branches"][0]["ziwei_calendar"]
        self.assertEqual(12, result["actual_civil_lunar_date"]["month"])
        self.assertEqual(11, result["local_solar_lunar_date"]["month"])
        self.assertEqual(11, result["effective_ziwei_lunar_date"]["month"])

    def test_leap_month_policy_is_scoped_and_does_not_mutate_raw_date(self):
        calendar = ChineseCalendarEngine()
        ziwei = ZiweiCalendarResolver(calendar)
        raw = calendar.from_gregorian_date(date(2020, 5, 23))
        self.assertEqual((4, 1, True), (raw.month, raw.day, raw.is_leap_month))
        for policy in ("FULLBOOK_NEXT_MONTH", "ZHONGZHOU_FIXED_15", "CURRENT_MONTH", "TRUE_HALF_SPLIT"):
            result = ziwei.resolve(
                date(2020, 5, 23),
                datetime(2020, 5, 23, 12),
                calendar_date_policy="LOCAL_SOLAR_DATE_INDEXED",
                life_body_leap_month_policy=policy,
            )
            self.assertEqual(raw, result.effective_ziwei_lunar_date)

    def test_2033_calendar_anomaly_uses_leap_eleventh_month(self):
        result = ChineseCalendarEngine().from_gregorian_date(date(2033, 12, 22))
        self.assertEqual((2033, 11, 1, True), (result.year, result.month, result.day, result.is_leap_month))

    def test_precision_interval_crossing_boundary_returns_multiple_classifications(self):
        result = self.foundation.resolve(
            birth(datetime(2000, 1, 7, 23, 0), uncertainty_seconds=90)
        )
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", result["status"])
        self.assertGreater(result["classification_count"], 1)

    def test_authority_and_independent_formula_regressions(self):
        calendar = ChineseCalendarEngine()
        for fixture in self.fixtures["authority_oracles"]:
            actual = calendar.from_gregorian_date(date.fromisoformat(fixture["gregorian_date"]))
            expected = fixture["expected_lunar"]
            self.assertEqual(
                (expected["year"], expected["month"], expected["day"], expected["is_leap_month"]),
                (actual.year, actual.month, actual.day, actual.is_leap_month),
            )
        spring = SolarTermEngine().term(2000, 315)
        self.assertEqual(date(2000, 2, 4), (spring.utc_instant + timedelta(hours=8)).date())

        # Independent NOAA/USNO-style approximation cross-checks EOT to one minute.
        instant = datetime(2024, 2, 11, 12, tzinfo=timezone.utc)
        n = instant.timetuple().tm_yday
        gamma = 2 * math.pi / 366 * (n - 1 + (instant.hour - 12) / 24)
        approximate_minutes = 229.18 * (
            0.000075
            + 0.001868 * math.cos(gamma)
            - 0.032077 * math.sin(gamma)
            - 0.014615 * math.cos(2 * gamma)
            - 0.040849 * math.sin(2 * gamma)
        )
        calculated_minutes = SolarTimeEngine.equation_of_time_seconds(instant) / 60
        self.assertLess(abs(approximate_minutes - calculated_minutes), 1.0)

    def test_non_civil_input_does_not_invent_utc(self):
        result = self.foundation.resolve(
            birth(datetime(2000, 1, 8, 0, 30), input_time_type=InputTimeType.ALREADY_TRUE_SOLAR)
        )
        self.assertEqual("UNRESOLVED_CIVIL_TIME", result["status"])
        self.assertFalse(result["branches"])

    def test_policy_registry_and_schema_are_machine_readable(self):
        defaults = self.registry.default_selection()
        self.assertEqual("CLASSICAL_CONTINUOUS", defaults.bazi_late_zi_hour_stem_policy)
        self.assertEqual("LOCAL_SOLAR_DATE_INDEXED", defaults.ziwei_calendar_date_policy)
        schema = json.loads((ROOT / "schemas" / "time-calendar-foundation-v1.schema.json").read_text(encoding="utf-8"))
        self.assertEqual("TIME-CALENDAR-FOUNDATION-RESULT-V1", schema["properties"]["schema"]["const"])


if __name__ == "__main__":
    unittest.main()

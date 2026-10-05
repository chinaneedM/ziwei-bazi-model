from __future__ import annotations

import json
import math
import tempfile
import unittest
from dataclasses import replace
from unittest.mock import patch
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import fortune_training.calendar_foundation.timezone as timezone_module
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
from fortune_training.calendar_foundation.models import CivilTimeStatus, HistoricalTimezoneConfidence
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

    def test_tzdb_confidence_uses_utc_posix_epoch_not_local_calendar_year(self):
        shanghai = CivilTimeResolver().resolve(
            birth(datetime(1970, 1, 1, 0, 30), "Shanghai", 121.4737, "Asia/Shanghai")
        )
        self.assertEqual("1969-12-31T16:30:00+00:00", shanghai.selected_candidate.utc_instant.isoformat())
        self.assertEqual(HistoricalTimezoneConfidence.TZDB_PRE_1970_REDUCED, shanghai.historical_confidence)
        self.assertIn("IANA tzdb does not guarantee complete pre-1970 historical coverage", shanghai.warnings)

        new_york = CivilTimeResolver().resolve(
            birth(datetime(1969, 12, 31, 19, 30), "New York", -74.006, "America/New_York")
        )
        self.assertEqual("1970-01-01T00:30:00+00:00", new_york.selected_candidate.utc_instant.isoformat())
        self.assertEqual(HistoricalTimezoneConfidence.TZDB_POST_1970, new_york.historical_confidence)
        self.assertNotIn("IANA tzdb does not guarantee complete pre-1970 historical coverage", new_york.warnings)

    def test_tzdb_version_metadata_follows_zoneinfo_source_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            zone_file = Path(tmp) / "Asia" / "Shanghai"
            zone_file.parent.mkdir(parents=True)
            zone_file.write_bytes(b"synthetic-zone-file")
            with (
                patch.object(timezone_module.zoneinfo, "TZPATH", (tmp,)),
                patch.object(timezone_module, "version", return_value="2099.1"),
            ):
                self.assertEqual(
                    "SYSTEM-TZDB-UNVERSIONED",
                    CivilTimeResolver._tzdb_version("Asia/Shanghai"),
                )

        with (
            patch.object(timezone_module.zoneinfo, "TZPATH", ()),
            patch.object(timezone_module, "version", return_value="2099.1"),
        ):
            self.assertEqual("2099.1", CivilTimeResolver._tzdb_version("Asia/Shanghai"))

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

    def test_explicit_fold_policies_select_pep495_reading_and_preserve_both_candidates(self):
        resolver = CivilTimeResolver()
        value = birth(datetime(2020, 11, 1, 1, 30), "New York", -74.006, "America/New_York")
        earlier = resolver.resolve(value, ambiguous_time_policy="EARLIER_OFFSET")
        later = resolver.resolve(value, ambiguous_time_policy="LATER_OFFSET")

        self.assertEqual(CivilTimeStatus.AMBIGUOUS, earlier.status)
        self.assertEqual(CivilTimeStatus.AMBIGUOUS, later.status)
        self.assertEqual(2, len(earlier.candidates))
        self.assertEqual(earlier.candidates, later.candidates)
        self.assertEqual(0, earlier.selected_candidate.fold)
        self.assertEqual(1, later.selected_candidate.fold)
        self.assertEqual("2020-11-01T05:30:00+00:00", earlier.selected_candidate.utc_instant.isoformat())
        self.assertEqual("2020-11-01T06:30:00+00:00", later.selected_candidate.utc_instant.isoformat())

    def test_reject_policy_preserves_fold_branches_at_foundation_layer(self):
        value = BirthInput(
            datetime(2020, 11, 1, 1, 30),
            "New York",
            40.7128,
            -74.006,
            "America/New_York",
        )
        default_result = self.foundation.resolve_bazi(value)
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", default_result["status"])
        self.assertEqual(2, len(default_result["branches"]))
        self.assertEqual(1, default_result["input_interval"]["ambiguous_sample_count"])

        earlier_selection = replace(
            self.registry.default_bazi_selection(),
            civil_ambiguous_time_policy="EARLIER_OFFSET",
        )
        selected_result = self.foundation.resolve_bazi(value, earlier_selection)
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", selected_result["status"])
        self.assertEqual(1, len(selected_result["branches"]))
        self.assertEqual(1, selected_result["input_interval"]["ambiguous_sample_count"])
        civil = selected_result["branches"][0]["civil_time"]
        self.assertEqual("AMBIGUOUS", civil["status"])
        self.assertEqual(2, len(civil["candidates"]))
        self.assertEqual(0, civil["selected_candidate"]["fold"])

    def test_fold_and_gap_handling_does_not_assume_one_hour_dst_transition(self):
        resolver = CivilTimeResolver()
        lord_howe_fold = resolver.resolve(
            birth(datetime(2020, 4, 5, 1, 45), "Lord Howe", 159.075, "Australia/Lord_Howe")
        )
        self.assertEqual(CivilTimeStatus.AMBIGUOUS, lord_howe_fold.status)
        self.assertEqual(
            1800,
            int((lord_howe_fold.candidates[1].utc_instant - lord_howe_fold.candidates[0].utc_instant).total_seconds()),
        )

        lord_howe_gap = resolver.resolve(
            birth(datetime(2020, 10, 4, 2, 15), "Lord Howe", 159.075, "Australia/Lord_Howe")
        )
        self.assertEqual(CivilTimeStatus.NONEXISTENT, lord_howe_gap.status)
        self.assertFalse(lord_howe_gap.candidates)

        kyiv_fold = resolver.resolve(
            birth(datetime(1990, 7, 1, 1, 30), "Kyiv", 30.5234, "Europe/Kyiv")
        )
        self.assertEqual(CivilTimeStatus.AMBIGUOUS, kyiv_fold.status)
        self.assertEqual({3600}, {candidate.daylight_saving_seconds for candidate in kyiv_fold.candidates})
        self.assertEqual(
            {"1990-06-30T21:30:00+00:00", "1990-06-30T22:30:00+00:00"},
            {candidate.utc_instant.isoformat() for candidate in kyiv_fold.candidates},
        )

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

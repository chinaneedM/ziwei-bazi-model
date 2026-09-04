from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta

from fortune_training.calendar_foundation import (
    BirthInput,
    ChineseCalendarEngine,
    CivilTimeResolver,
    SolarTermEngine,
)
from fortune_training.calendar_foundation.bazi import BaziTimeResolver
from fortune_training.calendar_foundation.models import CivilTimeStatus


class FusionChartTemporalBoundaryTortureR1Tests(unittest.TestCase):
    @staticmethod
    def _ny(local: datetime) -> BirthInput:
        return BirthInput(
            local,
            "New York",
            40.7128,
            -74.0060,
            "America/New_York",
        )

    def test_dst_gap_second_by_second_edges_fail_closed(self) -> None:
        resolver = CivilTimeResolver()
        before = resolver.resolve(self._ny(datetime(2020, 3, 8, 1, 59, 59)))
        start = resolver.resolve(self._ny(datetime(2020, 3, 8, 2, 0, 0)))
        end = resolver.resolve(self._ny(datetime(2020, 3, 8, 2, 59, 59)))
        after = resolver.resolve(self._ny(datetime(2020, 3, 8, 3, 0, 0)))
        self.assertEqual(CivilTimeStatus.UNIQUE, before.status)
        self.assertEqual(CivilTimeStatus.NONEXISTENT, start.status)
        self.assertEqual(CivilTimeStatus.NONEXISTENT, end.status)
        self.assertEqual(CivilTimeStatus.UNIQUE, after.status)

    def test_dst_fold_second_by_second_edges_preserve_two_instants(self) -> None:
        resolver = CivilTimeResolver()
        start = resolver.resolve(self._ny(datetime(2020, 11, 1, 1, 0, 0)))
        end = resolver.resolve(self._ny(datetime(2020, 11, 1, 1, 59, 59)))
        after = resolver.resolve(self._ny(datetime(2020, 11, 1, 2, 0, 0)))
        self.assertEqual(CivilTimeStatus.AMBIGUOUS, start.status)
        self.assertEqual(CivilTimeStatus.AMBIGUOUS, end.status)
        self.assertEqual(2, len(start.candidates))
        self.assertEqual(2, len(end.candidates))
        self.assertEqual(CivilTimeStatus.UNIQUE, after.status)

    def test_late_zi_23_00_and_midnight_boundaries_are_explicit(self) -> None:
        resolver = BaziTimeResolver()
        common = {
            "year_boundary_policy": "START_OF_SPRING",
            "day_boundary_policy": "MIDNIGHT",
            "late_zi_hour_stem_policy": "CLASSICAL_CONTINUOUS",
        }
        utc_anchor = datetime(2000, 1, 7, 15, 0)
        before = resolver.resolve(
            utc_anchor - timedelta(seconds=1),
            datetime(2000, 1, 7, 22, 59, 59),
            **common,
        )
        at_zi = resolver.resolve(
            utc_anchor,
            datetime(2000, 1, 7, 23, 0, 0),
            **common,
        )
        before_midnight = resolver.resolve(
            utc_anchor + timedelta(hours=1) - timedelta(seconds=1),
            datetime(2000, 1, 7, 23, 59, 59),
            **common,
        )
        at_midnight = resolver.resolve(
            utc_anchor + timedelta(hours=1),
            datetime(2000, 1, 8, 0, 0, 0),
            **common,
        )
        self.assertNotEqual(before.hour_pillar, at_zi.hour_pillar)
        self.assertEqual(at_zi.day_pillar, before_midnight.day_pillar)
        self.assertNotEqual(before_midnight.day_pillar, at_midnight.day_pillar)

        rollover = resolver.resolve(
            utc_anchor,
            datetime(2000, 1, 7, 23, 0, 0),
            year_boundary_policy="START_OF_SPRING",
            day_boundary_policy="ZI_START_23",
            late_zi_hour_stem_policy="ZI_START_ROLLOVER",
        )
        self.assertEqual(at_midnight.day_pillar, rollover.day_pillar)

    def test_start_of_spring_exact_second_switches_year_and_month(self) -> None:
        term = SolarTermEngine().term(2000, 315).utc_instant
        resolver = BaziTimeResolver()
        common = {
            "year_boundary_policy": "START_OF_SPRING",
            "day_boundary_policy": "MIDNIGHT",
            "late_zi_hour_stem_policy": "CLASSICAL_CONTINUOUS",
        }
        before = resolver.resolve(
            term - timedelta(seconds=1),
            datetime(2000, 2, 4, 20, 0, 0),
            **common,
        )
        after = resolver.resolve(
            term + timedelta(seconds=1),
            datetime(2000, 2, 4, 21, 0, 0),
            **common,
        )
        self.assertEqual("己卯", before.year_pillar)
        self.assertEqual("庚辰", after.year_pillar)
        self.assertNotEqual(before.month_pillar, after.month_pillar)

    def test_leap_month_entry_date_is_not_smeared_across_previous_day(self) -> None:
        calendar = ChineseCalendarEngine()
        before = calendar.from_gregorian_date(date(2020, 5, 22))
        entry = calendar.from_gregorian_date(date(2020, 5, 23))
        self.assertEqual((4, 1, True), (entry.month, entry.day, entry.is_leap_month))
        self.assertNotEqual(
            (before.month, before.day, before.is_leap_month),
            (entry.month, entry.day, entry.is_leap_month),
        )

    def test_true_solar_cross_day_is_stable_at_adjacent_seconds(self) -> None:
        from fortune_training.calendar_foundation import PolicyRegistry, TimeCalendarFoundation
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        foundation = TimeCalendarFoundation(
            PolicyRegistry.from_file(root / "config" / "time-calendar-policies.json")
        )
        rows = []
        for second in (39, 40, 41):
            result = foundation.resolve(
                BirthInput(
                    datetime(2000, 12, 26, 1, 40, second),
                    "Kashgar",
                    39.4704,
                    75.9898,
                    "Asia/Shanghai",
                )
            )
            rows.append(
                result["branches"][0]["solar_time"]["local_apparent_solar_datetime"][:10]
            )
        self.assertEqual(["2000-12-25"] * 3, rows)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta, timezone

from fortune_training.calendar_foundation import (
    BaziTimeResolver,
    double_hour_branch_index,
    five_rats_hour_pillar,
    sexagenary_day_index,
)
from fortune_training.calendar_foundation.sexagenary import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
)


class BaziNatalFourPillarCompositionAuditR1Tests(unittest.TestCase):
    def test_year_identity_and_five_tigers_yin_month_starts(self) -> None:
        resolver = BaziTimeResolver()
        expected_years = ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉"]
        expected_yin_months = ["丙寅", "戊寅", "庚寅", "壬寅", "甲寅", "丙寅", "戊寅", "庚寅", "壬寅", "甲寅"]
        for offset, year in enumerate(range(1984, 1994)):
            row = resolver.resolve_year_month(
                datetime(year, 2, 20, 12, tzinfo=timezone.utc),
                year_boundary_policy="START_OF_SPRING",
            )
            self.assertEqual(expected_years[offset], row.year_pillar)
            self.assertEqual(expected_yin_months[offset], row.month_pillar)

    def test_five_tigers_advances_all_twelve_month_positions(self) -> None:
        resolver = BaziTimeResolver()
        samples = [
            datetime(1984, 2, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 3, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 4, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 5, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 6, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 7, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 8, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 9, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 10, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 11, 20, 12, tzinfo=timezone.utc),
            datetime(1984, 12, 20, 12, tzinfo=timezone.utc),
            datetime(1985, 1, 20, 12, tzinfo=timezone.utc),
        ]
        expected = ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑"]
        actual = [
            resolver.resolve_year_month(
                instant,
                year_boundary_policy="START_OF_SPRING",
            ).month_pillar
            for instant in samples
        ]
        self.assertEqual(expected, actual)

    def test_gregorian_jdn_day_bridge_matches_modern_anchor_and_full_cycle(self) -> None:
        anchor = date(1949, 10, 1)
        self.assertEqual(0, sexagenary_day_index(anchor))
        self.assertEqual(
            list(range(60)),
            [sexagenary_day_index(anchor + timedelta(days=i)) for i in range(60)],
        )
        self.assertEqual(0, sexagenary_day_index(date(2000, 1, 7)))

    def test_selected_clock_double_hour_partition_is_explicit(self) -> None:
        expected = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 0]
        actual = [
            double_hour_branch_index(datetime(2000, 1, 1, hour, 0))
            for hour in range(24)
        ]
        self.assertEqual(expected, actual)

    def test_five_rats_replays_all_ten_day_stems_by_twelve_branches(self) -> None:
        anchor = date(1949, 10, 1)
        representative_hours = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
        seen = 0
        for day_stem_index in range(10):
            source_date = anchor + timedelta(days=day_stem_index)
            zi_stem_index = (day_stem_index % 5) * 2
            for branch_index, hour in enumerate(representative_hours):
                expected = (
                    HEAVENLY_STEMS[(zi_stem_index + branch_index) % 10]
                    + EARTHLY_BRANCHES[branch_index]
                )
                actual = five_rats_hour_pillar(
                    datetime(2000, 1, 1, hour, 0),
                    source_date,
                )
                self.assertEqual(expected, actual)
                seen += 1
        self.assertEqual(120, seen)

    def test_late_zi_source_day_candidates_remain_unranked_by_component_audit(self) -> None:
        resolver = BaziTimeResolver()
        utc = datetime(2000, 1, 7, 15, 30, tzinfo=timezone.utc)
        clock = datetime(2000, 1, 7, 23, 30)
        classical = resolver.resolve(
            utc,
            clock,
            year_boundary_policy="START_OF_SPRING",
            day_boundary_policy="MIDNIGHT",
            late_zi_hour_stem_policy="CLASSICAL_CONTINUOUS",
        )
        current = resolver.resolve(
            utc,
            clock,
            year_boundary_policy="START_OF_SPRING",
            day_boundary_policy="MIDNIGHT",
            late_zi_hour_stem_policy="CURRENT_DAY_STEM",
        )
        rollover = resolver.resolve(
            utc,
            clock,
            year_boundary_policy="START_OF_SPRING",
            day_boundary_policy="ZI_START_23",
            late_zi_hour_stem_policy="ZI_START_ROLLOVER",
        )
        self.assertEqual(("甲子", "丙子"), (classical.day_pillar, classical.hour_pillar))
        self.assertEqual(("甲子", "甲子"), (current.day_pillar, current.hour_pillar))
        self.assertEqual(("乙丑", "丙子"), (rollover.day_pillar, rollover.hour_pillar))


if __name__ == "__main__":
    unittest.main()

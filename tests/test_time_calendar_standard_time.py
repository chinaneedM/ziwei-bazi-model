from __future__ import annotations

import unittest
from datetime import date, datetime, timezone

from fortune_training.calendar_foundation import BirthInput, ChineseCalendarEngine, TimePrecision


class ChineseCalendarStandardTimeRegressionTests(unittest.TestCase):
    def test_calendar_day_boundary_uses_fixed_beijing_standard_time(self):
        calendar = ChineseCalendarEngine()

        # GB/T 33661 defines the Chinese-calendar day by Beijing Standard Time
        # (120E standard time), not by historical civil DST in Shanghai/China.
        # During Chinese DST in 1988, 15:30 UTC was 00:30 on the next civil day
        # under Asia/Shanghai, but it is still 23:30 on the same standard-time
        # calendar day at fixed UTC+08:00.
        instant = datetime(1988, 7, 1, 15, 30, tzinfo=timezone.utc)
        self.assertEqual(date(1988, 7, 1), calendar._local_date(instant))
        self.assertEqual("UTC+08:00", calendar.calendar_zone)
        self.assertEqual("BEIJING_STANDARD_TIME", calendar.calendar_time_standard)

    def test_approximate_precision_requires_explicit_uncertainty(self):
        with self.assertRaisesRegex(ValueError, "APPROXIMATE precision requires uncertainty_seconds > 0"):
            BirthInput(
                reported_local_datetime=datetime(2000, 1, 1, 12, 0),
                birth_place="Shanghai",
                latitude=31.2304,
                longitude=121.4737,
                timezone_id="Asia/Shanghai",
                precision=TimePrecision.APPROXIMATE,
            )

        value = BirthInput(
            reported_local_datetime=datetime(2000, 1, 1, 12, 0),
            birth_place="Shanghai",
            latitude=31.2304,
            longitude=121.4737,
            timezone_id="Asia/Shanghai",
            precision=TimePrecision.APPROXIMATE,
            uncertainty_seconds=900,
        )
        self.assertEqual(900, value.effective_uncertainty_seconds)


if __name__ == "__main__":
    unittest.main()

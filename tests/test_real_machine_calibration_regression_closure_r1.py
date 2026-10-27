from __future__ import annotations

import unittest
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationRequest,
    BaziApplicationResolutionError,
    BaziChartService,
    bazi_local_application_v1_profile,
)
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import (
    BaziSex,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.bazi_temporal.engine import _dayun_anniversary
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimePrecision


ROOT = Path(__file__).resolve().parents[1]
PRE_1970_WARNING = "IANA tzdb does not guarantee complete pre-1970 historical coverage"


class RealMachineCalibrationRegressionClosureR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.natal_profile = bazi_foundation_v1_profile(registry)
        cls.temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.application_profile = bazi_local_application_v1_profile()
        cls.service = BaziChartService.from_repository(ROOT)

    @classmethod
    def request(cls, birth: BirthInput) -> BaziApplicationRequest:
        return BaziApplicationRequest(
            birth=birth,
            sex=BaziSex.MALE,
            natal_profile=cls.natal_profile,
            temporal_profile=cls.temporal_profile,
            application_profile=cls.application_profile,
            dayun_count=12,
        )

    @staticmethod
    def shanghai_1900() -> BirthInput:
        return BirthInput(
            reported_local_datetime=datetime(1900, 12, 31, 23, 57),
            birth_place="Shanghai",
            latitude=31.2304,
            longitude=121.4737,
            timezone_id="Asia/Shanghai",
            precision=TimePrecision.EXACT_SECOND,
        )

    @staticmethod
    def apia(local: datetime, precision: TimePrecision) -> BirthInput:
        return BirthInput(
            reported_local_datetime=local,
            birth_place="Apia",
            latitude=-13.833333,
            longitude=-171.76666,
            timezone_id="Pacific/Apia",
            precision=precision,
        )

    @staticmethod
    def lord_howe(local: datetime, precision: TimePrecision) -> BirthInput:
        return BirthInput(
            reported_local_datetime=local,
            birth_place="Lord Howe Island",
            latitude=-31.5531,
            longitude=159.0839,
            timezone_id="Australia/Lord_Howe",
            precision=precision,
        )

    def test_shanghai_1900_lmt_to_cst_fold_keeps_both_civil_realizations(self) -> None:
        result = self.service.resolve(self.request(self.shanghai_1900()))
        provenance = result.time_calendar_provenance

        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(1, provenance.sample_count)
        self.assertEqual(1, provenance.ambiguous_sample_count)
        self.assertEqual(2, provenance.legal_realization_count)
        self.assertEqual(0, provenance.unresolved_sample_count)
        self.assertEqual(2, len(result.candidates))

        legal = provenance.legal_realizations
        self.assertEqual({"LMT", "CST"}, {row.timezone_abbreviation for row in legal})
        self.assertEqual({29143, 28800}, {row.utc_offset_seconds for row in legal})
        self.assertEqual(
            {"1900-12-31T15:51:17Z", "1900-12-31T15:57:00Z"},
            {row.birth_utc for row in legal},
        )
        self.assertEqual({0, 1}, {row.fold for row in legal})
        self.assertEqual({0, 1}, {row.source_time_branch_index for row in legal})
        self.assertEqual(
            {"TZDB_PRE_1970_REDUCED"},
            {row.historical_confidence for row in legal},
        )
        self.assertTrue(all(PRE_1970_WARNING in row.warnings for row in legal))

        # Distinct civil realizations survive even when the Natal fact identity is the same.
        self.assertEqual(1, len({row.natal_fact_hash for row in result.candidates}))
        self.assertEqual(2, len({row.temporal_fact_hash for row in result.candidates}))
        self.assertEqual("PASS", result.integrity.status)

    def test_samoa_whole_day_skip_exact_time_fails_closed(self) -> None:
        request = self.request(
            self.apia(datetime(2011, 12, 30, 12, 0), TimePrecision.EXACT_SECOND)
        )
        with self.assertRaises(BaziApplicationResolutionError) as caught:
            self.service.resolve(request)
        self.assertEqual("BAZI_APP_NATAL_RESOLUTION_FAILED", caught.exception.code)
        self.assertIn("TIME_CALENDAR_UNRESOLVED", caught.exception.detail)

    def test_samoa_whole_day_skip_nearest_hour_keeps_gap_provenance(self) -> None:
        result = self.service.resolve(
            self.request(
                self.apia(datetime(2011, 12, 30, 23, 30), TimePrecision.NEAREST_HOUR)
            )
        )
        provenance = result.time_calendar_provenance

        self.assertEqual(61, provenance.sample_count)
        self.assertEqual(0, provenance.ambiguous_sample_count)
        self.assertEqual(60, provenance.unresolved_sample_count)
        self.assertEqual(1, provenance.legal_realization_count)
        self.assertEqual(1, len(result.candidates))
        legal = provenance.legal_realizations[0]
        self.assertEqual("2011-12-31T00:00:00", legal.sample_reported_local_datetime)
        self.assertEqual("2011-12-30T10:00:00Z", legal.birth_utc)
        self.assertEqual(14 * 3600, legal.utc_offset_seconds)
        self.assertEqual(3600, legal.daylight_saving_seconds)
        self.assertEqual("PASS", result.integrity.status)

    def test_lord_howe_half_hour_fall_fold_keeps_two_realizations(self) -> None:
        result = self.service.resolve(
            self.request(
                self.lord_howe(datetime(2024, 4, 7, 1, 45), TimePrecision.EXACT_SECOND)
            )
        )
        provenance = result.time_calendar_provenance

        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(1, provenance.sample_count)
        self.assertEqual(1, provenance.ambiguous_sample_count)
        self.assertEqual(2, provenance.legal_realization_count)
        self.assertEqual(0, provenance.unresolved_sample_count)
        self.assertEqual({0, 1}, {row.fold for row in provenance.legal_realizations})
        utc_values = sorted(row.birth_utc for row in provenance.legal_realizations)
        first = datetime.fromisoformat(utc_values[0].replace("Z", "+00:00"))
        second = datetime.fromisoformat(utc_values[1].replace("Z", "+00:00"))
        self.assertEqual(1800, int((second - first).total_seconds()))
        self.assertEqual({39600, 37800}, {row.utc_offset_seconds for row in provenance.legal_realizations})
        self.assertEqual({1800, 0}, {row.daylight_saving_seconds for row in provenance.legal_realizations})
        self.assertEqual(1, len({row.natal_fact_hash for row in result.candidates}))
        self.assertEqual(2, len({row.temporal_fact_hash for row in result.candidates}))
        self.assertEqual("PASS", result.integrity.status)

    def test_lord_howe_half_hour_spring_gap_exact_time_fails_closed(self) -> None:
        request = self.request(
            self.lord_howe(datetime(2024, 10, 6, 2, 15), TimePrecision.EXACT_SECOND)
        )
        with self.assertRaises(BaziApplicationResolutionError) as caught:
            self.service.resolve(request)
        self.assertEqual("BAZI_APP_NATAL_RESOLUTION_FAILED", caught.exception.code)
        self.assertIn("TIME_CALENDAR_UNRESOLVED", caught.exception.detail)

    def test_lord_howe_half_hour_spring_gap_nearest_hour_distribution(self) -> None:
        result = self.service.resolve(
            self.request(
                self.lord_howe(datetime(2024, 10, 6, 2, 15), TimePrecision.NEAREST_HOUR)
            )
        )
        provenance = result.time_calendar_provenance

        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(61, provenance.sample_count)
        self.assertEqual(0, provenance.ambiguous_sample_count)
        self.assertEqual(30, provenance.unresolved_sample_count)
        self.assertEqual(31, provenance.legal_realization_count)
        self.assertEqual(31, len(result.candidates))
        self.assertEqual(
            Counter({37800: 15, 39600: 16}),
            Counter(row.utc_offset_seconds for row in provenance.legal_realizations),
        )
        self.assertEqual(
            Counter({0: 15, 1800: 16}),
            Counter(row.daylight_saving_seconds for row in provenance.legal_realizations),
        )
        self.assertEqual(1, len({row.natal_fact_hash for row in result.candidates}))
        self.assertEqual(31, len({row.temporal_fact_hash for row in result.candidates}))
        self.assertEqual("PASS", result.integrity.status)

    def test_continuous_dayun_leap_day_anniversary_recovers_after_clamp(self) -> None:
        first_transition = datetime(
            2032, 2, 29, 12, 26, 23, 390760, tzinfo=timezone.utc
        )
        year_10 = _dayun_anniversary(first_transition, 10, self.temporal_profile)
        year_20 = _dayun_anniversary(first_transition, 20, self.temporal_profile)
        year_30 = _dayun_anniversary(first_transition, 30, self.temporal_profile)
        year_40 = _dayun_anniversary(first_transition, 40, self.temporal_profile)

        self.assertEqual(
            datetime(2042, 2, 28, 12, 26, 23, 390760, tzinfo=timezone.utc),
            year_10,
        )
        self.assertEqual(
            datetime(2052, 2, 29, 12, 26, 23, 390760, tzinfo=timezone.utc),
            year_20,
        )
        self.assertEqual(
            datetime(2062, 2, 28, 12, 26, 23, 390760, tzinfo=timezone.utc),
            year_30,
        )
        self.assertEqual(
            datetime(2072, 2, 29, 12, 26, 23, 390760, tzinfo=timezone.utc),
            year_40,
        )


if __name__ == "__main__":
    unittest.main()

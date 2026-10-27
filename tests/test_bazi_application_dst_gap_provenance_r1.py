from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationRequest,
    BaziApplicationResolutionError,
    BaziChartService,
    bazi_local_application_v1_profile,
    validate_application_resolution,
)
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import (
    BaziSex,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimePrecision
from fortune_training.calendar_foundation.models import json_value


ROOT = Path(__file__).resolve().parents[1]


class BaziApplicationDstGapProvenanceR1Tests(unittest.TestCase):
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
    def birth(local: datetime, precision: TimePrecision) -> BirthInput:
        return BirthInput(
            reported_local_datetime=local,
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
            precision=precision,
            uncertainty_seconds=0,
        )

    def test_partial_dst_gap_unresolved_samples_are_exported(self):
        request = self.request(
            self.birth(datetime(1991, 4, 14, 2, 0), TimePrecision.NEAREST_HOUR)
        )
        result = self.service.resolve(request)
        provenance = result.time_calendar_provenance

        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(30, len(result.candidates))
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", provenance.status)
        self.assertEqual(1800, provenance.effective_uncertainty_seconds_each_side)
        self.assertEqual(61, provenance.sample_count)
        self.assertEqual(0, provenance.ambiguous_sample_count)
        self.assertEqual(31, provenance.unresolved_sample_count)
        self.assertEqual(31, len(provenance.unresolved_samples))
        self.assertEqual(
            {"NONEXISTENT"},
            {row.civil_status for row in provenance.unresolved_samples},
        )
        self.assertEqual(
            "1991-04-14T02:00:00",
            provenance.unresolved_samples[0].sample_reported_local_datetime,
        )
        self.assertEqual(
            "1991-04-14T02:30:00",
            provenance.unresolved_samples[-1].sample_reported_local_datetime,
        )

        exported = self.service.export(request)
        self.assertEqual(
            json_value(provenance),
            exported["time_calendar_provenance"],
        )
        self.assertEqual("PASS", exported["integrity"]["status"])

    def test_ordinary_nearest_hour_range_reports_zero_unresolved_samples(self):
        request = self.request(
            self.birth(datetime(1994, 5, 17, 14, 30), TimePrecision.NEAREST_HOUR)
        )
        result = self.service.resolve(request)
        provenance = result.time_calendar_provenance

        self.assertEqual(61, provenance.sample_count)
        self.assertEqual(0, provenance.unresolved_sample_count)
        self.assertEqual((), provenance.unresolved_samples)

    def test_fully_nonexistent_exact_time_remains_fail_closed(self):
        request = self.request(
            self.birth(datetime(1991, 4, 14, 2, 30), TimePrecision.EXACT_SECOND)
        )
        with self.assertRaises(BaziApplicationResolutionError) as caught:
            self.service.resolve(request)
        self.assertEqual("BAZI_APP_NATAL_RESOLUTION_FAILED", caught.exception.code)
        self.assertIn("TIME_CALENDAR_UNRESOLVED", caught.exception.detail)

    def test_fall_back_fold_behavior_remains_two_candidates(self):
        request = self.request(
            self.birth(datetime(1991, 9, 15, 1, 30), TimePrecision.EXACT_SECOND)
        )
        result = self.service.resolve(request)
        provenance = result.time_calendar_provenance

        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(2, len(result.candidates))
        self.assertEqual(1, provenance.sample_count)
        self.assertEqual(1, provenance.ambiguous_sample_count)
        self.assertEqual(0, provenance.unresolved_sample_count)

    def test_time_calendar_provenance_is_hash_bound(self):
        request = self.request(
            self.birth(datetime(1991, 4, 14, 2, 0), TimePrecision.NEAREST_HOUR)
        )
        result = self.service.resolve(request)
        changed_provenance = replace(
            result.time_calendar_provenance,
            unresolved_sample_count=0,
        )
        changed = replace(result, time_calendar_provenance=changed_provenance)
        report = validate_application_resolution(changed)

        self.assertEqual("FAIL", report.status)
        self.assertIn(
            "TIME_CALENDAR_UNRESOLVED_SAMPLE_COUNT_MISMATCH",
            report.diagnostics,
        )
        self.assertIn("SOURCE_FACT_HASH_MISMATCH", report.diagnostics)


if __name__ == "__main__":
    unittest.main()

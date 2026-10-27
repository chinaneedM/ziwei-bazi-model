from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationRequest,
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
PRE_1970_WARNING = "IANA tzdb does not guarantee complete pre-1970 historical coverage"


class BaziApplicationResolvedCivilProvenanceR1Tests(unittest.TestCase):
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

    def test_pre_1970_resolved_sample_preserves_reduced_historical_confidence(self):
        request = self.request(
            self.birth(datetime(1965, 1, 15, 12, 0), TimePrecision.EXACT_SECOND)
        )
        result = self.service.resolve(request)
        provenance = result.time_calendar_provenance

        self.assertEqual("RESOLVED", result.status)
        self.assertEqual(1, len(result.candidates))
        self.assertEqual(1, provenance.sample_count)
        self.assertEqual(1, provenance.legal_realization_count)
        self.assertEqual(1, len(provenance.legal_realizations))
        self.assertEqual(0, provenance.unresolved_sample_count)

        realization = provenance.legal_realizations[0]
        self.assertEqual(0, realization.source_time_branch_index)
        self.assertEqual("1965-01-15T12:00:00", realization.sample_reported_local_datetime)
        self.assertEqual("UNIQUE", realization.civil_status)
        self.assertEqual("Asia/Shanghai", realization.timezone_id)
        self.assertTrue(realization.tzdb_version)
        self.assertEqual("TZDB_PRE_1970_REDUCED", realization.historical_confidence)
        self.assertIn(PRE_1970_WARNING, realization.warnings)
        self.assertEqual("1965-01-15T04:00:00Z", realization.birth_utc)
        self.assertEqual(0, realization.fold)
        self.assertEqual(28800, realization.utc_offset_seconds)
        self.assertEqual(0, realization.daylight_saving_seconds)

        lineage = result.candidates[0].view["time_provenance"][0]
        self.assertEqual(0, lineage["source_time_branch_index"])
        self.assertEqual(realization.birth_utc, lineage["birth_utc"])
        self.assertEqual(
            realization.sample_reported_local_datetime,
            lineage["sample_reported_local_datetime"],
        )

        exported = self.service.export(request)
        self.assertEqual(
            json_value(provenance),
            exported["time_calendar_provenance"],
        )
        self.assertEqual("PASS", exported["integrity"]["status"])

    def test_post_1970_resolved_sample_has_post_1970_confidence_without_false_warning(self):
        request = self.request(
            self.birth(datetime(1994, 5, 17, 14, 30), TimePrecision.EXACT_SECOND)
        )
        result = self.service.resolve(request)
        realization = result.time_calendar_provenance.legal_realizations[0]

        self.assertEqual("TZDB_POST_1970", realization.historical_confidence)
        self.assertNotIn(PRE_1970_WARNING, realization.warnings)
        self.assertEqual("UNIQUE", realization.civil_status)

    def test_dst_gap_keeps_legal_and_unresolved_provenance_side_by_side(self):
        request = self.request(
            self.birth(datetime(1991, 4, 14, 2, 0), TimePrecision.NEAREST_HOUR)
        )
        result = self.service.resolve(request)
        provenance = result.time_calendar_provenance

        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(30, len(result.candidates))
        self.assertEqual(30, provenance.legal_realization_count)
        self.assertEqual(31, provenance.unresolved_sample_count)
        self.assertEqual(
            {"UNIQUE"},
            {row.civil_status for row in provenance.legal_realizations},
        )
        self.assertEqual(
            {"NONEXISTENT"},
            {row.civil_status for row in provenance.unresolved_samples},
        )

    def test_fall_back_exact_fold_preserves_both_legal_realizations(self):
        request = self.request(
            self.birth(datetime(1991, 9, 15, 1, 30), TimePrecision.EXACT_SECOND)
        )
        result = self.service.resolve(request)
        provenance = result.time_calendar_provenance

        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(2, len(result.candidates))
        self.assertEqual(1, provenance.sample_count)
        self.assertEqual(1, provenance.ambiguous_sample_count)
        self.assertEqual(2, provenance.legal_realization_count)
        self.assertEqual(
            {"AMBIGUOUS"},
            {row.civil_status for row in provenance.legal_realizations},
        )
        self.assertEqual(
            {0, 1},
            {row.fold for row in provenance.legal_realizations},
        )
        self.assertEqual(
            {"1991-09-14T16:30:00Z", "1991-09-14T17:30:00Z"},
            {row.birth_utc for row in provenance.legal_realizations},
        )
        self.assertEqual(
            {0, 1},
            {
                candidate.view["time_provenance"][0]["source_time_branch_index"]
                for candidate in result.candidates
            },
        )

    def test_fall_back_nearest_hour_preserves_121_realizations(self):
        request = self.request(
            self.birth(datetime(1991, 9, 15, 1, 30), TimePrecision.NEAREST_HOUR)
        )
        result = self.service.resolve(request)
        provenance = result.time_calendar_provenance

        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(121, len(result.candidates))
        self.assertEqual(61, provenance.sample_count)
        self.assertEqual(60, provenance.ambiguous_sample_count)
        self.assertEqual(121, provenance.legal_realization_count)
        self.assertEqual(0, provenance.unresolved_sample_count)
        self.assertEqual(
            set(range(121)),
            {row.source_time_branch_index for row in provenance.legal_realizations},
        )

    def test_legal_realization_provenance_is_hash_bound(self):
        request = self.request(
            self.birth(datetime(1965, 1, 15, 12, 0), TimePrecision.EXACT_SECOND)
        )
        result = self.service.resolve(request)
        original = result.time_calendar_provenance.legal_realizations[0]
        changed_realization = replace(
            original,
            historical_confidence="TAMPERED",
        )
        changed_provenance = replace(
            result.time_calendar_provenance,
            legal_realizations=(changed_realization,),
        )
        changed = replace(result, time_calendar_provenance=changed_provenance)
        report = validate_application_resolution(changed)

        self.assertEqual("FAIL", report.status)
        self.assertIn("SOURCE_FACT_HASH_MISMATCH", report.diagnostics)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import bazi_local_application_v1_profile
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedChartService,
    combined_chart_application_v1_profile,
)
from fortune_training.ziwei_application import (
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class CombinedDstGapFailClosedR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.birth = BirthInput(
            reported_local_datetime=datetime(2020, 3, 8, 2, 30),
            birth_place="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone_id="America/New_York",
        )
        cls.ziwei_calculation_profile = ziwei_chart_engine_v1_profile(registry)
        cls.ziwei_application_profile = ziwei_application_v1_profile()
        cls.ziwei_presentation_profile = (
            ziwei_application_default_presentation_profile()
        )
        cls.bazi_natal_profile = bazi_foundation_v1_profile(registry)
        cls.bazi_temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.bazi_application_profile = bazi_local_application_v1_profile()
        cls.combined_profile = combined_chart_application_v1_profile()
        cls.combined_service = CombinedChartService.from_repository(ROOT)
        cls.request = CombinedChartApplicationRequest(
            birth=cls.birth,
            sex="MALE",
            ziwei_calculation_profile=cls.ziwei_calculation_profile,
            ziwei_application_profile=cls.ziwei_application_profile,
            ziwei_presentation_profile=cls.ziwei_presentation_profile,
            bazi_natal_profile=cls.bazi_natal_profile,
            bazi_temporal_profile=cls.bazi_temporal_profile,
            bazi_application_profile=cls.bazi_application_profile,
            combined_profile=cls.combined_profile,
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )

    def test_dst_gap_preserves_unresolved_civil_time_without_inventing_chart(self):
        ziwei_time = self.combined_service.ziwei_foundation.time_calendar.resolve(
            self.birth,
            self.ziwei_calculation_profile.time_calendar_policies,
        )
        bazi_time = self.combined_service.ziwei_foundation.time_calendar.resolve_bazi(
            self.birth,
            self.bazi_natal_profile.time_calendar_policies,
        )
        for result in (ziwei_time, bazi_time):
            self.assertEqual("UNRESOLVED_CIVIL_TIME", result["status"])
            self.assertEqual([], result["branches"])
            self.assertEqual(1, len(result["unresolved_samples"]))
            civil = result["unresolved_samples"][0]["civil_time"]
            self.assertEqual("NONEXISTENT", civil["status"])
            self.assertEqual([], civil["candidates"])
            self.assertIsNone(civil["selected_candidate"])

        combined = self.combined_service.resolve(self.request)
        self.assertEqual("FAILED", combined.status)
        self.assertEqual("PASS", combined.integrity.status)
        self.assertIsNone(combined.ziwei_bundle)
        self.assertIsNone(combined.bazi_bundle)
        self.assertIsNotNone(combined.ziwei_error)
        self.assertIsNotNone(combined.bazi_error)
        self.assertEqual(
            "COMBINED_ZIWEI_TIME_CALENDAR_UNRESOLVED",
            combined.ziwei_error.code,
        )
        self.assertEqual(
            "BAZI_APP_NATAL_RESOLUTION_FAILED",
            combined.bazi_error.code,
        )

        shared = combined.shared_time_credential
        self.assertEqual(
            {"ziwei": "UNRESOLVED_CIVIL_TIME", "bazi": "UNRESOLVED_CIVIL_TIME"},
            shared["status"],
        )
        self.assertEqual([], shared["realizations"])
        self.assertEqual(1, len(shared["unresolved_samples"]))
        self.assertEqual("NONEXISTENT", shared["unresolved_samples"][0]["civil_status"])
        self.assertEqual(1, shared["input_interval"]["sample_count"])
        self.assertEqual(0, shared["input_interval"]["ambiguous_sample_count"])

        lineage = combined.candidate_lineage
        self.assertEqual(
            "ZIWEI-BAZI-SHARED-TIME-LINEAGE-V1",
            lineage["schema"],
        )
        self.assertEqual([], lineage["branches"])
        self.assertEqual(
            shared["computation_hash"],
            lineage["shared_time_computation_hash"],
        )

        exported = self.combined_service.export(combined)
        self.assertIsNone(exported["ziwei_export"])
        self.assertIsNone(exported["bazi_export"])
        self.assertEqual(
            shared,
            exported["manifest"]["shared_time_credential"],
        )
        self.assertEqual(
            lineage,
            exported["manifest"]["candidate_lineage"],
        )

        replay = self.combined_service.resolve(self.request)
        self.assertEqual(combined.manifest_hash, replay.manifest_hash)
        self.assertEqual(
            shared["computation_hash"],
            replay.shared_time_credential["computation_hash"],
        )
        self.assertEqual(
            lineage["lineage_hash"],
            replay.candidate_lineage["lineage_hash"],
        )


if __name__ == "__main__":
    unittest.main()

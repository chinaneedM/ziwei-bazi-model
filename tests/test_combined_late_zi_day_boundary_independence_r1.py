from __future__ import annotations

import unittest
from datetime import datetime, timedelta
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationRequest,
    BaziChartService,
    bazi_local_application_v1_profile,
)
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import (
    BaziSex,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedChartService,
    combined_chart_application_v1_profile,
)
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    ZiweiChartService,
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class CombinedLateZiDayBoundaryIndependenceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.birth = BirthInput(
            reported_local_datetime=datetime(2008, 11, 3, 22, 50),
            birth_place="Shanghai",
            latitude=31.2304,
            longitude=121.4737,
            timezone_id="Asia/Shanghai",
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
        cls.ziwei_service = ZiweiChartService.from_repository(ROOT)
        cls.bazi_service = BaziChartService.from_repository(ROOT)
        cls.request = CombinedChartApplicationRequest(
            birth=cls.birth,
            sex="MALE",
            ziwei_calculation_profile=cls.ziwei_calculation_profile,
            bazi_natal_profile=cls.bazi_natal_profile,
            bazi_temporal_profile=cls.bazi_temporal_profile,
            combined_profile=cls.combined_profile,
            ziwei_application_profile=cls.ziwei_application_profile,
            ziwei_presentation_profile=cls.ziwei_presentation_profile,
            bazi_application_profile=cls.bazi_application_profile,
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )

    def test_shared_true_solar_late_zi_preserves_independent_day_boundaries(self):
        combined = self.combined_service.resolve(self.request)

        self.assertEqual("RESOLVED_BOTH", combined.status)
        self.assertEqual("PASS", combined.integrity.status)
        policies = combined.shared_time_credential["selected_policies"]
        self.assertEqual("ZI_START_23", policies["ziwei"]["day_boundary_policy"])
        self.assertEqual("MIDNIGHT", policies["bazi"]["bazi_day_boundary_policy"])
        self.assertEqual(
            "CLASSICAL_CONTINUOUS",
            policies["bazi"]["bazi_late_zi_hour_stem_policy"],
        )

        self.assertEqual(1, len(combined.shared_time_credential["realizations"]))
        realization = combined.shared_time_credential["realizations"][0]
        local_solar = datetime.fromisoformat(
            realization["local_apparent_solar_datetime"]
        )
        self.assertEqual(datetime(2008, 11, 3).date(), local_solar.date())
        self.assertEqual((23, 12), (local_solar.hour, local_solar.minute))

        # Ba Zi keeps the same physical realization but does not roll the day at 23:00.
        self.assertEqual("2008-11-03", realization["bazi_effective_day_date"])
        self.assertEqual("丁未", realization["bazi_pillars"][2])
        self.assertEqual(
            "丁未",
            combined.bazi_bundle.candidates[0].view["pillars"][2]["ganzhi"],
        )

        # Zi Wei applies its own 23:00 day boundary to the same local-apparent-solar time.
        expected_lunar = (
            self.combined_service.ziwei_foundation.time_calendar.calendar.from_gregorian_date(
                local_solar.date() + timedelta(days=1)
            )
        )
        ziwei_candidate = combined.ziwei_bundle.candidate
        self.assertEqual(expected_lunar.year, ziwei_candidate.ziwei_birth_year)
        self.assertEqual(
            expected_lunar.month,
            ziwei_candidate.chart.structure.raw_lunar_month,
        )
        self.assertEqual(
            expected_lunar.day,
            ziwei_candidate.chart.structure.lunar_birth_day,
        )
        raw_lunar = realization["effective_ziwei_lunar_date"]
        self.assertNotEqual(
            (
                raw_lunar["year"],
                raw_lunar["month"],
                raw_lunar["day"],
                raw_lunar["is_leap_month"],
            ),
            (
                expected_lunar.year,
                expected_lunar.month,
                expected_lunar.day,
                expected_lunar.is_leap_month,
            ),
        )
        self.assertEqual(
            "LINKED_BOTH",
            combined.candidate_lineage["branches"][0]["status"],
        )

        standalone_ziwei = self.ziwei_service.resolve(
            ApplicationBirthRequest(
                birth=self.birth,
                sex=Sex.MALE,
                calculation_profile=self.ziwei_calculation_profile,
                presentation_profile=self.ziwei_presentation_profile,
                daxian_count=12,
            )
        )
        standalone_bazi = self.bazi_service.resolve(
            BaziApplicationRequest(
                birth=self.birth,
                sex=BaziSex.MALE,
                natal_profile=self.bazi_natal_profile,
                temporal_profile=self.bazi_temporal_profile,
                application_profile=self.bazi_application_profile,
                dayun_count=12,
            )
        )
        self.assertEqual(standalone_ziwei.bundle_hash, combined.ziwei_bundle.bundle_hash)
        self.assertEqual(standalone_bazi.bundle_hash, combined.bazi_bundle.bundle_hash)

        replay = self.combined_service.resolve(self.request)
        self.assertEqual(combined.manifest_hash, replay.manifest_hash)
        self.assertEqual(combined.ziwei_bundle.bundle_hash, replay.ziwei_bundle.bundle_hash)
        self.assertEqual(combined.bazi_bundle.bundle_hash, replay.bazi_bundle.bundle_hash)
        self.assertEqual(
            combined.shared_time_credential["fact_hash"],
            replay.shared_time_credential["fact_hash"],
        )
        self.assertEqual(
            combined.shared_time_credential["computation_hash"],
            replay.shared_time_credential["computation_hash"],
        )


if __name__ == "__main__":
    unittest.main()

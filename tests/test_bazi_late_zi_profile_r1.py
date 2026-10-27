from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application.local_app import (
    LocalAppRequestError,
    LocalBaziApplication,
)
from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    ZI_START_23_PROFILE_ID,
    bazi_foundation_v1_profile,
    bazi_foundation_zi_start_23_r1_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.combined_chart_application.local_app import (
    LocalCombinedAppRequestError,
    LocalCombinedChartApplication,
)


ROOT = Path(__file__).resolve().parents[1]


class BaziLateZiNatalProfileR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.foundation = BaziChartFoundation.from_repository(ROOT)
        cls.old_profile = bazi_foundation_v1_profile(cls.registry)
        cls.zi_start_profile = bazi_foundation_zi_start_23_r1_profile(cls.registry)
        cls.late_zi_birth = BirthInput(
            reported_local_datetime=datetime(2008, 11, 3, 22, 50),
            birth_place="Shanghai",
            latitude=31.2304,
            longitude=121.4737,
            timezone_id="Asia/Shanghai",
        )
        cls.ordinary_birth = BirthInput(
            reported_local_datetime=datetime(1994, 5, 17, 14, 30),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )

    def _single_candidate(self, birth: BirthInput, profile):
        resolution = self.foundation.resolve_typed(BaziChartRequest(birth, profile))
        self.assertEqual("RESOLVED", resolution.status)
        self.assertEqual(1, len(resolution.candidates))
        return resolution.candidates[0]

    @staticmethod
    def _pillars(candidate) -> tuple[str, ...]:
        return tuple(row.ganzhi for row in candidate.chart.pillars)

    def test_profile_policy_snapshots_are_explicit_and_old_profile_is_unchanged(self):
        old = self.old_profile.time_calendar_policies
        new = self.zi_start_profile.time_calendar_policies
        self.assertEqual("BAZI-FOUNDATION-V1-R1", self.old_profile.profile_id)
        self.assertEqual("MIDNIGHT", old.bazi_day_boundary_policy)
        self.assertEqual("CLASSICAL_CONTINUOUS", old.bazi_late_zi_hour_stem_policy)
        self.assertEqual(ZI_START_23_PROFILE_ID, self.zi_start_profile.profile_id)
        self.assertEqual("ZI_START_23", new.bazi_day_boundary_policy)
        self.assertEqual("ZI_START_ROLLOVER", new.bazi_late_zi_hour_stem_policy)
        self.assertEqual(old.bazi_year_boundary_policy, new.bazi_year_boundary_policy)
        self.assertEqual(old.civil_ambiguous_time_policy, new.civil_ambiguous_time_policy)

    def test_shanghai_late_zi_case_forks_only_at_explicit_natal_policy(self):
        old = self._single_candidate(self.late_zi_birth, self.old_profile)
        new = self._single_candidate(self.late_zi_birth, self.zi_start_profile)

        self.assertEqual(("戊子", "壬戌", "丁未", "壬子"), self._pillars(old))
        self.assertEqual(("戊子", "壬戌", "戊申", "壬子"), self._pillars(new))

        old_solar = old.temporal_seeds[0].local_apparent_solar_datetime
        new_solar = new.temporal_seeds[0].local_apparent_solar_datetime
        self.assertEqual(old_solar, new_solar)
        self.assertEqual(23, old_solar.hour)
        self.assertEqual(12, old_solar.minute)

    def test_non_boundary_birth_keeps_same_natal_semantics_under_both_profiles(self):
        old = self._single_candidate(self.ordinary_birth, self.old_profile)
        new = self._single_candidate(self.ordinary_birth, self.zi_start_profile)

        self.assertEqual(self._pillars(old), self._pillars(new))
        self.assertEqual(old.chart.day_master_stem, new.chart.day_master_stem)
        self.assertEqual(old.chart.stems, new.chart.stems)
        self.assertEqual(old.chart.branches, new.chart.branches)
        self.assertEqual(old.chart.hidden_stems, new.chart.hidden_stems)
        self.assertEqual(old.chart.ten_gods, new.chart.ten_gods)
        self.assertEqual(old.chart.exposures, new.chart.exposures)
        self.assertEqual(old.chart.affinities, new.chart.affinities)
        self.assertEqual(old.chart.raw_relations, new.chart.raw_relations)
        self.assertEqual(
            old.temporal_seeds[0].local_apparent_solar_datetime,
            new.temporal_seeds[0].local_apparent_solar_datetime,
        )

    def test_standalone_bazi_app_exposes_both_natal_profiles(self):
        app = LocalBaziApplication(ROOT)
        payload = {
            "birth_datetime": "2008-11-03T22:50",
            "birth_place": "Shanghai",
            "latitude": 31.2304,
            "longitude": 121.4737,
            "timezone_id": "Asia/Shanghai",
            "sex": "MALE",
            "precision": "EXACT_SECOND",
            "uncertainty_seconds": 0,
            "natal_profile_id": "BAZI-FOUNDATION-V1-R1",
            "temporal_profile_id": "BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1",
            "application_profile_id": "BAZI-LOCAL-APPLICATION-V1-R1",
            "dayun_count": 12,
        }

        old = app.resolve_payload(dict(payload))["application_bundle"]
        changed = dict(payload)
        changed["natal_profile_id"] = ZI_START_23_PROFILE_ID
        new = app.resolve_payload(changed)["application_bundle"]

        self.assertEqual("PASS", old["integrity"]["status"])
        self.assertEqual("PASS", new["integrity"]["status"])
        self.assertEqual("BAZI-FOUNDATION-V1-R1", old["natal_profile"]["profile_id"])
        self.assertEqual(ZI_START_23_PROFILE_ID, new["natal_profile"]["profile_id"])
        self.assertEqual("丁未", old["candidates"][0]["view"]["pillars"][2]["ganzhi"])
        self.assertEqual("戊申", new["candidates"][0]["view"]["pillars"][2]["ganzhi"])
        self.assertEqual(
            old["candidates"][0]["view"]["time_provenance"][0]["local_apparent_solar_datetime"],
            new["candidates"][0]["view"]["time_provenance"][0]["local_apparent_solar_datetime"],
        )

        invalid = dict(payload)
        invalid["natal_profile_id"] = "IMPLICIT-DEFAULT"
        with self.assertRaises(LocalAppRequestError):
            app.resolve_payload(invalid)

    def test_combined_shell_preserves_identity_only_composition_for_selected_natal_profile(self):
        app = LocalCombinedChartApplication(ROOT)
        payload = {
            "birth_datetime": "2008-11-03T22:50",
            "birth_place": "Shanghai",
            "latitude": 31.2304,
            "longitude": 121.4737,
            "timezone_id": "Asia/Shanghai",
            "sex": "MALE",
            "precision": "EXACT_SECOND",
            "uncertainty_seconds": 0,
            "ziwei_daxian_count": 12,
            "ziwei_daxian_frame_id": None,
            "ziwei_annual_year": None,
            "ziwei_minor_limit_age": None,
            "bazi_natal_profile_id": ZI_START_23_PROFILE_ID,
            "bazi_temporal_profile_id": "BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1",
            "bazi_dayun_count": 12,
            "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
        }
        response = app.resolve_payload(payload)
        resolution = response["combined_resolution"]
        manifest = response["combined_export"]["manifest"]

        self.assertEqual("RESOLVED_BOTH", resolution["status"])
        self.assertEqual("PASS", resolution["integrity"]["status"])
        self.assertEqual(ZI_START_23_PROFILE_ID, resolution["bazi_natal_profile"]["profile_id"])
        self.assertEqual(
            "戊申",
            resolution["bazi_bundle"]["candidates"][0]["view"]["pillars"][2]["ganzhi"],
        )
        self.assertEqual(ZI_START_23_PROFILE_ID, manifest["profiles"]["bazi_natal"]["profile_id"])
        self.assertEqual(
            resolution["bazi_bundle"]["bundle_hash"],
            manifest["subsystems"]["bazi"]["bundle_hash"],
        )
        self.assertIsNotNone(resolution["ziwei_bundle"])

        metadata = app.profile_metadata()["profiles"]
        self.assertIn("BAZI-FOUNDATION-V1-R1", metadata["bazi_natal_options"])
        self.assertIn(ZI_START_23_PROFILE_ID, metadata["bazi_natal_options"])

        invalid = dict(payload)
        invalid["bazi_natal_profile_id"] = "IMPLICIT-DEFAULT"
        with self.assertRaises(LocalCombinedAppRequestError):
            app.resolve_payload(invalid)


if __name__ == "__main__":
    unittest.main()

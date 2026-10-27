from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.bazi_application.flow_local_app import FlowLocalBaziApplication
from fortune_training.bazi_application.local_app import LocalBaziApplication
from fortune_training.bazi_chart import (
    PRODUCTION_BAZI_PROFILE_ID,
    PRODUCTION_BAZI_PROFILE_VERSION,
    ZI_START_23_PROFILE_ID,
    bazi_foundation_v1_profile,
    bazi_foundation_zi_start_23_r1_profile,
    build_production_bazi_profile,
)
from fortune_training.calendar_foundation import PolicyRegistry
from fortune_training.combined_chart_application.local_app import (
    LocalCombinedChartApplication,
)


ROOT = Path(__file__).resolve().parents[1]


class BaziProductionProfileFreezeR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )

    def test_production_builder_is_exact_legacy_authority_alias(self) -> None:
        self.assertIs(build_production_bazi_profile, bazi_foundation_v1_profile)
        profile = build_production_bazi_profile(self.registry)
        self.assertEqual(PRODUCTION_BAZI_PROFILE_ID, profile.profile_id)
        self.assertEqual(PRODUCTION_BAZI_PROFILE_VERSION, profile.profile_version)
        self.assertEqual("BAZI-FOUNDATION-V1-R1", profile.profile_id)
        self.assertEqual("1.1.0", profile.profile_version)

    def test_production_profile_preserves_every_released_binding(self) -> None:
        profile = build_production_bazi_profile(self.registry).validate(self.registry)
        self.assertEqual("LOCAL_APPARENT_SOLAR", profile.time_coordinate_policy)
        self.assertEqual(
            self.registry.default_bazi_selection(),
            profile.time_calendar_policies,
        )
        self.assertEqual("BAZI-SEXAGENARY-REGISTRY-R1", profile.sexagenary_registry_id)
        self.assertEqual(
            "S11-STANDARD-HIDDEN-STEM-MEMBERSHIP-R1",
            profile.hidden_stem_rule_set_id,
        )
        self.assertEqual("S11-TEN-GOD-RELATION-R1", profile.ten_god_rule_set_id)
        self.assertEqual(
            "BAZI-STEM-BRANCH-AFFINITY-R1", profile.affinity_rule_set_id
        )
        self.assertEqual(
            "BAZI-RAW-RELATION-CLASSICAL-CORE-R1",
            profile.raw_relation_rule_set_id,
        )
        self.assertEqual("BAZI-NATAL-GENERATOR-V1", profile.natal_algorithm_id)

    def test_explicit_late_zi_profile_remains_distinct_and_available(self) -> None:
        production = build_production_bazi_profile(self.registry)
        late_zi = bazi_foundation_zi_start_23_r1_profile(self.registry)
        self.assertEqual(ZI_START_23_PROFILE_ID, late_zi.profile_id)
        self.assertNotEqual(production.profile_id, late_zi.profile_id)
        self.assertEqual("MIDNIGHT", production.time_calendar_policies.bazi_day_boundary_policy)
        self.assertEqual("ZI_START_23", late_zi.time_calendar_policies.bazi_day_boundary_policy)

    def test_product_defaults_resolve_through_production_authority(self) -> None:
        standalone = LocalBaziApplication(ROOT)
        flow = FlowLocalBaziApplication(ROOT)
        combined = LocalCombinedChartApplication(ROOT)
        self.assertEqual(PRODUCTION_BAZI_PROFILE_ID, combined.bazi_natal_profile.profile_id)
        self.assertIs(
            build_production_bazi_profile,
            combined.bazi_natal_profiles[PRODUCTION_BAZI_PROFILE_ID],
        )
        self.assertEqual("ok", standalone.health()["status"])
        self.assertEqual("ok", flow.health()["status"])
        self.assertIn(ZI_START_23_PROFILE_ID, combined.bazi_natal_profiles)


if __name__ == "__main__":
    unittest.main()

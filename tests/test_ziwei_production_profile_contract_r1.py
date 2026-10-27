from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.calendar_foundation import PolicyRegistry
from fortune_training.ziwei_chart import (
    OPERATIONAL_ZIWEI_V1_PROFILE_ID,
    OPERATIONAL_ZIWEI_V1_PROFILE_VERSION,
    PRODUCTION_ZIWEI_PROFILE_ID,
    PRODUCTION_ZIWEI_PROFILE_VERSION,
    ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
    ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
    build_operational_ziwei_v1_profile,
    build_production_ziwei_profile,
    ziwei_chart_engine_v1_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiProductionProfileContractR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )

    def test_all_public_names_resolve_to_one_frozen_identity(self) -> None:
        self.assertEqual(
            {
                ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
                PRODUCTION_ZIWEI_PROFILE_ID,
                OPERATIONAL_ZIWEI_V1_PROFILE_ID,
            },
            {"ZIWEI-CHART-ENGINE-V1"},
        )
        self.assertEqual(
            {
                ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
                PRODUCTION_ZIWEI_PROFILE_VERSION,
                OPERATIONAL_ZIWEI_V1_PROFILE_VERSION,
            },
            {"1.0.0"},
        )

    def test_legacy_and_operational_builders_are_exact_authority_aliases(self) -> None:
        self.assertIs(ziwei_chart_engine_v1_profile, build_production_ziwei_profile)
        self.assertIs(build_operational_ziwei_v1_profile, build_production_ziwei_profile)
        self.assertEqual(
            ziwei_chart_engine_v1_profile(self.registry),
            build_production_ziwei_profile(self.registry),
        )

    def test_production_authority_preserves_every_frozen_v1_binding(self) -> None:
        profile = build_production_ziwei_profile(self.registry)
        self.assertEqual("ZI_START_23", profile.ziwei_day_boundary_policy)
        self.assertEqual("ZI_START_23", profile.time_calendar_policies.bazi_day_boundary_policy)
        self.assertEqual(
            "ZI_START_ROLLOVER",
            profile.time_calendar_policies.bazi_late_zi_hour_stem_policy,
        )
        self.assertEqual(
            "ZHONGZHOU_FIXED_15",
            profile.time_calendar_policies.ziwei_life_body_leap_month_policy,
        )
        self.assertEqual("WENMO_DEFAULT_CORE_AUX_R1", profile.auxiliary_rule_set_id)
        self.assertEqual("WENMO_DEFAULT_MINOR_R1", profile.minor_rule_set_id)
        self.assertEqual("2.0.0", profile.minor_rule_set_version)
        self.assertEqual("OPERATIONAL-ZIWEI-DIGNITY-R4", profile.dignity_rule_set_id)
        self.assertEqual("S08_CURRENT_40_ASSIGNMENT_R1", profile.transformation_rule_set_id)
        self.assertEqual("S10_CURRENT_TEMPORAL_R1", profile.temporal_rule_set_id)
        self.assertEqual("WENMO_DEFAULT_RING_R1", profile.ring_rule_set_id)
        self.assertEqual("WENMO_DEFAULT_ROLE_R1", profile.role_rule_set_id)


if __name__ == "__main__":
    unittest.main()

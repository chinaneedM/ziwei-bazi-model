from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import (
    ResolvedZiweiCalculationProfile,
    Sex,
    ZiweiChartFoundation,
    ZiweiChartRequest,
)
from fortune_training.ziwei_chart.main_stars import MainStarGenerator
from fortune_training.ziwei_chart.natal import NatalStructureGenerator, NatalStructureInput


ROOT = Path(__file__).resolve().parents[1]


class ZiweiNatalStructureTests(unittest.TestCase):
    def test_life_body_geometry_for_all_month_hour_pairs(self):
        generator = NatalStructureGenerator()
        for month in range(1, 13):
            for hour_index in range(12):
                hour = 23 if hour_index == 0 else 2 * hour_index - 1
                result = generator.generate(
                    NatalStructureInput(
                        lunar_year=1984,
                        lunar_month=month,
                        lunar_day=1,
                        is_leap_month=False,
                        lunar_month_length_days=30,
                        local_apparent_solar_datetime=datetime(1984, 2, 2, hour, 30),
                        life_body_leap_month_policy="FULLBOOK_NEXT_MONTH",
                    )
                )
                expected_anchor = (2 + month - 1) % 12
                self.assertEqual(expected_anchor, result.month_anchor.index)
                self.assertEqual((expected_anchor - hour_index) % 12, result.life_address.index)
                self.assertEqual((expected_anchor + hour_index) % 12, result.body_address.index)

    def test_zi_hour_life_and_body_equal_month_anchor(self):
        result = NatalStructureGenerator().generate(
            NatalStructureInput(
                lunar_year=1984,
                lunar_month=1,
                lunar_day=1,
                is_leap_month=False,
                lunar_month_length_days=30,
                local_apparent_solar_datetime=datetime(1984, 2, 2, 23, 30),
                life_body_leap_month_policy="FULLBOOK_NEXT_MONTH",
            )
        )
        self.assertEqual(result.month_anchor, result.life_address)
        self.assertEqual(result.month_anchor, result.body_address)

    def test_jia_year_life_in_yin_derives_fire_six_bureau(self):
        result = NatalStructureGenerator().generate(
            NatalStructureInput(
                lunar_year=1984,
                lunar_month=1,
                lunar_day=1,
                is_leap_month=False,
                lunar_month_length_days=30,
                local_apparent_solar_datetime=datetime(1984, 2, 2, 23, 30),
                life_body_leap_month_policy="FULLBOOK_NEXT_MONTH",
            )
        )
        self.assertEqual("甲", result.ziwei_birth_year_stem)
        self.assertEqual("寅", result.life_address.branch)
        self.assertEqual("丙", result.address_attributes[result.life_address.index].stem)
        self.assertEqual("丙寅", result.bureau.life_palace_ganzhi)
        self.assertEqual("炉中火", result.bureau.nayin_name)
        self.assertEqual(("火", 6), (result.bureau.element, result.bureau.number))

    def test_leap_month_policy_is_scoped_to_natal_month_coordinate(self):
        common = dict(
            lunar_year=2020,
            lunar_month=4,
            lunar_day=1,
            is_leap_month=True,
            lunar_month_length_days=29,
            local_apparent_solar_datetime=datetime(2020, 5, 23, 12, 0),
        )
        current = NatalStructureGenerator().generate(
            NatalStructureInput(**common, life_body_leap_month_policy="CURRENT_MONTH")
        )
        next_month = NatalStructureGenerator().generate(
            NatalStructureInput(**common, life_body_leap_month_policy="FULLBOOK_NEXT_MONTH")
        )
        self.assertEqual(4, current.raw_lunar_month)
        self.assertEqual(4, current.natal_month_coordinate)
        self.assertEqual(4, next_month.raw_lunar_month)
        self.assertEqual(5, next_month.natal_month_coordinate)


class ZiweiMainStarTests(unittest.TestCase):
    def test_fire_six_day_one_ziwei_is_you(self):
        self.assertEqual(9, MainStarGenerator.ziwei_anchor(1, 6))

    def test_tianfu_is_diameter_reflection_of_ziwei(self):
        for ziwei in range(12):
            tianfu = MainStarGenerator.tianfu_anchor(ziwei)
            self.assertEqual((4 - ziwei) % 12, tianfu)

    def test_main_star_configuration_covaries_under_half_turn(self):
        generator = MainStarGenerator()
        for ziwei in range(6):
            first = {
                row.entity_id: row.address.index
                for row in generator.generate_from_ziwei_anchor(ziwei)
            }
            second = {
                row.entity_id: row.address.index
                for row in generator.generate_from_ziwei_anchor(ziwei + 6)
            }
            self.assertEqual(
                {entity: (index + 6) % 12 for entity, index in first.items()},
                second,
            )


class ZiweiChartIntegrationTests(unittest.TestCase):
    def test_beijing_smoke_chart_resolves_to_structure_and_fourteen_main_stars(self):
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        profile = ResolvedZiweiCalculationProfile(
            profile_id="FOUNDATION-SMOKE-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=registry.version,
            time_calendar_policies=registry.default_selection(),
        )
        engine = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        result = engine.resolve(
            ZiweiChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4074,
                    timezone_id="Asia/Shanghai",
                ),
                sex=Sex.MALE,
                profile=profile,
            )
        )
        self.assertEqual("RESOLVED", result["status"])
        self.assertEqual(1, len(result["charts"]))
        chart = result["charts"][0]
        self.assertEqual(12, len(chart["structure"]["designation_bindings"]))
        self.assertEqual(14, len(chart["placements"]))
        self.assertEqual(14, len({row["entity_id"] for row in chart["placements"]}))

    def test_profile_registry_version_mismatch_fails_closed(self):
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        profile = ResolvedZiweiCalculationProfile(
            profile_id="BROKEN-PROFILE",
            profile_version="1.0.0",
            time_calendar_policy_registry_version="WRONG",
            time_calendar_policies=registry.default_selection(),
        )
        with self.assertRaisesRegex(ValueError, "registry version mismatch"):
            profile.validate(registry)


if __name__ == "__main__":
    unittest.main()

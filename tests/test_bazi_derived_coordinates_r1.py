from __future__ import annotations

import unittest

from fortune_training.bazi_application import (
    DERIVED_COORDINATE_PROFILE_ID,
    derived_coordinates_for_pillars,
    minggong_from_pillars,
    shengong_from_pillars,
    taiyuan_from_month_pillar,
    validate_derived_coordinate_profile,
)
from fortune_training.bazi_chart.registries import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    SEXAGENARY_CYCLE,
    sexagenary_index,
)


class BaziDerivedCoordinatesR1Tests(unittest.TestCase):
    def test_yuanhai_ziping_taiyuan_example_replays_exactly(self) -> None:
        row = taiyuan_from_month_pillar("己巳")
        self.assertEqual("庚申", row["ganzhi"])
        self.assertEqual(SEXAGENARY_CYCLE.index("庚申"), row["sexagenary_index"])
        self.assertEqual(1, row["basis"]["stem_offset"])
        self.assertEqual(3, row["basis"]["branch_offset"])
        self.assertEqual("PRESERVED_NOT_SELECTED", row["alternative_profiles"][0]["status"])

    def test_all_sixty_month_pillars_produce_legal_taiyuan_identity(self) -> None:
        for month_ganzhi in SEXAGENARY_CYCLE:
            with self.subTest(month_ganzhi=month_ganzhi):
                row = taiyuan_from_month_pillar(month_ganzhi)
                self.assertEqual(row["sexagenary_index"], sexagenary_index(row["ganzhi"]))
                self.assertEqual(
                    (HEAVENLY_STEMS.index(month_ganzhi[0]) + 1) % 10,
                    HEAVENLY_STEMS.index(row["stem"]),
                )
                self.assertEqual(
                    (EARTHLY_BRANCHES.index(month_ganzhi[1]) + 3) % 12,
                    EARTHLY_BRANCHES.index(row["branch"]),
                )

    def test_sanming_tonghui_minggong_example_replays_exactly(self) -> None:
        row = minggong_from_pillars("甲子", "戊辰", "甲戌")
        self.assertEqual("丁卯", row["ganzhi"])
        self.assertEqual("戌", row["basis"]["month_anchor_branch"])
        self.assertEqual("卯", row["basis"]["target_branch"])

    def test_shengong_uses_same_birth_coordinate_but_you_target(self) -> None:
        life = minggong_from_pillars("甲子", "戊辰", "甲戌")
        body = shengong_from_pillars("甲子", "戊辰", "甲戌")
        self.assertEqual("卯", life["basis"]["target_branch"])
        self.assertEqual("酉", body["basis"]["target_branch"])
        self.assertEqual("癸酉", body["ganzhi"])

    def test_every_legal_year_month_hour_combination_closes_in_cycle(self) -> None:
        for year in SEXAGENARY_CYCLE[::5]:
            for month in SEXAGENARY_CYCLE[::5]:
                for hour in SEXAGENARY_CYCLE[::5]:
                    with self.subTest(year=year, month=month, hour=hour):
                        rows = derived_coordinates_for_pillars(year, month, hour)
                        self.assertEqual(DERIVED_COORDINATE_PROFILE_ID, rows["profile_id"])
                        for key in ("taiyuan", "minggong", "shengong"):
                            self.assertEqual(
                                rows[key]["sexagenary_index"],
                                sexagenary_index(rows[key]["ganzhi"]),
                            )
                            self.assertEqual(
                                "DERIVED_COORDINATE_IDENTITY_ONLY_NO_INTERPRETATION",
                                rows[key]["semantic_scope"],
                            )

    def test_invalid_inputs_fail_closed(self) -> None:
        validate_derived_coordinate_profile()
        with self.assertRaises(ValueError):
            taiyuan_from_month_pillar("甲")
        with self.assertRaises(ValueError):
            minggong_from_pillars("甲子", "甲丑", "BAD")


if __name__ == "__main__":
    unittest.main()

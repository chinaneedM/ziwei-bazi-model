from __future__ import annotations

import unittest

from fortune_training.bazi_application import (
    FIXED_SEX_PROFILE_ID,
    HOUR_PILLAR_PROFILE_ID,
    fixed_sex_xiaoyun,
    hour_pillar_xiaoyun,
    validate_xiaoyun_profiles,
    xiaoyun_candidates,
)
from fortune_training.bazi_chart.registries import SEXAGENARY_CYCLE, sexagenary_index
from fortune_training.bazi_temporal import BaziSex


class BaziXiaoyunCandidatesR1Tests(unittest.TestCase):
    def test_hour_pillar_source_example_replays_exactly(self) -> None:
        row = hour_pillar_xiaoyun("甲子", "甲子", BaziSex.MALE, count=3)
        self.assertEqual(HOUR_PILLAR_PROFILE_ID, row["profile_id"])
        self.assertEqual("FORWARD", row["direction"])
        self.assertEqual(["乙丑", "丙寅", "丁卯"], [x["ganzhi"] for x in row["frames"]])

    def test_hour_pillar_direction_uses_year_polarity_and_sex(self) -> None:
        cases = (
            ("甲子", BaziSex.MALE, "FORWARD", "乙丑"),
            ("甲子", BaziSex.FEMALE, "REVERSE", "癸亥"),
            ("乙丑", BaziSex.MALE, "REVERSE", "癸亥"),
            ("乙丑", BaziSex.FEMALE, "FORWARD", "乙丑"),
        )
        for year, sex, direction, first in cases:
            with self.subTest(year=year, sex=sex):
                row = hour_pillar_xiaoyun(year, "甲子", sex, count=1)
                self.assertEqual(direction, row["direction"])
                self.assertEqual(first, row["frames"][0]["ganzhi"])

    def test_fixed_sex_alternative_replays_both_source_starts(self) -> None:
        male = fixed_sex_xiaoyun(BaziSex.MALE, count=2)
        female = fixed_sex_xiaoyun(BaziSex.FEMALE, count=2)
        self.assertEqual(FIXED_SEX_PROFILE_ID, male["profile_id"])
        self.assertEqual(["丙寅", "丁卯"], [x["ganzhi"] for x in male["frames"]])
        self.assertEqual(["壬申", "辛未"], [x["ganzhi"] for x in female["frames"]])

    def test_alternatives_are_preserved_without_silent_selection(self) -> None:
        result = xiaoyun_candidates("甲子", "甲子", BaziSex.MALE, count=60)
        self.assertEqual("UNRESOLVED_CLASSICAL_ALTERNATIVES", result["selection_status"])
        self.assertEqual(2, len(result["candidates"]))
        self.assertTrue(all(row["status"] == "CANDIDATE_NOT_ARBITRATED" for row in result["candidates"]))
        for candidate in result["candidates"]:
            self.assertEqual(60, len(candidate["frames"]))
            for frame in candidate["frames"]:
                self.assertEqual(frame["sexagenary_index"], sexagenary_index(frame["ganzhi"]))
                self.assertIn(frame["ganzhi"], SEXAGENARY_CYCLE)

    def test_invalid_inputs_fail_closed(self) -> None:
        validate_xiaoyun_profiles()
        with self.assertRaises(ValueError):
            hour_pillar_xiaoyun("BAD", "甲子", BaziSex.MALE, count=1)
        with self.assertRaises(ValueError):
            fixed_sex_xiaoyun(BaziSex.MALE, count=0)


if __name__ == "__main__":
    unittest.main()

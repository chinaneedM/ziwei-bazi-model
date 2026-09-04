from __future__ import annotations

import unittest

from fortune_training.bazi_application import (
    TWELVE_GROWTH_PHASES,
    TWELVE_GROWTH_START_BRANCH,
    twelve_growth_for,
    validate_classical_annotation_registries,
    xunkong_for_ganzhi,
    xunkong_for_sexagenary_index,
)
from fortune_training.bazi_chart.registries import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    SEXAGENARY_CYCLE,
    STEM_POLARITY,
)


class BaziClassicalAnnotationsR1Tests(unittest.TestCase):
    def test_six_xun_table_matches_yuanhai_ziping_source_table(self) -> None:
        expected = (
            ("甲子", ["戌", "亥"]),
            ("甲戌", ["申", "酉"]),
            ("甲申", ["午", "未"]),
            ("甲午", ["辰", "巳"]),
            ("甲辰", ["寅", "卯"]),
            ("甲寅", ["子", "丑"]),
        )
        actual = tuple(
            (
                xunkong_for_sexagenary_index(index)["xun_start_ganzhi"],
                xunkong_for_sexagenary_index(index)["void_branches"],
            )
            for index in range(0, 60, 10)
        )
        self.assertEqual(expected, actual)

    def test_all_sixty_identities_keep_their_xun_void_pair(self) -> None:
        for index, ganzhi in enumerate(SEXAGENARY_CYCLE):
            with self.subTest(index=index, ganzhi=ganzhi):
                row = xunkong_for_ganzhi(ganzhi)
                self.assertEqual(index // 10, row["xun_index"])
                self.assertEqual(2, len(row["void_branches"]))
                self.assertEqual(
                    row,
                    xunkong_for_sexagenary_index(index),
                )
                self.assertEqual(
                    "IDENTITY_ONLY_NO_AUSPICIOUSNESS",
                    row["semantic_scope"],
                )

    def test_twelve_growth_covers_every_stem_branch_cell(self) -> None:
        self.assertEqual(tuple(TWELVE_GROWTH_START_BRANCH), HEAVENLY_STEMS)
        for stem in HEAVENLY_STEMS:
            rows = [twelve_growth_for(stem, branch) for branch in EARTHLY_BRANCHES]
            with self.subTest(stem=stem):
                self.assertEqual({row["phase"] for row in rows}, set(TWELVE_GROWTH_PHASES))
                start = twelve_growth_for(stem, TWELVE_GROWTH_START_BRANCH[stem])
                self.assertEqual("长生", start["phase"])
                self.assertEqual(
                    "FORWARD" if STEM_POLARITY[stem] == "YANG" else "REVERSE",
                    start["direction"],
                )
                self.assertEqual(
                    "PHASE_IDENTITY_ONLY_NO_STRENGTH_CONCLUSION",
                    start["semantic_scope"],
                )
                self.assertEqual("1.0.1", start["profile_version"])
                self.assertIn("S11:YHZP-CH-015", start["source_refs"])
                self.assertNotIn("S12:YHZP-CH-016", start["source_refs"])

    def test_registry_integrity_and_invalid_inputs_fail_closed(self) -> None:
        validate_classical_annotation_registries()
        with self.assertRaises(ValueError):
            xunkong_for_sexagenary_index(60)
        with self.assertRaises(ValueError):
            twelve_growth_for("A", "子")
        with self.assertRaises(ValueError):
            twelve_growth_for("甲", "A")


if __name__ == "__main__":
    unittest.main()

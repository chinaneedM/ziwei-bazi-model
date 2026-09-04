from __future__ import annotations

import unittest

from fortune_training.ziwei_chart.auxiliary import (
    KUI_YUE_BY_STEM,
    WENMO_FIRE_BELL_BY_YEAR_BRANCH,
    WENMO_KUI_YUE_BY_STEM,
)
from fortune_training.ziwei_chart.historical_candidates import (
    JIELAN_1581_CHANGSHENG_ANCHOR_BY_ELEMENT,
    JIELAN_1581_DIGNITY_SOURCE_STATUS,
    JIELAN_1581_FIRE_BELL_START_BY_YEAR_BRANCH,
    JIELAN_1581_FOUR_TRANSFORMATIONS,
    JIELAN_1581_KUI_YUE_BY_STEM,
    JIELAN_1581_SELECTION_STATUS,
    JIELAN_1581_TIANSHANG_TIANSHI_OFFSETS,
    historical_candidate_hash,
    validate_historical_candidate_registry,
)
from fortune_training.ziwei_chart.rings import CHANGSHENG_ANCHOR_BY_ELEMENT
from fortune_training.ziwei_chart.transformations import ASSIGNMENTS_BY_STEM


class ZiweiJielan1581HistoricalCandidatesR1Test(unittest.TestCase):
    def test_registry_is_valid_and_not_selected(self) -> None:
        validate_historical_candidate_registry()
        self.assertEqual(JIELAN_1581_SELECTION_STATUS, "PRESERVED_NOT_SELECTED")
        self.assertEqual(len(historical_candidate_hash()), 64)
        self.assertEqual(
            JIELAN_1581_DIGNITY_SOURCE_STATUS,
            "SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING",
        )

    def test_1581_four_transformations_exactly_match_current_s08_table(self) -> None:
        current = {
            stem: tuple(row.target_display_name for row in rows)
            for stem, rows in ASSIGNMENTS_BY_STEM.items()
        }
        self.assertEqual(JIELAN_1581_FOUR_TRANSFORMATIONS, current)

    def test_1581_kui_yue_preserves_early_geng_variant(self) -> None:
        self.assertEqual(JIELAN_1581_KUI_YUE_BY_STEM["庚"], ("午", "寅"))
        self.assertEqual(KUI_YUE_BY_STEM["庚"], ("丑", "未"))
        # All non-Geng stems except Wenmo's separate Xin ordering agree with
        # their expected families; the important point is that Jielan is not
        # silently collapsed into either current production table.
        self.assertNotEqual(JIELAN_1581_KUI_YUE_BY_STEM, KUI_YUE_BY_STEM)
        self.assertNotEqual(JIELAN_1581_KUI_YUE_BY_STEM, WENMO_KUI_YUE_BY_STEM)

    def test_1581_fire_bell_diff_is_real_and_scoped(self) -> None:
        current = {
            branch: (row[0], row[1])
            for branch, row in WENMO_FIRE_BELL_BY_YEAR_BRANCH.items()
        }
        differing = {
            branch
            for branch in current
            if current[branch] != JIELAN_1581_FIRE_BELL_START_BY_YEAR_BRANCH[branch]
        }
        self.assertEqual(differing, {"巳", "酉", "丑"})
        for branch in ("巳", "酉", "丑"):
            self.assertEqual(
                JIELAN_1581_FIRE_BELL_START_BY_YEAR_BRANCH[branch],
                ("戌", "卯"),
            )
            self.assertEqual(current[branch], ("卯", "戌"))

    def test_1581_tianshang_tianshi_matches_fixed_r4_geometry(self) -> None:
        self.assertEqual(
            JIELAN_1581_TIANSHANG_TIANSHI_OFFSETS,
            {"STAR.TIANSHANG": 5, "STAR.TIANSHI": 7},
        )

    def test_1581_changsheng_ring_matches_current_anchor_table(self) -> None:
        self.assertEqual(
            JIELAN_1581_CHANGSHENG_ANCHOR_BY_ELEMENT,
            CHANGSHENG_ANCHOR_BY_ELEMENT,
        )


if __name__ == "__main__":
    unittest.main()

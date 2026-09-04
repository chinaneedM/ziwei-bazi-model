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
    JIELAN_1581_MINGZHU_BASIS,
    JIELAN_1581_MINGZHU_BY_BIRTH_YEAR_BRANCH,
    JIELAN_1581_SHENZHU_BASIS,
    JIELAN_1581_SHENZHU_ZI_WU_STATUS,
    JIELAN_1581_DAXIAN_RULE,
    JIELAN_1581_MINOR_LIMIT_START_BY_YEAR_BRANCH,
    JIELAN_1581_MINOR_LIMIT_DIRECTION,
    JIELAN_1581_BOSHI_MEMBERS,
    JIELAN_1581_SELECTION_STATUS,
    JIELAN_1581_TIANSHANG_TIANSHI_OFFSETS,
    historical_candidate_hash,
    validate_historical_candidate_registry,
)
from fortune_training.ziwei_chart.rings import (
    BOSHI_MEMBERS,
    CHANGSHENG_ANCHOR_BY_ELEMENT,
)
from fortune_training.ziwei_chart.roles import MINGZHU_BY_LIFE_BRANCH
from fortune_training.ziwei_chart.temporal import MINOR_AGE_ONE_START_BY_YEAR_BRANCH
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


    def test_1581_mingzhu_preserves_birth_year_basis_variant(self) -> None:
        self.assertEqual(JIELAN_1581_MINGZHU_BASIS, "ZIWEI_BIRTH_YEAR_BRANCH")
        current_values = {
            branch: display_name
            for branch, (_entity_id, display_name) in MINGZHU_BY_LIFE_BRANCH.items()
        }
        self.assertEqual(JIELAN_1581_MINGZHU_BY_BIRTH_YEAR_BRANCH, current_values)
        # Same lookup table, materially different key/basis from current Fullbook production.
        self.assertNotEqual(JIELAN_1581_MINGZHU_BASIS, "LIFE_PALACE_BRANCH")

    def test_1581_shenzhu_keeps_birth_year_basis_and_zi_wu_ambiguity(self) -> None:
        self.assertEqual(JIELAN_1581_SHENZHU_BASIS, "ZIWEI_BIRTH_YEAR_BRANCH")
        self.assertEqual(
            JIELAN_1581_SHENZHU_ZI_WU_STATUS,
            "TEXTUAL_COMPOSITE_FIRE_BELL_NOT_UNIQUELY_ARBITRATED",
        )

    def test_1581_daxian_matches_current_core_geometry(self) -> None:
        self.assertEqual(JIELAN_1581_DAXIAN_RULE["first_active_address"], "LIFE_PALACE")
        self.assertEqual(JIELAN_1581_DAXIAN_RULE["first_nominal_age"], "BUREAU_NUMBER")
        self.assertEqual(JIELAN_1581_DAXIAN_RULE["step_years"], 10)
        self.assertEqual(JIELAN_1581_DAXIAN_RULE["step_addresses"], 1)

    def test_1581_minor_limit_matches_current_start_table_and_direction(self) -> None:
        self.assertEqual(
            JIELAN_1581_MINOR_LIMIT_START_BY_YEAR_BRANCH,
            MINOR_AGE_ONE_START_BY_YEAR_BRANCH,
        )
        self.assertEqual(
            JIELAN_1581_MINOR_LIMIT_DIRECTION,
            {"MALE": "FORWARD", "FEMALE": "REVERSE"},
        )

    def test_1581_boshi_ring_matches_current_member_order(self) -> None:
        current = tuple(display_name for _member_id, display_name in BOSHI_MEMBERS)
        self.assertEqual(JIELAN_1581_BOSHI_MEMBERS, current)

if __name__ == "__main__":
    unittest.main()

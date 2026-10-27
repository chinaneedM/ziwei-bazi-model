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
    JIELAN_1581_RUNTIME_RESOLVER_ID,
    JIELAN_1581_RUNTIME_RESOLVER_VERSION,
    JIELAN_1581_BOSHI_MEMBERS,
    JIELAN_1581_SELECTION_STATUS,
    JIELAN_1581_TIANSHANG_TIANSHI_OFFSETS,
    historical_candidate_hash,
    resolve_jielan_1581_source_scoped_candidate,
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

    def test_source_scoped_runtime_resolves_replayable_1581_facts_without_selecting(self) -> None:
        resolved = resolve_jielan_1581_source_scoped_candidate(
            year_stem="庚",
            year_branch="巳",
            birth_hour_branch="午",
            life_palace_branch="寅",
            bureau_element="木",
            sex="MALE",
        )
        self.assertEqual(resolved["selection_status"], "PRESERVED_NOT_SELECTED")
        self.assertEqual(resolved["runtime_resolver_id"], JIELAN_1581_RUNTIME_RESOLVER_ID)
        self.assertEqual(resolved["runtime_resolver_version"], JIELAN_1581_RUNTIME_RESOLVER_VERSION)
        self.assertEqual(len(resolved["runtime_hash"]), 64)
        facts = resolved["facts"]
        self.assertEqual(facts["kui_yue"]["branches"], ("午", "寅"))
        self.assertEqual(facts["fire_bell"]["start_branches"], ("戌", "卯"))
        self.assertEqual(facts["fire_bell"]["resolved_branches"], ("辰", "酉"))
        self.assertEqual(
            facts["tianshang_tianshi"]["resolved_branches"],
            {"STAR.TIANSHANG": "未", "STAR.TIANSHI": "酉"},
        )
        self.assertEqual(facts["changsheng"]["direction"], "FORWARD")
        self.assertEqual(facts["mingzhu"]["basis"], "ZIWEI_BIRTH_YEAR_BRANCH")
        self.assertEqual(facts["mingzhu"]["display_name"], "武曲")
        self.assertFalse(facts["shenzhu"]["winner_selected"])
        self.assertEqual(facts["daxian"]["direction"], "FORWARD")
        self.assertEqual(facts["minor_limit"]["age_one_start_branch"], "未")
        self.assertEqual(facts["minor_limit"]["direction"], "FORWARD")
        self.assertEqual(facts["boshi"]["anchor_branch"], "申")
        self.assertEqual(facts["boshi"]["members"][0]["display_name"], "博士")
        self.assertEqual(facts["boshi"]["members"][0]["branch"], "申")
        self.assertFalse(facts["dignity"]["runtime_normalized"])

    def test_source_scoped_runtime_is_deterministic_and_fail_closed(self) -> None:
        kwargs = dict(
            year_stem="辛", year_branch="子", birth_hour_branch="子",
            life_palace_branch="午", bureau_element="金", sex="FEMALE",
        )
        first = resolve_jielan_1581_source_scoped_candidate(**kwargs)
        second = resolve_jielan_1581_source_scoped_candidate(**kwargs)
        self.assertEqual(first["runtime_hash"], second["runtime_hash"])
        with self.assertRaises(ValueError):
            resolve_jielan_1581_source_scoped_candidate(**{**kwargs, "sex": "UNKNOWN"})
        with self.assertRaises(ValueError):
            resolve_jielan_1581_source_scoped_candidate(**{**kwargs, "bureau_element": "风"})
if __name__ == "__main__":
    unittest.main()

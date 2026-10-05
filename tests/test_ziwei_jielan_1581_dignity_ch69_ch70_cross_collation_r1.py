from __future__ import annotations

import unittest

from fortune_training.ziwei_chart.dignity_historical_cross_collation import (
    JIELAN_1581_DIGNITY_CROSS_COLLATION_STATUS,
    jielan_1581_dignity_ch69_ch70_cross_collation_payload,
    resolve_jielan_1581_dignity_ch69_ch70_cross_collation,
)


class Jielan1581DignityCh69Ch70CrossCollationTest(unittest.TestCase):
    def test_full_grid_and_relation_accounting_are_frozen(self) -> None:
        payload = jielan_1581_dignity_ch69_ch70_cross_collation_payload()
        self.assertEqual(25, payload["entity_count"])
        self.assertEqual(300, payload["cell_count"])
        self.assertEqual(
            "CELL_LEVEL_CROSS_COLLATION_COMPLETE_NO_GRADE_COERCION",
            JIELAN_1581_DIGNITY_CROSS_COLLATION_STATUS,
        )
        self.assertEqual(
            {
                "EXACT_LEXEME_OVERLAP": 97,
                "SOURCE_EXPLICIT_EQUIVALENT": 37,
                "SOURCE_LOCAL_POLARITY_CONFLICT": 54,
                "ATTESTED_NON_EQUIVALENT_NO_DIRECT_GLOSS": 21,
                "CH69_UNSTATED": 82,
                "CH69_TEXT_UNRESOLVED": 8,
                "CH70_UNSTATED": 1,
            },
            payload["relation_counts"],
        )
        self.assertEqual(8, payload["ch69_unresolved_cell_count"])
        self.assertEqual(2, payload["ch70_source_conflict_cell_count"])
        self.assertEqual(1, payload["ch70_unstated_cell_count"])

    def test_ch70_conflicts_remain_conflicts_even_when_ch69_overlaps_one_lexeme(self) -> None:
        payload = jielan_1581_dignity_ch69_ch70_cross_collation_payload()
        ziwei_wu = next(
            row for row in payload["rows"]
            if row["display_name"] == "紫微" and row["branch"] == "午"
        )
        self.assertEqual(("庙",), ziwei_wu["ch69_source_lexemes"])
        self.assertEqual(("庙", "平"), ziwei_wu["ch70_source_lexemes"])
        self.assertTrue(ziwei_wu["ch70_source_conflict"])
        self.assertEqual("EXACT_LEXEME_OVERLAP", ziwei_wu["relation"])

        jumen_chou = next(
            row for row in payload["rows"]
            if row["display_name"] == "巨门" and row["branch"] == "丑"
        )
        self.assertEqual(("陷",), jumen_chou["ch69_source_lexemes"])
        self.assertEqual(("局", "陷"), jumen_chou["ch70_source_lexemes"])
        self.assertTrue(jumen_chou["ch70_source_conflict"])
        self.assertEqual("EXACT_LEXEME_OVERLAP", jumen_chou["relation"])

    def test_ch69_does_not_fill_ch70_unstated_tianji_si(self) -> None:
        payload = jielan_1581_dignity_ch69_ch70_cross_collation_payload()
        row = next(
            row for row in payload["rows"]
            if row["display_name"] == "天机" and row["branch"] == "巳"
        )
        self.assertEqual(("兴",), row["ch69_source_lexemes"])
        self.assertEqual((), row["ch70_source_lexemes"])
        self.assertEqual("CH70_UNSTATED", row["relation"])
        self.assertFalse(payload["ch69_used_to_fill_ch70"])

    def test_unresolved_ch69_text_is_typed_not_guessed(self) -> None:
        payload = jielan_1581_dignity_ch69_ch70_cross_collation_payload()
        wenchang_zi = next(
            row for row in payload["rows"]
            if row["display_name"] == "文昌" and row["branch"] == "子"
        )
        self.assertEqual((), wenchang_zi["ch69_source_lexemes"])
        self.assertEqual("UNRESOLVED_TEXT_SCOPE", wenchang_zi["ch69_attestation_status"])
        self.assertEqual("CH69_TEXT_UNRESOLVED", wenchang_zi["relation"])
        self.assertIn("singular 文", wenchang_zi["ch69_unresolved_note"])

        taiyang_chen = next(
            row for row in payload["rows"]
            if row["display_name"] == "太阳" and row["branch"] == "辰"
        )
        self.assertEqual("CH69_TEXT_UNRESOLVED", taiyang_chen["relation"])
        self.assertIn("午->日", taiyang_chen["ch69_unresolved_note"])

    def test_obvious_source_local_direction_conflict_is_flagged_without_r4_mapping(self) -> None:
        payload = jielan_1581_dignity_ch69_ch70_cross_collation_payload()
        tianji_zi = next(
            row for row in payload["rows"]
            if row["display_name"] == "天机" and row["branch"] == "子"
        )
        self.assertEqual(("陷",), tianji_zi["ch69_source_lexemes"])
        self.assertEqual(("得地",), tianji_zi["ch70_source_lexemes"])
        self.assertEqual("SOURCE_LOCAL_POLARITY_CONFLICT", tianji_zi["relation"])
        self.assertFalse(tianji_zi["production_grade_mapping_present"])
        self.assertFalse(payload["production_grade_mapping_present"])
        self.assertFalse(payload["production_dignity_registry_changed"])
        self.assertFalse(payload["winner_selected"])

    def test_entity_filter_keeps_twelve_branches_and_does_not_select_a_winner(self) -> None:
        payload = resolve_jielan_1581_dignity_ch69_ch70_cross_collation(
            display_name="紫微"
        )
        self.assertEqual(12, len(payload["rows"]))
        self.assertEqual("PRESERVED_NOT_SELECTED", payload["selection_status"])
        self.assertEqual(64, len(payload["cross_collation_hash"]))
        with self.assertRaisesRegex(ValueError, "unsupported Jielan dignity entity"):
            resolve_jielan_1581_dignity_ch69_ch70_cross_collation(
                display_name="UNKNOWN"
            )


if __name__ == "__main__":
    unittest.main()

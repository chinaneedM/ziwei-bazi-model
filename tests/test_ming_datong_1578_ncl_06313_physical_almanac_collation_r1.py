from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLLATION = ROOT / "docs" / "research" / "MING-DATONG-1578-NCL-06313-PHYSICAL-ALMANAC-COLLATION-R1.json"
ORACLE = ROOT / "tests" / "fixtures" / "ming-datong-1578-month-start-oracle-r1.json"
REPLAY = ROOT / "docs" / "research" / "MING-DATONG-1578-D1-SOURCE-REPLAY-R1.json"


class MingDatong1578Ncl06313PhysicalAlmanacCollationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(COLLATION.read_text(encoding="utf-8"))
        cls.oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        cls.replay = json.loads(REPLAY.read_text(encoding="utf-8"))

    def test_exact_same_year_qintianjian_identity_is_preserved(self) -> None:
        self.assertEqual(self.data["institutional_catalog"]["catalog_identifier"], "06313")
        self.assertEqual(self.data["institutional_catalog"]["edition"], "明欽天監刊本")
        self.assertIn("欽天監/曆日印", self.data["institutional_catalog"]["seals"])
        self.assertEqual(self.data["public_scan"]["pdf_page_count"], 28)
        self.assertEqual(self.data["public_scan"]["month_calendar_zero_based_page_range"], [8, 19])

    def test_all_twelve_month_pages_are_contiguous_and_directly_collated(self) -> None:
        months = self.data["months"]
        self.assertEqual([m["month"] for m in months], list(range(1, 13)))
        self.assertEqual([m["pdf_page_index_zero_based"] for m in months], list(range(8, 20)))
        self.assertTrue(all(m["direct_physical_page_status"] == "DIRECT_SCREENSHOT_COLLATION" for m in months))
        summary = self.data["direct_collation_summary"]
        self.assertEqual(summary["directly_rendered_month_pages"], 12)
        self.assertEqual(summary["unresolved_direct_page_months"], [])
        self.assertTrue(summary["complete_physical_month_page_collation"])

    def test_all_month_identity_and_size_labels_match_without_mismatch(self) -> None:
        oracle_by_month = {m["month"]: m for m in self.oracle["months"]}
        visible_lengths = []
        for month in self.data["months"]:
            expected = oracle_by_month[month["month"]]
            self.assertEqual(month["expected_length_days"], expected["length_days"])
            self.assertEqual(month["expected_start_ganzhi"], expected["start_ganzhi"])
            self.assertTrue(month["physical_month_identity_match"])
            self.assertTrue(month["physical_size_label_match"])
            self.assertEqual(
                month["expected_size_label"],
                "大" if expected["length_days"] == 30 else "小",
            )
            visible_lengths.append(month["expected_length_days"])
        summary = self.data["direct_collation_summary"]
        self.assertEqual(summary["direct_month_identity_matches"], 12)
        self.assertEqual(summary["direct_month_size_matches"], 12)
        self.assertEqual(summary["direct_month_size_mismatches"], 0)
        self.assertEqual(summary["directly_visible_month_length_sequence"], visible_lengths)
        self.assertEqual(visible_lengths, [29, 30, 30, 29, 30, 29, 30, 29, 29, 30, 29, 30])

    def test_month_6_direct_render_closes_only_identity_and_size(self) -> None:
        month6 = self.data["months"][5]
        self.assertEqual(month6["month"], 6)
        self.assertEqual(month6["label"], "六月")
        self.assertEqual(month6["pdf_page_index_zero_based"], 13)
        self.assertEqual(month6["expected_size_label"], "小")
        self.assertEqual(month6["direct_physical_page_status"], "DIRECT_SCREENSHOT_COLLATION")
        self.assertTrue(month6["physical_month_identity_match"])
        self.assertTrue(month6["physical_size_label_match"])
        self.assertEqual(
            month6["start_ganzhi_direct_physical_certification"],
            "GRID_VISUALLY_CONSISTENT_BUT_FINE_GLYPH_READING_BOUND_TO_ORACLE_CHAIN",
        )
        recovery = self.data["public_scan"]["direct_render_recovery"]
        self.assertTrue(recovery["recovered_direct_render"])
        self.assertEqual(recovery["directly_visible_heading"], "六月小")
        self.assertIn("FINE_FIRST_DAY_GANZHI_GLYPH_REMAINS_CHAIN_BOUND", recovery["certification_scope"])
        self.assertEqual(
            self.data["epistemic_firewalls"]["month_title_and_size_as_fine_first_day_ganzhi_glyph_transcription"],
            "FORBIDDEN",
        )

    def test_physical_oracle_and_d1_layers_are_bound_but_not_double_counted(self) -> None:
        expected = [m["start_ganzhi"] for m in self.oracle["months"]]
        replayed = [m["ganzhi"] for m in self.replay["months"][:12]]
        physical_expected = [m["expected_start_ganzhi"] for m in self.data["months"]]
        self.assertEqual(replayed, expected)
        self.assertEqual(physical_expected, expected)
        self.assertEqual(
            self.data["evidence_layering"]["independence_rule"],
            "DO_NOT_COUNT_PHYSICAL_SCAN_REIGN_RECORD_AND_D1_REPLAY_AS_THE_SAME_EVIDENCE_LAYER",
        )

    def test_physical_calendar_grid_never_certifies_subday_conjunction_meridian_or_runtime(self) -> None:
        scope = self.data["conjunction_time_scope"]
        self.assertFalse(scope["dedicated_month_start_conjunction_time_entries_identified_in_reviewed_month_pages"])
        self.assertFalse(scope["absence_from_entire_almanac_certified"])
        self.assertEqual(
            self.data["epistemic_firewalls"]["physical_day_grid_as_exact_conjunction_time_certification"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["same_year_match_as_qishuo_meridian_resolution"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["physical_scan_as_general_datong_runtime_certification"],
            "FORBIDDEN",
        )
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])


if __name__ == "__main__":
    unittest.main()

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
        self.assertEqual(cls := self.data["institutional_catalog"]["catalog_identifier"], "06313")
        self.assertEqual(self.data["institutional_catalog"]["edition"], "明欽天監刊本")
        self.assertIn("欽天監/曆日印", self.data["institutional_catalog"]["seals"])
        self.assertEqual(self.data["public_scan"]["pdf_page_count"], 28)
        self.assertEqual(self.data["public_scan"]["month_calendar_zero_based_page_range"], [8, 19])

    def test_month_pages_are_contiguous_and_only_month_6_has_render_gap(self) -> None:
        months = self.data["months"]
        self.assertEqual([m["month"] for m in months], list(range(1, 13)))
        self.assertEqual([m["pdf_page_index_zero_based"] for m in months], list(range(8, 20)))
        unresolved = [
            m["month"]
            for m in months
            if m["direct_physical_page_status"] != "DIRECT_SCREENSHOT_COLLATION"
        ]
        self.assertEqual(unresolved, [6])

    def test_directly_rendered_month_size_labels_match_oracle_without_mismatch(self) -> None:
        oracle_by_month = {m["month"]: m for m in self.oracle["months"]}
        direct = 0
        for month in self.data["months"]:
            expected = oracle_by_month[month["month"]]
            self.assertEqual(month["expected_length_days"], expected["length_days"])
            self.assertEqual(month["expected_start_ganzhi"], expected["start_ganzhi"])
            if month["direct_physical_page_status"] == "DIRECT_SCREENSHOT_COLLATION":
                direct += 1
                self.assertTrue(month["physical_month_identity_match"])
                self.assertTrue(month["physical_size_label_match"])
                self.assertEqual(
                    month["expected_size_label"],
                    "大" if expected["length_days"] == 30 else "小",
                )
            else:
                self.assertIsNone(month["physical_month_identity_match"])
                self.assertIsNone(month["physical_size_label_match"])
        self.assertEqual(direct, 11)
        self.assertEqual(self.data["direct_collation_summary"]["direct_month_size_mismatches"], 0)

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

    def test_month_6_is_not_silently_promoted_to_direct_physical_evidence(self) -> None:
        month6 = self.data["months"][5]
        self.assertEqual(month6["month"], 6)
        self.assertEqual(
            month6["direct_physical_page_status"],
            "PDF_PAGE_SCREENSHOT_TOOL_ERROR_NOT_DIRECTLY_CERTIFIED",
        )
        self.assertEqual(
            month6["start_ganzhi_direct_physical_certification"],
            "NOT_DIRECTLY_CERTIFIED_IN_THIS_SESSION",
        )
        self.assertFalse(self.data["direct_collation_summary"]["complete_physical_month_page_collation"])
        self.assertEqual(
            self.data["epistemic_firewalls"]["infer_month6_direct_physical_reading_from_neighbors"],
            "FORBIDDEN",
        )

    def test_physical_calendar_grid_never_certifies_subday_conjunction_or_meridian(self) -> None:
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
        self.assertFalse(self.data["runtime_selection_authorized"])


if __name__ == "__main__":
    unittest.main()

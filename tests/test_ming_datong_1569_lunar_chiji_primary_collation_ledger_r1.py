from __future__ import annotations

import json
import unittest
from decimal import Decimal, ROUND_DOWN
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "research" / "MING-DATONG-1569-LUNAR-CHIJI-PRIMARY-COLLATION-LEDGER-R1.json"


class MingDatong1569LunarChijiPrimaryCollationLedgerR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.rows = {row["limit"]: row for row in cls.data["rows"]}

    def test_primary_schema_restores_sunyi_jiefa(self) -> None:
        self.assertEqual(
            self.data["visible_table_schema"],
            ["限數","遲疾日率分","損益捷法","損益分","遲疾度"],
        )
        self.assertEqual(self.data["structural_findings"]["previously_omitted_column"], "損益捷法")

    def test_shortcut_formula_matches_all_formula_expectations(self) -> None:
        for n in range(0,168):
            row=self.rows[n]
            loss=Decimal(row["expected_loss_gain_source_fen"])
            expected=(loss*Decimal("100")/Decimal("820")).quantize(Decimal("0.0001"),rounding=ROUND_DOWN)
            self.assertEqual(expected,Decimal(row["expected_loss_gain_shortcut_source_seconds"]),n)
        self.assertIsNone(self.rows[168]["expected_loss_gain_shortcut_source_seconds"])

    def test_direct_controls_cover_start_center_and_terminal_boundaries(self) -> None:
        direct={n for n,row in self.rows.items() if row["collation_status"]=="DIRECT_PRIMARY_MATCH"}
        self.assertTrue(set(range(0,8)).issubset(direct))
        self.assertTrue(set(range(81,87)).issubset(direct))
        self.assertTrue({167,168}.issubset(direct))

    def test_central_shortcut_transition_and_terminal_blank(self) -> None:
        self.assertEqual(self.rows[83]["primary_reading"]["loss_gain_shortcut_source_seconds"],"0.0021")
        self.assertEqual(self.rows[84]["primary_reading"]["loss_gain_shortcut_source_seconds"],"0.0021")
        self.assertEqual(self.rows[167]["primary_reading"]["loss_gain_shortcut_source_seconds"],"1.3514")
        self.assertTrue(self.rows[168]["primary_reading"]["loss_gain_shortcut_blank"])
        self.assertTrue(self.rows[168]["primary_reading"]["loss_gain_blank"])
        self.assertTrue(self.rows[168]["primary_reading"]["accumulated_blank"])

    def test_in_progress_ledger_never_promotes_formula_rows(self) -> None:
        self.assertFalse(self.data["full_row_by_row_primary_collation_complete"])
        self.assertGreater(self.data["pending_rows"],0)
        self.assertEqual(
            self.data["directly_collated_rows"]+self.data["pending_rows"],
            self.data["total_rows"],
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["formula_expected_as_direct_primary_reading"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["terminal_blank_as_computed_zero"],
            "FORBIDDEN",
        )

    def test_all_primary_pages_are_registered_but_not_false_closed(self) -> None:
        pages=self.data["page_summaries"]
        self.assertEqual([p["pdf_page_index_zero_based"] for p in pages],list(range(24,33)))
        self.assertTrue(all(p["page_image_reviewed"] for p in pages))
        self.assertTrue(any(p["pending_direct_glyph_collation_count"]>0 for p in pages))

    def test_research_only(self) -> None:
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from decimal import Decimal, ROUND_DOWN
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "research" / "MING-DATONG-1569-LUNAR-XINGDU-PRIMARY-COLLATION-LEDGER-R1.json"


class MingDatong1569LunarXingduPrimaryCollationLedgerR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.rows = {row["limit"]: row for row in cls.data["rows"]}

    def test_primary_schema_restores_both_shortcut_columns(self) -> None:
        self.assertEqual(
            self.data["visible_table_schema"],
            ["限數","疾曆行度","疾曆捷法","遲曆行度","遲曆捷法"],
        )
        self.assertEqual(self.data["structural_findings"]["previously_omitted_columns"],["疾曆捷法","遲曆捷法"])

    def test_shortcut_formula_matches_all_formula_expectations(self) -> None:
        q=Decimal("0.0000001")
        for n in range(0,168):
            row=self.rows[n]
            ji_int=int(Decimal(row["expected_ji_xingdu_degree"])*Decimal("10000"))
            chi_int=int(Decimal(row["expected_chi_xingdu_degree"])*Decimal("10000"))
            ji=(Decimal("820")/Decimal(ji_int)).quantize(q,rounding=ROUND_DOWN)
            chi=(Decimal("820")/Decimal(chi_int)).quantize(q,rounding=ROUND_DOWN)
            self.assertEqual(ji,Decimal(row["expected_ji_xingdu_shortcut_source_ratio"]),n)
            self.assertEqual(chi,Decimal(row["expected_chi_xingdu_shortcut_source_ratio"]),n)

    def test_direct_controls_cover_start_center_and_terminal(self) -> None:
        direct={n for n,row in self.rows.items() if row["collation_status"]=="DIRECT_PRIMARY_MATCH"}
        self.assertTrue(set(range(0,8)).issubset(direct))
        self.assertTrue(set(range(81,87)).issubset(direct))
        self.assertTrue({167,168}.issubset(direct))

    def test_central_shortcut_pair_swaps_exactly(self) -> None:
        r83=self.rows[83]["primary_reading"]
        r84=self.rows[84]["primary_reading"]
        self.assertEqual(r83["ji_xingdu_shortcut_source_ratio"],r84["chi_xingdu_shortcut_source_ratio"])
        self.assertEqual(r83["chi_xingdu_shortcut_source_ratio"],r84["ji_xingdu_shortcut_source_ratio"])
        self.assertEqual(r83["ji_xingdu_shortcut_source_ratio"],"0.0747834")
        self.assertEqual(r83["chi_xingdu_shortcut_source_ratio"],"0.0748106")

    def test_terminal_limit_preserves_all_blanks(self) -> None:
        r=self.rows[168]["primary_reading"]
        self.assertTrue(r["ji_xingdu_blank"])
        self.assertTrue(r["ji_shortcut_blank"])
        self.assertTrue(r["chi_xingdu_blank"])
        self.assertTrue(r["chi_shortcut_blank"])

    def test_in_progress_ledger_does_not_promote_formula_rows(self) -> None:
        self.assertFalse(self.data["full_row_by_row_primary_collation_complete"])
        self.assertGreater(self.data["pending_rows"],0)
        self.assertEqual(self.data["directly_collated_rows"]+self.data["pending_rows"],self.data["total_rows"])
        self.assertEqual(self.data["epistemic_firewalls"]["formula_expected_as_direct_primary_reading"],"FORBIDDEN")

    def test_all_primary_pages_are_registered(self) -> None:
        pages=self.data["page_summaries"]
        self.assertEqual([p["pdf_page_index_zero_based"] for p in pages],list(range(33,41)))
        self.assertTrue(all(p["page_image_reviewed"] for p in pages))
        self.assertTrue(any(p["pending_direct_glyph_collation_count"]>0 for p in pages))

    def test_research_only(self) -> None:
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])


if __name__ == "__main__":
    unittest.main()

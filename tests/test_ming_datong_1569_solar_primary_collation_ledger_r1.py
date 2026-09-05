from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "research" / "MING-DATONG-1569-SOLAR-PRIMARY-COLLATION-LEDGER-R1.json"


class MingDatong1569SolarPrimaryCollationLedgerR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_primary_table_schema_includes_message_column(self) -> None:
        self.assertEqual(
            self.data["visible_table_schema"],
            ["積日", "消息分", "盈縮加分", "盈縮積度"],
        )
        self.assertEqual(self.data["structural_findings"]["omitted_column_discovered"], "消息分")

    def test_completed_ledger_closes_only_direct_primary_glyph_work(self) -> None:
        self.assertTrue(self.data["full_row_by_row_primary_collation_complete"])
        self.assertEqual(self.data["directly_collated_rows"], self.data["total_rows"])
        self.assertEqual(self.data["pending_rows"], 0)
        self.assertEqual(self.data["variant_rows"], 0)
        self.assertEqual(self.data["glyph_ambiguous_rows"], 0)
        self.assertEqual(
            self.data["epistemic_firewalls"]["formula_expected_as_direct_primary_reading"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["page_image_opened_as_all_rows_collated"],
            "FORBIDDEN",
        )

    def test_direct_controls_cover_both_table_starts_and_ends(self) -> None:
        direct={(r["family_id"],r["day_index"]):r for r in self.data["rows"] if r["collation_status"]=="DIRECT_PRIMARY_MATCH"}
        for key in [
            ("YING_INITIAL_SUO_TERMINAL",0),
            ("YING_INITIAL_SUO_TERMINAL",87),
            ("YING_INITIAL_SUO_TERMINAL",88),
            ("YING_INITIAL_SUO_TERMINAL",89),
            ("SUO_INITIAL_YING_TERMINAL",0),
            ("SUO_INITIAL_YING_TERMINAL",92),
            ("SUO_INITIAL_YING_TERMINAL",93),
            ("SUO_INITIAL_YING_TERMINAL",94),
        ]:
            self.assertIn(key,direct)

    def test_message_boundary_controls_are_preserved(self) -> None:
        direct={(r["family_id"],r["day_index"]):r for r in self.data["rows"] if r["collation_status"]=="DIRECT_PRIMARY_MATCH"}
        self.assertEqual(direct[("YING_INITIAL_SUO_TERMINAL",0)]["primary_reading"]["message_source_table_units"],"4.9386")
        self.assertEqual(direct[("YING_INITIAL_SUO_TERMINAL",87)]["primary_reading"]["message_source_table_units"],"6.5568")
        self.assertTrue(direct[("YING_INITIAL_SUO_TERMINAL",88)]["primary_reading"]["message_blank"])
        self.assertEqual(direct[("SUO_INITIAL_YING_TERMINAL",0)]["primary_reading"]["message_source_table_units"],"4.4362")
        self.assertEqual(direct[("SUO_INITIAL_YING_TERMINAL",92)]["primary_reading"]["message_source_table_units"],"5.9266")
        self.assertTrue(direct[("SUO_INITIAL_YING_TERMINAL",93)]["primary_reading"]["message_blank"])

    def test_every_page_13_to_22_is_fully_directly_collated(self) -> None:
        pages=self.data["page_summaries"]
        self.assertEqual([p["pdf_page_index_zero_based"] for p in pages],list(range(13,23)))
        self.assertTrue(all(p["page_image_reviewed"] for p in pages))
        self.assertTrue(all(p["pending_direct_glyph_collation_count"] == 0 for p in pages))
        self.assertTrue(all(p["page_collation_status"] == "FULL_PAGE_ROW_GLYPH_COLLATION_COMPLETE" for p in pages))

    def test_research_only(self) -> None:
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])


if __name__ == "__main__":
    unittest.main()

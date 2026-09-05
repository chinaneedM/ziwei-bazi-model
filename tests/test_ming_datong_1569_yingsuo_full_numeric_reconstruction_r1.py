from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs" / "research" / "MING-DATONG-1569-YINGSUO-FULL-NUMERIC-RECONSTRUCTION-R1.json"


class MingDatong1569YingsuoFullNumericReconstructionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        cls.families = {item["family_id"]: item for item in cls.data["families"]}

    def test_research_firewall(self) -> None:
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])
        self.assertEqual(
            self.data["epistemic_firewalls"]["full_numeric_reconstruction_as_verbatim_primary_transcription"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["support_row_as_admissible_initial_limit_input"],
            "FORBIDDEN",
        )

    def _verify_family_formula(self, family_id: str) -> None:
        family = self.families[family_id]
        D = Decimal(family["three_difference_constants"]["dingcha_degree"])
        P = Decimal(family["three_difference_constants"]["pingcha_degree"])
        L = Decimal(family["three_difference_constants"]["licha_degree"])
        rows = {row["day_index"]: row for row in family["rows"]}
        support = family["terminal_support_row_day"]

        self.assertEqual(set(rows), set(range(support + 1)))
        for n in range(support + 1):
            N = Decimal(n)
            c = N * (D - N * (P + N * L))
            stored = Decimal(rows[n]["accumulated_degree"] or "0")
            self.assertEqual(c, stored, (family_id, n))
            if n < support:
                M = Decimal(n + 1)
                c_next = M * (D - M * (P + M * L))
                add = c_next - c
                self.assertEqual(add, Decimal(rows[n]["add_degree"]), (family_id, n))
                self.assertEqual(add * Decimal("10000"), Decimal(rows[n]["add_source_table_units"]), (family_id, n))
            else:
                self.assertIsNone(rows[n]["add_degree"])
                self.assertIsNone(rows[n]["add_source_table_units"])
                self.assertTrue(rows[n]["support_row_only"])

    def test_both_three_difference_table_families_reconstruct_exactly(self) -> None:
        self._verify_family_formula("YING_INITIAL_SUO_TERMINAL")
        self._verify_family_formula("SUO_INITIAL_YING_TERMINAL")

    def test_message_column_is_adjacent_add_difference(self) -> None:
        for family in self.families.values():
            rows = {row["day_index"]: row for row in family["rows"]}
            support = family["terminal_support_row_day"]
            for n in range(support):
                current = rows[n]
                nxt = rows[n + 1]
                if current["add_source_table_units"] is not None and nxt["add_source_table_units"] is not None:
                    expected = Decimal(current["add_source_table_units"]) - Decimal(nxt["add_source_table_units"])
                    self.assertEqual(expected, Decimal(current["message_source_table_units"]), (family["family_id"], n))
                else:
                    self.assertIsNone(current["message_source_table_units"])
            self.assertIsNone(rows[support]["message_source_table_units"])

    def test_message_column_source_controls_and_terminal_blanks(self) -> None:
        a = {row["day_index"]: row for row in self.families["YING_INITIAL_SUO_TERMINAL"]["rows"]}
        b = {row["day_index"]: row for row in self.families["SUO_INITIAL_YING_TERMINAL"]["rows"]}
        self.assertEqual(a[0]["message_source_table_units"], "4.9386")
        self.assertEqual(a[87]["message_source_table_units"], "6.5568")
        self.assertIsNone(a[88]["message_source_table_units"])
        self.assertIsNone(a[89]["message_source_table_units"])
        self.assertEqual(b[0]["message_source_table_units"], "4.4362")
        self.assertEqual(b[92]["message_source_table_units"], "5.9266")
        self.assertIsNone(b[93]["message_source_table_units"])
        self.assertIsNone(b[94]["message_source_table_units"])

    def test_primary_initial_controls(self) -> None:
        a = {row["day_index"]: row for row in self.families["YING_INITIAL_SUO_TERMINAL"]["rows"]}
        b = {row["day_index"]: row for row in self.families["SUO_INITIAL_YING_TERMINAL"]["rows"]}
        self.assertEqual(a[0]["add_source_table_units"], "510.8569")
        self.assertEqual(a[1]["add_source_table_units"], "505.9183")
        self.assertEqual(a[2]["accumulated_source_table_units"], "1016.7752")
        self.assertEqual(b[0]["add_source_table_units"], "484.8473")
        self.assertEqual(b[1]["add_source_table_units"], "480.4111")
        self.assertEqual(b[2]["accumulated_source_table_units"], "965.2584")

    def test_exact_cutoffs_leave_terminal_support_rows_outside_initial_limit(self) -> None:
        a = self.families["YING_INITIAL_SUO_TERMINAL"]
        b = self.families["SUO_INITIAL_YING_TERMINAL"]
        self.assertEqual(a["max_interpolation_whole_day"], 88)
        self.assertEqual(a["terminal_support_row_day"], 89)
        self.assertEqual(a["exact_initial_limit_cutoff"]["days"], 88)
        self.assertEqual(a["exact_initial_limit_cutoff"]["source_fraction"], "9092.25")
        self.assertEqual(b["max_interpolation_whole_day"], 93)
        self.assertEqual(b["terminal_support_row_day"], 94)
        self.assertEqual(b["exact_initial_limit_cutoff"]["days"], 93)
        self.assertEqual(b["exact_initial_limit_cutoff"]["source_fraction"], "7120.25")

    def test_terminal_support_values_and_last_usable_add_values(self) -> None:
        a = {row["day_index"]: row for row in self.families["YING_INITIAL_SUO_TERMINAL"]["rows"]}
        b = {row["day_index"]: row for row in self.families["SUO_INITIAL_YING_TERMINAL"]["rows"]}
        self.assertEqual(a[88]["add_source_table_units"], "5.0593")
        self.assertEqual(a[89]["accumulated_source_table_units"], "24014.4161")
        self.assertIsNone(a[89]["add_source_table_units"])
        self.assertEqual(b[93]["add_source_table_units"], "2.9771")
        self.assertEqual(b[94]["accumulated_source_table_units"], "24013.5032")
        self.assertIsNone(b[94]["add_source_table_units"])

    def test_interpolation_formula_uses_10000_day_radix(self) -> None:
        family = self.families["YING_INITIAL_SUO_TERMINAL"]
        rows = {row["day_index"]: row for row in family["rows"]}
        n = 10
        remainder = Decimal("2500")
        c = Decimal(rows[n]["accumulated_degree"])
        add = Decimal(rows[n]["add_degree"])
        result = c + remainder / Decimal("10000") * add
        self.assertEqual(result, Decimal("0.4999258475"))


if __name__ == "__main__":
    unittest.main()

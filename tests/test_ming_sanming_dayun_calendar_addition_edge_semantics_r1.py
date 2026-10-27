from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research" / "MING-SANMING-DAYUN-CALENDAR-ADDITION-EDGE-SEMANTICS-R1.json"
OU = ROOT / "docs" / "research" / "MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json"

class MingSanmingDayunCalendarAdditionEdgeSemanticsR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(RESEARCH.read_text(encoding="utf-8"))
        cls.findings = {x["finding_id"]: x for x in cls.data["findings"]}
        cls.ou = json.loads(OU.read_text(encoding="utf-8"))
        cls.gates = {x["gate_id"]: x for x in cls.ou["gates"]}

    def test_runtime_remains_fail_closed(self) -> None:
        self.assertEqual(self.data["status"], "EDGE_SEMANTICS_PARTIALLY_CLOSED_RUNTIME_STILL_FAIL_CLOSED")
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["production_default_changed"])
        self.assertFalse(self.data["algorithm_reopen_authorized"])
        self.assertFalse(self.data["candidate_collapse_authorized"])
        self.assertEqual(
            self.data["runtime_firewall"]["required_adapter_result"],
            "UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER",
        )

    def test_explicit_worked_example_semantics_are_separated(self) -> None:
        self.assertEqual(
            self.findings["SMTH-CALADD-F01-SMALL-MONTH-DEFICIT"]["status"],
            "CLOSED_RECEIVED_TEXT_WORKED_EXAMPLE",
        )
        self.assertEqual(
            self.findings["SMTH-CALADD-F02-INTERCALARY-EXTRA-MONTH"]["status"],
            "CLOSED_RECEIVED_TEXT_WORKED_EXAMPLE",
        )
        self.assertEqual(
            self.findings["SMTH-CALADD-F03-TEN-ANNIVERSARY-CHANGE"]["status"],
            "CLOSED_TEXTUAL_STATEMENT_EXECUTION_DEPENDENCY_BLOCKED",
        )

    def test_invalid_day_policy_is_not_invented(self) -> None:
        finding = self.findings["SMTH-CALADD-F04-INVALID-DAY-IN-SMALL-MONTH"]
        self.assertEqual(finding["status"], "UNRESOLVED_NOT_ATTESTED_IN_REVIEWED_PASSAGE")
        self.assertIn("NO_CLAMP_TO_29", finding["prohibited_inference"])
        self.assertIn("NO_GREGORIAN_INVALID_DATE_RULE", finding["prohibited_inference"])

    def test_duplicate_intercalary_identity_is_not_invented(self) -> None:
        finding = self.findings["SMTH-CALADD-F05-REGULAR_VS_INTERCALARY_DUPLICATE_MONTH_IDENTITY"]
        self.assertEqual(finding["status"], "UNRESOLVED_NOT_ATTESTED_IN_REVIEWED_PASSAGE")
        self.assertIn("NO_AUTOMATIC_REGULAR_MONTH_PREFERENCE", finding["prohibited_inference"])
        self.assertIn("NO_DROP_LEAP_FLAG", finding["prohibited_inference"])
        self.assertEqual(
            self.findings["SMTH-CALADD-F06-BIRTH_OR_ANCHOR_INSIDE_INTERCALARY_MONTH"]["status"],
            "UNRESOLVED_NOT_ATTESTED_IN_REVIEWED_PASSAGE",
        )

    def test_12ou_gate_statuses_do_not_change(self) -> None:
        self.assertEqual(self.gates["MD-G07-INVALID-TARGET-DATE-POLICY"]["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(self.gates["MD-G08-INTERCALARY-MONTH-IDENTITY-AND-TRAVERSAL"]["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(self.gates["MD-G10-TEN-YEAR-RECURRENCE-SAME-REGIME"]["status"], "DEPENDENCY_BLOCKED")
        self.assertEqual(
            self.gates["MD-G08-INTERCALARY-MONTH-IDENTITY-AND-TRAVERSAL"]["batch_12ov_refinement"]["aggregate_intercalary_extra_month_counting"],
            "CLOSED_RECEIVED_TEXT_WORKED_EXAMPLE",
        )

    def test_wanli_target_page_is_not_falsely_claimed_as_direct_collation(self) -> None:
        self.assertFalse(self.data["evidence_policy"]["direct_target_page_wanli_physical_collation_completed"])
        wanli = [w for w in self.data["witnesses"] if "WANLI" in w["witness_id"] or w["witness_id"] == "EXT-SANMING-NCL-1578-MAIN"]
        self.assertTrue(wanli)
        self.assertTrue(all(w.get("target_dayun_page_directly_collated_in_12ov", False) is False for w in wanli))

    def test_accounting_is_unchanged(self) -> None:
        accounting = self.data["accounting"]
        self.assertEqual(accounting["matrix_rows"], 222)
        self.assertEqual(accounting["audited_rows"], 222)
        self.assertEqual(accounting["current_missing_from_product_rows"], 4)
        self.assertEqual(accounting["provenance_defects_confirmed"], 45)
        self.assertEqual(accounting["provenance_defects_repaired"], 45)
        self.assertEqual(accounting["algorithm_reopens"], 0)
        self.assertEqual(accounting["candidate_collapses"], 0)

if __name__ == "__main__":
    unittest.main()

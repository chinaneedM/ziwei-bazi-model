from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research" / "MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json"

class MingDatongExecutableAdapterBlockerDecompositionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(RESEARCH.read_text(encoding="utf-8"))
        cls.gates = {item["gate_id"]: item for item in cls.data["gates"]}

    def test_general_runtime_remains_fail_closed(self) -> None:
        self.assertEqual(self.data["status"], "DECOMPOSED_RUNTIME_STILL_FAIL_CLOSED")
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["production_default_changed"])
        self.assertFalse(self.data["algorithm_reopen_authorized"])
        self.assertFalse(self.data["candidate_collapse_authorized"])

    def test_gate_accounting_is_frozen(self) -> None:
        counts = self.data["counts"]
        self.assertEqual(counts["closed_source_scoped"], 4)
        self.assertEqual(counts["open_blocking_general_adapter"], 5)
        self.assertEqual(counts["dependency_blocked"], 2)
        self.assertEqual(counts["total_gates"], sum(
            counts[k] for k in ("closed_source_scoped", "open_blocking_general_adapter", "dependency_blocked")
        ))

    def test_qishuo_internal_coordinate_is_closed_but_geography_is_not(self) -> None:
        self.assertEqual(self.gates["MD-G02-INTERNAL-DAY-AND-CLOCK-COORDINATE"]["status"], "CLOSED_SOURCE_SCOPED")
        geo = self.gates["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(geo["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertIn("MODULE_SPECIFIC_MIXED_GEOGRAPHY", geo["preserved_hypotheses"])
        self.assertIn("1495", " ".join(geo["diagnostics"]))

    def test_1578_target_year_closure_is_not_multi_year_generalization(self) -> None:
        target = self.gates["MD-G06-1578-TARGET-YEAR-MONTH-STRUCTURE"]
        self.assertEqual(target["status"], "CLOSED_SOURCE_SCOPED")
        self.assertEqual(target["scope_limit"], "TARGET_YEAR_AND_BOUND_ORACLE_ONLY_NOT_MULTI_YEAR_GENERALIZATION")
        self.assertEqual(self.gates["MD-G09-MULTI-YEAR-LEAP-GENERALIZATION"]["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")

    def test_calendar_addition_edges_have_no_silent_fallback(self) -> None:
        invalid = self.gates["MD-G07-INVALID-TARGET-DATE-POLICY"]
        intercalary = self.gates["MD-G08-INTERCALARY-MONTH-IDENTITY-AND-TRAVERSAL"]
        self.assertEqual(invalid["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(intercalary["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertIn("NO_SILENT_CLAMP_TO_LAST_DAY", invalid["forbidden_fallbacks"])
        self.assertIn("NO_DROP_INTERCALARY_IDENTITY", intercalary["forbidden_fallbacks"])
        self.assertIn("NO_MODERN_CALENDAR_LIBRARY_BEHAVIOR_AS_HISTORICAL_AUTHORITY", intercalary["forbidden_fallbacks"])

    def test_recurrence_and_runtime_are_dependency_blocked(self) -> None:
        recurrence = self.gates["MD-G10-TEN-YEAR-RECURRENCE-SAME-REGIME"]
        runtime = self.gates["MD-G11-BAZI-RUNTIME-AND-PRODUCT-INTEGRATION"]
        self.assertEqual(recurrence["status"], "DEPENDENCY_BLOCKED")
        self.assertEqual(runtime["status"], "DEPENDENCY_BLOCKED")
        self.assertIn("MD-G09-MULTI-YEAR-LEAP-GENERALIZATION", recurrence["depends_on"])
        self.assertIn("MD-G03-QISHUO-GEOGRAPHIC-REFERENCE", runtime["depends_on"])
        self.assertIn("UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER", runtime["current_required_behavior"])

    def test_accounting_does_not_reduce_missing_rows(self) -> None:
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

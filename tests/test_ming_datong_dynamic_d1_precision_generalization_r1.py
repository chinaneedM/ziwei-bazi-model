from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research" / "MING-DATONG-DYNAMIC-D1-PRECISION-GENERALIZATION-R1.json"
FIXTURE = ROOT / "docs" / "research" / "MING-DATONG-D1-56-CONJUNCTION-VALIDATION-R1.json"
OU = ROOT / "docs" / "research" / "MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json"

class MingDatongDynamicD1PrecisionGeneralizationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(RESEARCH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.ou = json.loads(OU.read_text(encoding="utf-8"))

    def test_final_time_fixture_is_complete(self) -> None:
        stats = self.fixture["statistics"]
        self.assertEqual(stats["total_rows"], 56)
        self.assertEqual(stats["years"], [1531, 1532, 1604, 1616, 1629, 1639])
        self.assertEqual(stats["d1_in_printed_bin_count"], 56)
        self.assertEqual(stats["d1_outside_printed_bin_count"], 0)
        self.assertEqual(stats["d2_in_printed_bin_count"], 8)
        self.assertEqual(stats["d2_outside_printed_bin_count"], 48)

    def test_narrowest_control_is_1639_month_four(self) -> None:
        narrow = self.fixture["statistics"]["narrowest_bin"]
        self.assertEqual(narrow["year"], 1639)
        self.assertEqual(narrow["month"], "四")
        self.assertEqual(narrow["tolerance_day"], 0.0008)
        self.assertEqual(narrow["full_width_minutes"], 2.304)
        self.assertTrue(narrow["d1_in_printed_bin"])
        self.assertFalse(narrow["d2_in_printed_bin"])

    def test_fixture_has_only_one_d2_sexagenary_day_change(self) -> None:
        self.assertEqual(self.fixture["statistics"]["d2_sexagenary_day_change_count"], 1)
        rows = [r for r in self.fixture["rows"] if r["d2_changes_sexagenary_day"]]
        self.assertEqual([(r["year"], r["month"]) for r in rows], [(1639, "五")])

    def test_dynamic_intermediate_precision_remains_open(self) -> None:
        self.assertEqual(
            self.data["status"],
            "CROSS_YEAR_FINAL_TIME_VALIDATION_CLOSED_DYNAMIC_STAGE_PRECISION_GENERALIZATION_OPEN",
        )
        adj = self.data["adjudication"]
        self.assertEqual(
            adj["d1_cross_year_final_time_operational_consistency"],
            "CLOSED_56_OF_56_MODERN_COMPARISON_TO_SURVIVING_MING_ALMANAC_TIME_BINS",
        )
        self.assertEqual(adj["dynamic_intermediate_precision_policy"], "OPEN")
        self.assertFalse(adj["universalize_1596_widths"])

    def test_g05_status_does_not_change(self) -> None:
        gates = {g["gate_id"]: g for g in self.ou["gates"]}
        g05 = gates["MD-G05-DYNAMIC-D1-PRECISION-GENERALIZATION"]
        self.assertEqual(g05["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(
            g05["batch_12ow_refinement"]["final_time_operational_validation"],
            "CLOSED_56_OF_56_D1_WITHIN_PRINTED_BINS",
        )
        self.assertEqual(
            g05["batch_12ow_refinement"]["dynamic_intermediate_precision_profile"],
            "OPEN_NOT_UNIQUELY_IDENTIFIED",
        )

    def test_runtime_firewalls_remain_closed(self) -> None:
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["production_default_changed"])
        self.assertFalse(self.data["algorithm_reopen_authorized"])
        self.assertFalse(self.data["candidate_collapse_authorized"])

    def test_accounting_unchanged(self) -> None:
        a = self.data["accounting"]
        self.assertEqual(a["matrix_rows"], 222)
        self.assertEqual(a["audited_rows"], 222)
        self.assertEqual(a["current_missing_from_product_rows"], 4)
        self.assertEqual(a["provenance_defects_confirmed"], 45)
        self.assertEqual(a["provenance_defects_repaired"], 45)
        self.assertEqual(a["algorithm_reopens"], 0)
        self.assertEqual(a["candidate_collapses"], 0)

if __name__ == "__main__":
    unittest.main()

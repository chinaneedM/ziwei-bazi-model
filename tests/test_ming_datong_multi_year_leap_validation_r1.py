from __future__ import annotations

import importlib.util
import json
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "research_ming_datong_multi_year_leap_validation_r1.py"
RESEARCH = ROOT / "docs" / "research" / "MING-DATONG-MULTI-YEAR-LEAP-RULE-VALIDATION-R1.json"
OU = ROOT / "docs" / "research" / "MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json"

spec = importlib.util.spec_from_file_location("multi_year_leap", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MingDatongMultiYearLeapValidationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = module.run(ROOT)
        cls.research = json.loads(RESEARCH.read_text(encoding="utf-8"))
        cls.ou = json.loads(OU.read_text(encoding="utf-8"))

    def test_all_sample_years_match_under_all_profiles(self) -> None:
        self.assertEqual(self.result["profile_count"], 4)
        self.assertEqual(self.result["sample_year_count"], 7)
        self.assertEqual(self.result["profile_year_control_count"], 28)
        self.assertEqual(self.result["matched_profile_year_controls"], 28)
        self.assertTrue(self.result["all_profile_year_controls_match"])

    def test_known_leap_months_are_reproduced(self) -> None:
        by_year = {}
        for item in self.result["controls"]:
            by_year.setdefault(item["year"], set()).add(item["generated_leap_month"])
        self.assertEqual(by_year[1531], {6})
        self.assertEqual(by_year[1596], {8})
        self.assertEqual(by_year[1629], {4})
        for year in (1532, 1578, 1616, 1639):
            self.assertEqual(by_year[year], {None})

    def test_1596_exposes_old_datong_day_level_semantics(self) -> None:
        self.assertEqual(self.result["1596_day_level_leap_month"], 8)
        self.assertEqual(self.result["1596_exact_time_counterfactual_leap_month"], 9)
        self.assertTrue(self.result["1596_zhongqi10_and_next_conjunction_same_day"])
        gap_hours = Decimal(self.result["1596_zhongqi10_precedes_next_conjunction_hours"])
        self.assertGreater(gap_hours, Decimal("2"))
        self.assertLess(gap_hours, Decimal("3"))

    def test_g09_remains_open_pending_boundary_census(self) -> None:
        self.assertEqual(self.research["status"], "LEAP_EXISTENCE_AND_DAY_LEVEL_PLACEMENT_SAMPLE_VALIDATED_G09_REMAINS_OPEN_PENDING_MING_ERA_BOUNDARY_SWEEP")
        adj = self.research["adjudication"]
        self.assertEqual(adj["leap_year_existence_subrule"], "CLOSED_SOURCE_SCOPED_PRIMARY_1569")
        self.assertEqual(adj["old_datong_day_level_no_zhongqi_placement_subrule"], "CLOSED_SOURCE_SCOPED_RECEIVED_SEMANTIC_BRIDGE_PLUS_MULTI_YEAR_REPLAY")
        self.assertEqual(adj["sampled_multi_year_validation"], "CLOSED_28_OF_28_PROFILE_YEAR_CONTROLS")
        self.assertEqual(adj["g09_status_after_batch"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        gates = {item["gate_id"]: item for item in self.ou["gates"]}
        self.assertEqual(gates["MD-G09-MULTI-YEAR-LEAP-GENERALIZATION"]["status"], "CLOSED_SOURCE_SCOPED")\n        self.assertEqual(gates["MD-G09-MULTI-YEAR-LEAP-GENERALIZATION"]["batch_12pb_refinement"]["profile_year_controls"], "60_OF_60_MATCH")

    def test_runtime_and_accounting_firewalls(self) -> None:
        self.assertFalse(self.research["runtime_selection_authorized"])
        self.assertFalse(self.research["production_default_changed"])
        self.assertFalse(self.research["algorithm_reopen_authorized"])
        self.assertFalse(self.research["candidate_collapse_authorized"])
        a = self.research["accounting"]
        self.assertEqual((a["matrix_rows"], a["audited_rows"], a["current_missing_from_product_rows"]), (222, 222, 4))
        self.assertEqual((a["provenance_defects_confirmed"], a["provenance_defects_repaired"]), (45, 45))
        self.assertEqual((a["algorithm_reopens"], a["candidate_collapses"]), (0, 0))


if __name__ == "__main__":
    unittest.main()

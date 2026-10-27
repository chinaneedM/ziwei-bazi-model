from __future__ import annotations

import importlib.util
import json
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "research_ming_datong_d1_precision_profile_sensitivity_r1.py"
RESEARCH = ROOT / "docs" / "research" / "MING-DATONG-D1-PRECISION-PROFILE-SENSITIVITY-R1.json"
OU = ROOT / "docs" / "research" / "MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json"

spec = importlib.util.spec_from_file_location("d1_precision_profile_harness", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MingDatongD1PrecisionProfileSensitivityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = module.run(ROOT)
        cls.research = json.loads(RESEARCH.read_text(encoding="utf-8"))
        cls.ou = json.loads(OU.read_text(encoding="utf-8"))

    def test_existing_1578_source_replay_is_exact_regression(self) -> None:
        self.assertEqual(self.result["reference_1578_exact_matches"], 13)
        self.assertEqual(self.research["internal_regression"]["expected_exact_true_conjunction_matches"], 13)

    def test_all_four_profiles_match_all_56_printed_bins(self) -> None:
        self.assertEqual(self.result["all_profiles_in_all_bins"], 56)
        for counts in self.result["profile_counts"].values():
            self.assertEqual(counts["in_bin"], 56)
            self.assertEqual(counts["out_of_bin"], 0)

    def test_profile_spread_is_far_below_observation_resolution(self) -> None:
        spread = self.result["max_profile_spread"]
        margin = self.result["minimum_edge_margin"]
        ratio = Decimal(self.result["edge_margin_to_profile_spread_ratio"])
        self.assertEqual((spread["year"], spread["month"]), (1639, "四"))
        self.assertLess(Decimal(spread["day"]), Decimal("0.0000011"))
        self.assertLess(Decimal(spread["seconds"]), Decimal("0.10"))
        self.assertEqual((margin["year"], margin["month"]), (1604, "正"))
        self.assertGreater(Decimal(margin["day"]), Decimal("0.00015"))
        self.assertGreater(Decimal(margin["seconds"]), Decimal("13"))
        self.assertGreater(ratio, Decimal("150"))

    def test_negative_discrimination_result_does_not_close_g05(self) -> None:
        adj = self.research["adjudication"]
        self.assertFalse(adj["final_time_corpus_discriminates_dynamic_precision_profiles"])
        self.assertFalse(adj["universal_1596_profile_authorized"])
        self.assertFalse(adj["numerical_fit_as_historical_authority"])
        self.assertEqual(adj["g05_status_after_batch"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        gates = {row["gate_id"]: row for row in self.ou["gates"]}
        g05 = gates["MD-G05-DYNAMIC-D1-PRECISION-GENERALIZATION"]
        self.assertEqual(g05["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g05["batch_12ox_refinement"]["corpus_discrimination_result"], "NEGATIVE_ALL_4_PROFILES_MATCH_56_OF_56")

    def test_runtime_and_accounting_firewalls_remain_closed(self) -> None:
        self.assertFalse(self.research["runtime_selection_authorized"])
        self.assertFalse(self.research["production_default_changed"])
        self.assertFalse(self.research["algorithm_reopen_authorized"])
        self.assertFalse(self.research["candidate_collapse_authorized"])
        a = self.research["accounting"]
        self.assertEqual(a["matrix_rows"], 222)
        self.assertEqual(a["audited_rows"], 222)
        self.assertEqual(a["current_missing_from_product_rows"], 4)
        self.assertEqual(a["provenance_defects_confirmed"], 45)
        self.assertEqual(a["provenance_defects_repaired"], 45)
        self.assertEqual(a["algorithm_reopens"], 0)
        self.assertEqual(a["candidate_collapses"], 0)


if __name__ == "__main__":
    unittest.main()

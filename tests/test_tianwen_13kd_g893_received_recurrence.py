"""13KD safeguards against fit-only, mixed-copy, and false-rounding promotion."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"scripts/verify-tianwen-13kd-g893-received-recurrence.py"
spec=importlib.util.spec_from_file_location("tianwen13kd",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)


class ReceivedRuleBridge(unittest.TestCase):
    def setUp(self):
        self.e=json.loads((ROOT/mod.E).read_text(encoding="utf-8"))
    def test_exact_original_ten(self):
        self.assertEqual(mod.verify(self.e)["received_rule_exact_matches"],10)
    def test_formula_constant_not_refit(self):
        x=copy.deepcopy(self.e);x["historical_unit_position_candidate"]["derived"]["initial_step_microfen"]=58151
        with self.assertRaises(ValueError):mod.verify(x)
    def test_cannot_silently_change_g893_original(self):
        x=copy.deepcopy(self.e);x["exact_same_copy_replay"][0]["expected_microfen"][2]+=1
        with self.assertRaises(ValueError):mod.verify(x)
    def test_loss_mirror_not_assumed_firsthand(self):
        x=copy.deepcopy(self.e);x["indexing"]["loss_mirror_status"]="PROVED_DIRECT_FROM_MING_SHI"
        with self.assertRaises(ValueError):mod.verify(x)
    def test_ji_rounding_counterexample_retained(self):
        x=copy.deepcopy(self.e);x["ji_limit_exploration"]["four_decimal_half_up_violation_limit"]=None
        with self.assertRaises(ValueError):mod.verify(x)
    def test_no_historical_winner(self):
        x=copy.deepcopy(self.e);x["results"]["historical_cross_witness_numeric_winners"]=1
        with self.assertRaises(ValueError):mod.verify(x)
    def test_no_duplicate_witness(self):
        x=copy.deepcopy(self.e);x["source_physical_copy_count"]=3
        with self.assertRaises(ValueError):mod.verify(x)


if __name__=="__main__":
    unittest.main()

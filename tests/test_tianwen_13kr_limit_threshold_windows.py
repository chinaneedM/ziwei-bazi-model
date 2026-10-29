import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kr-limit-threshold-windows.py"
spec=importlib.util.spec_from_file_location("tw13kr",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class FractionalFloorWindow(unittest.TestCase):
 def setUp(self):self.values=copy.deepcopy(list(v.read()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.values)
 def test_valid(self):self.assertEqual(v.verify(*self.values)["status"],"PASS")
 def test_five_day_missing(self):self.values[0]["conditional_model"]["integer_day_disagreement_days"].remove(5);self.fails()
 def test_second_exact_value_wrong(self):self.values[0]["conditional_model"]["integer_day_disagreement_records"][1]["exact_trunc_limit"]=122;self.fails()
 def test_83_window_wrong(self):self.values[0]["conditional_model"]["thresholds"][0]["crossing_advance_day"]="84/30500";self.fails()
 def test_84_window_wrong(self):self.values[0]["conditional_model"]["thresholds"][1]["approx_crossing_day"]="421/61";self.fails()
 def test_fake_ancient_floor(self):self.values[0]["claim_boundaries"]["source_historic_integer_truncation_or_floor_attested"]=True;self.fails()
 def test_fabricate_index_equivalence(self):self.values[0]["claim_boundaries"]["proof_83_84_index_offset_caused_by_rounding"]=True;self.fails()
 def test_original_source_promotion(self):self.values[0]["source_identity"]["new_independent_witnesses"]=1;self.fails()
 def test_future_focus(self):
  self.values[1]["historical_audit"]["current_focus"].append("13KS future research")
  self.values[2]["binding"]["latest_research_focus_prefix"]="13KS"
  self.values[2]["binding"]["source_focus_count"]+=1
  self.assertEqual(v.verify(*self.values)["status"],"PASS")
if __name__=="__main__":unittest.main()

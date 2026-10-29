import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kq-daily-limit-rounding.py"
spec=importlib.util.spec_from_file_location("tw13kq",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class DailyRateRounding(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.load()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.a)
 def test_positive(self):self.assertEqual(v.verify(*self.a)["status"],"PASS")
 def test_820_changed(self):self.a[0]["exact_arithmetic"]["limit_base_units"]=821;self.fails()
 def test_remainder_changed(self):self.a[0]["exact_arithmetic"]["remaining_units"]=161;self.fails()
 def test_huang_original_mutation(self):self.a[0]["sources"]["huang_p75"]["positive_phrases"][1]="一日得十二限餘一百五十分今就整為二十分";self.fails()
 def test_ming_original_roi_mutation(self):self.a[0]["sources"]["ming_p12"]["roi_rgb_sha256"]="0"*64;self.fails()
 def test_denominator_mutation(self):self.a[0]["exact_arithmetic"]["approximation_surplus_limits_per_day"]="1/204";self.fails()
 def test_false_index_proof(self):self.a[0]["negative_boundaries"]["historic_index_base_selected"]=True;self.fails()
 def test_false_one_limit_cause(self):self.a[0]["negative_boundaries"]["rounding_was_the_only_source_of_one_limit_offset"]=True;self.fails()
 def test_future_focus(self):
  self.a[1]["historical_audit"]["current_focus"].append("13KR future analysis")
  self.a[2]["binding"]["source_focus_count"]+=1
  self.a[2]["binding"]["latest_research_focus_prefix"]="13KR"
  self.assertEqual(v.verify(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()

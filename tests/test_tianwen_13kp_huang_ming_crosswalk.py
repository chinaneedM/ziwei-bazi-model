import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kp-huang-ming-crosswalk.py"
spec=importlib.util.spec_from_file_location("tw13kp",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class OriginalIndexCrosswalk(unittest.TestCase):
 def setUp(self):self.args=copy.deepcopy(list(v.load()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.args)
 def test_positive(self):self.assertEqual(v.verify(*self.args)["status"],"PASS")
 def test_huang_167_mutation(self):self.args[0]["sources"]["huang"]["original_glyphs"][1]="已上者置一百六十八限以所得限減之餘為末限";self.fails()
 def test_ming_168_mutation(self):self.args[0]["sources"]["ming"]["original_glyphs"][2]="已上轉減一百六十七限餘為末";self.fails()
 def test_ming_roi_hash_mutation(self):self.args[0]["sources"]["ming"]["roi_rgb_sha256"]="0"*64;self.fails()
 def test_offset_branch_mutation(self):self.args[0]["counterfactual"]["samples"][3]["ming_minus_huang"]=0;self.fails()
 def test_false_full_equivalence(self):self.args[0]["mathematical_boundaries"]["historical_full_formula_equivalence_proven"]=True;self.fails()
 def test_false_physical_impression(self):self.args[0]["source_boundaries"]["verified_exact_independent_physical_impressions"]=True;self.fails()
 def test_still_open(self):self.args[0]["source_boundaries"]["verified_g893_six_variant_winners"]=1;self.fails()
 def test_future_focus_append_only(self):
  self.args[1]["historical_audit"]["current_focus"].append("13KQ future analysis")
  self.args[2]["binding"]["source_focus_count"]+=1
  self.args[2]["binding"]["latest_research_focus_prefix"]="13KQ"
  self.assertEqual(v.verify(*self.args)["status"],"PASS")
if __name__=="__main__":unittest.main()

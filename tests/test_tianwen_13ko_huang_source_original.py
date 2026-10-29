import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13ko-huang-source-original.py"
spec=importlib.util.spec_from_file_location("tw13ko",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class TestHuangOriginalP79P80(unittest.TestCase):
 def setUp(self):self.data=copy.deepcopy(list(v.load()))
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.data)
 def test_positive(self):self.assertEqual(v.verify(*self.data)["status"],"PASS")
 def test_167_glyph_mutation(self):self.data[0]["original_regions"][2]["original"][1]="已上者置一百六十八限以所得限減之餘為末限";self.bad()
 def test_operator_mutation(self):self.data[0]["original_regions"][0]["original"][1]="損加之即為次日損益分";self.bad()
 def test_rgb_pixel_mutation(self):self.data[0]["original_regions"][2]["rgb_sha256"]="0"*64;self.bad()
 def test_83_boundary_promotion(self):self.data[0]["unproven"]["complete_83_84_limit_semantics"]=False;self.bad()
 def test_edition_upgrade(self):self.data[0]["source"]["physical_copy_or_impression_authenticated"]=True;self.bad()
 def test_independent_copy_upgrade(self):self.data[0]["unproven"]["independent_second_witness"]=False;self.bad()
 def test_future_append_only(self):
  self.data[1]["historical_audit"]["current_focus"].append("13KP FUTURE research")
  self.data[2]["binding"]["source_focus_count"]+=1
  self.data[2]["binding"]["latest_research_focus_prefix"]="13KP"
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()

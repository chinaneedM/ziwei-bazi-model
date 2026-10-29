import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13km-shanghai-p75p79.py"
spec=importlib.util.spec_from_file_location("tw13km",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ShanghaiOriginalP75P79(unittest.TestCase):
 def setUp(self):self.data=copy.deepcopy(list(v.load()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.data)
 def test_original_positive_only(self):self.assertEqual(v.verify(*self.data)["status"],"PASS")
 def test_source_sha_mutation(self):self.data[0]["source"]["pdf_sha256"]="0"*64;self.fails()
 def test_168_to_167_mutation(self):self.data[0]["positive_original_image_regions"][0]["positive_glyphs"][0]="中限一百六十七";self.fails()
 def test_original_roi_change(self):self.data[0]["positive_original_image_regions"][2]["rect_rgb_sha256"]="0"*64;self.fails()
 def test_false_same_mechanism(self):self.data[0]["interpretation_boundaries"]["huang_received_益加損減_same_step_as_dayanscope_proven"]=True;self.fails()
 def test_false_1923_identity(self):self.data[0]["interpretation_boundaries"]["physical_manuscript_or_1923_identity_proven"]=True;self.fails()
 def test_future_append_only(self):
  self.data[1]["historical_audit"]["current_focus"].append("13KN FUTURE research")
  self.data[2]["binding"]["latest_research_focus_prefix"]="13KN"
  self.data[2]["binding"]["source_focus_count"]+=1
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()

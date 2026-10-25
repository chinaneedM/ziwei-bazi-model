import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gv",R/"scripts/verify-tianwen-13gv-day14-heading-scope.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SourceHeader(unittest.TestCase):
 def setUp(self): self.e=json.loads(m.P.read_text(encoding="utf8"))
 def test_original_label_is_bounded(self): self.assertTrue(m.verify(self.e))
 def test_invented_fourfen_rejected(self):
  self.e["still_unresolved"]["same_day_fourfen_row"]="四分六六三〇"
  with self.assertRaises(AssertionError):m.verify(self.e)
 def test_false_label_rejected(self):
  self.e["bounded_visual_review"]["visible_label"]="十三日"
  with self.assertRaises(AssertionError):m.verify(self.e)
 def test_wrong_source_region_rejected(self):
  self.e["bounded_visual_review"]["source_native_xyxy"][0]+=1
  with self.assertRaises(AssertionError):m.verify(self.e)
 def test_incorrect_source_rgb_rejected(self):
  self.e["original_source"]["permanent_context_rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.verify(self.e)
 def test_false_independent_copy_rejected(self):
  self.e["quantitative_guards"]["new_physical_copies"]=1
  with self.assertRaises(AssertionError):m.verify(self.e)
 def test_wrong_unit_certification_rejected(self):
  self.e["still_unresolved"]["historical_fourfen_chudu_unit"]="秒"
  with self.assertRaises(AssertionError):m.verify(self.e)
if __name__=="__main__":unittest.main()

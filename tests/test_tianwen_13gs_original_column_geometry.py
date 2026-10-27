import copy,importlib.util,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("gs",P/"scripts/verify-tianwen-13gs-original-column-geometry.py")
mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
class TestOriginalGeometry(unittest.TestCase):
 def setUp(self):self.data=json.loads(mod.E.read_text(encoding="utf8"))
 def test_native_source_and_disjoint_lane(self):self.assertEqual(len(mod.check(self.data)["rects"]),5)
 def test_false_number_promotion_rejected(self):
  self.data["evaluation"]["complete_day14_fourfen"]="四分六六三〇"
  with self.assertRaises(AssertionError):mod.check(self.data)
 def test_off_by_one_lower_start_rejected(self):
  self.data["rects"][1]["box"][1]=821
  with self.assertRaises(AssertionError):mod.check(self.data)
 def test_neighbor_overlap_rejected(self):
  self.data["rects"][3]["box"][0]=170
  with self.assertRaises(AssertionError):mod.check(self.data)
 def test_false_independent_source_rejected(self):
  self.data["counters"]["new_original_witnesses"]=1
  with self.assertRaises(AssertionError):mod.check(self.data)
 def test_false_heading_numeric_alignment_rejected(self):
  self.data["prior_date_heading_numeric_right_edges"]["day14"]=170
  with self.assertRaises(AssertionError):mod.check(self.data)
if __name__=="__main__":unittest.main()

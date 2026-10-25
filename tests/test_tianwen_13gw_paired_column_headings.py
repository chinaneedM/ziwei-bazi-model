import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("gw",ROOT/"scripts/verify-tianwen-13gw-paired-column-headings.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Headers(unittest.TestCase):
 def setUp(self):self.v=json.loads(m.E.read_text(encoding="utf8"))
 def test_headers_still_numeric_null(self):self.assertEqual(m.check(self.v)["certified_numeric_rows"],0)
 def test_false_fourfen_value(self):
  self.v["inference_firewall"]["d14_fourfen_complete_literal"]="四分六六三〇"
  with self.assertRaises(AssertionError):m.check(self.v)
 def test_false_mechanical_equivalence(self):
  self.v["inference_firewall"]["fourfen_chudu_are_mechanical_identical"]=True
  with self.assertRaises(AssertionError):m.check(self.v)
 def test_false_independent_copy(self):
  self.v["counters"]["new_independent_witnesses"]=1
  with self.assertRaises(AssertionError):m.check(self.v)
 def test_forged_source_image(self):
  self.v["source"]["source_image_rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(self.v)
 def test_merged_neighbor_column(self):
  self.v["scope"][1]["source_xyxy"][0]=170
  with self.assertRaises(AssertionError):m.check(self.v)
 def test_false_ancient_unit(self):
  self.v["inference_firewall"]["original_ancient_unit"]="秒"
  with self.assertRaises(AssertionError):m.check(self.v)
if __name__=="__main__":unittest.main()

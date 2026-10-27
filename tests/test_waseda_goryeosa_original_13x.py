import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-waseda-goryeosa-original-13x.py"
s=importlib.util.spec_from_file_location("n13x",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class NativeWaseda13X(unittest.TestCase):
 def test_baseline(self):self.assertTrue(m.check(m.read()))
 def test_source_original_title_not_fabricated(self):
  e=copy.deepcopy(m.read());e["original_title"]="高麗史五十三"
  with self.assertRaises(AssertionError):m.check(e)
 def test_d16_glyph_not_fabricated(self):
  e=copy.deepcopy(m.read());e["direct_readings"]["day16"]["short"]="五分二三六二"
  with self.assertRaises(AssertionError):m.check(e)
 def test_d18_cumulative_not_fabricated(self):
  e=copy.deepcopy(m.read());e["direct_readings"]["day18"]["cumulative_original"]="八千四百二十四六四〇八"
  with self.assertRaises(AssertionError):m.check(e)
 def test_no_inflated_witnesses(self):
  e=copy.deepcopy(m.read());e["adjudication"]["independent_final_numeric_votes_added"]=1
  with self.assertRaises(AssertionError):m.check(e)
if __name__=="__main__":unittest.main()

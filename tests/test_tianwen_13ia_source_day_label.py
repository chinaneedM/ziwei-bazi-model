import unittest,copy,json,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/"scripts/verify-tianwen-13ia-source-day-label.py"
S=importlib.util.spec_from_file_location("a",P);M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class Gate(unittest.TestCase):
 def setUp(self):self.d=json.loads(M.E.read_text(encoding="utf8"))
 def test_real(self):self.assertTrue(M.check(self.d))
 def test_false_original_waseda_D17(self):
  d=copy.deepcopy(self.d);d["original_printed"][1]["rows"][0]["day"]=17
  with self.assertRaises(AssertionError):M.check(d,False)
 def test_must_not_strip_modern_three(self):
  d=copy.deepcopy(self.d);d["official_modern"][1]["raw"]="八千四百二十四六四〇八"
  with self.assertRaises(AssertionError):M.check(d,False)
 def test_source_frozen(self):
  d=copy.deepcopy(self.d);d["frozen_sources"][0]["sha"]="0"*40
  with self.assertRaises(AssertionError):M.check(d,False)
if __name__=="__main__":unittest.main()

import unittest,copy,json,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("t13ic",R/"scripts/verify-tianwen-13ic-legacy-day-erratum.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class Gate(unittest.TestCase):
 def setUp(self):self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_current(self):self.assertTrue(M.check(self.e))
 def test_stale_day(self):
  e=copy.deepcopy(self.e);e["corrections"][0]["new_day"]=17
  with self.assertRaises(AssertionError):M.check(e,False)
 def test_crossholding_old_shift(self):
  e=copy.deepcopy(self.e);e["new_cross_holding_local_d18_c_offset"]=1
  with self.assertRaises(AssertionError):M.check(e,False)
 def test_source_frozen(self):
  e=copy.deepcopy(self.e);e["frozen_dependencies"][1]["sha"]="0"*40
  with self.assertRaises(AssertionError):M.check(e,False)
 def test_roi_corruption(self):
  e=copy.deepcopy(self.e);e["corrections"][1]["overlap_pixels"]=0
  with self.assertRaises(AssertionError):M.check(e,False)
 def test_modern_three_preserved(self):
  e=copy.deepcopy(self.e);e["strict"]["NIKH_modern_D18_raw"]="八千四百二十四六四〇八"
  with self.assertRaises(AssertionError):M.check(e,False)
if __name__=="__main__":unittest.main()

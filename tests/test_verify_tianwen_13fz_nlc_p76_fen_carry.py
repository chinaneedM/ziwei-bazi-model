import copy, importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify13fz",ROOT/"scripts/verify-tianwen-13fz-nlc-p76-fen-carry.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13FZ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.read(m.E);cls.fy=m.read(m.FY);cls.l=m.read(m.L);cls.s=m.read(m.S)
 def check(self,e):return m.check(e,self.fy,self.l,self.s)
 def test_source_original_carry(self):self.assertTrue(self.check(self.e))
 def test_no_fabricated_day30(self):
  x=copy.deepcopy(self.e);x["unresolved"]["nlc_day30_exact_original"]="九二二二"
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_still_four_prefix_on_day35(self):
  x=copy.deepcopy(self.e);x["direct_original_rows"][3]["prefix"]="四"
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_false_carry_integer(self):
  x=copy.deepcopy(self.e);x["direct_original_rows"][3]["numeric_10000_grid"]=40032
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_wrong_source_crop_sha(self):
  x=copy.deepcopy(self.e);x["direct_original_rows"][4]["roi_rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_historical_unit_winner(self):
  x=copy.deepcopy(self.e);x["unresolved"]["historic_unit_bridge"]="PROVED"
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_algorithm_reopen(self):
  x=copy.deepcopy(self.e);x["counts"]["algorithm_reopens"]=1
  with self.assertRaises(AssertionError):self.check(x)
if __name__=="__main__":unittest.main()

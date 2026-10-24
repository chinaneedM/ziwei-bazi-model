import copy, importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify13ga",ROOT/"scripts/verify-tianwen-13ga-nlc-p76-d26-d28.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13GA(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.read(m.E);cls.fy=m.read(m.FY);cls.fz=m.read(m.FZ);cls.l=m.read(m.L);cls.s=m.read(m.S)
 def check(self,e): return m.check(e,self.fy,self.fz,self.l,self.s)
 def test_positive(self): self.assertTrue(self.check(self.e))
 def test_reject_day30_fill(self):
  a=copy.deepcopy(self.e);a["day30_boundary"]["day30_complete_source_glyph"]="九二二二"
  with self.assertRaises(AssertionError): self.check(a)
 def test_reject_digit_inference(self):
  a=copy.deepcopy(self.e);a["direct_original_rows"][1]["remainder"]="八七三七"
  with self.assertRaises(AssertionError): self.check(a)
 def test_reject_heading_swap(self):
  a=copy.deepcopy(self.e);a["direct_original_rows"][1]["source_heading"]="二十八日"
  with self.assertRaises(AssertionError): self.check(a)
 def test_reject_source_hash(self):
  a=copy.deepcopy(self.e);a["direct_original_rows"][0]["heading_rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError): self.check(a)
 def test_reject_false_independent_witness(self):
  a=copy.deepcopy(self.e);a["counts"]["new_ancient_witnesses"]=1
  with self.assertRaises(AssertionError): self.check(a)
 def test_reject_hist_unit_winner(self):
  a=copy.deepcopy(self.e);a["unresolved"]["historical_numerical_unit_bridge"]="PROVEN"
  with self.assertRaises(AssertionError): self.check(a)
if __name__=="__main__": unittest.main()

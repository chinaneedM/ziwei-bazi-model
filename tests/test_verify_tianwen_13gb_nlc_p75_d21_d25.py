import copy, importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify13gb",ROOT/"scripts/verify-tianwen-13gb-nlc-p75-d21-d25.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13GB(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.read(m.E);cls.ga=m.read(m.GA);cls.fu=m.read(m.FU);cls.l=m.read(m.L);cls.s=m.read(m.S)
 def check(self,e):return m.check(e,self.ga,self.fu,self.l,self.s)
 def test_source_positive(self):self.assertTrue(self.check(self.e))
 def test_reject_day30_fabrication(self):
  x=copy.deepcopy(self.e);x["unresolved"]["NLC_day30_exact_original"]="四分九二二二"
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_crosspage_false_step(self):
  x=copy.deepcopy(self.e);x["cross_page"]["neighbor_differences"][-1]=163
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_source_heading_shift(self):
  x=copy.deepcopy(self.e);x["direct_original_rows"][2]["source_heading"]="二十四日"
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_roi_mutation(self):
  x=copy.deepcopy(self.e);x["direct_original_rows"][1]["roi_rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_unit_promotion(self):
  x=copy.deepcopy(self.e);x["unresolved"]["historic_unit_equivalence"]="PROVEN"
  with self.assertRaises(AssertionError):self.check(x)
 def test_reject_witness_inflation(self):
  x=copy.deepcopy(self.e);x["counts"]["new_ancient_physical_witnesses"]=1
  with self.assertRaises(AssertionError):self.check(x)
if __name__=="__main__":unittest.main()

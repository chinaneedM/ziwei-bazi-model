import copy, importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify13gc",ROOT/"scripts/verify-tianwen-13gc-nlc-p75-d17-d20.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13GC(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.fu=m.read(m.FU);cls.gb=m.read(m.GB);cls.l=m.read(m.L);cls.s=m.read(m.S)
 def check(self,e):return m.check(e,self.fu,self.gb,self.l,self.s)
 def reject(self,k,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):self.check(x)
 def test_positive(self):self.assertTrue(self.check(self.e))
 def test_reject_day30_guess(self):self.reject("D30",lambda e:e["unresolved"].update(NLC_day30_exact_original="四分九二二二"))
 def test_reject_digit(self):self.reject("glyph",lambda e:e["direct_original_rows"][2].update(remainder="七四四二"))
 def test_reject_heading(self):self.reject("heading",lambda e:e["direct_original_rows"][3].update(source_heading="二十一日"))
 def test_reject_hash(self):self.reject("hash",lambda e:e["direct_original_rows"][0].update(roi_rgb_sha256="0"*64))
 def test_reject_progression(self):self.reject("progression",lambda e:e["continuity"]["neighbor_differences"].__setitem__(0,161))
 def test_reject_unit_promotion(self):self.reject("unit",lambda e:e["unresolved"].update(historic_unit_equivalence="PROVEN"))
 def test_reject_physical_witness_inflation(self):self.reject("witness",lambda e:e["counts"].update(new_ancient_physical_witnesses=1))
if __name__=="__main__":unittest.main()

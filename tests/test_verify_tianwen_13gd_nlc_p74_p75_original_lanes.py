import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v13gd",ROOT/"scripts/verify-tianwen-13gd-nlc-p74-p75-original-lanes.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13GD(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.l=m.read(m.L);cls.s=m.read(m.S);cls.fu=m.read(m.FU);cls.gb=m.read(m.GB)
 def check(self,e):return m.check(e,self.l,self.s,self.fu,self.gb)
 def reject(self,mutator):
  e=copy.deepcopy(self.e);mutator(e)
  with self.assertRaises(AssertionError):self.check(e)
 def test_positive(self):self.assertTrue(self.check(self.e))
 def test_day9_not_guess(self):self.reject(lambda e:e["non_adjudicated_original_scopes"][0].update(complete_source_original_literal="四分五八二〇"))
 def test_day14_not_interpolate(self):self.reject(lambda e:e["cross_original"].update(p74_to_p75_d13_d15_gap_day14_original="四分六六三〇"))
 def test_day30_not_fill(self):self.reject(lambda e:e["unresolved"].update(NLC_day30_exact_original="四分九二二二"))
 def test_reject_row_glyph(self):self.reject(lambda e:e["positive_source_rows"][0].update(remainder="五九八三"))
 def test_reject_roi_hash(self):self.reject(lambda e:e["positive_source_rows"][1].update(roi_rgb_sha256="0"*64))
 def test_reject_false_unit(self):self.reject(lambda e:e["unresolved"].update(historic_unit_equivalence="PROVEN"))
 def test_reject_witness_inflation(self):self.reject(lambda e:e["counts"].update(new_ancient_physical_witnesses=1))
 def test_reject_false_step(self):self.reject(lambda e:e["cross_original"]["p74_local_differences"].__setitem__(0,163))
if __name__=="__main__":unittest.main()

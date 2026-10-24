import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify13ge",ROOT/"scripts/verify-tianwen-13ge-nlc416-1909-p152.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13GE(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.s=m.read(m.S);cls.l=m.read(m.L);cls.fy=m.read(m.FY);cls.fx=m.read(m.FX);cls.dd=m.read(m.DD)
 def check(self,e):return m.check(e,self.s,self.l,self.fy,self.fx,self.dd)
 def reject(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.check(e)
 def test_source_positive(self):self.assertTrue(self.check(self.e))
 def test_reject_1909_source_d30_change(self):self.reject(lambda e:e["source_original_rows"][1].update(digits="九二二一"))
 def test_reject_1909_source_heading_shift(self):self.reject(lambda e:e["source_original_rows"][2].update(source_heading="三十日"))
 def test_reject_source_hash_mutation(self):self.reject(lambda e:e["source_original_rows"][1].update(roi_rgb_sha256="0"*64))
 def test_reject_NLC_old_d30_promotion(self):self.reject(lambda e:e["source_scoped_comparison"].update(NLC_03130_original_day30="四分九二二二"))
 def test_reject_source_unit_promotion(self):self.reject(lambda e:e["unresolved"].update(ancient_fourfen_chudu_unit_bridge="PROVEN"))
 def test_reject_ancient_witness_inflation(self):self.reject(lambda e:e["counts"].update(new_ancient_physical_witnesses=1))
 def test_reject_fake_step(self):self.reject(lambda e:e["arithmetic"]["integer_grid_steps"].__setitem__(0,163))
if __name__=="__main__":unittest.main()

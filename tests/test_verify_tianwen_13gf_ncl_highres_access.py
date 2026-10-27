import copy,importlib.util,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v13gf",R/"scripts/verify-tianwen-13gf-ncl-highres-access.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13GF(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L);cls.gd=m.load(m.GD);cls.ge=m.load(m.GE)
 def ck(self,e):return m.check(e,self.s,self.l,self.gd,self.ge)
 def reject(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):self.ck(x)
 def test_positive(self):self.assertTrue(self.ck(self.e))
 def test_unseen_old_day30(self):self.reject(lambda x:x["unresolved"].update(old_d30="四分九二二二"))
 def test_no_approval(self):self.reject(lambda x:x["official_policy"][0].update(specific_target_approved=True))
 def test_no_license(self):self.reject(lambda x:x["official_policy"][1].update(republication_license=True))
 def test_no_leaf_guess(self):self.reject(lambda x:x["catalog_description"].update(source_specific_folio_id="guessed"))
 def test_no_reg_inflation(self):self.reject(lambda x:x["counts"].update(new_source_registry_entries=1))
if __name__=="__main__":unittest.main()

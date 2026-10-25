import copy,importlib.util,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("s13gh",R/"scripts/verify-tianwen-13gh-ncl-faq.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Test13GH(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def ck(self,x):return m.check(x,self.s,self.l)
 def reject(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):self.ck(x)
 def test_positive(self):self.assertTrue(self.ck(self.e))
 def test_no_old_d30_guess(self):self.reject(lambda x:x["unverified_item"].update(target_d30_original="四分九二二二"))
 def test_no_catalog_identity_guess(self):self.reject(lambda x:x["unverified_item"].update(firstparty_physical_item_id="20803130"))
 def test_no_remote_copy_claim(self):self.reject(lambda x:x["verified_policy"].update(onsite_form_is_not_proven_remote_copy_order=False))
 def test_no_applicant_or_payment(self):self.reject(lambda x:x["request_manifest"].update(submitted=True))
 def test_no_image_claim(self):self.reject(lambda x:x["negative_guards"].update(new_original_images=1))
 def test_no_lineage_inflation(self):self.reject(lambda x:x["negative_guards"].update(new_genealogy_nodes=1))
if __name__=="__main__":unittest.main()

import copy,importlib.util,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("v13gi",R/"scripts/verify-tianwen-13gi-ncl-catalog-gate.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13GI(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def reject(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):m.check(x,self.s,self.l)
 def test_positive(self):self.assertTrue(m.check(self.e,self.s,self.l))
 def test_no_csv_target_premature(self):self.reject(lambda x:x["retrieval"].update(target_record_observed=True))
 def test_no_target_d30_guess(self):self.reject(lambda x:x["targets"].update(d30="四分九二二二"))
 def test_no_physical_id_guess(self):self.reject(lambda x:x["targets"].update(exact_physical_copy_identifier="03130"))
 def test_no_source_inflation(self):self.reject(lambda x:x["counts"].update(new_sources=1))
 def test_no_fake_dataset_sha(self):self.reject(lambda x:x["retrieval"].update(dataset_snapshot_sha256="fake"))
if __name__=="__main__":unittest.main()

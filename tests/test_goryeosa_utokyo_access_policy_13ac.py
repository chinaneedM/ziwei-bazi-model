import importlib.util,copy,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-utokyo-access-policy-13ac.py"
spec=importlib.util.spec_from_file_location("utokyo13ac",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class UTokyoScopedPolicy(unittest.TestCase):
 def test_source_scope(self):self.assertTrue(m.check())
 def test_no_specific_storage_from_generic_rule(self):
  d=copy.deepcopy(m.load(m.E));d["target_item"]["exact_storage_location"]="保存書庫（和漢古書）"
  with self.assertRaises(AssertionError):m.check(d)
 def test_no_premature_scan_claim(self):
  d=copy.deepcopy(m.load(m.E));d["target_item"]["d16_d18_original_folio"]=10
  with self.assertRaises(AssertionError):m.check(d)
 def test_no_numeric_vote(self):
  d=copy.deepcopy(m.load(m.E));d["restrictions"]["physical_numeric_votes_added"]=1
  with self.assertRaises(AssertionError):m.check(d)
if __name__=="__main__":unittest.main()

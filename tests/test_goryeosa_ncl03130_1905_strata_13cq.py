import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-ncl03130-1905-strata-13cq.py"
spec=importlib.util.spec_from_file_location("goryeosa13cq",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13CQ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def check(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.check())
 def test_missing_list_not_read(self):
  e=copy.deepcopy(self.e);e["limits"]["missing_register_read_directly"]=True
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_juan52_filled_by_guess(self):
  e=copy.deepcopy(self.e);e["limits"]["juan52_in_missing_list"]="MISSING"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_exemplar_date_collapse(self):
  e=copy.deepcopy(self.e);e["provenance"]["juan52_original_stratum"]="1905"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_third_copy_vote(self):
  e=copy.deepcopy(self.e);e["limits"]["third_independent_d16_original_witnesses"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_future_forward_only(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.754.0";s["historical_audit"]["current_focus"].append("13CR future")
  l["binding"]["reviewed_state_version"]="1.754.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()

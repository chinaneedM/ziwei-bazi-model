import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-krdb-v52-d16-13cv.py"
spec=importlib.util.spec_from_file_location("tw13cv",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13CV(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L);cls.old=m.load(m.OLD)
 def check(self,e=None,s=None,l=None,old=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.old if old is None else old)
 def test_pass(self):self.assertTrue(self.check())
 def test_051_must_not_replace_direct_052(self):
  x=copy.deepcopy(self.e);x["first_party_direct_target"]["url"]=x["forward_only_link_erratum"]["wrong_url_as_preserved_in_13cu"]
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_16_must_remain_received_1362(self):
  x=copy.deepcopy(self.e);x["first_party_direct_target"]["adjacent_day_readings"][1]["numeric"]="5.2362"
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_arithmetic_must_remain_conjecture(self):
  x=copy.deepcopy(self.e);x["source_scope_firewalls"]["force_corrected_d16_as_printed"]=True
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_krdb_cannot_be_third_ancient_copy(self):
  x=copy.deepcopy(self.e);x["source_scope_firewalls"]["direct_third_historical_original_count_new"]=1
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_preserve_old_link_in_historical_record(self):
  x=copy.deepcopy(self.old);x["text_structure"]["url"]="https://db.history.go.kr/goryeo/level.do?levelId=kr_052_0010_0010_0020_0010&types=o"
  with self.assertRaises(AssertionError):self.check(old=x)
 def test_zhi_six_still_unresolved(self):
  x=copy.deepcopy(self.e);x["source_scope_firewalls"]["ncl_mirror_p7_zhi_range_connector"]="DECIDED"
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_state_version_continuity(self):
  s=copy.deepcopy(self.s);s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.757.0"
  with self.assertRaises(AssertionError):self.check(s=s)
if __name__=="__main__":unittest.main()

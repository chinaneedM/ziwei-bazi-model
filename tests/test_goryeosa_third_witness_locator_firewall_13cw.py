import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-third-witness-locator-firewall-13cw.py"
spec=importlib.util.spec_from_file_location("tw13cw",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13CW(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def test_baseline(self):self.assertTrue(m.check(self.e,self.s,self.l))
 def test_ncl_neighbor_not_target(self):
  e=copy.deepcopy(self.e);e["first_party_ncl_neighbor_control"]["is_target_item"]=True
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_cnts_gap_never_invented(self):
  e=copy.deepcopy(self.e);e["commons_korean_category_bounded_listing"]["proposed_identifier_verified"]=True
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_no_absence_proof(self):
  e=copy.deepcopy(self.e);e["commons_korean_category_bounded_listing"]["v52_physical_copy_presence"]="ABSENT"
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_24_digital_is_not_40_physical(self):
  e=copy.deepcopy(self.e);e["commons_taiwan_mirror_separation"]["mirror_part_count_cannot_establish_missing_fascicles"]=False
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_no_third_original(self):
  e=copy.deepcopy(self.e);e["scope"]["third_new_independent_historical_originals"]=1
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_keep_printed_1362(self):
  e=copy.deepcopy(self.e);e["scope"]["original_d16_two_holding_literal"]="5.2362"
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_all_issues_reviewed(self):
  l=copy.deepcopy(self.l);l["binding"]["source_focus_count"]-=1
  with self.assertRaises(AssertionError):m.check(self.e,self.s,l)
if __name__=="__main__":unittest.main()

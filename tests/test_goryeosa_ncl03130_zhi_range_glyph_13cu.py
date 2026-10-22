import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-ncl03130-zhi-range-glyph-13cu.py"
spec=importlib.util.spec_from_file_location("tw13cu",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Test13CU(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=mod.load(mod.E);cls.s=mod.load(mod.S);cls.l=mod.load(mod.L)
 def check(self,e=None,s=None,l=None):
  return mod.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_valid(self):self.assertTrue(self.check())
 def test_source_png_mismatch_rejected(self):
  a=copy.deepcopy(self.e);a["physical_source_boundary"]["source_png_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(e=a)
 def test_crop_digest_mismatch_rejected(self):
  a=copy.deepcopy(self.e);a["manual_red_ink_crops"][3]["rgb_sha256"]="a"*64
  with self.assertRaises(AssertionError):self.check(e=a)
 def test_range_not_promoted(self):
  a=copy.deepcopy(self.e);a["bounded_reading"]["current_option"]="A"
  with self.assertRaises(AssertionError):self.check(e=a)
 def test_six_not_claimed(self):
  a=copy.deepcopy(self.e);a["bounded_reading"]["is_zhi_six_mentioned_or_included"]="YES"
  with self.assertRaises(AssertionError):self.check(e=a)
 def test_no_new_copy_votes(self):
  a=copy.deepcopy(self.e);a["next_gate"]["third_historical_copy_votes"]=1
  with self.assertRaises(AssertionError):self.check(e=a)
 def test_no_1905_source_as_old_print(self):
  a=copy.deepcopy(self.e);a["physical_source_boundary"]["hosting"]="NCL_FIRSTPARTY_VERIFIED"
  with self.assertRaises(AssertionError):self.check(e=a)
 def test_state_sync(self):
  a=copy.deepcopy(self.s);a["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.756.0"
  with self.assertRaises(AssertionError):self.check(s=a)
if __name__=="__main__":unittest.main()

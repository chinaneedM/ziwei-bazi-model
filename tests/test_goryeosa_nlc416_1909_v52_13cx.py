import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-nlc416-1909-v52-13cx.py"
s=importlib.util.spec_from_file_location("tw13cx",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13CX(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.state=m.load(m.S);cls.ledger=m.load(m.L)
 def check(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.state if s is None else s,self.ledger if l is None else l)
 def test_pass(self):self.assertTrue(self.check())
 def test_toc_cannot_claim_glyph(self):
  x=copy.deepcopy(self.e);x["positive_concrete_volume_locator"]["v52_exact_pdf_page"]=123
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_nlc1909_not_early_original(self):
  x=copy.deepcopy(self.e);x["cross_source_firewall"]["nlc1909_new_independent_early_original"]=True
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_no_proven_pdf_offset(self):
  x=copy.deepcopy(self.e);x["publication_and_digital_surrogate"]["content_page_offset_from_pdf"]="9"
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_d16_derived_not_printed(self):
  x=copy.deepcopy(self.e);x["cross_source_firewall"]["prior_waseda_naj_direct_historical_original_d16"]="5.2362"
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_sister_88_not_v52(self):
  x=copy.deepcopy(self.e);x["nearby_series_edition_controls"][0]["catalog_start_juan"]=52
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_no_pdf_sha_fabrication(self):
  x=copy.deepcopy(self.e);x["publication_and_digital_surrogate"]["digital_pdf_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_issue_continuity(self):
  x=copy.deepcopy(self.ledger);x["binding"]["source_focus_count"]-=1
  with self.assertRaises(AssertionError):self.check(l=x)
if __name__=="__main__":unittest.main()

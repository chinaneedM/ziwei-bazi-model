#!/usr/bin/env python3
import copy,importlib.util,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify12uv",ROOT/"scripts/verify-yehuobian-kyoto-letters-inquiry-12uv.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class KyotoLettersPreflight(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
  cls.r=read(m.RECORD);cls.p=read(m.PACKET);cls.u=read(m.UM)
 def check(self,r=None,p=None,u=None):
  return m.validate(r if r is not None else self.r,p if p is not None else self.p,u if u is not None else self.u)
 def test_preflight(self):self.assertEqual(self.check()["original_juan20_items"],2)
 def test_no_email_sent(self):
  r=copy.deepcopy(self.r);r["acquisition"]["sent"]=True
  with self.assertRaises(ValueError):self.check(r)
 def test_no_paid_order(self):
  r=copy.deepcopy(self.r);r["acquisition"]["payment"]=True
  with self.assertRaises(ValueError):self.check(r)
 def test_no_copy_permission(self):
  r=copy.deepcopy(self.r);r["acquisition"]["item_specific_permission"]=True
  with self.assertRaises(ValueError):self.check(r)
 def test_188987_not_188987l(self):
  r=copy.deepcopy(self.r);r["items"][2]["role"]="JUAN20_ORIGINAL_LEAF"
  with self.assertRaises(ValueError):self.check(r)
 def test_kyoto_two_libraries_not_mixed(self):
  r=copy.deepcopy(self.r);r["items"][0]["call_number"]="B||VIb||9-1 188987L"
  with self.assertRaises(ValueError):self.check(r)
 def test_generic_archive_not_original_scan(self):
  r=copy.deepcopy(self.r);r["items"][0]["original_image_url"]="https://example.org/test.jpg"
  with self.assertRaises(ValueError):self.check(r)
 def test_1827_preface_not_original_print(self):
  r=copy.deepcopy(self.r);r["policy_boundaries"]["preface_dated_1827_not_print_impression_proof"]=False
  with self.assertRaises(ValueError):self.check(r)
 def test_2026_main_library_not_automatically_applicable(self):
  r=copy.deepcopy(self.r);r["policy_boundaries"]["main_central_library_policy_does_not_apply_automatically"]=False
  with self.assertRaises(ValueError):self.check(r)
 def test_rare_book_permission_is_conditional(self):
  r=copy.deepcopy(self.r);r["policy_boundaries"]["rare_book_form_only_if_item_specific_classification_requires"]=False
  with self.assertRaises(ValueError):self.check(r)
 def test_source_vote_must_be_zero(self):
  r=copy.deepcopy(self.r);r["acquisition"]["original_glyph_votes"]=1
  with self.assertRaises(ValueError):self.check(r)
 def test_no_unsupported_extra_historical_source(self):
  r=copy.deepcopy(self.r);r["acquisition"]["new_external_source_count"]=1
  with self.assertRaises(ValueError):self.check(r)
if __name__=="__main__":unittest.main()

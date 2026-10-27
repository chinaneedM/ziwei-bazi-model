#!/usr/bin/env python3
import unittest,copy,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("q12vc",ROOT/"scripts/verify-yehuobian-jingzhiju-quote-locator-12vc.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
class JingzhijuQuote12VC(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.docs=[load(p) for p in (m.REC,m.STATE,m.PREV)]
 def check(self,docs=None):return m.validate(*(docs or self.docs))
 def bad(self,i,path,value):
  docs=copy.deepcopy(self.docs);x=docs[i]
  for k in path[:-1]:x=x[k]
  x[path[-1]]=value
  with self.assertRaises(ValueError):self.check(docs)
 def test_baseline(self):self.assertFalse(self.check()["citation_error_disproved"])
 def test_no_physical_leaf_claim(self):self.bad(0,["prior_registered_secondary","original_leaf_id"],"1819-17")
 def test_no_complete_absence_claim(self):self.bad(0,["locator_probe",0,"complete_all_editions_verified"],True)
 def test_no_new_quote_reading(self):self.bad(0,["locator_probe",0,"wording_quoted_in_1959_present_in_this_displayed_entry"],True)
 def test_no_author_misattribution_verdict(self):self.bad(0,["firewalls","1959_author_misattribution_not_proven"],False)
 def test_unproofread_ocr_is_not_authority(self):self.bad(0,["locator_probe",1,"negative_quote_vote_authorized"],True)
 def test_do_not_equate_1819_and_1827_books(self):self.bad(0,["firewalls","1819_fulishanfang_jingzhiju_is_not_1827_yehuobian"],False)
 def test_no_original_glyph_increment(self):self.bad(0,["adjudication","new_ancient_glyph_votes"],1)
 def test_no_source_growth(self):self.bad(0,["adjudication","new_registered_sources"],1)
 def test_no_citation_error_outcome(self):self.bad(0,["adjudication","conclusion"],"PANG1959_MISQUOTE_PROVED")
 def test_state_reopens_stay_zero(self):self.assertEqual(self.docs[1]["invariants"]["algorithm_reopen_count"],0)
 def test_no_1827_page_claim(self):self.bad(0,["firewalls","exact_1827_1869_gaizao_original_pages_not_obtained"],False)
if __name__=="__main__":unittest.main()

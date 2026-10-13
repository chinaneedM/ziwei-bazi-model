#!/usr/bin/env python3
import unittest,copy,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("q12vd",ROOT/"scripts/verify-yehuobian-jingzhiju-referent-12vd.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class JingzhijuReferent12VD(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.docs=[read(p) for p in (m.REC,m.STATE,m.PREV)]
 def bad(self,i,path,val):
  docs=copy.deepcopy(self.docs);obj=docs[i]
  for k in path[:-1]:obj=obj[k]
  obj[path[-1]]=val
  with self.assertRaises(ValueError):m.validate(*docs)
 def test_pass(self):self.assertFalse(m.validate(*self.docs)["misquote_proved"])
 def test_1959_full_article_not_seen(self):self.bad(0,["passages",0,"full_article_read"],True)
 def test_original_print_leaf_unknown(self):self.bad(0,["passages",0,"exact_original_folio"],"1819-17-1")
 def test_shen_nonhit_is_scoped(self):self.bad(0,["passages",1,"contains_claimed_1959_quote"],True)
 def test_daoyuan_referent(self):self.bad(0,["passages",2,"referent"],"沈德符《萬曆野獲編》")
 def test_daoyuan_not_shen(self):self.bad(0,["passages",2,"not_referring_to"],"道源")
 def test_near_not_exact(self):self.bad(0,["collated_differences","exact_wording_match"],True)
 def test_no_citation_verdict(self):self.bad(0,["collated_differences","misquotation_proved"],True)
 def test_no_copy_claim(self):self.bad(0,["collated_differences","source_to_source_copying_proved"],True)
 def test_no_referent_transfer(self):self.bad(0,["collated_differences","referent_identity"],True)
 def test_no_unearned_glyph(self):self.bad(0,["accounting","new_glyph_votes"],1)
 def test_no_registration(self):self.bad(0,["accounting","new_registered_sources"],1)
 def test_no_external_order(self):self.bad(0,["controls","no_external_request"],False)
 def test_state_reopen(self):self.bad(1,["invariants","algorithm_reopen_count"],1)
if __name__=="__main__":unittest.main()

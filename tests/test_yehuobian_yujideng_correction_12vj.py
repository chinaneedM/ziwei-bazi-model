#!/usr/bin/env python3
import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("v12vj",ROOT/"scripts/verify-yehuobian-yujideng-correction-12vj.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class HistoricalAttributionCorrection(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.a=[v.read(p) for p in (v.DOC,v.VH,v.VI,v.STATE)]
 def bad(self,i,path,value):
  a=copy.deepcopy(self.a);x=a[i]
  for k in path[:-1]:x=x[k]
  x[path[-1]]=value
  with self.assertRaises(ValueError):v.validate(*a)
 def test_pass(self):self.assertEqual(v.validate(*self.a)["corrected_attribution_claims"],1)
 def test_cannot_rewrite_old_scope(self):self.bad(0,["supersedes_assertion_scopes",0,"old_claim"],"卷十一")
 def test_prior_preserved(self):self.bad(1,["witnesses",1,"locus"],"corrected in place")
 def test_yu_no_peng(self):self.bad(0,["scoped_evidence",0,"attributed_to_peng_in_target_paragraph"],True)
 def test_yu_numeral_retained(self):self.bad(0,["scoped_evidence",0,"winter"],"辰初二刻")
 def test_second_yu_no_peng(self):self.bad(0,["scoped_evidence",1,"attributed_to_peng_in_target_paragraph"],True)
 def test_shilu_peng(self):self.bad(0,["scoped_evidence",2,"attributed_to_peng_in_target_paragraph"],False)
 def test_shilu_explicit_text(self):self.bad(0,["scoped_evidence",2,"explicit_attribution"],"彭德清奏")
 def test_yehuobian_numeral(self):self.bad(0,["scoped_evidence",3,"summer"],"戌初一刻")
 def test_paragraph_boundary(self):self.bad(0,["scoped_evidence",0,"preceding_subject"],"彭德清奏")
 def test_no_shidian_image(self):self.bad(0,["scoped_evidence",4,"original_juan11_leaf_downloaded"],True)
 def test_not_ncl_copy(self):self.bad(0,["scoped_evidence",4,"scan_to_ncl_02253_or_02254_verified"],True)
 def test_no_direct_copying(self):self.bad(0,["philology_and_provenance_firewalls","identical_numeric_pair_not_direct_copy"],False)
 def test_no_target_image(self):self.bad(0,["target_status","original_1827_yehuobian_juan20_target_folio"],"p2")
 def test_no_original_votes(self):self.bad(0,["accounting","new_independent_original_glyph_votes"],1)
 def test_no_registry_growth(self):self.bad(0,["accounting","new_registered_sources"],1)
 def test_no_transmission_edge(self):self.bad(0,["transmission_impact","edges_supported"],["Yu copies Shilu"])
 def test_no_algorithm(self):self.bad(3,["invariants","algorithm_reopen_count"],1)
 def test_no_state_rollback(self):self.bad(3,["schema_version"],"1.565.0")
if __name__=="__main__":unittest.main()

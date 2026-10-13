#!/usr/bin/env python3
import unittest,copy,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v12vf",ROOT/"scripts/verify-yehuobian-12vf-received-and-leads.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class ForwardVariant12VF(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.docs=[read(p) for p in (m.REC,m.LEADS,m.STATE,m.PZ,m.VE)]
 def bad(self,i,path,value):
  docs=copy.deepcopy(self.docs);v=docs[i]
  for k in path[:-1]:v=v[k]
  v[path[-1]]=value
  with self.assertRaises(ValueError):m.validate(*docs)
 def test_baseline(self):self.assertEqual(m.validate(*self.docs)["secondary_unverified_leads"],3)
 def test_ji_not_drop(self):self.bad(0,["witnesses",1,"readings","PRINTING_CLAUSE"],"惜未梓")
 def test_ws_not_assumed_ji(self):self.bad(0,["witnesses",0,"readings","PRINTING_CLAUSE"],"惜未及梓")
 def test_count_separate_locus(self):self.bad(0,["loci",1,"readings","CTEXT_RECEIVED"],"十二卷")
 def test_no_original_edition(self):self.bad(0,["witnesses",1,"edition_physical_copy_identified"],True)
 def test_no_direct_ocr_read(self):self.bad(0,["forward_correction","ctext_direct_source_html_not_claimed"],False)
 def test_no_edition_winner(self):self.bad(0,["forward_correction","no_alternative_winner_selected"],False)
 def test_no_stemmatic_pairing(self):self.bad(0,["forward_correction","no_recension_pairing_proved_from_two_websites"],False)
 def test_no_original_glyph(self):self.bad(0,["loci",0,"physical_print_glyph_authority"],True)
 def test_henan_not_verified(self):self.bad(1,["leads",0,"provider_verified"],True)
 def test_qinghua_not_verified(self):self.bad(1,["leads",1,"provider_catalog_item_id"],"shelfmark")
 def test_shandong_no_unearned_leaf(self):self.bad(1,["leads",2,"image_url"],"http://example.com/image")
 def test_tsinghua_7_not_missing_juan20(self):self.bad(1,["no_inference_from_7_copies_about_juan20_missing"],False)
 def test_no_new_source_count(self):self.bad(0,["accounting","new_sources"],1)
 def test_no_ancient_votes(self):self.bad(0,["accounting","new_glyph_votes"],1)
 def test_no_new_genealogy(self):self.bad(1,["accounting","new_graph_edges"],1)
 def test_no_algorithm_reopen(self):self.bad(2,["invariants","algorithm_reopen_count"],1)
if __name__=='__main__':unittest.main()

#!/usr/bin/env python3
import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("q12vg",ROOT/"scripts/verify-yehuobian-pku1869-crosswalk-12vg.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def j(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class PKU1869Crosswalk(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.docs=[j(m.DOC),j(m.PRIOR),j(m.STATE)]
 def bad(self,i,path,value):
  args=copy.deepcopy(self.docs);d=args[i]
  for k in path[:-1]:d=d[k]
  d[path[-1]]=value
  with self.assertRaises(ValueError):m.validate(*args)
 def test_baseline(self):self.assertEqual(m.validate(*self.docs)["six_unsatisfied_evidence_gates"],6)
 def test_not_provider_item(self):self.bad(0,["candidate_1869","first_party_item_url"],"https://lib.pku.edu.cn/some-item")
 def test_no_shelfmark(self):self.bad(0,["candidate_1869","source_issued_shelfmark"],"pseudo-shelfmark")
 def test_no_physical_identifier(self):self.bad(0,["candidate_1869","first_party_physical_copy_identifier"],"fake")
 def test_no_impression_proof(self):self.bad(0,["candidate_1869","confirmed_original_1869_revised_impression"],True)
 def test_no_page(self):self.bad(0,["candidate_1869","original_juan20_folio"],"folio12a")
 def test_no_image(self):self.bad(0,["candidate_1869","source_issued_target_image_url"],"https://example.com/folio")
 def test_no_digest(self):self.bad(0,["candidate_1869","source_binary_sha256"],"0"*64)
 def test_no_gloss_vote(self):self.bad(0,["candidate_1869","four_loci","GONGJIN"],"宮禁")
 def test_no_extra_vote(self):self.bad(0,["candidate_1869","independent_target_votes"],1)
 def test_not_official_item(self):self.bad(0,["first_party_platform_evidence",0,"item_1869_confirmed"],True)
 def test_no_acquisition_step_early(self):self.bad(0,["crosswalk_requirements",3,"satisfied"],True)
 def test_same_date_not_same_plate(self):self.bad(0,["source_identity_firewalls","same_1869_catalogued_year_not_same_plate"],False)
 def test_not_two_ancient_votes(self):self.bad(0,["accounting","new_independent_glyph_votes"],1)
 def test_source_registry_not_promoted(self):self.bad(0,["accounting","new_registry_rows"],1)
 def test_no_genealogy_edge(self):self.bad(0,["accounting","new_graph_edges"],1)
 def test_original_eight_queue_locked(self):self.bad(1,["original_copy_candidates",3,"source_catalog_url"],"https://fake.example/item")
 def test_no_algorithm_reopen(self):self.bad(2,["invariants","algorithm_reopen_count"],1)
if __name__=='__main__':unittest.main()

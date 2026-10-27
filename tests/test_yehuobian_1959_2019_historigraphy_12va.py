#!/usr/bin/env python3
import unittest,copy,json,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify12va",ROOT/"scripts/verify-yehuobian-1959-2019-historiography-12va.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class HistoricalPrintDebate12VA(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.docs=[read(p) for p in (m.REC,m.SHARD,m.MAN,m.STATE,m.GRAPH,m.OLD)]
 def check(self,docs=None):return m.validate(*(self.docs if docs is None else docs))
 def bad(self,i,path,v):
  docs=copy.deepcopy(self.docs);d=docs[i]
  for p in path[:-1]:d=d[p]
  d[path[-1]]=v
  with self.assertRaises(ValueError):self.check(docs)
 def test_baseline(self):self.assertEqual(self.check()["new_scholarly_sources"],1)
 def test_different_publication_year(self):self.bad(0,["scholarly_witnesses",0,"issue"],"1827")
 def test_2019_not_doublecounted(self):self.bad(0,["scholarly_witnesses",1,"source_id"],"new-duplicate")
 def test_full_1959_unread(self):self.bad(0,["scholarly_witnesses",0,"full_article_inspected"],True)
 def test_full_2019_unread(self):self.bad(0,["scholarly_witnesses",1,"full_article_inspected"],True)
 def test_no_ming_print_existence_claim(self):self.bad(0,["claim_boundaries","1959_unresolved_discussion_is_not_ming_print_existence_proof"],False)
 def test_no_negative_physical_proof(self):self.bad(0,["claim_boundaries","2019_negative_hypothesis_is_scholarly_not_physical_nonexistence_proof"],False)
 def test_no_1619_target_assumed(self):self.bad(0,["claim_boundaries","work_1619_arrangement_not_later_themed_30volume_juan20"],False)
 def test_no_1827_glyph(self):self.bad(0,["historical_state","original_1827_target_image"],True)
 def test_no_1869_glyph(self):self.bad(0,["historical_state","original_1869_target_image"],True)
 def test_no_physical_glyph_vote(self):self.bad(1,["sources",0,"physical_glyph_authority"],True)
 def test_manifest_count(self):self.bad(2,["combined_source_count"],self.docs[2]["combined_source_count"]+1)
 def test_no_graph_promotions(self):self.bad(0,["historical_state","transmission_edges_added"],1)
 def test_no_algorithm_reopen(self):self.bad(0,["historical_state","algorithm_reopen_authorized"],True)
 def test_state_count(self):self.bad(3,["historical_audit","external_source_registry_total_unique_count"],689)
 def test_no_fake_earliest_year(self):self.bad(0,["historical_state","earliest_surviving_confirmed_print_date"],"1827")
if __name__=="__main__":unittest.main()

#!/usr/bin/env python3
import unittest,copy,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("q12ve",ROOT/"scripts/verify-yehuobian-shenzhen-three-predicates-12ve.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def j(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
class ThreePredicates(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.a=j(m.REC); cls.st=j(m.STATE)
 def bad(self,path,value):
  a=copy.deepcopy(self.a);d=a
  for key in path[:-1]: d=d[key]
  d[path[-1]]=value
  with self.assertRaises(ValueError): m.validate(a,self.st)
 def test_baseline(self): self.assertEqual(m.validate(self.a,self.st)["predicates"],3)
 def test_no_print_not_no_completion(self): self.bad(["predicates",0,"key"],"NOT_FINISHED")
 def test_shiguan_not_printing(self): self.bad(["predicates",1,"key"],"NOT_PRINTED")
 def test_completion_not_shiguan(self): self.bad(["predicates",2,"key"],"NOT_PRESENTED_TO_SHIGUAN")
 def test_original_physical_not_seen(self): self.bad(["predicates",1,"physical_leaf_seen"],True)
 def test_pang_phrase(self): self.bad(["reported_transmission","pang1959_claimed_jingzhiju_quote"],"惜其未就也")
 def test_not_same_zhu_text(self): self.bad(["reported_transmission","shizong_and_jingzhiju_same_passage_proven"],True)
 def test_not_historical_glyph(self): self.bad(["accounting","new_ancient_glyph_votes"],1)
 def test_no_source_addition(self): self.bad(["accounting","new_source_registry_rows"],1)
 def test_no_genealogy_edge(self): self.bad(["accounting","new_graph_edges"],1)
 def test_no_algorithm_reopen(self): self.bad(["accounting","new_algorithm_reopens"],1)
 def test_no_paid_contact(self): self.bad(["firewalls","no_external_requests"],False)
 def test_no_ming_print_universal_negative(self): self.bad(["firewalls","not_yet_printed_not_universal_ming_print_negative"],False)
 def test_no_full_pang_article(self): self.bad(["witnesses",2,"full_article_seen"],True)
if __name__=="__main__": unittest.main()

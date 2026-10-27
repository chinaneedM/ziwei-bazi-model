#!/usr/bin/env python3
import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("q12vh",ROOT/"scripts/verify-yehuobian-yujideng-12vh.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class ReceivedGate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=read(m.DOC);cls.s=read(m.STATE)
 def bad(self,which,path,v):
  d,s=copy.deepcopy(self.d),copy.deepcopy(self.s);o=d if which==0 else s
  for k in path[:-1]:o=o[k]
  o[path[-1]]=v
  with self.assertRaises(ValueError):m.validate(d,s)
 def test_pass(self):self.assertEqual(m.validate(self.d,self.s)["new_glyph_votes"],0)
 def test_yu_winter(self):self.bad(0,["witnesses",1,"winter"],"辰初二刻")
 def test_yu_summer(self):self.bad(0,["witnesses",1,"summer"],"戌初二刻")
 def test_ye_winter(self):self.bad(0,["witnesses",2,"winter"],"辰初一刻")
 def test_ye_summer(self):self.bad(0,["witnesses",2,"summer"],"戌初一刻")
 def test_yu_no_gongjin(self):self.bad(0,["witnesses",1,"gongjin"],"宮禁")
 def test_yu_no_clock(self):self.bad(0,["witnesses",1,"clock"],"宮漏")
 def test_not_original(self):self.bad(0,["witnesses",1,"grade"],"ORIGINAL_1827")
 def test_no_copy_claim(self):self.bad(0,["nonpromotion","separate_work_does_not_prove_descent"],False)
 def test_no_new_vote(self):self.bad(0,["accounting","new_glyph_votes"],1)
 def test_no_new_source(self):self.bad(0,["accounting","new_source_rows"],1)
 def test_no_graph_edge(self):self.bad(0,["transmission_impact","edges_supported"],["copies"])
 def test_no_algorithm(self):self.bad(1,["invariants","algorithm_reopen_count"],1)
 def test_state_version(self):self.bad(1,["schema_version"],"1.563.0")
if __name__=="__main__":unittest.main()

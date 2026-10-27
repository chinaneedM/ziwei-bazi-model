#!/usr/bin/env python3
import unittest,copy,importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('t12vi',R/'scripts/verify-yehuobian-ncl-copies-12vi.py')
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def j(p):return json.loads((R/p).read_text(encoding='utf-8'))
class NCLCopyGate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=j(v.D);cls.s=j(v.S)
 def bad(self,i,path,val):
  d,s=copy.deepcopy(self.d),copy.deepcopy(self.s);x=d if i==0 else s
  for k in path[:-1]:x=x[k]
  x[path[-1]]=val
  with self.assertRaises(ValueError):v.validate(d,s)
 def test_baseline(self):self.assertEqual(v.validate(self.d,self.s)['catalogued_copies'],2)
 def test_02253_count(self):self.bad(0,['catalog_records',0,'fascicles'],16)
 def test_02254_count(self):self.bad(0,['catalog_records',1,'fascicles'],18)
 def test_02253_id(self):self.bad(0,['catalog_records',0,'catalog_id'],'02254')
 def test_02254_id(self):self.bad(0,['catalog_records',1,'catalog_id'],'02253')
 def test_target_leaf(self):self.bad(0,['catalog_records',0,'juan11_original_leaf'],'p100')
 def test_winter_glyph(self):self.bad(0,['catalog_records',1,'target_numeral_winter'],'辰初一刻')
 def test_no_glyph_votes(self):self.bad(0,['catalog_records',1,'independent_glyph_votes'],1)
 def test_item_link(self):self.bad(0,['provider_link','item_issued_url'],'https://fake.test/item')
 def test_scan_sha(self):self.bad(0,['surrogate_locator','page_sha256'],'0'*64)
 def test_no_same_plates(self):self.bad(0,['no_promotion','same_edition_description_is_not_identical_plate'],False)
 def test_no_source(self):self.bad(0,['accounting','new_source_rows'],1)
 def test_no_new_edge(self):self.bad(0,['transmission_impact','edges_supported'],['a copies b'])
 def test_no_algorithm(self):self.bad(1,['invariants','algorithm_reopen_count'],1)
 def test_no_rollback(self):self.bad(1,['schema_version'],'1.564.0')
if __name__=='__main__':unittest.main()

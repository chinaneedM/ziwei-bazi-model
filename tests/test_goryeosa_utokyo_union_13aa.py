import importlib.util,copy,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-utokyo-union-13aa.py"
spec=importlib.util.spec_from_file_location("utokyo13aa",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class UTokyoNIIUnionBoundary(unittest.TestCase):
 def test_catalog_locator_and_state(self):self.assertTrue(m.verify())
 def test_not_a_direct_original_witness(self):
  x=copy.deepcopy(m.load(m.S));x["sources"][0]["physical_glyph_authority"]=True
  self.assertNotEqual(x["sources"][0]["physical_glyph_authority"],m.load(m.S)["sources"][0]["physical_glyph_authority"])
 def test_utokyo_item_not_waseda_object(self):
  e=m.load(m.E)
  self.assertEqual(e["bibliographic_source"]["item_holding_identifier"],"0008542011")
  self.assertNotEqual(e["bibliographic_source"]["call_number"],e["independent_catalog_comparator"]["shelfmark"])
if __name__=="__main__":unittest.main()

import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-nlc-group40-direct-13r.py"
sp=importlib.util.spec_from_file_location("g13r",p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class DirectPixel13R(unittest.TestCase):
 def test_consistency(self):self.assertEqual(m.verify()["status"],"PASS")
 def test_original_reading_not_fabricated(self):
  x=copy.deepcopy(m.get(m.E));x["native_page_records"][1]["direct_text"]="五分二三六二"
  with self.assertRaises(AssertionError):m.check(x)
 def test_no_extra_three_without_original(self):
  x=copy.deepcopy(m.get(m.E));x["direct_comparison"]["d18"]["nlc_image_glyph"]+="三"
  with self.assertRaises(AssertionError):m.check(x)
 def test_source_pixel_hash_immutable(self):
  x=copy.deepcopy(m.get(m.E));x["native_page_records"][2]["embedded_raster_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(x)
 def test_not_two_physical_witnesses(self):
  x=copy.deepcopy(m.get(m.E));x["evidence_grading"]["independent_physical_original_numeric_votes_added"]=1
  with self.assertRaises(AssertionError):m.check(x)
 def test_not_fabricated_nlc_catalog_identity(self):
  x=copy.deepcopy(m.get(m.E));x["evidence_grading"]["original_nlc_firstparty_item_identifier_bound"]=True
  with self.assertRaises(AssertionError):m.check(x)
if __name__=="__main__":unittest.main()

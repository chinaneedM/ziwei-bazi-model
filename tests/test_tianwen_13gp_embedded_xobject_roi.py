import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location("probe",R/"scripts/verify-tianwen-13gp-embedded-xobject-roi.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class SourceProbe(unittest.TestCase):
 def setUp(self):self.d=json.loads(m.E.read_text(encoding="utf8"))
 def test_sealed_image_bytes(self):self.assertTrue(m.check(self.d))
 def test_clipped_d14_does_not_pass(self):
  self.d["images"][0]["source_box"][2]=160
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_clipped_d30_does_not_pass(self):
  self.d["images"][1]["source_box"][3]=830
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_distinct_physical_source_cannot_be_claimed(self):
  self.d["no_promotion_guards"]["new_physical_witnesses"]=1
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_invented_historic_digits_fail(self):
  self.d["target_status"]["D30_complete_source_literal"]="四分九二二二"
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_transposed_source_pdf_hash_fails(self):
  self.d["source"]["pdf_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_render_pixel_masquerading_as_embedded_fails(self):
  self.d["images"][0]["image_wh"]=[35,275]
  with self.assertRaises(AssertionError):m.check(self.d)
if __name__=="__main__":unittest.main()

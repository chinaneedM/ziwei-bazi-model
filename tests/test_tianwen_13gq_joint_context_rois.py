import importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location("context",R/"scripts/verify-tianwen-13gq-joint-context-rois.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SameSourceContext(unittest.TestCase):
 def setUp(self):self.d=json.loads(m.E.read_text(encoding="utf8"))
 def test_original_jpeg_context_hashes(self):self.assertTrue(m.check(self.d))
 def test_context_clip_D14_invalid(self):
  self.d["context_panels"][1]["box"][2]=160
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_context_clip_D30_invalid(self):
  self.d["context_panels"][2]["box"][3]=825
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_field_identity_must_not_be_fabricated(self):
  self.d["context_panels"][1]["field_identity_certified"]=True
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_original_number_must_not_be_inferred(self):
  self.d["context_panels"][2]["exact_ancient_literal"]="四分九二二二"
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_same_source_is_not_an_independent_witness(self):
  self.d["firewall"]["new_independent_sources"]=1
  with self.assertRaises(AssertionError):m.check(self.d)
 def test_original_sha_cannot_change(self):
  self.d["source"]["original_pdf_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(self.d)
if __name__=="__main__":unittest.main()

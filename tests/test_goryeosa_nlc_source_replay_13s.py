import copy,importlib.util,unittest,io,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"replay-goryeosa-nlc-source-pixels-13s.py"
spec=importlib.util.spec_from_file_location("replay13s",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Replay13S(unittest.TestCase):
 def test_static_scope(self):self.assertTrue(m.static_check(m.read()))
 def test_no_promotion_of_secondary_identifier(self):
  e=copy.deepcopy(m.read());e["upload_bibliography_secondary"]["catalog_candidate_status"]="NLC_FIRST_PARTY_VERIFIED"
  with self.assertRaises(AssertionError):m.static_check(e)
 def test_no_inflated_physical_witnesses(self):
  e=copy.deepcopy(m.read());e["adjudication"]["independent_numeric_votes_added"]=1
  with self.assertRaises(AssertionError):m.static_check(e)
 def test_crop_encoded_bytes_require_rgb(self):
  from PIL import Image
  src=Image.new("L",(4,4),42);b=io.BytesIO();src.save(b,format="PNG")
  raw,png=m.rgb_crop_bytes(b.getvalue(),[1,1,3,3])
  self.assertEqual(raw,bytes([42,42,42]*4))
  self.assertEqual(len(raw),12)
  self.assertEqual(Image.open(io.BytesIO(png)).mode,"RGB")
 def test_no_mutated_crop_sha(self):
  e=copy.deepcopy(m.read());e["page_replay"][1]["rgb_crop_encoded_png_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.static_check(e)
if __name__=="__main__":unittest.main()

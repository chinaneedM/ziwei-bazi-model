import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);x=importlib.util.module_from_spec(spec);spec.loader.exec_module(x);return x
V=module("v13iw","scripts/verify-tianwen-13iw-official-xml-byte-binding.py")
P=module("p13iw","scripts/probe-tianwen-13iw-official-2114-2-target-contexts.py")
class Bound(unittest.TestCase):
 def setUp(self):self.e=V.load()
 def reject(self):
  with self.assertRaises(AssertionError):V.check(self.e)
 def test_good(self):self.assertTrue(V.check(self.e))
 def test_fake_200_short_code_promotion(self):self.e["negative_control"]["matched_target_title"]=True;self.reject()
 def test_original_bytes_hash_identity(self):self.e["source"]["body_sha256"]="0"*64;self.reject()
 def test_copied_short_code_false_identity(self):self.e["source"]["official_book_code"]="21140200";self.reject()
 def test_original_leaf_not_copied_from_official_description(self):self.e["source_authentication"]["physical_original_leaf_verified"]=True;self.reject()
 def test_book29_retraction_still_live(self):self.e["source_authentication"]["book29_juan81_83_status"]="CONFIRMED";self.reject()
 def test_official_words_not_pre_adjudicated_as_copy(self):self.e["firstparty_korean_juan_and_book_scope"]["gk5554_juan81_82"]="CONFIRMED";self.reject()
 def test_legacy_13ei_retracted(self):self.e["original_ancient_controls"]["older_13EI"]="PROVEN";self.reject()
 def test_six_g893_original_numbers_not_inferred(self):self.e["original_ancient_controls"]["g893_six_original_numeric"]=[1]*6;self.reject()
class Read(unittest.TestCase):
 def test_hash_guard_blocks_synthetic(self):
  x=P.validate(b"<heritage><content>fake</content></heritage>")
  self.assertFalse(x["bound_firstparty_text"])
 def test_target_snippet_slice(self):
  x=P.excerpts("abc"*20+"규귀5553"+"def"*25)
  self.assertTrue(any(z["marker"]=="5553" for z in x))
  self.assertLessEqual(len(x[0]["context"]),95)
 def test_markers_do_not_claim_ancient(self):
  self.assertFalse(P.validate(b"short")["ancient_original_leaf"])
if __name__=="__main__":unittest.main()

import importlib.util,unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wm",ROOT/"scripts/verify-yehuobian-cadal-first-fascicle-dual-original-12wm.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class DualSourceDigitalOnly(unittest.TestCase):
 def setUp(self):self.arr=[v.load(x) for x in (v.REC,v.PENDING,v.WK,v.STATE,v.MANIFEST)]
 def bad(self,m):
  with self.assertRaisesRegex(ValueError,m):v.validate(*self.arr)
 def test_live_record(self):self.assertEqual(v.verify()["historic_independent_print_votes"],0)
 def test_false_digest(self):
  self.arr[0]["acquisition"]["artifact_zip_sha256_independently_recomputed"]="0"*64
  self.bad("archived bytes independently")
 def test_old_original_source_hash_tampered(self):
  self.arr[0]["source_files"][0]["sha256"]="f"*64
  self.bad("original binary SHA256")
 def test_missing_original_pages(self):
  self.arr[0]["source_files"][0]["pages"]=114
  self.bad("original binary bytes")
 def test_digital_near_identity_must_not_equal_full_pixel_identity(self):
  self.arr[0]["computed_relation"]["same_exact_decoded_grayscale_pixels_on_checked_pages"]=True
  self.bad("digital near duplicate")
 def test_no_paper_copy_proven(self):
  self.arr[0]["computed_relation"]["identity_of_underlying_scanned_physical_paper_copy"]="SAME_COPY"
  self.bad("no paper-copy")
 def test_no_cross_fascicle_identity(self):
  self.arr[0]["computed_relation"]["cross_fascicle_physical_copy_identity_to_CADAL02096915"]="PROVEN"
  self.bad("no paper-copy")
 def test_no_new_original_glyph_vote(self):
  self.arr[0]["image_glyph_limit"]["new_juan20_gaizao_louke_glyph_votes"]=1
  self.bad("manual ancient glyph")
 def test_dated_1827_paper_image_still_missing(self):
  self.arr[0]["image_glyph_limit"]["no_independent_original_1827_paper_first_impression_leaf"]=False
  self.bad("no original dated")
 def test_no_double_source_registry(self):
  self.arr[0]["accounting"]["source_registry_additions"]=1
  self.bad("no source double")
 def test_negative_transmission_edge(self):
  self.arr[0]["transmission_impact"]["edges_supported"]=["digital image proves same paper"]
  self.bad("no lineage")
 def test_pixel_delta_must_match_real(self):
  self.arr[0]["page_comparisons"][1]["delta"]=0.0
  self.bad("actual preview")
if __name__=="__main__":unittest.main()

import unittest,importlib.util
from pathlib import Path
f=Path(__file__).resolve().parents[1]/"scripts/verify-mingshi-cadal-12ym-original-dual-locus.py"
sp=importlib.util.spec_from_file_location("tianwen_12ym",f);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class OriginalDualLocusTest(unittest.TestCase):
 def setUp(self):self.d=list(v.load())
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.d)
 def test_valid(self):self.assertEqual(v.verify(*self.d)["original_direct_glyph_loci"],2)
 def test_unproven_physical_impression_date(self):self.d[0]["provenance"]["source_origin_physical_impression_date"]="1739";self.fails()
 def test_invalid_original_sha(self):self.d[0]["provenance"]["sha256"]="fake";self.fails()
 def test_uncertified_folio(self):self.d[0]["provenance"]["folio_number_in_source"]="卷33葉7";self.fails()
 def test_no_arithmetic_correction_to_printed_first_locus(self):self.d[0]["original_two_loci"][0]["target_glyph"]="一秒八十六微";self.fails()
 def test_no_arithmetic_correction_to_printed_sum(self):self.d[0]["original_two_loci"][1]["target_glyph"]="四分九十二秒八十六微";self.fails()
 def test_roi_pixel_hash_required(self):self.d[0]["original_two_loci"][0]["region"]["rgb_pixel_sha256"]="000";self.fails()
 def test_disjoint_roi_required(self):self.d[0]["original_two_loci"][0]["region"]["png_pixel_crop_xyxy"]=[800,290,1905,2910];self.fails()
 def test_no_unproven_witness_voting(self):self.d[0]["safeguards"]["new_independent_physical_impressions_awarded"]=1;self.fails()
 def test_no_algorithms_reopen(self):self.d[0]["safeguards"]["algorithm_reopens"]=1;self.fails()
 def test_issue5_open(self):next(i for i in self.d[1]["issues"] if i["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.fails()
 def test_state_fresh(self):self.d[2]["schema_version"]="1.626.0";self.fails()
 def test_later_batch_does_not_erase_12ym(self):
  self.d[2]["historical_audit"]["current_focus"].append("12YO FUTURE_GUARD")
  self.assertEqual(v.verify(*self.d)["original_direct_glyph_loci"],2)
 def test_missing_original_12ym_focus_rejected(self):
  self.d[2]["historical_audit"]["current_focus"]=[x for x in self.d[2]["historical_audit"]["current_focus"] if not x.startswith("12YM ")]
  self.fails()
if __name__=="__main__":unittest.main()

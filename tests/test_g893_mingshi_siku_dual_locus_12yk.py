import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-g893-mingshi-siku-dual-locus-12yk.py"
spec=importlib.util.spec_from_file_location("dual_12yk",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class DualLocusScope(unittest.TestCase):
 def setUp(self):self.d=list(v.load())
 def invalid(self):
  with self.assertRaises(ValueError):v.verify(*self.d)
 def test_pass(self):self.assertEqual(v.verify(*self.d)["siku_multiplication_delta"],"-0.0050")
 def test_siku_midpoint_fabrication(self):self.d[0]["received_text_presentations"][1]["intermediate_decimal"]="0.0186";self.invalid()
 def test_general_total_fabrication(self):self.d[0]["received_text_presentations"][0]["sum_decimal"]="4.9386";self.invalid()
 def test_other_received_surface_not_physical(self):self.d[0]["received_text_presentations"][2]["representation"]="DATED_ORIGINAL";self.invalid()
 def test_fake_siku_mathematical_closure(self):self.d[0]["mechanical_semantics"]["delta_siku_self_sum"]="0.0000";self.invalid()
 def test_incorrect_historical_micro(self):self.d[0]["mechanical_semantics"]["delta_siku_intermediate"]="-0.0005";self.invalid()
 def test_unverified_pdf_original_not_promoted(self):self.d[0]["scan_candidate"]["actual_scanned_folio_read"]=True;self.invalid()
 def test_pdf_unverified_sha(self):self.d[0]["scan_candidate"]["scan_payload_hash_verified"]=True;self.invalid()
 def test_false_one_source_equals_4_votes(self):self.d[0]["crosswalk"]["physical_witnesses_added"]=4;self.invalid()
 def test_false_cross_edition_same_field(self):self.d[0]["crosswalk"]["mingshi_field_same_as_g893"]="PROVEN";self.invalid()
 def test_false_original_glyph_bridge(self):self.d[0]["crosswalk"]["native_g893_少_vs_received_微"]="SAME";self.invalid()
 def test_false_alg_reopen(self):self.d[0]["crosswalk"]["algorithm_reopens"]=1;self.invalid()
 def test_issue_closed(self):next(x for x in self.d[1]["issues"] if x["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.invalid()
 def test_old_review_deleted(self):next(x for x in self.d[1]["issues"] if x["id"]=="TW-OPEN-0005")["g893_12yk_dual_locus_received_comparison"]=[];self.invalid()
 def test_stale_state(self):self.d[2]["schema_version"]="1.624.0";self.invalid()
if __name__=="__main__": unittest.main()

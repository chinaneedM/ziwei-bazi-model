import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-mingshi-nlc1892-two-originals-12yn.py"
spec=importlib.util.spec_from_file_location("tianwen_12yn",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TwoOriginalImprintTest(unittest.TestCase):
 def setUp(self):self.d=list(m.load())
 def rejects(self):
  with self.assertRaises(ValueError):m.verify(*self.d)
 def test_positive(self):self.assertEqual(m.verify(*self.d)["first_locus_micro_gap"],50)
 def test_reject_source_sha(self):self.d[0]["source"]["image_pdf_sha256"]="false";self.rejects()
 def test_reject_fake_first_locus(self):self.d[0]["target_loci"][0]["direct_printed_result"]="一秒三十六微";self.rejects()
 def test_reject_fake_sum(self):self.d[0]["target_loci"][1]["direct_printed_result"]="四分九十二秒八十六微";self.rejects()
 def test_reject_fake_second_source(self):self.d[0]["cross_source_collation"]["cadal_12ym"]["first"]="一秒八十六微";self.rejects()
 def test_reject_wrong_page(self):self.d[0]["source"]["pdf_page_index_one_based"]=63;self.rejects()
 def test_reject_wrong_pixel(self):self.d[0]["target_loci"][1]["ROI_rgb_sha256"]="false";self.rejects()
 def test_reject_fake_1739(self):self.d[0]["source"]["physical_object_specific_colophon_directly_authenticated"]=True;self.rejects()
 def test_reject_false_copy(self):self.d[0]["cross_source_collation"]["independent_stemmatic_origin_or_direct_copy_proven"]=True;self.rejects()
 def test_reject_stemmatic_vote(self):self.d[0]["safeguards"]["new_independent_stemmatic_root_awarded"]=1;self.rejects()
 def test_reject_chart_reopen(self):self.d[0]["safeguards"]["new_algorithm_reopens"]=1;self.rejects()
 def test_reject_closed_issue(self):next(x for x in self.d[1]["issues"] if x["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.rejects()
 def test_reject_stale_state(self):self.d[2]["schema_version"]="1.627.0";self.rejects()
if __name__=="__main__":unittest.main()

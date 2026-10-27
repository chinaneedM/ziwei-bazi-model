"""12QL digitized ten fascicle capture coverage is not manual old20 collation."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
SOURCE=ROOT/"scripts/probe-yehuobian-nlc-old20-fascicles-wave1-12qi.py"
class NLCOld20TenFascicleClosure(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(E.read_text(encoding="utf8"))
 def test_ten_files_one_holding_source_scope(self):
  d=self.e
  self.assertEqual([x["fascicle"] for x in d["sources"]],list(range(1,11)))
  self.assertEqual([x["source_pdf_pages"] for x in d["sources"]],[119,72,121,56,63,116,110,87,141,145])
  self.assertEqual(d["source_capture"]["total_pdf_pages"],1030)
  self.assertEqual(d["source_capture"]["total_page_images"],1030)
  self.assertEqual(d["source_capture"]["contact_sheets_total"],132)
  self.assertEqual(d["independent_physical_copy_count_increment"],0)
  self.assertTrue(d["one_cataloged_physical_holding"])
  self.assertFalse(d["source_capture"]["full_manual_1030_page_review_completed"])
  self.assertFalse(d["source_capture"]["original_20v_target_paragraph_folio_located"])
 def test_six_new_direct_headings_are_source_scoped(self):
  obs=self.e["direct_new_manual_volume_headings"]
  self.assertEqual([x["fascicle"] for x in obs],list(range(4,10)))
  self.assertEqual([x["pdf_page"] for x in obs],[1]*6)
  self.assertEqual(len({x["jpeg_sha256"] for x in obs}),6)
  self.assertEqual([x["exact_opening"].split("卷")[-1] for x in obs],["八","十","十一","十二","十五","十六"])
 def test_pin_source_hashes_for_nine_captured_original_pdfs(self):
  src=SOURCE.read_text(encoding="utf8")
  for x in self.e["sources"][:9]:
   self.assertEqual(len(x["source_pdf_sha256"]),64)
   self.assertIn(x["source_pdf_sha256"],src)
  self.assertFalse(self.e["stemmatic_scope"]["no_proof_it_is_absent_in_this_copy"] is False)
  self.assertTrue(self.e["stemmatic_scope"]["no_algorithm_reopen"])
  self.assertEqual(self.e["invariants"]["product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()

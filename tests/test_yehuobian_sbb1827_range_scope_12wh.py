import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("wh",ROOT/"scripts/verify-yehuobian-sbb1827-range-scope-12wh.py")
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class PreviewEvidence(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((ROOT/v.REC).read_text())
  self.state=json.loads((ROOT/v.STATE).read_text())
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):v.validate(self.r,self.state)
 def test_exact_successful_source_receipt(self):
  self.assertEqual(v.verify()["independent_1827_vs_1869_print_votes"],0)
 def test_38_range_named_pretence(self):
  self.r["receipt"]["manifest"]["iiif_range_labels_in_order"][3]="卷二十";self.bad("source named scope")
 def test_no_physical_book_absence_from_sample(self):
  self.r["adjudication"]["catalogued_paper_book_has_no_juan20"]=True;self.bad("sample != physical missing volume")
 def test_no_unread_original_glyph(self):
  self.r["adjudication"]["source_specific_guangjing_gonglou_reading_glyphs"]["GONGJIN"]="官禁";self.bad("missing original glyphs")
 def test_catalogue_timeout_not_absence_proof(self):
  self.r["receipt"]["nlc"]["absence_of_wenzhou_1827_1869_holdings_inferred"]=True;self.bad("NLC timeout")
 def test_source_sha_is_exact(self):
  self.r["receipt"]["manifest"]["sha256"]="0"*64;self.bad("manifest SHA")
 def test_no_undocumented_archive_independent_rehash(self):
  self.r["receipt"]["artifact_zip_independently_redownloaded_and_rehashed"]=True;self.bad("zip scope")
 def test_no_early_1827_print_winner(self):
  self.r["adjudication"]["physical_1827_first_print_proven"]=True;self.bad("no printing state")
if __name__=="__main__":unittest.main()

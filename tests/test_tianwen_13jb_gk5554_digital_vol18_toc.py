import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13jb-gk5554-digital-vol18-toc.py"
spec=importlib.util.spec_from_file_location("v13jb",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class SourceIndex(unittest.TestCase):
 def setUp(self):self.e=v.get(v.E)
 def deny(self):
  with self.assertRaises(AssertionError):v.check(self.e)
 def test_positive(self):self.assertTrue(v.check(self.e))
 def test_sha_mismatch(self):self.e["source"]["raw_html_sha256"]="0"*64;self.deny()
 def test_source_no_pdf_to_ancient(self):self.e["source_emitted_toc"][1]["photo_bytes"]=100;self.deny()
 def test_glyph_not_proven(self):self.e["source_emitted_toc"][2]["original_folio_glyph_verified"]=True;self.deny()
 def test_no_juan81_page_swap(self):self.e["source_emitted_toc"][1]["page_no"]="085a";self.deny()
 def test_no_juan82_page_swap(self):self.e["source_emitted_toc"][2]["page_no"]="048a";self.deny()
 def test_no_vol17_inference(self):self.e["corroboration_scope"]["can_infer_vol17_exact_juan79_from_complement"]=True;self.deny()
 def test_no_antique_juan_inference(self):self.e["corroboration_scope"]["can_assign_antique_physical_folio_page"]=True;self.deny()
 def test_no_book29_revival(self):self.e["corroboration_scope"]["gk5553_book29_to_81_83"]="CONFIRMED";self.deny()
 def test_no_source_html_offset_guess(self):self.e["page_metadata"]["first_named_page"]="000a";self.deny()
 def test_no_conflation_with_gk5553(self):self.e["source_emitted_toc"][1]["onclick"]="fn_originalImg('GJB','GK05553_00' ,'0018','048a');";self.deny()
 def test_no_original_pages_registered(self):self.e["impact"]["ancient_page_images_added"]=2;self.deny()
if __name__=="__main__":unittest.main()

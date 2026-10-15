import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wv",ROOT/"scripts/probe-yehuobian-12wv-tokyo-kanseki-exact-search-form.py")
p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
class ExactUniversityCatalogAdvancedForm(unittest.TestCase):
 def test_exact_official_url(self):self.assertTrue(p.guard())
 def test_guessed_record_endpoint_forbidden(self):
  with self.assertRaisesRegex(ValueError,"only source-issued"):
   p.guard("https://kanseki.ioc.u-tokyo.ac.jp/kanzi/user/get.php?doc=6403767830")
 def test_form_action_recorded_as_issued_not_guessed(self):
  b='<form method="post" action="go.php"><input type="text" name="k"><select name="field"><option value="ti">書名</option></select><button type="submit">Go</button></form>'.encode()
  s=p.inspect(b)
  self.assertEqual(s["source_emitted_forms"][0]["action"],"go.php")
  self.assertEqual(s["source_emitted_forms"][0]["method"],"post")
  self.assertEqual(s["source_emitted_forms"][0]["inputs"][0]["name"],"k")
  self.assertEqual(s["source_emitted_forms"][0]["selects"][0]["options"][0]["value"],"ti")
 def test_search_form_is_not_book_image(self):
  x=p.inspect("野獲編 書名 索書號".encode())
  self.assertTrue(x["visible_book_title_field"])
  self.assertFalse(x["provider_copy_to_image_mapping_obtained"])
  self.assertEqual(x["original_print_votes"],0)
 def test_script_captured_for_provider_js_semantics(self):
  x=p.inspect(b'<script>submitData()</script>')
  self.assertEqual(x["source_script_fragments"],["submitData()"])
 def test_bytes_cap(self):
  with self.assertRaisesRegex(ValueError,"360KB"):p.inspect(b"a"*(p.MAX+1))
 def test_no_ocr_or_page(self):
  x=p.inspect(b'<html></html>')
  self.assertFalse(x["original_1827_juan20_page_obtained"])
  self.assertFalse(x["original_1869_juan20_page_obtained"])
 def test_no_query_sent_for_unknown_fields(self):
  self.assertNotIn("野獲編",p.URL)
if __name__=="__main__":unittest.main()

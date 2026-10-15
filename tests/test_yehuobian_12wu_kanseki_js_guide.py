import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("wu",ROOT/"scripts/probe-yehuobian-12wu-tokyo-kanseki-source-declared-js-guide.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ProviderSourceOnly(unittest.TestCase):
 def test_two_official_source_emitted_links(self):
  self.assertEqual(len(m.SOURCES),2)
  for k,v in m.SOURCES.items():self.assertTrue(m.guard(k,v))
 def test_reject_unemitted_form_endpoint(self):
  with self.assertRaisesRegex(ValueError,"source-emitted"):m.guard("entry_script","https://kanseki.ioc.u-tokyo.ac.jp/user/query.php")
 def test_reject_guessing_images(self):
  with self.assertRaisesRegex(ValueError,"source-emitted"):m.guard("source_guide","https://kanseki.ioc.u-tokyo.ac.jp/kanseki/image/folio1.jpg")
 def test_guide_not_original_glyph(self):
  raw="本データベース2001年まで2002年以降、物理的な書冊、全文画像".encode()
  x=m.parse("source_guide",raw)
  self.assertTrue(x["manual_scope_notes"]["catalog_pre2001_originals"])
  self.assertFalse(x["keio_or_tokyo_book_copy_binding"])
  self.assertEqual(x["original_juan20_target_glyphs"],0)
 def test_javascript_not_executed(self):
  js=b'function popUp(t){window.open("./new.php","x");}'
  x=m.parse("entry_script",js)
  self.assertEqual(x["script_function_names"],["popUp"])
  self.assertFalse(x["contains_request_or_image_bulk_execution"])
  self.assertEqual(x["independent_original_1827_1869_print_votes"],0)
 def test_html_links_not_authenticated_as_physical_items(self):
  x=m.parse("source_guide",b'<a href="search.html">begin</a>')
  self.assertEqual(len(x["anchors"]),1)
  self.assertFalse(x["keio_or_tokyo_book_copy_binding"])
 def test_byte_limit(self):
  with self.assertRaisesRegex(ValueError,"byte bound"):m.parse("entry_script",b"a"*(m.MAX_BYTES+1))
if __name__=="__main__":unittest.main()

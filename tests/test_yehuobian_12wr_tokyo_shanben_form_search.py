import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("wr",ROOT/"scripts/probe-yehuobian-12wr-tokyo-shanben-form-search.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SourceForm(unittest.TestCase):
 def test_exact_emitted_form(self):self.assertTrue(m.guard())
 def test_no_id_enumeration(self):
  with self.assertRaisesRegex(ValueError,"source-issued"):m.guard("https://shanben.ioc.u-tokyo.ac.jp/item/6403767830")
 def test_no_broad_queries(self):
  with self.assertRaisesRegex(ValueError,"title search"):m.guard(form={"str":"","col":"ti","submits":"檢索"})
 def test_one_target_only(self):
  with self.assertRaisesRegex(ValueError,"title search"):m.guard(form={"str":"野獲編 OR something","col":"ti","submits":"檢索"})
 def test_one_source_positive_title_is_not_glyph_vote(self):
  z=m.summarize("<a href='main_p.php'>野獲編</a>".encode())
  self.assertTrue(z["visible_text_contains_exact_target_title"])
  self.assertEqual(z["title_bearing_links_count"],1)
  self.assertEqual(z["original_print_votes"],0)
 def test_no_result_is_not_catalog_absence(self):
  z=m.summarize("検索結果なし".encode())
  self.assertFalse(z["visible_text_contains_exact_target_title"])
  self.assertFalse(z["source_absence_proven"])
  self.assertFalse(z["list_form_search_exhausts_historical_catalog"])
 def test_no_dated_print_from_positive(self):
  z=m.summarize("野獲編 1827 1869".encode())
  self.assertFalse(z["tokyo_1827_folio_glyph_attested"])
  self.assertFalse(z["tokyo_1869_folio_glyph_attested"])
 def test_max_bytes(self):
  with self.assertRaisesRegex(ValueError,"oversized"):m.summarize(b"b"*(m.MAX_BYTES+1))
if __name__=="__main__":unittest.main()

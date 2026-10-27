import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wu",ROOT/"scripts/probe-yehuobian-12wu-tokyo-kanseki-official-fields.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class TokyoSeparateImageField(unittest.TestCase):
 def test_only_three_source_linked_docs(self):
  self.assertEqual(len(m.SOURCES),3)
  for n,u in m.SOURCES.items():self.assertTrue(m.allow(n,u))
 def test_no_speculative_juan20_url(self):
  with self.assertRaisesRegex(ValueError,"only official"):m.allow("catalog_field_legend","https://kanseki.ioc.u-tokyo.ac.jp/kanzi/juan20.jpg")
 def test_separate_frontmatter_from_fulltext(self):
  a=m.parse("catalog_field_legend",m.SOURCES["catalog_field_legend"],"書影 卷首".encode())
  self.assertTrue(a["explicit_frontmatter_or_cover_image_field"])
  self.assertFalse(a["explicit_fulltext_link_field"])
  b=m.parse("catalog_field_legend",m.SOURCES["catalog_field_legend"],"連結文本 全文影像資料庫".encode())
  self.assertTrue(b["explicit_fulltext_link_field"])
  self.assertFalse(b["explicit_frontmatter_or_cover_image_field"])
 def test_fulltext_field_not_proof_target_image(self):
  z=m.parse("catalog_field_legend",m.SOURCES["catalog_field_legend"],"連結文本 6403767830".encode())
  self.assertFalse(z["exact_1827_or_1869_item_image_authenticated"])
  self.assertEqual(z["observed_original_juan20_glyphs"],0)
 def test_only_provider_metadata_links(self):
  z=m.parse("catalog_use_guide",m.SOURCES["catalog_use_guide"],b'<a href="https://example.com">offsite</a><a href="/user/index.php">on</a>')
  self.assertEqual(len(z["provider_metadata_links"]),1)
 def test_size_cap(self):
  with self.assertRaisesRegex(ValueError,"too large"):m.parse("catalog_use_guide",m.SOURCES["catalog_use_guide"],b"a"*(m.MAX+1))
 def test_not_an_original_page(self):
  z=m.parse("catalog_use_guide",m.SOURCES["catalog_use_guide"],"野獲編 卷二十 1827".encode())
  self.assertEqual(z["historical_print_votes"],0)
 def test_no_auto_id_guess(self):self.assertFalse(any("6403767830" in s for s in m.SOURCES.values()))
if __name__=="__main__":unittest.main()

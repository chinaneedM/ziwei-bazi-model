import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wt",ROOT/"scripts/probe-yehuobian-12wt-tokyo-kanseki-source-form.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class OfficialCatalogue(unittest.TestCase):
 def test_exact_two_firstparty_pages(self):
  self.assertEqual(len(m.SOURCES),2)
  for k,url in m.SOURCES.items():self.assertTrue(m.guard(k,url))
 def test_no_guessed_juan20_images(self):
  with self.assertRaisesRegex(ValueError,"two provider-issued"):m.guard("kanseki_catalog_home","https://kanseki.ioc.u-tokyo.ac.jp/download.php?item=6403767830")
 def test_no_unrelated_query_host(self):
  with self.assertRaisesRegex(ValueError,"two provider-issued"):m.guard("other","https://example.com/")
 def test_actual_form_controls_parsed(self):
  doc=b'<form action="/user/search.php" method="POST"><input name="q" type="text"/><select name="col"><option value="title"></option></select></form>'
  p=m.parse("kanseki_catalog_home",m.SOURCES["kanseki_catalog_home"],doc)
  self.assertEqual(p["html_forms"][0]["method"],"post")
  self.assertEqual(p["html_forms"][0]["inputs"][0]["name"],"q")
  self.assertEqual(p["html_forms"][0]["selects"][0]["values"],["title"])
 def test_metadata_not_same_as_original_print(self):
  z=m.parse("kanseki_catalog_home",m.SOURCES["kanseki_catalog_home"],"野獲編 6403767830".encode())
  self.assertTrue(z["visible_text_mentions_original_1827_item"])
  self.assertEqual(z["original_paper_impression_votes"],0)
  self.assertEqual(z["original_page_pixels_retrieved"],0)
 def test_oversize_strict(self):
  with self.assertRaisesRegex(ValueError,"600KB"):m.parse("kanseki_catalog_home",m.SOURCES["kanseki_catalog_home"],b"a"*(m.MAX+1))
 def test_offsite_anchor_excluded(self):
  raw=b'<a href="https://attacker.example/steal">bad</a><a href="/user/help.php">ok</a>'
  z=m.parse("kanseki_catalog_home",m.SOURCES["kanseki_catalog_home"],raw)
  self.assertEqual(len(z["allowed_provider_links"]),1)
 def test_no_authentication_credentials(self):
  self.assertFalse(any("token=" in u or "apikey=" in u for u in m.SOURCES.values()))
if __name__=="__main__":unittest.main()

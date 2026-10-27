import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("tokyo",ROOT/"scripts/probe-yehuobian-12wp-tokyo-shanben-official-navigation.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TokyoOfficialNoImages(unittest.TestCase):
 def test_six_exact_official_metadata_pages(self):self.assertEqual(len(m.URLS),m.MAX_REQUESTS)
 def test_valid_official_urls(self):
  for n,u in m.URLS.items():self.assertTrue(m.permitted(n,u))
 def test_reject_forged_path(self):
  with self.assertRaisesRegex(ValueError,"preapproved"):m.permitted("shanben_home","https://shanben.ioc.u-tokyo.ac.jp/fictional/juan20.jpg")
 def test_reject_forged_key(self):
  with self.assertRaisesRegex(ValueError,"preapproved"):m.permitted("invented","https://shanben.ioc.u-tokyo.ac.jp/")
 def test_extract_only_textual_indices(self):
  b=b'<html><a href="/help.html">help</a><a href="/images/000123.jpg">image</a><body>Title index</body></html>'
  r=m.extract("shanben_home",m.URLS["shanben_home"],b)
  self.assertEqual(len(r["document_links"]),1)
  self.assertFalse(r["visible_html_contains_1827_catalog_id"])
 def test_reference_number_is_not_proof_of_image(self):
  b="卷20 6403767830 6403148395".encode()
  r=m.extract("shanben_home",m.URLS["shanben_home"],b)
  self.assertTrue(r["visible_html_contains_1827_catalog_id"])
  self.assertEqual(r["document_links"],[])
 def test_enforce_source_size_limit(self):
  with self.assertRaisesRegex(ValueError,"oversized"):
   m.extract("shanben_help",m.URLS["shanben_help"],b"b"*(m.TEXTLIMIT+1))
 def test_disallow_forged_image_endpoint_even_if_host_valid(self):
  with self.assertRaisesRegex(ValueError,"preapproved"):
   m.permitted("shanben_help","https://shanben.ioc.u-tokyo.ac.jp/image/secret")
 def test_request_cap(self):self.assertLessEqual(m.MAX_REQUESTS,6)
 def test_oauth_not_needed(self):
  self.assertFalse(any("oauth" in u or "token" in u for u in m.URLS.values()))
if __name__=="__main__":unittest.main()

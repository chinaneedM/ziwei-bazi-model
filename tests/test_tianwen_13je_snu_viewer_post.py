import hashlib,importlib.util,unittest,urllib.error,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13je-snu-source-emitted-viewer-post.py"
spec=importlib.util.spec_from_file_location("t13je",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

class ExactPost(unittest.TestCase):
 def test_sha_bound_prior_sources(self):
  self.assertEqual(v.OFFICIAL_JS_SHA256,"b2b4aaabf3da440b84b64f25768965a6c2c5500775b53e7634e98e4f59adf087")
  self.assertEqual(v.SOURCE_HTML_SHA256,"31c9afa4e92d68b6ec728758c20ca4cd0787c91a5690cbcd222bf8febdd13374")
 def test_post_url_from_original_function(self):
  self.assertEqual(v.ENDPOINT,"https://kyudb.snu.ac.kr/pf01/rendererImg.do")
 def test_only_two_source_emitted_targets(self):
  self.assertEqual(v.PAGE_IDS,("048a","085a"))
  with self.assertRaises(ValueError):v.payload_for("003a")
 def test_actual_form_fields_no_invented_keys(self):
  p=v.payload_for("048a")
  self.assertEqual(tuple(p),v.FIELDS)
  self.assertEqual((p["item_cd"],p["book_cd"],p["vol_no"],p["page_no"]),("GJB","GK05554_00","0018","048a"))
  self.assertTrue(all(p[k]=="" for k in v.FIELDS[4:]))
 def test_html_link_parser_does_not_request_images(self):
  x=v.analyze(b'<html><img src="/images/source-emitted-page.jpg"><form action="/f"></form></html>',"text/html")
  self.assertEqual(x["literal_links"][0]["literal_attributes"]["src"],"/images/source-emitted-page.jpg")
  self.assertEqual(x["independent_historical_witness_votes"],0)
  self.assertFalse(x["original_ancient_folio_verified"])
 def test_non_html_response_not_physical_proof(self):
  x=v.analyze(b"\xff\xd8\xff","image/jpeg")
  self.assertEqual(x["status"],"NON_HTML_RESPONSE_NOT_INTERPRETED")
  self.assertFalse(x["physical_copy_bound"])
 def test_sha_replay(self):
  raw=b"<html></html>"
  self.assertEqual(v.analyze(raw,"text/html")["sha256"],hashlib.sha256(raw).hexdigest())
 def test_redirect_protection(self):
  with self.assertRaises(urllib.error.HTTPError):
   v.ProviderOnly().redirect_request(urllib.request.Request(v.REFERER),None,302,"found",{},"https://untrusted.example/renderer")
 def test_provider_validation(self):
  self.assertTrue(v.firstparty_url(v.ENDPOINT))
  self.assertFalse(v.firstparty_url("http://kyudb.snu.ac.kr/pf01/rendererImg.do"))
  self.assertFalse(v.firstparty_url("https://other.example/"))
if __name__=="__main__":unittest.main()

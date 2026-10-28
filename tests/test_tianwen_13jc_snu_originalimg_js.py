import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13jc-snu-booksearch-originalimg.py"
spec=importlib.util.spec_from_file_location("t13jc",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class BoundJS(unittest.TestCase):
 def test_exact_source_uri(self):self.assertEqual(v.URL,"https://kyudb.snu.ac.kr/js/book/bookSearch.js")
 def test_positive_function_signature(self):
  a=v.inspect(b"function fn_originalImg(item_cd, book_cd, vol_no, page_no) { return 1; }")
  self.assertEqual(a["function_signature"],"function fn_originalImg(item_cd, book_cd, vol_no, page_no)")
  self.assertFalse(a["printed_folio_content_acquired"])
 def test_no_function_in_comments(self):
  a=v.inspect(b"// not a defined function but fn_originalImg is mentioned")
  self.assertFalse(a["function_definition_observed"])
 def test_no_fake_photo_from_script(self):self.assertEqual(v.inspect(b"imgViewer")["new_physical_witness_votes"],0)
 def test_sha_replay(self):
  import hashlib
  b=b"function fn_originalImg(x){}"
  self.assertEqual(v.inspect(b)["sha256"],hashlib.sha256(b).hexdigest())
 def test_accepts_known_javascript_media(self):
  self.assertTrue(v.accepts_script_payload("text/javascript; charset=utf-8",b"function fn_originalImg(){}"))
  self.assertTrue(v.accepts_script_payload("application/javascript",b"var x=1;"))
 def test_rejects_html_even_when_labeled_js(self):
  self.assertFalse(v.accepts_script_payload("text/javascript",b"  <!DOCTYPE HTML><html>not a script</html>"))
  self.assertFalse(v.accepts_script_payload("text/plain",b"<html>Access Denied</html>"))
 def test_rejects_unknown_media_and_empty(self):
  self.assertFalse(v.accepts_script_payload("image/jpeg",b"not actually js"))
  self.assertFalse(v.accepts_script_payload("text/javascript",b"   "))
 def test_retry_is_bounded(self):
  self.assertEqual(v.MAX_ATTEMPTS,3)
  self.assertEqual(v.RETRY_HTTP,{429,502,503,504})
 def test_transport_category_does_not_leak_network_names(self):
  self.assertEqual(v.transport_category("timed out"),"TIMEOUT")
  self.assertEqual(v.transport_category("certificate verify failed"),"TLS")
  self.assertEqual(v.transport_category("Temporary failure in name resolution"),"DNS")
 def test_redirect_to_outside_provider_is_denied(self):
  import urllib.request,urllib.error
  handler=v.StrictProvider()
  request=urllib.request.Request(v.URL)
  with self.assertRaises(urllib.error.HTTPError):
   handler.redirect_request(request,None,302,"Found",{},"https://untrusted.example/other.js")
if __name__=="__main__":unittest.main()

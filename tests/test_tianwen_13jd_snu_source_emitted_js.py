import hashlib,importlib.util,unittest,urllib.error,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13jd-snu-source-emitted-js.py"
spec=importlib.util.spec_from_file_location("t13jd",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

class FirstpartyScripts(unittest.TestCase):
 def test_source_provenance(self):
  self.assertEqual(v.SOURCE_HTML_ARTIFACT,12792862189)
  self.assertEqual(v.SOURCE_HTML_SHA256,"31c9afa4e92d68b6ec728758c20ca4cd0787c91a5690cbcd222bf8febdd13374")
 def test_three_exact_source_emitted_paths_only(self):
  self.assertEqual(v.SOURCE_EMITTED_SCRIPTS,("/js/common.js","/js/common2.js","/js/ux.js"))
  self.assertEqual(v.script_url("/js/common2.js"),"https://kyudb.snu.ac.kr/js/common2.js")
  with self.assertRaises(ValueError):v.script_url("/imgviewer/new-guess.js")
 def test_definition_found_without_folio_award(self):
  x=v.analyze(b"function fn_originalImg(item_cd,book_cd,vol_no,page_no){return '/viewer';}")
  self.assertTrue(x["function_definition_observed"])
  self.assertEqual(x["independent_physical_witness_votes"],0)
  self.assertFalse(x["printed_folio_acquired"])
  self.assertIsNone(x["original_image_bytes"])
 def test_comment_not_function(self):
  raw=b"/* function fn_originalImg(x) {} */\n// function fn_originalImg(y) {}\nvar x=3;"
  self.assertFalse(v.analyze(raw)["function_definition_observed"])
 def test_assignment_function(self):
  self.assertTrue(v.analyze(b"window.fn_originalImg = function(a,b) {return 1;}")["function_definition_observed"])
 def test_sha_replay(self):
  raw=b"function other(){}"
  self.assertEqual(v.analyze(raw)["sha256"],hashlib.sha256(raw).hexdigest())
 def test_html_and_binary_rejected(self):
  self.assertEqual(v.classify_payload("text/javascript",b" <html>blocked</html>"),"HTML_NOT_SCRIPT")
  self.assertEqual(v.classify_payload("image/jpeg",b"123"),"UNEXPECTED_MEDIA_TYPE")
 def test_bound_attempts(self):
  self.assertEqual(v.MAX_ATTEMPTS,3)
  self.assertEqual(v.failure_category("certificate verify failed"),"TLS")
 def test_cross_host_redirect_rejected(self):
  handler=v.FirstpartyOnly()
  with self.assertRaises(urllib.error.HTTPError):
   handler.redirect_request(urllib.request.Request(v.BASE),None,302,"Found",{},"https://attacker.example/other.js")

if __name__=="__main__":unittest.main()

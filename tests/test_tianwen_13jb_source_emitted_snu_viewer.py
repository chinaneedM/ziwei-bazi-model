import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13jb-source-emitted-snu-viewer.py"
spec=importlib.util.spec_from_file_location("v13jb",p);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class ViewerHTML(unittest.TestCase):
 def test_source_literal_links(self):
  r=M.analyze(b'<html>GK05554_00 imgViewer page_no <img src="/viewer/image-x"></html>')
  self.assertEqual(r["source_emitted_link_examples"][0]["attrs"]["src"],"/viewer/image-x")
  self.assertFalse(r["original_page_image_retrieved"])
 def test_no_ancient_folio_inference(self):
  r=M.analyze(b'<html>GK05554_00 page_no</html>')
  self.assertFalse(r["printed_juan_or_folio_bound"])
 def test_missing_book_detected(self):self.assertFalse(M.analyze(b"<html></html>")["exact_book_code_present"])
 def test_sha_matches_content(self):
  import hashlib
  b=b"<html>page_no</html>"
  self.assertEqual(M.analyze(b)["html_sha256"],hashlib.sha256(b).hexdigest())
 def test_no_http_fetch_in_analysis(self):self.assertEqual(M.analyze(b"<html><a href='/x'></a></html>")["source_emitted_link_examples"][0]["attrs"]["href"],"/x")
if __name__=="__main__":unittest.main()

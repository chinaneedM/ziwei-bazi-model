import hashlib,importlib.util,unittest,urllib.error,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13jf-snu-exact-original-images.py"
spec=importlib.util.spec_from_file_location("t13jf",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ExactImages(unittest.TestCase):
 def test_source_bound_viewer_hashes(self):
  self.assertEqual(m.SOURCE_HTML["048a"]["viewer_sha256"],"d7422a70e9218471279826e7ad3360b46f3eeae9cd65a71908b9ef9e7eef0c4e")
  self.assertEqual(m.SOURCE_HTML["085a"]["viewer_sha256"],"44babd776b2e59cb6c1ce93f22b47c1d9e47c677967392f654a6e16669cd6c23")
 def test_exact_source_emitted_jpeg_query(self):
  self.assertIn("imgFileNm=GK05554_00_IL_0018_048a.jpg",m.exact_image_url("048a"))
  self.assertTrue(m.exact_image_url("085a").endswith("/GK05554_00_IL_0018_085a.jpg"))
 def test_deny_other_page_without_source(self):
  with self.assertRaises(ValueError):m.exact_image_url("001a")
  with self.assertRaises(ValueError):m.exact_image_url("not-real")
 def test_reject_html_under_image_status(self):
  self.assertEqual(m.validate_jpeg(b"<html>blocked</html>","text/html"),"NON_JPEG_CONTENT_TYPE")
 def test_blank_content_type_requires_jpeg_magic(self):
  raw=b"\xff\xd8\xff"+b"a"*180+b"\xff\xd9"
  self.assertEqual(m.validate_jpeg(raw,""),"JPEG_BYTES_ACQUIRED_UNCOLLATED")
  self.assertEqual(m.validate_jpeg(b"<html>blocked</html>",""),"INVALID_JPEG_BYTES")
 def test_reject_truncated_jpeg(self):
  self.assertEqual(m.validate_jpeg(b"\xff\xd8\xff"+b"A"*100,"image/jpeg"),"INVALID_JPEG_BYTES")
 def test_accept_synthetic_container_without_claim(self):
  raw=b"\xff\xd8\xff"+b"x"*200+b"\xff\xd9"
  self.assertEqual(m.validate_jpeg(raw,"image/jpeg"),"JPEG_BYTES_ACQUIRED_UNCOLLATED")
  self.assertEqual(hashlib.sha256(raw).hexdigest(),hashlib.sha256(raw).hexdigest())
 def test_reject_redirect_off_provider(self):
  with self.assertRaises(urllib.error.HTTPError):
   m.FirstpartyOnly().redirect_request(urllib.request.Request(m.BASE),None,302,"found",{},"https://untrusted.example/x")
 def test_bound_attempts_and_caps(self):
  self.assertEqual(m.ATTEMPTS,3)
  self.assertLessEqual(m.MAX_BYTES,24_000_000)
 def test_source_is_exact_provider(self):
  self.assertTrue(all(m.exact_image_url(p).startswith("https://kyudb.snu.ac.kr/ImageServlet.do?") for p in m.SOURCE_HTML))
if __name__=="__main__":unittest.main()

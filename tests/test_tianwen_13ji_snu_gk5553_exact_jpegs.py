import hashlib,importlib.util,unittest,urllib.error,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13ji-snu-gk5553-exact-jpegs.py"
spec=importlib.util.spec_from_file_location("t13ji",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ExactJpeg(unittest.TestCase):
 def test_provenance_sha(self):
  self.assertEqual(v.SOURCE_ARTIFACT,12807899103)
  self.assertEqual(v.VOLUMES["0029"]["html_sha256"],"18d51d8fb8571fc455129781ac9b0ab0d57752f67002216d702b89ac270d891d")
 def test_allowed_exact_source_calls(self):
  self.assertTrue(v.source_target("0012","075a"))
  self.assertTrue(v.source_target("0029","081a"))
  self.assertFalse(v.source_target("0029","075a"))
  self.assertFalse(v.source_target("0046","001a"))
 def test_post_field_provenance(self):
  d=v.body("0029","001a").decode()
  self.assertIn("book_cd=GK05553_00",d)
  self.assertIn("vol_no=0029",d)
  self.assertIn("add_page_no=",d)
 def test_bad_page_rejected(self):
  with self.assertRaises(ValueError):v.body("0012","001a")
 def test_exact_server_link_only(self):
  src="/ImageServlet.do?imgFileNm=GK05553_00_IL_0029_001a.jpg&path=/data01/stream/GJB/IMG/GK05553_00/GK05553_00_0029/GK05553_00_IL_0029_001a.jpg"
  self.assertTrue(v.authorize_src(src,"0029","001a"))
  self.assertFalse(v.authorize_src(src,"0012","002a"))
  self.assertFalse(v.authorize_src(src.replace("ImageServlet.do","FakeServlet.do"),"0029","001a"))
 def test_html_extraction(self):
  h=b'<html><img src="/ImageServlet.do?imgFileNm=test.jpg&path=xyz"></html>'
  p=v.Images();p.feed(h.decode());self.assertEqual(len(p.srcs),1)
 def test_jpeg_content_type_blank(self):
  raw=b"\xff\xd8\xff"+b"a"*220+b"\xff\xd9"
  self.assertTrue(v.valid_jpeg(raw,""))
  self.assertFalse(v.valid_jpeg(b"<html>denied</html>",""))
 def test_mime_reject_html(self):
  self.assertFalse(v.valid_jpeg(b"\xff\xd8\xff"+b"x"*150+b"\xff\xd9","text/html"))
 def test_firstparty_redirect(self):
  with self.assertRaises(urllib.error.HTTPError):
   v.SourceOnly().redirect_request(urllib.request.Request(v.VIEWER),None,302,"Found",{},"https://attacker.example/image")
if __name__=="__main__":unittest.main()

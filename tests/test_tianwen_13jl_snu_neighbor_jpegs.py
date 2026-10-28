import importlib.util,unittest,urllib.error,urllib.request
from pathlib import Path
f=Path(__file__).resolve().parents[1]/'scripts/probe-tianwen-13jl-snu-gk5553-neighbor-jpegs.py'
spec=importlib.util.spec_from_file_location('jl',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SixOriginals(unittest.TestCase):
 def test_source_run(self):
  self.assertEqual(m.SOURCE_RUN,40674164409);self.assertEqual(m.SOURCE_ARTIFACT,12809168697)
 def test_exact_six_volumes(self):
  self.assertEqual(set(m.VOLUMES),{'0008','0026','0011','0013','0025','0027'})
 def test_exact_page_source_gate(self):
  self.assertTrue(m.source_target('0026','001a'));self.assertTrue(m.source_target('0011','002a'))
  self.assertFalse(m.source_target('0011','001a'));self.assertFalse(m.source_target('0029','001a'))
 def test_image_signature(self):
  raw=b'\xff\xd8\xff'+b'z'*250+b'\xff\xd9'
  self.assertTrue(m.valid_jpeg(raw,''));self.assertFalse(m.valid_jpeg(raw,'text/html'))
 def test_cross_host_denied(self):
  with self.assertRaises(urllib.error.HTTPError):m.SourceOnly().redirect_request(urllib.request.Request(m.VIEWER),None,302,'x',{},'https://fake.example/image')
 def test_strict_source_image_path(self):
  s='/ImageServlet.do?imgFileNm=GK05553_00_IL_0026_001a.jpg&path=/data01/stream/GJB/IMG/GK05553_00/GK05553_00_0026/GK05553_00_IL_0026_001a.jpg'
  self.assertTrue(m.authorize_src(s,'0026','001a'));self.assertFalse(m.authorize_src(s,'0008','001a'))
if __name__=='__main__':unittest.main()

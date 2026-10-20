import importlib.util,json,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-najda-goryeosa-13av.py"
s=importlib.util.spec_from_file_location("naj13av",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13AV(unittest.TestCase):
 def test_three_source_image_ordinals_only(self):
  self.assertEqual(m.source_page_ordinals(32),[3,21,26])
  self.assertEqual(m.source_page_ordinals(26),[])
  self.assertEqual(m.MAX_DOWNLOAD_IMAGES,3)
 def test_no_guessed_image_resource(self):
  u="https://www.digital.archives.go.jp/api/content/item/da12/C103403935300/iiif/M2022071510153404631_0004.jp2/full/max/0/native.jpg"
  j={"sequences":[{"canvases":[{"images":[{"resource":{"@id":u}}]}]}]}
  self.assertEqual(m.manifest_full_jpeg_urls(json.dumps(j).encode()),[u])
  j["sequences"][0]["canvases"][0]["images"][0]["resource"]["@id"]="https://example.org/x.jpg"
  self.assertEqual(m.manifest_full_jpeg_urls(json.dumps(j).encode()),[])
if __name__=="__main__":unittest.main()

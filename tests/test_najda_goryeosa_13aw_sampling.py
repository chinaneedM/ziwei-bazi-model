import importlib.util, json, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-najda-goryeosa-13aw.py"
spec=importlib.util.spec_from_file_location("naj13aw",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13AW(unittest.TestCase):
 def test_manifest_indices(self):
  self.assertEqual(m.source_page_ordinals(32),[22,24,28])
  self.assertEqual(m.source_page_ordinals(28),[])
  self.assertEqual(m.MAX_DOWNLOAD_IMAGES,3)
 def test_only_firstparty_published_resource(self):
  u="https://www.digital.archives.go.jp/api/content/item/da12/C103403937200/iiif/M2022071510153404631_0023.jp2/full/max/0/native.jpg"
  j={"sequences":[{"canvases":[{"images":[{"resource":{"@id":u}}]}]}]}
  self.assertEqual(m.manifest_full_jpeg_urls(json.dumps(j).encode()),[u])
  j["sequences"][0]["canvases"][0]["images"][0]["resource"]["@id"]="https://other.example/test.jpg"
  self.assertEqual(m.manifest_full_jpeg_urls(json.dumps(j).encode()),[])
if __name__=="__main__":unittest.main()

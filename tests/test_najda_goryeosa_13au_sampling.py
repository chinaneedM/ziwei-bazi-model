import importlib.util, json, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-najda-goryeosa-13au.py"
spec=importlib.util.spec_from_file_location("naj13au",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13AU(unittest.TestCase):
 def test_only_exact_three_source_ordinals(self):
  self.assertEqual(m.source_page_ordinals(32),[2,15,30])
  self.assertEqual(m.source_page_ordinals(0),[])
  self.assertEqual(m.source_page_ordinals(30),[])
  self.assertEqual(m.MAX_DOWNLOAD_IMAGES,3)
 def test_only_source_emitted_allowlisted_iiif_resource(self):
  u="https://www.digital.archives.go.jp/api/content/item/da12/C103403935200/iiif/M2022071510153404631_0003.jp2/full/max/0/native.jpg"
  j={"sequences":[{"canvases":[{"images":[{"resource":{"@id":u}}]}]}]}
  self.assertEqual(m.manifest_full_jpeg_urls(json.dumps(j).encode()),[u])
  j["sequences"][0]["canvases"][0]["images"][0]["resource"]["@id"]="https://example.org/forged.jpg"
  self.assertEqual(m.manifest_full_jpeg_urls(json.dumps(j).encode()),[])
if __name__=="__main__":unittest.main()

import importlib.util, json, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-najda-goryeosa-13ay.py"
s=importlib.util.spec_from_file_location("naj13ay",p); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
GOOD="https://www.digital.archives.go.jp/api/content/item/da12/C103403937300/iiif/M2022071510153404631_0024.jp2/full/max/0/native.jpg"
def manifest(urls):
 return json.dumps({"sequences":[{"canvases":[{"images":[{"resource":{"@id":u}}]} for u in urls]}]}).encode()
class TestNaj13ay(unittest.TestCase):
 def test_exact_four_disjoint_parts(self):
  self.assertEqual([m.part_indices(i) for i in (1,2,3,4)],[list(range(0,8)),list(range(8,16)),list(range(16,24)),list(range(24,32))])
  with self.assertRaises(ValueError):m.part_indices(5)
 def test_only_exact_provider_emitted_urls(self):
  urls=[GOOD.replace("_0024.jp2",f"_{i:04d}.jp2") for i in range(1,33)]
  self.assertEqual(m.parse_manifest(manifest(urls)),urls)
  with self.assertRaises(ValueError):m.parse_manifest(manifest(urls[:-1]))
  urls[2]="https://other.example/api/content/item/da12/C12/iiif/M11_1.jp2/full/max/0/native.jpg"
  with self.assertRaises(ValueError):m.parse_manifest(manifest(urls))
 def test_reject_duplicates_and_bypass(self):
  urls=[GOOD.replace("_0024.jp2",f"_{i:04d}.jp2") for i in range(1,33)]
  urls[31]=urls[0]
  with self.assertRaises(ValueError):m.parse_manifest(manifest(urls))
  urls[31]="https://www.digital.archives.go.jp/api/content/item/da12/C123/iiif/M1_1.jp2/full/max/0/native.jpg?token=x"
  with self.assertRaises(ValueError):m.parse_manifest(manifest(urls))
if __name__=="__main__":unittest.main()

import importlib.util,unittest,json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-najda-goryeosa-13az.py"
s=importlib.util.spec_from_file_location("probe13az",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13AZ(unittest.TestCase):
 def test_exact_item_pair(self):
  doc='<h3 id="row-52-title"><a href="'+m.ITEM+'"><span>高麗史５１</span></a></h3><a href="'+m.VIEWER+'">Browse</a><h3 id="row-53-title">高麗史５２</h3>'
  self.assertTrue(m.provider_bound_book51(doc))
  self.assertFalse(m.provider_bound_book51(doc.replace(m.VIEWER,"https://example.test/img/en/4898853")))
 def test_source_manifest(self):
  self.assertEqual(m.emitted_manifest('<a href="https://www.digital.archives.go.jp/api/iiif/4898853/manifest.json">manifest</a>'),"https://www.digital.archives.go.jp/api/iiif/4898853/manifest.json")
 def test_only_exact_original_canvas_resource(self):
  u="https://www.digital.archives.go.jp/api/content/item/da12/C103403937300/iiif/M2022071510153404631_0024.jp2/full/max/0/native.jpg"
  def enc(u):return json.dumps({"sequences":[{"canvases":[{"images":[{"resource":{"@id":u}}]}]}]}).encode()
  self.assertEqual(m.manifest_urls(enc(u)),[u])
  with self.assertRaises(ValueError):m.manifest_urls(enc(u+"?guess=1"))
  with self.assertRaises(ValueError):m.manifest_urls(enc("https://fake.test/img.jpg"))
if __name__=="__main__":unittest.main()

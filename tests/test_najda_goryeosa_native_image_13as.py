import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-najda-goryeosa-13as.py"
q=importlib.util.spec_from_file_location("acq13as",p);m=importlib.util.module_from_spec(q);q.loader.exec_module(m)
class Test13AS(unittest.TestCase):
 def test_original_emitted_paths(self):
  data='var najContentList = [{"path":"/content/item/da12/C103403935000/iiif/M2022071510153404631_0001.jp2","contentName":"x","source":{"width":6500,"height":4800}}];'
  rows=m.extracted_image_metadata(data);self.assertEqual(len(rows),1)
  self.assertEqual(rows[0]["width"],6500)
 def test_no_guessed_paths(self):
  self.assertEqual(m.extracted_image_metadata('var najContentList = [{"path":"../../etc/passwd"}];'),[])
 def test_manifest_firstparty_only(self):
  self.assertEqual(m.emitted_manifest_link('<a href="https://www.digital.archives.go.jp/api/iiif/4898854/manifest.json">IIIF</a>'),"https://www.digital.archives.go.jp/api/iiif/4898854/manifest.json")
  self.assertIsNone(m.emitted_manifest_link('<a href="https://example.org/api/iiif/4898854/manifest.json">fake</a>'))
if __name__=="__main__":unittest.main()

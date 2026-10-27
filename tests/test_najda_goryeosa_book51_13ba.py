import importlib.util,unittest,json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-najda-goryeosa-book51-13ba.py"
s=importlib.util.spec_from_file_location("naj13ba",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13BA(unittest.TestCase):
 def test_exact_disjoint_36(self):
  self.assertEqual([m.part_indices(k) for k in range(1,5)],[list(range(0,9)),list(range(9,18)),list(range(18,27)),list(range(27,36))])
  with self.assertRaises(ValueError):m.part_indices(0)
 def test_manifest_immutable_gate(self):
  with self.assertRaises(ValueError):m.provider_urls(json.dumps({"sequences":[{"canvases":[]}]}).encode())
 def test_expected_source_host(self):
  self.assertEqual(m.MANIFEST,"https://www.digital.archives.go.jp/api/iiif/4898853/manifest.json")
if __name__=="__main__":unittest.main()

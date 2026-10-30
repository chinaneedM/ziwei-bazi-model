"""13LY volume-index positive route and conservative page-capture scope."""
import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/probe-tianwen-13ly-bsb-volume1-manifest.py"
s=importlib.util.spec_from_file_location("bsb1",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestManifest(unittest.TestCase):
 def test_declared_provider_id(self):self.assertTrue(m.URL.endswith("/bsb11166691/manifest"))
 def test_deny_offsite(self):
  with self.assertRaises(ValueError):m.safe("https://example.com/iiif")
 def test_bounded_indices(self):
  a=m.indices(1880);self.assertEqual(len(a),40);self.assertEqual(a[0],1);self.assertEqual(a[-1],1880)
 def test_small_index(self):self.assertEqual(m.indices(3),[1,2,3])
 def test_iiif_v2_service(self):
  self.assertEqual(m.service({"images":[{"resource":{"service":{"@id":"https://api.digitale-sammlungen.de/i"}}}]}),"https://api.digitale-sammlungen.de/i")
if __name__=="__main__":unittest.main()

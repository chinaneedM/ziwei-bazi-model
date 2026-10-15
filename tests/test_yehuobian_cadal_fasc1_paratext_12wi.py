import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("cadalwi",ROOT/"scripts/probe-yehuobian-cadal-fasc1-paratext-12wi.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SourceGate(unittest.TestCase):
 def test_only_first_fascicle_source(self):
  self.assertEqual(m.CADAL_ID,"02096900")
  self.assertEqual(m.TITLE,"File:CADAL02096900 野獲編（一）.djvu")
 def test_inventory_original_bytes(self):self.assertEqual(m.EXPECTED_INVENTORY_BYTES,2833699)
 def test_bound(self):self.assertEqual(m.MAX_SOURCE,8_000_000)
 def test_commons_original_host_only(self):
  self.assertIsNone(m.check_host("https://upload.wikimedia.org/wikipedia/commons/1/11/a.djvu"))
  with self.assertRaisesRegex(ValueError,"non-commons"):m.check_host("https://evil.test/a.djvu")
  with self.assertRaisesRegex(ValueError,"non-commons"):m.check_host("http://upload.wikimedia.org/wikipedia/commons/a.djvu")
 def test_no_unsafe_filename_guessing(self):
  self.assertTrue(m.COMMS_API.startswith("https://commons.wikimedia.org/"))
if __name__=="__main__":unittest.main()

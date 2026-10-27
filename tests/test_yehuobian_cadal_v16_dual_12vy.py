import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"scripts/probe-yehuobian-cadal-v16-dual-images-12vy.py"
spec=importlib.util.spec_from_file_location("cadal12vy",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class SourceScope(unittest.TestCase):
 def test_two_separate_digital_files(self):
  self.assertEqual([x["id"] for x in v.SOURCES],["CADAL02096915","CADAL02112262"])
 def test_hash_provenance(self):
  self.assertTrue(all(len(x["sha1"])==40 for x in v.SOURCES))
 def test_page_bounds(self):
  self.assertTrue(all(max(x["pages"])<=x["expected_pages"] for x in v.SOURCES))
 def test_existing_sha256_preserved(self):
  self.assertTrue(v.SOURCES[0]["existing_sha256"].startswith("262edac8"))
 def test_second_identity_not_assumed(self):
  self.assertIsNone(v.SOURCES[1]["existing_sha256"])
 def test_only_public_commons_hosts(self):
  self.assertTrue(all(x["url"].startswith("https://upload.wikimedia.org/wikipedia/commons/") for x in v.SOURCES))
 def test_8mb_bound(self):
  self.assertEqual(v.LIMIT,8000000)
if __name__=="__main__":unittest.main()

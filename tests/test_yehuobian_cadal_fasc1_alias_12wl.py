import importlib.util,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("wl",ROOT/"scripts/probe-yehuobian-cadal-fasc1-old-new-alias-12wl.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class FirstFascicleCommonsBounds(unittest.TestCase):
 def test_valid_original_two_ids(self):self.assertTrue(m.validate_config())
 def test_only_old_and_new_fascicle_one(self):
  bad=[dict(x) for x in m.ITEMS];bad[0]["title"]="File:野獲編(十六).djvu"
  with self.assertRaisesRegex(ValueError,"first fascicle"):m.validate_config(tuple(bad))
 def test_strict_known_source_sha256(self):
  bad=[dict(x) for x in m.ITEMS];bad[1]["expected_sha256"]="0"*64
  with self.assertRaisesRegex(ValueError,"sha256"):m.validate_config(tuple(bad))
 def test_unchanged_catalogue_reported_bytes(self):
  bad=[dict(x) for x in m.ITEMS];bad[0]["expected_bytes"]=2791558
  with self.assertRaisesRegex(ValueError,"byte boundary"):m.validate_config(tuple(bad))
 def test_only_original_signature_page_range(self):
  with self.assertRaisesRegex(ValueError,"fixed selected"):m.validate_config(m.ITEMS,(5,6,7,10))
 def test_capture_inherits_12wc_host_and_size_gates(self):
  mod=m.load_capture_module()
  with self.assertRaisesRegex(ValueError,"unexpected source host"):mod.check_url("http://example.com/image.djvu","upload.wikimedia.org","/wikipedia/commons/")
  with self.assertRaisesRegex(ValueError,"unexpected source host"):mod.check_url("https://upload.wikimedia.org/private/secrets","upload.wikimedia.org","/wikipedia/commons/")
 def test_no_direct_printing_claim_in_captured_wrapper(self):
  self.assertEqual(m.KNOWN_NEW_SHA,"711dc16b17d139612fbe852dc99869bb709b85c161440dfc7618ee1dbd6f38fa")
if __name__=="__main__":unittest.main()

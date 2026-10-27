import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ww",ROOT/"scripts/probe-yehuobian-12ww-tokyo-kanseki-search-js.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class OfficialSourceScript(unittest.TestCase):
 def test_provider_exact_uri(self):self.assertTrue(m.guard())
 def test_deny_guessed_script(self):
  with self.assertRaisesRegex(ValueError,"original form"):m.guard("https://kanseki.ioc.u-tokyo.ac.jp/user/js/imaginary.js")
 def test_real_js_scope(self):
  z=m.inspect(b'function qadv_ck() { return true; }')
  self.assertTrue(z["contains_advanced_form_validator"])
  self.assertFalse(z["no_1827_1869_page_images"] is False)
  self.assertTrue(z["no_independent_historical_print_vote"])
 def test_missing_validator_kept_unknown(self):
  z=m.inspect(b'function search(){}')
  self.assertFalse(z["contains_advanced_form_validator"])
  self.assertIsNone(z["qadv_ck_source_excerpt"])
 def test_too_large(self):
  with self.assertRaisesRegex(ValueError,"too large"):m.inspect(b"b"*(m.LIMIT+1))
 def test_no_automatic_get_search(self):self.assertFalse("query_adv.php?" in m.SCRIPT_URL)
if __name__=="__main__":unittest.main()

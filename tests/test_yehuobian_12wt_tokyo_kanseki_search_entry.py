import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("wt",ROOT/"scripts/probe-yehuobian-12wt-tokyo-kanseki-official-search-entry.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ExactGeneralCatalog(unittest.TestCase):
 def test_real_home(self):self.assertTrue(m.exact_url(m.LANDING))
 def test_reject_guessed_volume_and_folio(self):
  for x in ("https://kanseki.ioc.u-tokyo.ac.jp/user/book.php?id=6403767830",
            "https://kanseki.ioc.u-tokyo.ac.jp/user/index.php?volume=6403148395",
            "http://kanseki.ioc.u-tokyo.ac.jp/user/index.php"):
   with self.assertRaisesRegex(ValueError,"only provider-issued"):m.exact_url(x)
 def test_source_form_parsed_not_executed(self):
  b=b'<form method="post" action="list.php"><input name="keyword"><select name="col"><option value="ti"></option></select></form>'
  r=m.parse(b)
  self.assertEqual(r["forms"][0]["method"],"POST")
  self.assertEqual(r["forms"][0]["inputs"][0]["name"],"keyword")
  self.assertEqual(r["forms"][0]["selects"][0]["options"],["ti"])
  self.assertFalse(r["official_volume_item_search_executed"])
 def test_image_elements_not_original_page_review(self):
  r=m.parse(b'<img src="/user/images/button.gif"><a href="help.php">help</a>')
  self.assertEqual(r["source_emitted_image_element_count"],1)
  self.assertFalse(r["juan20_original_paper_scan_acquired"])
  self.assertEqual(r["historical_independent_print_votes"],0)
 def test_relative_scripts_resolved_without_fetching(self):
  r=m.parse(b'<script src="assets/search.js"></script>')
  self.assertEqual(r["source_emitted_script_urls"],["https://kanseki.ioc.u-tokyo.ac.jp/user/assets/search.js"])
 def test_no_oversize(self):
  with self.assertRaisesRegex(ValueError,"oversize"):m.parse(b"a"*(m.MAX_BYTES+1))
 def test_no_fabricated_object_binding(self):
  r=m.parse("6403767830 6403148395".encode())
  self.assertFalse(r["item_6403767830_explicitly_bound"])
  self.assertFalse(r["item_6403148395_explicitly_bound"])
if __name__=="__main__":unittest.main()

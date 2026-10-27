import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("wv",ROOT/"scripts/probe-yehuobian-12wv-tokyo-kanseki-advanced-form.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class FormOnly(unittest.TestCase):
 def test_source_emitted(self):self.assertTrue(m.guard(m.SOURCE))
 def test_no_guessed_item_route(self):
  for s in ["https://kanseki.ioc.u-tokyo.ac.jp/user/query_detail.php?dno=6403767830","http://kanseki.ioc.u-tokyo.ac.jp/user/query_adv.php"]:
   with self.assertRaisesRegex(ValueError,"source-issue"):m.guard(s)
 def test_form_method_and_select_options(self):
  raw=b'<form action="result.php" method="post"><input name="key"><select name="col"><option value="title">Title</option></select></form>'
  x=m.parse(raw)
  self.assertEqual(x["html_forms"][0]["method"],"POST")
  self.assertEqual(x["html_forms"][0]["fields"][0]["name"],"key")
  self.assertEqual(x["html_forms"][0]["selects"][0]["options"][0]["value"],"title")
  self.assertFalse(x["source_catalog_historic_title_query_executed"])
 def test_form_controls_do_not_attest_paper(self):
  r=m.parse(b'<form><input name="6403767830"></form>')
  self.assertEqual(r["historic_independent_print_votes"],0)
  self.assertFalse(r["item_6403767830_page_image_proven"])
 def test_emitted_external_script_stays_source_only(self):
  r=m.parse(b'<script src="js/form.js"></script>')
  self.assertEqual(r["external_script_urls"],["https://kanseki.ioc.u-tokyo.ac.jp/user/js/form.js"])
  self.assertEqual(r["new_original_juan20_glyphs"],0)
 def test_byte_limit(self):
  with self.assertRaisesRegex(ValueError,"too large"):m.parse(b"a"*(m.MAX_BYTES+1))
if __name__=="__main__":unittest.main()

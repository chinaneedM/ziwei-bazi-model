import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("wq",ROOT/"scripts/probe-yehuobian-12wq-tokyo-shanben-source-issued-index.py")
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class TokyoListSourceOnly(unittest.TestCase):
 def test_actual_emitted_link(self):self.assertTrue(p.validate_url("https://shanben.ioc.u-tokyo.ac.jp/list.php"))
 def test_guessed_id_denied(self):
  with self.assertRaisesRegex(ValueError,"not source-issued"):p.validate_url("https://shanben.ioc.u-tokyo.ac.jp/view.php?id=6403767830")
 def test_sitemap_not_image(self):
  with self.assertRaisesRegex(ValueError,"not source-issued"):p.validate_url("https://shanben.ioc.u-tokyo.ac.jp/juan20.jpg")
 def test_parser_retains_actual_form_controls(self):
  raw=b'<form method="GET" action="/list.php"><input name="page" value="1"><select name="section"><option value="2">B</option></select></form>'
  d=p.summarize(raw)
  self.assertEqual(d["html_forms"][0]["inputs"][0]["name"],"page")
  self.assertEqual(d["html_forms"][0]["selects"][0]["options"],["2"])
 def test_catalog_name_not_copy_image(self):
  raw="野獲編 6403767830 6403148395".encode()
  d=p.summarize(raw)
  self.assertTrue(d["visible_text_mentions_yekakuhen"])
  self.assertTrue(d["visible_text_mentions_1827_copy_identifier"])
  self.assertFalse(d["original_paper_copy_bound"])
  self.assertFalse(d["original_juan20_image_acquired"])
  self.assertEqual(d["ancient_print_votes"],0)
 def test_page_count_does_not_prove_absence(self):
  raw="共 3889 筆，目前 1 / 195 頁".encode()
  d=p.summarize(raw)
  self.assertFalse(d["source_attests_entire_shanben_catalog_absence"])
  self.assertTrue(d["index_page_labels"])
 def test_source_max_size(self):
  with self.assertRaisesRegex(ValueError,"too large"):p.summarize(b"a"*(p.MAX_BYTES+1))
 def test_prevent_bulk(self):self.assertLessEqual(p.MAX_BYTES,600000)
if __name__=="__main__":unittest.main()

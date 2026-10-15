import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("wx",ROOT/"scripts/probe-yehuobian-12wx-tokyo-kanseki-exact-title.py")
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
class ProviderOneTitleSearch(unittest.TestCase):
 def test_exact_single_title_query(self):
  pairs=p.payload()
  self.assertTrue(p.guard(p.URL,pairs))
  self.assertEqual(pairs[1][1],"and"+chr(30)+"ti"+chr(30)+"野獲編"+chr(31))
 def test_no_guessed_record_id(self):
  with self.assertRaisesRegex(ValueError,"first-party"):p.guard("https://kanseki.ioc.u-tokyo.ac.jp/user/query_detail.php?no=6403767830")
 def test_no_multiple_bulk_titles(self):
  pairs=p.payload();pairs[1]=("q_str","野獲編|other")
  with self.assertRaisesRegex(ValueError,"exact source JS"):p.guard(p.URL,pairs)
 def test_positive_catalog_row_not_glyph(self):
  z=p.examine("<a href='query_detail.php'>野獲編</a>".encode())
  self.assertEqual(z["source_visible_target_anchor_count"],1)
  self.assertFalse(z["source_emitted_original_volume20_paper_image"])
  self.assertEqual(z["new_independent_historical_paper_impression_votes"],0)
 def test_zero_result_does_not_erase_cinii(self):
  z=p.examine("無任何資料".encode())
  self.assertTrue(z["a_zero_hit_is_not_absence_of_tokyo_cinii_holdings"])
  self.assertEqual(z["source_visible_target_anchor_count"],0)
 def test_script_echo_not_visible_result(self):
  z=p.examine("<script>var q='野獲編'</script><p>No records</p>".encode())
  self.assertFalse(z["result_visible_title_in_page"])
 def test_response_guard(self):
  with self.assertRaisesRegex(ValueError,"too large"):p.examine(b"x"*(p.MAX+1))
 def test_no_image_url_guesses(self):
  self.assertNotIn("6403767830",p.URL)
if __name__=="__main__":unittest.main()

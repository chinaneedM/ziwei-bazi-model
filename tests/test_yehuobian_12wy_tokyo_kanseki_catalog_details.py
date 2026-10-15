import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("wy",ROOT/"scripts/probe-yehuobian-12wy-tokyo-kanseki-seven-catalog-details.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class SevenExactSourceDetails(unittest.TestCase):
 def test_seven_source_ids(self):
  self.assertEqual([z[0] for z in m.ACTUAL_PROVIDER_TUPLES],["9927","9928","78464","90972","103841","104379","109371"])
 def test_id_and_rank_bound(self):
  self.assertTrue(m.url_for("103841",5).endswith("dno=103841&no=5&tp=qadv"))
  with self.assertRaisesRegex(ValueError,"not one of seven"):m.url_for("103841",4)
 def test_no_random_ids(self):
  with self.assertRaisesRegex(ValueError,"not one of seven"):m.url_for("6403148395",7)
 def test_original_detail_not_paper_glyph(self):
  z=m.parse("9927",1,"野獲編 道光七年 大木".encode())
  self.assertTrue(z["visible_1827_year"])
  self.assertFalse(z["original_page_pixels_downloaded"])
  self.assertFalse(z["independent_historical_print_voting"])
 def test_html_button_retains_source_link(self):
  z=m.parse("90972",4,b'<a href="../fulltext/abc">abc</a><img src="portrait.jpg" onclick="zoom()"/>')
  self.assertEqual(z["provider_emitted_href_controls"][0]["href"],"../fulltext/abc")
  self.assertEqual(z["provider_emitted_image_controls"][0]["onclick"],"zoom()")
 def test_cap(self):
  with self.assertRaisesRegex(ValueError,"exceeded cap"):m.parse("9927",1,b"x"*(m.MAX_PAGE+1))
 def test_no_ocr(self):
  self.assertFalse(m.parse("90972",4,b"<p>text</p>")["ocr"])
 def test_exact_query_sha(self):
  self.assertEqual(len(m.SOURCE_HTML_SHA256),64)
if __name__=="__main__":unittest.main()

import importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-najda-goryeosa-13ap.py"
s=importlib.util.spec_from_file_location("najda13ap",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestNAJSourceEmittedLinks(unittest.TestCase):
 def test_exact_html_anchor(self):
  html='<a href="/item/12345">高麗史５２</a><a href="/item/6789">高麗史５３</a>'
  self.assertEqual(m.exact_item_links(html),["https://www.digital.archives.go.jp/item/12345"])
 def test_no_link_guessing(self):
  html='<span>高麗史５２</span><a href="https://example.com/item/12345">高麗史５２</a>'
  self.assertEqual(m.exact_item_links(html),[])
 def test_firstparty_en_links_with_same_row_pairing(self):
  row='<li class="archive-result-table__body-item"><a href="https://www.digital.archives.go.jp/item/en/4898854">高麗史５２</a><a href="https://www.digital.archives.go.jp/img/en/4898854">Browse</a></li>'
  self.assertEqual(m.exact_item_links(row),["https://www.digital.archives.go.jp/item/en/4898854"])
  self.assertEqual(m.exact_image_links(row),["https://www.digital.archives.go.jp/img/en/4898854"])
 def test_cross_row_mismatch_rejected(self):
  row1='<li class="archive-result-table__body-item"><a href="/item/en/1234">高麗史５２</a><a href="/img/en/1235">Browse</a></li>'
  self.assertEqual(m.exact_image_links(row1),[])
 def test_bounded(self):
  self.assertLessEqual(m.CAP,1500000)
  self.assertEqual(m.SOURCE,"https://www.digital.archives.go.jp/search?fond=1073275&lang=en&page=1")
if __name__=="__main__":unittest.main()

import importlib.util
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts" / "probe-nikh-goryeosa-image-13ez.py"
spec = importlib.util.spec_from_file_location("probe13ez", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class Test13EZ(unittest.TestCase):
    def test_explicit_notice_link(self):
        html = '<a href="/main/notice/noticeView.do?noticeId=sample">고려사 원문이미지 LINK 변경 안내</a>'
        self.assertEqual(m.official_notice_links(html), ["https://db.history.go.kr/main/notice/noticeView.do?noticeId=sample"])
    def test_js_link_not_guessed(self):
        h = '<a href="javascript:goNotice(123)">고려사 원문이미지 LINK 변경 안내</a>'
        self.assertEqual(m.official_notice_links(h), [])
    def test_outside_host_not_followed(self):
        h = '<a href="https://example.org/notice/noticeView.do?noticeId=123">고려사 원문이미지 LINK 변경 안내</a>'
        self.assertEqual(m.official_notice_links(h), [])
    def test_jeolyo_not_accepted(self):
        h = '<a href="/main/notice/noticeView.do?noticeId=sample">고려사절요 원문이미지 LINK 변경 안내</a>'
        self.assertEqual(m.official_notice_links(h), [])
    def test_bounded_context_only_literal_source(self):
        got = m.bounded_literal_context("abc TARGET xyz", "TARGET", flank=2)
        self.assertEqual(got[0]["markup"], "c TARGET xy")
    def test_no_guessed_2023_notice_markup(self):
        self.assertEqual(m.bounded_literal_context("<div>other</div>", m.NOTICE_TITLE), [])
    def test_only_original_widget_metadata_not_photo(self):
        p = m.PageAnchors()
        p.feed('<button onclick="showViewer(1)" title="고려사 원문이미지">원문이미지</button>')
        self.assertEqual(p.image_widgets[0]["attributes"]["onclick"], "showViewer(1)")
        self.assertTrue("onclick" in p.image_widgets[0]["attributes"])

if __name__ == "__main__":
    unittest.main()

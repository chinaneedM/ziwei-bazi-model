"""Synthetic inputs validate fail-closed source locator handling, not history."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/acquire-tianwen-13kb-g893-neighbor-pages.py'
spec = importlib.util.spec_from_file_location('neighbor_intake', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestSourceIssuedNeighborGate(unittest.TestCase):
    def test_target_window_narrow(self):
        self.assertEqual(mod.TARGETS, ('020a', '035a', '037a'))
        self.assertTrue(set(mod.TARGETS).isdisjoint(mod.PREEXISTING))

    def test_official_path_emitted_is_required(self):
        full = mod.DIR + 'GK00893_00IH_0001_020a.jpg'
        url = mod.source_issued_image_url('020a', "var imgFileNm = '" + full + "';")
        mod.validate_url('020a', url)
        self.assertIn('imgFileNm=GK00893_00IH_0001_020a.jpg', url)

    def test_reject_bare_or_synthetic_name(self):
        for html in ('', 'var imgFileNm = "GK00893_00IH_0001_020a.jpg";',
                     'var imgFileNm = "/unrelated/GK00893_00IH_0001_020a.jpg";',
                     "var imgFileNm = '" + mod.DIR + "GK00893_00IH_0001_019b.jpg';"):
            with self.subTest(html=html):
                with self.assertRaises(ValueError):
                    mod.source_issued_image_url('020a', html)

    def test_reject_wrong_book_or_wrong_route(self):
        for bad in (
            'https://other.example/ImageServlet.do?imgFileNm=a&path=b',
            'https://kyudb.snu.ac.kr/ImageServlet.do?imgFileNm=GK00893_00IH_0001_035a.jpg&path=%2Ftmp%2Fimg.jpg',
            'https://kyudb.snu.ac.kr/other?imgFileNm=a&path=b'):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    mod.validate_url('035a', bad)

    def test_image_bytes_must_be_valid(self):
        with self.assertRaises(ValueError):
            mod.inspect_image(b'<html>not source image</html>')

    def test_unregistered_neighbor_cannot_be_issued(self):
        with self.assertRaises(ValueError):
            mod.source_issued_image_url('036b', 'var imgFileNm = "' + mod.DIR + 'GK00893_00IH_0001_036b.jpg";')


if __name__ == '__main__':
    unittest.main()

import gzip
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('gk3467color', ROOT / 'scripts/acquire-gk3467-listed-color-pages-13if.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class ProviderListedPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = gzip.decompress(M.SOURCE.read_bytes()).decode()

    def test_real_first_party_list_and_cover(self):
        pages = M.listed_pages(self.source)
        self.assertEqual(len(pages), 104)
        self.assertEqual(pages[:4], ['000a', '000b', '001a', '001b'])
        self.assertEqual(len(M.image_urls(self.source, '000a')), 1)

    def test_cover_url_cannot_attest_an_unreturned_page(self):
        self.assertEqual(M.image_urls(self.source, '001a'), [])

    def test_page_list_cannot_inject_an_arbitrary_identifier(self):
        bad = self.source.replace("fn_goPageJumpWithMokIdxClear('001a')", "fn_goPageJumpWithMokIdxClear('../secret')")
        with self.assertRaises(ValueError):
            M.listed_pages(bad)

    def test_foreign_image_host_rejected(self):
        bad = self.source.replace("location.href='/ImageDown.do?", "location.href='https://example.org/ImageDown.do?")
        self.assertEqual(M.image_urls(bad, '000a'), [])

    def test_cross_book_path_rejected(self):
        bad = self.source.replace('/data01/stream/STH/IMG/GK03467_04/', '/data01/stream/STH/IMG/GK05553_00/')
        self.assertEqual(M.image_urls(bad, '000a'), [])

    def test_retry_subset_cannot_introduce_unknown_or_duplicate_pages(self):
        pages = M.listed_pages(self.source)
        self.assertEqual(M.select_pages(pages, ['000a', '000b', '001a']), ['000a', '000b', '001a'])
        for requested in (['099a'], ['001a', '001a'], []):
            with self.subTest(requested=requested), self.assertRaises(ValueError):
                M.select_pages(pages, requested)


if __name__ == '__main__':
    unittest.main()

"""13KF fail-closed binary intake: no historical winner or guessed target folio."""
import importlib.util
import unittest
from pathlib import Path

path=Path(__file__).resolve().parents[1]/"scripts/acquire-tianwen-13kf-harvard-mingshi-v10.py"
spec=importlib.util.spec_from_file_location("harvard_intake",path)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class HarvardGate(unittest.TestCase):
    def test_specific_harvard_drs_volume10(self):
        self.assertEqual(mod.TITLE,"File:Harvard drs 428231183 明史 v.10.pdf")
        self.assertIn("428231183",mod.SPECIAL)
    def test_metadata_scoped_exact_title(self):
        v={"query":{"pages":{"42":{"title":mod.TITLE,"imageinfo":[{"url":"https://upload.wikimedia.org/wikipedia/commons/f/fe/Harvard.pdf","mime":"application/pdf","size":60000000,"sha1":"a"*40}]}}}}
        self.assertEqual(mod.parse_metadata(v)["size"],60000000)
    def test_reject_false_title(self):
        v={"query":{"pages":{"42":{"title":"File:unrelated.pdf","imageinfo":[{"url":"https://upload.wikimedia.org/wikipedia/commons/f/fe/z.pdf","mime":"application/pdf","size":60000000}]}}}}
        with self.assertRaises(ValueError):mod.parse_metadata(v)
    def test_reject_non_source_host(self):
        for url in ("https://fake.example/a.pdf","http://upload.wikimedia.org/wikipedia/commons/x.pdf",
                    "https://upload.wikimedia.org/wikipedia/commons/z.jpg",
                    "https://upload.wikimedia.org/other/secret.pdf"):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):mod.validate_source_url(url)
    def test_reject_fake_mime(self):
        v={"query":{"pages":{"3":{"title":mod.TITLE,"imageinfo":[{"url":"https://upload.wikimedia.org/wikipedia/commons/f/fe/a.pdf","mime":"text/html","size":60000000}]}}}}
        with self.assertRaises(ValueError):mod.parse_metadata(v)

if __name__=="__main__":unittest.main()

"""13KI source URL / SHA-1 identity: reject unrelated images and unsupported copy attribution."""
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/acquire-tianwen-13ki-shanghai-huang.py"
spec=importlib.util.spec_from_file_location("shanghai_huang_intake",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def record(title=v.TITLE,sha1=v.EXPECTED_SHA1,size=v.EXPECTED_BYTES,url="https://upload.wikimedia.org/wikipedia/commons/2/25/test.pdf",mime="application/pdf"):
    return {"query":{"pages":{"1":{"title":title,"imageinfo":[{"url":url,"size":size,"sha1":sha1,"mime":mime}]}}}}

class SourceIdentity(unittest.TestCase):
    def test_provider_metadata(self):
        self.assertEqual(v.read_metadata(record())["sha1"],v.EXPECTED_SHA1)
        self.assertEqual(v.UPSTREAM_UPLOAD_NAME,"dGJ2300966.pdf")
    def test_reject_wrong_file_name(self):
        with self.assertRaises(ValueError):v.read_metadata(record(title="File:1923 assumed.pdf"))
    def test_reject_wrong_sha_or_size(self):
        for kwargs in ({"sha1":"0"*40},{"size":1}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):v.read_metadata(record(**kwargs))
    def test_reject_wrong_mime(self):
        with self.assertRaises(ValueError):v.read_metadata(record(mime="text/html"))
    def test_reject_non_source_urls(self):
        for u in ("https://example.org/a.pdf","http://upload.wikimedia.org/wikipedia/commons/2/2/a.pdf",
                  "https://upload.wikimedia.org/wikipedia/commons/2/2/a.png",
                  "https://upload.wikimedia.org/wikipedia/other/a.pdf"):
            with self.subTest(url=u):
                with self.assertRaises(ValueError):v.valid_original_url(u)
    def test_source_does_not_bind_1923_impression(self):
        self.assertIn("NOT_PROVEN_1923",v.download.__code__.co_consts.__repr__())

if __name__=="__main__":unittest.main()

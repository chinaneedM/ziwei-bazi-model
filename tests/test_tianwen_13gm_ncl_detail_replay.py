import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ncl_detail_replay', ROOT/'scripts/verify-tianwen-13gm-ncl-detail-replay.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class DetailReplayTest(unittest.TestCase):
    def setUp(self):
        self.e = json.loads(m.EVIDENCE.read_text(encoding='utf-8'))
        self.raw = gzip.decompress((ROOT/self.e['source']['archive']).read_bytes())
    def test_real_public_response(self):
        self.assertTrue(m.check(self.e, self.raw))
    def test_wrong_book_rejected_even_with_recomputed_digest(self):
        raw = self.raw.replace(b'03130', b'03136')
        self.e['source']['sha256'] = hashlib.sha256(raw).hexdigest()
        with self.assertRaises(AssertionError): m.check(self.e, raw)
    def test_forged_original_value_rejected(self):
        self.e['unresolved']['old_d30'] = '四分九二二二'
        with self.assertRaises(AssertionError): m.check(self.e, self.raw)
    def test_catalog_date_cannot_be_relabelled(self):
        self.e['metadata']['出版年(西曆)'] = '1905'
        with self.assertRaises(AssertionError): m.check(self.e, self.raw)
    def test_truncation_rejected(self):
        with self.assertRaises(AssertionError): m.check(self.e, self.raw[:-100])
    def test_duplicate_title_rejected(self):
        raw = self.raw + '<tr><th>正題名</th><td>另一書</td></tr>'.encode()
        self.e['source'].update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        with self.assertRaises(AssertionError): m.check(self.e, raw)
if __name__ == '__main__': unittest.main()

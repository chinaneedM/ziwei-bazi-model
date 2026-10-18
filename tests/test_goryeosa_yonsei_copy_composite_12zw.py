import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-yonsei-copy-composite-12zw.py"
spec=importlib.util.spec_from_file_location("yonsei_12zw",P)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class Yonsei12ZWTests(unittest.TestCase):
    def test_machine_consistency(self):
        self.assertEqual(mod.verify()["status"],"PASS")
    def test_manuscript_books_not_woodblock_votes(self):
        d=mod.load(mod.DOC)
        self.assertEqual(d["explicit_book_level_composite"]["work_volumes"],[122,123])
        self.assertFalse(d["explicit_book_level_composite"]["ordinary_woodblock_numeric_vote_for_122_123"])
    def test_no_fake_colophon_or_original_target(self):
        d=mod.load(mod.DOC)
        self.assertIsNone(d["physical"]["work52_target_original_image_sha256"])
        self.assertFalse(d["impression_scope"]["dated_edition_colophon_seen"])
    def test_original_prior_preserved(self):
        p=mod.load(mod.PRIOR)
        self.assertIsNone(p["new_physical_copy_candidate"]["work52_original_image_sha256"])
if __name__=="__main__":
    unittest.main()

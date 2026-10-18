import unittest
from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-yonsei-later-impression-12zv.py"
spec=importlib.util.spec_from_file_location("heritage_12zv",P)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class TestYonsei12ZV(unittest.TestCase):
    def test_source_graded_physical_copy(self):
        self.assertEqual(mod.verify()["status"],"PASS")
    def test_no_fake_original_glyph(self):
        d=mod.load(mod.DOC)
        self.assertIsNone(d["new_physical_copy_candidate"]["work52_original_image_sha256"])
        self.assertEqual(d["unresolved"]["new_cross_physical_d16_d18_votes"],0)
    def test_prior_snapshot_preserved(self):
        p=mod.load(mod.PRIOR)
        self.assertEqual([x["snu_catalog_code"] for x in p["items"]],["GK03539_00","GK03579_00"])
if __name__=="__main__":
    unittest.main()

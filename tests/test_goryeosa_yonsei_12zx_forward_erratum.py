import unittest
import importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-yonsei-12zx-forward-erratum.py"
spec=importlib.util.spec_from_file_location("yonsei_12zx",p)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class TestYonseiForwardErratum(unittest.TestCase):
    def test_forward_correction(self):
        self.assertEqual(mod.verify()["corrected_field_overclaims"],2)
    def test_52_book_index_is_unknown(self):
        x=mod.read(mod.DOC)
        self.assertIsNone(x["effective_copy_reading"]["work52_in_physical_book30"])
        self.assertIsNone(x["effective_copy_reading"]["work52_material_type"])
    def test_139_cannot_be_called_printed_original(self):
        x=mod.read(mod.DOC)
        self.assertIsNone(x["prior_field_overclaims"][0]["original_woodblock_printed_work_volume_total"])
if __name__=="__main__":
    unittest.main()

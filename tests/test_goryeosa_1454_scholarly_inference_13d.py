import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-1454-scholarly-inference-13d.py"
sp=importlib.util.spec_from_file_location("goryeosa13d",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class TestGoryeosa13D(unittest.TestCase):
 def test_contract(self):self.assertEqual(m.verify()["status"],"PASS")
 def test_scholar_not_historical_print_receipt(self):self.assertIsNone(m.read(m.E)["evidence_scope"]["verified_1454_distribution_delivery_receipt"])
 def test_pdf_and_html_same_source(self):self.assertTrue(m.read(m.E)["evidence_scope"]["nihk_text_and_pdf_same_intellectual_source"])
 def test_work52_still_missing(self):self.assertIsNone(m.read(m.E)["evidence_scope"]["work52_D16_D18_native_folio_sha256"])
if __name__=="__main__":unittest.main()

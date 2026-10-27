import unittest
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-gugak-3539-caption-12zz.py"
sp=importlib.util.spec_from_file_location("goryeosa_12zz",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class TestGoryeosa12ZZ(unittest.TestCase):
 def test_contract(self): self.assertEqual(m.verify()["status"],"PASS")
 def test_1454_not_physical_print(self):
  d=m.read(m.P);self.assertFalse(d["historical_inference"]["media_year_1454_proves_original_copy_printed_1454"])
 def test_no_duplicate_witness(self):
  d=m.read(m.P);self.assertEqual(d["historical_inference"]["independent_physical_witnesses_from_6426_and_6545"],0)
 def test_target_52_still_unbound(self):
  d=m.read(m.P);self.assertIsNone(d["original_snu_copy"]["work52_exact_physical_book"])
if __name__=="__main__":unittest.main()

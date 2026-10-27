import unittest
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-snu-curatorial-13b.py"
sp=importlib.util.spec_from_file_location("goryeosa_13b",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class TestGoryeosa13B(unittest.TestCase):
 def test_contract(self): self.assertEqual(m.verify()["status"],"PASS")
 def test_retrospective_not_verified_distribution(self):
  x=m.load(m.P)
  self.assertFalse(x["decision"]["can_prove_1453_oct_wide_print_distribution"])
 def test_1454_report_not_completed_new_print(self):
  x=m.load(m.P)
  self.assertFalse(x["decision"]["can_prove_1454_new_approval_completed"])
 def test_no_work52_target(self):
  x=m.load(m.P)
  self.assertIsNone(x["decision"]["target_work52_book_number"])
if __name__=="__main__":unittest.main()

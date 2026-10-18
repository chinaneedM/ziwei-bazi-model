import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-gukjobogam-13f.py"
s=importlib.util.spec_from_file_location("goryeosa13f",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestGoryeosa13F(unittest.TestCase):
 def test_gate(self): self.assertEqual(m.verify()["status"],"PASS")
 def test_no_print_receipt(self):self.assertFalse(m.rd(m.E)["read_locus"]["text_proves_copies_delivered"])
 def test_later_copy(self):self.assertEqual(m.rd(m.E)["catalog"]["edition_catalog_date"],1782)
if __name__=="__main__": unittest.main()

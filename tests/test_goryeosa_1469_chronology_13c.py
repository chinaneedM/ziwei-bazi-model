import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-1469-chronology-13c.py"
s=importlib.util.spec_from_file_location("goryeosa13c",p); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13C(unittest.TestCase):
 def test_contract(self): self.assertEqual(m.verify()["status"],"PASS")
 def test_no_false_publication(self):self.assertFalse(m.load(m.E)["scope"]["petition_1469_fulfilled"])
 def test_no_numeric_original(self):self.assertIsNone(m.load(m.E)["scope"]["original_work52_D16_D18_sha256"])
if __name__=="__main__":unittest.main()

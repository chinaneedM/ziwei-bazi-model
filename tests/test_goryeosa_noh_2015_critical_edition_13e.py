import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-noh-2015-critical-edition-13e.py"
s=importlib.util.spec_from_file_location('goryeosa13e',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestGoryeosa13E(unittest.TestCase):
 def test_gate(self):self.assertEqual(m.verify()['status'],'PASS')
 def test_no_folio(self):self.assertIsNone(m.read(m.E)['boundaries']['direct_original_woodblock_page_sha256'])
 def test_no_independent_vote(self):self.assertEqual(m.read(m.E)['boundaries']['new_independent_physical_witnesses'],0)
if __name__=='__main__':unittest.main()

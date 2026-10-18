import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import importlib.util
P=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-ncl-copyscope-13g.py"
spec=importlib.util.spec_from_file_location("verify13g",P);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestCopyScope13G(unittest.TestCase):
    def test_guard(self):
        self.assertEqual(mod.verify()["status"],"PASS")
if __name__=="__main__": unittest.main()

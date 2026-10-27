import unittest,copy,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v13in",ROOT/"scripts/verify-tianwen-13in-gk5553-material.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class MaterialScope(unittest.TestCase):
    def test_current_evidence(self):self.assertTrue(m.check(m.read()))
    def test_no_book29_original_image(self):
        a=copy.deepcopy(m.read());a["snu_firstparty"]["book29_original_folio_images_obtained"]=True
        with self.assertRaises(AssertionError):m.check(a,False)
    def test_no_paper_error_without_original(self):
        a=copy.deepcopy(m.read());a["conflict"]["paper_proven_wrong"]=True
        with self.assertRaises(AssertionError):m.check(a,False)
    def test_no_spurious_g893_closure(self):
        a=copy.deepcopy(m.read());a["evidence_scope"]["confirms_g893_six_numerals"]=True
        with self.assertRaises(AssertionError):m.check(a,False)
if __name__=="__main__":unittest.main()

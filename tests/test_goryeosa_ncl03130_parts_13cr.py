import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-ncl03130-parts-13cr.py"
spec=importlib.util.spec_from_file_location("ncl13cr",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class Test13CR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
    def check(self,e=None,s=None,l=None):
        return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
    def test_positive(self):self.assertTrue(self.check())
    def test_no_false_part_to_book_identity(self):
        e=copy.deepcopy(self.e);e["mismatch_firewall"]["mirror_part_count_is_physical_book_count"]=True
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_no_false_juan52_part_08(self):
        e=copy.deepcopy(self.e);e["mismatch_firewall"]["pdf_part_08_proves_juan52"]=True
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_missing_red_bookfront(self):
        e=copy.deepcopy(self.e);e["priority_front_part"]["image_obtained"]=True
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_missing_part_rejected(self):
        e=copy.deepcopy(self.e);e["mirror_parts"].pop()
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_unsupported_third_vote(self):
        e=copy.deepcopy(self.e);e["mismatch_firewall"]["third_independent_historical_d16_copy_votes"]=1
        with self.assertRaises(AssertionError):self.check(e=e)
    def test_state_ledger_mismatch(self):
        s=copy.deepcopy(self.s);s["schema_version"]="1.999.0"
        with self.assertRaises(AssertionError):self.check(s=s)
if __name__=="__main__":unittest.main()

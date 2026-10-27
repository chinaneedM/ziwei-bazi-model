import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ver13io',ROOT/'scripts/verify-tianwen-13io-copy-map-and-head-repair.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ScopeRepair(unittest.TestCase):
    def test_repository_replay(self): self.assertTrue(m.check(m.read()))
    def test_no_unjustified_copy_juan(self):
        d=copy.deepcopy(m.read());d['snu_firstparty']['book_29_juan_81_83_explicitly_bound']=True
        with self.assertRaises(AssertionError):m.check(d,False)
    def test_no_premature_material_verdict(self):
        d=copy.deepcopy(m.read());d['adjudication']['physical_copy_material_conflict_between_the_two_proven']=True
        with self.assertRaises(AssertionError):m.check(d,False)
    def test_no_false_archival_upgrade(self):
        d=copy.deepcopy(m.read());d['journal_2020']['raw_pdf_sha256']='fabricated'
        with self.assertRaises(AssertionError):m.check(d,False)
    def test_no_algorithm_reopen(self):
        d=copy.deepcopy(m.read());d['adjudication']['algorithm_reopen_count']=1
        with self.assertRaises(AssertionError):m.check(d,False)
if __name__=='__main__':unittest.main()

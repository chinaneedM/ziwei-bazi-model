import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ver13ip",ROOT/"scripts/verify-tianwen-13ip-catalog-and-legacy-ci.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Check13IP(unittest.TestCase):
    def test_repo(self): self.assertTrue(m.check(m.read()))
    def test_no_unproved_imprint(self):
        d=copy.deepcopy(m.read());d["adjudication"]["specific_NCID_bound_to_GK5554_paper_claim"]=True
        with self.assertRaises(AssertionError): m.check(d,False)
    def test_no_old_mapping(self):
        d=copy.deepcopy(m.read());d["adjudication"]["book29_to_juan81_83_binding_retracted_by_13io"]=False
        with self.assertRaises(AssertionError): m.check(d,False)
    def test_no_source_vote(self):
        d=copy.deepcopy(m.read());d["adjudication"]["new_original_pages"]=1
        with self.assertRaises(AssertionError): m.check(d,False)
if __name__=="__main__": unittest.main()

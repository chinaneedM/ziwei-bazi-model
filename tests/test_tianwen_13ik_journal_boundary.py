import copy, importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify13ik",ROOT/"scripts/verify-tianwen-13ik-journal-boundary.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class Gate(unittest.TestCase):
    def test_source_scope(self): self.assertTrue(m.check(m.read()))
    def test_no_original_pdf_false_positive(self):
        for k,v in (("pdf_binary_obtained",True),("original_article_target_paragraph_original_page_verified",True),("original_article_target_footnotes_verified",True)):
            x=copy.deepcopy(m.read()); x["source_layer"][k]=v
            with self.assertRaises(AssertionError): m.check(x,False)
    def test_no_missing_leaf_false_positive(self):
        for k,v in (("physically_missing_leaf_count",6),("other_volume_lacuna_reporting_implies_volume52_completeness",True)):
            x=copy.deepcopy(m.read());x["copy_layer"][k]=v
            with self.assertRaises(AssertionError):m.check(x,False)
    def test_no_stemmatic_or_chart_promotion(self):
        x=copy.deepcopy(m.read());x["adjudication"]["new_independent_historical_vote_count"]=1
        with self.assertRaises(AssertionError):m.check(x,False)
if __name__=="__main__": unittest.main()

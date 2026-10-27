import copy, importlib.util, unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify13il",root/"scripts/verify-tianwen-13il-snu-copy-scope.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class SourceFirewall(unittest.TestCase):
    def test_real(self):self.assertTrue(module.check(module.read()))
    def test_catalog_is_not_original_leaf(self):
        x=copy.deepcopy(module.read());x["original_scope"]["number_physically_missing_leaves"]=6
        with self.assertRaises(AssertionError):module.check(x,False)
    def test_1972_5554_not_same_copy(self):
        x=copy.deepcopy(module.read());x["journal_reconciliation"]["are_facsimile_base_and_target_same_item"]=True
        with self.assertRaises(AssertionError):module.check(x,False)
    def test_pdf_not_verified(self):
        x=copy.deepcopy(module.read());x["journal_reconciliation"]["original_article_pdf_bytes_obtained"]=True
        with self.assertRaises(AssertionError):module.check(x,False)
if __name__=="__main__":unittest.main()

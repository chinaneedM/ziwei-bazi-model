import copy
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tianwen13ig",ROOT/"scripts/verify-tianwen-13ig-catalog-paratext.py")
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
class CatalogParatextScopeTest(unittest.TestCase):
    def test_live_repository_evidence_and_state(self):
        self.assertTrue(M.check(M.load()))
    def test_catalog_cannot_supply_original_leaf(self):
        for key in ("own_winter_table_title_original_page","frontmatter_physical_presence_in_book6","exact_impression_year","book_level_physical_leaf_missing_count"):
            with self.subTest(key=key):
                x=copy.deepcopy(M.load());x["source_copy_grade"][key]="CATALOG_ASSUMPTION"
                with self.assertRaises(AssertionError):M.check(x,False)
    def test_no_fullbook_absence_from_bounded_images(self):
        x=copy.deepcopy(M.load())
        x["source_copy_grade"]["whole_book_linewise_negative_proof"]=True
        with self.assertRaises(AssertionError):M.check(x,False)
    def test_catalog_1451_is_not_physical_impression(self):
        x=copy.deepcopy(M.load())
        x["adjudication"]["catalog_paratext_proves_same_copy_1451_folio"]=True
        with self.assertRaises(AssertionError):M.check(x,False)
if __name__=="__main__":unittest.main()

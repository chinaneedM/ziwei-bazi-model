import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tianwen_13hk",ROOT/"scripts/verify-tianwen-13hk-ncl03130-teldap-catalog-crosswalk.py")
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
class NCL03130TeldapCatalogScope(unittest.TestCase):
    def setUp(self):
        self.e=json.loads(M.E.read_text(encoding="utf8"))
    def test_institutional_catalog_scope_and_prior_sha(self):
        self.assertTrue(M.check(self.e))
    def test_aggregation_is_not_new_physical_copy(self):
        e=copy.deepcopy(self.e);e["deduplication"]["does_not_create_an_independent_physical_copy"]=False
        with self.assertRaises(AssertionError):M.check(e)
    def test_catalog_datetime_not_page_ink_date(self):
        e=copy.deepcopy(self.e);e["chronology_disambiguation"]["physical_copy_item_specific_folio_date"]="1644-1735"
        with self.assertRaises(AssertionError):M.check(e)
    def test_standalone_catalog_is_not_native_item_record(self):
        e=copy.deepcopy(self.e);e["institutional_catalog"]["provider_native_exact_item_record_obtained"]=True
        with self.assertRaises(AssertionError):M.check(e)
    def test_ncl_d14_does_not_inherit_nikh_string(self):
        e=copy.deepcopy(self.e);e["unresolved_original"]["national_library_native_d14_complete_literal"]="四分六六三〇"
        with self.assertRaises(AssertionError):M.check(e)

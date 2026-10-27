import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("tianwen_13hf",ROOT/"scripts/verify-tianwen-13hf-ncl03130-access-rights.py")
M=importlib.util.module_from_spec(S)
S.loader.exec_module(M)
class NCL03130HighResAndRights(unittest.TestCase):
    def setUp(self):
        self.e=json.loads(M.E.read_text(encoding="utf8"))
    def test_source_scoped_policy(self):
        self.assertTrue(M.check(self.e))
    def test_research_image_has_not_been_authorized(self):
        e=copy.deepcopy(self.e);e["firstparty"]["reading_scope"]["research_high_resolution_approval_granted"]=True
        with self.assertRaises(AssertionError):M.check(e)
    def test_public_format_does_not_prove_specific_300dpi_image(self):
        e=copy.deepcopy(self.e);e["firstparty"]["licensing_scope"]["image_available_for_item_03130_in_format"]="300dpi TIFF"
        with self.assertRaises(AssertionError):M.check(e)
    def test_digital_reuse_license_not_automatically_granted(self):
        e=copy.deepcopy(self.e);e["firstparty"]["licensing_scope"]["commercial_or_rehosting_permission_granted"]=True
        with self.assertRaises(AssertionError):M.check(e)
    def test_application_not_submitted(self):
        e=copy.deepcopy(self.e);e["firstparty"]["licensing_scope"]["formal_request_submitted"]=True
        with self.assertRaises(AssertionError):M.check(e)
    def test_ncl_missing_original_cannot_copy_nikh_numeral(self):
        e=copy.deepcopy(self.e);e["target"]["NCL_original_full_D14_literal"]="四分六六三〇"
        with self.assertRaises(AssertionError):M.check(e)
    def test_platform_rights_do_not_resolve_object_license(self):
        e=copy.deepcopy(self.e);e["firstparty"]["notices_are_a_copy_specific_legal_resolution"]=True
        with self.assertRaises(AssertionError):M.check(e)

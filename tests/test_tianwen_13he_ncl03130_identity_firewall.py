import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tianwen_13he",ROOT/"scripts/verify-tianwen-13he-ncl03130-identity-firewall.py")
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
class NCL03130IdentityFirewall(unittest.TestCase):
    def setUp(self):
        self.e=json.loads(M.E.read_text(encoding="utf8"))
    def test_documented_metadata_and_source_sha(self):
        self.assertTrue(M.check(self.e))
    def test_catalog_year_cannot_promote_folio_age(self):
        e=copy.deepcopy(self.e)
        e["commons_bibliographic_transcription"]["juan52_copy_layer"]="GUANGXU_SUPPLEMENT"
        with self.assertRaises(AssertionError):M.check(e)
    def test_upload_label_cannot_be_recast_as_source_file(self):
        e=copy.deepcopy(self.e)
        e["commons_upload_sample"]["pdf_content_replacement_proven"]=True
        with self.assertRaises(AssertionError):M.check(e)
    def test_old_ncl_d14_cannot_inherit_nikh_photo(self):
        e=copy.deepcopy(self.e)
        e["day14_scope"]["NCL_03130_09_p74_D14_full_original_literal"]="四分六六三〇"
        with self.assertRaises(AssertionError):M.check(e)
    def test_original_copy_is_not_proven_by_pdf_count(self):
        e=copy.deepcopy(self.e)
        e["commons_upload_sample"]["pdf_to_physical_book_fascicle_mapping_proven"]=True
        with self.assertRaises(AssertionError):M.check(e)

import copy
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ver13it",ROOT/"scripts"/"verify-tianwen-13it-heritage-copy-crosswalk.py")
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
class ScopeTests(unittest.TestCase):
    def setUp(self): self.e=M.load()
    def test_live(self): self.assertTrue(M.check(self.e))
    def test_secondary_cannot_be_promoted_to_firstparty(self):
        self.e["evidence_tiers"]["copied_heritage_description"]["official_paragraph_verified_against_firstparty"]=True
        with self.assertRaises(AssertionError): M.check(self.e)
    def test_book29_mapping_cannot_be_promoted(self):
        self.e["evidence_tiers"]["kyujanggak_firstparty_catalog"]["explicit_book29_to_juan81_83_binding"]=True
        with self.assertRaises(AssertionError): M.check(self.e)
    def test_secondary_number_conflict_cannot_silently_close(self):
        self.e["source_conflicts"]["supplement_book_number_sets"]["resolved"]=True
        with self.assertRaises(AssertionError): M.check(self.e)
    def test_original_numerical_cannot_be_invented(self):
        self.e["controls"]["nlc03130_solar_d30"]=49386
        with self.assertRaises(AssertionError): M.check(self.e)
    def test_no_false_new_original(self):
        self.e["controls"]["new_original_images"]=1
        with self.assertRaises(AssertionError): M.check(self.e)
    def test_retraction_is_preserved(self):
        self.e["source_conflicts"]["historical_13IN_book29_to_juan81_83_status"]="CONFIRMED"
        with self.assertRaises(AssertionError): M.check(self.e)
    def test_source_scope_must_stay_separate(self):
        self.e["evidence_tiers"]["korean_heritage_firstparty_index"]["official_long_description_directly_retrieved"]=True
        with self.assertRaises(AssertionError): M.check(self.e)
if __name__=="__main__": unittest.main()

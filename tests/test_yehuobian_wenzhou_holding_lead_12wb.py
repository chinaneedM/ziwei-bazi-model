import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("wb",ROOT/"scripts/verify-yehuobian-wenzhou-holding-lead-12wb.py")
wb=importlib.util.module_from_spec(spec)
spec.loader.exec_module(wb)

class WenzhouScope(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((ROOT/wb.REC).read_text())
        self.st=json.loads((ROOT/wb.STATE).read_text())
    def bad(self,key):
        with self.assertRaisesRegex(ValueError,key): wb.validate(self.r,self.st)
    def test_live_evidence_ledger(self):
        self.assertEqual(wb.validate(self.r,self.st)["new_independent_print_votes"],0)
    def test_no_independent_edition_vote_from_mixed_label(self):
        self.r["physical_target_gate"]["independent_1827_versus_1869_glyph_votes"]=2
        self.bad("no print comparison")
    def test_cannot_upgrade_secondary_to_official_item(self):
        self.r["secondary_catalogue"]["item_specific_official_confirmation"]=True
        self.bad("no false official item")
    def test_no_ancient_glyph_without_source(self):
        self.r["physical_target_gate"]["four_loci"]["GONGJIN"]="宮禁"
        self.bad("no glyph votes")
    def test_opac_timeout_not_absence_proof(self):
        self.r["first_party_access"]["opac_timeout_not_negative_catalogue_result"]=False
        self.bad("scoped OPAC boundary")
    def test_eight_copy_queue_unchanged(self):
        self.r["crosswalk"]["add_to_existing_eight_verified_item_bound_candidates"]=True
        self.bad("eight item packet unchanged")
    def test_no_unperformed_outreach(self):
        self.r["first_party_access"]["contact_attempted"]=True
        self.bad("no external action")
if __name__=="__main__": unittest.main()

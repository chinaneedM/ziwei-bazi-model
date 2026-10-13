#!/usr/bin/env python3
import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify12uw",ROOT/"scripts/verify-yehuobian-tokyo-two-print-inquiry-12uw.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class TokyoOriginalPrintInquiry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load(m.RECORD);cls.p=load(m.PACKET)
    def check(self,r=None,p=None):
        return m.validate(r if r is not None else self.r,p if p is not None else self.p)
    def mutate(self, path, value):
        r=copy.deepcopy(self.r);cur=r
        for x in path[:-1]:cur=cur[x]
        cur[path[-1]]=value
        with self.assertRaises(ValueError):self.check(r)
    def test_baseline_two_copies(self):self.assertEqual(self.check()["item_bound_print_candidates"],2)
    def test_1869_preface_not_1827_target(self):self.mutate(["scope_firewalls","1827_preface_in_1869_copy_not_1827_print_impression"],False)
    def test_notes_archive_is_not_rare_books(self):self.mutate(["scope_firewalls","lecture_notes_archive_not_kuraishi_rare_book_scan"],False)
    def test_source_issued_image_absent(self):self.mutate(["physical_targets",1,"source_issued_image_url"],"https://example.org/undocumented.jpg")
    def test_original_folio_is_unbound(self):self.mutate(["physical_targets",0,"original_folio"],"12")
    def test_sha_not_assumed(self):self.mutate(["physical_targets",1,"target_page_sha256"],"0"*64)
    def test_print_state_not_verified(self):self.mutate(["physical_targets",1,"physical_impression_verified"],True)
    def test_no_cad_alternative_glyph_vote(self):self.mutate(["physical_targets",1,"source_glyph_votes"],1)
    def test_four_loci_are_unread(self):self.mutate(["physical_targets",0,"readings","CLOCK_NOUN"],"宮漏")
    def test_copy_specific_rights_unknown(self):self.mutate(["physical_targets",0,"copy_specific_permission"],True)
    def test_no_email_sent(self):self.mutate(["external_actions","sent"],True)
    def test_no_paid_order(self):self.mutate(["external_actions","reproduction_order"],True)
    def test_2023_reservation_not_2026_verified(self):self.mutate(["scope_firewalls","2023_reservation_guide_not_assumed_updated_2026_policy"],False)
    def test_item_identity_unmodified(self):self.mutate(["physical_targets",1,"item"],"6403148396")
    def test_no_historical_source_count(self):self.mutate(["acquisition","new_historical_source_registry_rows"],1)
    def test_counts_unchanged(self):self.mutate(["accounting","sources_total"],688)
if __name__=="__main__":unittest.main()

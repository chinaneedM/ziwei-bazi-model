#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("packet12uu",ROOT/"scripts/verify-yehuobian-original-juan20-acquisition-packet-12uu.py")
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)
class OriginalJuan20PacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def j(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
        cls.data=j(m.DATA);cls.base=j(m.BASE);cls.extra=j(m.EXTRA);cls.damaged=j(m.DAMAGED)
    def trial(self,d=None,b=None,e=None,z=None):
        return m.validate(d if d is not None else self.data,b if b is not None else self.base,e if e is not None else self.extra,z if z is not None else self.damaged)
    def test_exact_prior_queue_is_accepted(self):
        self.assertEqual(self.trial()["catalogued_actionable_candidates"],8)
    def test_original_page_url_without_image_not_allowed(self):
        d=copy.deepcopy(self.data);d["original_copy_candidates"][0]["source_issued_original_image_url"]="https://example.org/not-proved"
        with self.assertRaises(ValueError):self.trial(d)
    def test_modern_transcription_not_original_glyph(self):
        d=copy.deepcopy(self.data);d["original_copy_candidates"][0]["four_locus_readings"]["GONGJIN"]="宮禁"
        with self.assertRaises(ValueError):self.trial(d)
    def test_revised_1869_does_not_become_1827_original(self):
        d=copy.deepcopy(self.data)
        next(x for x in d["original_copy_candidates"] if x["queue_id"]=="TOKYO_1869_6403148395")["date_class"]="CATALOGUED_1827_IMPRESSION_UNVERIFIED"
        with self.assertRaises(ValueError):self.trial(d)
    def test_first_fascicle_is_not_kyoto_target(self):
        d=copy.deepcopy(self.data)
        next(x for x in d["original_copy_candidates"] if x["queue_id"]=="KYOTO_1827_188987L")["source_issued_item_identifier"]="B||VIb||9-1 188987"
        with self.assertRaises(ValueError):self.trial(d)
    def test_hokkaido_not_silent_source_relabel(self):
        d=copy.deepcopy(self.data)
        next(x for x in d["original_copy_candidates"] if x["queue_id"]=="HOKKAIDO_1827_0181427762")["source_catalog_url"]="https://ci.nii.ac.jp/ncid/BB18578034"
        with self.assertRaises(ValueError):self.trial(d)
    def test_stitched_item_copy_policy_is_not_permission(self):
        d=copy.deepcopy(self.data);d["original_copy_candidates"][3]["item_specific_copy_permission_obtained"]=True
        with self.assertRaises(ValueError):self.trial(d)
    def test_digital_plan_does_not_prove_original(self):
        d=copy.deepcopy(self.data)
        next(x for x in d["original_copy_candidates"] if x["queue_id"]=="NAJ_3080212")["date_class"]="CATALOGUED_1827_IMPRESSION_UNVERIFIED"
        with self.assertRaises(ValueError):self.trial(d)
    def test_typographic_10x23_setting_kept_separate(self):
        d=copy.deepcopy(self.data)
        next(x for x in d["original_copy_candidates"] if x["queue_id"]=="TSUKUBA_V20_10076865665")["date_class"]="CATALOGUED_1827_IMPRESSION_UNVERIFIED"
        with self.assertRaises(ValueError):self.trial(d)
    def test_damaged_copy_not_reintroduced(self):
        d=copy.deepcopy(self.data);d["original_copy_candidates"][0]["source_issued_item_identifier"]=d["exclusion_control"]["damaged_copy_item"]
        with self.assertRaises(ValueError):self.trial(d)
    def test_incorrect_group_count_rejected(self):
        d=copy.deepcopy(self.data);d["source_groups"][0]["candidate_count"]=3
        with self.assertRaises(ValueError):self.trial(d)
    def test_unearned_glyph_voting_rejected(self):
        d=copy.deepcopy(self.data);d["null_evidence_accounting"]["new_original_glyph_votes"]=1
        with self.assertRaises(ValueError):self.trial(d)

if __name__ == "__main__":
    unittest.main()

"""12UQ: bounded nine-page direct manuscript review and fail-closed inference."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/verify-yehuobian-old20-juan20-bounded-review-r1.py"
spec=importlib.util.spec_from_file_location("bounded12uq",SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
load=lambda p:json.loads((ROOT/p).read_text(encoding="utf-8"))
D="docs/research/MING-DATONG-YEHUOBIAN-12UQ-OLD20-JUAN20-NINE-PAGE-SCOPED-REVIEW-R1.json"
P="docs/research/MING-DATONG-YEHUOBIAN-12UP-OLD20-JUAN-SEAMS-FORWARD-CORRECTION-R1.json"
Q="docs/research/MING-DATONG-YEHUOBIAN-12QD-SHLIB-FIRSTPARTY-AND-NLC-OLD20-ATLAS-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"

class Boundary12UQ(unittest.TestCase):
    def setUp(self):
        self.d,self.p,self.q,self.s=(load(x) for x in (D,P,Q,S))
    def check(self):return m.validate(self.d,self.p,self.q,self.s)
    def test_nine_bounded_pages(self):
        a=self.check()
        self.assertEqual((a["bounded_pages"],a["verified_page_hashes"],a["new_independent_witnesses"]),("137-145",9,0))
    def test_page_hashes_cannot_disagree_with_prior(self):
        self.d["scope"]["pages"][0]["jpg_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"12UP old source page SHA"):self.check()
    def test_nine_pages_not_thousand_words_transcribed(self):
        self.d["scope"]["whole_page_text_transcribed"]=True
        with self.assertRaisesRegex(ValueError,"false complete"):self.check()
    def test_right_half_137_is_juan19(self):
        self.d["scope"]["first_leaf_half"]="PDF137_BOTH_HALVES_JUAN20"
        with self.assertRaisesRegex(ValueError,"double-leaf"):self.check()
    def test_old_volume_not_same_as_thematic_new_juan20(self):
        self.d["inference_guards"]["old_chronological_juan20_equals_1827_thematic_juan20"]=True
        with self.assertRaisesRegex(ValueError,"overclaim"):self.check()
    def test_clock_calculation_not_identified_gaizao_louke(self):
        self.d["astronomical_context"]["same_text_as_later_thematic_gaizao_louke"]="PROVEN"
        with self.assertRaisesRegex(ValueError,"not attested"):self.check()
    def test_no_ancient_glyph_vote_from_reopened_artifact(self):
        self.d["accounting"]["independent_glyph_votes_new"]=1
        with self.assertRaisesRegex(ValueError,"independent witness"):self.check()
    def test_cannot_derive_absence_from_limited_scans(self):
        self.d["inference_guards"]["target_absent_from_all_145_pages_proven"]=True
        with self.assertRaisesRegex(ValueError,"overclaim"):self.check()
    def test_state_stays_closed_and_forward(self):
        self.check()
        self.assertTrue(any(x.startswith("12UQ ") for x in self.s["historical_audit"]["current_focus"]))
        self.assertEqual(len(self.s["historical_audit"]["completed_batches"]),487)
        # Preserve 12UQ's immutable 687-count historical accounting; newer batches may add sources.
        self.assertEqual(self.d["accounting"]["root_sources"]+self.d["accounting"]["extension_sources"],687)
        self.assertGreaterEqual(self.s["historical_audit"]["external_source_registry_total_unique_count"],self.d["accounting"]["total_sources"])
        self.assertEqual(self.s["invariants"]["algorithm_reopen_count"],0)
if __name__=="__main__":unittest.main()

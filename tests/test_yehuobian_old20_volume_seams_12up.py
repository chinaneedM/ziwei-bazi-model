"""12UP: original-source page seam test and explicit correction of 12UO title misreading."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("seams12up",ROOT/"scripts/verify-yehuobian-old20-volume-seams-r1.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
load=lambda p:json.loads((ROOT/p).read_text(encoding="utf-8"))
DOC="docs/research/MING-DATONG-YEHUOBIAN-12UP-OLD20-JUAN-SEAMS-FORWARD-CORRECTION-R1.json"
PREV="docs/research/MING-DATONG-YEHUOBIAN-12UO-NLC-OLD20-TERMINAL-FOLIO-IMAGE-ANCHORS-R1.json"
QD="docs/research/MING-DATONG-YEHUOBIAN-12QD-SHLIB-FIRSTPARTY-AND-NLC-OLD20-ATLAS-R1.json"

class Old20Seam12UP(unittest.TestCase):
    def setUp(self):
        self.d,self.p,self.q=(load(x) for x in (DOC,PREV,QD))
    def check(self):
        return m.validate(self.d,self.p,self.q)
    def test_live_seams_and_forward_correction(self):
        result=self.check()
        self.assertEqual(result["scan_seams"],[81,137])
        self.assertEqual(result["corrections"],1)
        self.assertEqual(result["ancient_new_witnesses"],0)
        self.assertEqual(result["chart_algorithm_reopens"],0)
    def test_misread_page1_cannot_be_reintroduced(self):
        self.d["anchors"][0]["visible_title"]="萬曆野獲編卷十八"
        with self.assertRaisesRegex(ValueError,"title misread"):self.check()
    def test_juan19_uncertain_juan_character_not_formalized(self):
        self.d["anchors"][1]["reading_scope"]="FULLY_CONFIRMED_ALL_GLYPHS"
        with self.assertRaisesRegex(ValueError,"uncertain explicit"):self.check()
    def test_no_old20_new30_juan20_collapse(self):
        self.d["chronology_scope"]["old_chronological_juan20_identical_to_1827_thematic_juan20"]=True
        with self.assertRaisesRegex(ValueError,"unproven target"):self.check()
    def test_no_absence_claim_based_on_partial_review(self):
        self.d["chronology_scope"]["gaizao_louke_absent_from_old20_proven"]=True
        with self.assertRaisesRegex(ValueError,"unproven target"):self.check()
    def test_no_unverified_printing_state(self):
        self.d["chronology_scope"]["first_1827_unchanged_print_impression_verified"]=True
        with self.assertRaisesRegex(ValueError,"unproven target"):self.check()
    def test_original_image_sha_and_artifact_scope_required(self):
        self.d["pages"][2]["page_jpeg_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"image-bound"):self.check()
    def test_seam_reverse_order_prohibited(self):
        self.d["seams"][1]["preceding_juan_half"]="LEFT"
        with self.assertRaisesRegex(ValueError,"page seams shifted"):self.check()
    def test_12qd_same_source_not_new_ancient_witness(self):
        self.d["accounting"]["new_independent_physical_witnesses"]=1
        with self.assertRaisesRegex(ValueError,"accounting"):self.check()
    def test_continuity_state_preserves_closed_product(self):
        self.check()
        st=load("docs/PROJECT-CURRENT-STATE-R1.json")
        self.assertTrue(any(x.startswith("12UP ") for x in st["historical_audit"]["current_focus"]))
        # New independently registered sources may grow after the 12UP snapshot.
        self.assertEqual(self.d["accounting"]["total_sources"],687)
        self.assertEqual(self.d["accounting"]["source_root"]+self.d["accounting"]["source_extensions"],687)
        self.assertGreaterEqual(st["historical_audit"]["external_source_registry_total_unique_count"],self.d["accounting"]["total_sources"])
        self.assertEqual(len(st["historical_audit"]["completed_batches"]),487)
        self.assertEqual(st["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(st["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")

if __name__=="__main__":
    unittest.main()

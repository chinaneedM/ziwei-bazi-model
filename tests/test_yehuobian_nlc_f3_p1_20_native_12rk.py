"""12RK fail closed on lineage, page hashes, nonnegative evidence scope."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rk",ROOT/"scripts/verify_yehuobian_nlc_f3_p1_20_native_12rk.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestFascicle3Native12RK(unittest.TestCase):
    def mutate(self, change):
        data=copy.deepcopy(GATE.read(GATE.RECORD))
        change(data)
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/"mutated.json"
            f.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=f)

    def test_real_f3_first20_source_ledger(self):
        r=GATE.verify()
        self.assertEqual(r["native_page_screened_in_f3"],20)
        self.assertEqual(r["fascicle3_native_screen_pending"],101)
        self.assertEqual(r["whole_source_native_screened"],238)
        self.assertEqual(r["whole_source_preview_only_pending"],790)
        self.assertEqual(r["whole_body_full_text_collation_pending"],1027)
        self.assertEqual(r["positive_target_glyph_or_wholetext_absence_proofs"],0)
    def test_changed_source_jpeg_hash(self):
        self.mutate(lambda x:x["review"]["original_jpeg_sha256_in_page_order"].__setitem__(5,"0"*64))
    def test_wrong_f3_archive(self):
        self.mutate(lambda x:x["source"].__setitem__("artifact_id",11673909003))
    def test_wrong_original_volume_witness(self):
        self.mutate(lambda x:x["source"].__setitem__("catalogued_original_juan_candidates",[6]))
    def test_falsely_claim_new_volume_boundary(self):
        self.mutate(lambda x:x["review"].__setitem__("exact_juan_6_to_7_change_boundary_directly_located_in_window",True))
    def test_falsely_claim_full_text(self):
        self.mutate(lambda x:x["review"].__setitem__("complete_text_collation_performed",True))
    def test_falsely_claim_page_absence(self):
        self.mutate(lambda x:x["review"].__setitem__("any_page_target_absence_proven",True))
    def test_fake_new_fascicle_witness(self):
        self.mutate(lambda x:x["queue"].__setitem__("new_independent_physical_holding_count",1))
    def test_falsely_eliminate_review_queue(self):
        self.mutate(lambda x:x["queue"].__setitem__("fascicle3_remaining_native_target_screens",0))
    def test_pdf_binary_unverified(self):
        self.mutate(lambda x:x["source"].__setitem__("source_pdf_binary_rehashed_in_12rk",True))
if __name__=="__main__":
    unittest.main()

"""12RJ: fail closed on altered native source hashes, counts, absent glyph and lineage claims."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rj", ROOT/"scripts/verify_yehuobian_nlc_f2_p61_72_native_12rj.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestNlcOld20Fascicle2CompleteNative12RJ(unittest.TestCase):
    def test_complete_native_bounded_f2_scope(self):
        r=GATE.verify()
        self.assertEqual(r["native_fascicle2_pages"], 72)
        self.assertEqual(r["fascicle2_remaining_native_target_screens"], 0)
        self.assertEqual(r["all_native_source_bounded_screens"], 218)
        self.assertEqual(r["preview_only_remaining"], 810)
        self.assertEqual(r["whole_body_full_text_collation_remaining"], 1027)
        self.assertEqual(r["target_glyph_absence_or_algorithm_changes"], 0)

    def mutate(self, action):
        rec=copy.deepcopy(GATE.read(GATE.RECORD))
        action(rec)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"altered.json"
            path.write_text(json.dumps(rec, ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=path)

    def test_last_page_hash_altered(self):
        self.mutate(lambda r:r["review"]["source_image_sha256_in_pdf_order"].__setitem__(-1,"0"*64))
    def test_window_chain_altered(self):
        self.mutate(lambda r:r["review"].__setitem__("ordered_source_image_hash_chain_sha256","0"*64))
    def test_whole_fascicle_chain_altered(self):
        self.mutate(lambda r:r["review"].__setitem__("fascicle2_p1_72_ordered_source_hash_chain_sha256","0"*64))
    def test_source_fascicle_cannot_change(self):
        self.mutate(lambda r:r["source"].__setitem__("digital_fascicle",3))
    def test_source_pdf_rehash_cannot_be_claimed(self):
        self.mutate(lambda r:r["source"].__setitem__("source_pdf_binary_rehashed_in_12rj",True))
    def test_no_false_full_text_transcription(self):
        self.mutate(lambda r:r["review"].__setitem__("full_text_transcription_performed",True))
    def test_no_fascicle_text_absence_promotion(self):
        self.mutate(lambda r:r["review"].__setitem__("fascicle2_target_absence_proven",True))
    def test_no_independent_copy_inflation(self):
        self.mutate(lambda r:r["queue"].__setitem__("new_independent_physical_witnesses",1))
    def test_no_work_negative_promotion(self):
        self.mutate(lambda r:r["review"].__setitem__("whole_manuscript_target_absence_proven",True))
    def test_full_text_backlog_cannot_disappear(self):
        self.mutate(lambda r:r["queue"].__setitem__("whole_body_full_text_collation_pending",0))
    def test_p72_text_bearing_not_blank(self):
        self.mutate(lambda r:r["review"].__setitem__("page_72_contains_text_not_blank",False))
    def test_1827_30juan_edition_cannot_merge(self):
        self.mutate(lambda r:r["review"].__setitem__("old20_and_1827_30juan_equated",True))

if __name__=="__main__":
    unittest.main()

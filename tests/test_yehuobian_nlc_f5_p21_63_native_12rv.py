"""12RV F5 source original p21-63 hash identity, dedup, no-negative proof."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rv",ROOT/"scripts/verify_yehuobian_nlc_f5_p21_63_native_12rv.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
class TestFifthFascicleOriginalScreens12RV(unittest.TestCase):
    def fake(self,change):
        x=copy.deepcopy(GATE.read(GATE.RECORD))
        change(x)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"test.json"
            p.write_text(json.dumps(x,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12RV_"):
                GATE.verify(record_path=p)
    def test_real_source_window(self):
        r=GATE.verify()
        self.assertEqual(r["fascicle5_native_bounded_visual_coverage"],"63/63")
        self.assertEqual(r["newly_screened_window"],43)
        self.assertEqual(r["prior_direct_page_overlaps"],[1,31,63])
        self.assertFalse(r["global_unique_native_source_count_reconciled"])
        self.assertEqual(r["fulltext_body_pages_still_pending"],1027)
    def test_source_pin_mutation(self):
        self.fake(lambda d:d["review"]["original_jpeg_sha256_in_source_page_order"].__setitem__(10,"0"*64))
    def test_63_page_hash_chain_mutation(self):
        self.fake(lambda d:d["review"].__setitem__("fascicle5_full63_sha256_chain","0"*64))
    def test_old_prior_page_overlap_must_remain(self):
        self.fake(lambda d:d["identity_dedup"].__setitem__("this_batch_overlap_with_12qm",[]))
    def test_no_falsified_new_original_juan11(self):
        self.fake(lambda d:d["review"].__setitem__("new_original_juan11_heading_directly_attested",True))
    def test_no_falsified_target_absence(self):
        self.fake(lambda d:d["review"].__setitem__("entire_old20_work_target_absence_proven",True))
    def test_no_falsified_fulltext(self):
        self.fake(lambda d:d["review"].__setitem__("fulltext_linewise_text_collation_performed",True))
    def test_no_1827_volume_equivalence(self):
        self.fake(lambda d:d["review"].__setitem__("later_1827_thirty_juan_equivalent_original_juan_proven",True))
    def test_no_global_count_inflation(self):
        self.fake(lambda d:d["queue"].__setitem__("new_whole_holding_global_native_reconciled_pages",400))
    def test_parent_and_stage_distinct(self):
        self.fake(lambda d:d.__setitem__("parent_open_batch","12QE_OPEN"))
    def test_archive_hash_identity(self):
        self.fake(lambda d:d["source"].__setitem__("archive_zip_sha256","0"*64))
if __name__=="__main__":
    unittest.main()

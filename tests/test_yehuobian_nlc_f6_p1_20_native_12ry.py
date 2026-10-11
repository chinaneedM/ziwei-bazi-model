"""12RY native source ZIP hash-ledger and source-grade no-overclaim tests."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("ry",ROOT/"scripts/verify_yehuobian_nlc_f6_p1_20_native_12ry.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class Test12RY(unittest.TestCase):
    def mutation(self,fn):
        d=copy.deepcopy(M.read(M.RECORD));fn(d)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"bad.json";p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12RY_"):M.verify(record_path=p)
    def test_actual_record(self):
        x=M.verify()
        self.assertEqual(x["new_f6_original_source_visual_pages"],20)
        self.assertEqual(x["full_source_native"],478)
        self.assertEqual(x["full_source_preview"],550)
        self.assertEqual(x["full_source_prelims"],2)
    def test_bad_parent(self):self.mutation(lambda x:x.__setitem__("parent_open_batch","12QE_OPEN"))
    def test_archive_zip_pin(self):self.mutation(lambda x:x["source"].__setitem__("archive_zip_sha256","0"*64))
    def test_single_page_pin(self):self.mutation(lambda x:x["review"]["individual_page_sha256_in_order"].__setitem__(11,"0"*64))
    def test_heading_scope(self):self.mutation(lambda x:x["review"].__setitem__("p1_heading_original_glyph","萬曆野獲編卷二十"))
    def test_no_false_absence(self):self.mutation(lambda x:x["review"].__setitem__("any_page_or_whole_work_target_absence_proven",True))
    def test_not_fulltext(self):self.mutation(lambda x:x["review"].__setitem__("fulltext_transcribed",True))
    def test_preview_remaining(self):self.mutation(lambda x:x["dedup"].__setitem__("f6_remaining_preview_only_pages",95))
    def test_one_physical_holding(self):self.mutation(lambda x:x["dedup"].__setitem__("one_physical_holding_increment",1))
    def test_no_1827_assumed_equivalent(self):self.mutation(lambda x:x["review"].__setitem__("original_juan_equivalence_to_1827_thematic_volume_proven",True))
    def test_no_algorithm_reopen(self):self.mutation(lambda x:x["invariants"].__setitem__("algorithm_reopens",1))
if __name__=="__main__":unittest.main()

"""12SC F7 original page SHA and provenance-grade mutation regressions."""
import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("sc",ROOT/"scripts/verify_yehuobian_nlc_f7_p21_60_native_12sc.py")
SC=importlib.util.module_from_spec(S);S.loader.exec_module(SC)
class Test12SC(unittest.TestCase):
    def mutate(self, change):
        d=copy.deepcopy(SC.read(SC.RECORD));change(d)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"record.json";p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12SC_"): SC.verify(path=p)
    def test_valid(self):
        x=SC.verify()
        self.assertEqual((x["native_graded_pages"],x["preview_only_pages"]),(614,414))
    def test_first_page_corruption(self):
        self.mutate(lambda d:d["review"]["page_sha256_in_order"].__setitem__(0,"0"*64))
    def test_last_page_corruption(self):
        self.mutate(lambda d:d["review"]["page_sha256_in_order"].__setitem__(39,"0"*64))
    def test_window_overlap(self):
        self.mutate(lambda d:d["review"]["montage_page_windows"].__setitem__(5,[40,43]))
    def test_pdf_rehash_overclaim(self):
        self.mutate(lambda d:d["source"].__setitem__("source_pdf_binary_rehashed_this_batch",True))
    def test_absence_overclaim(self):
        self.mutate(lambda d:d["review"].__setitem__("entire_f7_target_absence_proven",True))
    def test_fulltext_overclaim(self):
        self.mutate(lambda d:d["review"].__setitem__("fulltext_line_by_line_collated",True))
    def test_independent_witness_overclaim(self):
        self.mutate(lambda d:d["grade_union"].__setitem__("independent_witness_increment",1))
    def test_native_count_drift(self):
        self.mutate(lambda d:d["grade_union"].__setitem__("whole_holding_native_source_pages_after",615))
if __name__=="__main__": unittest.main()

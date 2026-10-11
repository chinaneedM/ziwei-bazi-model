"""12RZ source JPEG windows, cross-batch source identity and no-negative evidence gates."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("rz",ROOT/"scripts/verify_yehuobian_nlc_f6_p21_40_native_12rz.py")
G=importlib.util.module_from_spec(S);S.loader.exec_module(G)
class Test12RZ(unittest.TestCase):
    def mutate(self,change):
        x=copy.deepcopy(G.read(G.RECORD));change(x)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"change.json";p.write_text(json.dumps(x,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12RZ_"):G.verify(record_path=p)
    def test_source_p21_40(self):
        result=G.verify()
        self.assertEqual(result["f6_native_source_pages"],40)
        self.assertEqual(result["whole_source_native"],498)
        self.assertEqual(result["whole_source_preview"],530)
        self.assertEqual(result["remaining_f6_preview_pages"],76)
    def test_source_window_sha_mutation(self):self.mutate(lambda d:d["review"]["source_jpeg_sha256_in_page_order"].__setitem__(7,"0"*64))
    def test_prior_chain_must_match(self):self.mutate(lambda d:d["review"].__setitem__("previous_p1_20_ordered_jpeg_chain","0"*64))
    def test_no_date_claim_in_source(self):self.mutate(lambda d:d["source"].__setitem__("source_pdf_sha256","0"*64))
    def test_prior_parent_stage_distinct(self):self.mutate(lambda d:d.__setitem__("parent_open_batch","12QE_OPEN"))
    def test_not_fulltext(self):self.mutate(lambda d:d["review"].__setitem__("full_text_linewise_collation_performed",True))
    def test_not_target_absent(self):self.mutate(lambda d:d["review"].__setitem__("negative_whole_fascicle_or_work_absence_proven",True))
    def test_original_juan_not_equated(self):self.mutate(lambda d:d["review"].__setitem__("original_juan_equivalent_to_1827_thematic_juan_proven",True))
    def test_no_global_count_inflation(self):self.mutate(lambda d:d["dedup"].__setitem__("new_whole_source_native",499))
    def test_no_lineage_edge(self):self.mutate(lambda d:d["transmission_impact"]["edges_supported"].append("UNPROVEN"))
if __name__=="__main__":unittest.main()

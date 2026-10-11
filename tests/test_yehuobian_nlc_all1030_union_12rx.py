"""12RX 1030-page cross-batch grade/identity and evidence-scope regression tests."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("rx",ROOT/"scripts/verify_yehuobian_nlc_all1030_union_12rx.py")
G=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(G)
class Test12RX(unittest.TestCase):
    def mutate(self, fn):
        d=copy.deepcopy(G.read(G.RECORD)); fn(d)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"mutation.json";p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"12RX_"):
                G.verify(record_path=p)
    def test_real_whole1030_source_grade_union(self):
        z=G.verify()
        self.assertEqual(z["source_pages"],1030)
        self.assertEqual(z["bounded_native_source_pages"],458)
        self.assertEqual(z["bounded_native_body_pages"],457)
        self.assertEqual(z["preview_only_body_pages"],570)
        self.assertEqual(z["unreviewed_prelim_pages"],2)
        self.assertEqual(z["full_text_collation_body_backlog"],1027)
    def test_f10_p136_context_not_promoted(self):
        self.mutate(lambda d:d["fascicles"][9]["native_target_bounded_ranges"].insert(0,[136,136]))
    def test_f7_preview_not_promoted(self):
        self.mutate(lambda d:d["fascicles"][6].__setitem__("preview_only_ranges",[[22,110]]))
    def test_f1_preliminary_not_body_native(self):
        self.mutate(lambda d:d["fascicles"][0].__setitem__("non_target_prelim_ranges",[]))
    def test_f10_p145_colophon_not_body(self):
        self.mutate(lambda d:d["accounting"].__setitem__("body_pages_with_prior_bounded_native_target_screen",458))
    def test_no_global_target_absence_proof(self):
        self.mutate(lambda d:d["scoped_original_page_controls"].__setitem__("no_direct_old20_gaizao_louke_target_attested",False))
    def test_same_name_juan_not_identity(self):
        self.mutate(lambda d:d["scoped_original_page_controls"].__setitem__("original20_chronicle_juan_not_equivalent_to_1827_thematic30_juan",False))
    def test_f7_SHA_chain_immutable(self):
        self.mutate(lambda d:d["scoped_original_page_controls"].__setitem__("f7_native_20_ordered_sha_chain","0"*64))
    def test_10th_fascicle_colophon_sha(self):
        self.mutate(lambda d:d["scoped_original_page_controls"].__setitem__("f10_p145_colophon_jpeg_sha256","0"*64))
    def test_not_new_witness(self):
        self.mutate(lambda d:d["transmission_impact"]["edges_supported"].append("UNPROVEN_LINEAGE"))
    def test_no_unverified_algorithm_activation(self):
        self.mutate(lambda d:d["invariants"].__setitem__("algorithm_reopens",1))
if __name__=="__main__":unittest.main()

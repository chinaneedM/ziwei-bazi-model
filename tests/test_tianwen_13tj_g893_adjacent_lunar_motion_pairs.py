import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/TIANWEN-13TJ-G893-THREE-ADJACENT-PAIRED-LUNAR-MOTION-COLLATION-R1.json"

def fmt(value, rule):
    n = value * 10000
    return -(-n.numerator // n.denominator) if rule == "CEIL" else n.numerator // n.denominator

class G893AdjacentOriginalSymmetry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(DOC.read_text(encoding="utf-8"))
        cls.rows = {r["limit"]: r for r in cls.doc["original_source_scoped_rows"]}
        cls.ming = json.loads((ROOT / cls.doc["cross_source_controls"]["ming_original_doc"]).read_text(encoding="utf-8"))

    def test_source_original_page_hashes_and_six_nonoverlapping_roi_bindings(self):
        d = self.doc
        page_sha = {r["page"]: r["sha256"] for r in d["original_source"]["original_jpeg_pages"]}
        self.assertEqual(set(page_sha), {"023a", "023b", "036b"})
        self.assertEqual(len(set((r["page"], tuple(r["rect"])) for r in self.rows.values())), 6)
        for limit,r in self.rows.items():
            self.assertEqual(r["jpeg_sha256"], page_sha[r["page"]])
            self.assertEqual(len(r["rgb"]), 64)
            self.assertEqual(len(r["crop_sha"]), 64)
            self.assertEqual(r["original_q_literal"], r["sign"]+r["q"])
            self.assertEqual(r["source_literal_scope"], "DIRECT_ORIGINAL_VISIBLE_LINE_LIMIT_Q_AND_CHI_JI_FOUR_PLACE_GLYPHS")
            self.assertEqual((r["limit"] in (34,35,36)), r["sign"] == "益")

    def test_three_paired_source_rows_and_exact_l35_l132_exception(self):
        r = self.rows
        for p in self.doc["paired_symmetry_review"]:
            a,b = [r[n] for n in p["limits"]]
            self.assertEqual(F(a["q_degree"]),F(b["q_degree"]))
            self.assertEqual(a["sign"],"益")
            self.assertEqual(b["sign"],"損")
            source_min=[a["chi"],b["ji"]]
            source_max=[a["ji"],b["chi"]]
            self.assertEqual(source_min,p["speed_min"])
            self.assertEqual(source_max,p["speed_max"])
            self.assertEqual(source_min[0],source_min[1])
            self.assertEqual(source_max[0]==source_max[1],p["symmetric_both_columns"])
        self.assertEqual(F(r[132]["chi"])-F(r[35]["ji"]),F("0.0001"))
        self.assertEqual(self.doc["source_internal_result"]["matched_symmetric_pair_count"],2)

    def test_ming_scoped_primary_rows_and_three_exact_candidates(self):
        old = {r["limit"]:r for r in self.ming["rows"]}
        for row in self.doc["cross_source_controls"]["ming_print_six_rows"]:
            source=old[row["limit"]]
            self.assertEqual(source["chi_xingdu_degree"], row["chi"])
            self.assertEqual(source["ji_xingdu_degree"], row["ji"])
        for model in self.doc["cross_source_controls"]["three_previously_scoped_models"]:
            mean=F(model["mean_fraction"])
            misses=[]
            for row in self.rows.values():
                q=F(row["q_degree"])
                chi=fmt(mean-q if row["sign"]=="益" else mean+q,model["quantizer"])
                ji=fmt(mean+q if row["sign"]=="益" else mean-q,model["quantizer"])
                for lane,print_val in (("chi",row["chi"]),("ji",row["ji"])):
                    orig=int(F(print_val)*10000)
                    pred=chi if lane=="chi" else ji
                    if pred!=orig:
                        misses.append({"limit":row["limit"],"lane":lane,"predicted_1e4":pred,"original_g893_1e4":orig})
            self.assertEqual(12-len(misses),model["matches_out_of_12"])
            self.assertEqual(misses,[model["only_mismatch"]])

    def test_open_issue_source_and_product_firewall(self):
        a=self.doc["adjudication"]
        self.assertEqual(a["additional_physical_witnesses"],0)
        self.assertEqual(a["source_registry_additions"],0)
        self.assertEqual(a["genealogy_edges_additions"],0)
        self.assertEqual(a["g893_cross_witness_final_adjudications"],"0/6")
        self.assertEqual(a["g893_named_control_fields"],"5/6")
        self.assertEqual(a["algorithm_reopens"],0)
        self.assertEqual(a["chart_product"],"CLOSED")
        self.assertTrue(a["hypotheses_open"])

if __name__ == "__main__":
    unittest.main()

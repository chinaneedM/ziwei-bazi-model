import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/research/TIANWEN-13TI-G893-DIRECT-L35-L132-ASYMMETRIC-LUNAR-SPEED-PRINT-R1.json"

def render_1e4(x, quantizer):
    v = x * 10000
    if quantizer == "CEIL":
        return -(-v.numerator // v.denominator)
    if quantizer == "TRUNCATE":
        return v.numerator // v.denominator
    raise ValueError(quantizer)

class OriginalTwoFolioSourceScopedGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.previous = json.loads((ROOT / cls.d["references"]["prior_discriminator"]).read_text(encoding="utf-8"))
        cls.g893 = json.loads((ROOT / cls.d["references"]["g893_original_loss_gain"]).read_text(encoding="utf-8"))
        cls.ming = json.loads((ROOT / cls.d["references"]["ming1569_source_table"]).read_text(encoding="utf-8"))

    def test_source_sha_and_literal_bindings_without_artifact_image_claim(self):
        archived = {x["page_id"]: x["jpeg_sha256"] for x in self.g893["original_page_evidence"]}
        qrows = {x["limit"]:x for x in self.g893["direct_original_collation"]["rows"]}
        obs=self.d["direct_source_reads"]
        self.assertEqual([(x["limit"],x["field"],x["original_printed_literal"]) for x in obs],
                         [(35,"疾行度","一度一七五一"),(132,"遲行度","一度一七五二")])
        for x in obs:
            self.assertEqual(x["original_jpeg_sha256"], archived[x["page_id"]])
            self.assertEqual(x["source_q_literal"],qrows[x["limit"]]["complete_field"])
            self.assertEqual(x["page_id"],qrows[x["limit"]]["page_id"])
            self.assertEqual(len(x["roi_rgb_sha256"]),64)
            self.assertEqual(len(x["roi_jpeg_sha256"]),64)
            self.assertEqual(F(x["normalized_degree"])*10000,int(F(x["normalized_degree"])*10000))
        self.assertEqual([int(F(x["normalized_degree"])*10000) for x in obs],[11751,11752])
        self.assertTrue(self.d["discrepancy"]["equal_abs_original_q"])
        self.assertEqual(self.d["discrepancy"]["original_pair_difference_1e4"],1)

    def test_exact_fraction_candidate_predictions_and_ming_comparator(self):
        original=[11751,11752]
        for model in self.d["conditional_comparison"]["models"]:
            old=next(x for x in self.previous["exact_full_primary_replay"]["models"] if x["name"]==model["name"])
            self.assertEqual(model["mean_fraction"],old["mean_fraction"])
            predicted=render_1e4(F(model["mean_fraction"])+F("0.07886075"),old["quantizer"])
            self.assertEqual(model["predicted_pair_1e4"],[predicted,predicted])
            self.assertEqual(sum(x==y for x,y in zip(original,model["predicted_pair_1e4"])),1)
        rows={r["limit"]:r for r in self.ming["rows"]}
        self.assertEqual(rows[35]["ji_xingdu_degree"],"1.1751")
        self.assertEqual(rows[132]["chi_xingdu_degree"],"1.1751")

    def test_uncertainty_and_closure_guard(self):
        a=self.d["accounting"]
        self.assertEqual(a["new_direct_source_speed_fields"],2)
        self.assertEqual(a["additional_physical_witnesses"],0)
        self.assertEqual(a["source_registry_delta"],0)
        self.assertEqual(a["cross_witness_historical_final_decisions"],"0/6")
        self.assertEqual(a["original_six_named_control_complete_fields"],"5/6")
        self.assertEqual(a["algorithm_reopens"],0)
        self.assertEqual(a["chart_product"],"CLOSED")
        self.assertEqual(self.d["discrepancy"]["source_native_mechanism_for_unequal_pair"],"UNRESOLVED")

if __name__ == "__main__":
    unittest.main()

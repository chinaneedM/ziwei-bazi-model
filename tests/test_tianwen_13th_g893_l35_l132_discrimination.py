import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/research/TIANWEN-13TH-G893-L35-L132-DISCRIMINATING-MING1569-AND-TIANGEN-CONTROL-R1.json"

def display(value, rule):
    x = value * 10000
    if rule == "CEIL":
        return -(-x.numerator // x.denominator)
    if rule == "TRUNCATE":
        return x.numerator // x.denominator
    raise AssertionError(rule)

class SourceScopedDiscriminator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(REPORT.read_text(encoding="utf8"))
        cls.ming = json.loads((ROOT / cls.doc["historical_sources"]["ming_original"]["normalized_primary_table"]).read_text(encoding="utf8"))
        cls.g893 = json.loads((ROOT / cls.doc["historical_sources"]["g893_original_same_copy"]["source_12yc"]).read_text(encoding="utf8"))

    def test_336_printed_cells_vs_three_exact_candidate_models(self):
        valid = [r for r in self.ming["rows"] if r["loss_gain_degree"] is not None and r["chi_xingdu_degree"] is not None and r["ji_xingdu_degree"] is not None]
        self.assertEqual(len(valid), 168)
        observed = {}
        for model in self.doc["exact_full_primary_replay"]["models"]:
            mean = F(model["mean_fraction"])
            mismatches = []
            matched = 0
            for row in valid:
                q = F(row["loss_gain_degree"])
                chi = display(mean - q if row["loss_gain_sign"] == "益" else mean + q, model["quantizer"])
                ji = display(mean + q if row["loss_gain_sign"] == "益" else mean - q, model["quantizer"])
                for lane, candidate in (("chi", chi), ("ji", ji)):
                    original = int(F(row[lane + "_xingdu_degree"]) * 10000)
                    if candidate == original:
                        matched += 1
                    else:
                        mismatches.append({"limit": row["limit"], "lane": lane,
                                           "predicted_1e4": candidate,
                                           "original_1569_1e4": original})
            self.assertEqual(matched, model["matches"])
            self.assertEqual(mismatches,
                             sorted(model["central_exceptions"] + model["other_disagreements"],
                                    key=lambda x: (x["limit"], 0 if x["lane"] == "chi" else 1)))
            self.assertEqual(model["matches_out_of"], 336)
            observed[model["name"]] = matched
        self.assertEqual(observed, {"NOMINAL_820_CEIL":334,
                                    "HALF_TURN_168_TRUNCATE":326,
                                    "TIANGEN_109633975_TRUNCATE_CONDITIONAL":332})

    def test_original_source_bound_L35_L132_distinguishes_models(self):
        source_rows = {r["limit"]: r for r in self.g893["direct_original_collation"]["rows"]}
        names = [m["name"] for m in self.doc["exact_full_primary_replay"]["models"]]
        for target in self.doc["paired_original_discriminators"]:
            n = target["limit"]
            self.assertIn(n, [35, 132])
            self.assertEqual(source_rows[n]["complete_field"], target["original_g893_q_glyphs"])
            self.assertEqual(source_rows[n]["page_id"], target["copy_original_page"])
            self.assertEqual(target["g893_differentiating_lane_direct_original_read"], "NOT_YET_COLLATED")
            self.assertEqual(target["original_ming1569_lanes"][target["differentiating_lane"]], "1.1751")
            for model in self.doc["exact_full_primary_replay"]["models"]:
                prediction = display(F(model["mean_fraction"]) + F("0.07886075"), model["quantizer"])
                self.assertEqual(target["model_predictions_1e4"][model["name"]], prediction)
            self.assertEqual(target["model_predictions_1e4"][names[0]], 11751)
            self.assertEqual(target["model_predictions_1e4"][names[1]], 11752)
            self.assertEqual(target["model_predictions_1e4"][names[2]], 11752)

    def test_historical_source_scope_firewall(self):
        d = self.doc
        self.assertEqual(d["adjudication"]["original_six_historical_final_controls"], "0/6")
        self.assertEqual(d["adjudication"]["new_direct_source_page_collations"], 0)
        self.assertEqual(d["adjudication"]["new_physical_witnesses"], 0)
        self.assertEqual(d["adjudication"]["algorithm_reopens"], 0)
        self.assertEqual(d["adjudication"]["chart_product"], "CLOSED")
        self.assertIn("NOT", d["historical_sources"]["mei_received"]["printed_claim_not_established"].upper())

if __name__ == "__main__":
    unittest.main()

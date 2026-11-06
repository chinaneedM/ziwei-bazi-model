import json
import unittest
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CURRENT=ROOT/"docs/research/TIANWEN-13SJ-ZHOU1569-P14-D1-SHORT-GLYPH-AND-RESEARCH-TRANSCRIPTION-ERRATUM-R1.json"
OLD_ZHOU=ROOT/"docs/research/TIANWEN-13MY-ZHOU1569-D0-D18-BOUNDED-SHORT-LANE-R1.json"
OLD_G893=ROOT/"docs/research/TIANWEN-13NA-G893-001A-D0-D2-ORIGINAL-SHORT-LANE-R1.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

class Zhou13SJ(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e,cls.prior,cls.g=load(CURRENT),load(OLD_ZHOU),load(OLD_G893)

    def test_old_source_preserved_and_corrected_forward_only(self):
        e=self.e
        self.assertEqual([self.prior["rows"][i]["short_normalized"] for i in range(3)],["4.9386","4.9572","4.9758"])
        self.assertEqual(e["prior_research_correction"]["prior_13my_reported_zhou_d1"],"4.9572")
        self.assertEqual(e["original_native_roi_attestations"]["day1_short"]["observed_literal"],"九五二七")
        self.assertEqual(e["original_native_roi_attestations"]["day1_short"]["normalized_source_local"],"4.9527")
        self.assertTrue(e["prior_research_correction"]["previous_files_preserved"])

    def test_independent_g893_original_not_silently_changed(self):
        e=self.e
        self.assertEqual([x["normalized"] for x in self.g["native_glyph_reviews"]],["4.9386","4.9572","4.9758"])
        self.assertEqual(self.g["original_source"]["jpeg_sha256"],e["independent_same_topic_original_comparator"]["source_original_jpeg_sha256"])
        self.assertEqual(self.g["original_source"]["rgb_sha256"],e["independent_same_topic_original_comparator"]["source_original_rgb_sha256"])
        self.assertEqual(e["independent_same_topic_original_comparator"]["d1_original_literal"],"四分九五七二")

    def test_integer_local_counterexample(self):
        q=self.e["exact_integer_replay"]
        self.assertEqual(q["zhou_original_S4"],[49386,49527,49758])
        self.assertEqual([b-a for a,b in zip(q["zhou_original_S4"],q["zhou_original_S4"][1:])],q["zhou_adjacent_increments_S4"])
        self.assertEqual(q["zhou_adjacent_increments_S4"],[141,231])
        self.assertEqual([b-a for a,b in zip(q["g893_original_S4"],q["g893_original_S4"][1:])],q["g893_adjacent_increments_S4"])
        self.assertEqual(q["g893_adjacent_increments_S4"],[186,186])
        self.assertEqual(q["zhou_original_S4"][1]-q["g893_original_S4"][1],-45)

    def test_image_and_decision_boundaries(self):
        e=self.e
        self.assertEqual(e["source"]["pdf_sha256"],self.prior["source"]["prior_capture_sha256"])
        self.assertEqual(e["source"]["rendered_pdf_page_one_based"],14)
        self.assertEqual(e["source"]["render_size"],[2526,1786])
        for v in e["original_native_roi_attestations"].values():
            self.assertEqual(len(v["rgb_sha256"]),64)
            self.assertEqual(len(v["bbox_ltrb"]),4)
        self.assertEqual(e["adjudication"]["six_historic_G893_finals"],"0/6")
        self.assertEqual(e["adjudication"]["product"],"CLOSED")
        for k in ("physical_originals_newly_acquired","source_registry_delta","genealogy_nodes_added","genealogy_edges_added","matrix_rows_changed","algorithm_reopens","candidate_collapses","risk_issues_closed"):
            self.assertEqual(e["adjudication"][k],0)
        self.assertEqual(e["transmission_impact"]["edges_supported"],[])
        self.assertTrue(e["prior_research_correction"]["old_reading_must_not_be_silently_edited"])

if __name__=="__main__":
    unittest.main()

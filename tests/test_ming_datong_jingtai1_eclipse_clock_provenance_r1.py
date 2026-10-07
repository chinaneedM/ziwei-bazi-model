import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MingDatongJingtai1EclipseClockProvenanceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads((ROOT / "docs/research/MING-DATONG-JINGTAI1-ECLIPSE-CLOCK-PROVENANCE-R1.json").read_text(encoding="utf-8"))
        cls.b = json.loads((ROOT / "docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.g = json.loads((ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.s = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_contemporaneous_operational_discrepancy_closed(self):
        a = self.r["adjudication"]
        self.assertEqual(a["contemporaneous_operational_eclipse_timing_discrepancy"], "CLOSED_SOURCE_SCOPED")
        self.assertEqual(a["qintianjian_prediction_error"], "ATTESTED")
        self.assertEqual(a["actual_time_label_baomaozheng_sanke"], "ATTESTED")
        self.assertIn("卯正三刻", self.r["primary_event_record"]["received_text"])
        self.assertIn("辰初初刻", self.r["primary_event_record"]["received_text"])

    def test_absolute_clock_phase_and_locality_remain_open(self):
        a = self.r["adjudication"]
        self.assertEqual(a["actual_time_measurement_provenance"], "UNRESOLVED")
        self.assertEqual(a["actual_time_phase_identity"], "UNRESOLVED")
        self.assertEqual(a["actual_time_capital_locality_binding"], "UNRESOLVED")
        self.assertEqual(a["actual_time_official_clepsydra_identity"], "UNRESOLVED")
        self.assertFalse(a["modern_ephemeris_meridian_fit_authorized"])

    def test_g03_and_product_remain_fail_closed(self):
        g03 = {x["gate_id"]: x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12pn_refinement"]["independent_absolute_anchor_status"], "NOT_YET_ADMISSIBLE")
        row = next(x for x in self.m["rows"] if x["rule_id"] == "HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["batch_12pn_jingtai1_eclipse_clock_provenance"]["runtime_authorized"])

    def test_transmission_and_source_bindings_exist(self):
        nodes = {x["node_id"] for x in self.g["nodes"]}
        edges = {x["edge_id"] for x in self.g["edges"]}
        for node in self.r["transmission_impact"]["graph_nodes_added"]:
            self.assertIn(node, nodes)
        for edge in self.r["transmission_impact"]["graph_edges_added"]:
            self.assertIn(edge, edges)
        sources = {x["source_id"] for x in self.s["sources"]}
        self.assertIn("EXT-CTEXT-MINGSHILU-YINGZONG-V187-JINGTAI1-ECLIPSE-CLOCK-ERROR", sources)
        self.assertIn("EXT-IHP-MINGSHILU-YINGZONG-V187-CATALOG", sources)

if __name__ == "__main__":
    unittest.main()

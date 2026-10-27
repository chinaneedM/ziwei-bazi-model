import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MingDatongEclipseRescuePhaseClockProtocolR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads((ROOT / "docs/research/MING-DATONG-ECLIPSE-RESCUE-PHASE-CLOCK-PROTOCOL-R1.json").read_text(encoding="utf-8"))
        cls.b = json.loads((ROOT / "docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.g = json.loads((ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.s = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_rescue_protocol_is_not_intrinsically_visual(self):
        p = self.r["wanli_huidian_rescue_protocol"]
        self.assertTrue(p["precomputed_timing_and_start_recovery_geometry"])
        self.assertTrue(p["bureau_officer_reports_time_during_rite"])
        self.assertTrue(p["cloudy_invisible_case_still_has_recovery_time_reporting"])
        self.assertFalse(p["protocol_requires_direct_visual_phase_detection"])

    def test_positive_control_is_explicit_but_not_back_projected(self):
        p = self.r["late_ming_positive_control"]
        self.assertTrue(p["explicit_phase_term_chukui"])
        self.assertTrue(p["explicit_observation_term_cehou"])
        self.assertTrue(p["explicit_clock_methods_named"])
        self.assertIn("POSITIVE_CONTROL_ONLY", p["firewall"])

    def test_jingtai_phase_clock_still_unresolved(self):
        a = self.r["adjudication"]
        self.assertEqual(a["jingtai1_bare_event_time_phase_identity"], "UNRESOLVED")
        self.assertEqual(a["jingtai1_actual_time_measurement_chain"], "UNRESOLVED")
        self.assertEqual(a["jingtai1_official_clepsydra_identity"], "UNRESOLVED")
        self.assertEqual(a["jingtai1_independent_absolute_anchor_status"], "NOT_YET_ADMISSIBLE")
        self.assertFalse(a["modern_ephemeris_meridian_fit_authorized"])

    def test_g03_and_product_remain_fail_closed(self):
        g03 = {x["gate_id"]: x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12po_refinement"]["jingtai1_phase_identity"], "UNRESOLVED")
        row = next(x for x in self.m["rows"] if x["rule_id"] == "HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["batch_12po_eclipse_rescue_phase_clock_protocol"]["runtime_authorized"])

    def test_graph_and_source_bindings_exist(self):
        nodes = {x["node_id"] for x in self.g["nodes"]}
        edges = {x["edge_id"] for x in self.g["edges"]}
        for node in self.r["transmission_impact"]["graph_nodes_added"]:
            self.assertIn(node, nodes)
        for edge in self.r["transmission_impact"]["graph_edges_added"]:
            self.assertIn(edge, edges)
        sources = {x["source_id"] for x in self.s["sources"]}
        self.assertIn("EXT-CTEXT-XINFA-SUANSHU-CHONGZHEN5-ECLIPSE-TIME-MEASUREMENT", sources)

if __name__ == "__main__":
    unittest.main()

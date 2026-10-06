import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MingDatongQishuoGnomonObservationBridgeR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"docs/research/MING-DATONG-QISHUO-GNOMON-OBSERVATION-BRIDGE-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.g=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.s=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_observational_calibration_is_attested(self):
        a=self.r["adjudication"]
        self.assertEqual(a["observational_verification_of_qi_shuo"],"ATTESTED")
        self.assertEqual(a["gnomon_instrument_use_for_calendar_calibration"],"ATTESTED")
        self.assertEqual(a["huaxiang_program_includes_heshuo_as_verification_target"],"ATTESTED_RECEIVED_TEXT")

    def test_direct_numeric_bridge_is_not_attested(self):
        a=self.r["adjudication"]
        self.assertEqual(a["direct_gnomon_shadow_to_dingshuo_remainder_formula"],"NOT_ATTESTED")
        self.assertEqual(a["direct_local_clock_to_dingshuo_remainder_formula"],"NOT_ATTESTED")
        self.assertEqual(a["qishuo_geographic_reference"],"UNRESOLVED")
        self.assertFalse(a["modern_ephemeris_meridian_fit_authorized"])

    def test_g03_and_product_remain_fail_closed(self):
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12pm_refinement"]["direct_gnomon_to_qishuo_numeric_bridge"],"NOT_ATTESTED")
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")
        self.assertFalse(row["batch_12pm_qishuo_gnomon_observation_bridge"]["runtime_authorized"])

    def test_graph_and_sources_are_bound(self):
        nodes={x["node_id"] for x in self.g["nodes"]}
        edges={x["edge_id"] for x in self.g["edges"]}
        for n in self.r["transmission_impact"]["graph_nodes_added"]:
            self.assertIn(n,nodes)
        for e in self.r["transmission_impact"]["graph_edges_added"]:
            self.assertIn(e,edges)
        sources={x["source_id"] for x in self.s["sources"]}
        self.assertIn("EXT-CTEXT-MINGSHI-V25-JIAJING7-GNOMON-QISHUO-YUANFA",sources)
        self.assertIn("EXT-CTEXT-MINGSHI-V31-HUAXIANG-JIAJING2-OBSERVATION-PROGRAM",sources)

if __name__=="__main__":
    unittest.main()

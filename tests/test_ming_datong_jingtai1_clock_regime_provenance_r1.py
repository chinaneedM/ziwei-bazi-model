import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Jingtai1ClockRegimeProvenanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record=json.loads((ROOT/"docs/research/MING-DATONG-JINGTAI1-CLOCK-REGIME-PROVENANCE-R1.json").read_text(encoding="utf-8"))
        cls.matrix=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.graph=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.registry=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_order_does_not_prove_completion(self):
        a=self.record["adjudication"]
        self.assertEqual(a["zhengtong12_rebuild_completed_before_1450"],"NOT_ATTESTED_IN_REVIEWED_SOURCES")
        self.assertEqual(a["zhengtong14_physical_clock_reversion"],"NOT_ATTESTED")
        self.assertEqual(a["jingtai1_corrected_clock_identity"],"UNRESOLVED")

    def test_fail_closed(self):
        a=self.record["adjudication"]
        self.assertEqual(a["jingtai1_absolute_time_anchor"],"NOT_YET_ADMISSIBLE")
        self.assertEqual(a["md_g03_status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertFalse(a["runtime_authorized"])
        self.assertEqual(a["new_independent_physical_witness_increment"],0)
        row=next(x for x in self.matrix["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")

    def test_existing_witnesses_and_new_graph(self):
        srcs={x["source_id"] for x in self.registry["sources"]}
        for item in self.record["prior_physical_controls"]: self.assertIn(item["source_id"],srcs)
        self.assertIn(self.record["received_institutional_control"]["source_id"],srcs)
        nodes={x["node_id"] for x in self.graph["nodes"]}
        edges={x["edge_id"] for x in self.graph["edges"]}
        for n in self.record["transmission_impact"]["graph_nodes_added"]: self.assertIn(n,nodes)
        for e in self.record["transmission_impact"]["graph_edges_added"]: self.assertIn(e,edges)

if __name__=="__main__":
    unittest.main()

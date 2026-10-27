import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MingDatongJingtai1EclipseSourceChainAuditR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"docs/research/MING-DATONG-JINGTAI1-ECLIPSE-SOURCE-CHAIN-AUDIT-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.g=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.s=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_derivative_chain_adds_no_missing_semantics(self):
        a=self.r["adjudication"]
        self.assertEqual(a["later_derivative_chain_adds_phase_label"],"NO")
        self.assertEqual(a["later_derivative_chain_adds_observer"],"NO")
        self.assertEqual(a["later_derivative_chain_adds_clock_instrument"],"NO")
        self.assertFalse(a["derivative_repetition_counts_as_independent_witnesses"])

    def test_negative_is_scope_limited(self):
        h=self.r["public_search_horizon"]
        self.assertFalse(h["new_target_specific_phase_source_recovered"])
        self.assertEqual(h["scope"],"PUBLIC_DIGITAL_SEARCH_HORIZON_ONLY")
        self.assertIn("!=",h["firewall"])
        self.assertFalse(self.r["adjudication"]["historical_nonexistence_claim_authorized"])

    def test_guoque_physical_route_is_next(self):
        p=self.r["next_physical_route"]
        self.assertEqual(p["target"],"卷二十九 庚午景泰元年正月")
        self.assertFalse(p["target_page_collated_in_this_batch"])
        self.assertEqual(self.r["route_disposition"]["next_batch"],"12PQ")

    def test_g03_product_remain_fail_closed(self):
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12pp_refinement"]["generic_derivative_search_route"],"PARKED_UNLESS_NEW_WITNESS")
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")
        self.assertFalse(row["batch_12pp_jingtai1_eclipse_source_chain_audit"]["runtime_authorized"])

    def test_graph_and_sources_exist(self):
        nodes={x["node_id"] for x in self.g["nodes"]}
        edges={x["edge_id"] for x in self.g["edges"]}
        for node in self.r["transmission_impact"]["graph_nodes_added"]: self.assertIn(node,nodes)
        for edge in self.r["transmission_impact"]["graph_edges_added"]: self.assertIn(edge,edges)
        sources={x["source_id"] for x in self.s["sources"]}
        for sid in ["EXT-SHIDIAN-QIANAN-NIMINGSHIGAO-V5-JINGTAI1-ECLIPSE-DERIVATIVE","EXT-SHIDIAN-WANGHONGXU-MINGSHIGAO-V7-JINGTAI1-ECLIPSE-DERIVATIVE","EXT-CTEXT-MINGHUIYAO-V27-JINGTAI1-ECLIPSE-DERIVATIVE","EXT-WIKISOURCE-XUWENXIANTONGKAO-V212-JINGTAI1-ECLIPSE-DERIVATIVE","EXT-COMMONS-ZJLIB-GUOQUE-V25-JINGTAI1-PHYSICAL-ROUTE"]: self.assertIn(sid,sources)

if __name__=="__main__":
    unittest.main()

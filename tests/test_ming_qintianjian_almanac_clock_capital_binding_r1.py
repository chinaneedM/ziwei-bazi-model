import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MingQintianjianAlmanacClockCapitalBindingR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads((ROOT / "docs/research/MING-QINTIANJIAN-ALMANAC-CLOCK-CAPITAL-BINDING-R1.json").read_text(encoding="utf-8"))
        cls.b = json.loads((ROOT / "docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.g = json.loads((ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.s = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_institutional_colocation_is_closed(self):
        a = self.r["adjudication"]
        self.assertEqual(a["qintianjian_official_clock_service"], "CLOSED_RECEIVED_INSTITUTIONAL_TEXT")
        self.assertEqual(a["qintianjian_eclipse_time_prediction_and_reporting"], "CLOSED_RECEIVED_INSTITUTIONAL_TEXT")
        self.assertEqual(a["qintianjian_datong_almanac_production_and_distribution"], "CLOSED_RECEIVED_INSTITUTIONAL_TEXT")

    def test_capital_and_clepsydra_shortcuts_are_rejected(self):
        a = self.r["adjudication"]
        self.assertEqual(a["same_bureau_clock_service_equals_qishuo_numeric_coordinate"], "NOT_ATTESTED")
        self.assertEqual(a["qiaolou_clepsydra_equals_published_qishuo_time_labels"], "NOT_ATTESTED")
        self.assertEqual(a["current_capital_automatically_defines_all_calendar_time_modules"], "REJECTED_BY_DAYLIGHT_MODULE_COUNTEREXAMPLE")
        self.assertEqual(a["qishuo_identity_with_official_clepsydra_standard"], "UNRESOLVED")

    def test_g03_and_product_remain_fail_closed(self):
        g03 = {x["gate_id"]: x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12pl_refinement"]["capital_auto_inheritance"], "REJECTED")
        self.assertEqual(g03["batch_12pl_refinement"]["qishuo_capital_clock_binding"], "UNRESOLVED")
        row = next(x for x in self.m["rows"] if x["rule_id"] == "HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["batch_12pl_qintianjian_almanac_clock_capital_binding"]["runtime_authorized"])

    def test_transmission_and_source_bindings_exist(self):
        nodes = {x["node_id"] for x in self.g["nodes"]}
        edges = {x["edge_id"] for x in self.g["edges"]}
        for node in self.r["transmission_impact"]["graph_nodes_added"]:
            self.assertIn(node, nodes)
        for edge in self.r["transmission_impact"]["graph_edges_added"]:
            self.assertIn(edge, edges)
        sources = {x["source_id"] for x in self.s["sources"]}
        self.assertIn("EXT-CTEXT-WANLI-DAMING-HUIDIAN-V223-TIMEKEEPING", sources)
        self.assertIn("EXT-CTEXT-MINGSHI-V31-YINGTIAN-SHUNTIAN-DAYNIGHT-STANDARD", sources)

if __name__ == "__main__":
    unittest.main()

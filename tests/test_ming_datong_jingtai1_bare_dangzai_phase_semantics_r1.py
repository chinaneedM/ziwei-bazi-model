import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MingDatongJingtai1BareDangzaiPhaseSemanticsR1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((ROOT / "docs/research/MING-DATONG-JINGTAI1-BARE-DANGZAI-PHASE-SEMANTICS-R1.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.graph = json.loads((ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_target_remains_phase_unbound(self):
        self.assertFalse(self.record["target"]["explicit_phase_lexeme"])
        self.assertEqual(self.record["philology"]["syntactic_role"], "TIMING_PREDICATION")
        self.assertEqual(self.record["philology"]["normalization_bridge_to_chukui"], "NOT_ATTESTED")
        self.assertEqual(self.record["adjudication"]["normalize_dangzai_time_to_chukui_time"], "FORBIDDEN")
        self.assertEqual(self.record["adjudication"]["target_phase_identity_after_batch"], "UNRESOLVED")

    def test_controls_explicitly_mark_phase(self):
        by_source = {x["source_id"]: x for x in self.record["comparative_corpus"]}
        self.assertIn("初虧", by_source["EXT-SHIDIAN-MINGSHILU-XIANZONG-V4-TIANSHUN8-ECLIPSE-CHUKUI-CONTROL"]["wording"])
        self.assertIn("寅虧卯圓", by_source["EXT-SHIDIAN-MINGSHILU-XIAOZONG-V162-HONGZHI13-ECLIPSE-QIYUAN-CONTROL"]["wording"])
        self.assertIn("食甚", by_source["EXT-SHIDIAN-MINGSHILU-SHENZONG-V477-WANLI38-ECLIPSE-PHASE-CLOCK-CONTROL"]["wording"])
        self.assertIn("復圓", by_source["EXT-SHIDIAN-MINGSHILU-SHENZONG-V477-WANLI38-ECLIPSE-PHASE-CLOCK-CONTROL"]["wording"])

    def test_fail_closed_and_no_false_inverse(self):
        a = self.record["adjudication"]
        self.assertEqual(a["infer_target_is_not_chukui"], "NOT_AUTHORIZED")
        self.assertEqual(a["jingtai1_absolute_anchor_status"], "NOT_YET_ADMISSIBLE")
        self.assertEqual(a["md_g03_status_after_batch"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertFalse(a["runtime_authorized"])
        row = next(x for x in self.matrix["rows"] if x["rule_id"] == "HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")

    def test_registry_and_genealogy(self):
        source_ids = {x["source_id"] for x in self.registry["sources"]}
        for source in ("EXT-SHIDIAN-MINGSHILU-XIANZONG-V4-TIANSHUN8-ECLIPSE-CHUKUI-CONTROL", "EXT-SHIDIAN-MINGSHILU-XIAOZONG-V162-HONGZHI13-ECLIPSE-QIYUAN-CONTROL", "EXT-SHIDIAN-MINGSHILU-SHENZONG-V477-WANLI38-ECLIPSE-PHASE-CLOCK-CONTROL"):
            self.assertIn(source, source_ids)
        node_ids = {x["node_id"] for x in self.graph["nodes"]}
        edge_ids = {x["edge_id"] for x in self.graph["edges"]}
        for node in self.record["transmission_impact"]["graph_nodes_added"]:
            self.assertIn(node, node_ids)
        for edge in self.record["transmission_impact"]["graph_edges_added"]:
            self.assertIn(edge, edge_ids)


if __name__ == "__main__":
    unittest.main()

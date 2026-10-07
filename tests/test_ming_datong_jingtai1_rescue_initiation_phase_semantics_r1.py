import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MingDatongJingtai1RescueInitiationPhaseSemanticsR1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((ROOT / "docs/research/MING-DATONG-JINGTAI1-RESCUE-INITIATION-PHASE-SEMANTICS-R1.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.graph = json.loads((ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_early_ming_rescue_starts_at_initial_eclipse(self):
        controls = self.record["institutional_controls"]
        self.assertIn("報日初蝕", controls[0]["wording"])
        self.assertIn("月食儀注同前", controls[0]["wording"])
        self.assertIn("報日初食", controls[1]["wording"])
        self.assertTrue(self.record["adjudication"]["early_ming_rescue_initiation_source_scoped_closed"])
        self.assertEqual(self.record["adjudication"]["early_ming_rescue_initiation_phase"], "INITIAL_ECLIPSE_ONSET")
        self.assertEqual(self.record["adjudication"]["jingtai1_rescue_operational_trigger"], "INITIAL_ECLIPSE_ONSET")

    def test_12ps_lexical_firewall_is_preserved(self):
        self.assertFalse(self.record["target"]["explicit_phase_lexeme"])
        self.assertEqual(self.record["adjudication"]["normalize_bare_dangzai_to_explicit_chukui_lexeme"], "FORBIDDEN")
        self.assertEqual(self.record["adjudication"]["target_bare_dangzai_lexical_phase_identity"], "UNRESOLVED")

    def test_absolute_anchor_and_runtime_remain_fail_closed(self):
        a = self.record["adjudication"]
        self.assertEqual(a["target_time_acquisition_method"], "UNRESOLVED")
        self.assertEqual(a["target_explicit_locality"], "UNRESOLVED")
        self.assertEqual(a["jingtai1_absolute_anchor_status"], "NOT_YET_ADMISSIBLE")
        self.assertEqual(a["md_g03_status_after_batch"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertFalse(a["runtime_authorized"])
        row = next(x for x in self.matrix["rows"] if x["rule_id"] == "HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")

    def test_registry_and_genealogy(self):
        source_ids = {x["source_id"] for x in self.registry["sources"]}
        for source in ("EXT-CTEXT-ZHUSI-ZHIZHANG-HONGWU26-ECLIPSE-RESCUE-INITIATION", "EXT-CTEXT-ZHENGDE-MING-HUIDIAN-V95-ECLIPSE-RESCUE-INITIATION"):
            self.assertIn(source, source_ids)
        node_ids = {x["node_id"] for x in self.graph["nodes"]}
        edge_ids = {x["edge_id"] for x in self.graph["edges"]}
        for node in self.record["transmission_impact"]["graph_nodes_added"]:
            self.assertIn(node, node_ids)
        for edge in self.record["transmission_impact"]["graph_edges_added"]:
            self.assertIn(edge, edge_ids)


if __name__ == "__main__":
    unittest.main()

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MingDatongJingtai1MingShiluPhysicalCollationR1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((ROOT / "docs/research/MING-DATONG-JINGTAI1-MINGSHILU-PHYSICAL-COLLATION-R1.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.graph = json.loads((ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_physical_target(self):
        p = self.record["physical_page_binding"]
        self.assertEqual(p["juan187_opening_pdf_page"], 2)
        self.assertEqual(p["target_pdf_page"], 10)
        self.assertEqual(p["target_page_sha256"], "8e431e1b51a8cf7b040564d94d18f120ac31b4418053b0abee9ffb30937c07e5")
        self.assertEqual(p["direct_target_reading"], "是日早月食當在卯正三刻欽天監官以為辰初初刻致失救護六科十三道劾監正許惇等推測不明下三法司論罪當徒詔宥之")
        self.assertEqual(p["target_name_glyph"], "許惇")
        self.assertFalse(self.record["source_route"]["ocr_used_for_final_glyph_claims"])

    def test_digital_variant_firewall(self):
        p = self.record["physical_page_binding"]
        self.assertEqual(p["received_digital_transcription_variant"], "許敦")
        self.assertEqual(p["received_digital_transcription_variant_status"], "DIGITAL_TRANSCRIPTION_VARIANT_NOT_PHYSICAL_GLYPH_AUTHORITY")
        self.assertFalse(self.record["physical_vs_received_text"]["person_identity_split_authorized"])
        self.assertEqual(self.record["physical_vs_received_text"]["independent_witness_increment_from_digital_variant"], 0)

    def test_fail_closed(self):
        a = self.record["adjudication"]
        self.assertEqual(a["jingtai1_absolute_anchor_status"], "NOT_YET_ADMISSIBLE")
        self.assertEqual(a["md_g03_status_after_batch"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertFalse(a["runtime_authorized"])
        row = next(x for x in self.matrix["rows"] if x["rule_id"] == "HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")

    def test_registry_and_genealogy_bindings(self):
        src = next(x for x in self.registry["sources"] if x["source_id"] == "EXT-NLC-WIKIMEDIA-YINGZONG-SHILU-V19-P10-JINGTAI1-ECLIPSE-PHYSICAL")
        self.assertTrue(src["physical_glyph_authority"])
        nodes = {x["node_id"] for x in self.graph["nodes"]}
        edges = {x["edge_id"] for x in self.graph["edges"]}
        for node in self.record["transmission_impact"]["graph_nodes_added"]:
            self.assertIn(node, nodes)
        for edge in self.record["transmission_impact"]["graph_edges_added"]:
            self.assertIn(edge, edges)


if __name__ == "__main__":
    unittest.main()

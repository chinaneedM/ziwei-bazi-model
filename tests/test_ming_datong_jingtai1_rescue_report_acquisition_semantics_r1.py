import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MingDatongJingtai1RescueReportAcquisitionSemanticsR1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((ROOT / "docs/research/MING-DATONG-JINGTAI1-RESCUE-REPORT-ACQUISITION-SEMANTICS-R1.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.graph = json.loads((ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))

    def test_forecast_and_live_cehou_are_separate(self):
        e = self.record["evidence_controls"][1]
        self.assertIn("上命臨時測候", e["received_points"])
        self.assertEqual(
            self.record["adjudication"]["early_mid_ming_prediction_vs_live_observation_separation"],
            "CLOSED_SOURCE_SCOPED",
        )
        self.assertEqual(
            self.record["adjudication"]["rescue_report_not_intrinsically_direct_observation"],
            "CLOSED_SOURCE_SCOPED",
        )

    def test_weather_waiver_does_not_become_observation_method(self):
        s = self.record["semantic_adjudication"]
        self.assertEqual(s["hongwu_weather_waiver_proves_direct_observation"], "NO")
        self.assertEqual(
            s["hongwu_weather_waiver_scope"],
            "RITUAL_EXECUTION_VISIBILITY_CONDITION_ONLY",
        )
        self.assertEqual(s["direct_visual_observation_inferred_from_bao_chushi"], "FORBIDDEN")

    def test_jingtai_corrected_time_remains_unbound(self):
        s = self.record["semantic_adjudication"]
        self.assertEqual(
            s["jingtai1_wrong_qintianjian_time_role"],
            "FAILED_FORECAST_OR_PREDICTIVE_DETERMINATION",
        )
        self.assertEqual(s["jingtai1_corrected_maozheng_time_acquisition"], "UNRESOLVED")
        self.assertEqual(s["jingtai1_corrected_time_clock_or_instrument"], "UNRESOLVED")
        a = self.record["adjudication"]
        self.assertEqual(a["jingtai1_absolute_anchor_status"], "NOT_YET_ADMISSIBLE")
        self.assertFalse(a["runtime_authorized"])
        row = next(x for x in self.matrix["rows"] if x["rule_id"] == "HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")

    def test_registry_and_genealogy(self):
        source_ids = {x["source_id"] for x in self.registry["sources"]}
        self.assertIn("EXT-CTEXT-WANLI-DAMING-HUIDIAN-V103-HONGWU-ECLIPSE-WEATHER-WAIVER", source_ids)
        node_ids = {x["node_id"] for x in self.graph["nodes"]}
        edge_ids = {x["edge_id"] for x in self.graph["edges"]}
        for node in self.record["transmission_impact"]["graph_nodes_added"]:
            self.assertIn(node, node_ids)
        for edge in self.record["transmission_impact"]["graph_edges_added"]:
            self.assertIn(edge, edge_ids)


if __name__ == "__main__":
    unittest.main()

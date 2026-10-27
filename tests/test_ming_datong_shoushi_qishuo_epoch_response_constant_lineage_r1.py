import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class MingDatongShoushiQishuoEpochResponseConstantLineageR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"docs/research/MING-DATONG-SHOUSHI-QISHUO-EPOCH-RESPONSE-CONSTANT-LINEAGE-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
        cls.g=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))

    def test_direct_gk12437_epoch_and_revised_constants(self):
        g=self.r["evidence_layers"]["gk12437_direct_physical"]
        self.assertEqual(g["readings"]["pages_001b_002a"]["閏應"],"202050")
        self.assertEqual(g["readings"]["pages_001b_002a"]["轉應"],"130205")
        self.assertEqual(g["readings"]["pages_001b_002a"]["交應"],"260388")
        self.assertIn("至元辛巳積年減一",g["readings"]["page_002a_formula"])

    def test_yuan_epoch_and_ying_are_separate(self):
        y=self.r["evidence_layers"]["yuanshi_received_shoushi"]
        self.assertIn("隨時推測，不用為元",y["passage"])
        self.assertEqual(y["initial_values"]["閏應"],"201850")
        self.assertEqual(self.r["adjudication"]["closed_subquestion"],"ZHIYUAN_XINSI_EPOCH_INHERITANCE_IS_NOT_A_GEOGRAPHIC_MERIDIAN_BINDING")

    def test_goryeo_mixed_recension(self):
        g=self.r["evidence_layers"]["goryeosa_received_transmission"]
        self.assertEqual(g["values"]["閏應"],"202050")
        self.assertEqual(g["values"]["轉應"],"131904")
        self.assertEqual(g["values"]["交應"],"260388")

    def test_g03_stays_open(self):
        self.assertFalse(self.r["adjudication"]["epoch_identity_proves_qishuo_meridian"])
        self.assertEqual(self.r["adjudication"]["dadu_beijing_qishuo_reference"],"UNRESOLVED")
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertFalse(g03["batch_12pe_refinement"]["epoch_identity_proves_qishuo_meridian"])

    def test_matrix_state_and_graph(self):
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")
        self.assertIn("BATCH-12-BAZI-MING-DATONG-SHOUSHI-QISHUO-EPOCH-RESPONSE-CONSTANT-LINEAGE-PE",self.s["historical_audit"]["completed_batches"])
        nodes={n["node_id"] for n in self.g["nodes"]}
        self.assertIn("RULE-SHOUSHI-LIYUAN-YING-SEPARATION-QISHUO",nodes)
        nes=[x for x in self.g["explicit_non_edges"] if x.get("adjudication_batch")=="BATCH-12-BAZI-MING-DATONG-SHOUSHI-QISHUO-EPOCH-RESPONSE-CONSTANT-LINEAGE-PE"]
        self.assertEqual(len(nes),1)
        self.assertEqual(nes[0]["status"],"DISPROVED")

if __name__=="__main__":
    unittest.main()

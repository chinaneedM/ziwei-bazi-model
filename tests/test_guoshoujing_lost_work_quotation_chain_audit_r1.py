import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class GuoShoujingLostWorkQuotationChainAuditR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"docs/research/GUOSHOUJING-LOST-WORK-QUOTATION-CHAIN-AUDIT-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
        cls.g=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))

    def test_no_direct_lost_work_quote_recovered(self):
        a=self.r["adjudication"]
        self.assertFalse(a["direct_quote_from_xiugai_yuanliu_recovered"])
        self.assertFalse(a["direct_quote_from_gujin_jiaoshikao_recovered"])
        self.assertFalse(a["explicit_source_citation_for_1294_revision_recovered"])
        self.assertEqual(a["later_narrative_convergence"],"ATTESTED")

    def test_no_site_gain(self):
        a=self.r["adjudication"]
        self.assertFalse(a["site_or_meridian_wording_recovered"])
        self.assertEqual(a["evidence_increment_for_1294_site"],0)
        self.assertEqual(a["qishuo_geographic_reference"],"UNRESOLVED")

    def test_route_is_parked(self):
        d=self.r["route_disposition"]
        self.assertEqual(d["repeat_same_generic_lost_work_title_search"],"PARKED_UNLESS_MATERIALLY_NEW_WITNESS")
        self.assertIn("ALMANAC",d["next_route"])

    def test_g03_and_product_remain_fail_closed(self):
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12ph_refinement"]["direct_lost_work_quote_recovered"],False)
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")
        self.assertIn("BATCH-12-BAZI-GUOSHOUJING-LOST-WORK-QUOTATION-CHAIN-AUDIT-PH",self.s["historical_audit"]["completed_batches"])

    def test_graph_firewall(self):
        ne=[x for x in self.g["explicit_non_edges"] if x.get("adjudication_batch")=="BATCH-12-BAZI-GUOSHOUJING-LOST-WORK-QUOTATION-CHAIN-AUDIT-PH"]
        self.assertGreaterEqual(len(ne),2)
        self.assertTrue(all(x["status"]=="DISPROVED" for x in ne))

if __name__=="__main__":
    unittest.main()

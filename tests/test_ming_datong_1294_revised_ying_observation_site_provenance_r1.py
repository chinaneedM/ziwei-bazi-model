import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class MingDatong1294RevisedYingObservationSiteProvenanceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"docs/research/MING-DATONG-1294-REVISED-YING-OBSERVATION-SITE-PROVENANCE-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
        cls.g=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))

    def test_multi_site_network(self):
        n=self.r["evidence"]["yuan_observation_network"]
        self.assertIn("建司天臺於大都",n["dadu"])
        self.assertIn("上都",n["additional_sites"])
        self.assertIn("MULTI_SITE",n["result"])

    def test_target_site_remains_unresolved(self):
        a=self.r["adjudication"]
        self.assertEqual(a["revised_ying_exact_observation_site"],"UNRESOLVED")
        self.assertEqual(a["dadu_as_target_revision_site"],"UNRESOLVED")
        self.assertEqual(a["shangdu_as_target_revision_site"],"UNRESOLVED")
        self.assertEqual(a["qishuo_geographic_reference"],"UNRESOLVED")
        self.assertFalse(a["runtime_authorized"])

    def test_later_trigger_does_not_gain_site(self):
        t=self.r["evidence"]["later_revision_trigger"]
        self.assertFalse(t["site_named"])
        self.assertIn("差天二刻",t["statement"])

    def test_g03_and_product_stay_fail_closed(self):
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12pf_refinement"]["exact_1294_revision_site"],"UNRESOLVED")
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")
        self.assertIn("BATCH-12-BAZI-MING-DATONG-1294-REVISED-YING-OBSERVATION-SITE-PROVENANCE-PF",self.s["historical_audit"]["completed_batches"])

    def test_graph_records_network_without_meridian_selection(self):
        ids={n["node_id"] for n in self.g["nodes"]}
        self.assertIn("NETWORK-YUAN-SHOUSHI-MULTISITE-OBSERVATION-1279",ids)
        ne=[x for x in self.g["explicit_non_edges"] if x.get("adjudication_batch")=="BATCH-12-BAZI-MING-DATONG-1294-REVISED-YING-OBSERVATION-SITE-PROVENANCE-PF"]
        self.assertEqual(len(ne),1)
        self.assertEqual(ne[0]["status"],"DISPROVED")

if __name__=="__main__":
    unittest.main()

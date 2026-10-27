import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class GuoShoujingLostWorksBibliographicSurvivalControlR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"docs/research/GUOSHOUJING-LOST-WORKS-BIBLIOGRAPHIC-SURVIVAL-CONTROL-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
        cls.s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
        cls.g=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))

    def test_one_juan_preferred(self):
        self.assertEqual(self.r["bibliographic_witnesses"]["yuanshi_biography"]["work_counts"]["修改源流"],"1卷")
        self.assertEqual(self.r["bibliographic_witnesses"]["qianqingtang_shumu"]["work_counts"]["修改源流"],"1卷")
        self.assertEqual(self.r["bibliographic_witnesses"]["xinyuanshi"]["work_counts"]["修改源流"],"7卷")
        self.assertEqual(self.r["adjudication"]["xiugai_yuanliu_preferred_volume_count"],"1卷")

    def test_homonyms_do_not_collapse(self):
        self.assertFalse(self.r["homonym_controls"]["chongzhen_lishu"]["same_as_guo_work"])
        self.assertFalse(self.r["homonym_controls"]["zhu_zaiyu"]["same_as_guo_work"])
        self.assertFalse(self.r["adjudication"]["title_only_homonym_match_authorized"])

    def test_survival_and_site_remain_open(self):
        self.assertFalse(self.r["survival_and_access"]["direct_public_text_of_guo_xiugai_yuanliu_located"])
        self.assertFalse(self.r["survival_and_access"]["direct_public_text_of_guo_gujin_jiaoshikao_located"])
        self.assertEqual(self.r["adjudication"]["qishuo_geographic_reference"],"UNRESOLVED")
        self.assertEqual(self.r["adjudication"]["evidence_increment_for_1294_site"],0)

    def test_project_invariants(self):
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")
        self.assertIn("BATCH-12-BAZI-GUOSHOUJING-LOST-WORKS-BIBLIOGRAPHIC-SURVIVAL-CONTROL-PG",self.s["historical_audit"]["completed_batches"])
        self.assertEqual(self.r["provenance"]["provenance_defect_increment"],0)

    def test_graph_work_nodes_exist(self):
        ids={n["node_id"] for n in self.g["nodes"]}
        self.assertIn("TEXT-WORK-GUOSHOUJING-XIUGAI-YUANLIU",ids)
        self.assertIn("TEXT-WORK-GUOSHOUJING-GUJIN-JIAOSHIKAO",ids)
        nes=[x for x in self.g["explicit_non_edges"] if x.get("adjudication_batch")=="BATCH-12-BAZI-GUOSHOUJING-LOST-WORKS-BIBLIOGRAPHIC-SURVIVAL-CONTROL-PG"]
        self.assertEqual(len(nes),2)

if __name__=="__main__":
    unittest.main()

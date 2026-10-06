import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MingDatongGK12437QishuoLocalityOperatorAuditR1Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.research=json.loads((ROOT/"docs/research/MING-DATONG-GK12437-QISHUO-LOCALITY-OPERATOR-AUDIT-R1.json").read_text(encoding="utf-8"))
  cls.blockers=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
  cls.matrix=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))
  cls.state=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
  cls.graph=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8"))
 def test_physical_scope_and_positive_controls(self):
  a=self.research["acquisition"];self.assertEqual(a["method_block_reviewed"],"001a-005b");self.assertFalse(a["ocr_used_for_final_glyph_or_operator_claims"])
  p=self.research["page_bindings"]["direct_positive_controls"];self.assertIn("求經朔分",p["002b"]);self.assertIn("求定朔及望分",p["004b"]);self.assertIn("大陽冬至前後二象盈初縮末限",p["006a"])
 def test_negative_claim_is_strictly_scoped(self):
  a=self.research["locality_operator_audit"];self.assertFalse(a["named_place_or_meridian_operator_attested"]);self.assertFalse(a["li_difference_operator_attested"]);self.assertEqual(a["result"],"EXPLICIT_LOCALITY_OPERATOR_NOT_ATTESTED_ON_COMPLETE_REVIEWED_QISHUO_METHOD_BLOCK")
  d=self.research["adjudication"];self.assertEqual(d["md_g03_status_after_batch"],"OPEN_BLOCKING_GENERAL_ADAPTER");self.assertEqual(d["qishuo_geographic_reference"],"UNRESOLVED");self.assertFalse(d["runtime_selection_authorized"])
 def test_live_blocker_ledger_preserves_g03(self):
  g={x["gate_id"]:x for x in self.blockers["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"];self.assertEqual(g["status"],"OPEN_BLOCKING_GENERAL_ADAPTER");r=g["batch_12pd_refinement"];self.assertEqual(r["explicit_locality_operator_subquestion"],"CLOSED_NEGATIVE_OBJECT_METHOD_BLOCK_SCOPE");self.assertEqual(r["implicit_or_inherited_reference"],"UNRESOLVED");self.assertFalse(r["runtime_authorized"])
  self.assertEqual(self.blockers["batch_12pd_forward_refinement"]["current_live_gate_accounting_after_12pd"],{"closed_source_scoped":5,"open_blocking_general_adapter":4,"dependency_blocked":2,"total_gates":11})
 def test_matrix_and_state_remain_fail_closed(self):
  row=next(r for r in self.matrix["rows"] if r["rule_id"]=="HPA-DAYUN-CAL-002");self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT");self.assertFalse(row["batch_12pd_gk12437_qishuo_locality_operator_audit"]["runtime_authorized"]);self.assertEqual(self.state["historical_audit"]["current_missing_from_product_row_count"],4);self.assertIn("BATCH-12-BAZI-MING-DATONG-GK12437-QISHUO-LOCALITY-OPERATOR-AUDIT-PD",self.state["historical_audit"]["completed_batches"])
 def test_genealogy_records_passage_without_parentage_claim(self):
  nodes={n["node_id"]:n for n in self.graph["nodes"]};self.assertIn("PASSAGE-KYUDB-GK12437-QISHUO-METHOD-BLOCK-001A-005B",nodes)
  edges=[e for e in self.graph["edges"] if e.get("adjudication_batch")=="BATCH-12-BAZI-MING-DATONG-GK12437-QISHUO-LOCALITY-OPERATOR-AUDIT-PD"];self.assertEqual(len(edges),1);self.assertEqual(edges[0]["relation"],"ATTESTS");self.assertEqual(edges[0]["status"],"CONFIRMED")
if __name__=="__main__": unittest.main()

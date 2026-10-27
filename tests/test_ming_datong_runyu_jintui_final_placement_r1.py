from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/research_ming_datong_runyu_jintui_final_placement_r1.py"
spec=importlib.util.spec_from_file_location("ming_datong_runyu_jintui_pc",SCRIPT);assert spec and spec.loader
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class MingDatongRunyuJintuiFinalPlacementR1Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.result=module.run(ROOT);cls.research=json.loads((ROOT/"docs/research/MING-DATONG-RUNYU-JINTUI-FINAL-PLACEMENT-R1.json").read_text(encoding="utf-8"));cls.ou=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
 def test_q2_boundary_is_exactly_ten_and_splits_five_five(self):
  self.assertEqual(self.result["q2_boundary_count"],10);self.assertEqual(self.result["retreat_threshold_labels"],[1374,1393,1412,1431,1526]);self.assertEqual(self.result["stay_threshold_labels"],[1450,1469,1488,1507,1545]);self.assertEqual((self.result["retreat_count"],self.result["stay_count"]),(5,5))
 def test_all_q2_controls_match_all_profiles(self):
  self.assertEqual((self.result["precision_profile_count"],self.result["q2_profile_control_count"],self.result["matched_q2_profile_controls"]),(4,40,40));self.assertTrue(self.result["all_q2_profile_controls_match"])
 def test_full_ming_threshold_owner_alignment_closes(self):
  self.assertEqual(self.result["year_range"],[1368,1644]);self.assertEqual(self.result["year_count"],277);self.assertEqual(self.result["runyu_threshold_label_count"],102);self.assertEqual(self.result["full_owner_count"],102);self.assertEqual(self.result["full_owner_ambiguities"],[]);self.assertEqual(self.result["profile_structural_divergence_years"],[]);self.assertEqual(self.result["final_owner_existence_mismatches_1368_1643"],[])
 def test_q2_is_not_collapsible_to_one_quotient_owner_rule(self):
  self.assertEqual({x["disposition"] for x in self.result["summaries"]},{"RETREAT_TO_PRECEDING_CIVIL_YEAR","STAY_IN_THRESHOLD_LABEL_CIVIL_YEAR"});self.assertTrue(all(x["all_profiles_match"] for x in self.result["summaries"]))
 def test_g09_closes_only_forward_live_state(self):
  g={x["gate_id"]:x for x in self.ou["gates"]}["MD-G09-MULTI-YEAR-LEAP-GENERALIZATION"];self.assertEqual(g["status"],"OPEN_BLOCKING_GENERAL_ADAPTER");r=g["batch_12pc_refinement"];self.assertEqual(r["status_after_batch"],"CLOSED_SOURCE_SCOPED");self.assertEqual(r["q2_profile_controls"],"40_OF_40_MATCH");self.assertFalse(r["runtime_authorized"]);self.assertFalse(self.research["runtime_selection_authorized"]);self.assertEqual(self.ou["batch_12pc_forward_refinement"]["current_live_gate_accounting_after_12pc"],{"closed_source_scoped":5,"open_blocking_general_adapter":4,"dependency_blocked":2,"total_gates":11})
if __name__=="__main__":unittest.main()

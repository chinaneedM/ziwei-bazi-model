from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/research_ming_datong_preyear_leap_global_validation_r1.py"
spec=importlib.util.spec_from_file_location("preyear_global_pb",SCRIPT);assert spec and spec.loader
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class MingDatongPreyearLeapGlobalValidationR1Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.result=module.run(ROOT);cls.research=json.loads((ROOT/"docs/research/MING-DATONG-PREYEAR-LEAP-CIVIL-YEAR-GLOBAL-VALIDATION-R1.json").read_text(encoding="utf-8"));cls.oracle=json.loads((ROOT/"docs/research/MING-DATONG-PREYEAR-LEAP-CIVIL-YEAR-ORACLE-R1.json").read_text(encoding="utf-8"));cls.ou=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
 def test_all_15_controls_match_all_profiles(self):
  self.assertEqual((self.result["preyear_candidate_year_count"],self.result["profile_count"],self.result["profile_year_control_count"],self.result["matched_profile_year_controls"]),(15,4,60,60));self.assertTrue(self.result["all_preyear_profile_year_controls_match"])
 def test_expected_leap_months(self):
  expected={int(x["civil_year"]):int(x["expected_leap_month"]) for x in self.oracle["controls"]};got={int(x["civil_year"]):int(x["expected_leap_month"]) for x in self.result["year_summaries"] if x["all_profiles_match"]};self.assertEqual(got,expected);self.assertEqual((expected[1384],expected[1403],expected[1422],expected[1642]),(10,11,12,11))
 def test_explicit_boundary_not_fixed_k2(self):
  self.assertFalse(self.result["fixed_k2_anchor_used"]);source=(ROOT/"scripts/research_ming_datong_multi_year_leap_validation_r1.py").read_text(encoding="utf-8");self.assertNotIn('if row["k"] < 2',source);self.assertIn("FIRST_REGULAR_MONTH_1_TO_BEFORE_NEXT_REGULAR_MONTH_1",source)
 def test_full_ming_rerun(self):
  self.assertEqual(self.result["year_range"],[1368,1644]);self.assertEqual(self.result["year_count"],277);self.assertEqual(self.result["profile_structural_divergence_years"],[]);self.assertEqual(self.result["formula_ownership_mismatches_1368_1643"],[]);self.assertTrue(self.result["terminal_year_1644_formula_ownership_comparison_excluded"])
 def test_g09_closed_source_scoped_runtime_closed(self):
  g={x["gate_id"]:x for x in self.ou["gates"]}["MD-G09-MULTI-YEAR-LEAP-GENERALIZATION"];self.assertEqual(g["status"],"OPEN_BLOCKING_GENERAL_ADAPTER");self.assertEqual(g["batch_12pb_refinement"]["profile_year_controls"],"60_OF_60_MATCH");self.assertEqual(g["batch_12pb_refinement"]["status_after_batch"],"CLOSED_SOURCE_SCOPED");self.assertEqual(g["batch_12pb_refinement"]["historical_snapshot_top_level_status_preserved"],"OPEN_BLOCKING_GENERAL_ADAPTER");self.assertFalse(g["batch_12pb_refinement"]["runtime_authorized"]);self.assertFalse(self.research["runtime_selection_authorized"])
if __name__=="__main__":unittest.main()

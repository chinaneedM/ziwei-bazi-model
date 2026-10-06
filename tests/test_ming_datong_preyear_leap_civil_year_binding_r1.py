from __future__ import annotations
import importlib.util,json,unittest
from decimal import localcontext
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/research_ming_datong_preyear_leap_civil_year_binding_r1.py"
RESEARCH=ROOT/"docs/research/MING-DATONG-PREYEAR-LEAP-CIVIL-YEAR-BINDING-R1.json"
OU=ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json"
spec=importlib.util.spec_from_file_location("preyear_binding",SCRIPT);assert spec and spec.loader
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class MingDatongPreyearLeapCivilYearBindingR1Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.result=module.run(ROOT);cls.data=json.loads(RESEARCH.read_text(encoding="utf-8"));cls.ou=json.loads(OU.read_text(encoding="utf-8"))
 def test_full_ming_candidate_census_is_reproducible(self):
  self.assertEqual(self.result["year_count"],277);self.assertEqual(self.result["candidate_count"],15)
  self.assertEqual(self.result["candidate_threshold_label_years"],[1385,1404,1423,1442,1461,1480,1499,1518,1537,1556,1575,1594,1613,1632,1643])
  self.assertEqual(self.result["candidate_preceding_civil_years"],[1384,1403,1422,1441,1460,1479,1498,1517,1536,1555,1574,1593,1612,1631,1642])
 def test_1385_and_1480_take_preyear_branch(self):
  a=self.result["tension_controls"]["1385"];b=self.result["tension_controls"]["1480"]
  self.assertEqual((a["runyu_remainder_source_units"],a["shuo_minus_runyu_source_units"],a["placement_quotient_floor"],a["assigned_preceding_civil_year"]),("290824.02","4481.91",0,1384))
  self.assertEqual((b["runyu_remainder_source_units"],b["shuo_minus_runyu_source_units"],b["placement_quotient_floor"],b["assigned_preceding_civil_year"]),("286731.27","8574.66",0,1479))
  self.assertTrue(a["preyear_branch"]);self.assertTrue(b["preyear_branch"])
 def test_authority_layers_stay_separate(self):
  layers={x["layer_id"]:x for x in self.data["authority_layers"]}
  self.assertEqual(layers["PRIMARY_1569_RUNYU_EXISTENCE"]["authority"],"DIRECT_MING_FACSIMILE")
  self.assertEqual(layers["RECEIVED_MINGSHI_PREYEAR_PLACEMENT"]["authority"],"QING_COMPILED_RECEIVED_DATONG_RULE")
  self.assertIn("NOT_PROMOTED_TO_1569_DIRECT_WORDING",layers["RECEIVED_MINGSHI_PREYEAR_PLACEMENT"]["source_scope_firewall"])
 def test_four_12oz_tensions_resolved_without_closing_g09(self):
  self.assertEqual(self.data["adjudication"]["four_12oz_tension_labels"],"RESOLVED_AS_MISSING_PREYEAR_CIVIL_OWNERSHIP_BRANCH_NOT_PRIMARY_RUNYU_FORMULA_FAILURE")
  self.assertFalse(self.data["adjudication"]["d1_precision_failure_implicated"]);self.assertFalse(self.data["adjudication"]["fixed_k2_first_month_civil_anchor_universal"])
  self.assertEqual(self.data["adjudication"]["g09_status_after_batch"],"OPEN_BLOCKING_GENERAL_ADAPTER")
  gates={r["gate_id"]:r for r in self.ou["gates"]};self.assertEqual(gates["MD-G09-MULTI-YEAR-LEAP-GENERALIZATION"]["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
 def test_direct_civil_controls(self):
  c=self.data["authority_layers"][2]["controls"];self.assertEqual([(x["civil_year"],x["expected_leap_month"]) for x in c],[(1384,10),(1479,10)])
  self.assertEqual(c[0]["observed_heading"],"洪武十七年閏十月乙未朔");self.assertEqual(c[1]["observed_heading"],"成化十五年閏十月癸丑朔")
 def test_decimal_context_is_local(self):
  with localcontext() as poisoned: poisoned.prec=10; result=module.run(ROOT)
  self.assertEqual(result["candidate_count"],15);self.assertEqual(result["tension_controls"]["1385"]["shuo_minus_runyu_source_units"],"4481.91")
 def test_runtime_and_accounting_unchanged(self):
  for k in ("runtime_selection_authorized","production_default_changed","algorithm_reopen_authorized","candidate_collapse_authorized"): self.assertFalse(self.data[k])
  a=self.data["accounting"];self.assertEqual((a["matrix_rows"],a["audited_rows"],a["current_missing_from_product_rows"]),(222,222,4));self.assertEqual((a["provenance_defects_confirmed"],a["provenance_defects_repaired"]),(45,45))
if __name__=="__main__":unittest.main()

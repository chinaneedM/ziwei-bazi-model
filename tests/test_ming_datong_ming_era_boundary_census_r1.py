from __future__ import annotations
import importlib.util,json,unittest
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);assert spec and spec.loader
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
module=load("ming_era_boundary_census",ROOT/"scripts/research_ming_datong_ming_era_boundary_census_r1.py")
class MingDatongMingEraBoundaryCensusR1Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.result=module.run(ROOT);cls.research=json.loads((ROOT/"docs/research/MING-DATONG-MING-ERA-BOUNDARY-CENSUS-R1.json").read_text(encoding="utf-8"));cls.controls=json.loads((ROOT/"docs/research/MING-DATONG-CIVIL-YEAR-LATE-LEAP-CONTROLS-R1.json").read_text(encoding="utf-8"));cls.ou=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
 def test_full_sweep_profile_stable(self):
  self.assertEqual((self.result["year_count"],self.result["profile_count"]),(277,4));self.assertEqual(self.result["profile_structural_divergence_years"],[]);self.assertEqual(self.result["profile_new_moon_source_day_divergence_years"],[])
 def test_four_runyu_sui_tensions(self):
  t=self.result["runyu_vs_true_sui_tensions"];self.assertEqual([x["year"] for x in t],[1384,1385,1479,1480]);b={x["year"]:x for x in t};self.assertFalse(b[1384]["runyu_threshold_flag"]);self.assertTrue(b[1384]["sui_has_intercalary_month"]);self.assertEqual(b[1384]["sui_leap_month"],10);self.assertTrue(b[1385]["runyu_threshold_flag"]);self.assertFalse(b[1385]["sui_has_intercalary_month"]);self.assertFalse(b[1479]["runyu_threshold_flag"]);self.assertEqual(b[1479]["sui_leap_month"],10);self.assertTrue(b[1480]["runyu_threshold_flag"]);self.assertFalse(b[1480]["sui_has_intercalary_month"])
 def test_boundary_rankings(self):
  n=self.result["closest_new_moon_day_boundaries"][0];self.assertEqual((n["year"],n["k"]),(1425,5));self.assertLess(Decimal(n["margin_source_units"]),Decimal("2"));p=self.result["closest_same_day_zhongqi_new_moon_pairs"][0];self.assertEqual((p["year"],p["z"],p["k"]),(1414,11,12));self.assertLess(abs(Decimal(p["gap_source_units"])),Decimal("100"))
 def test_1596_control(self):self.assertEqual((self.result["1596_day_level_leap_month"],self.result["1596_exact_order_counterfactual_leap_month"]),(8,9))
 def test_civil_controls(self):
  c={x["civil_year"]:x for x in self.controls["controls"]};self.assertEqual(c[1373]["normalized_leap_month"],11);self.assertEqual(c[1384]["normalized_leap_month"],10)
 def test_g09_open_forward_only(self):
  self.assertTrue(self.research["scope_correction"]["batch_12oy_snapshot_preserved"]);g={x["gate_id"]:x for x in self.ou["gates"]}["MD-G09-MULTI-YEAR-LEAP-GENERALIZATION"];self.assertEqual(g["status"],"OPEN_BLOCKING_GENERAL_ADAPTER");r=g["batch_12oz_refinement"];self.assertEqual(r["runyu_vs_true_sui_tension_years"],[1384,1385,1479,1480]);self.assertFalse(r["runtime_authorized"])
if __name__=="__main__":unittest.main()

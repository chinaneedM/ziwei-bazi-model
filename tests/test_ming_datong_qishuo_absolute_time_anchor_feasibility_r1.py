import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class MingDatongQishuoAbsoluteTimeAnchorFeasibilityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"docs/research/MING-DATONG-QISHUO-ABSOLUTE-TIME-ANCHOR-FEASIBILITY-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))

    def test_ephemeris_span_and_delta_t(self):
        self.assertTrue(self.r["modern_ephemeris"]["target_1531_1639_covered"])
        self.assertEqual(self.r["earth_rotation"]["nasa_1300_1600_typical_uncertainty_seconds"],20)
        self.assertGreater(self.r["earth_rotation"]["signal_to_20s_delta_t_uncertainty_ratio"],20)

    def test_clock_semantics_is_real_blocker(self):
        s=self.r["solar_time_semantics"]
        self.assertEqual(s["historical_datong_qishuo_clock_mapping_to_apparent_solar_time"],"UNRESOLVED")
        self.assertEqual(s["historical_datong_qishuo_clock_mapping_to_mean_solar_time"],"UNRESOLVED")
        self.assertGreater(s["apparent_vs_mean_difference_can_reach_minutes"],s["beijing_nanjing_longitude_signal_minutes"])

    def test_no_meridian_selection(self):
        a=self.r["adjudication"]
        self.assertTrue(a["absolute_ephemeris_anchor_feasible"])
        self.assertFalse(a["delta_t_uncertainty_fatal_for_beijing_nanjing_discrimination"])
        self.assertFalse(a["historical_clock_standard_semantics_closed"])
        self.assertFalse(a["absolute_time_comparison_historically_admissible_for_meridian_selection"])

    def test_g03_remains_open(self):
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12pj_refinement"]["historical_qishuo_clock_standard_semantics"],"UNRESOLVED")
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")

if __name__=="__main__":
    unittest.main()

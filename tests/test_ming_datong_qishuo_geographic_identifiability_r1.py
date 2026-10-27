import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/research_ming_datong_qishuo_geographic_identifiability_r1.py"
spec=importlib.util.spec_from_file_location("qishuo_geo_ident",SCRIPT)
assert spec and spec.loader
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class MingDatongQishuoGeographicIdentifiabilityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=module.run(ROOT)
        cls.r=json.loads((ROOT/"docs/research/MING-DATONG-QISHUO-GEOGRAPHIC-IDENTIFIABILITY-AUDIT-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))

    def test_shift_diagnostic_counts(self):
        self.assertEqual(self.result["counts"],{"no_shift":56,"plus_delta":22,"minus_delta":17})
        self.assertEqual(self.result["plus_day_crossings"],0)
        self.assertEqual(self.result["minus_day_crossings"],0)
        self.assertAlmostEqual(float(self.result["nearest_boundary"]["minutes"]),17.28,places=6)

    def test_identifiability_firewall(self):
        i=self.r["identifiability"]
        self.assertTrue(i["printed_bins_and_d1_share_same_unknown_historical_coordinate"])
        self.assertFalse(i["internal_fit_identifies_absolute_meridian"])
        self.assertFalse(i["no_shift_best_fit_is_geographic_evidence"])
        self.assertEqual(i["direct_beijing_vs_nanjing_selection_from_56_bins"],"FORBIDDEN")

    def test_g03_stays_open(self):
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12pi_refinement"]["absolute_meridian_identifiable_from_56_internal_bins"],False)
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")

if __name__=="__main__":
    unittest.main()

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class MingDatongQishuoZizhengClockStandardSemanticsR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/"docs/research/MING-DATONG-QISHUO-ZIZHENG-CLOCK-STANDARD-SEMANTICS-R1.json").read_text(encoding="utf-8"))
        cls.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8"))
        cls.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8"))

    def test_internal_clock_is_closed(self):
        a=self.r["adjudication"]
        self.assertEqual(a["internal_uniform_100ke_zizheng_coordinate"],"CLOSED_SOURCE_SCOPED")
        self.assertEqual(self.r["direct_shoushi_clock_rule"]["source_day_unit"],"日周10000")
        self.assertIn("命子正算外",self.r["direct_shoushi_clock_rule"]["received_text"])

    def test_absolute_realization_stays_open(self):
        a=self.r["adjudication"]
        self.assertEqual(a["direct_identity_with_local_apparent_solar_time"],"NOT_ATTESTED")
        self.assertEqual(a["direct_identity_with_local_mean_solar_time"],"NOT_ATTESTED")
        self.assertEqual(a["direct_identity_with_measured_clepsydra_time"],"NOT_ATTESTED_IN_QISHUO_METHOD")
        self.assertEqual(a["absolute_clock_standard_semantics"],"UNRESOLVED")

    def test_gengwu_is_positive_control_only(self):
        p=self.r["explicit_geographic_positive_control"]
        self.assertTrue(p["different_calendar_from_shoushi"])
        self.assertIn("里差",p["received_text"])
        self.assertIn("must not be imported",p["firewall"])

    def test_g03_remains_open(self):
        g03={x["gate_id"]:x for x in self.b["gates"]}["MD-G03-QISHUO-GEOGRAPHIC-REFERENCE"]
        self.assertEqual(g03["status"],"OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(g03["batch_12pk_refinement"]["internal_uniform_zizheng_clock"],"CLOSED_SOURCE_SCOPED")
        self.assertEqual(g03["batch_12pk_refinement"]["absolute_physical_time_realization"],"UNRESOLVED")
        row=next(x for x in self.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002")
        self.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT")

if __name__=="__main__":
    unittest.main()

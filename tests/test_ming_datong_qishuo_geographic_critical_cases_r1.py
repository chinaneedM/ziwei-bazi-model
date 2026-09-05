import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs" / "research" / "MING-DATONG-QISHUO-GEOGRAPHIC-CRITICAL-CASES-R1.json"


class MingDatongQishuoGeographicCriticalCasesR1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = {item["case_id"]: item for item in cls.data["cases"]}

    def test_research_only_firewall(self):
        self.assertEqual(self.data["status"], "RESEARCH_ONLY_DIAGNOSTIC_NOT_RUNTIME")
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["geographic_reference_closed"])
        self.assertEqual(
            self.data["geographic_firewall"]["ming_datong_qishuo_geographic_reference"],
            "UNRESOLVED",
        )
        self.assertTrue(
            self.data["geographic_firewall"]["no_single_longitude_shift_adjudication_without_physical_almanac"]
        )

    def test_beijing_nanjing_diagnostic_delta(self):
        geo = self.data["modern_comparison_coordinates"]
        delta_deg = geo["nanjing_longitude_east_deg"] - geo["beijing_longitude_east_deg"]
        delta_min = delta_deg * 4.0
        self.assertTrue(math.isclose(delta_deg, 2 + 28 / 60, abs_tol=1e-9))
        self.assertTrue(math.isclose(delta_min, 9 + 52 / 60, abs_tol=1e-9))
        self.assertTrue(
            math.isclose(delta_min, geo["local_apparent_solar_time_delta_minutes"], abs_tol=1e-8)
        )

    @staticmethod
    def day_crossing(fraction, shift_minutes):
        shifted = fraction + shift_minutes / 1440.0
        if shifted >= 1.0:
            return 1
        if shifted < 0.0:
            return -1
        return 0

    def test_boundary_sensitivity_is_diagnostic_not_adjudicative(self):
        shift = self.data["modern_comparison_coordinates"]["local_apparent_solar_time_delta_minutes"]

        # 1370 D1 is 3.456 min after 子正: an eastward shift stays on 辛酉,
        # while a westward shift of the Beijing-Nanjing magnitude crosses backward.
        self.assertEqual(self.day_crossing(0.0024, shift), 0)
        self.assertEqual(self.day_crossing(0.0024, -shift), -1)

        # 1497 D1 is only 25.92 s before 子正: an eastward shift crosses forward.
        self.assertEqual(self.day_crossing(0.9997, shift), 1)
        self.assertEqual(self.day_crossing(0.9997, -shift), 0)

        # 1495 is over four hours after 子正. A ~9m52s longitude shift cannot
        # explain a previous-day reign-record date.
        self.assertEqual(self.day_crossing(0.1775, shift), 0)
        self.assertEqual(self.day_crossing(0.1775, -shift), 0)

    def test_reign_record_is_not_physical_almanac_certification(self):
        case_1462 = self.cases["MING-1462-M11"]
        self.assertEqual(case_1462["ming_shilu_ganzhi"], "壬辰")
        self.assertEqual(case_1462["surviving_same_year_almanac_ganzhi"], "辛卯")
        self.assertEqual(case_1462["d1_ganzhi"], "辛卯")
        self.assertEqual(
            self.data["adjudication"]["reign_record_as_same_year_almanac_substitute"],
            "FORBIDDEN",
        )

    def test_new_reign_record_controls_preserve_conflict(self):
        self.assertEqual(self.cases["MING-1370-M02"]["ming_shilu_ganzhi"], "辛酉")
        self.assertEqual(self.cases["MING-1495-M07"]["ming_shilu_ganzhi"], "辛巳")
        self.assertEqual(self.cases["MING-1497-M10"]["ming_shilu_ganzhi"], "己巳")
        self.assertEqual(self.cases["MING-1581-M10"]["ming_shilu_ganzhi"], "辛卯")
        self.assertEqual(self.data["adjudication"]["geographic_conclusion"], "UNRESOLVED")


if __name__ == "__main__":
    unittest.main()

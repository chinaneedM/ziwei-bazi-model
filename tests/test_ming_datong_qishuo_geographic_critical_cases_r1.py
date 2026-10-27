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
        cls.contexts = {item["context_id"]: item for item in cls.data["historical_operational_context"]}

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


    def test_hongzhi_10_target_calendar_was_issued_but_not_physically_certified(self):
        ctx = self.contexts["MING-1496-ISSUE-HONGZHI-10-ALMANAC"]
        self.assertIn("弘治十年大統曆", ctx["record"])
        self.assertFalse(ctx["physical_copy_located"])
        self.assertEqual(
            ctx["inference_scope"],
            "ISSUANCE_CERTIFICATION_NOT_MONTH_START_VALUE_CERTIFICATION",
        )

    def test_1497_reform_memorial_does_not_explain_qishuo_mismatch_by_itself(self):
        ctx = self.contexts["MING-1497-ZHUSHENG-REFORM-MEMORIAL"]
        self.assertEqual(ctx["observed_problem"], "曆法有差月食不驗")
        self.assertIn("歲差", ctx["ministry_response_mentions"])
        self.assertTrue(
            ctx["do_not_attribute_1497_m10_mismatch_to_memorial_without_direct_link"]
        )
        self.assertEqual(
            self.data["adjudication"]["reform_memorial_as_qishuo_meridian_proof"],
            "FORBIDDEN",
        )

    def test_1521_mixed_geography_evidence_preserves_qishuo_firewall(self):
        ctx = self.contexts["MING-1521-ZHUYU-MIXED-GEOGRAPHY-MEMORIAL"]
        self.assertIn("雖以大統為名實授時之曆", ctx["direct_claims"])
        self.assertIn("推算曆數用南京日出分杪似相矛盾", ctx["direct_claims"])
        self.assertTrue(ctx["nanjing_sunrise_parameter_use_supported"])
        self.assertFalse(ctx["qishuo_meridian_explicitly_defined"])
        self.assertEqual(
            self.data["adjudication"]["nanjing_sunrise_parameter_as_qishuo_meridian_proof"],
            "FORBIDDEN",
        )


    def test_hongzhi_8_target_calendar_was_issued(self):
        ctx = self.contexts["MING-1494-ISSUE-HONGZHI-8-ALMANAC"]
        self.assertIn("弘治八年大統曆", ctx["record"])
        self.assertFalse(ctx["physical_copy_located"])
        self.assertEqual(
            ctx["inference_scope"],
            "ISSUANCE_CERTIFICATION_NOT_MONTH_START_VALUE_CERTIFICATION",
        )

    def test_hongzhi_8_eclipse_warning_has_causal_firewall(self):
        ctx = self.contexts["MING-1495-H8-LUNAR-ECLIPSE-NON-EVENT"]
        self.assertEqual(ctx["witness_period"], "LATER_MING")
        self.assertIn("月食不應", ctx["record"])
        self.assertFalse(ctx["qishuo_meridian_evidence"])
        self.assertEqual(
            self.data["adjudication"]["hongzhi_8_eclipse_failure_as_cause_of_month_7_qishuo_conflict"],
            "FORBIDDEN_WITHOUT_DIRECT_MECHANICAL_EVIDENCE",
        )

    def test_collection_negatives_are_scoped_not_global(self):
        nlc = self.contexts["COLLECTION-NLC-2007-MING-DATONG-FACSIMILES"]
        self.assertFalse(nlc["hongzhi_8_present"])
        self.assertFalse(nlc["hongzhi_10_present"])
        self.assertEqual(nlc["negative_evidence_scope"], "THIS_COLLECTION_ONLY")
        self.assertEqual(nlc["global_nonexistence_inference"], "FORBIDDEN")

        kyu = self.contexts["COLLECTION-KYUJANGGAK-MING-PRINTED-DATONG"]
        self.assertEqual(kyu["identified_year"], 1637)
        self.assertFalse(kyu["hongzhi_8_present_in_identified_ming_printed_holding"])
        self.assertFalse(kyu["hongzhi_10_present_in_identified_ming_printed_holding"])
        self.assertEqual(kyu["korea_wide_nonexistence_inference"], "FORBIDDEN")

        self.assertEqual(
            self.data["adjudication"]["search_result_absence_as_historical_nonexistence"],
            "FORBIDDEN",
        )

    def test_joseon_gift_is_transmission_lead_not_survival_proof(self):
        ctx = self.contexts["MING-1497-JOSEON-DATONG-GIFT"]
        self.assertIn("大統曆一百本", ctx["record"])
        self.assertEqual(
            ctx["specific_gift_copy_identity_with_hongzhi_10_target"],
            "UNRESOLVED",
        )
        self.assertEqual(ctx["survival_of_gifted_copies"], "UNRESOLVED")
        self.assertEqual(
            self.data["adjudication"]["joseon_gift_as_surviving_hongzhi_10_copy"],
            "UNRESOLVED_NOT_CERTIFIED",
        )


    def test_hongzhi_17_survival_control_is_not_target_year_certification(self):
        ctx = self.contexts["MING-1504-H17-SURVIVING-DATONG-ALMANAC"]
        self.assertEqual(ctx["gregorian_year"], 1504)
        self.assertEqual(ctx["title"], "大明弘治十七年歲次甲子大統曆")
        self.assertIn("欽天監刻本", ctx["edition"])
        self.assertEqual(ctx["holding_institution"], "北京市文物局")
        self.assertTrue(ctx["physical_survival_supported"])
        self.assertTrue(ctx["same_reign_as_targets"])
        self.assertFalse(ctx["hongzhi_8_target_copy_certified"])
        self.assertFalse(ctx["hongzhi_10_target_copy_certified"])
        self.assertEqual(
            self.data["adjudication"]["hongzhi_period_survival_as_hongzhi_8_or_10_target_certification"],
            "FORBIDDEN",
        )

if __name__ == "__main__":
    unittest.main()

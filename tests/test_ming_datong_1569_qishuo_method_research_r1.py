from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research" / "MING-DATONG-1569-QISHUO-METHOD-RESEARCH-R1.json"
ORACLE = ROOT / "tests" / "fixtures" / "ming-datong-1578-month-start-oracle-r1.json"


class MingDatong1569QishuoMethodResearchR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(RESEARCH.read_text(encoding="utf-8"))
        cls.oracle = json.loads(ORACLE.read_text(encoding="utf-8"))

    def test_d1_is_historically_adjudicated_but_general_runtime_remains_closed(self) -> None:
        self.assertEqual(self.data["schema"], "MING-DATONG-1569-QISHUO-METHOD-RESEARCH-R1")
        adjudication = self.data["historical_subrule_adjudication"]
        self.assertEqual(
            adjudication["winner_id"],
            "MING_DATONG_D1_SHOUSHI_STYLE_CHIJIXINGDU",
        )
        self.assertEqual(
            adjudication["status"],
            "HISTORICALLY_ADJUDICATED_FOR_MING_OFFICIAL_PRODUCTION",
        )
        self.assertEqual(
            adjudication["d2_disposition"],
            "LATER_RECEIVED_TEXT_VARIANT_NOT_EQUAL_PRODUCTION_CANDIDATE",
        )
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])

    def test_primary_facsimile_directly_closes_d1_divisor(self) -> None:
        primary = self.data["primary_facsimile_transcription"]
        self.assertEqual(primary["qishuo_volume_heading"]["text"], "步氣朔卷第一")
        d1 = primary["d1_direct_method"]
        self.assertEqual(d1["pdf_page_index_zero_based"], 32)
        self.assertEqual(d1["divisor_identity"], "CORRESPONDING_LUNAR_CHI_OR_JI_XINGDU")
        self.assertEqual(d1["candidate_id"], "MING_DATONG_D1_SHOUSHI_STYLE_CHIJIXINGDU")
        headings = {item["text"] for item in primary["verified_method_headings"]}
        self.assertIn("推遲疾差度分法", headings)
        self.assertIn("推加減差分法", headings)

    def test_ming_worked_example_corresponds_to_primary_d1(self) -> None:
        worked = self.data["corroborating_historical_witness"]
        self.assertEqual(worked["result"], "INDEPENDENTLY_CORROBORATES_D1")
        self.assertIn("迟行度一度一五二六", worked["normalized_mechanics"])

    def test_d2_is_preserved_as_received_variant_not_erased(self) -> None:
        d2 = self.data["contradicted_received_variant"]
        self.assertEqual(d2["candidate_id"], "MING_DATONG_D2_RECEIVED_TEXT_DINGXIANDU")
        self.assertEqual(
            d2["disposition"],
            "PRESERVED_FOR_TRANSMISSION_HISTORY_NOT_EQUAL_MING_PRODUCTION_CANDIDATE",
        )
        self.assertIn("定限度", d2["normalized_mechanics"])

    def test_modern_validation_is_supporting_not_primary_authority(self) -> None:
        validation = {item["source_id"]: item for item in self.data["modern_validation"]}
        observed = validation["EXT-YTLIU-MING-DATONG-CONJUNCTION-D1-D2"]["result"]
        self.assertIn("D1_REPORTED_56_OF_56", observed)
        self.assertIn("D2_MOSTLY_OUTSIDE", observed)
        self.assertTrue(self.oracle["months"])
        self.assertIn("SOURCE_DERIVED_D1_REPLAY_TO_1578_MONTH_START_ORACLE", self.data["unresolved_before_runtime"])
    
    def test_formula_semantics_artifact_refines_remaining_gates(self) -> None:
        self.assertEqual(
            self.data["formula_semantics_artifact"],
            "docs/research/MING-DATONG-1569-INTERPOLATION-REPLAY-R1.json",
        )
        self.assertEqual(
            self.data["formula_semantics_status"]["ming_d1_worked_replay"],
            "MACHINE_REPLAYED_AT_PRINTED_SOURCE_PRECISION",
        )
        unresolved = set(self.data["unresolved_before_runtime"])
        self.assertIn("QISHUO_GEOGRAPHIC_REFERENCE", unresolved)
        self.assertNotIn("HISTORICAL_DAY_BOUNDARY_AND_CLOCK_COORDINATE", unresolved)
        self.assertIn(
            "COMPLETE_1569_FULL_YINGSUO_CHIJI_TABLE_TRANSCRIPTION_AND_CROSS_EDITION_COLLATION",
            unresolved,
        )
        self.assertIn(
            "GENERALIZE_AND_VERIFY_SOURCE_PRECISION_RULES_ACROSS_FULL_1569_TABLE_REPLAY",
            unresolved,
        )


if __name__ == "__main__":
    unittest.main()

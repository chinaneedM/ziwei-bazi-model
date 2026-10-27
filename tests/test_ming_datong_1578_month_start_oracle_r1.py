from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "ming-datong-1578-month-start-oracle-r1.json"


class MingDatong1578MonthStartOracleR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_fixture_is_evidence_only_and_fail_closed(self) -> None:
        self.assertEqual(self.data["schema"], "MING-DATONG-1578-MONTH-START-ORACLE-R1")
        self.assertEqual(self.data["historical_context_id"], "MING-DATONG-CALENDAR-CONTEXT-R1")
        self.assertFalse(self.data["same_year_official_almanac_image_values_extracted"])
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])

    def test_complete_month_start_chain_matches_official_record_transcription(self) -> None:
        expected = ["癸丑", "壬午", "壬子", "壬午", "辛亥", "辛巳", "庚戌", "庚辰", "己酉", "戊寅", "戊申", "丁丑"]
        months = self.data["months"]
        self.assertEqual([item["month"] for item in months], list(range(1, 13)))
        self.assertEqual([item["start_ganzhi"] for item in months], expected)
        self.assertEqual(self.data["next_anchor"]["start_ganzhi"], "丁未")

    def test_month_lengths_are_recomputed_from_sexagenary_transitions(self) -> None:
        months = self.data["months"]
        expected_lengths = [29, 30, 30, 29, 30, 29, 30, 29, 29, 30, 29, 30]
        starts = [item["start_index"] for item in months] + [self.data["next_anchor"]["start_index"]]
        derived = [(starts[i + 1] - starts[i]) % 60 for i in range(12)]
        self.assertEqual(derived, expected_lengths)
        self.assertEqual([item["length_days"] for item in months], expected_lengths)
        self.assertTrue(all(length in (29, 30) for length in derived))
        self.assertEqual(sum(derived), 354)
        self.assertEqual(self.data["derived_year_length_days"], 354)

    def test_represented_year_is_twelve_consecutive_numbered_months_without_leap_label(self) -> None:
        self.assertFalse(self.data["represented_month_sequence_has_leap_month"])
        self.assertEqual(
            self.data["represented_month_sequence_basis"],
            "MONTH_LABELS_1_TO_12_ARE_CONSECUTIVE_AND_NEXT_ANCHOR_IS_WANLI_7_MONTH_1",
        )


if __name__ == "__main__":
    unittest.main()

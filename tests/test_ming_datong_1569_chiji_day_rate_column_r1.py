from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "docs" / "research" / "MING-DATONG-1569-CHIJI-DAY-RATE-COLUMN-R1.json"


class MingDatong1569ChijiDayRateColumnR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(TABLE.read_text(encoding="utf-8"))
        cls.rows = cls.data["rows"]

    def test_all_168_limits_are_present_in_order(self) -> None:
        self.assertEqual(len(self.rows), 168)
        self.assertEqual([row["limit"] for row in self.rows], list(range(1, 169)))
        self.assertEqual(self.data["invariants"]["row_count"], 168)

    def test_integer_reconstruction_matches_every_stored_row(self) -> None:
        previous = -1
        for row in self.rows:
            limit = row["limit"]
            raw_hundredths = limit * 82008
            printed = raw_hundredths // 100
            self.assertEqual(printed, row["printed_total_day_rate_source_units"])
            self.assertEqual(raw_hundredths % 100, row["dropped_hundredths"])
            self.assertEqual(printed // 10000, row["printed_days"])
            self.assertEqual(
                f"{printed % 10000:04d}",
                row["printed_source_fraction"],
            )
            self.assertGreater(printed, previous)
            previous = printed

    def test_primary_page_partition_covers_each_limit_once(self) -> None:
        expected = {}
        for item in self.data["page_row_ranges"]:
            start, end = item["limits"]
            for limit in range(start, end + 1):
                self.assertNotIn(limit, expected)
                expected[limit] = item["page"]
        self.assertEqual(set(expected), set(range(1, 169)))
        for row in self.rows:
            self.assertEqual(row["primary_pdf_page_index_zero_based"], expected[row["limit"]])

    def test_key_primary_and_worked_example_controls(self) -> None:
        by_limit = {row["limit"]: row for row in self.rows}
        self.assertEqual(
            (by_limit[1]["printed_days"], by_limit[1]["printed_source_fraction"]),
            (0, "0820"),
        )
        self.assertEqual(
            (by_limit[7]["printed_days"], by_limit[7]["printed_source_fraction"]),
            (0, "5740"),
        )
        self.assertEqual(
            (by_limit[13]["printed_days"], by_limit[13]["printed_source_fraction"]),
            (1, "0661"),
        )
        self.assertEqual(
            (by_limit[116]["printed_days"], by_limit[116]["printed_source_fraction"]),
            (9, "5129"),
        )
        self.assertEqual(
            (by_limit[168]["printed_days"], by_limit[168]["printed_source_fraction"]),
            (13, "7773"),
        )

    def test_820_08_day_rate_increment_stays_separate_from_820_interpolation_divisor(self) -> None:
        rule = self.data["reconstruction_rule"]
        self.assertEqual(rule["nominal_day_rate_increment_source_units"], "820.08")
        self.assertIn("820, not this 820.08", rule["distinction_from_interpolation_denominator"])
        self.assertEqual(
            self.data["epistemic_firewalls"]["table_day_rate_increment_as_interpolation_denominator"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["derived_column_as_verbatim_full_table_transcription"],
            "FORBIDDEN",
        )

    def test_received_820_summary_does_not_overwrite_primary_820_08_rows(self) -> None:
        conflict = self.data["cross_edition_conflict"]
        controls = {item["limit"]: item for item in conflict["decisive_primary_controls"]}
        self.assertEqual(controls[13]["primary_printed_total"], 10661)
        self.assertEqual(controls[13]["floor_limit_times_820_08"], 10661)
        self.assertEqual(controls[13]["limit_times_received_820"], 10660)
        self.assertEqual(controls[116]["primary_printed_total"], 95129)
        self.assertEqual(controls[116]["limit_times_received_820"], 95120)
        self.assertEqual(controls[168]["primary_printed_total"], 137773)
        self.assertEqual(controls[168]["limit_times_received_820"], 137760)
        self.assertEqual(
            conflict["received_witness"]["disposition"],
            "PRESERVE_AS_RECEIVED_TRANSMISSION_VARIANT_NOT_AS_1569_PRINTED_TABLE_GENERATOR",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["received_820_summary_as_1569_printed_day_rate_generator"],
            "FORBIDDEN",
        )


if __name__ == "__main__":
    unittest.main()

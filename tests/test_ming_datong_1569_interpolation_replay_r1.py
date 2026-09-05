from __future__ import annotations

import json
import unittest
from decimal import Decimal, ROUND_DOWN, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPLAY = ROOT / "docs" / "research" / "MING-DATONG-1569-INTERPOLATION-REPLAY-R1.json"


class MingDatong1569InterpolationReplayR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        getcontext().prec = 40
        cls.data = json.loads(REPLAY.read_text(encoding="utf-8"))
        cls.worked = cls.data["ming_worked_d1_replay"]

    def test_research_firewall_and_formula_pages(self) -> None:
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])
        pages = self.data["primary_formula_pages"]
        self.assertEqual(pages["solar_yingsuo_limit_and_interpolation"]["pdf_page_index_zero_based"], 13)
        self.assertEqual(pages["lunar_chiji_history_and_row_interpolation"]["pdf_page_index_zero_based"], 24)
        self.assertEqual(pages["d1_conjunction_correction"]["pdf_page_index_zero_based"], 32)
        self.assertFalse(pages["d1_conjunction_correction"]["received_d2_subtraction_of_820_used"])
        self.assertFalse(pages["lunar_chiji_xingdu_table"]["full_numeric_transcription_complete"])

    def test_source_day_radix_and_limit_width_are_not_modern_time_units(self) -> None:
        radix = self.data["source_radices"]
        self.assertEqual(Decimal(radix["day_source_units_per_day"]), Decimal("10000"))
        self.assertEqual(Decimal(radix["lunar_table_day_rate_increment_source_units"]), Decimal("820.08"))\n        self.assertEqual(Decimal(radix["lunar_interpolation_denominator_source_units"]), Decimal("820"))
        self.assertEqual(
            self.data["epistemic_firewalls"]["modern_decimal_as_historical_notation"],
            "FORBIDDEN",
        )

    def test_lunar_interpolation_replays_ming_worked_example(self) -> None:
        w = self.worked
        target_units = Decimal(w["chiji_history"]["days"]) * Decimal("10000") + Decimal(
            w["chiji_history"]["source_fraction"]
        )
        row_units = Decimal(w["selected_row_day_rate"]["days"]) * Decimal("10000") + Decimal(
            w["selected_row_day_rate"]["source_fraction"]
        )
        residual = target_units - row_units
        self.assertEqual(residual, Decimal(w["residual_source_units"]))

        loss_in_source_fen = (
            residual
            * Decimal(w["selected_row_loss_gain_source_fen"])
            / Decimal(self.data["source_radices"]["lunar_interpolation_denominator_source_units"])
        )
        self.assertEqual(
            loss_in_source_fen,
            Decimal(w["raw_within_limit_loss_source_fen"]),
        )

        loss_in_degree = loss_in_source_fen / Decimal("100")
        self.assertEqual(
            loss_in_degree,
            Decimal(w["raw_within_limit_loss_degree"]),
        )

        raw_chiji = Decimal(w["selected_row_accumulated_chiji_degree"]) - loss_in_degree
        printed_chiji = raw_chiji.quantize(Decimal("0.000001"), rounding=ROUND_DOWN)
        self.assertEqual(printed_chiji, Decimal(w["printed_chiji_difference_degree"]))

    def test_d1_division_truncation_and_day_carry_replay_exactly(self) -> None:
        w = self.worked
        combined = Decimal(w["printed_chiji_difference_degree"]) - Decimal(
            w["yingsuo_difference_degree"]
        )
        self.assertEqual(combined, Decimal(w["combined_difference_degree"]))

        raw_add = (
            combined
            * Decimal(w["d1_multiplier"])
            / Decimal(w["corresponding_chi_xingdu_degree"])
        )
        self.assertEqual(raw_add, Decimal(w["raw_add_correction_source_units"]))

        printed_add = raw_add.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        self.assertEqual(printed_add, Decimal(w["printed_add_correction_source_units"]))

        true_units = Decimal(w["mean_conjunction_source_units"]) + printed_add
        self.assertEqual(true_units, Decimal(w["true_conjunction_source_units"]))

        day_radix = Decimal(self.data["source_radices"]["day_source_units_per_day"])
        day_carry = int(true_units // day_radix)
        small_remainder = true_units - day_radix * day_carry
        self.assertEqual(day_carry, w["day_carry_count"])
        self.assertEqual(
            small_remainder,
            Decimal(w["true_conjunction_small_remainder_source_units"]),
        )

    def test_observed_truncation_is_not_promoted_to_universal_rule(self) -> None:
        self.assertEqual(
            self.data["epistemic_firewalls"]["worked_example_truncation_as_universal_precision_rule"],
            "NOT_YET_AUTHORIZED",
        )
        self.assertIn(
            "GENERALIZE_AND_VERIFY_SOURCE_PRECISION_RULES_ACROSS_FULL_1569_TABLE_REPLAY",
            self.data["remaining_gates"],
        )


if __name__ == "__main__":
    unittest.main()

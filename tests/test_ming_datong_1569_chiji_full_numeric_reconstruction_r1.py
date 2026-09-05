from __future__ import annotations

import json
import unittest
from decimal import Decimal, ROUND_CEILING, ROUND_DOWN
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "docs" / "research" / "MING-DATONG-1569-CHIJI-FULL-NUMERIC-RECONSTRUCTION-R1.json"


class MingDatong1569ChijiFullNumericReconstructionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(FULL.read_text(encoding="utf-8"))
        cls.rows = {row["limit"]: row for row in cls.data["rows"]}

    def test_row_domain_and_firewall(self) -> None:
        self.assertEqual(len(self.rows), 169)
        self.assertEqual(set(self.rows), set(range(169)))
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])
        self.assertEqual(
            self.data["epistemic_firewalls"]["full_numeric_reconstruction_as_verbatim_primary_transcription"],
            "FORBIDDEN",
        )

    def test_three_difference_formula_reconstructs_generic_initial_side(self) -> None:
        D = Decimal("0.11110000")
        P = Decimal("0.00028100")
        L = Decimal("0.00000325")
        for n in range(0, 83):
            N = Decimal(n)
            expected = N * (D - N * (P + N * L))
            stored = Decimal(self.rows[n]["accumulated_chiji_degree"] or "0")
            self.assertEqual(expected, stored, n)

    def test_terminal_side_mirrors_initial_side_outside_central_block(self) -> None:
        for n in range(86, 169):
            left = Decimal(self.rows[168 - n]["accumulated_chiji_degree"] or "0")
            right = Decimal(self.rows[n]["accumulated_chiji_degree"] or "0")
            self.assertEqual(left, right, n)

    def test_central_primary_overrides_and_sign_boundary(self) -> None:
        self.assertEqual(self.rows[83]["accumulated_chiji_degree"], "5.42916616")
        self.assertEqual(self.rows[84]["accumulated_chiji_degree"], "5.42934424")
        self.assertEqual(self.rows[85]["accumulated_chiji_degree"], "5.42916616")
        self.assertEqual(self.rows[83]["loss_gain_sign"], "益")
        self.assertEqual(self.rows[84]["loss_gain_sign"], "損")
        self.assertEqual(self.rows[83]["loss_gain_source_fen"], "0.017808")
        self.assertEqual(self.rows[84]["loss_gain_source_fen"], "0.017808")

    def test_every_loss_gain_is_adjacent_accumulated_difference(self) -> None:
        for n in range(0, 168):
            here = Decimal(self.rows[n]["accumulated_chiji_degree"] or "0")
            nxt = Decimal(self.rows[n + 1]["accumulated_chiji_degree"] or "0")
            expected_fen = abs(nxt - here) * Decimal("100")
            self.assertEqual(
                expected_fen,
                Decimal(self.rows[n]["loss_gain_source_fen"]),
                n,
            )

    def test_generic_line_speed_rule_and_central_overrides(self) -> None:
        mean = Decimal("1.09623750")
        quantum = Decimal("0.0001")
        for n in range(0, 168):
            row = self.rows[n]
            adjustment = Decimal(row["loss_gain_degree"])
            if n <= 83:
                chi_raw, ji_raw = mean - adjustment, mean + adjustment
            else:
                chi_raw, ji_raw = mean + adjustment, mean - adjustment
            chi = chi_raw.quantize(quantum, rounding=ROUND_CEILING)
            ji = ji_raw.quantize(quantum, rounding=ROUND_CEILING)
            if n == 82:
                chi = Decimal("1.0960")
            if n == 85:
                ji = Decimal("1.0960")
            self.assertEqual(chi, Decimal(row["chi_xingdu_degree"]), n)
            self.assertEqual(ji, Decimal(row["ji_xingdu_degree"]), n)

    def test_loss_gain_shortcut_column_uses_820_and_truncates(self) -> None:
        for n in range(0, 168):
            row = self.rows[n]
            loss = Decimal(row["loss_gain_source_fen"])
            expected = (loss * Decimal("100") / Decimal("820")).quantize(
                Decimal("0.0001"), rounding=ROUND_DOWN
            )
            self.assertEqual(expected, Decimal(row["loss_gain_shortcut_source_seconds"]), n)
        self.assertIsNone(self.rows[168]["loss_gain_shortcut_source_seconds"])

    def test_loss_gain_shortcut_primary_controls(self) -> None:
        self.assertEqual(self.rows[0]["loss_gain_shortcut_source_seconds"], "1.3514")
        self.assertEqual(self.rows[1]["loss_gain_shortcut_source_seconds"], "1.3443")
        self.assertEqual(self.rows[83]["loss_gain_shortcut_source_seconds"], "0.0021")
        self.assertEqual(self.rows[84]["loss_gain_shortcut_source_seconds"], "0.0021")
        self.assertEqual(self.rows[167]["loss_gain_shortcut_source_seconds"], "1.3514")
        self.assertIsNone(self.rows[168]["loss_gain_shortcut_source_seconds"])

    def test_worked_example_limit_116_is_exactly_present(self) -> None:
        row = self.rows[116]
        self.assertEqual(row["day_rate_days"], 9)
        self.assertEqual(row["day_rate_source_fraction"], "5129")
        self.assertEqual(row["accumulated_chiji_degree"], "4.56040000")
        self.assertEqual(row["loss_gain_source_fen"], "5.629675")
        self.assertEqual(row["chi_xingdu_degree"], "1.1526")
        self.assertEqual(row["ji_xingdu_degree"], "1.0400")

    def test_xingdu_shortcut_columns_use_fixed_point_reciprocal(self) -> None:
        quantum = Decimal("0.0000001")
        for n in range(0, 168):
            row = self.rows[n]
            ji_int = int(Decimal(row["ji_xingdu_degree"]) * Decimal("10000"))
            chi_int = int(Decimal(row["chi_xingdu_degree"]) * Decimal("10000"))
            ji = (Decimal("820") / Decimal(ji_int)).quantize(quantum, rounding=ROUND_DOWN)
            chi = (Decimal("820") / Decimal(chi_int)).quantize(quantum, rounding=ROUND_DOWN)
            self.assertEqual(ji, Decimal(row["ji_xingdu_shortcut_source_ratio"]), n)
            self.assertEqual(chi, Decimal(row["chi_xingdu_shortcut_source_ratio"]), n)
        self.assertIsNone(self.rows[168]["ji_xingdu_shortcut_source_ratio"])
        self.assertIsNone(self.rows[168]["chi_xingdu_shortcut_source_ratio"])

    def test_xingdu_shortcut_primary_controls(self) -> None:
        self.assertEqual(self.rows[0]["ji_xingdu_shortcut_source_ratio"], "0.0679314")
        self.assertEqual(self.rows[0]["chi_xingdu_shortcut_source_ratio"], "0.0832064")
        self.assertEqual(self.rows[83]["ji_xingdu_shortcut_source_ratio"], "0.0747834")
        self.assertEqual(self.rows[83]["chi_xingdu_shortcut_source_ratio"], "0.0748106")
        self.assertEqual(self.rows[84]["ji_xingdu_shortcut_source_ratio"], "0.0748106")
        self.assertEqual(self.rows[84]["chi_xingdu_shortcut_source_ratio"], "0.0747834")
        self.assertEqual(self.rows[167]["ji_xingdu_shortcut_source_ratio"], "0.0832064")
        self.assertEqual(self.rows[167]["chi_xingdu_shortcut_source_ratio"], "0.0679314")

    def test_primary_row_124_quarantines_cross_witness_anomaly(self) -> None:
        row = self.rows[124]
        self.assertEqual(row["chi_xingdu_degree"], "1.1645")
        self.assertEqual(row["ji_xingdu_degree"], "1.0281")
        anomaly = self.data["cross_regional_controls"]["quarantined_anomaly"]
        self.assertEqual(anomaly["limit"], 124)
        self.assertEqual(anomaly["goryeosa_current_digital_value_ji_xingdu"], "1.0821")
        self.assertEqual(anomaly["reconstructed_and_1569_primary_value_ji_xingdu"], "1.0281")
        self.assertEqual(anomaly["previous_project_transcription"], "0.0821")
        self.assertEqual(anomaly["previous_project_transcription_status"], "CORRECTED_PROJECT_METADATA_ERROR_NOT_SOURCE_VALUE")
        self.assertEqual(anomaly["status"], "CROSS_WITNESS_VARIANT_DO_NOT_PROPAGATE")

    def test_terminal_limit_has_day_rate_but_no_next_interval_values(self) -> None:
        row = self.rows[168]
        self.assertEqual(row["day_rate_days"], 13)
        self.assertEqual(row["day_rate_source_fraction"], "7773")
        self.assertIsNone(row["accumulated_chiji_degree"])
        self.assertIsNone(row["loss_gain_source_fen"])
        self.assertIsNone(row["chi_xingdu_degree"])
        self.assertIsNone(row["ji_xingdu_degree"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSITION = ROOT / "docs" / "research" / "MING-DATONG-1569-CHIJI-CENTRAL-TRANSITION-R1.json"
DAY_RATE = ROOT / "docs" / "research" / "MING-DATONG-1569-CHIJI-DAY-RATE-COLUMN-R1.json"


class MingDatong1569ChijiCentralTransitionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(TRANSITION.read_text(encoding="utf-8"))
        cls.rows = {row["limit"]: row for row in cls.data["rows"]}
        day = json.loads(DAY_RATE.read_text(encoding="utf-8"))
        cls.day_rows = {row["limit"]: row for row in day["rows"]}

    def test_primary_transition_boundary_is_83_yi_then_84_sun(self) -> None:
        self.assertEqual(self.data["transition_semantics"]["last_yi_limit"], 83)
        self.assertEqual(self.data["transition_semantics"]["first_sun_limit"], 84)
        self.assertEqual(self.rows[83]["loss_gain_sign"], "益")
        self.assertEqual(self.rows[84]["loss_gain_sign"], "損")
        self.assertEqual(
            self.data["transition_semantics"]["generic_same_sign_recurrence_across_83_84"],
            "FORBIDDEN",
        )

    def test_central_day_rates_match_full_day_rate_artifact(self) -> None:
        for limit in range(81, 87):
            self.assertEqual(
                self.rows[limit]["day_rate_total_source_units"],
                self.day_rows[limit]["printed_total_day_rate_source_units"],
            )

    def test_limit_84_is_peak_and_83_84_adjustments_are_symmetric(self) -> None:
        r83 = self.rows[83]
        r84 = self.rows[84]
        r85 = self.rows[85]
        adjustment_degree = Decimal(r83["loss_gain_source_fen"]) / Decimal("100")
        self.assertEqual(adjustment_degree, Decimal("0.00017808"))
        self.assertEqual(
            Decimal(r83["accumulated_chiji_degree"]) + adjustment_degree,
            Decimal(r84["accumulated_chiji_degree"]),
        )
        self.assertEqual(
            Decimal(r84["accumulated_chiji_degree"]) - adjustment_degree,
            Decimal(r85["accumulated_chiji_degree"]),
        )
        self.assertGreater(
            Decimal(r84["accumulated_chiji_degree"]),
            Decimal(r83["accumulated_chiji_degree"]),
        )
        self.assertEqual(
            self.data["transition_semantics"]["peak_accumulated_chiji_degree_limit"],
            84,
        )

    def test_d1_chi_ji_divisor_pair_swaps_at_transition(self) -> None:
        pair83 = self.data["transition_semantics"]["d1_divisor_selection"]["limit_83"]
        pair84 = self.data["transition_semantics"]["d1_divisor_selection"]["limit_84"]
        self.assertEqual(pair83["遲"], "1.0961")
        self.assertEqual(pair83["疾"], "1.0965")
        self.assertEqual(pair84["遲"], "1.0965")
        self.assertEqual(pair84["疾"], "1.0961")
        self.assertEqual(pair83["遲"], pair84["疾"])
        self.assertEqual(pair83["疾"], pair84["遲"])

    def test_symmetry_window_around_central_peak(self) -> None:
        self.assertEqual(self.rows[83]["accumulated_chiji_degree"], self.rows[85]["accumulated_chiji_degree"])
        self.assertEqual(self.rows[82]["accumulated_chiji_degree"], self.rows[86]["accumulated_chiji_degree"])
        self.assertEqual(self.rows[82]["loss_gain_source_fen"], self.rows[85]["loss_gain_source_fen"])
        self.assertEqual(self.rows[81]["loss_gain_source_fen"], self.rows[86]["loss_gain_source_fen"])

    def test_cross_regional_and_later_controls_never_replace_primary(self) -> None:
        self.assertEqual(
            self.data["epistemic_firewalls"]["goryeosa_as_ming_1569_authority"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["later_qing_exegesis_as_primary_table_replacement"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["transition_closure_as_full_168_row_table_transcription"],
            "FORBIDDEN",
        )
        self.assertFalse(self.data["runtime_selection_authorized"])


if __name__ == "__main__":
    unittest.main()

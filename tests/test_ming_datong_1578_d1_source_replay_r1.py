from __future__ import annotations

import json
import unittest
from decimal import Decimal, ROUND_DOWN
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPLAY = ROOT / "docs" / "research" / "MING-DATONG-1578-D1-SOURCE-REPLAY-R1.json"
ORACLE = ROOT / "tests" / "fixtures" / "ming-datong-1578-month-start-oracle-r1.json"
SOLAR = ROOT / "docs" / "research" / "MING-DATONG-1569-YINGSUO-FULL-NUMERIC-RECONSTRUCTION-R1.json"
LUNAR = ROOT / "docs" / "research" / "MING-DATONG-1569-CHIJI-FULL-NUMERIC-RECONSTRUCTION-R1.json"


class MingDatong1578D1SourceReplayR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REPLAY.read_text(encoding="utf-8"))
        cls.oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        solar = json.loads(SOLAR.read_text(encoding="utf-8"))
        cls.solar = {item["family_id"]: {row["day_index"]: row for row in item["rows"]} for item in solar["families"]}
        lunar = json.loads(LUNAR.read_text(encoding="utf-8"))
        cls.lunar = {row["limit"]: row for row in lunar["rows"]}

    def test_source_anchor_recomputes_exactly(self) -> None:
        c = self.data["source_constants"]
        distance = Decimal(c["target_year_distance"])
        middle = distance * Decimal(c["year_source_units"])
        self.assertEqual(middle, Decimal("1084770225"))
        winter = (middle + Decimal(c["qi_response_source_units"])) % Decimal(c["ji_fa_source_units"])
        run = (middle + Decimal(c["run_response_source_units"])) % Decimal(c["shuo_source_units"])
        mean = (winter - run) % Decimal(c["ji_fa_source_units"])
        suo = Decimal(c["half_year_source_units"]) - run
        zraw = (middle + Decimal(c["zhuan_response_source_units"]) - run) % Decimal(c["zhuan_end_source_units"])
        self.assertEqual(winter, Decimal("520825"))
        self.assertEqual(run, Decimal("18288.18"))
        self.assertEqual(mean, Decimal("502536.82"))
        self.assertEqual(suo, Decimal("1807924.32"))
        self.assertEqual(zraw, Decimal("57539.82"))

    def _solar_difference(self, state: str, history: Decimal) -> Decimal:
        c = self.data["source_constants"]
        half = Decimal(c["half_year_source_units"])
        a_cut = Decimal(c["yingsuo_cutoffs"]["ying_initial_suo_terminal"])
        b_cut = Decimal(c["yingsuo_cutoffs"]["suo_initial_ying_terminal"])
        if state == "盈":
            family = "YING_INITIAL_SUO_TERMINAL" if history <= a_cut else "SUO_INITIAL_YING_TERMINAL"
            x = history if history <= a_cut else half - history
        else:
            family = "SUO_INITIAL_YING_TERMINAL" if history <= b_cut else "YING_INITIAL_SUO_TERMINAL"
            x = history if history <= b_cut else half - history
        day = int(x // Decimal("10000"))
        rem = x - Decimal(day) * Decimal("10000")
        row = self.solar[family][day]
        accumulated = Decimal(row["accumulated_degree"] or "0")
        add = Decimal(row["add_degree"])
        return accumulated + rem / Decimal("10000") * add

    def _lunar_difference_and_divisor(self, state: str, history: Decimal) -> tuple[Decimal, Decimal, int]:
        selected = 0
        for limit in range(1, 169):
            rate = self.lunar[limit]["day_rate_total_source_units"]
            if rate is not None and Decimal(rate) <= history:
                selected = limit
            else:
                break
        row = self.lunar[selected]
        rate = Decimal(row["day_rate_total_source_units"] or "0")
        rem = history - rate
        accumulated = Decimal(row["accumulated_chiji_degree"] or "0")
        loss_gain = Decimal(row["loss_gain_degree"])
        if row["loss_gain_sign"] == "益":
            difference = accumulated + rem * loss_gain / Decimal("820")
        else:
            difference = accumulated - rem * loss_gain / Decimal("820")
        divisor = Decimal(row["chi_xingdu_degree"] if state == "迟" else row["ji_xingdu_degree"])
        return difference, divisor, selected

    def test_all_13_conjunctions_recompute_from_reconstructed_primary_tables(self) -> None:
        for month in self.data["months"]:
            solar = self._solar_difference(month["solar_state"], Decimal(month["solar_history"]))
            lunar, divisor, limit = self._lunar_difference_and_divisor(
                month["lunar_state"], Decimal(month["lunar_history"])
            )
            self.assertEqual(solar.quantize(Decimal("0.000000000001")), Decimal(month["solar_difference_degree"]))
            self.assertEqual(lunar.quantize(Decimal("0.000000000001")), Decimal(month["lunar_difference_degree"]))
            self.assertEqual(divisor, Decimal(month["d1_divisor"]))
            self.assertEqual(limit, month["lunar_limit"])

            signed = (solar if month["solar_state"] == "盈" else -solar) + (
                lunar if month["lunar_state"] == "迟" else -lunar
            )
            raw = signed * Decimal("820") / divisor
            printed = raw.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            true = (Decimal(month["mean_conjunction"]) + printed) % Decimal("600000")
            index = int(true // Decimal("10000"))

            self.assertEqual(signed.quantize(Decimal("0.000000000001")), Decimal(month["signed_combined_degree"]))
            self.assertEqual(raw.quantize(Decimal("0.000000000001")), Decimal(month["correction_raw"]))
            self.assertEqual(printed, Decimal(month["correction_print"]))
            self.assertEqual(true, Decimal(month["true_conjunction"]))
            self.assertEqual(index, month["index"])

    def test_complete_official_record_oracle_chain_matches_13_of_13(self) -> None:
        expected = [item["start_index"] for item in self.oracle["months"]]
        expected.append(self.oracle["next_anchor"]["start_index"])
        observed = [item["index"] for item in self.data["months"]]
        self.assertEqual(observed, expected)
        self.assertEqual(observed, [49, 18, 48, 18, 47, 17, 46, 16, 45, 14, 44, 13, 43])
        self.assertEqual(self.data["oracle_result"]["mismatch_count"], 0)
        self.assertEqual(self.data["oracle_result"]["total_compared_month_starts"], 13)

    def test_month_start_ganzhi_chain_matches_oracle_names(self) -> None:
        expected = [item["start_ganzhi"] for item in self.oracle["months"]]
        expected.append(self.oracle["next_anchor"]["start_ganzhi"])
        self.assertEqual([item["ganzhi"] for item in self.data["months"]], expected)

    def test_day_labels_are_robust_to_unresolved_subunit_precision_policy(self) -> None:
        margins = [Decimal(item["boundary_margin_source_units"]) for item in self.data["months"]]
        self.assertEqual(min(margins), Decimal("197.31"))
        self.assertGreater(min(margins), Decimal("0.01"))
        self.assertEqual(
            self.data["oracle_result"]["precision_sensitivity_conclusion"],
            "DAY_LABEL_RESULT_IS_NOT_SENSITIVE_TO_SUB_0_01_SOURCE_UNIT_TRUNCATION_UNCERTAINTY_IN_THIS_1578_CHAIN",
        )

    def test_day_level_success_does_not_overclaim_physical_almanac_or_runtime(self) -> None:
        fw = self.data["epistemic_firewalls"]
        self.assertEqual(fw["official_reign_record_as_physical_1578_almanac_substitute"], "FORBIDDEN")
        self.assertEqual(fw["day_level_match_as_exact_conjunction_time_certification"], "FORBIDDEN")
        self.assertEqual(fw["geographic_reference_inference_from_day_match"], "FORBIDDEN")
        self.assertEqual(fw["runtime_activation_from_single_year_replay"], "FORBIDDEN")
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])


if __name__ == "__main__":
    unittest.main()

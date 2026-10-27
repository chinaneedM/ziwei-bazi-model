from pathlib import Path
import unittest
from unittest.mock import patch

from fortune_training.contamination_relay import (
    NON_EXECUTED_STATUS,
    PACKET_SCHEMA,
    RESOLVE_CURRENT_ROUND,
    parse_contamination_report,
    process_contamination_report,
)
from fortune_training.formal import (
    PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
    PREDICTION_CANONICAL_RUNTIME_READ_GATE_FAILURE,
    PREDICTION_CONTEXT_VIOLATION,
    PRE_FREEZE_RUNTIME_GATE_FAILED_NOT_EXECUTED,
)
from fortune_training.util import TrainingError


class ContaminationRelayRegressionTests(unittest.TestCase):
    def test_issue_137_administrative_form_parses_without_training_packet_json(self):
        report = parse_contamination_report(
            "\n".join(
                (
                    "round_id: FORMAL-ROUND-026",
                    "case_id: CASE-006",
                    f"status: {NON_EXECUTED_STATUS}",
                    "reason: "
                    "PREDICTION_ACCESS_CONTRACT_NOT_EXECUTED_BEFORE_REPOSITORY_READ",
                )
            )
        )
        self.assertEqual(
            report,
            {
                "schema": PACKET_SCHEMA,
                "round_id": "FORMAL-ROUND-026",
                "case_id": "CASE-006",
                "reason": PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
            },
        )

    def test_administrative_form_rejects_extra_or_prediction_fields(self):
        body = "\n".join(
            (
                "round_id: FORMAL-ROUND-026",
                "case_id: CASE-006",
                f"status: {NON_EXECUTED_STATUS}",
                "reason: "
                "PREDICTION_ACCESS_CONTRACT_NOT_EXECUTED_BEFORE_REPOSITORY_READ",
                "top1: A",
            )
        )
        with self.assertRaises(TrainingError):
            parse_contamination_report(body)

    def test_issue_139_header_with_explanatory_prose_resolves_current_round(self):
        body = "\n".join(
            (
                f"round_id: {RESOLVE_CURRENT_ROUND}",
                "case_id: CASE-006",
                f"status: {NON_EXECUTED_STATUS}",
                "reason: "
                "PREDICTION_ACCESS_CONTRACT_NOT_EXECUTED_BEFORE_REPOSITORY_READ",
                "",
                "Contamination scope:",
                "- GitHub repository search happened before contract execution.",
                "- No case materials, answers, or prior predictions were read.",
                "",
                "Required controller actions:",
                "1. Resolve the current round from main.",
                "2. Preserve strict first-blind eligibility.",
                "",
                "Expected result: NOT_EXECUTED; clean replacement round required.",
            )
        )
        report = parse_contamination_report(body)
        self.assertEqual(report["round_id"], RESOLVE_CURRENT_ROUND)
        self.assertEqual(report["case_id"], "CASE-006")
        self.assertEqual(
            report["reason"],
            PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
        )

        expected = {"next_round_id": "FORMAL-ROUND-028"}
        with (
            patch(
                "fortune_training.contamination_relay.load_json",
                return_value={
                    "round_id_prefix": "FORMAL-ROUND",
                    "round_sequence": 26,
                },
            ),
            patch(
                "fortune_training.contamination_relay."
                "invalidate_current_pre_freeze_round",
                return_value=expected,
            ) as invalidate,
            patch(
                "fortune_training.contamination_relay.quarantine_current_case"
            ) as quarantine,
        ):
            self.assertEqual(
                process_contamination_report(Path("."), report),
                expected,
            )
        invalidate.assert_called_once_with(
            Path("."),
            "FORMAL-ROUND-027",
            "CASE-006",
            reason=PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
        )
        quarantine.assert_not_called()

    def test_administrative_prose_rejects_machine_prediction_fields(self):
        body = "\n".join(
            (
                "round_id: FORMAL-ROUND-027",
                "case_id: CASE-006",
                f"status: {NON_EXECUTED_STATUS}",
                "reason: "
                "PREDICTION_ACCESS_CONTRACT_NOT_EXECUTED_BEFORE_REPOSITORY_READ",
                "",
                "top1: A",
            )
        )
        with self.assertRaises(TrainingError):
            parse_contamination_report(body)

    def test_current_round_placeholder_cannot_quarantine_a_case(self):
        report = {
            "schema": PACKET_SCHEMA,
            "round_id": RESOLVE_CURRENT_ROUND,
            "case_id": "CASE-006",
            "reason": PREDICTION_CONTEXT_VIOLATION,
        }
        with self.assertRaises(TrainingError):
            process_contamination_report(Path("."), report)

    def test_startup_order_violation_invalidates_round_without_quarantining_case(self):
        report = {
            "schema": PACKET_SCHEMA,
            "round_id": "FORMAL-ROUND-026",
            "case_id": "CASE-006",
            "reason": PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
        }
        expected = {"next_round_id": "FORMAL-ROUND-027"}
        with (
            patch(
                "fortune_training.contamination_relay."
                "invalidate_current_pre_freeze_round",
                return_value=expected,
            ) as invalidate,
            patch(
                "fortune_training.contamination_relay.quarantine_current_case"
            ) as quarantine,
        ):
            self.assertEqual(
                process_contamination_report(Path("."), report),
                expected,
            )
        invalidate.assert_called_once_with(
            Path("."),
            "FORMAL-ROUND-026",
            "CASE-006",
            reason=PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
        )
        quarantine.assert_not_called()

    def test_runtime_gate_failure_invalidates_round_without_contaminating_case(self):
        body = "\n".join(
            (
                "round_id: FORMAL-ROUND-031",
                "case_id: CASE-057",
                f"status: {PRE_FREEZE_RUNTIME_GATE_FAILED_NOT_EXECUTED}",
                f"reason: {PREDICTION_CANONICAL_RUNTIME_READ_GATE_FAILURE}",
            )
        )
        report = parse_contamination_report(body)
        expected = {"next_round_id": "FORMAL-ROUND-032"}
        with (
            patch(
                "fortune_training.contamination_relay."
                "invalidate_current_pre_freeze_round",
                return_value=expected,
            ) as invalidate,
            patch(
                "fortune_training.contamination_relay.quarantine_current_case"
            ) as quarantine,
        ):
            self.assertEqual(
                process_contamination_report(Path("."), report),
                expected,
            )
        invalidate.assert_called_once_with(
            Path("."),
            "FORMAL-ROUND-031",
            "CASE-057",
            reason=PREDICTION_CANONICAL_RUNTIME_READ_GATE_FAILURE,
        )
        quarantine.assert_not_called()

    def test_allowlist_violation_still_quarantines_case(self):
        report = {
            "schema": PACKET_SCHEMA,
            "round_id": "FORMAL-ROUND-026",
            "case_id": "CASE-006",
            "reason": PREDICTION_CONTEXT_VIOLATION,
        }
        expected = {"next_case_id": "CASE-007"}
        with (
            patch(
                "fortune_training.contamination_relay.quarantine_current_case",
                return_value=expected,
            ) as quarantine,
            patch(
                "fortune_training.contamination_relay."
                "invalidate_current_pre_freeze_round"
            ) as invalidate,
        ):
            self.assertEqual(
                process_contamination_report(Path("."), report),
                expected,
            )
        quarantine.assert_called_once_with(
            Path("."),
            "FORMAL-ROUND-026",
            "CASE-006",
            reason=PREDICTION_CONTEXT_VIOLATION,
        )
        invalidate.assert_not_called()


if __name__ == "__main__":
    unittest.main()

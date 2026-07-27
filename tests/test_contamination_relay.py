from pathlib import Path
import unittest
from unittest.mock import patch

from fortune_training.contamination_relay import (
    NON_EXECUTED_STATUS,
    PACKET_SCHEMA,
    parse_contamination_report,
    process_contamination_report,
)
from fortune_training.formal import (
    PREDICTION_ACCESS_STARTUP_ORDER_VIOLATION,
    PREDICTION_CONTEXT_VIOLATION,
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

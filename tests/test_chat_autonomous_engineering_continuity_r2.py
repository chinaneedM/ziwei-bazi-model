from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "chat-input" / "session-recovery-contract.json"
STATE_PATH = ROOT / "chat-input" / "work-session-state.json"


class ChatAutonomousEngineeringContinuityR2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

    def test_live_github_state_precedes_checkpoint_and_chat_memory(self) -> None:
        self.assertEqual("CHAT_SESSION_RECOVERY_R2", self.contract["contract"])
        precedence = self.contract["authority"]["precedence"]
        self.assertEqual(
            "live_github_pull_request_issue_head_checks_and_reviews",
            precedence[0],
        )
        self.assertLess(
            precedence.index("stored_work_session_checkpoint"),
            precedence.index("historical_chat_context"),
        )
        reconciliation = self.contract["live_reconciliation"]
        self.assertTrue(reconciliation["required"])
        self.assertEqual(
            "live_github_state_overrides_stored_checkpoint",
            reconciliation["conflict_rule"],
        )
        self.assertEqual(
            "never_repeat",
            reconciliation["completed_action_policy"],
        )

    def test_chat_execution_does_not_require_mode_switch_or_continue(self) -> None:
        continuity = self.contract["execution_continuity"]
        self.assertEqual("CHAT_AUTONOMOUS_ENGINEERING", continuity["mode"])
        self.assertFalse(continuity["mode_switch_required"])
        self.assertFalse(continuity["work_mode_required"])
        self.assertFalse(continuity["user_continue_required"])
        self.assertTrue(continuity["progress_updates_are_non_final"])
        self.assertIn(
            "authorized_next_action_exists",
            continuity["final_response_forbidden_when"],
        )
        self.assertIn(
            "ci_is_running_and_can_be_polled",
            continuity["final_response_forbidden_when"],
        )

    def test_final_response_is_gated_by_completion_or_hard_blocker(self) -> None:
        allowed = set(
            self.contract["execution_continuity"]["final_response_allowed_when"]
        )
        self.assertEqual(
            {
                "completion_criteria_satisfied",
                "hard_blocker_requires_user_decision",
                "user_explicitly_pauses_or_replaces_task",
            },
            allowed,
        )

    def test_context_limit_requires_complete_durable_handoff(self) -> None:
        boundary = self.contract["context_boundary"]
        self.assertEqual(
            "persist_durable_handoff_before_final_response",
            boundary["near_limit_action"],
        )
        self.assertEqual(
            {
                "repository",
                "main_sha",
                "active_issue_or_pull_request",
                "head_sha",
                "completed_actions",
                "current_blocker_or_running_check",
                "next_authorized_action",
                "scope_constraints",
                "completion_criteria",
            },
            set(boundary["required_handoff_fields"]),
        )
        self.assertEqual(
            "forbidden_when_handoff_can_be_persisted",
            boundary["unsummarized_context_exit"],
        )

    def test_work_state_is_a_reconciled_checkpoint_not_runtime_authority(self) -> None:
        self.assertEqual("CHAT_WORK_SESSION_STATE_R2", self.state["schema"])
        self.assertEqual(
            "checkpoint_only_must_reconcile_with_live_github_state",
            self.state["authority"],
        )
        self.assertEqual(
            "LIVE_GITHUB_DISCOVERY_REQUIRED",
            self.state["task_resolution"]["strategy"],
        )
        self.assertTrue(
            self.state["staleness_policy"][
                "checkpoint_is_never_sufficient_for_execution"
            ]
        )
        self.assertEqual(
            "DO_NOT_REPEAT",
            self.state["staleness_policy"]["completed_action_in_checkpoint"],
        )
        continuity = self.state["continuity"]
        self.assertFalse(continuity["mode_switch_required"])
        self.assertFalse(continuity["user_continue_required"])
        self.assertTrue(continuity["status_updates_are_non_final"])
        self.assertTrue(continuity["stop_only_on_completion_or_hard_blocker"])


if __name__ == "__main__":
    unittest.main()

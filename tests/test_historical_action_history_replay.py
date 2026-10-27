"""Historical provenance gates must survive handoff advancement and reject lost history."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("13HK", "verify-tianwen-13hk-ncl03130-teldap-catalog-crosswalk.py", None),
    ("13HL", "verify-tianwen-13hl-ncl03130-source-native-intake.py", "13HK"),
    ("13HO", "verify-tianwen-13ho-ndl991069-day14-day16-locators.py", "13HN"),
    ("13HQ", "verify-tianwen-13hq-ndl991069-winter-context.py", "13HP"),
)


class HistoricalActionHistoryReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads((ROOT / "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text())
        cls.cases = []
        for tag, filename, predecessor in CASES:
            spec = importlib.util.spec_from_file_location(tag, ROOT / "scripts" / filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            cls.cases.append((tag, module, json.loads(module.E.read_text()), predecessor))

    def replay(self, mutate, rejected):
        for tag, module, evidence, predecessor in self.cases:
            with self.subTest(batch=tag):
                ledger = copy.deepcopy(self.ledger)
                issue = next(i for i in ledger["issues"] if i["id"] == "TW-OPEN-0005")
                revision = next(h for h in issue["history"]
                                if h.get("revision_id", "").startswith(f"TW-OPEN-0005-{tag}-"))
                mutate(issue, revision, predecessor)
                if rejected:
                    with self.assertRaises(AssertionError):
                        module.check(copy.deepcopy(evidence), ledger=ledger)
                else:
                    self.assertTrue(module.check(copy.deepcopy(evidence), ledger=ledger))

    def test_later_current_action_needs_no_inline_historical_prose(self):
        self.replay(lambda i, h, p: i.update(next_action="A later source review is now current."), False)

    def test_current_action_cannot_replace_deleted_revision(self):
        def remove(issue, revision, _):
            issue["next_action"] = "13HK CURRENT ACTION: 13HL CURRENT ACTION: 13HO CURRENT ACTION: 13HQ CURRENT ACTION:"
            issue["history"].remove(revision)
        self.replay(remove, True)

    def test_unrelated_history_event_is_not_an_action_revision(self):
        self.replay(lambda i, h, p: h.update(event="SOURCE_SCOPE_RECHECK_ONLY"), True)

    def test_revision_must_declare_action_change(self):
        self.replay(lambda i, h, p: h.update(changed_fields=["source_refs"]), True)

    def test_revision_must_reference_its_original_evidence(self):
        self.replay(lambda i, h, p: h.update(evidence_refs=["unrelated.json"]), True)

    def test_predecessor_transition_cannot_disappear(self):
        def remove(issue, revision, predecessor):
            target = predecessor or "13HK"
            issue["history"] = [h for h in issue["history"]
                                if not h.get("revision_id", "").startswith(f"TW-OPEN-0005-{target}-")]
        self.replay(remove, True)

    def test_historical_transition_cannot_close_live_original_target(self):
        self.replay(lambda i, h, p: i.update(status="CLOSED"), True)


if __name__ == "__main__":
    unittest.main()

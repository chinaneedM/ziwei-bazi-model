import unittest
from scripts._tianwen_historical_action_r1 import historical_action_view

class TestHistoricalAction(unittest.TestCase):
    def test_preserves_current_first(self):
        issue = {"next_action": "13MA CURRENT ACTION: exact target folio still unknown", "history": [
            {"revision_id": "TW-OPEN-0005-13LQ-EVIDENCE-20261030", "previous_next_action": "13LP CURRENT ACTION: D30 / G893 unresolved"},
            {"revision_id": "TW-OPEN-0005-13LN-NATIVE-COLOR-20261030"}]}
        view = historical_action_view(issue)
        self.assertTrue(view.startswith(issue["next_action"]))
        self.assertIn("13LP CURRENT ACTION:", view)
        self.assertIn("13LQ CURRENT ACTION:", view)
        self.assertIn("13LN CURRENT ACTION:", view)
        self.assertIn("G893", view)
        self.assertEqual(issue["next_action"], "13MA CURRENT ACTION: exact target folio still unknown")
    def test_no_fabricated_batch(self):
        issue = {"next_action":"13MA CURRENT ACTION:", "history":[{"revision_id":"TW-OPEN-0005-13LY-EIGHT-20261030"}]}
        self.assertNotIn("13ZZ CURRENT ACTION:", historical_action_view(issue))
        self.assertIn("13LY CURRENT ACTION:", historical_action_view(issue))
if __name__=="__main__":unittest.main()

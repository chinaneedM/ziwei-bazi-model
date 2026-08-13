from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.local_app import APP_JS


class CombinedChartMultiCandidateUiRuntimeR1Tests(unittest.TestCase):
    def test_candidate_selector_rebinds_to_selected_index(self) -> None:
        self.assertIn("function renderBazi(bundle,index=0)", APP_JS)
        self.assertIn("option.selected=candidateIndex===index", APP_JS)
        self.assertIn("candidateIndex+1", APP_JS)
        self.assertIn("index+1", APP_JS)

    def test_single_candidate_path_has_no_ambiguity_banner(self) -> None:
        self.assertIn("if(count>1){", APP_JS)
        self.assertNotIn("if(count>=1){", APP_JS)


if __name__ == "__main__":
    unittest.main()

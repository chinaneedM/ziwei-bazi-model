from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.local_app import APP_JS, STYLE_CSS


class CombinedChartMultiCandidateUiR1Tests(unittest.TestCase):
    def test_multi_candidate_renderer_is_explicit_and_switchable(self) -> None:
        self.assertIn("const count=bundle.candidates.length;", APP_JS)
        self.assertIn("if(count>1){", APP_JS)
        self.assertIn("时间不确定性：共 ${count} 个八字候选；当前候选 ${index+1}/${count}", APP_JS)
        self.assertIn("bundle.candidates.forEach", APP_JS)
        self.assertIn("select.addEventListener('change'", APP_JS)
        self.assertIn("renderBazi(bundle,Number.parseInt(select.value,10))", APP_JS)

    def test_renderer_does_not_silently_lock_to_first_candidate(self) -> None:
        self.assertNotIn("bundle.candidates[0]?.view", APP_JS)
        self.assertIn("const candidate=bundle.candidates[index];", APP_JS)
        self.assertIn("const view=candidate?.view;", APP_JS)

    def test_uncertainty_controls_are_presentation_only(self) -> None:
        self.assertIn("bazi-candidate-bar", STYLE_CSS)
        self.assertNotIn("winner", APP_JS.lower())
        self.assertNotIn("score", APP_JS.lower())
        self.assertNotIn("rank", APP_JS.lower())


if __name__ == "__main__":
    unittest.main()

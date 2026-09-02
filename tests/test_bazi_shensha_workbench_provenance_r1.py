from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.local_app_assets import APP_JS


class BaziShenshaWorkbenchProvenanceR1Test(unittest.TestCase):
    def test_renderer_surfaces_backend_candidate_provenance_without_arbitration(self) -> None:
        for field in (
            "shensha_id",
            "target_kind",
            "target_values",
            "anchor_basis",
            "anchor_value",
            "match_scope",
            "matched_pillars",
            "present",
            "selection_status",
            "qualification_status",
            "source_refs",
            "semantic_scope",
            "occurrences",
        ):
            self.assertIn(f"row.{field}", APP_JS)

        self.assertIn("(set?.candidates||[]).forEach((row)=>{", APP_JS)
        self.assertNotIn("set.candidates.filter((row)=>row.present)", APP_JS)
        self.assertNotIn("const basis={DAY_STEM:", APP_JS)
        self.assertIn("value===undefined||value===null||value===''?'—':String(value)", APP_JS)
        self.assertIn("`${label}: ${value}`", APP_JS)
        self.assertIn("`occurrences: ${occurrences}`", APP_JS)


if __name__ == "__main__":
    unittest.main()

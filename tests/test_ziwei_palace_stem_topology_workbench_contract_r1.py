from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.palace_stem_topology_assets import (
    PALACE_STEM_TOPOLOGY_JS,
    palace_stem_topology_index_html,
)


class ZiweiPalaceStemTopologyWorkbenchContractR1Tests(unittest.TestCase):
    def test_browser_consumes_released_topology_without_recomputing_rules(self) -> None:
        for expected in (
            "/api/ziwei-palace-stem-topology",
            "ziwei_palace_stem_transformation_topology",
            "source_address_index",
            "source_branch",
            "source_stem",
            "transformation_type",
            "target_display_name",
            "target_branch",
            "topology_relation",
            "assignment_id",
            "mechanism_id",
            "source_refs",
            "classification_policy",
            "selection_semantics",
            "semantic_scope",
            "source_transformation_rule_set_id",
            "source_application_bundle_hash",
            "fact_hash",
            "computation_hash",
            "integrity",
            "同宫 / 对宫 / 其他宫不等于离心 / 向心自化",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, PALACE_STEM_TOPOLOGY_JS)

        for forbidden in (
            "TransformationGenerator",
            "S08-ASG-",
            "_TARGETS",
            "+ 6",
            "% 12",
            "OUTWARD_DISSIPATION",
            "INWARD_RECEPTION",
            "SELF_LU",
            "OPPOSITE_LU",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, PALACE_STEM_TOPOLOGY_JS)

    def test_assets_are_additive_and_idempotence_guarded(self) -> None:
        base = "<html><head></head><body><main>chart</main></body></html>"
        rendered = palace_stem_topology_index_html(base)
        self.assertIn("/ziwei-palace-stem-topology.css", rendered)
        self.assertIn("/ziwei-palace-stem-topology.js", rendered)
        with self.assertRaises(ValueError):
            palace_stem_topology_index_html(rendered)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.palace_stem_topology_assets import (
    PALACE_STEM_TOPOLOGY_JS,
)


class ZiweiStarProvenanceWorkbenchContractR1Tests(unittest.TestCase):
    def test_browser_consumes_backend_provenance_without_star_classification_table(self) -> None:
        for expected in (
            "/api/ziwei-star-provenance",
            "ziwei_star_placement_provenance",
            "generator_family_id",
            "generator_family_label",
            "main_star_system_id",
            "main_star_system_label",
            "generator_id",
            "algorithm_version",
            "source_refs",
            "source_application_bundle_hash",
            "classification_policy",
            "semantic_scope",
            "fact_hash",
            "computation_hash",
            "integrity",
            "仅按后端已发布的生成器来源与主星来源系分组",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, PALACE_STEM_TOPOLOGY_JS)

        for forbidden in (
            "STAR.ZIWEI",
            "STAR.TIANFU",
            "MAIN_STAR_ALGORITHM_ID",
            "ZIWEI-FOURTEEN-MAIN-STARS-V1",
            "ZIWEI-CORE-AUXILIARY-V1",
            "ZIWEI-DERIVED-AUXILIARY-V1",
            "ZIWEI-OPERATIONAL-MINOR-STARS-V1",
            "benefic",
            "malefic",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, PALACE_STEM_TOPOLOGY_JS)


if __name__ == "__main__":
    unittest.main()

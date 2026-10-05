from __future__ import annotations

import unittest

from fortune_training.ziwei_chart.temporal_auxiliary import TemporalAuxiliaryGenerator


class ReceivedFullbookAnnualVirtueCandidateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = TemporalAuxiliaryGenerator()
        self.branches = tuple("子丑寅卯辰巳午未申酉戌亥")

    def test_yuede_is_annual_only_and_maps_zi_start_directly(self) -> None:
        for branch in self.branches:
            row = self.generator.annual_yuede_candidate_set(
                branch,
                source_stem="甲",
                source_layer="ANNUAL",
                context_id=f"ANNUAL:{branch}",
                temporal_source_refs=("TEST:ANNUAL",),
            )
            self.assertEqual(branch, row.method_candidates[0].activations[0].target_address.branch)
            self.assertEqual(("STAR.YUEDE",), row.entity_ids)
            self.assertEqual("SOURCE_SCOPED_CANDIDATE_PRESERVED_NO_SELECTION", row.selection_status)
            self.assertIn("S01:ZZQS-A-1944", row.source_refs)
        with self.assertRaisesRegex(ValueError, "ANNUAL only"):
            self.generator.annual_yuede_candidate_set(
                "子", source_stem="甲", source_layer="NATAL",
                context_id="NATAL", temporal_source_refs=(),
            )

    def test_tiande_is_annual_only_and_maps_you_start_forward(self) -> None:
        expected = tuple("酉戌亥子丑寅卯辰巳午未申")
        for branch, target in zip(self.branches, expected, strict=True):
            row = self.generator.annual_tiande_candidate_set(
                branch,
                source_stem="甲",
                source_layer="ANNUAL",
                context_id=f"ANNUAL:{branch}",
                temporal_source_refs=("TEST:ANNUAL",),
            )
            self.assertEqual(target, row.method_candidates[0].activations[0].target_address.branch)
            self.assertEqual(("STAR.TIANDE",), row.entity_ids)
            self.assertEqual("SOURCE_SCOPED_CANDIDATE_PRESERVED_NO_SELECTION", row.selection_status)
            self.assertIn("S01:ZZQS-A-1943", row.source_refs)
        with self.assertRaisesRegex(ValueError, "ANNUAL only"):
            self.generator.annual_tiande_candidate_set(
                "子", source_stem="甲", source_layer="NATAL",
                context_id="NATAL", temporal_source_refs=(),
            )

    def test_fullbook_annual_candidates_are_unselected_source_scoped_methods(self) -> None:
        for builder in (
            self.generator.annual_yuede_candidate_set,
            self.generator.annual_tiande_candidate_set,
        ):
            row = builder(
                "子", source_stem="甲", source_layer="ANNUAL",
                context_id="ANNUAL:TEST", temporal_source_refs=("TEST:ANNUAL",),
            )
            self.assertEqual(
                "RECEIVED_FULLBOOK_ANNUAL_SOURCE_SCOPED_METHOD",
                row.method_candidates[0].authority_status,
            )
            self.assertEqual(
                "SOURCE_SCOPED_CANDIDATE_PRESERVED_NO_SELECTION",
                row.selection_status,
            )


if __name__ == "__main__":
    unittest.main()

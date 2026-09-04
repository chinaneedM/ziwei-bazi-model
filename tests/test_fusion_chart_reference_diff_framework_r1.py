from __future__ import annotations

import unittest

from fortune_training.fusion_chart_acceptance import (
    DefectClass,
    DefectRecord,
    compare_reference_snapshot,
)


class FusionChartReferenceDiffFrameworkR1Tests(unittest.TestCase):
    def test_reference_difference_never_auto_promotes_to_implementation_defect(self) -> None:
        differences = compare_reference_snapshot(
            {"bazi": {"day_pillar": "甲子"}, "ziwei": {"hour_method": "A"}},
            {"bazi": {"day_pillar": "乙丑"}, "ziwei": {"hour_method": "B"}},
            disputed_paths=("ziwei.hour_method",),
        )
        self.assertEqual(2, len(differences))
        by_path = {row.path: row for row in differences}
        self.assertEqual(
            DefectClass.REFERENCE_DIFFERENCE,
            by_path["bazi.day_pillar"].classification,
        )
        self.assertEqual(
            DefectClass.DISPUTED_CANDIDATE,
            by_path["ziwei.hour_method"].classification,
        )
        self.assertNotIn(
            DefectClass.IMPLEMENTATION_DEFECT,
            {row.classification for row in differences},
        )

    def test_expected_profile_difference_is_explicit(self) -> None:
        differences = compare_reference_snapshot(
            {"bazi": {"day_boundary": "MIDNIGHT"}},
            {"bazi": {"day_boundary": "ZI_START_23"}},
            expected_profile_paths=("bazi.day_boundary",),
        )
        self.assertEqual(
            DefectClass.EXPECTED_PROFILE_DIFFERENCE,
            differences[0].classification,
        )

    def test_only_evidenced_implementation_defect_can_reopen_algorithm(self) -> None:
        with self.assertRaises(ValueError):
            DefectRecord(
                defect_id="D-1",
                classification=DefectClass.REFERENCE_DIFFERENCE,
                capability_id="CAP-TIME",
                case_id="CASE-1",
                summary="reference differs",
                algorithm_reopened=True,
            )
        record = DefectRecord(
            defect_id="D-2",
            classification=DefectClass.IMPLEMENTATION_DEFECT,
            capability_id="CAP-TIME",
            case_id="CASE-2",
            summary="canonical source plus replay evidence proves implementation mismatch",
            evidence=("canonical-source:example", "replay:example"),
            algorithm_reopened=True,
        )
        self.assertTrue(record.algorithm_reopened)


if __name__ == "__main__":
    unittest.main()

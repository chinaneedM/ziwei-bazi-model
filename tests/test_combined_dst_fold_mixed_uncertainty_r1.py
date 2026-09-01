from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import bazi_local_application_v1_profile
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimePrecision
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedChartService,
    combined_chart_application_v1_profile,
    validate_combined_application_full_replay,
)
from fortune_training.ziwei_application import (
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import (
    Sex,
    ZiweiChartRequest,
    ziwei_chart_engine_v1_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedDstFoldMixedUncertaintyR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.birth = BirthInput(
            reported_local_datetime=datetime(2020, 11, 1, 1, 0),
            birth_place="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone_id="America/New_York",
            precision=TimePrecision.NEAREST_MINUTE,
            uncertainty_seconds=0,
        )
        cls.ziwei_calculation_profile = ziwei_chart_engine_v1_profile(registry)
        cls.ziwei_application_profile = ziwei_application_v1_profile()
        cls.ziwei_presentation_profile = (
            ziwei_application_default_presentation_profile()
        )
        cls.bazi_natal_profile = bazi_foundation_v1_profile(registry)
        cls.bazi_temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.bazi_application_profile = bazi_local_application_v1_profile()
        cls.combined_profile = combined_chart_application_v1_profile()
        cls.service = CombinedChartService.from_repository(ROOT)
        cls.request = CombinedChartApplicationRequest(
            birth=cls.birth,
            sex="MALE",
            ziwei_calculation_profile=cls.ziwei_calculation_profile,
            ziwei_application_profile=cls.ziwei_application_profile,
            ziwei_presentation_profile=cls.ziwei_presentation_profile,
            bazi_natal_profile=cls.bazi_natal_profile,
            bazi_temporal_profile=cls.bazi_temporal_profile,
            bazi_application_profile=cls.bazi_application_profile,
            combined_profile=cls.combined_profile,
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )

    def test_mixed_fold_deduplicates_shared_branches_without_selecting_winner(self):
        foundation = self.service.ziwei_foundation.resolve_typed(
            ZiweiChartRequest(
                birth=self.birth,
                sex=Sex.MALE,
                profile=self.ziwei_calculation_profile,
            )
        )
        self.assertEqual("MULTI_CANDIDATE", foundation.status)
        self.assertEqual(2, len(foundation.candidates))

        time_calendar = foundation.time_calendar
        self.assertEqual(
            "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY",
            time_calendar["status"],
        )
        self.assertEqual(30, time_calendar["input_interval"]["uncertainty_seconds_each_side"])
        self.assertEqual(3, time_calendar["input_interval"]["sample_count"])
        self.assertEqual(2, time_calendar["input_interval"]["ambiguous_sample_count"])
        self.assertEqual(5, len(time_calendar["branches"]))
        self.assertEqual([], time_calendar["unresolved_samples"])
        self.assertEqual(
            {0, 1},
            {
                row["selected_civil_candidate"]["fold"]
                for row in time_calendar["branches"]
            },
        )

        expected_by_branch: dict[int, str] = {}
        branch_group_sizes = []
        for candidate in foundation.candidates:
            self.assertEqual("PASS", candidate.integrity.status)
            branch_group_sizes.append(len(candidate.branch_indices))
            for branch_index in candidate.branch_indices:
                self.assertNotIn(branch_index, expected_by_branch)
                expected_by_branch[branch_index] = candidate.hashes.fact_hash
        self.assertEqual(set(range(5)), set(expected_by_branch))
        self.assertEqual(2, len(set(expected_by_branch.values())))
        self.assertEqual([2, 3], sorted(branch_group_sizes))

        combined = self.service.resolve(self.request)
        self.assertEqual("PASS", combined.integrity.status)
        self.assertIsNone(combined.ziwei_bundle)
        self.assertIsNotNone(combined.ziwei_error)
        self.assertEqual(
            "APPLICATION_UNIQUE_NATAL_CANDIDATE_REQUIRED",
            combined.ziwei_error.code,
        )
        self.assertIn(combined.status, {"PARTIAL", "FAILED"})

        shared = combined.shared_time_credential
        self.assertEqual(
            {
                "ziwei": "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY",
                "bazi": "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY",
            },
            shared["status"],
        )
        self.assertEqual(30, shared["input_interval"]["uncertainty_seconds_each_side"])
        self.assertEqual(3, shared["input_interval"]["sample_count"])
        self.assertEqual(2, shared["input_interval"]["ambiguous_sample_count"])
        self.assertEqual(5, len(shared["realizations"]))
        self.assertEqual([], shared["unresolved_samples"])
        self.assertEqual(
            {0, 1},
            {row["fold"] for row in shared["realizations"]},
        )
        self.assertEqual(
            2,
            sum(row["fold"] == 1 for row in shared["realizations"]),
        )

        lineage = combined.candidate_lineage
        self.assertEqual(5, len(lineage["branches"]))
        actual_by_branch = {
            row["source_time_branch_index"]: row["ziwei_natal_fact_hash"]
            for row in lineage["branches"]
        }
        self.assertEqual(expected_by_branch, actual_by_branch)
        self.assertEqual(2, len(set(actual_by_branch.values())))
        for row in lineage["branches"]:
            self.assertIsNotNone(row["ziwei_natal_fact_hash"])
            self.assertIn(row["status"], {"LINKED_BOTH", "ZIWEI_ONLY"})

        exported = self.service.export(combined)
        self.assertEqual(shared, exported["manifest"]["shared_time_credential"])
        self.assertEqual(lineage, exported["manifest"]["candidate_lineage"])
        self.assertIsNone(exported["ziwei_export"])

        full_replay = validate_combined_application_full_replay(
            self.service,
            self.request,
            combined,
        )
        self.assertEqual("PASS", full_replay.status)
        self.assertEqual((), full_replay.diagnostics)

        replay = self.service.resolve(self.request)
        self.assertEqual(combined.manifest_hash, replay.manifest_hash)
        self.assertEqual(
            shared["computation_hash"],
            replay.shared_time_credential["computation_hash"],
        )
        self.assertEqual(
            lineage["lineage_hash"],
            replay.candidate_lineage["lineage_hash"],
        )


if __name__ == "__main__":
    unittest.main()

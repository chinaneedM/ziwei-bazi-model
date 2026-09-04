from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import bazi_local_application_v1_profile
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedChartService,
    combined_chart_application_v1_profile,
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


class CombinedDstFoldZiweiCandidateLineageR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.birth = BirthInput(
            reported_local_datetime=datetime(2020, 11, 1, 1, 30),
            birth_place="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone_id="America/New_York",
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
        cls.combined_service = CombinedChartService.from_repository(ROOT)
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

    def test_dst_fold_preserves_all_ziwei_foundation_fact_hashes(self):
        foundation = self.combined_service.ziwei_foundation.resolve_typed(
            ZiweiChartRequest(
                birth=self.birth,
                sex=Sex.MALE,
                profile=self.ziwei_calculation_profile,
            )
        )
        self.assertEqual("MULTI_CANDIDATE", foundation.status)
        self.assertEqual(2, len(foundation.candidates))
        self.assertEqual(2, len(foundation.time_calendar["branches"]))
        self.assertEqual(
            {0, 1},
            {
                row["selected_civil_candidate"]["fold"]
                for row in foundation.time_calendar["branches"]
            },
        )

        expected_by_branch: dict[int, str] = {}
        for candidate in foundation.candidates:
            self.assertEqual("PASS", candidate.integrity.status)
            for branch_index in candidate.branch_indices:
                expected_by_branch[branch_index] = candidate.hashes.fact_hash
        self.assertEqual({0, 1}, set(expected_by_branch))
        self.assertEqual(2, len(set(expected_by_branch.values())))

        combined = self.combined_service.resolve(self.request)
        self.assertEqual("PASS", combined.integrity.status)
        self.assertIsNone(combined.ziwei_bundle)
        self.assertIsNotNone(combined.ziwei_error)
        self.assertEqual(
            "APPLICATION_UNIQUE_NATAL_CANDIDATE_REQUIRED",
            combined.ziwei_error.code,
        )
        self.assertIn(combined.status, {"PARTIAL", "FAILED"})

        shared = combined.shared_time_credential
        self.assertEqual(1, shared["input_interval"]["ambiguous_sample_count"])
        self.assertEqual(2, len(shared["realizations"]))
        self.assertEqual(
            {0, 1},
            {row["fold"] for row in shared["realizations"]},
        )

        lineage = combined.candidate_lineage
        self.assertEqual(
            "ZIWEI-BAZI-SHARED-TIME-LINEAGE-V1",
            lineage["schema"],
        )
        self.assertEqual(shared["computation_hash"], lineage["shared_time_computation_hash"])
        self.assertEqual(2, len(lineage["branches"]))
        actual_by_branch = {
            row["source_time_branch_index"]: row["ziwei_natal_fact_hash"]
            for row in lineage["branches"]
        }
        self.assertEqual(expected_by_branch, actual_by_branch)
        self.assertEqual(2, len(set(actual_by_branch.values())))
        for row in lineage["branches"]:
            self.assertIsNotNone(row["ziwei_natal_fact_hash"])
            self.assertIn(row["status"], {"LINKED_BOTH", "ZIWEI_ONLY"})

        exported = self.combined_service.export(combined)
        self.assertEqual(
            lineage,
            exported["manifest"]["candidate_lineage"],
        )
        self.assertIsNone(exported["ziwei_export"])

        replay = self.combined_service.resolve(self.request)
        self.assertEqual(combined.manifest_hash, replay.manifest_hash)
        self.assertEqual(
            combined.candidate_lineage["lineage_hash"],
            replay.candidate_lineage["lineage_hash"],
        )
        self.assertEqual(
            actual_by_branch,
            {
                row["source_time_branch_index"]: row["ziwei_natal_fact_hash"]
                for row in replay.candidate_lineage["branches"]
            },
        )


if __name__ == "__main__":
    unittest.main()

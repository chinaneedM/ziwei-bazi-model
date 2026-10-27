from __future__ import annotations

import unittest
from dataclasses import replace
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
    validate_combined_resolution,
)
from fortune_training.ziwei_application import (
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class CombinedDstGapMixedProvenanceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.birth = BirthInput(
            reported_local_datetime=datetime(1991, 4, 14, 2, 0),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
            precision=TimePrecision.NEAREST_HOUR,
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

    def test_mixed_dst_gap_is_hash_bound_across_combined_runtime(self):
        result = self.service.resolve(self.request)

        self.assertEqual("UNCERTAINTY_PRESENT", result.status)
        self.assertEqual("PASS", result.integrity.status)
        self.assertIsNotNone(result.ziwei_bundle)
        self.assertIsNotNone(result.bazi_bundle)
        self.assertIsNone(result.ziwei_error)
        self.assertIsNone(result.bazi_error)

        ziwei_bundle = result.ziwei_bundle
        bazi_bundle = result.bazi_bundle
        assert ziwei_bundle is not None
        assert bazi_bundle is not None
        self.assertEqual(
            "RESOLVED_SINGLE_CHART_WITH_TIME_UNCERTAINTY",
            ziwei_bundle.resolution_status,
        )
        self.assertEqual(tuple(range(30)), ziwei_bundle.candidate.branch_indices)
        self.assertEqual("MULTI_CANDIDATE", bazi_bundle.status)
        self.assertEqual(30, len(bazi_bundle.candidates))

        shared = result.shared_time_credential
        expected_time_status = "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY"
        self.assertEqual(
            {"ziwei": expected_time_status, "bazi": expected_time_status},
            shared["status"],
        )
        self.assertEqual(1800, shared["input_interval"]["uncertainty_seconds_each_side"])
        self.assertEqual(61, shared["input_interval"]["sample_count"])
        self.assertEqual(0, shared["input_interval"]["ambiguous_sample_count"])
        self.assertEqual(30, len(shared["realizations"]))
        self.assertEqual(31, len(shared["unresolved_samples"]))
        self.assertEqual(
            {"NONEXISTENT"},
            {row["civil_status"] for row in shared["unresolved_samples"]},
        )
        self.assertEqual(
            "1991-04-14T02:00:00",
            shared["unresolved_samples"][0]["sample_reported_local_datetime"],
        )
        self.assertEqual(
            "1991-04-14T02:30:00",
            shared["unresolved_samples"][-1]["sample_reported_local_datetime"],
        )

        lineage = result.candidate_lineage
        self.assertEqual(30, len(lineage["branches"]))
        self.assertEqual(
            set(range(30)),
            {row["source_time_branch_index"] for row in lineage["branches"]},
        )
        self.assertEqual(
            {"LINKED_BOTH"},
            {row["status"] for row in lineage["branches"]},
        )
        self.assertEqual(
            1,
            len({row["ziwei_natal_fact_hash"] for row in lineage["branches"]}),
        )
        self.assertTrue(
            all(len(row["bazi_candidate_ids"]) == 1 for row in lineage["branches"])
        )

        exported = self.service.export(result)
        self.assertEqual(shared, exported["manifest"]["shared_time_credential"])
        self.assertEqual(lineage, exported["manifest"]["candidate_lineage"])

        changed_shared = dict(shared)
        changed_unresolved = [dict(row) for row in shared["unresolved_samples"]]
        changed_unresolved[0]["civil_status"] = "UNIQUE"
        changed_shared["unresolved_samples"] = changed_unresolved
        changed = replace(result, shared_time_credential=changed_shared)
        report = validate_combined_resolution(changed)
        self.assertEqual("FAIL", report.status)
        self.assertIn("SHARED_TIME_FACT_HASH_MISMATCH", report.diagnostics)
        self.assertIn("SHARED_TIME_COMPUTATION_HASH_MISMATCH", report.diagnostics)

        replay = self.service.resolve(self.request)
        self.assertEqual(result.manifest_hash, replay.manifest_hash)
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

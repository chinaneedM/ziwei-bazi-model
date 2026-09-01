from __future__ import annotations

import unittest
from dataclasses import replace
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
    combined_manifest_hash,
    validate_combined_application_full_replay,
)
from fortune_training.util import object_sha256
from fortune_training.ziwei_application import (
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class CombinedApplicationFullReplayR1Tests(unittest.TestCase):
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
        cls.service = CombinedChartService.from_repository(ROOT)
        cls.request = CombinedChartApplicationRequest(
            birth=cls.birth,
            sex="MALE",
            ziwei_calculation_profile=ziwei_chart_engine_v1_profile(registry),
            ziwei_application_profile=ziwei_application_v1_profile(),
            ziwei_presentation_profile=(
                ziwei_application_default_presentation_profile()
            ),
            bazi_natal_profile=bazi_foundation_v1_profile(registry),
            bazi_temporal_profile=bazi_temporal_v1_continuous_profile(),
            bazi_application_profile=bazi_local_application_v1_profile(),
            combined_profile=combined_chart_application_v1_profile(),
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )

    def test_full_replay_passes_for_dst_multi_candidate_resolution(self):
        resolution = self.service.resolve(self.request)
        self.assertIsNone(resolution.ziwei_bundle)
        self.assertIsNotNone(resolution.ziwei_error)
        self.assertEqual(
            "APPLICATION_UNIQUE_NATAL_CANDIDATE_REQUIRED",
            resolution.ziwei_error.code,
        )

        report = validate_combined_application_full_replay(
            self.service,
            self.request,
            resolution,
        )
        self.assertEqual("PASS", report.status)
        self.assertEqual((), report.diagnostics)
        self.assertEqual(
            "ZIWEI-BAZI-COMBINED-APPLICATION-FULL-REPLAY-INTEGRITY-R1",
            report.algorithm_id,
        )

    def test_full_replay_rejects_forged_well_formed_ziwei_fact_hash(self):
        resolution = self.service.resolve(self.request)
        lineage = dict(resolution.candidate_lineage)
        branches = [dict(row) for row in lineage["branches"]]
        actual_hashes = {
            row["ziwei_natal_fact_hash"]
            for row in branches
            if row["ziwei_natal_fact_hash"] is not None
        }
        self.assertEqual(2, len(actual_hashes))

        forged_hash = "0" * 64
        if forged_hash in actual_hashes:
            forged_hash = "f" * 64
        branches[0]["ziwei_natal_fact_hash"] = forged_hash
        lineage_payload = {
            "schema": lineage["schema"],
            "shared_time_computation_hash": lineage[
                "shared_time_computation_hash"
            ],
            "branches": branches,
        }
        forged_lineage = {
            **lineage_payload,
            "lineage_hash": object_sha256(lineage_payload),
        }
        forged = replace(
            resolution,
            candidate_lineage=forged_lineage,
            manifest_hash="PENDING",
        )
        forged = replace(
            forged,
            manifest_hash=combined_manifest_hash(forged),
        )

        report = validate_combined_application_full_replay(
            self.service,
            self.request,
            forged,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn(
            "CANDIDATE_LINEAGE_FULL_REPLAY_MISMATCH",
            report.diagnostics,
        )
        self.assertIn(
            "COMBINED_MANIFEST_FULL_REPLAY_MISMATCH",
            report.diagnostics,
        )
        self.assertIn(
            "COMBINED_APPLICATION_FULL_REPLAY_MISMATCH",
            report.diagnostics,
        )


if __name__ == "__main__":
    unittest.main()

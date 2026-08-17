from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

import jsonschema

from fortune_training.bazi_target_temporal import (
    TargetTemporalCoordinateFoundation,
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
    validate_target_temporal_resolution,
)
from fortune_training.calendar_foundation import BaziTimeResolver, TimePrecision
from fortune_training.calendar_foundation.models import json_value


ROOT = Path(__file__).resolve().parents[1]
PRE_1970_WARNING = "IANA tzdb does not guarantee complete pre-1970 historical coverage"


class BaziTargetTemporalCoordinateFoundationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.foundation = TargetTemporalCoordinateFoundation()
        cls.profile = bazi_target_temporal_coordinate_r1_profile()
        cls.schema = json.loads(
            (ROOT / "schemas" / "bazi-target-temporal-coordinate-foundation-r1.schema.json").read_text(
                encoding="utf-8"
            )
        )

    @staticmethod
    def target(
        local: datetime,
        *,
        place: str,
        latitude: float,
        longitude: float,
        timezone_id: str,
        precision: TimePrecision = TimePrecision.EXACT_SECOND,
        uncertainty_seconds: int = 0,
    ) -> TargetTemporalInput:
        return TargetTemporalInput(
            reported_local_datetime=local,
            target_place=place,
            latitude=latitude,
            longitude=longitude,
            timezone_id=timezone_id,
            precision=precision,
            uncertainty_seconds=uncertainty_seconds,
        )

    def test_greenwich_exact_target_resolves_deterministically_and_validates_schema(self) -> None:
        target = self.target(
            datetime(2025, 1, 15, 12, 0),
            place="Greenwich",
            latitude=51.4769,
            longitude=0.0,
            timezone_id="Europe/London",
        )
        first = self.foundation.resolve(target, self.profile)
        second = self.foundation.resolve(target, self.profile)

        self.assertEqual("RESOLVED", first.status)
        self.assertEqual("PASS", first.integrity.status)
        self.assertEqual(1, first.sample_count)
        self.assertEqual(1, len(first.candidates))
        self.assertEqual(first.hashes, second.hashes)
        self.assertEqual(first.candidates, second.candidates)
        self.assertEqual(target.reported_local_datetime, first.candidates[0].sample_reported_local_datetime)
        jsonschema.Draft202012Validator(self.schema).validate(json_value(first))

    def test_same_utc_different_longitude_changes_las_not_annual_monthly(self) -> None:
        greenwich = self.foundation.resolve(
            self.target(
                datetime(2025, 1, 15, 12, 0),
                place="Greenwich",
                latitude=51.4769,
                longitude=0.0,
                timezone_id="Europe/London",
            ),
            self.profile,
        )
        beijing = self.foundation.resolve(
            self.target(
                datetime(2025, 1, 15, 20, 0),
                place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            self.profile,
        )
        g = greenwich.candidates[0]
        b = beijing.candidates[0]
        self.assertEqual(g.target_utc, b.target_utc)
        self.assertNotEqual(g.local_apparent_solar_datetime, b.local_apparent_solar_datetime)
        self.assertNotEqual(greenwich.hashes.fact_hash, beijing.hashes.fact_hash)

        bazi_time = BaziTimeResolver()
        g_frames = bazi_time.resolve_year_month(g.target_utc, year_boundary_policy="START_OF_SPRING")
        b_frames = bazi_time.resolve_year_month(b.target_utc, year_boundary_policy="START_OF_SPRING")
        self.assertEqual(g_frames.year_pillar, b_frames.year_pillar)
        self.assertEqual(g_frames.month_pillar, b_frames.month_pillar)
        self.assertEqual(g_frames.annual_start_boundary.utc_instant, b_frames.annual_start_boundary.utc_instant)
        self.assertEqual(g_frames.active_month_boundary.utc_instant, b_frames.active_month_boundary.utc_instant)

    def test_explicit_target_longitude_is_not_birth_fallback(self) -> None:
        target = self.target(
            datetime(2025, 1, 15, 12, 0),
            place="Explicit East Longitude",
            latitude=0.0,
            longitude=120.0,
            timezone_id="Etc/UTC",
        )
        resolved = self.foundation.resolve(target, self.profile)
        candidate = resolved.candidates[0]
        self.assertGreater(candidate.local_apparent_solar_datetime.hour, candidate.target_utc.hour)

        with self.assertRaises(TypeError):
            TargetTemporalInput(
                reported_local_datetime=datetime(2025, 1, 15, 12, 0),
                target_place="Missing longitude",
                latitude=0.0,
                timezone_id="Etc/UTC",
            )

    def test_new_york_dst_fold_preserves_both_realizations(self) -> None:
        resolved = self.foundation.resolve(
            self.target(
                datetime(2024, 11, 3, 1, 30),
                place="New York",
                latitude=40.7128,
                longitude=-74.0060,
                timezone_id="America/New_York",
            ),
            self.profile,
        )
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", resolved.status)
        self.assertEqual("PASS", resolved.integrity.status)
        self.assertEqual(1, resolved.ambiguous_sample_count)
        self.assertEqual(2, len(resolved.candidates))
        self.assertEqual({0, 1}, {row.fold for row in resolved.candidates})
        self.assertEqual(2, len({row.target_utc for row in resolved.candidates}))
        self.assertEqual(2, len({row.candidate_id for row in resolved.candidates}))

    def test_new_york_dst_gap_exact_fails_closed_with_provenance(self) -> None:
        resolved = self.foundation.resolve(
            self.target(
                datetime(2024, 3, 10, 2, 30),
                place="New York",
                latitude=40.7128,
                longitude=-74.0060,
                timezone_id="America/New_York",
            ),
            self.profile,
        )
        self.assertEqual("FAILED", resolved.status)
        self.assertEqual("PASS", resolved.integrity.status)
        self.assertEqual((), resolved.candidates)
        self.assertEqual(1, len(resolved.unresolved_samples))
        self.assertEqual("NONEXISTENT", resolved.unresolved_samples[0].civil_status)
        self.assertIn("TARGET_CIVIL_TIME_UNRESOLVED", resolved.diagnostics)
        jsonschema.Draft202012Validator(self.schema).validate(json_value(resolved))

    def test_explicit_uncertainty_preserves_sample_identity(self) -> None:
        resolved = self.foundation.resolve(
            self.target(
                datetime(2025, 1, 15, 12, 0),
                place="Greenwich",
                latitude=51.4769,
                longitude=0.0,
                timezone_id="Europe/London",
                uncertainty_seconds=120,
            ),
            self.profile,
        )
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", resolved.status)
        self.assertEqual(5, resolved.sample_count)
        self.assertEqual(5, len(resolved.candidates))
        self.assertEqual(list(range(5)), [row.source_sample_index for row in resolved.candidates])

    def test_pre_1970_target_preserves_historical_confidence(self) -> None:
        resolved = self.foundation.resolve(
            self.target(
                datetime(1965, 1, 15, 12, 0),
                place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            self.profile,
        )
        candidate = resolved.candidates[0]
        self.assertEqual("TZDB_PRE_1970_REDUCED", candidate.historical_confidence)
        self.assertIn(PRE_1970_WARNING, candidate.warnings)

    def test_tampered_target_longitude_or_las_fails_integrity_replay(self) -> None:
        resolved = self.foundation.resolve(
            self.target(
                datetime(2025, 1, 15, 12, 0),
                place="Greenwich",
                latitude=51.4769,
                longitude=0.0,
                timezone_id="Europe/London",
            ),
            self.profile,
        )
        tampered_input = replace(resolved.target_input, longitude=30.0)
        tampered_resolution = replace(resolved, target_input=tampered_input)
        report = validate_target_temporal_resolution(
            tampered_resolution,
            self.profile,
            self.foundation.civil,
            self.foundation.solar,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("TARGET_CANDIDATE_REPLAY_MISMATCH", {row.code for row in report.diagnostics})

        candidate = resolved.candidates[0]
        tampered_candidate = replace(
            candidate,
            local_apparent_solar_datetime=candidate.local_apparent_solar_datetime.replace(hour=13),
        )
        tampered_resolution = replace(resolved, candidates=(tampered_candidate,))
        report = validate_target_temporal_resolution(
            tampered_resolution,
            self.profile,
            self.foundation.civil,
            self.foundation.solar,
        )
        self.assertEqual("FAIL", report.status)


if __name__ == "__main__":
    unittest.main()

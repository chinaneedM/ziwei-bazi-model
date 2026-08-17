from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import InputTimeType, TimePrecision
from fortune_training.calendar_foundation.models import json_value
from fortune_training.target_temporal_coordinate import (
    TargetTemporalCoordinateEngine,
    TargetTemporalInput,
    target_temporal_coordinate_r1_profile,
    validate_target_coordinate,
)


ROOT = Path(__file__).resolve().parents[1]


class TargetTemporalCoordinateR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = TargetTemporalCoordinateEngine()
        cls.profile = target_temporal_coordinate_r1_profile()

    def resolve(self, target: TargetTemporalInput):
        return self.engine.resolve(target, self.profile)

    @staticmethod
    def greenwich_target(**overrides) -> TargetTemporalInput:
        values = {
            "reported_local_datetime": datetime(2025, 2, 3, 14, 10),
            "target_place": "Greenwich",
            "latitude": 51.4769,
            "longitude": 0.0,
            "timezone_id": "Europe/London",
        }
        values.update(overrides)
        return TargetTemporalInput(**values)

    def test_greenwich_point_resolves_deterministically(self) -> None:
        target = self.greenwich_target()
        first = self.resolve(target)
        second = self.resolve(target)
        self.assertEqual("RESOLVED", first.status)
        self.assertEqual(1, first.sample_count)
        self.assertEqual(1, first.legal_realization_count)
        self.assertEqual(first.fact_hash, second.fact_hash)
        self.assertEqual(first.computation_hash, second.computation_hash)
        self.assertEqual("PASS", first.candidates[0].integrity.status)

    def test_schema_required_keys_match_public_resolution_projection(self) -> None:
        result = self.resolve(self.greenwich_target())
        schema = json.loads(
            (ROOT / "schemas" / "target-temporal-coordinate-r1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        projection = json_value(result)
        self.assertEqual("TARGET-TEMPORAL-COORDINATE-RESOLUTION-R1", projection["schema"])
        self.assertEqual(set(schema["required"]), set(projection))
        self.assertEqual(schema["properties"]["schema"]["const"], projection["schema"])
        self.assertIn(projection["status"], schema["properties"]["status"]["enum"])

    def test_same_utc_different_longitude_changes_las_and_identity(self) -> None:
        base = dict(
            reported_local_datetime=datetime(2025, 6, 1, 12, 0),
            latitude=0.0,
            timezone_id="UTC",
        )
        greenwich = self.resolve(TargetTemporalInput(target_place="Greenwich", longitude=0.0, **base))
        east = self.resolve(TargetTemporalInput(target_place="East 30", longitude=30.0, **base))
        left = greenwich.candidates[0].coordinate
        right = east.candidates[0].coordinate
        self.assertEqual(left.civil_candidate.utc_instant, right.civil_candidate.utc_instant)
        self.assertNotEqual(
            left.solar_time.local_apparent_solar_datetime,
            right.solar_time.local_apparent_solar_datetime,
        )
        self.assertNotEqual(greenwich.fact_hash, east.fact_hash)
        self.assertNotEqual(greenwich.computation_hash, east.computation_hash)

    def test_target_input_has_no_birth_location_fallback(self) -> None:
        with self.assertRaises(ValueError):
            TargetTemporalInput(
                reported_local_datetime=datetime(2025, 6, 1, 12, 0),
                target_place="",
                latitude=0.0,
                longitude=0.0,
                timezone_id="UTC",
            )
        self.assertNotIn("birth_place", TargetTemporalInput.__dataclass_fields__)

    def test_new_york_dst_fold_preserves_both_realizations(self) -> None:
        result = self.resolve(
            TargetTemporalInput(
                reported_local_datetime=datetime(2024, 11, 3, 1, 30),
                target_place="New York",
                latitude=40.7128,
                longitude=-74.0060,
                timezone_id="America/New_York",
            )
        )
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", result.status)
        self.assertEqual(1, result.sample_count)
        self.assertEqual(1, result.ambiguous_sample_count)
        self.assertEqual(2, result.legal_realization_count)
        self.assertEqual({0, 1}, {row.coordinate.civil_candidate.fold for row in result.candidates})
        self.assertEqual(2, len({row.hashes.fact_hash for row in result.candidates}))
        self.assertEqual({0, 1}, {row.coordinate.source_civil_candidate_index for row in result.candidates})

    def test_lord_howe_gap_exact_fails_closed(self) -> None:
        result = self.resolve(
            TargetTemporalInput(
                reported_local_datetime=datetime(2024, 10, 6, 2, 15),
                target_place="Lord Howe Island",
                latitude=-31.5531,
                longitude=159.0839,
                timezone_id="Australia/Lord_Howe",
            )
        )
        self.assertEqual("FAILED", result.status)
        self.assertEqual(0, result.legal_realization_count)
        self.assertEqual(1, len(result.unresolved_samples))
        self.assertEqual("NONEXISTENT", result.unresolved_samples[0].civil_status)

    def test_uncertainty_preserves_legal_and_gap_samples(self) -> None:
        result = self.resolve(
            TargetTemporalInput(
                reported_local_datetime=datetime(2024, 10, 6, 2, 0),
                target_place="Lord Howe Island",
                latitude=-31.5531,
                longitude=159.0839,
                timezone_id="Australia/Lord_Howe",
                precision=TimePrecision.EXACT_SECOND,
                uncertainty_seconds=1800,
            )
        )
        self.assertEqual("MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY", result.status)
        self.assertGreater(result.legal_realization_count, 0)
        self.assertGreater(len(result.unresolved_samples), 0)
        self.assertEqual(61, result.sample_count)

    def test_pre_1970_timezone_confidence_is_preserved(self) -> None:
        result = self.resolve(
            TargetTemporalInput(
                reported_local_datetime=datetime(1965, 1, 1, 12, 0),
                target_place="Shanghai",
                latitude=31.2304,
                longitude=121.4737,
                timezone_id="Asia/Shanghai",
            )
        )
        coordinate = result.candidates[0].coordinate
        self.assertEqual("TZDB_PRE_1970_REDUCED", coordinate.historical_confidence)
        self.assertTrue(any("pre-1970" in warning for warning in coordinate.warnings))

    def test_approximate_sampling_uses_shared_precision_contract(self) -> None:
        target = self.greenwich_target(
            precision=TimePrecision.APPROXIMATE,
            uncertainty_seconds=120,
        )
        result = self.resolve(target)
        self.assertEqual(120, result.effective_uncertainty_seconds_each_side)
        self.assertEqual(5, result.sample_count)
        self.assertEqual(5, result.legal_realization_count)
        self.assertEqual(set(range(5)), {row.coordinate.source_sample_index for row in result.candidates})

    def test_non_civil_input_fails_closed(self) -> None:
        result = self.resolve(self.greenwich_target(input_time_type=InputTimeType.UNKNOWN))
        self.assertEqual("FAILED", result.status)
        self.assertEqual("NOT_APPLICABLE", result.unresolved_samples[0].civil_status)

    def test_integrity_rejects_tampered_longitude(self) -> None:
        target = self.greenwich_target()
        coordinate = self.resolve(target).candidates[0].coordinate
        report = validate_target_coordinate(target, replace(coordinate, longitude=1.0), self.profile)
        self.assertEqual("FAIL", report.status)
        self.assertIn("LONGITUDE_MISMATCH", {row.code for row in report.diagnostics})

    def test_integrity_rejects_tampered_sample_lineage(self) -> None:
        target = self.greenwich_target(
            precision=TimePrecision.APPROXIMATE,
            uncertainty_seconds=120,
        )
        coordinate = self.resolve(target).candidates[0].coordinate
        report = validate_target_coordinate(
            target,
            replace(coordinate, source_sample_index=999),
            self.profile,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("SOURCE_SAMPLE_INDEX_OUT_OF_RANGE", {row.code for row in report.diagnostics})

    def test_integrity_rejects_tampered_fold_lineage(self) -> None:
        target = TargetTemporalInput(
            reported_local_datetime=datetime(2024, 11, 3, 1, 30),
            target_place="New York",
            latitude=40.7128,
            longitude=-74.0060,
            timezone_id="America/New_York",
        )
        coordinate = self.resolve(target).candidates[0].coordinate
        report = validate_target_coordinate(
            target,
            replace(coordinate, source_civil_candidate_index=1),
            self.profile,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("SOURCE_CIVIL_CANDIDATE_MISMATCH", {row.code for row in report.diagnostics})


if __name__ == "__main__":
    unittest.main()

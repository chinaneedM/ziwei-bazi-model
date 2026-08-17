from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jsonschema

from fortune_training.bazi_application import (
    BaziApplicationFlowRequest,
    BaziApplicationFlowService,
    BaziApplicationRequest,
    BaziApplicationResolutionError,
    BaziChartService,
    bazi_local_application_v1_profile,
    validate_application_flow_resolution,
)
from fortune_training.bazi_application.flow_local_app import (
    FLOW_LOCAL_APP_RESOLVE_SCHEMA,
    FlowLocalBaziApplication,
)
from fortune_training.bazi_application.local_app import LocalBaziApplication
from fortune_training.bazi_chart import (
    bazi_foundation_v1_profile,
    bazi_foundation_zi_start_23_r1_profile,
)
from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput
from fortune_training.calendar_foundation.models import json_value


ROOT = Path(__file__).resolve().parents[1]


class _DuplicateTemporalEngine:
    def __init__(self) -> None:
        self.inner = BaziTemporalEngine()

    def resolve_typed(self, request):
        result = self.inner.resolve_typed(request)
        if not result.candidates:
            return result
        row = result.candidates[0]
        return replace(
            result,
            status="MULTI_CANDIDATE",
            candidates=(row, row),
            events=tuple(dict.fromkeys((*result.events, "SYNTHETIC_DUPLICATE_LINEAGE"))),
        )


class BaziApplicationFlowIntegrationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_service = BaziChartService.from_repository(ROOT)
        cls.flow_service = BaziApplicationFlowService(cls.base_service)
        cls.registry = cls.base_service.chart_foundation.time_calendar.policy_registry
        cls.midnight_profile = bazi_foundation_v1_profile(cls.registry)
        cls.zi_profile = bazi_foundation_zi_start_23_r1_profile(cls.registry)
        cls.temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.application_profile = bazi_local_application_v1_profile()
        cls.target_profile = bazi_target_temporal_coordinate_r1_profile()
        cls.birth = BirthInput(
            reported_local_datetime=datetime(2025, 2, 7, 10, 10),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.schema = json.loads(
            (
                ROOT
                / "schemas"
                / "bazi-application-flow-integration-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

    @classmethod
    def _base_request(cls, *, birth=None, natal_profile=None, dayun_count=6):
        return BaziApplicationRequest(
            birth=birth or cls.birth,
            sex=BaziSex.MALE,
            natal_profile=natal_profile or cls.midnight_profile,
            temporal_profile=cls.temporal_profile,
            application_profile=cls.application_profile,
            dayun_count=dayun_count,
        )

    @classmethod
    def _target(
        cls,
        local: datetime,
        *,
        place: str = "Greenwich",
        latitude: float = 51.4769,
        longitude: float = 0.0,
        timezone_id: str = "Etc/UTC",
        uncertainty_seconds: int = 0,
    ) -> TargetTemporalInput:
        return TargetTemporalInput(
            reported_local_datetime=local,
            target_place=place,
            latitude=latitude,
            longitude=longitude,
            timezone_id=timezone_id,
            uncertainty_seconds=uncertainty_seconds,
        )

    @classmethod
    def _request(cls, target, *, base_request=None):
        return BaziApplicationFlowRequest(
            application_request=base_request or cls._base_request(),
            target_input=target,
            target_coordinate_profile=cls.target_profile,
        )

    @classmethod
    def _resolve(cls, target, *, base_request=None):
        return cls.flow_service.resolve(
            cls._request(target, base_request=base_request)
        )

    @classmethod
    def _target_wall_for_las(cls, desired_las: datetime) -> datetime:
        wall = desired_las
        for _ in range(5):
            resolution = cls.flow_service.target_foundation.resolve(
                cls._target(wall), cls.target_profile
            )
            if len(resolution.candidates) != 1:
                raise RuntimeError("LAS solver fixture requires one target candidate")
            actual = resolution.candidates[0].local_apparent_solar_datetime
            wall += desired_las - actual
        return wall

    def test_ordinary_target_is_deterministic_schema_valid_and_closed(self) -> None:
        target = self._target(datetime(2026, 6, 1, 12, 0))
        first = self._resolve(target)
        second = self._resolve(target)
        self.assertEqual("RESOLVED", first.status)
        self.assertEqual("PASS", first.integrity.status)
        self.assertEqual(first, second)
        self.assertEqual(first.bundle_hash, second.bundle_hash)
        row = first.candidates[0]
        self.assertEqual("PASS", row.view["integrity"]["flow"])
        self.assertEqual("PASS", row.view["integrity"]["daily_hourly"])
        self.assertTrue(row.view["flow"]["annual"]["ganzhi"])
        self.assertTrue(row.view["flow"]["monthly"]["ganzhi"])
        self.assertTrue(row.view["daily"]["ganzhi"])
        self.assertTrue(row.view["hourly"]["ganzhi"])
        jsonschema.Draft202012Validator(self.schema).validate(json_value(first))

        injected = copy.deepcopy(json_value(first))
        injected["candidates"][0]["view"]["prediction"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.schema).validate(injected)

    def test_legacy_application_v1_is_byte_and_hash_stable(self) -> None:
        base_request = self._base_request()
        before = self.base_service.resolve(base_request)
        self._resolve(
            self._target(datetime(2026, 6, 1, 12, 0)),
            base_request=base_request,
        )
        after = self.base_service.resolve(base_request)
        self.assertEqual(before, after)
        self.assertEqual(json_value(before), json_value(after))
        self.assertEqual(before.source_fact_hash, after.source_fact_hash)
        self.assertEqual(before.view_hash, after.view_hash)
        self.assertEqual(before.bundle_hash, after.bundle_hash)

        legacy = LocalBaziApplication(ROOT)
        flow_app = FlowLocalBaziApplication(ROOT)
        payload = self._local_payload()
        self.assertEqual(
            legacy.resolve_payload(payload),
            flow_app.resolve_payload(payload),
        )

    def test_same_utc_different_target_longitude_preserves_annual_monthly(self) -> None:
        wall = datetime(2026, 6, 1, 0, 30)
        west = self._resolve(
            self._target(
                wall,
                place="UTC meridian",
                latitude=0.0,
                longitude=0.0,
            )
        )
        east = self._resolve(
            self._target(
                wall,
                place="Explicit east longitude",
                latitude=0.0,
                longitude=120.0,
            )
        )
        left = west.candidates[0].view
        right = east.candidates[0].view
        self.assertEqual(left["target"]["target_utc"], right["target"]["target_utc"])
        self.assertEqual(left["flow"]["annual"], right["flow"]["annual"])
        self.assertEqual(left["flow"]["monthly"], right["flow"]["monthly"])
        self.assertNotEqual(
            left["target"]["local_apparent_solar_datetime"],
            right["target"]["local_apparent_solar_datetime"],
        )
        self.assertNotEqual(left["hourly"]["ganzhi"], right["hourly"]["ganzhi"])
        self.assertNotEqual(west.bundle_hash, east.bundle_hash)

    def test_23_las_profile_split_survives_application_composition(self) -> None:
        target = self._target(datetime(2026, 1, 15, 23, 30))
        midnight = self._resolve(target)
        zi = self._resolve(
            target,
            base_request=self._base_request(natal_profile=self.zi_profile),
        )
        m = midnight.candidates[0].view
        z = zi.candidates[0].view
        self.assertEqual("MIDNIGHT", m["daily"]["day_boundary_policy"])
        self.assertEqual("ZI_START_23", z["daily"]["day_boundary_policy"])
        self.assertEqual(
            "CLASSICAL_CONTINUOUS",
            m["hourly"]["late_zi_hour_stem_policy"],
        )
        self.assertEqual(
            "ZI_START_ROLLOVER",
            z["hourly"]["late_zi_hour_stem_policy"],
        )
        self.assertNotEqual(
            m["daily"]["effective_day_date"],
            z["daily"]["effective_day_date"],
        )
        self.assertNotEqual(midnight.bundle_hash, zi.bundle_hash)

    def test_start_of_spring_and_monthly_jie_authority_survive_application(self) -> None:
        terms = self.base_service.chart_foundation.time_calendar.solar_terms
        spring = terms.term(2026, 315).utc_instant
        before_spring = self._resolve(
            self._target((spring - timedelta(microseconds=1)).replace(tzinfo=None))
        ).candidates[0].view
        exact_spring = self._resolve(
            self._target(spring.replace(tzinfo=None))
        ).candidates[0].view
        self.assertEqual("乙巳", before_spring["flow"]["annual"]["ganzhi"])
        self.assertEqual("丙午", exact_spring["flow"]["annual"]["ganzhi"])
        self.assertEqual("己丑", before_spring["flow"]["monthly"]["ganzhi"])
        self.assertEqual("庚寅", exact_spring["flow"]["monthly"]["ganzhi"])
        self.assertEqual(json_value(spring), exact_spring["flow"]["annual"]["start_utc"])

        jingzhe = terms.term(2026, 345).utc_instant
        before_jie = self._resolve(
            self._target((jingzhe - timedelta(microseconds=1)).replace(tzinfo=None))
        ).candidates[0].view
        exact_jie = self._resolve(
            self._target(jingzhe.replace(tzinfo=None))
        ).candidates[0].view
        self.assertEqual("庚寅", before_jie["flow"]["monthly"]["ganzhi"])
        self.assertEqual("辛卯", exact_jie["flow"]["monthly"]["ganzhi"])
        self.assertEqual("AWAKENING_OF_INSECTS", exact_jie["flow"]["monthly"]["start_jie_name"])
        self.assertEqual(json_value(jingzhe), exact_jie["flow"]["monthly"]["start_utc"])

    def test_daily_and_hourly_half_open_turnover_survives_application(self) -> None:
        midnight_wall = self._target_wall_for_las(datetime(2026, 6, 2, 0, 0))
        before_midnight = self._resolve(
            self._target(midnight_wall - timedelta(seconds=1))
        ).candidates[0].view
        at_midnight = self._resolve(
            self._target(midnight_wall)
        ).candidates[0].view
        self.assertNotEqual(
            before_midnight["daily"]["frame_id"], at_midnight["daily"]["frame_id"]
        )
        self.assertEqual(
            before_midnight["daily"]["end_las"], at_midnight["daily"]["start_las"]
        )

        branch_wall = self._target_wall_for_las(datetime(2026, 6, 2, 3, 0))
        before_branch = self._resolve(
            self._target(branch_wall - timedelta(seconds=1))
        ).candidates[0].view
        at_branch = self._resolve(
            self._target(branch_wall)
        ).candidates[0].view
        self.assertNotEqual(
            before_branch["hourly"]["frame_id"], at_branch["hourly"]["frame_id"]
        )
        self.assertEqual(
            before_branch["hourly"]["end_las"], at_branch["hourly"]["start_las"]
        )

    def test_dst_fold_preserved_and_dst_gap_fails_closed(self) -> None:
        fold = self._resolve(
            self._target(
                datetime(2026, 11, 1, 1, 30),
                place="New York",
                latitude=40.7128,
                longitude=-74.006,
                timezone_id="America/New_York",
            )
        )
        self.assertEqual("MULTI_CANDIDATE", fold.status)
        self.assertEqual(2, len(fold.candidates))
        self.assertEqual(
            {0, 1},
            {row.source_target_coordinate_candidate_index for row in fold.candidates},
        )
        self.assertEqual(
            2,
            len({row.view["target"]["target_utc"] for row in fold.candidates}),
        )

        with self.assertRaises(BaziApplicationResolutionError) as gap_error:
            self._resolve(
                self._target(
                    datetime(2026, 3, 8, 2, 30),
                    place="New York",
                    latitude=40.7128,
                    longitude=-74.006,
                    timezone_id="America/New_York",
                )
            )
        self.assertEqual(
            "BAZI_APP_FLOW_TARGET_RESOLUTION_FAILED", gap_error.exception.code
        )

    def test_target_uncertainty_preserves_every_compatible_target_candidate(self) -> None:
        result = self._resolve(
            self._target(datetime(2026, 6, 1, 12, 0), uncertainty_seconds=120)
        )
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertGreater(result.target_coordinate_sample_count, 1)
        self.assertEqual(
            list(range(len(result.candidates))),
            [row.source_target_coordinate_candidate_index for row in result.candidates],
        )
        self.assertEqual(
            len(result.candidates),
            len({row.target_coordinate_candidate_id for row in result.candidates}),
        )

    def test_target_before_birth_and_after_materialized_dayun_fail_closed(self) -> None:
        with self.assertRaises(BaziApplicationResolutionError) as before_error:
            self._resolve(self._target(datetime(2024, 1, 1, 0, 0)))
        self.assertEqual(
            "BAZI_APP_FLOW_CONTEXT_RESOLUTION_FAILED", before_error.exception.code
        )
        self.assertIn("TARGET_BEFORE_BIRTH", before_error.exception.detail)

        short_request = self._base_request(dayun_count=1)
        with self.assertRaises(BaziApplicationResolutionError) as after_error:
            self._resolve(
                self._target(datetime(2050, 1, 1, 0, 0)),
                base_request=short_request,
            )
        self.assertEqual(
            "BAZI_APP_FLOW_CONTEXT_RESOLUTION_FAILED", after_error.exception.code
        )
        self.assertIn("TARGET_OUT_OF_MATERIALIZED_DAYUN_RANGE", after_error.exception.detail)

    def test_explicit_target_daily_hourly_do_not_inherit_birth_longitude(self) -> None:
        alternate_birth = BirthInput(
            reported_local_datetime=datetime(2025, 2, 7, 2, 10),
            birth_place="Greenwich birth",
            latitude=51.4769,
            longitude=0.0,
            timezone_id="Etc/UTC",
        )
        target = self._target(
            datetime(2026, 6, 1, 18, 0),
            place="Explicit target",
            latitude=0.0,
            longitude=90.0,
        )
        beijing_birth = self._resolve(target)
        greenwich_birth = self._resolve(
            target,
            base_request=self._base_request(birth=alternate_birth),
        )
        left = beijing_birth.candidates[0].view
        right = greenwich_birth.candidates[0].view
        self.assertEqual(
            left["target"]["local_apparent_solar_datetime"],
            right["target"]["local_apparent_solar_datetime"],
        )
        self.assertEqual(left["daily"]["ganzhi"], right["daily"]["ganzhi"])
        self.assertEqual(left["hourly"]["ganzhi"], right["hourly"]["ganzhi"])
        self.assertNotEqual(
            left["source_hashes"]["natal_fact_hash"],
            right["source_hashes"]["natal_fact_hash"],
        )

    def test_identical_flow_payload_aggregation_preserves_all_application_lineage(self) -> None:
        duplicate_base = BaziChartService(
            self.base_service.chart_foundation,
            temporal_engine=_DuplicateTemporalEngine(),
        )
        service = BaziApplicationFlowService(duplicate_base)
        result = service.resolve(
            self._request(
                self._target(datetime(2026, 6, 1, 12, 0)),
                base_request=self._base_request(),
            )
        )
        self.assertEqual("RESOLVED", result.status)
        row = result.candidates[0]
        self.assertEqual((0, 1), row.source_temporal_candidate_indices)
        self.assertEqual(2, len(row.source_application_candidate_ids))
        self.assertEqual(
            [0, 1], row.view["lineage"]["source_temporal_candidate_indices"]
        )

    def test_application_flow_tamper_fails_integrity(self) -> None:
        result = self._resolve(self._target(datetime(2026, 6, 1, 12, 0)))
        row = result.candidates[0]
        changed_view = copy.deepcopy(row.view)
        changed_view["target"]["target_place"] = "Tampered place"
        tampered = replace(
            result,
            candidates=(replace(row, view=changed_view),),
        )
        report = validate_application_flow_resolution(tampered)
        self.assertEqual("FAIL", report.status)
        self.assertTrue(
            {
                "CANDIDATE:0:VIEW_HASH_MISMATCH",
                "CANDIDATE:0:VIEW_TARGET_PLACE_MISMATCH",
            }.issubset(set(report.diagnostics))
        )

        index_tamper = replace(
            result,
            candidates=(
                replace(row, source_target_coordinate_candidate_index=99),
            ),
        )
        index_report = validate_application_flow_resolution(index_tamper)
        self.assertEqual("FAIL", index_report.status)
        self.assertIn(
            "CANDIDATE:0:VIEW_TARGET_INDEX_LINEAGE_MISMATCH",
            index_report.diagnostics,
        )

    def test_flow_local_api_is_separate_and_validates_explicit_target_fields(self) -> None:
        app = FlowLocalBaziApplication(ROOT)
        payload = self._local_payload()
        payload.update(
            {
                "target_datetime": "2026-06-01T12:00:00",
                "target_place": "Greenwich",
                "target_latitude": 51.4769,
                "target_longitude": 0.0,
                "target_timezone_id": "Etc/UTC",
                "target_precision": "EXACT_SECOND",
                "target_uncertainty_seconds": 0,
                "target_temporal_profile_id": (
                    "BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1"
                ),
            }
        )
        response = app.resolve_flow_payload(payload)
        self.assertEqual(FLOW_LOCAL_APP_RESOLVE_SCHEMA, response["schema"])
        self.assertEqual("PASS", response["application_bundle"]["integrity"]["status"])
        self.assertEqual("PASS", response["target_flow_bundle"]["integrity"]["status"])
        jsonschema.Draft202012Validator(self.schema).validate(
            response["target_flow_bundle"]
        )

        changed = dict(payload)
        changed["target_timezone_id"] = "Mars/Olympus"
        with self.assertRaises(Exception) as error:
            app.resolve_flow_payload(changed)
        self.assertEqual(
            "LOCAL_APP_INVALID_TARGET_TIMEZONE",
            getattr(error.exception, "code", None),
        )

    @classmethod
    def _local_payload(cls) -> dict[str, object]:
        return {
            "birth_datetime": "2025-02-07T10:10:00",
            "birth_place": "Beijing",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone_id": "Asia/Shanghai",
            "sex": "MALE",
            "precision": "EXACT_SECOND",
            "uncertainty_seconds": 0,
            "natal_profile_id": "BAZI-FOUNDATION-V1-R1",
            "temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "application_profile_id": "BAZI-LOCAL-APPLICATION-V1-R1",
            "dayun_count": 6,
        }


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import (
    PlainTextZiweiRenderer,
    PresentationProfile,
    Sex,
    ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
    ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
    ZiweiChartFoundation,
    ZiweiChartRequest,
    ZiweiTemporalEngine,
    ZiweiViewProjectionCompiler,
    temporal_hash_bundle,
    validate_temporal_state,
    ziwei_chart_engine_v1_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiChartV1ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.profile = ziwei_chart_engine_v1_profile(cls.registry)
        cls.engine = ZiweiChartFoundation(TimeCalendarFoundation(cls.registry))
        cls.request = ZiweiChartRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex=Sex.MALE,
            profile=cls.profile,
        )

    @staticmethod
    def _schema(filename: str) -> dict:
        return json.loads((ROOT / "schemas" / filename).read_text(encoding="utf-8"))

    @classmethod
    def _validate_schema(cls, filename: str, value) -> None:
        schema = cls._schema(filename)
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(value), key=lambda row: list(row.absolute_path))
        if errors:
            rendered = "\n".join(
                f"{'.'.join(str(part) for part in row.absolute_path) or '<root>'}: {row.message}"
                for row in errors
            )
            raise AssertionError(f"{filename} validation failed:\n{rendered}")

    def test_frozen_profile_identity_and_operational_bindings(self) -> None:
        profile = self.profile
        self.assertEqual(ZIWEI_CHART_ENGINE_V1_PROFILE_ID, profile.profile_id)
        self.assertEqual(ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION, profile.profile_version)
        self.assertEqual("ZI_START_23", profile.ziwei_day_boundary_policy)
        self.assertEqual("ZI_START_23", profile.time_calendar_policies.bazi_day_boundary_policy)
        self.assertEqual("ZI_START_ROLLOVER", profile.time_calendar_policies.bazi_late_zi_hour_stem_policy)
        self.assertEqual("ZHONGZHOU_FIXED_15", profile.time_calendar_policies.ziwei_life_body_leap_month_policy)
        self.assertEqual("WENMO_DEFAULT_CORE_AUX_R1", profile.auxiliary_rule_set_id)
        self.assertEqual("WENMO_DEFAULT_MINOR_R1", profile.minor_rule_set_id)
        self.assertEqual("2.0.0", profile.minor_rule_set_version)
        self.assertEqual("OPERATIONAL-ZIWEI-DIGNITY-R4", profile.dignity_rule_set_id)
        self.assertEqual("S08_CURRENT_40_ASSIGNMENT_R1", profile.transformation_rule_set_id)
        self.assertEqual("S10_CURRENT_TEMPORAL_R1", profile.temporal_rule_set_id)
        self.assertEqual("WENMO_DEFAULT_RING_R1", profile.ring_rule_set_id)
        self.assertEqual("WENMO_DEFAULT_ROLE_R1", profile.role_rule_set_id)

    def test_public_typed_resolution_materializes_full_v1_inventory(self) -> None:
        typed = self.engine.resolve_typed(self.request)
        self.assertEqual("ZIWEI-CHART-TYPED-RESOLUTION-V1", typed.schema)
        self.assertEqual("RESOLVED", typed.status)
        self.assertEqual(1, len(typed.candidates))
        candidate = typed.candidates[0]
        self.assertEqual(1994, candidate.ziwei_birth_year)
        self.assertEqual(Sex.MALE, candidate.sex)
        self.assertEqual("PASS", candidate.integrity.status)
        self.assertEqual(70, len(candidate.chart.placements))
        self.assertEqual(70, len({row.entity_id for row in candidate.chart.placements}))
        self.assertEqual(70, len(candidate.chart.annotations))
        self.assertEqual(4, len(candidate.chart.transformations))
        self.assertEqual(4, len(candidate.chart.rings))
        self.assertEqual(2, len(candidate.chart.role_bindings))
        self.assertRegex(candidate.hashes.fact_hash, r"^[0-9a-f]{64}$")
        self.assertRegex(candidate.hashes.computation_hash, r"^[0-9a-f]{64}$")

    def test_typed_uncertainty_deduplicates_without_losing_branch_lineage(self) -> None:
        request = ZiweiChartRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
                uncertainty_seconds=60,
            ),
            sex=Sex.MALE,
            profile=self.profile,
        )
        typed = self.engine.resolve_typed(request)
        self.assertEqual("RESOLVED_SINGLE_CHART_WITH_TIME_UNCERTAINTY", typed.status)
        self.assertEqual(1, len(typed.candidates))
        self.assertGreater(len(typed.candidates[0].branch_indices), 1)

    def test_full_public_vertical_path_and_all_published_schemas(self) -> None:
        typed = self.engine.resolve_typed(self.request)
        self.assertEqual("RESOLVED", typed.status)
        candidate = typed.candidates[0]
        temporal_context = candidate.temporal_context()

        temporal = ZiweiTemporalEngine().generate(
            temporal_context,
            self.profile,
            max_nominal_age=30,
        )
        temporal_integrity = validate_temporal_state(temporal, temporal_context)
        self.assertEqual("PASS", temporal_integrity.status)
        temporal_hashes = temporal_hash_bundle(temporal, self.profile)
        self.assertRegex(temporal_hashes.fact_hash, r"^[0-9a-f]{64}$")
        self.assertRegex(temporal_hashes.computation_hash, r"^[0-9a-f]{64}$")

        first_daxian = temporal.daxian_frames[0]
        view = ZiweiViewProjectionCompiler().compile(
            candidate.chart,
            candidate.hashes,
            PresentationProfile(
                profile_id="ZIWEI-CHART-V1-DEFAULT-VIEW",
                profile_version="1.0.0",
            ),
            temporal_state=temporal,
            temporal_context=temporal_context,
            daxian_frame_id=first_daxian.frame_id,
            annual_year=first_daxian.absolute_year_start,
            minor_limit_age=first_daxian.nominal_age_start,
        )
        rendered = PlainTextZiweiRenderer().render(view)
        self.assertIn("view=ZIWEI-CHART-V1-DEFAULT-VIEW@1.0.0", rendered)
        self.assertIn("fact_hash=", rendered)
        self.assertIn("temporal=", rendered)

        json_result = self.engine.resolve(self.request)
        self.assertEqual(candidate.hashes.fact_hash, json_result["hashes"][0]["fact_hash"])
        self.assertEqual(candidate.hashes.computation_hash, json_result["hashes"][0]["computation_hash"])

        self._validate_schema("ziwei-chart-foundation-v1.schema.json", json_result)
        self._validate_schema("ziwei-temporal-state-v1.schema.json", json_value(temporal))
        self._validate_schema("ziwei-chart-view-v1.schema.json", json_value(view))


if __name__ == "__main__":
    unittest.main()

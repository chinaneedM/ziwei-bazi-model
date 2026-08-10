from __future__ import annotations

import json
import unittest
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jsonschema

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    SymbolicLuckAge,
    bazi_temporal_v1_continuous_profile,
    bazi_temporal_wenzhen_china_compatibility_r1_profile,
    realize_wenzhen_calendar_month_displacement_utc,
    temporal_hash_bundle,
    validate_dayun_state,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = json.loads(
    (ROOT / "tests" / "fixtures" / "bazi-dayun-wenzhen-compatibility-r1.json").read_text(
        encoding="utf-8"
    )
)
HOUR_MICROSECONDS = 3_600_000_000
DAY_MICROSECONDS = 24 * HOUR_MICROSECONDS


def observed_symbolic_hours(case: dict) -> int:
    age = case["wenzhen_symbolic_age"]
    return (((age["years"] * 12 + age["months"]) * 30 + age["days"]) * 24) + age[
        "hours"
    ]


class BaziTemporalWenzhenCompatibilityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.chart_profile = bazi_foundation_v1_profile(
            cls.chart_engine.time_calendar.policy_registry
        )
        cls.temporal_engine = BaziTemporalEngine()
        cls.profile = bazi_temporal_wenzhen_china_compatibility_r1_profile()
        cls.schema = json.loads(
            (ROOT / "schemas" / "bazi-temporal-v1.schema.json").read_text(encoding="utf-8")
        )
        cls.rows: dict[str, tuple[dict, object, object]] = {}
        for case in FIXTURES["cases"]:
            candidate = cls._candidate(case)
            result = cls.temporal_engine.resolve_typed(
                BaziTemporalRequest(
                    candidate=candidate,
                    sex=BaziSex(case["sex"]),
                    profile=cls.profile,
                    dayun_count=3,
                )
            )
            if result.status != "RESOLVED":
                raise RuntimeError(f"{case['id']} compatibility resolution failed: {result.diagnostics}")
            cls.rows[case["id"]] = (case, candidate, result.candidates[0])

    @classmethod
    def _candidate(cls, case: dict):
        birth = BirthInput(
            reported_local_datetime=datetime.fromisoformat(case["reported_local_datetime"]),
            birth_place=case["place"],
            latitude=case["latitude"],
            longitude=case["longitude"],
            timezone_id=case["timezone_id"],
        )
        resolved = cls.chart_engine.resolve_typed(
            BaziChartRequest(birth=birth, profile=cls.chart_profile)
        )
        if len(resolved.candidates) != 1:
            raise RuntimeError(f"{case['id']} requires one natal candidate: {resolved.status}")
        return resolved.candidates[0]

    def test_fixture_is_compatibility_witness_not_calendar_truth(self):
        self.assertEqual("THIRD_PARTY_COMPATIBILITY_WITNESS", FIXTURES["authority_class"])
        self.assertFalse(FIXTURES["canonical_calendar_truth"])
        self.assertFalse(FIXTURES["capture_context"]["transition_minute_second_certified"])
        self.assertEqual(FIXTURES["profile_id"], self.profile.profile_id)
        self.assertEqual("THIRD_PARTY_COMPATIBILITY_WITNESS", self.profile.calendar_realization_source_class)

    def test_a7_through_a11_replay_certified_direction_anchor_pillars_and_ui_components(self):
        max_hour_error = FIXTURES["model_contract"]["ui_hour_model_max_absolute_error_hours"]
        for case, candidate, temporal_candidate in self.rows.values():
            with self.subTest(case=case["id"]):
                state = temporal_candidate.state
                self.assertEqual(case["expected_pillars"], [row.ganzhi for row in candidate.chart.pillars])
                self.assertEqual(case["expected_direction"], state.direction.direction)
                self.assertEqual(case["expected_anchor_kind"], state.jiaoyun.anchor_kind)
                self.assertEqual(case["expected_anchor_name"], state.jiaoyun.anchor_jie_name)
                self.assertEqual(
                    FIXTURES["model_contract"]["interval_coordinate_policy"],
                    state.jiaoyun.interval_coordinate_policy,
                )
                observed = case["wenzhen_symbolic_age"]
                modeled = state.jiaoyun.symbolic_age
                self.assertEqual(
                    (observed["years"], observed["months"], observed["days"]),
                    (modeled.years_360, modeled.months_30, modeled.days),
                )
                modeled_hours = modeled.total_symbolic_microseconds // HOUR_MICROSECONDS
                self.assertLessEqual(
                    abs(modeled_hours - observed_symbolic_hours(case)),
                    max_hour_error,
                )
                self.assertEqual("PASS", temporal_candidate.integrity.status)

    def test_a7_a10_longitude_change_is_mirrored_by_direction(self):
        a7 = self.rows["A7"][2].state.jiaoyun.symbolic_age.total_symbolic_microseconds
        a8 = self.rows["A8"][2].state.jiaoyun.symbolic_age.total_symbolic_microseconds
        a9 = self.rows["A9"][2].state.jiaoyun.symbolic_age.total_symbolic_microseconds
        a10 = self.rows["A10"][2].state.jiaoyun.symbolic_age.total_symbolic_microseconds
        self.assertEqual(a7 - a8, a10 - a9)
        observed_reverse_delta = observed_symbolic_hours(self.rows["A7"][0]) - observed_symbolic_hours(
            self.rows["A8"][0]
        )
        observed_forward_delta = observed_symbolic_hours(self.rows["A10"][0]) - observed_symbolic_hours(
            self.rows["A9"][0]
        )
        self.assertEqual(13 * 24 + 12, observed_reverse_delta)
        self.assertEqual(observed_reverse_delta, observed_forward_delta)

    def test_a11_combines_year_and_month_before_leap_day_clamp(self):
        case = self.rows["A11"][0]
        observed = case["wenzhen_symbolic_age"]
        total = observed_symbolic_hours(case) * HOUR_MICROSECONDS
        symbolic = SymbolicLuckAge(
            total_symbolic_microseconds=total,
            years_360=observed["years"],
            months_30=observed["months"],
            days=observed["days"],
            residual_microseconds=observed["hours"] * HOUR_MICROSECONDS,
            rule_set_id="BAZI-THREE-DAYS-ONE-YEAR-360D-R1",
            rule_set_version="1.0.0",
            source_refs=("EXTERNAL_COMPATIBILITY:WENZHEN:A11",),
        )
        birth_utc = datetime(2024, 2, 29, 2, 10, tzinfo=timezone.utc)
        realized = realize_wenzhen_calendar_month_displacement_utc(birth_utc, symbolic)
        expected = datetime.fromisoformat(
            case["calendar_month_displacement_fixture"]["model_realization_china_standard"]
        )
        self.assertEqual(expected, realized.astimezone(expected.tzinfo))

        sequential_clamp = datetime(2025, 2, 28, 10, 10, tzinfo=expected.tzinfo).replace(
            month=10
        ) + timedelta(days=3, hours=7)
        self.assertEqual(
            case["calendar_month_displacement_fixture"]["sequential_year_clamp_date_must_not_be_used"],
            sequential_clamp.date().isoformat(),
        )
        self.assertNotEqual(sequential_clamp.date(), expected.date())
        self.assertTrue(
            case["calendar_month_displacement_fixture"]["model_only_not_external_minute_second_truth"]
        )

    def test_wenzhen_public_json_validates_and_carries_profile_boundaries(self):
        case = FIXTURES["cases"][0]
        candidate = self.rows[case["id"]][1]
        result = self.temporal_engine.resolve(
            BaziTemporalRequest(candidate, BaziSex(case["sex"]), self.profile, dayun_count=2)
        )
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(result, self.schema)
        profile = result["calculation_profile"]
        self.assertEqual(FIXTURES["profile_id"], profile["profile_id"])
        self.assertEqual(
            "CALENDAR_MONTH_DISPLACEMENT_THEN_DAY_HOUR_R1",
            profile["calendar_realization_rule_set"],
        )
        mixed_profile_payload = deepcopy(result)
        mixed_profile_payload["candidates"][0]["state"]["jiaoyun"][
            "calendar_realization_rule_set"
        ] = "MODERN_CONTINUOUS_RATIO_120X"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(mixed_profile_payload, self.schema)

    def test_profile_provenance_is_computation_hash_only_but_policy_is_fact(self):
        case, candidate, temporal_candidate = self.rows["A7"]
        state = temporal_candidate.state
        changed_refs = replace(
            state,
            jiaoyun=replace(state.jiaoyun, source_refs=state.jiaoyun.source_refs + ("AUDIT:COPY",)),
        )
        changed_ref_hashes = temporal_hash_bundle(changed_refs, self.profile)
        self.assertEqual(temporal_candidate.hashes.fact_hash, changed_ref_hashes.fact_hash)
        self.assertNotEqual(
            temporal_candidate.hashes.computation_hash,
            changed_ref_hashes.computation_hash,
        )

        tampered_policy = replace(
            state,
            jiaoyun=replace(state.jiaoyun, interval_coordinate_policy="ABSOLUTE_UTC_DURATION"),
        )
        report = validate_dayun_state(tampered_policy, candidate, self.profile)
        self.assertEqual("FAIL", report.status)
        self.assertIn("INTERVAL_COORDINATE_POLICY_MISMATCH", {row.code for row in report.diagnostics})
        self.assertNotEqual(
            temporal_candidate.hashes.fact_hash,
            temporal_hash_bundle(tampered_policy, self.profile).fact_hash,
        )

    def test_continuous_profile_signature_and_semantics_remain_unchanged(self):
        continuous = bazi_temporal_v1_continuous_profile()
        self.assertEqual("BAZI-TEMPORAL-V1-CONTINUOUS-R1", continuous.profile_id)
        self.assertEqual("ABSOLUTE_UTC_DURATION", continuous.interval_coordinate_policy)
        self.assertEqual("MODERN_CONTINUOUS_RATIO_120X", continuous.calendar_realization_rule_set)
        case, candidate, wenzhen_candidate = self.rows["A7"]
        result = self.temporal_engine.resolve_typed(
            BaziTemporalRequest(candidate, BaziSex(case["sex"]), continuous, dayun_count=3)
        )
        self.assertEqual("RESOLVED", result.status)
        continuous_candidate = result.candidates[0]
        seed = candidate.temporal_seeds[0]
        expected_raw = int((seed.birth_utc - seed.previous_jie_utc).total_seconds() * 1_000_000)
        self.assertEqual(expected_raw, continuous_candidate.state.jiaoyun.raw_interval_microseconds)
        self.assertEqual(
            seed.birth_utc
            + timedelta(microseconds=continuous_candidate.state.jiaoyun.symbolic_age.total_symbolic_microseconds),
            continuous_candidate.state.jiaoyun.first_transition_utc,
        )
        self.assertNotEqual(continuous_candidate.hashes.fact_hash, wenzhen_candidate.hashes.fact_hash)


if __name__ == "__main__":
    unittest.main()

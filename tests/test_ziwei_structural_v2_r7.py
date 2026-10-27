from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import Sex, ZiweiChartFoundation, ZiweiChartRequest, ziwei_chart_engine_v1_profile
from fortune_training.ziwei_structural import ZiweiStructuralRuntime, ziwei_structural_v2_r1_profile
from fortune_training.ziwei_structural.r2 import ZiweiRelativePalaceFrameRuntime, ziwei_structural_v2_r2_profile
from fortune_training.ziwei_structural.r7 import (
    ONE_SIX_CLOCKWISE_OFFSET,
    ONE_SIX_RELATIVE_ORDINAL,
    ONE_SIX_SEMANTIC_SCOPE,
    ONE_SIX_SOURCE_CLAUSE_IDS,
    ONE_SIX_SOURCE_RUNTIME_BLOB_SHA,
    ONE_SIX_SOURCE_RUNTIME_PATH,
    ONE_SIX_SOURCE_TECHNIQUE_ID,
    OneSixGenerationError,
    ZiweiOneSixCommonRootRuntime,
    one_six_hash_bundle,
    validate_one_six_state,
    ziwei_structural_v2_r7_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.natal_profile = ziwei_chart_engine_v1_profile(registry)
        cls.natal_runtime = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        cls.r1_profile = ziwei_structural_v2_r1_profile()
        cls.r1_runtime = ZiweiStructuralRuntime()
        cls.r2_profile = ziwei_structural_v2_r2_profile()
        cls.r2_runtime = ZiweiRelativePalaceFrameRuntime()
        cls.r7_profile = ziwei_structural_v2_r7_profile()
        cls.r7_runtime = ZiweiOneSixCommonRootRuntime()

        request = ZiweiChartRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex=Sex.MALE,
            profile=cls.natal_profile,
        )
        typed = cls.natal_runtime.resolve_typed(request)
        if typed.status != "RESOLVED" or len(typed.candidates) != 1:
            raise AssertionError(f"unexpected V1 typed resolution: {typed.status}")
        cls.candidate = typed.candidates[0]
        cls.r1_state = cls.r1_runtime.generate_from_candidate(cls.candidate, cls.r1_profile)
        cls.r2_state = cls.r2_runtime.generate_from_candidate(
            cls.candidate,
            cls.r1_state,
            cls.r2_profile,
        )
        cls.r7_state = cls.r7_runtime.generate_from_candidate(
            cls.candidate,
            cls.r1_state,
            cls.r2_state,
            cls.r7_profile,
        )

    def test_profile_freezes_r2_ordinal_6_clockwise_offset_7(self) -> None:
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R7", self.r7_profile.profile_id)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R2", self.r7_profile.upstream_r2_profile_id)
        self.assertEqual(6, self.r7_profile.relative_ordinal)
        self.assertEqual(7, self.r7_profile.clockwise_offset)
        self.assertEqual(ONE_SIX_SEMANTIC_SCOPE, self.r7_profile.semantic_scope)
        self.assertFalse(self.r7_profile.direct_event_permission)
        self.assertFalse(self.r7_profile.direct_endpoint_permission)
        self.assertEqual("NATAL", self.r7_profile.supported_time_layer)

    def test_all_12_origins_match_r2_relative_sixth_geometry_exactly(self) -> None:
        expected_pairs = (
            ("LIFE", "HEALTH"),
            ("SIBLINGS", "TRAVEL"),
            ("SPOUSE", "SERVANTS_FRIENDS"),
            ("CHILDREN", "CAREER"),
            ("WEALTH", "PROPERTY"),
            ("HEALTH", "FORTUNE"),
            ("TRAVEL", "PARENTS"),
            ("SERVANTS_FRIENDS", "LIFE"),
            ("CAREER", "SIBLINGS"),
            ("PROPERTY", "SPOUSE"),
            ("FORTUNE", "CHILDREN"),
            ("PARENTS", "WEALTH"),
        )
        actual = tuple(
            (row.origin_designation_id, row.target_designation_id)
            for row in self.r7_state.one_six_facts
        )
        self.assertEqual(expected_pairs, actual)
        r2_by_key = {
            (row.origin_designation_id, row.relative_ordinal): row
            for row in self.r2_state.frame_facts
        }
        for row in self.r7_state.one_six_facts:
            self.assertEqual(ONE_SIX_SOURCE_TECHNIQUE_ID, row.source_technique_id)
            self.assertEqual(ONE_SIX_RELATIVE_ORDINAL, row.relative_ordinal)
            self.assertEqual(ONE_SIX_CLOCKWISE_OFFSET, row.clockwise_offset)
            self.assertEqual("HEALTH", row.relative_role_designation_id)
            self.assertEqual(ONE_SIX_SEMANTIC_SCOPE, row.semantic_scope)
            self.assertFalse(row.direct_event_permission)
            self.assertFalse(row.direct_endpoint_permission)
            upstream = r2_by_key[(row.origin_designation_id, ONE_SIX_RELATIVE_ORDINAL)]
            self.assertEqual(upstream.target_designation_id, row.target_designation_id)
            self.assertEqual(upstream.origin_address, row.origin_address)
            self.assertEqual(upstream.target_address, row.target_address)
            self.assertEqual(upstream.clockwise_offset, row.clockwise_offset)

    def test_source_lineage_closes_definition_generalization_and_no_result_boundary(self) -> None:
        text = (ROOT / ONE_SIX_SOURCE_RUNTIME_PATH).read_text(encoding="utf-8")
        self.assertIn('"technique_id":"HL_ONE_SIX_COMMON_ROOT"', text)
        self.assertIn('"direct_event_permission":"NO","direct_endpoint_permission":"NO"', text)
        for clause_id in ONE_SIX_SOURCE_CLAUSE_IDS:
            self.assertIn(f'"clause_id":"{clause_id}"', text)
        self.assertIn("由命宫逆数六位，为疾厄宫。", text)
        self.assertIn("此关系称为“一六共宗”。", text)
        self.assertIn("以财帛为本宫，田宅为第六位，", text)
        self.assertEqual("8401f1d190e3ee4b87aab86f82216972bea7dde8", ONE_SIX_SOURCE_RUNTIME_BLOB_SHA)

    def test_r7_state_is_deterministic_and_bound_to_r2_hashes(self) -> None:
        rerun = self.r7_runtime.generate_from_candidate(
            self.candidate,
            self.r1_state,
            self.r2_state,
            self.r7_profile,
        )
        self.assertEqual(self.r7_state, rerun)
        self.assertEqual(self.r2_state.hashes.fact_hash, self.r7_state.upstream_r2_fact_hash)
        self.assertEqual(
            self.r2_state.hashes.computation_hash,
            self.r7_state.upstream_r2_computation_hash,
        )
        self.assertEqual("PASS", self.r7_state.integrity.status)
        self.assertEqual("PASS", validate_one_six_state(self.r2_state, self.r7_state).status)

    def test_tampered_one_six_target_is_rejected_by_integrity(self) -> None:
        first = self.r7_state.one_six_facts[0]
        tampered_first = replace(first, target_designation_id="WEALTH")
        tampered_facts = (tampered_first,) + self.r7_state.one_six_facts[1:]
        tampered_hashes = one_six_hash_bundle(
            self.r7_state.upstream_r2_fact_hash,
            self.r7_state.upstream_r2_computation_hash,
            self.r7_state.profile,
            self.r7_state.time_layer,
            tampered_facts,
        )
        tampered = replace(self.r7_state, one_six_facts=tampered_facts, hashes=tampered_hashes)
        report = validate_one_six_state(self.r2_state, tampered)
        self.assertEqual("FAIL", report.status)
        self.assertIn("ONE_SIX_FACT_PROJECTION_MISMATCH", {row.code for row in report.diagnostics})

    def test_direct_result_permission_tamper_is_rejected(self) -> None:
        first = replace(self.r7_state.one_six_facts[0], direct_event_permission=True)
        facts = (first,) + self.r7_state.one_six_facts[1:]
        hashes = one_six_hash_bundle(
            self.r7_state.upstream_r2_fact_hash,
            self.r7_state.upstream_r2_computation_hash,
            self.r7_state.profile,
            self.r7_state.time_layer,
            facts,
        )
        report = validate_one_six_state(
            self.r2_state,
            replace(self.r7_state, one_six_facts=facts, hashes=hashes),
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("ILLEGAL_ONE_SIX_RESULT_PERMISSION", {row.code for row in report.diagnostics})

    def test_non_natal_time_layer_is_rejected(self) -> None:
        with self.assertRaises(OneSixGenerationError) as ctx:
            self.r7_runtime.generate_from_candidate(
                self.candidate,
                self.r1_state,
                self.r2_state,
                self.r7_profile,
                time_layer="ANNUAL",
            )
        self.assertEqual("UNSUPPORTED_ONE_SIX_TIME_LAYER", ctx.exception.diagnostic_code)


if __name__ == "__main__":
    unittest.main()

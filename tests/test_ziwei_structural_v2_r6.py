from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import Sex, ZiweiChartFoundation, ZiweiChartRequest, ziwei_chart_engine_v1_profile
from fortune_training.ziwei_structural import ZiweiStructuralRuntime, ziwei_structural_v2_r1_profile
from fortune_training.ziwei_structural.r2 import ZiweiRelativePalaceFrameRuntime, ziwei_structural_v2_r2_profile
from fortune_training.ziwei_structural.r6 import (
    QISHU_CLOCKWISE_OFFSET,
    QISHU_MAPPING_SPECS,
    QISHU_RELATIVE_ORDINAL,
    QISHU_SOURCE_RUNTIME_BLOB_SHA,
    QISHU_SOURCE_RUNTIME_PATH,
    QiShuGenerationError,
    ZiweiQiShuPositionRuntime,
    qishu_hash_bundle,
    validate_qishu_state,
    ziwei_structural_v2_r6_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R6Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.natal_profile = ziwei_chart_engine_v1_profile(registry)
        cls.natal_runtime = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        cls.r1_profile = ziwei_structural_v2_r1_profile()
        cls.r1_runtime = ZiweiStructuralRuntime()
        cls.r2_profile = ziwei_structural_v2_r2_profile()
        cls.r2_runtime = ZiweiRelativePalaceFrameRuntime()
        cls.r6_profile = ziwei_structural_v2_r6_profile()
        cls.r6_runtime = ZiweiQiShuPositionRuntime()

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
        cls.r2_state = cls.r2_runtime.generate_from_candidate(cls.candidate, cls.r1_state, cls.r2_profile)
        cls.r6_state = cls.r6_runtime.generate_from_candidate(
            cls.candidate, cls.r1_state, cls.r2_state, cls.r6_profile
        )

    def test_profile_freezes_r2_ordinal_9_clockwise_offset_4(self) -> None:
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R6", self.r6_profile.profile_id)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R2", self.r6_profile.upstream_r2_profile_id)
        self.assertEqual(9, self.r6_profile.relative_ordinal)
        self.assertEqual(4, self.r6_profile.clockwise_offset)
        self.assertEqual("NATAL", self.r6_profile.supported_time_layer)

    def test_s04_qs_01_through_12_match_r2_geometry_exactly(self) -> None:
        expected_pairs = (
            ("S04-QS-01", "LIFE", "CAREER"),
            ("S04-QS-02", "SIBLINGS", "PROPERTY"),
            ("S04-QS-03", "SPOUSE", "FORTUNE"),
            ("S04-QS-04", "CHILDREN", "PARENTS"),
            ("S04-QS-05", "WEALTH", "LIFE"),
            ("S04-QS-06", "HEALTH", "SIBLINGS"),
            ("S04-QS-07", "TRAVEL", "SPOUSE"),
            ("S04-QS-08", "SERVANTS_FRIENDS", "CHILDREN"),
            ("S04-QS-09", "CAREER", "WEALTH"),
            ("S04-QS-10", "PROPERTY", "HEALTH"),
            ("S04-QS-11", "FORTUNE", "TRAVEL"),
            ("S04-QS-12", "PARENTS", "SERVANTS_FRIENDS"),
        )
        actual = tuple(
            (row.source_mapping_id, row.origin_designation_id, row.target_designation_id)
            for row in self.r6_state.qishu_facts
        )
        self.assertEqual(expected_pairs, actual)
        r2_by_key = {
            (row.origin_designation_id, row.relative_ordinal): row
            for row in self.r2_state.frame_facts
        }
        for row in self.r6_state.qishu_facts:
            self.assertEqual(QISHU_RELATIVE_ORDINAL, row.relative_ordinal)
            self.assertEqual(QISHU_CLOCKWISE_OFFSET, row.clockwise_offset)
            upstream = r2_by_key[(row.origin_designation_id, QISHU_RELATIVE_ORDINAL)]
            self.assertEqual("CAREER", upstream.relative_role_designation_id)
            self.assertEqual(upstream.target_designation_id, row.target_designation_id)
            self.assertEqual(upstream.origin_address, row.origin_address)
            self.assertEqual(upstream.target_address, row.target_address)
            self.assertEqual(upstream.clockwise_offset, row.clockwise_offset)

    def test_s04_runtime_source_contains_all_12_frozen_rows_and_meanings(self) -> None:
        text = (ROOT / QISHU_SOURCE_RUNTIME_PATH).read_text(encoding="utf-8")
        labels = {
            "LIFE": "命宫",
            "SIBLINGS": "兄弟宫",
            "SPOUSE": "夫妻宫",
            "CHILDREN": "子女宫",
            "WEALTH": "财帛宫",
            "HEALTH": "疾厄宫",
            "TRAVEL": "迁移宫",
            "SERVANTS_FRIENDS": "交友宫",
            "CAREER": "官禄宫",
            "PROPERTY": "田宅宫",
            "FORTUNE": "福德宫",
            "PARENTS": "父母宫",
        }
        self.assertEqual(12, len(QISHU_MAPPING_SPECS))
        for spec in QISHU_MAPPING_SPECS:
            row_prefix = f"| {spec.source_mapping_id} | {labels[spec.origin_designation_id]} | {labels[spec.target_designation_id]} | {spec.fixed_support_meaning} |"
            self.assertIn(row_prefix, text)
        self.assertIn("气数位见禄=成功`固定非法", text)
        self.assertIn("气数位见忌=失败`固定非法", text)
        self.assertIn("S04只提供词表，不对实际命盘赋值", text)
        self.assertEqual("8401f1d190e3ee4b87aab86f82216972bea7dde8", QISHU_SOURCE_RUNTIME_BLOB_SHA)

    def test_r6_state_is_deterministic_and_bound_to_r2_hashes(self) -> None:
        rerun = self.r6_runtime.generate_from_candidate(
            self.candidate, self.r1_state, self.r2_state, self.r6_profile
        )
        self.assertEqual(self.r6_state, rerun)
        self.assertEqual(self.r2_state.hashes.fact_hash, self.r6_state.upstream_r2_fact_hash)
        self.assertEqual(self.r2_state.hashes.computation_hash, self.r6_state.upstream_r2_computation_hash)
        self.assertEqual("PASS", self.r6_state.integrity.status)
        self.assertEqual("PASS", validate_qishu_state(self.r2_state, self.r6_state).status)

    def test_tampered_qishu_fact_is_rejected_by_integrity(self) -> None:
        first = self.r6_state.qishu_facts[0]
        tampered_first = replace(first, target_designation_id="WEALTH")
        tampered_facts = (tampered_first,) + self.r6_state.qishu_facts[1:]
        tampered_hashes = qishu_hash_bundle(
            self.r6_state.upstream_r2_fact_hash,
            self.r6_state.upstream_r2_computation_hash,
            self.r6_state.profile,
            self.r6_state.time_layer,
            tampered_facts,
        )
        tampered = replace(self.r6_state, qishu_facts=tampered_facts, hashes=tampered_hashes)
        report = validate_qishu_state(self.r2_state, tampered)
        self.assertEqual("FAIL", report.status)
        self.assertIn("QISHU_FACT_PROJECTION_MISMATCH", {row.code for row in report.diagnostics})

    def test_non_natal_time_layer_is_rejected(self) -> None:
        with self.assertRaises(QiShuGenerationError) as ctx:
            self.r6_runtime.generate_from_candidate(
                self.candidate,
                self.r1_state,
                self.r2_state,
                self.r6_profile,
                time_layer="ANNUAL",
            )
        self.assertEqual("UNSUPPORTED_QISHU_TIME_LAYER", ctx.exception.diagnostic_code)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import (
    Sex,
    ZiweiChartFoundation,
    ZiweiChartRequest,
    ziwei_chart_engine_v1_profile,
)
from fortune_training.ziwei_structural import ZiweiStructuralRuntime, ziwei_structural_v2_r1_profile
from fortune_training.ziwei_structural.r2 import (
    ZiweiRelativePalaceFrameRuntime,
    ziwei_structural_v2_r2_profile,
)
from fortune_training.ziwei_structural.r3 import (
    ZiweiBorrowProjectionRuntime,
    ziwei_structural_v2_r3_profile,
)
from fortune_training.ziwei_structural.r4 import (
    ZiweiNamedStructuralSemanticRuntime,
    ziwei_structural_v2_r4_profile,
)
from fortune_training.ziwei_structural.r5 import (
    ResolvedStructuralGenerationError,
    ZiweiResolvedStructuralRuntime,
    ziwei_structural_v2_r5_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R5ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        natal_profile = ziwei_chart_engine_v1_profile(registry)
        natal_runtime = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        request = ZiweiChartRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex=Sex.MALE,
            profile=natal_profile,
        )
        typed = natal_runtime.resolve_typed(request)
        if typed.status != "RESOLVED" or len(typed.candidates) != 1:
            raise AssertionError(f"unexpected V1 typed resolution: {typed.status}")
        candidate = typed.candidates[0]

        r1_state = ZiweiStructuralRuntime().generate_from_candidate(
            candidate,
            ziwei_structural_v2_r1_profile(),
        )
        r2_state = ZiweiRelativePalaceFrameRuntime().generate_from_candidate(
            candidate,
            r1_state,
            ziwei_structural_v2_r2_profile(),
        )
        cls.r3_state = ZiweiBorrowProjectionRuntime().generate_from_candidate(
            candidate,
            r1_state,
            r2_state,
            ziwei_structural_v2_r3_profile(),
        )
        cls.r4_state = ZiweiNamedStructuralSemanticRuntime().generate(
            r2_state,
            ziwei_structural_v2_r4_profile(),
        )
        cls.r5_runtime = ZiweiResolvedStructuralRuntime()
        cls.r5_profile = ziwei_structural_v2_r5_profile()

    def test_stale_r3_pass_and_hashes_cannot_hide_tampered_member(self) -> None:
        original = self.r3_state.member_facts[0]
        tampered_member = replace(
            original,
            structure_physical_key="STRUCTURE-PHYSICAL:" + "0" * 64,
        )
        tampered = replace(
            self.r3_state,
            member_facts=(tampered_member, *self.r3_state.member_facts[1:]),
        )
        self.assertEqual("PASS", tampered.integrity.status)
        self.assertEqual(self.r3_state.hashes, tampered.hashes)
        with self.assertRaises(ResolvedStructuralGenerationError) as caught:
            self.r5_runtime.generate(tampered, self.r4_state, self.r5_profile)
        self.assertEqual("UPSTREAM_R3_HASH_MISMATCH", caught.exception.diagnostic_code)

    def test_stale_r4_pass_and_hashes_cannot_hide_tampered_semantic_frame(self) -> None:
        original = self.r4_state.sanfang_sizheng_frames[0]
        tampered_frame = replace(original, trine_group_key="TRINE_GROUP:TAMPER")
        tampered = replace(
            self.r4_state,
            sanfang_sizheng_frames=(tampered_frame, *self.r4_state.sanfang_sizheng_frames[1:]),
        )
        self.assertEqual("PASS", tampered.integrity.status)
        self.assertEqual(self.r4_state.hashes, tampered.hashes)
        with self.assertRaises(ResolvedStructuralGenerationError) as caught:
            self.r5_runtime.generate(self.r3_state, tampered, self.r5_profile)
        self.assertEqual("UPSTREAM_R4_HASH_MISMATCH", caught.exception.diagnostic_code)

    def test_r3_and_r4_integrity_algorithm_lineage_is_rechecked(self) -> None:
        tampered_r3 = replace(
            self.r3_state,
            integrity=replace(self.r3_state.integrity, algorithm_version="TAMPERED"),
        )
        with self.assertRaises(ResolvedStructuralGenerationError) as caught_r3:
            self.r5_runtime.generate(tampered_r3, self.r4_state, self.r5_profile)
        self.assertEqual(
            "UPSTREAM_R3_INTEGRITY_LINEAGE_INVALID",
            caught_r3.exception.diagnostic_code,
        )

        tampered_r4 = replace(
            self.r4_state,
            integrity=replace(self.r4_state.integrity, algorithm_version="TAMPERED"),
        )
        with self.assertRaises(ResolvedStructuralGenerationError) as caught_r4:
            self.r5_runtime.generate(self.r3_state, tampered_r4, self.r5_profile)
        self.assertEqual(
            "UPSTREAM_R4_INTEGRITY_LINEAGE_INVALID",
            caught_r4.exception.diagnostic_code,
        )


if __name__ == "__main__":
    unittest.main()

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
from fortune_training.ziwei_structural.r4 import (
    NamedSemanticGenerationError,
    ZiweiNamedStructuralSemanticRuntime,
    ziwei_structural_v2_r4_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R4ReleaseTests(unittest.TestCase):
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
        cls.r2_state = ZiweiRelativePalaceFrameRuntime().generate_from_candidate(
            candidate,
            r1_state,
            ziwei_structural_v2_r2_profile(),
        )
        cls.r4_runtime = ZiweiNamedStructuralSemanticRuntime()
        cls.r4_profile = ziwei_structural_v2_r4_profile()

    def test_stale_pass_and_hashes_cannot_hide_tampered_unused_r2_fact(self) -> None:
        facts = list(self.r2_state.frame_facts)
        index = next(i for i, row in enumerate(facts) if row.clockwise_offset == 1)
        original = facts[index]
        replacement_target = "SIBLINGS" if original.target_designation_id != "SIBLINGS" else "LIFE"
        facts[index] = replace(original, target_designation_id=replacement_target)
        tampered = replace(self.r2_state, frame_facts=tuple(facts))

        self.assertEqual("PASS", tampered.integrity.status)
        self.assertEqual(self.r2_state.hashes, tampered.hashes)
        with self.assertRaises(NamedSemanticGenerationError) as caught:
            self.r4_runtime.generate(tampered, self.r4_profile)
        self.assertEqual("UPSTREAM_R2_HASH_MISMATCH", caught.exception.diagnostic_code)

    def test_r2_integrity_algorithm_lineage_is_rechecked_before_r4_compilation(self) -> None:
        tampered_integrity = replace(
            self.r2_state.integrity,
            algorithm_version="TAMPERED",
        )
        tampered = replace(self.r2_state, integrity=tampered_integrity)
        with self.assertRaises(NamedSemanticGenerationError) as caught:
            self.r4_runtime.generate(tampered, self.r4_profile)
        self.assertEqual(
            "UPSTREAM_R2_INTEGRITY_LINEAGE_MISMATCH",
            caught.exception.diagnostic_code,
        )


if __name__ == "__main__":
    unittest.main()

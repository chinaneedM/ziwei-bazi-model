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
    validate_relative_frame_state,
    ziwei_structural_v2_r2_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R2TamperTests(unittest.TestCase):
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
        cls.candidate = typed.candidates[0]
        cls.r1_state = ZiweiStructuralRuntime().generate_from_candidate(
            cls.candidate,
            ziwei_structural_v2_r1_profile(),
        )
        cls.r2_state = ZiweiRelativePalaceFrameRuntime().generate_from_candidate(
            cls.candidate,
            cls.r1_state,
            ziwei_structural_v2_r2_profile(),
        )
        cls.target_index = next(
            index
            for index, row in enumerate(cls.r2_state.frame_facts)
            if row.origin_designation_id == "LIFE" and row.relative_ordinal == 9
        )
        cls.original = cls.r2_state.frame_facts[cls.target_index]
        cls.binding_by_id = {
            row.designation_id: row
            for row in cls.candidate.chart.structure.designation_bindings
        }

    def _report_for(self, tampered_row):
        facts = list(self.r2_state.frame_facts)
        facts[self.target_index] = tampered_row
        state = replace(self.r2_state, frame_facts=tuple(facts))
        report = validate_relative_frame_state(self.candidate.chart, self.r1_state, state)
        self.assertEqual("FAIL", report.status)
        codes = {row.code for row in report.diagnostics}
        self.assertIn("RELATIVE_FRAME_FACT_HASH_MISMATCH", codes)
        self.assertIn("RELATIVE_FRAME_COMPUTATION_HASH_MISMATCH", codes)
        return codes

    def test_target_designation_tamper_fails_closed(self) -> None:
        codes = self._report_for(
            replace(self.original, target_designation_id="PROPERTY")
        )
        self.assertIn("RELATIVE_TARGET_DESIGNATION_MISMATCH", codes)
        self.assertIn("INCOMPLETE_RELATIVE_TARGET_COVERAGE", codes)

    def test_target_address_tamper_fails_closed(self) -> None:
        codes = self._report_for(
            replace(
                self.original,
                target_address=self.binding_by_id["PROPERTY"].address,
            )
        )
        self.assertIn("TARGET_ADDRESS_MISMATCH", codes)
        self.assertIn("RELATIVE_OFFSET_TARGET_MISMATCH", codes)
        self.assertIn("MISSING_UPSTREAM_TOPOLOGY_FACT", codes)

    def test_relative_ordinal_tamper_fails_closed(self) -> None:
        codes = self._report_for(replace(self.original, relative_ordinal=8))
        self.assertIn("DUPLICATE_RELATIVE_FRAME_KEY", codes)
        self.assertIn("NON_CANONICAL_RELATIVE_FRAME_ORDER", codes)
        self.assertIn("RELATIVE_ROLE_MISMATCH", codes)
        self.assertIn("RELATIVE_TARGET_DESIGNATION_MISMATCH", codes)


if __name__ == "__main__":
    unittest.main()

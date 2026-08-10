from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import (
    Sex,
    ZiweiChartFoundation,
    ZiweiChartRequest,
    ziwei_chart_engine_v1_profile,
)
from fortune_training.ziwei_structural import ZiweiStructuralRuntime, ziwei_structural_v2_r1_profile
from fortune_training.ziwei_structural.r2 import (
    ZiweiRelativePalaceFrameRuntime,
    canonical_designation_ids,
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
    RESOLVED_MEMBER_OFFSETS,
    RESOLVED_MEMBER_ROLE_BY_OFFSET,
    ResolvedStructuralGenerationError,
    ZiweiResolvedStructuralRuntime,
    resolved_structural_fact_projection,
    resolved_structural_hash_bundle,
    validate_resolved_structural_state,
    ziwei_structural_v2_r5_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.natal_profile = ziwei_chart_engine_v1_profile(registry)
        cls.natal_runtime = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        cls.r1_profile = ziwei_structural_v2_r1_profile()
        cls.r1_runtime = ZiweiStructuralRuntime()
        cls.r2_profile = ziwei_structural_v2_r2_profile()
        cls.r2_runtime = ZiweiRelativePalaceFrameRuntime()
        cls.r3_profile = ziwei_structural_v2_r3_profile()
        cls.r3_runtime = ZiweiBorrowProjectionRuntime()
        cls.r4_profile = ziwei_structural_v2_r4_profile()
        cls.r4_runtime = ZiweiNamedStructuralSemanticRuntime()
        cls.r5_profile = ziwei_structural_v2_r5_profile()
        cls.r5_runtime = ZiweiResolvedStructuralRuntime()

        cls.candidate = cls._candidate(datetime(1994, 5, 17, 14, 30), registry)
        cls.r1_state = cls.r1_runtime.generate_from_candidate(cls.candidate, cls.r1_profile)
        cls.r2_state = cls.r2_runtime.generate_from_candidate(
            cls.candidate, cls.r1_state, cls.r2_profile
        )
        cls.r3_state = cls.r3_runtime.generate_from_candidate(
            cls.candidate, cls.r1_state, cls.r2_state, cls.r3_profile
        )
        cls.r4_state = cls.r4_runtime.generate(cls.r2_state, cls.r4_profile)
        cls.r5_state = cls.r5_runtime.generate(cls.r3_state, cls.r4_state, cls.r5_profile)

        cls.other_candidate = cls._candidate(datetime(1992, 6, 10, 14, 0), registry)
        cls.other_r1_state = cls.r1_runtime.generate_from_candidate(
            cls.other_candidate, cls.r1_profile
        )
        cls.other_r2_state = cls.r2_runtime.generate_from_candidate(
            cls.other_candidate, cls.other_r1_state, cls.r2_profile
        )
        cls.other_r4_state = cls.r4_runtime.generate(cls.other_r2_state, cls.r4_profile)

    @classmethod
    def _candidate(cls, value: datetime, registry: PolicyRegistry):
        request = ZiweiChartRequest(
            birth=BirthInput(
                reported_local_datetime=value,
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
        return typed.candidates[0]

    @staticmethod
    def _schema() -> dict:
        return json.loads(
            (ROOT / "schemas" / "ziwei-resolved-structural-view-v2-r5.schema.json").read_text(
                encoding="utf-8"
            )
        )

    def test_r5_profile_and_upstream_bindings_are_frozen(self) -> None:
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R5", self.r5_profile.profile_id)
        self.assertEqual("1.0.0", self.r5_profile.profile_version)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R3", self.r5_profile.upstream_r3_profile_id)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R4", self.r5_profile.upstream_r4_profile_id)
        self.assertEqual("NATAL", self.r5_profile.supported_time_layer)

    def test_birth_to_r5_handoff_has_12_frames_and_48_references(self) -> None:
        state = self.r5_state
        self.assertEqual("ZIWEI-RESOLVED-STRUCTURAL-VIEW-STATE-V2-R5", state.schema)
        self.assertEqual("NATAL", state.time_layer)
        self.assertEqual(12, len(state.frames))
        self.assertEqual(48, sum(len(frame.members) for frame in state.frames))
        self.assertEqual("PASS", state.integrity.status)
        self.assertFalse(state.integrity.diagnostics)
        self.assertEqual(self.r3_state.hashes.fact_hash, state.upstream_r3_fact_hash)
        self.assertEqual(self.r3_state.hashes.computation_hash, state.upstream_r3_computation_hash)
        self.assertEqual(self.r4_state.hashes.fact_hash, state.upstream_r4_fact_hash)
        self.assertEqual(self.r4_state.hashes.computation_hash, state.upstream_r4_computation_hash)
        self.assertEqual(list(canonical_designation_ids()), [row.origin_designation_id for row in state.frames])
        for frame in state.frames:
            self.assertEqual(list(RESOLVED_MEMBER_OFFSETS), [row.member_offset for row in frame.members])
            self.assertEqual(
                [RESOLVED_MEMBER_ROLE_BY_OFFSET[offset] for offset in RESOLVED_MEMBER_OFFSETS],
                [row.semantic_role for row in frame.members],
            )

    def test_r5_is_reference_only_and_preserves_r3_physical_identity(self) -> None:
        rendered = json.dumps(json_value(self.r5_state), ensure_ascii=False)
        self.assertNotIn("projected_placements", rendered)
        self.assertNotIn("projected_transformations", rendered)

        r3_by_key = {
            (row.evaluation_origin_designation_id, row.member_offset): row
            for row in self.r3_state.member_facts
        }
        for frame in self.r5_state.frames:
            for member in frame.members:
                r3_member = r3_by_key[(frame.origin_designation_id, member.member_offset)]
                self.assertEqual(r3_member.structure_physical_key, member.structure_physical_key)
                self.assertEqual(r3_member.closure_status, member.closure_status)
                self.assertEqual(r3_member.borrowed_from_raw_address, member.borrowed_from_raw_address)
                if member.closure_status == "DIRECT_PHYSICAL":
                    self.assertEqual(member.target_raw_address, member.physical_source_address)
                elif member.closure_status == "BORROWED_DIRECT":
                    self.assertEqual(member.borrowed_from_raw_address, member.physical_source_address)
                else:
                    self.assertIsNone(member.physical_source_address)

    def test_r4_semantic_identity_is_preserved_without_new_axis_or_group_identity(self) -> None:
        r4_by_origin = {
            row.origin_designation_id: row for row in self.r4_state.sanfang_sizheng_frames
        }
        for frame in self.r5_state.frames:
            semantic = r4_by_origin[frame.origin_designation_id]
            self.assertEqual(semantic.trine_group_key, frame.trine_group_key)
            self.assertEqual(semantic.opposition_axis_key, frame.opposition_axis_key)
            by_offset = {row.member_offset: row for row in frame.members}
            self.assertEqual(semantic.trine_partner_designation_ids[0], by_offset[4].target_designation_id)
            self.assertEqual(semantic.opposition_designation_id, by_offset[6].target_designation_id)
            self.assertEqual(semantic.trine_partner_designation_ids[1], by_offset[8].target_designation_id)

    def test_schema_validation(self) -> None:
        schema = self._schema()
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(json_value(self.r5_state)),
            key=lambda row: list(row.absolute_path),
        )
        if errors:
            rendered = "\n".join(
                f"{'.'.join(str(part) for part in row.absolute_path) or '<root>'}: {row.message}"
                for row in errors
            )
            self.fail(f"R5 schema validation failed:\n{rendered}")

    def test_projection_and_hashes_are_input_order_independent(self) -> None:
        state = self.r5_state
        forward = resolved_structural_fact_projection(
            state.upstream_r3_fact_hash,
            state.upstream_r4_fact_hash,
            state.time_layer,
            state.frames,
        )
        reversed_frames = tuple(
            replace(frame, members=tuple(reversed(frame.members)))
            for frame in reversed(state.frames)
        )
        reverse = resolved_structural_fact_projection(
            state.upstream_r3_fact_hash,
            state.upstream_r4_fact_hash,
            state.time_layer,
            reversed_frames,
        )
        self.assertEqual(forward, reverse)

        forward_hashes = resolved_structural_hash_bundle(
            state.upstream_r3_fact_hash,
            state.upstream_r3_computation_hash,
            state.upstream_r4_fact_hash,
            state.upstream_r4_computation_hash,
            self.r5_profile,
            state.time_layer,
            state.frames,
        )
        reverse_hashes = resolved_structural_hash_bundle(
            state.upstream_r3_fact_hash,
            state.upstream_r3_computation_hash,
            state.upstream_r4_fact_hash,
            state.upstream_r4_computation_hash,
            self.r5_profile,
            state.time_layer,
            reversed_frames,
        )
        self.assertEqual(forward_hashes, reverse_hashes)

    def test_profile_lineage_changes_computation_hash_not_fact_hash(self) -> None:
        changed_profile = replace(self.r5_profile, profile_version="1.0.1")
        changed = resolved_structural_hash_bundle(
            self.r5_state.upstream_r3_fact_hash,
            self.r5_state.upstream_r3_computation_hash,
            self.r5_state.upstream_r4_fact_hash,
            self.r5_state.upstream_r4_computation_hash,
            changed_profile,
            self.r5_state.time_layer,
            self.r5_state.frames,
        )
        self.assertEqual(self.r5_state.hashes.fact_hash, changed.fact_hash)
        self.assertNotEqual(self.r5_state.hashes.computation_hash, changed.computation_hash)
        with self.assertRaises(ValueError):
            changed_profile.validate()

    def test_tampered_structure_and_semantic_references_fail_closed(self) -> None:
        frame = self.r5_state.frames[0]
        member = frame.members[0]
        tampered_member = replace(member, structure_physical_key="STRUCTURE-PHYSICAL:" + "0" * 64)
        tampered_frame = replace(frame, members=(tampered_member, *frame.members[1:]))
        tampered_state = replace(self.r5_state, frames=(tampered_frame, *self.r5_state.frames[1:]))
        report = validate_resolved_structural_state(self.r3_state, self.r4_state, tampered_state)
        self.assertEqual("FAIL", report.status)
        self.assertIn("RESOLVED_R3_REFERENCE_MISMATCH", {row.code for row in report.diagnostics})

        tampered_group = replace(frame, trine_group_key="TRINE_GROUP:TAMPER")
        tampered_group_state = replace(
            self.r5_state, frames=(tampered_group, *self.r5_state.frames[1:])
        )
        group_report = validate_resolved_structural_state(
            self.r3_state, self.r4_state, tampered_group_state
        )
        self.assertEqual("FAIL", group_report.status)
        self.assertIn(
            "RESOLVED_TRINE_GROUP_KEY_MISMATCH",
            {row.code for row in group_report.diagnostics},
        )

    def test_tampered_upstream_hashes_and_cross_r3_r4_fail_closed(self) -> None:
        tampered_r3 = replace(
            self.r3_state,
            hashes=replace(self.r3_state.hashes, fact_hash="0" * 64),
        )
        with self.assertRaises(ResolvedStructuralGenerationError):
            self.r5_runtime.generate(tampered_r3, self.r4_state, self.r5_profile)

        with self.assertRaises(ResolvedStructuralGenerationError) as ctx:
            self.r5_runtime.generate(self.r3_state, self.other_r4_state, self.r5_profile)
        self.assertIn(
            ctx.exception.diagnostic_code,
            {
                "CROSS_R3_R4_R2_FACT_HASH_MISMATCH",
                "CROSS_R3_R4_R2_COMPUTATION_HASH_MISMATCH",
            },
        )

    def test_generation_is_deterministic_and_dynamic_layer_fails_closed(self) -> None:
        replay = self.r5_runtime.generate(self.r3_state, self.r4_state, self.r5_profile)
        self.assertEqual(self.r5_state.frames, replay.frames)
        self.assertEqual(self.r5_state.hashes, replay.hashes)
        self.assertEqual(self.r5_state.integrity, replay.integrity)
        with self.assertRaises(ResolvedStructuralGenerationError):
            self.r5_runtime.generate(
                self.r3_state,
                self.r4_state,
                self.r5_profile,
                time_layer="DAXIAN",
            )


if __name__ == "__main__":
    unittest.main()

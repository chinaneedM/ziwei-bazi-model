from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

import fortune_training.ziwei_structural as ziwei_structural
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
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
from fortune_training.ziwei_structural.r4 import (
    S04_CANONICAL_MANIFEST_OBJECT_SHA256,
    S04_CANONICAL_SOURCE_SHA256,
    S04_SANFANG_SIZHENG_RULE_SET_ID,
    NamedSemanticGenerationError,
    ZiweiNamedStructuralSemanticRuntime,
    named_semantic_fact_projection,
    named_semantic_hash_bundle,
    validate_named_semantic_state,
    ziwei_structural_v2_r4_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.natal_profile = ziwei_chart_engine_v1_profile(registry)
        cls.natal_runtime = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        cls.r1_profile = ziwei_structural_v2_r1_profile()
        cls.r1_runtime = ZiweiStructuralRuntime()
        cls.r2_profile = ziwei_structural_v2_r2_profile()
        cls.r2_runtime = ZiweiRelativePalaceFrameRuntime()
        cls.r4_profile = ziwei_structural_v2_r4_profile()
        cls.r4_runtime = ZiweiNamedStructuralSemanticRuntime()

        cls.candidate = cls._candidate(datetime(1994, 5, 17, 14, 30), registry)
        cls.r1_state = cls.r1_runtime.generate_from_candidate(cls.candidate, cls.r1_profile)
        cls.r2_state = cls.r2_runtime.generate_from_candidate(
            cls.candidate,
            cls.r1_state,
            cls.r2_profile,
        )
        cls.r4_state = cls.r4_runtime.generate(cls.r2_state, cls.r4_profile)

        cls.other_candidate = cls._candidate(datetime(1992, 6, 10, 14, 0), registry)
        cls.other_r1_state = cls.r1_runtime.generate_from_candidate(
            cls.other_candidate,
            cls.r1_profile,
        )
        cls.other_r2_state = cls.r2_runtime.generate_from_candidate(
            cls.other_candidate,
            cls.other_r1_state,
            cls.r2_profile,
        )

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
            (ROOT / "schemas" / "ziwei-named-structural-semantics-v2-r4.schema.json").read_text(
                encoding="utf-8"
            )
        )

    def test_source_binding_matches_current_git_canonical_correction(self) -> None:
        manifest = json.loads((ROOT / "sources" / "canonical-manifest.json").read_text(encoding="utf-8"))
        source_policy = json.loads((ROOT / "config" / "source-policy.json").read_text(encoding="utf-8"))
        s04 = next(row for row in manifest["sources"] if row["source_id"] == "S04")
        self.assertEqual(1_435_537, s04["bytes"])
        self.assertEqual(S04_CANONICAL_SOURCE_SHA256, s04["sha256"])
        self.assertEqual(S04_CANONICAL_MANIFEST_OBJECT_SHA256, object_sha256(manifest))
        self.assertEqual(S04_CANONICAL_MANIFEST_OBJECT_SHA256, source_policy["canonical_manifest_sha256"])

        segment = (ROOT / "sources" / "canonical-runtime" / "S04" / "segment-0001.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"PATCH_ID={S04_SANFANG_SIZHENG_RULE_SET_ID}", segment)
        self.assertIn("PATCH_STATUS=ACTIVE_HIGHEST_PRECEDENCE", segment)
        self.assertIn("ACTIVE_S04_SANFANG_SIZHENG_INVARIANT=OPPOSITION:+6;TRINE_SET:+4,+8", segment)

    def test_release_contracts_remain_frozen_and_r4_is_independent(self) -> None:
        self.assertEqual("2.0.0-r1", ziwei_structural.__version__)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R2", self.r2_profile.profile_id)
        self.assertEqual("1.0.0", self.r2_profile.profile_version)
        self.assertIsNone(self.r2_profile.semantic_rule_set_id)
        self.assertIsNone(self.r2_profile.semantic_rule_set_version)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R4", self.r4_profile.profile_id)
        self.assertEqual("1.0.0", self.r4_profile.profile_version)
        self.assertEqual(S04_SANFANG_SIZHENG_RULE_SET_ID, self.r4_profile.semantic_rule_set_id)

    def test_canonical_semantic_fact_counts_and_dedup_identity(self) -> None:
        state = self.r4_state
        canonical_ids = canonical_designation_ids()
        self.assertEqual(6, len(state.opposition_axes))
        self.assertEqual(4, len(state.trine_groups))
        self.assertEqual(12, len(state.sanfang_sizheng_frames))
        self.assertEqual(22, 6 + 4 + 12)
        self.assertEqual("PASS", state.integrity.status)
        self.assertFalse(state.integrity.diagnostics)

        axis_members = [member for axis in state.opposition_axes for member in axis.member_designation_ids]
        group_members = [member for group in state.trine_groups for member in group.member_designation_ids]
        self.assertCountEqual(canonical_ids, axis_members)
        self.assertCountEqual(canonical_ids, group_members)
        self.assertEqual(set(canonical_ids), {frame.origin_designation_id for frame in state.sanfang_sizheng_frames})

        axes_by_key = {row.axis_key: row for row in state.opposition_axes}
        groups_by_key = {row.group_key: row for row in state.trine_groups}
        for frame in state.sanfang_sizheng_frames:
            self.assertEqual((4, 8), frame.trine_offsets)
            self.assertEqual(6, frame.opposition_offset)
            self.assertIn(frame.opposition_axis_key, axes_by_key)
            self.assertIn(frame.trine_group_key, groups_by_key)
            self.assertEqual(
                {frame.origin_designation_id, frame.opposition_designation_id},
                set(axes_by_key[frame.opposition_axis_key].member_designation_ids),
            )
            self.assertEqual(
                {frame.origin_designation_id, *frame.trine_partner_designation_ids},
                set(groups_by_key[frame.trine_group_key].member_designation_ids),
            )

    def test_corrected_s04_rows_07_to_12_are_materialized_exactly(self) -> None:
        frames = {row.origin_designation_id: row for row in self.r4_state.sanfang_sizheng_frames}
        expected = {
            "TRAVEL": ({"SPOUSE", "FORTUNE"}, "LIFE"),
            "SERVANTS_FRIENDS": ({"CHILDREN", "PARENTS"}, "SIBLINGS"),
            "CAREER": ({"LIFE", "WEALTH"}, "SPOUSE"),
            "PROPERTY": ({"SIBLINGS", "HEALTH"}, "CHILDREN"),
            "FORTUNE": ({"SPOUSE", "TRAVEL"}, "WEALTH"),
            "PARENTS": ({"CHILDREN", "SERVANTS_FRIENDS"}, "HEALTH"),
        }
        for origin, (trines, opposite) in expected.items():
            frame = frames[origin]
            self.assertEqual(trines, set(frame.trine_partner_designation_ids), origin)
            self.assertEqual(opposite, frame.opposition_designation_id, origin)

    def test_birth_to_r2_to_r4_typed_handoff_and_schema(self) -> None:
        state = self.r4_state
        self.assertEqual("ZIWEI-NAMED-STRUCTURAL-SEMANTIC-STATE-V2-R4", state.schema)
        self.assertEqual(self.r2_state.hashes.fact_hash, state.upstream_r2_fact_hash)
        self.assertEqual(self.r2_state.hashes.computation_hash, state.upstream_r2_computation_hash)
        self.assertRegex(state.hashes.fact_hash, r"^[0-9a-f]{64}$")
        self.assertRegex(state.hashes.computation_hash, r"^[0-9a-f]{64}$")
        self.assertEqual("PASS", validate_named_semantic_state(self.r2_state, state).status)

        schema = self._schema()
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        errors = sorted(
            validator.iter_errors(json_value(state)),
            key=lambda row: list(row.absolute_path),
        )
        if errors:
            rendered = "\n".join(
                f"{'.'.join(str(part) for part in row.absolute_path) or '<root>'}: {row.message}"
                for row in errors
            )
            self.fail(f"R4 schema validation failed:\n{rendered}")

    def test_projection_and_hashes_are_input_order_independent(self) -> None:
        state = self.r4_state
        forward = named_semantic_fact_projection(
            self.r2_state.hashes.fact_hash,
            state.opposition_axes,
            state.trine_groups,
            state.sanfang_sizheng_frames,
        )
        reverse = named_semantic_fact_projection(
            self.r2_state.hashes.fact_hash,
            tuple(reversed(state.opposition_axes)),
            tuple(reversed(state.trine_groups)),
            tuple(reversed(state.sanfang_sizheng_frames)),
        )
        self.assertEqual(forward, reverse)

        forward_hashes = named_semantic_hash_bundle(
            self.r2_state.hashes.fact_hash,
            self.r2_state.hashes.computation_hash,
            self.r4_profile,
            state.opposition_axes,
            state.trine_groups,
            state.sanfang_sizheng_frames,
        )
        reverse_hashes = named_semantic_hash_bundle(
            self.r2_state.hashes.fact_hash,
            self.r2_state.hashes.computation_hash,
            self.r4_profile,
            tuple(reversed(state.opposition_axes)),
            tuple(reversed(state.trine_groups)),
            tuple(reversed(state.sanfang_sizheng_frames)),
        )
        self.assertEqual(forward_hashes, reverse_hashes)

    def test_source_lineage_changes_only_computation_hash_when_facts_are_unchanged(self) -> None:
        state = self.r4_state
        changed_source = replace(
            self.r4_profile,
            canonical_source_sha256="0" * 64,
        )
        changed = named_semantic_hash_bundle(
            self.r2_state.hashes.fact_hash,
            self.r2_state.hashes.computation_hash,
            changed_source,
            state.opposition_axes,
            state.trine_groups,
            state.sanfang_sizheng_frames,
        )
        self.assertEqual(state.hashes.fact_hash, changed.fact_hash)
        self.assertNotEqual(state.hashes.computation_hash, changed.computation_hash)
        with self.assertRaises(ValueError):
            changed_source.validate()
        with self.assertRaises(NamedSemanticGenerationError):
            self.r4_runtime.generate(self.r2_state, changed_source)

    def test_tampered_axis_group_and_frame_fail_closed(self) -> None:
        state = self.r4_state

        tampered_axis = replace(state.opposition_axes[0], axis_key="OPPOSITION_AXIS:TAMPER")
        bad_axis_state = replace(state, opposition_axes=(tampered_axis, *state.opposition_axes[1:]))
        self.assertEqual("FAIL", validate_named_semantic_state(self.r2_state, bad_axis_state).status)

        tampered_group = replace(state.trine_groups[0], group_key="TRINE_GROUP:TAMPER")
        bad_group_state = replace(state, trine_groups=(tampered_group, *state.trine_groups[1:]))
        self.assertEqual("FAIL", validate_named_semantic_state(self.r2_state, bad_group_state).status)

        tampered_frame = replace(
            state.sanfang_sizheng_frames[0],
            opposition_designation_id="SIBLINGS",
        )
        bad_frame_state = replace(
            state,
            sanfang_sizheng_frames=(tampered_frame, *state.sanfang_sizheng_frames[1:]),
        )
        self.assertEqual("FAIL", validate_named_semantic_state(self.r2_state, bad_frame_state).status)

    def test_cross_r2_composition_fails_closed(self) -> None:
        report = validate_named_semantic_state(self.other_r2_state, self.r4_state)
        self.assertEqual("FAIL", report.status)
        codes = {row.code for row in report.diagnostics}
        self.assertIn("UPSTREAM_R2_FACT_HASH_MISMATCH", codes)
        self.assertIn("UPSTREAM_R2_COMPUTATION_HASH_MISMATCH", codes)

    def test_generation_is_deterministic(self) -> None:
        replay = self.r4_runtime.generate(self.r2_state, self.r4_profile)
        self.assertEqual(self.r4_state.opposition_axes, replay.opposition_axes)
        self.assertEqual(self.r4_state.trine_groups, replay.trine_groups)
        self.assertEqual(self.r4_state.sanfang_sizheng_frames, replay.sanfang_sizheng_frames)
        self.assertEqual(self.r4_state.hashes, replay.hashes)
        self.assertEqual(self.r4_state.integrity, replay.integrity)


if __name__ == "__main__":
    unittest.main()

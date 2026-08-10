from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

import fortune_training.ziwei_chart as ziwei_chart
import fortune_training.ziwei_structural as ziwei_structural
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
    RelativeFrameGenerationError,
    ZiweiRelativePalaceFrameRuntime,
    canonical_designation_ids,
    relative_frame_fact_projection,
    relative_frame_hash_bundle,
    validate_relative_frame_state,
    ziwei_structural_v2_r2_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.natal_profile = ziwei_chart_engine_v1_profile(registry)
        cls.natal_runtime = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        cls.r1_profile = ziwei_structural_v2_r1_profile()
        cls.r1_runtime = ZiweiStructuralRuntime()
        cls.r2_profile = ziwei_structural_v2_r2_profile()
        cls.r2_runtime = ZiweiRelativePalaceFrameRuntime()

        cls.candidate = cls._candidate(
            datetime(1994, 5, 17, 14, 30),
            registry=registry,
        )
        cls.r1_state = cls.r1_runtime.generate_from_candidate(cls.candidate, cls.r1_profile)
        cls.r2_state = cls.r2_runtime.generate_from_candidate(
            cls.candidate,
            cls.r1_state,
            cls.r2_profile,
        )

        cls.other_candidate = cls._candidate(
            datetime(1992, 6, 10, 14, 0),
            registry=registry,
        )
        cls.other_r1_state = cls.r1_runtime.generate_from_candidate(
            cls.other_candidate,
            cls.r1_profile,
        )

    @classmethod
    def _candidate(cls, value: datetime, *, registry: PolicyRegistry):
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
            (ROOT / "schemas" / "ziwei-relative-palace-frame-v2-r2.schema.json").read_text(
                encoding="utf-8"
            )
        )

    def test_v1_and_r1_release_contracts_remain_frozen(self) -> None:
        self.assertEqual("1.0.0", ziwei_chart.__version__)
        self.assertEqual("2.0.0-r1", ziwei_structural.__version__)
        self.assertEqual("ZIWEI-CHART-ENGINE-V1", self.natal_profile.profile_id)
        self.assertEqual("1.0.0", self.natal_profile.profile_version)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R1", self.r1_profile.profile_id)
        self.assertEqual("1.0.0", self.r1_profile.profile_version)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R2", self.r2_profile.profile_id)
        self.assertEqual("1.0.0", self.r2_profile.profile_version)

    def test_relative_frame_is_complete_canonical_and_rotationally_covariant(self) -> None:
        facts = self.r2_state.frame_facts
        canonical_ids = canonical_designation_ids()
        self.assertEqual(12, len(canonical_ids))
        self.assertEqual(144, len(facts))
        self.assertEqual(
            [(origin, ordinal) for origin in canonical_ids for ordinal in range(1, 13)],
            [(row.origin_designation_id, row.relative_ordinal) for row in facts],
        )
        self.assertEqual(
            144,
            len({(row.origin_designation_id, row.relative_ordinal) for row in facts}),
        )

        upstream_by_id = {
            row.designation_id: row
            for row in self.candidate.chart.structure.designation_bindings
        }
        r1_edges = {
            (row.source.index, row.target.index, row.clockwise_offset)
            for row in self.r1_state.topology_facts
        }

        for origin_index, origin_id in enumerate(canonical_ids):
            origin_rows = [row for row in facts if row.origin_designation_id == origin_id]
            self.assertEqual(set(range(1, 13)), {row.relative_ordinal for row in origin_rows})
            self.assertEqual(set(canonical_ids), {row.target_designation_id for row in origin_rows})

            for role_offset, row in enumerate(origin_rows):
                expected_role_id = canonical_ids[role_offset]
                expected_target_id = canonical_ids[(origin_index + role_offset) % 12]
                self.assertEqual(expected_role_id, row.relative_role_designation_id)
                self.assertEqual(expected_target_id, row.target_designation_id)
                self.assertEqual(upstream_by_id[origin_id].address, row.origin_address)
                self.assertEqual(upstream_by_id[expected_target_id].address, row.target_address)
                self.assertEqual((-role_offset) % 12, row.clockwise_offset)
                self.assertIn(
                    (row.origin_address.index, row.target_address.index, row.clockwise_offset),
                    r1_edges,
                )

    def test_special_ordinals_are_geometry_only_without_named_semantics(self) -> None:
        canonical_ids = canonical_designation_ids()
        by_origin_ordinal = {
            (row.origin_designation_id, row.relative_ordinal): row
            for row in self.r2_state.frame_facts
        }
        expected_offsets = {1: 0, 5: 8, 6: 7, 7: 6, 9: 4}
        for origin_id in canonical_ids:
            for ordinal, expected_offset in expected_offsets.items():
                self.assertEqual(
                    expected_offset,
                    by_origin_ordinal[(origin_id, ordinal)].clockwise_offset,
                )

        self.assertIsNone(self.r2_profile.semantic_rule_set_id)
        self.assertIsNone(self.r2_profile.semantic_rule_set_version)
        serialized = json_value(self.r2_state)
        rendered = json.dumps(serialized, ensure_ascii=False).lower()
        for forbidden in (
            "opposition",
            "sanfang",
            "qishu",
            "yiliu",
            "三方",
            "对宫",
            "气数",
            "一六共宗",
        ):
            self.assertNotIn(forbidden.lower(), rendered)

        named = replace(
            self.r2_profile,
            semantic_rule_set_id="UNFROZEN-TRADITIONAL-SEMANTICS",
            semantic_rule_set_version="0.0.0",
        )
        with self.assertRaises(ValueError):
            named.validate()

    def test_birth_to_natal_to_r1_to_r2_typed_handoff_and_schema(self) -> None:
        state = self.r2_state
        self.assertEqual("ZIWEI-RELATIVE-PALACE-FRAME-STATE-V2-R2", state.schema)
        self.assertEqual(144, len(state.frame_facts))
        self.assertEqual("PASS", state.integrity.status)
        self.assertFalse(state.integrity.diagnostics)
        self.assertEqual(self.r1_state.hashes.fact_hash, state.upstream_structural_fact_hash)
        self.assertEqual(
            self.r1_state.hashes.computation_hash,
            state.upstream_structural_computation_hash,
        )
        self.assertRegex(state.hashes.fact_hash, r"^[0-9a-f]{64}$")
        self.assertRegex(state.hashes.computation_hash, r"^[0-9a-f]{64}$")
        self.assertEqual(
            "PASS",
            validate_relative_frame_state(self.candidate.chart, self.r1_state, state).status,
        )

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
            self.fail(f"relative-frame schema validation failed:\n{rendered}")

    def test_canonical_projection_and_hash_are_input_order_independent(self) -> None:
        facts = self.r2_state.frame_facts
        forward = relative_frame_fact_projection(self.r1_state.hashes.fact_hash, facts)
        reverse = relative_frame_fact_projection(
            self.r1_state.hashes.fact_hash,
            tuple(reversed(facts)),
        )
        self.assertEqual(forward, reverse)

        forward_hashes = relative_frame_hash_bundle(
            self.r1_state.hashes.fact_hash,
            self.r1_state.hashes.computation_hash,
            self.r2_profile,
            facts,
        )
        reverse_hashes = relative_frame_hash_bundle(
            self.r1_state.hashes.fact_hash,
            self.r1_state.hashes.computation_hash,
            self.r2_profile,
            tuple(reversed(facts)),
        )
        self.assertEqual(forward_hashes, reverse_hashes)

    def test_relative_frame_generation_is_deterministic(self) -> None:
        replay = self.r2_runtime.generate(
            self.candidate.chart,
            self.candidate.hashes,
            self.r1_state,
            self.r2_profile,
        )
        self.assertEqual(self.r2_state.frame_facts, replay.frame_facts)
        self.assertEqual(self.r2_state.hashes, replay.hashes)
        self.assertEqual(self.r2_state.integrity, replay.integrity)

    def test_hash_layers_bind_r1_fact_computation_profile_and_algorithm(self) -> None:
        facts = self.r2_state.frame_facts

        changed_fact = relative_frame_hash_bundle(
            "0" * 64,
            self.r1_state.hashes.computation_hash,
            self.r2_profile,
            facts,
        )
        self.assertNotEqual(self.r2_state.hashes.fact_hash, changed_fact.fact_hash)
        self.assertNotEqual(self.r2_state.hashes.computation_hash, changed_fact.computation_hash)

        changed_computation = relative_frame_hash_bundle(
            self.r1_state.hashes.fact_hash,
            "f" * 64,
            self.r2_profile,
            facts,
        )
        self.assertEqual(self.r2_state.hashes.fact_hash, changed_computation.fact_hash)
        self.assertNotEqual(
            self.r2_state.hashes.computation_hash,
            changed_computation.computation_hash,
        )

        unsupported_profile = replace(self.r2_profile, profile_version="1.0.1")
        changed_profile = relative_frame_hash_bundle(
            self.r1_state.hashes.fact_hash,
            self.r1_state.hashes.computation_hash,
            unsupported_profile,
            facts,
        )
        self.assertEqual(self.r2_state.hashes.fact_hash, changed_profile.fact_hash)
        self.assertNotEqual(self.r2_state.hashes.computation_hash, changed_profile.computation_hash)
        with self.assertRaises(ValueError):
            unsupported_profile.validate()

        unsupported_algorithm = replace(
            self.r2_profile,
            relative_frame_algorithm_version="1.0.1",
        )
        changed_algorithm = relative_frame_hash_bundle(
            self.r1_state.hashes.fact_hash,
            self.r1_state.hashes.computation_hash,
            unsupported_algorithm,
            facts,
        )
        self.assertEqual(self.r2_state.hashes.fact_hash, changed_algorithm.fact_hash)
        self.assertNotEqual(
            self.r2_state.hashes.computation_hash,
            changed_algorithm.computation_hash,
        )
        with self.assertRaises(ValueError):
            unsupported_algorithm.validate()

    def test_cross_chart_r1_and_natal_composition_fails_closed(self) -> None:
        self.assertNotEqual(self.candidate.hashes.fact_hash, self.other_candidate.hashes.fact_hash)
        with self.assertRaises(RelativeFrameGenerationError) as caught:
            self.r2_runtime.generate_from_candidate(
                self.other_candidate,
                self.r1_state,
                self.r2_profile,
            )
        self.assertEqual("CROSS_CHART_UPSTREAM_BINDING_MISMATCH", caught.exception.diagnostic_code)

    def test_tampered_frame_fails_integrity_and_hash_validation(self) -> None:
        target_index = next(
            index
            for index, row in enumerate(self.r2_state.frame_facts)
            if row.origin_designation_id == "LIFE" and row.relative_ordinal == 9
        )
        original = self.r2_state.frame_facts[target_index]
        tampered_row = replace(original, clockwise_offset=(original.clockwise_offset + 1) % 12)
        tampered_facts = list(self.r2_state.frame_facts)
        tampered_facts[target_index] = tampered_row
        tampered = replace(self.r2_state, frame_facts=tuple(tampered_facts))

        report = validate_relative_frame_state(self.candidate.chart, self.r1_state, tampered)
        self.assertEqual("FAIL", report.status)
        codes = {row.code for row in report.diagnostics}
        self.assertIn("RELATIVE_OFFSET_TARGET_MISMATCH", codes)
        self.assertIn("RELATIVE_FRAME_GEOMETRY_MISMATCH", codes)
        self.assertIn("MISSING_UPSTREAM_TOPOLOGY_FACT", codes)
        self.assertIn("RELATIVE_FRAME_FACT_HASH_MISMATCH", codes)
        self.assertIn("RELATIVE_FRAME_COMPUTATION_HASH_MISMATCH", codes)


if __name__ == "__main__":
    unittest.main()

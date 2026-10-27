from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

import fortune_training.ziwei_chart as ziwei_chart
import fortune_training.ziwei_structural as ziwei_structural
import fortune_training.ziwei_structural.r2 as ziwei_structural_r2
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import (
    Sex,
    ZiweiChartFoundation,
    ZiweiChartRequest,
    ziwei_chart_engine_v1_profile,
)
from fortune_training.ziwei_chart.dignity import MAIN_STAR_ENTITY_IDS
from fortune_training.ziwei_structural import ZiweiStructuralRuntime, ziwei_structural_v2_r1_profile
from fortune_training.ziwei_structural.r2 import (
    ZiweiRelativePalaceFrameRuntime,
    ziwei_structural_v2_r2_profile,
)
from fortune_training.ziwei_structural.r3 import (
    BORROW_MEMBER_OFFSETS,
    BorrowProjectionGenerationError,
    BorrowProjectionGenerator,
    ZiweiBorrowProjectionRuntime,
    borrow_projection_hash_bundle,
    validate_borrow_projection_state,
    ziwei_structural_v2_r3_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R3Tests(unittest.TestCase):
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
        cls.generator = BorrowProjectionGenerator()

        cls.candidate = cls._candidate(datetime(1994, 5, 17, 14, 30), registry)
        cls.r1_state = cls.r1_runtime.generate_from_candidate(cls.candidate, cls.r1_profile)
        cls.r2_state = cls.r2_runtime.generate_from_candidate(
            cls.candidate, cls.r1_state, cls.r2_profile
        )
        cls.r3_state = cls.r3_runtime.generate_from_candidate(
            cls.candidate, cls.r1_state, cls.r2_state, cls.r3_profile
        )

        cls.other_candidate = cls._candidate(datetime(1992, 6, 10, 14, 0), registry)

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
            (ROOT / "schemas" / "ziwei-borrow-projection-v2-r3.schema.json").read_text(
                encoding="utf-8"
            )
        )

    @staticmethod
    def _placements_at(chart, address_index):
        return tuple(
            sorted(
                (row for row in chart.placements if row.address.index == address_index),
                key=lambda row: row.entity_id,
            )
        )

    @staticmethod
    def _main_at(chart, address_index):
        return tuple(
            row
            for row in chart.placements
            if row.address.index == address_index and row.entity_id in MAIN_STAR_ENTITY_IDS
        )

    @classmethod
    def _source_with_main(cls, chart):
        for source_index in range(12):
            if cls._main_at(chart, source_index):
                return source_index
        raise AssertionError("test chart has no principal-star source")

    def test_release_contracts_remain_frozen_and_r3_profile_is_independent(self) -> None:
        self.assertEqual("1.0.0", ziwei_chart.__version__)
        self.assertEqual("2.0.0-r1", ziwei_structural.__version__)
        self.assertEqual("2.0.0-r2", ziwei_structural_r2.__version__)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R3", self.r3_profile.profile_id)
        self.assertEqual("1.0.0", self.r3_profile.profile_version)
        self.assertEqual("NATAL", self.r3_profile.supported_time_layer)

    def test_birth_to_v1_r1_r2_r3_handoff_and_schema(self) -> None:
        state = self.r3_state
        self.assertEqual("ZIWEI-BORROW-PROJECTION-STATE-V2-R3", state.schema)
        self.assertEqual("NATAL", state.time_layer)
        self.assertEqual(48, len(state.member_facts))
        self.assertEqual("PASS", state.integrity.status)
        self.assertFalse(state.integrity.diagnostics)
        self.assertEqual(self.r2_state.hashes.fact_hash, state.upstream_relative_frame_fact_hash)
        self.assertEqual(
            self.r2_state.hashes.computation_hash,
            state.upstream_relative_frame_computation_hash,
        )
        self.assertRegex(state.hashes.fact_hash, r"^[0-9a-f]{64}$")
        self.assertRegex(state.hashes.computation_hash, r"^[0-9a-f]{64}$")

        by_origin = {}
        for row in state.member_facts:
            by_origin.setdefault(row.evaluation_origin_designation_id, []).append(row)
        self.assertEqual(12, len(by_origin))
        for rows in by_origin.values():
            self.assertEqual(list(BORROW_MEMBER_OFFSETS), [row.member_offset for row in rows])

        schema = self._schema()
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(json_value(state)),
            key=lambda row: list(row.absolute_path),
        )
        if errors:
            rendered = "\n".join(
                f"{'.'.join(str(part) for part in row.absolute_path) or '<root>'}: {row.message}"
                for row in errors
            )
            self.fail(f"borrow projection schema validation failed:\n{rendered}")

    def test_real_projection_is_reference_only_and_complete(self) -> None:
        borrowed = [row for row in self.r3_state.member_facts if row.closure_status == "BORROWED_DIRECT"]
        direct = [row for row in self.r3_state.member_facts if row.closure_status == "DIRECT_PHYSICAL"]
        self.assertTrue(borrowed)
        self.assertTrue(direct)

        for row in direct:
            self.assertFalse(row.target_main_star_empty)
            self.assertIsNone(row.borrowed_from_raw_address)
            self.assertFalse(row.zero_second_contribution)
            self.assertEqual(
                self._placements_at(self.candidate.chart, row.target_raw_address.index),
                row.projected_placements,
            )

        for row in borrowed:
            self.assertTrue(row.target_main_star_empty)
            self.assertIsNotNone(row.borrowed_from_raw_address)
            self.assertEqual(
                (row.target_raw_address.index + 6) % 12,
                row.borrowed_from_raw_address.index,
            )
            self.assertTrue(row.zero_second_contribution)
            source_rows = self._placements_at(
                self.candidate.chart, row.borrowed_from_raw_address.index
            )
            self.assertEqual(source_rows, row.projected_placements)
            self.assertTrue(any(item.entity_id in MAIN_STAR_ENTITY_IDS for item in source_rows))
            self.assertTrue(all(item in self.candidate.chart.placements for item in row.projected_placements))

        rendered = json.dumps(json_value(self.r3_state), ensure_ascii=False).lower()
        for forbidden in ("三方四正", "左合宫", "右合宫", "pair_strength", "auspicious"):
            self.assertNotIn(forbidden.lower(), rendered)

    def test_auxiliary_only_target_remains_borrow_eligible_and_source_projects_all_placements(self) -> None:
        chart = self.candidate.chart
        source_index = self._source_with_main(chart)
        target_index = (source_index + 6) % 12

        non_main = next(row for row in chart.placements if row.entity_id not in MAIN_STAR_ENTITY_IDS)
        kept = tuple(
            row
            for row in chart.placements
            if row.entity_id != non_main.entity_id
            and not (row.address.index == target_index and row.entity_id in MAIN_STAR_ENTITY_IDS)
        )
        moved_aux = replace(non_main, address=chart.structure.designation_bindings[0].address)
        moved_aux = replace(
            moved_aux,
            address=type(moved_aux.address)(index=target_index, branch="子丑寅卯辰巳午未申酉戌亥"[target_index]),
        )
        synthetic = replace(chart, placements=kept + (moved_aux,))
        facts = self.generator.generate(synthetic, self.r2_state)
        target_rows = [row for row in facts if row.target_raw_address.index == target_index]
        self.assertTrue(target_rows)
        self.assertTrue(all(row.target_main_star_empty for row in target_rows))
        self.assertTrue(all(row.closure_status == "BORROWED_DIRECT" for row in target_rows))
        expected_source = self._placements_at(synthetic, source_index)
        self.assertTrue(expected_source)
        for row in target_rows:
            self.assertEqual(expected_source, row.projected_placements)
            self.assertNotIn(moved_aux, row.projected_placements)

    def test_double_empty_opposition_fails_closed_without_recursion(self) -> None:
        chart = self.candidate.chart
        source_index = self._source_with_main(chart)
        target_index = (source_index + 6) % 12
        synthetic = replace(
            chart,
            placements=tuple(
                row
                for row in chart.placements
                if not (
                    row.entity_id in MAIN_STAR_ENTITY_IDS
                    and row.address.index in {source_index, target_index}
                )
            ),
        )
        facts = self.generator.generate(synthetic, self.r2_state)
        target_rows = [row for row in facts if row.target_raw_address.index == target_index]
        self.assertTrue(target_rows)
        for row in target_rows:
            self.assertTrue(row.target_main_star_empty)
            self.assertEqual("BORROW_SOURCE_EMPTY_OR_UNKNOWN", row.closure_status)
            self.assertIsNone(row.borrowed_from_raw_address)
            self.assertFalse(row.projected_placements)
            self.assertFalse(row.projected_transformations)
            self.assertFalse(row.zero_second_contribution)

    def test_natal_transformations_are_projected_only_from_physical_source(self) -> None:
        chart = self.candidate.chart
        source_activation = None
        for activation in chart.transformations:
            if self._main_at(chart, activation.target_address.index):
                source_activation = activation
                break
        self.assertIsNotNone(source_activation)
        source_index = source_activation.target_address.index
        target_index = (source_index + 6) % 12
        synthetic = replace(
            chart,
            placements=tuple(
                row
                for row in chart.placements
                if not (
                    row.entity_id in MAIN_STAR_ENTITY_IDS and row.address.index == target_index
                )
            ),
        )
        facts = self.generator.generate(synthetic, self.r2_state)
        target_rows = [
            row
            for row in facts
            if row.target_raw_address.index == target_index
            and row.closure_status == "BORROWED_DIRECT"
        ]
        self.assertTrue(target_rows)
        for row in target_rows:
            self.assertIn(source_activation, row.projected_transformations)
            self.assertTrue(
                all(
                    activation.target_address.index == source_index
                    for activation in row.projected_transformations
                )
            )

    def test_structure_physical_key_deduplicates_same_physical_member_across_views(self) -> None:
        by_target = {}
        for row in self.r3_state.member_facts:
            by_target.setdefault(row.target_raw_address.index, []).append(row)
        self.assertEqual(set(range(12)), set(by_target))
        for rows in by_target.values():
            self.assertGreater(len(rows), 1)
            self.assertEqual(1, len({row.structure_physical_key for row in rows}))

    def test_hash_projection_is_order_independent_and_profile_lineage_is_separate(self) -> None:
        forward = borrow_projection_hash_bundle(
            self.r2_state.hashes.fact_hash,
            self.r2_state.hashes.computation_hash,
            self.r3_profile,
            "NATAL",
            self.r3_state.member_facts,
        )
        reverse = borrow_projection_hash_bundle(
            self.r2_state.hashes.fact_hash,
            self.r2_state.hashes.computation_hash,
            self.r3_profile,
            "NATAL",
            tuple(reversed(self.r3_state.member_facts)),
        )
        self.assertEqual(forward, reverse)

        unsupported = replace(self.r3_profile, profile_version="1.0.1")
        changed = borrow_projection_hash_bundle(
            self.r2_state.hashes.fact_hash,
            self.r2_state.hashes.computation_hash,
            unsupported,
            "NATAL",
            self.r3_state.member_facts,
        )
        self.assertEqual(forward.fact_hash, changed.fact_hash)
        self.assertNotEqual(forward.computation_hash, changed.computation_hash)
        with self.assertRaises(ValueError):
            unsupported.validate()

    def test_tampered_source_projection_and_time_layer_fail_closed(self) -> None:
        borrowed_index = next(
            index
            for index, row in enumerate(self.r3_state.member_facts)
            if row.closure_status == "BORROWED_DIRECT"
        )
        original = self.r3_state.member_facts[borrowed_index]
        tampered_row = replace(original, projected_placements=original.projected_placements[1:])
        tampered_facts = list(self.r3_state.member_facts)
        tampered_facts[borrowed_index] = tampered_row
        tampered = replace(self.r3_state, member_facts=tuple(tampered_facts))
        report = validate_borrow_projection_state(
            self.candidate.chart,
            self.r1_state,
            self.r2_state,
            tampered,
        )
        self.assertEqual("FAIL", report.status)
        codes = {row.code for row in report.diagnostics}
        self.assertIn("BORROW_PROJECTED_PLACEMENTS_MISMATCH", codes)
        self.assertIn("BORROW_FACT_HASH_MISMATCH", codes)

        with self.assertRaises(BorrowProjectionGenerationError):
            self.r3_runtime.generate_from_candidate(
                self.candidate,
                self.r1_state,
                self.r2_state,
                self.r3_profile,
                time_layer="DAXIAN",
            )

    def test_cross_chart_composition_fails_closed(self) -> None:
        with self.assertRaises(BorrowProjectionGenerationError):
            self.r3_runtime.generate_from_candidate(
                self.other_candidate,
                self.r1_state,
                self.r2_state,
                self.r3_profile,
            )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import Sex, ZiweiChartFoundation, ZiweiChartRequest, ziwei_chart_engine_v1_profile
from fortune_training.ziwei_structural import ZiweiStructuralRuntime, ziwei_structural_v2_r1_profile
from fortune_training.ziwei_structural.r2 import ZiweiRelativePalaceFrameRuntime, ziwei_structural_v2_r2_profile
from fortune_training.ziwei_structural.r8 import (
    ADJACENT_PALACE_SEMANTIC_SCOPE,
    ADJACENT_PALACE_SOURCE_PARAGRAPH_ID,
    ADJACENT_PALACE_SOURCE_RELATION_ID,
    ADJACENT_PALACE_SOURCE_RUNTIME_BLOB_SHA,
    ADJACENT_PALACE_SOURCE_RUNTIME_PATH,
    ADJACENT_PALACE_SOURCE_SEGMENT_IDS,
    ADJACENT_PALACE_SOURCE_TERM_ID,
    AdjacentPalaceGenerationError,
    ZiweiAdjacentPalaceRuntime,
    adjacent_palace_hash_bundle,
    validate_adjacent_palace_state,
    ziwei_structural_v2_r8_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R8Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        natal_profile = ziwei_chart_engine_v1_profile(registry)
        natal_runtime = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        r1_profile = ziwei_structural_v2_r1_profile()
        r1_runtime = ZiweiStructuralRuntime()
        r2_profile = ziwei_structural_v2_r2_profile()
        r2_runtime = ZiweiRelativePalaceFrameRuntime()
        cls.r8_profile = ziwei_structural_v2_r8_profile()
        cls.r8_runtime = ZiweiAdjacentPalaceRuntime()
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
        cls.r1_state = r1_runtime.generate_from_candidate(cls.candidate, r1_profile)
        cls.r2_state = r2_runtime.generate_from_candidate(cls.candidate, cls.r1_state, r2_profile)
        cls.r8_state = cls.r8_runtime.generate_from_candidate(
            cls.candidate,
            cls.r1_state,
            cls.r2_state,
            cls.r8_profile,
        )

    def test_profile_freezes_bilateral_r2_geometry_and_no_flank_semantics(self) -> None:
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R8", self.r8_profile.profile_id)
        self.assertEqual(2, self.r8_profile.counterclockwise_relative_ordinal)
        self.assertEqual(11, self.r8_profile.counterclockwise_clockwise_offset)
        self.assertEqual(12, self.r8_profile.clockwise_relative_ordinal)
        self.assertEqual(1, self.r8_profile.clockwise_clockwise_offset)
        self.assertEqual(ADJACENT_PALACE_SEMANTIC_SCOPE, self.r8_profile.semantic_scope)
        self.assertFalse(self.r8_profile.flank_semantics_permission)
        self.assertFalse(self.r8_profile.direct_event_permission)
        self.assertFalse(self.r8_profile.direct_endpoint_permission)
        self.assertFalse(self.r8_profile.direct_score_permission)

    def test_all_12_origins_match_r2_adjacent_geometry_exactly(self) -> None:
        expected = (
            ("LIFE", "SIBLINGS", "PARENTS"),
            ("SIBLINGS", "SPOUSE", "LIFE"),
            ("SPOUSE", "CHILDREN", "SIBLINGS"),
            ("CHILDREN", "WEALTH", "SPOUSE"),
            ("WEALTH", "HEALTH", "CHILDREN"),
            ("HEALTH", "TRAVEL", "WEALTH"),
            ("TRAVEL", "SERVANTS_FRIENDS", "HEALTH"),
            ("SERVANTS_FRIENDS", "CAREER", "TRAVEL"),
            ("CAREER", "PROPERTY", "SERVANTS_FRIENDS"),
            ("PROPERTY", "FORTUNE", "CAREER"),
            ("FORTUNE", "PARENTS", "PROPERTY"),
            ("PARENTS", "LIFE", "FORTUNE"),
        )
        actual = tuple(
            (
                row.origin_designation_id,
                row.counterclockwise_designation_id,
                row.clockwise_designation_id,
            )
            for row in self.r8_state.adjacent_palace_pairs
        )
        self.assertEqual(expected, actual)
        r2_by_key = {
            (row.origin_designation_id, row.relative_ordinal): row
            for row in self.r2_state.frame_facts
        }
        for row in self.r8_state.adjacent_palace_pairs:
            ccw = r2_by_key[(row.origin_designation_id, 2)]
            cw = r2_by_key[(row.origin_designation_id, 12)]
            self.assertEqual(ccw.target_designation_id, row.counterclockwise_designation_id)
            self.assertEqual(ccw.target_address, row.counterclockwise_address)
            self.assertEqual(cw.target_designation_id, row.clockwise_designation_id)
            self.assertEqual(cw.target_address, row.clockwise_address)
            self.assertEqual(11, row.counterclockwise_clockwise_offset)
            self.assertEqual(1, row.clockwise_clockwise_offset)

    def test_source_example_child_palace_has_chou_and_hai_neighbors(self) -> None:
        origin = next(row for row in self.r8_state.adjacent_palace_pairs if row.origin_address.branch == "子")
        self.assertEqual({"丑", "亥"}, {origin.counterclockwise_address.branch, origin.clockwise_address.branch})

    def test_source_lineage_and_permissions_are_frozen(self) -> None:
        text = (ROOT / ADJACENT_PALACE_SOURCE_RUNTIME_PATH).read_text(encoding="utf-8")
        for source_id in (
            ADJACENT_PALACE_SOURCE_PARAGRAPH_ID,
            *ADJACENT_PALACE_SOURCE_SEGMENT_IDS,
            ADJACENT_PALACE_SOURCE_RELATION_ID,
            ADJACENT_PALACE_SOURCE_TERM_ID,
        ):
            self.assertIn(source_id, text)
        self.assertIn("本宫两侧相邻之两个宫垣。如子宫为本宫，则丑宫与亥宫即为其邻宫。", text)
        self.assertIn("本宫左右相邻的两个宫垣，是相夹结构的物理位置。", text)
        self.assertIn('"direct_event_permission":"NO","direct_endpoint_permission":"NO","direct_score_permission":"NO"', text)
        self.assertEqual("8401f1d190e3ee4b87aab86f82216972bea7dde8", ADJACENT_PALACE_SOURCE_RUNTIME_BLOB_SHA)

    def test_r8_state_is_deterministic_and_bound_to_r2_hashes(self) -> None:
        rerun = self.r8_runtime.generate_from_candidate(
            self.candidate,
            self.r1_state,
            self.r2_state,
            self.r8_profile,
        )
        self.assertEqual(self.r8_state, rerun)
        self.assertEqual(self.r2_state.hashes.fact_hash, self.r8_state.upstream_r2_fact_hash)
        self.assertEqual(self.r2_state.hashes.computation_hash, self.r8_state.upstream_r2_computation_hash)
        self.assertEqual("PASS", self.r8_state.integrity.status)
        self.assertEqual("PASS", validate_adjacent_palace_state(self.r2_state, self.r8_state).status)

    def test_tampered_neighbor_is_rejected_even_with_recomputed_hash(self) -> None:
        first = self.r8_state.adjacent_palace_pairs[0]
        tampered_first = replace(first, clockwise_designation_id="WEALTH")
        facts = (tampered_first,) + self.r8_state.adjacent_palace_pairs[1:]
        hashes = adjacent_palace_hash_bundle(
            self.r8_state.upstream_r2_fact_hash,
            self.r8_state.upstream_r2_computation_hash,
            self.r8_state.profile,
            self.r8_state.time_layer,
            facts,
        )
        report = validate_adjacent_palace_state(
            self.r2_state,
            replace(self.r8_state, adjacent_palace_pairs=facts, hashes=hashes),
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("ADJACENT_PALACE_FACT_PROJECTION_MISMATCH", {row.code for row in report.diagnostics})

    def test_flank_semantics_tamper_is_rejected(self) -> None:
        first = replace(self.r8_state.adjacent_palace_pairs[0], flank_semantics_permission=True)
        facts = (first,) + self.r8_state.adjacent_palace_pairs[1:]
        hashes = adjacent_palace_hash_bundle(
            self.r8_state.upstream_r2_fact_hash,
            self.r8_state.upstream_r2_computation_hash,
            self.r8_state.profile,
            self.r8_state.time_layer,
            facts,
        )
        report = validate_adjacent_palace_state(
            self.r2_state,
            replace(self.r8_state, adjacent_palace_pairs=facts, hashes=hashes),
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("ILLEGAL_ADJACENT_PALACE_RESULT_PERMISSION", {row.code for row in report.diagnostics})

    def test_non_natal_time_layer_is_rejected(self) -> None:
        with self.assertRaises(AdjacentPalaceGenerationError) as ctx:
            self.r8_runtime.generate_from_candidate(
                self.candidate,
                self.r1_state,
                self.r2_state,
                self.r8_profile,
                time_layer="ANNUAL",
            )
        self.assertEqual("UNSUPPORTED_ADJACENT_PALACE_TIME_LAYER", ctx.exception.diagnostic_code)


if __name__ == "__main__":
    unittest.main()

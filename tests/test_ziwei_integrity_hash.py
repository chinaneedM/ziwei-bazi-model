from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import ResolvedZiweiCalculationProfile, Sex, ZiweiChartFoundation, ZiweiChartRequest
from fortune_training.ziwei_chart.auxiliary import (
    AUXILIARY_ALGORITHM_ID,
    AUXILIARY_ALGORITHM_VERSION,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
)
from fortune_training.ziwei_chart.integrity import (
    natal_hash_bundle,
    temporal_hash_bundle,
    validate_natal_chart,
    validate_temporal_state,
)
from fortune_training.ziwei_chart.minor_stars import (
    MINOR_STAR_ALGORITHM_ID,
    MINOR_STAR_ALGORITHM_VERSION,
    WENMO_DEFAULT_MINOR_RULE_SET_ID,
    WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
)
from fortune_training.ziwei_chart.rings import (
    RING_ALGORITHM_ID,
    RING_ALGORITHM_VERSION,
    WENMO_DEFAULT_RING_RULE_SET_ID,
    WENMO_DEFAULT_RING_RULE_SET_VERSION,
)
from fortune_training.ziwei_chart.roles import (
    ROLE_ALGORITHM_ID,
    ROLE_ALGORITHM_VERSION,
    WENMO_DEFAULT_ROLE_RULE_SET_ID,
    WENMO_DEFAULT_ROLE_RULE_SET_VERSION,
)
from fortune_training.ziwei_chart.temporal import (
    S10_CURRENT_TEMPORAL_RULE_SET_ID,
    S10_CURRENT_TEMPORAL_RULE_SET_VERSION,
    TEMPORAL_ALGORITHM_ID,
    TEMPORAL_ALGORITHM_VERSION,
    TemporalNatalContext,
    ZiweiTemporalEngine,
)
from fortune_training.ziwei_chart.transformations import (
    S08_TRANSFORMATION_RULE_SET_ID,
    S08_TRANSFORMATION_RULE_SET_VERSION,
    TRANSFORMATION_ALGORITHM_ID,
    TRANSFORMATION_ALGORITHM_VERSION,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiIntegrityHashTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.time_calendar = TimeCalendarFoundation(cls.registry)
        cls.birth = BirthInput(
            reported_local_datetime=datetime(2001, 12, 15, 12, 0),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4,
            timezone_id="Asia/Shanghai",
        )
        cls.profile = ResolvedZiweiCalculationProfile(
            profile_id="WENMO-INTEGRITY-HASH-R1",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=cls.registry.version,
            time_calendar_policies=cls.registry.default_selection(),
            auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
            minor_rule_set_id=WENMO_DEFAULT_MINOR_RULE_SET_ID,
            minor_rule_set_version=WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
            minor_algorithm_id=MINOR_STAR_ALGORITHM_ID,
            minor_algorithm_version=MINOR_STAR_ALGORITHM_VERSION,
            transformation_rule_set_id=S08_TRANSFORMATION_RULE_SET_ID,
            transformation_rule_set_version=S08_TRANSFORMATION_RULE_SET_VERSION,
            transformation_algorithm_id=TRANSFORMATION_ALGORITHM_ID,
            transformation_algorithm_version=TRANSFORMATION_ALGORITHM_VERSION,
            ring_rule_set_id=WENMO_DEFAULT_RING_RULE_SET_ID,
            ring_rule_set_version=WENMO_DEFAULT_RING_RULE_SET_VERSION,
            ring_algorithm_id=RING_ALGORITHM_ID,
            ring_algorithm_version=RING_ALGORITHM_VERSION,
            role_rule_set_id=WENMO_DEFAULT_ROLE_RULE_SET_ID,
            role_rule_set_version=WENMO_DEFAULT_ROLE_RULE_SET_VERSION,
            role_algorithm_id=ROLE_ALGORITHM_ID,
            role_algorithm_version=ROLE_ALGORITHM_VERSION,
        ).validate(cls.registry)
        cls.engine = ZiweiChartFoundation(cls.time_calendar)
        cls.request = ZiweiChartRequest(birth=cls.birth, sex=Sex.MALE, profile=cls.profile)
        cls.time_result = cls.time_calendar.resolve(cls.birth, cls.profile.time_calendar_policies)
        cls.typed_chart = cls.engine._generate_chart(cls.time_result["branches"][0], cls.request)

    def test_full_operational_chart_integrity_passes(self):
        report = validate_natal_chart(self.typed_chart)
        self.assertEqual("PASS", report.status)
        self.assertEqual((), report.diagnostics)

    def test_public_engine_emits_integrity_and_stable_hashes(self):
        first = self.engine.resolve(self.request)
        second = self.engine.resolve(self.request)
        self.assertEqual("RESOLVED", first["status"])
        self.assertEqual("PASS", first["integrity_reports"][0]["status"])
        self.assertEqual(1, len(first["hashes"]))
        self.assertEqual(64, len(first["hashes"][0]["fact_hash"]))
        self.assertEqual(64, len(first["hashes"][0]["computation_hash"]))
        self.assertEqual(first["hashes"], second["hashes"])
        direct = natal_hash_bundle(self.typed_chart, self.profile)
        self.assertEqual(direct.fact_hash, first["hashes"][0]["fact_hash"])
        self.assertEqual(direct.computation_hash, first["hashes"][0]["computation_hash"])

    def test_fact_hash_ignores_profile_identity_but_computation_hash_does_not(self):
        other_profile = replace(self.profile, profile_id="SAME-FACTS-DIFFERENT-PROFILE", profile_version="9.9.9")
        first = natal_hash_bundle(self.typed_chart, self.profile)
        second = natal_hash_bundle(self.typed_chart, other_profile)
        self.assertEqual(first.fact_hash, second.fact_hash)
        self.assertNotEqual(first.computation_hash, second.computation_hash)

    def test_display_name_is_not_a_fact_or_computation_lineage_field(self):
        placement = self.typed_chart.placements[0]
        changed = replace(placement, display_name="DISPLAY-ONLY-ALIAS")
        chart = replace(self.typed_chart, placements=(changed,) + self.typed_chart.placements[1:])
        first = natal_hash_bundle(self.typed_chart, self.profile)
        second = natal_hash_bundle(chart, self.profile)
        self.assertEqual(first.fact_hash, second.fact_hash)
        self.assertEqual(first.computation_hash, second.computation_hash)

    def test_provenance_change_preserves_fact_hash_but_changes_computation_hash(self):
        placement = self.typed_chart.placements[0]
        changed = replace(placement, source_refs=placement.source_refs + ("TEST:ALTERNATE-WITNESS",))
        chart = replace(self.typed_chart, placements=(changed,) + self.typed_chart.placements[1:])
        first = natal_hash_bundle(self.typed_chart, self.profile)
        second = natal_hash_bundle(chart, self.profile)
        self.assertEqual(first.fact_hash, second.fact_hash)
        self.assertNotEqual(first.computation_hash, second.computation_hash)

    def test_physical_fact_change_changes_fact_and_computation_hashes(self):
        index = next(i for i, row in enumerate(self.typed_chart.placements) if row.entity_id == "STAR.TIANKONG")
        placement = self.typed_chart.placements[index]
        changed = replace(placement, address=replace(placement.address, index=(placement.address.index + 1) % 12, branch="未" if placement.address.branch != "未" else "申"))
        placements = list(self.typed_chart.placements)
        placements[index] = changed
        chart = replace(self.typed_chart, placements=tuple(placements))
        first = natal_hash_bundle(self.typed_chart, self.profile)
        second = natal_hash_bundle(chart, self.profile)
        self.assertNotEqual(first.fact_hash, second.fact_hash)
        self.assertNotEqual(first.computation_hash, second.computation_hash)

    def test_duplicate_entity_is_integrity_failure(self):
        duplicate = self.typed_chart.placements[0]
        chart = replace(self.typed_chart, placements=self.typed_chart.placements + (duplicate,))
        report = validate_natal_chart(chart)
        self.assertEqual("FAIL", report.status)
        self.assertIn("DUPLICATE_PLACEMENT_ENTITY", {row.code for row in report.diagnostics})

    def test_transformation_cannot_move_target_star(self):
        row = self.typed_chart.transformations[0]
        moved = replace(row, target_address=replace(row.target_address, index=(row.target_address.index + 1) % 12, branch="子" if row.target_address.branch != "子" else "丑"))
        chart = replace(self.typed_chart, transformations=(moved,) + self.typed_chart.transformations[1:])
        report = validate_natal_chart(chart)
        self.assertEqual("FAIL", report.status)
        self.assertIn("TRANSFORMATION_TARGET_ADDRESS_MISMATCH", {item.code for item in report.diagnostics})

    def test_temporal_integrity_and_hashes_are_deterministic(self):
        temporal_profile = replace(
            self.profile,
            temporal_rule_set_id=S10_CURRENT_TEMPORAL_RULE_SET_ID,
            temporal_rule_set_version=S10_CURRENT_TEMPORAL_RULE_SET_VERSION,
            temporal_algorithm_id=TEMPORAL_ALGORITHM_ID,
            temporal_algorithm_version=TEMPORAL_ALGORITHM_VERSION,
        ).validate(self.registry)
        context = TemporalNatalContext.from_natal_chart(2001, Sex.MALE, self.typed_chart)
        state = ZiweiTemporalEngine().generate(context, temporal_profile)
        report = validate_temporal_state(state, context)
        self.assertEqual("PASS", report.status)
        first = temporal_hash_bundle(state, temporal_profile)
        second = temporal_hash_bundle(state, temporal_profile)
        self.assertEqual(first, second)

        daxian0 = state.daxian_frames[0]
        changed_daxian = replace(daxian0, source_refs=daxian0.source_refs + ("TEST:SECOND-TEMPORAL-WITNESS",))
        changed_state = replace(state, daxian_frames=(changed_daxian,) + state.daxian_frames[1:])
        changed_hash = temporal_hash_bundle(changed_state, temporal_profile)
        self.assertEqual(first.fact_hash, changed_hash.fact_hash)
        self.assertNotEqual(first.computation_hash, changed_hash.computation_hash)

        annual0 = state.annual_frames[0]
        moved_doujun = replace(
            annual0,
            doujun_address=replace(
                annual0.doujun_address,
                index=(annual0.doujun_address.index + 1) % 12,
                branch="丑" if annual0.doujun_address.branch == "子" else "子",
            ),
        )
        tampered = replace(
            state,
            annual_frames=(moved_doujun,) + state.annual_frames[1:],
        )
        report = validate_temporal_state(tampered, context)
        self.assertIn(
            "ANNUAL_DOUJUN_ADDRESS_MISMATCH",
            {row.code for row in report.diagnostics},
        )
        self.assertNotEqual(
            first.fact_hash,
            temporal_hash_bundle(tampered, temporal_profile).fact_hash,
        )

    def test_engine_fails_closed_when_generated_chart_breaks_integrity(self):
        class DuplicateMainStarGenerator:
            def __init__(self, delegate):
                self.delegate = delegate

            def generate(self, lunar_day, bureau_number):
                rows = self.delegate.generate(lunar_day, bureau_number)
                return rows + (rows[0],)

        registry = self.registry
        profile = ResolvedZiweiCalculationProfile(
            profile_id="INTEGRITY-FAIL-CLOSED",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=registry.version,
            time_calendar_policies=registry.default_selection(),
        )
        engine = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        engine.main_stars = DuplicateMainStarGenerator(engine.main_stars)
        result = engine.resolve(ZiweiChartRequest(birth=self.birth, sex=Sex.MALE, profile=profile))
        self.assertEqual("FAILED", result["status"])
        self.assertTrue(any(code.startswith("INTEGRITY:DUPLICATE_PLACEMENT_ENTITY") for code in result["diagnostics"]))
        self.assertEqual("FAIL", result["integrity_reports"][0]["status"])
        self.assertEqual([], result["hashes"])


if __name__ == "__main__":
    unittest.main()

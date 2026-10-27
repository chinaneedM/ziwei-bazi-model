from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import PolicyRegistry
from fortune_training.ziwei_chart.auxiliary import (
    AUXILIARY_ALGORITHM_ID,
    AUXILIARY_ALGORITHM_VERSION,
    AuxiliaryContext,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
    WenmoDefaultCoreAuxiliaryGenerator,
)
from fortune_training.ziwei_chart.dignity import (
    CORE_AUX_DIGNITY_ENTITY_IDS,
    DIGNITY_ALGORITHM_ID,
    DIGNITY_ALGORITHM_VERSION,
    OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH,
    OPERATIONAL_DIGNITY_RULE_SET_ID,
    OPERATIONAL_DIGNITY_RULE_SET_VERSION,
    OperationalZiweiDignityGenerator,
)
from fortune_training.ziwei_chart.integrity import natal_hash_bundle, validate_natal_chart
from fortune_training.ziwei_chart.main_stars import MainStarGenerator
from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_chart.natal import NatalStructureGenerator, NatalStructureInput
from fortune_training.ziwei_chart.profile import ResolvedZiweiCalculationProfile
from fortune_training.ziwei_chart.registries import EARTHLY_BRANCHES, HEAVENLY_STEMS, address
from fortune_training.ziwei_chart.view import PlainTextZiweiRenderer, PresentationProfile, ZiweiViewProjectionCompiler


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "wenmo-core-aux-dignity-r2.json"


class ZiweiCoreAuxDignityR2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.policy_registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.aux = WenmoDefaultCoreAuxiliaryGenerator()
        cls.main = MainStarGenerator()
        cls.dignity = OperationalZiweiDignityGenerator()
        cls.profile = ResolvedZiweiCalculationProfile(
            profile_id="OPERATIONAL-ZIWEI-DIGNITY-R2-TEST",
            profile_version="2.0.0",
            time_calendar_policy_registry_version=cls.policy_registry.version,
            time_calendar_policies=cls.policy_registry.default_selection(),
            auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
            dignity_rule_set_id=OPERATIONAL_DIGNITY_RULE_SET_ID,
            dignity_rule_set_version=OPERATIONAL_DIGNITY_RULE_SET_VERSION,
            dignity_algorithm_id=DIGNITY_ALGORITHM_ID,
            dignity_algorithm_version=DIGNITY_ALGORITHM_VERSION,
        ).validate(cls.policy_registry)

    @staticmethod
    def _context(*, stem="甲", branch="子", month=1, hour=0) -> AuxiliaryContext:
        return AuxiliaryContext(
            ziwei_birth_year_stem=stem,
            ziwei_birth_year_branch=branch,
            raw_lunar_month=month,
            is_leap_month=False,
            birth_hour_branch=address(hour),
            lunar_day=10,
            lunar_month_length_days=30,
        )

    def _r2_chart_with_all_unrated_examples(self) -> NatalChartState:
        # 辛 selects the operational 寅/午 Kui-Yue pair; 子时 places 地劫 in 亥.
        aux = self.aux.generate(self._context(stem="辛", branch="巳", month=11, hour=0))
        main = self.main.generate_from_ziwei_anchor(11)
        placements = main + aux
        annotations = self.dignity.generate(placements)
        structure = NatalStructureGenerator().generate(
            NatalStructureInput(
                lunar_year=2001,
                lunar_month=11,
                lunar_day=1,
                is_leap_month=False,
                lunar_month_length_days=30,
                local_apparent_solar_datetime=datetime(2001, 12, 15, 0, 0),
                life_body_leap_month_policy="CURRENT_MONTH",
            )
        )
        return NatalChartState(
            structure=structure,
            placements=placements,
            profile_id=self.profile.profile_id,
            profile_version=self.profile.profile_version,
            annotations=annotations,
            algorithm_versions={
                "natal_structure": "1.0.0",
                "main_stars": "1.0.1",
                "core_auxiliary": AUXILIARY_ALGORITHM_VERSION,
                "dignity": DIGNITY_ALGORITHM_VERSION,
            },
        )

    def test_fixture_and_runtime_registry_match_exactly(self) -> None:
        runtime = {
            entity_id: {
                branch: [state.status, state.grade]
                for branch, state in cells.items()
            }
            for entity_id, cells in OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH.items()
        }
        self.assertEqual(self.fixture["cells"], runtime)
        self.assertEqual(134, self.fixture["reachable_cell_count"])
        self.assertEqual(131, self.fixture["graded_cell_count"])
        self.assertEqual(3, self.fixture["unrated_cell_count"])
        self.assertEqual(0, self.fixture["conflict_count"])

    def test_registry_summary_is_168_main_plus_134_reachable_aux(self) -> None:
        summary = self.dignity.registry_summary()
        self.assertEqual(28, summary.entity_count)
        self.assertEqual(302, summary.cell_count)
        self.assertEqual(299, summary.graded_cell_count)
        self.assertEqual(3, summary.unrated_cell_count)

    def test_exact_unrated_cells_are_typed_not_coerced_to_ping(self) -> None:
        unrated = {
            f"{entity_id}@{branch}"
            for entity_id, cells in OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH.items()
            for branch, state in cells.items()
            if state.status == "UNRATED"
        }
        self.assertEqual({"STAR.TIANKUI@寅", "STAR.TIANYUE@午", "STAR.DIJIE@亥"}, unrated)
        self.assertEqual(set(self.fixture["unrated_cells"]), unrated)
        for entity_id, branch in (item.split("@") for item in unrated):
            self.assertIsNone(OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH[entity_id][branch].grade)

    def test_generator_reachable_domain_equals_registry_domain(self) -> None:
        observed: set[tuple[str, str]] = set()

        def collect(context: AuxiliaryContext) -> None:
            for row in self.aux.generate(context):
                if row.entity_id in CORE_AUX_DIGNITY_ENTITY_IDS:
                    observed.add((row.entity_id, row.address.branch))
                    self.assertIn(row.address.branch, OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH[row.entity_id])

        # Vary every primitive input dimension independently; Fire/Bell use year-branch + hour.
        for hour in range(12):
            collect(self._context(hour=hour))
        for month in range(1, 13):
            collect(self._context(month=month))
        for stem in HEAVENLY_STEMS:
            collect(self._context(stem=stem))
        for branch in EARTHLY_BRANCHES:
            collect(self._context(branch=branch))
        for branch in EARTHLY_BRANCHES:
            for hour in range(12):
                collect(self._context(branch=branch, hour=hour))

        registry = {
            (entity_id, branch)
            for entity_id, cells in OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH.items()
            for branch in cells
        }
        self.assertEqual(registry, observed)
        self.assertEqual(134, len(observed))

    def test_r2_materializes_all_28_targets_and_three_unrated_states(self) -> None:
        chart = self._r2_chart_with_all_unrated_examples()
        self.assertEqual("PASS", validate_natal_chart(chart).status)
        self.assertEqual(28, len(chart.annotations))
        unrated = {(row.target_entity_id, row.target_address.branch) for row in chart.annotations if row.status == "UNRATED"}
        self.assertEqual({("STAR.TIANKUI", "寅"), ("STAR.TIANYUE", "午"), ("STAR.DIJIE", "亥")}, unrated)
        self.assertTrue(all(row.grade is None for row in chart.annotations if row.status == "UNRATED"))

    def test_profile_r2_fails_closed_without_compatible_core_auxiliary(self) -> None:
        base = ResolvedZiweiCalculationProfile(
            profile_id="BAD-R2",
            profile_version="1",
            time_calendar_policy_registry_version=self.policy_registry.version,
            time_calendar_policies=self.policy_registry.default_selection(),
            dignity_rule_set_id=OPERATIONAL_DIGNITY_RULE_SET_ID,
            dignity_rule_set_version=OPERATIONAL_DIGNITY_RULE_SET_VERSION,
            dignity_algorithm_id=DIGNITY_ALGORITHM_ID,
            dignity_algorithm_version=DIGNITY_ALGORITHM_VERSION,
        )
        with self.assertRaisesRegex(ValueError, "REQUIRES_COMPATIBLE_CORE_AUXILIARY_PROFILE"):
            base.validate(self.policy_registry)

    def test_unrated_status_is_canonical_fact_and_view_visible_state(self) -> None:
        chart = self._r2_chart_with_all_unrated_examples()
        hashes = natal_hash_bundle(chart, self.profile)
        first = next(row for row in chart.annotations if row.status == "UNRATED")
        changed = replace(first, status="GRADED", grade="平")
        rows = tuple(changed if row.annotation_id == first.annotation_id else row for row in chart.annotations)
        changed_chart = replace(chart, annotations=rows)
        self.assertEqual("PASS", validate_natal_chart(changed_chart).status)
        changed_hashes = natal_hash_bundle(changed_chart, self.profile)
        self.assertNotEqual(hashes.fact_hash, changed_hashes.fact_hash)

        compiler = ZiweiViewProjectionCompiler()
        shown = compiler.compile(chart, hashes, PresentationProfile("R2.SHOWN", "1", show_dignity=True))
        hidden = compiler.compile(chart, hashes, PresentationProfile("R2.HIDDEN", "1", show_dignity=False))
        shown_unrated = [row for cell in shown.cells for row in cell.placements if row.dignity_status == "UNRATED"]
        self.assertEqual(3, len(shown_unrated))
        self.assertTrue(all(row.dignity_grade is None for row in shown_unrated))
        self.assertFalse(any(row.dignity_status for cell in hidden.cells for row in cell.placements))
        rendered = PlainTextZiweiRenderer().render(shown)
        self.assertGreaterEqual(rendered.count("[未评级]"), 3)

    def test_integrity_rejects_incoherent_status_grade_pairs(self) -> None:
        chart = self._r2_chart_with_all_unrated_examples()
        unrated = next(row for row in chart.annotations if row.status == "UNRATED")
        broken = replace(unrated, grade="平")
        rows = tuple(broken if row.annotation_id == unrated.annotation_id else row for row in chart.annotations)
        report = validate_natal_chart(replace(chart, annotations=rows))
        self.assertEqual("FAIL", report.status)
        self.assertIn("UNRATED_DIGNITY_MUST_NOT_HAVE_GRADE", {row.code for row in report.diagnostics})


if __name__ == "__main__":
    unittest.main()

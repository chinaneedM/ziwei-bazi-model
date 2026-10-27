from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import PolicyRegistry
from fortune_training.ziwei_chart.dignity import (
    DIGNITY_ALGORITHM_ID,
    DIGNITY_ALGORITHM_VERSION,
    OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS,
    OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID,
    OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_VERSION,
    OperationalMainStarDignityGenerator,
)
from fortune_training.ziwei_chart.integrity import natal_hash_bundle, validate_natal_chart
from fortune_training.ziwei_chart.main_stars import MainStarGenerator
from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_chart.natal import NatalStructureGenerator, NatalStructureInput
from fortune_training.ziwei_chart.profile import ResolvedZiweiCalculationProfile
from fortune_training.ziwei_chart.registries import branch_index
from fortune_training.ziwei_chart.view import PresentationProfile, ZiweiViewProjectionCompiler


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "wenmo-main-star-dignity-r1.json"


class ZiweiOperationalDignityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.main = MainStarGenerator()
        cls.dignity = OperationalMainStarDignityGenerator()
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.profile = ResolvedZiweiCalculationProfile(
            profile_id="OPERATIONAL-ZIWEI-DIGNITY-TEST",
            profile_version="1.0.0",
            time_calendar_policy_registry_version=cls.registry.version,
            time_calendar_policies=cls.registry.default_selection(),
            dignity_rule_set_id=OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID,
            dignity_rule_set_version=OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_VERSION,
            dignity_algorithm_id=DIGNITY_ALGORITHM_ID,
            dignity_algorithm_version=DIGNITY_ALGORITHM_VERSION,
        ).validate(cls.registry)

    def _chart_for_anchor(self, anchor_branch: str) -> NatalChartState:
        structure = NatalStructureGenerator().generate(
            NatalStructureInput(
                lunar_year=2001,
                lunar_month=11,
                lunar_day=1,
                is_leap_month=False,
                lunar_month_length_days=30,
                local_apparent_solar_datetime=datetime(2001, 12, 15, 11, 50),
                life_body_leap_month_policy="CURRENT_MONTH",
            )
        )
        placements = self.main.generate_from_ziwei_anchor(branch_index(anchor_branch))
        annotations = self.dignity.generate(placements)
        return NatalChartState(
            structure=structure,
            placements=placements,
            profile_id=self.profile.profile_id,
            profile_version=self.profile.profile_version,
            annotations=annotations,
            algorithm_versions={
                "natal_structure": "1.0.0",
                "main_stars": "1.0.1",
                "dignity": DIGNITY_ALGORITHM_VERSION,
            },
        )

    def test_registry_is_complete_14_by_12(self) -> None:
        summary = self.dignity.registry_summary()
        self.assertEqual(14, summary.entity_count)
        self.assertEqual(12, summary.address_count)
        self.assertEqual(168, summary.cell_count)
        self.assertEqual(14, len(OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS))
        self.assertTrue(all(len(row) == 12 for row in OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS.values()))
        self.dignity.validate_registry()

    def test_all_12_anchor_fixtures_close_all_168_main_star_cells(self) -> None:
        observed_cells: set[tuple[str, str]] = set()
        self.assertEqual(12, len(self.fixture["anchors"]))
        for anchor_branch, case in self.fixture["anchors"].items():
            placements = self.main.generate_from_ziwei_anchor(branch_index(anchor_branch))
            annotations = self.dignity.generate(placements)
            placement_by_entity = {row.entity_id: row for row in placements}
            annotation_by_entity = {row.target_entity_id: row for row in annotations}
            self.assertEqual(14, len(annotation_by_entity), anchor_branch)
            for entity_id, (expected_branch, expected_grade) in case["observations"].items():
                self.assertEqual(expected_branch, placement_by_entity[entity_id].address.branch, (anchor_branch, entity_id))
                self.assertEqual(expected_grade, annotation_by_entity[entity_id].grade, (anchor_branch, entity_id))
                self.assertEqual(expected_branch, annotation_by_entity[entity_id].target_address.branch)
                observed_cells.add((entity_id, expected_branch))
        self.assertEqual(168, len(observed_cells))
        self.assertEqual(0, self.fixture["conflict_count"])

    def test_dignity_is_annotation_not_placement_mutation(self) -> None:
        placements = self.main.generate_from_ziwei_anchor(branch_index("亥"))
        before = tuple((row.entity_id, row.address.index, row.display_name) for row in placements)
        annotations = self.dignity.generate(placements)
        after = tuple((row.entity_id, row.address.index, row.display_name) for row in placements)
        self.assertEqual(before, after)
        self.assertEqual(14, len(annotations))
        self.assertTrue(all(row.annotation_type == "DIGNITY" for row in annotations))

    def test_dignity_grade_is_canonical_fact_but_provenance_is_lineage(self) -> None:
        chart = self._chart_for_anchor("亥")
        base = natal_hash_bundle(chart, self.profile)
        first = chart.annotations[0]

        alternate_grade = "旺" if first.grade != "旺" else "庙"
        grade_changed = replace(chart, annotations=(replace(first, grade=alternate_grade),) + chart.annotations[1:])
        grade_hash = natal_hash_bundle(grade_changed, self.profile)
        self.assertNotEqual(base.fact_hash, grade_hash.fact_hash)
        self.assertNotEqual(base.computation_hash, grade_hash.computation_hash)

        provenance_changed = replace(
            chart,
            annotations=(replace(first, source_refs=first.source_refs + ("TEST:SECONDARY-WITNESS",)),) + chart.annotations[1:],
        )
        provenance_hash = natal_hash_bundle(provenance_changed, self.profile)
        self.assertEqual(base.fact_hash, provenance_hash.fact_hash)
        self.assertNotEqual(base.computation_hash, provenance_hash.computation_hash)

    def test_integrity_rejects_dignity_detached_from_target_placement(self) -> None:
        chart = self._chart_for_anchor("亥")
        first = chart.annotations[0]
        moved_address = replace(first.target_address, index=(first.target_address.index + 1) % 12)
        broken = replace(chart, annotations=(replace(first, target_address=moved_address),) + chart.annotations[1:])
        report = validate_natal_chart(broken)
        self.assertEqual("FAIL", report.status)
        self.assertIn("ANNOTATION_TARGET_ADDRESS_MISMATCH", {row.code for row in report.diagnostics})

    def test_view_can_hide_dignity_without_mutating_fact_hash(self) -> None:
        chart = self._chart_for_anchor("亥")
        hashes = natal_hash_bundle(chart, self.profile)
        compiler = ZiweiViewProjectionCompiler()
        shown = compiler.compile(chart, hashes, PresentationProfile("VIEW.DIGNITY", "1.0.0", show_dignity=True))
        hidden = compiler.compile(chart, hashes, PresentationProfile("VIEW.NO_DIGNITY", "1.0.0", show_dignity=False))

        shown_grades = [row.dignity_grade for cell in shown.cells for row in cell.placements if row.dignity_grade]
        hidden_grades = [row.dignity_grade for cell in hidden.cells for row in cell.placements if row.dignity_grade]
        self.assertEqual(14, len(shown_grades))
        self.assertEqual([], hidden_grades)
        self.assertEqual(hashes.fact_hash, shown.source_fact_hash)
        self.assertEqual(hashes.fact_hash, hidden.source_fact_hash)
        self.assertNotEqual(shown.view_hash, hidden.view_hash)


if __name__ == "__main__":
    unittest.main()

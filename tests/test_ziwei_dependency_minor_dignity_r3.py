from __future__ import annotations

import hashlib
import json
import unittest
from dataclasses import replace
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
from fortune_training.ziwei_chart.derived_auxiliary import DerivedAuxiliaryGenerator
from fortune_training.ziwei_chart.dignity import (
    DIGNITY_ALGORITHM_ID,
    DIGNITY_ALGORITHM_VERSION,
)
from fortune_training.ziwei_chart.dignity_r3 import (
    DEPENDENCY_MINOR_DIGNITY_ENTITY_IDS,
    OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH,
    OPERATIONAL_FULL_DIGNITY_RULE_SET_ID,
    OPERATIONAL_FULL_DIGNITY_RULE_SET_VERSION,
    OperationalFullZiweiDignityGenerator,
)
from fortune_training.ziwei_chart.main_stars import MainStarGenerator
from fortune_training.ziwei_chart.minor_stars import (
    MINOR_STAR_ALGORITHM_ID,
    MINOR_STAR_ALGORITHM_VERSION,
    WENMO_DEFAULT_MINOR_RULE_SET_ID,
    WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
    MinorStarContext,
    WenmoDefaultMinorStarGenerator,
)
from fortune_training.ziwei_chart.profile import ResolvedZiweiCalculationProfile
from fortune_training.ziwei_chart.registries import EARTHLY_BRANCHES, HEAVENLY_STEMS, address


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "wenmo-dependency-minor-dignity-r3.json"


class ZiweiDependencyMinorDignityR3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.policy_registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.aux = WenmoDefaultCoreAuxiliaryGenerator()
        cls.derived = DerivedAuxiliaryGenerator()
        cls.minor = WenmoDefaultMinorStarGenerator()
        cls.main = MainStarGenerator()
        cls.dignity = OperationalFullZiweiDignityGenerator()

    @staticmethod
    def _fixture_cells(fixture: dict) -> dict[str, dict[str, tuple[str, str | None]]]:
        cells: dict[str, dict[str, tuple[str, str | None]]] = {}
        for entity_id, (branches, grades) in fixture["graded_rows"].items():
            cells[entity_id] = {
                branch: ("GRADED", grade)
                for branch, grade in zip(branches, grades)
            }
        for entity_id, branches in fixture["unrated_rows"].items():
            cells[entity_id] = {branch: ("UNRATED", None) for branch in branches}
        return cells

    @staticmethod
    def _matrix_sha(cells: dict[str, dict[str, tuple[str, str | None]]]) -> str:
        rows: list[str] = []
        for entity_id in sorted(cells):
            for branch in EARTHLY_BRANCHES:
                if branch not in cells[entity_id]:
                    continue
                status, grade = cells[entity_id][branch]
                rows.append(f"{entity_id}|{branch}|{status}|{grade or ''}")
        return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()

    def test_fixture_and_runtime_registry_match_exactly(self) -> None:
        fixture_cells = self._fixture_cells(self.fixture)
        runtime_cells = {
            entity_id: {
                branch: (state.status, state.grade)
                for branch, state in cells.items()
            }
            for entity_id, cells in OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH.items()
        }
        self.assertEqual(fixture_cells, runtime_cells)
        self.assertEqual(39, self.fixture["entity_count"])
        self.assertEqual(379, self.fixture["reachable_cell_count"])
        self.assertEqual(290, self.fixture["graded_cell_count"])
        self.assertEqual(89, self.fixture["unrated_cell_count"])
        self.assertEqual(0, self.fixture["conflict_count"])
        self.assertEqual(
            "3eb9f9c5d7d359707293d566cfe69035fa84d0d3d0a55b18e35eb654ea321ab5",
            self.fixture["matrix_sha256"],
        )
        self.assertEqual(self.fixture["matrix_sha256"], self._matrix_sha(fixture_cells))

    def test_registry_summary_is_full_67_entity_v1_scope(self) -> None:
        summary = self.dignity.registry_summary()
        self.assertEqual(67, summary.entity_count)
        self.assertEqual(681, summary.cell_count)
        self.assertEqual(589, summary.graded_cell_count)
        self.assertEqual(92, summary.unrated_cell_count)

    def test_exact_ten_unrated_dependency_minor_domains(self) -> None:
        actual = {
            entity_id: "".join(
                branch
                for branch in EARTHLY_BRANCHES
                if branch in cells and cells[branch].status == "UNRATED"
            )
            for entity_id, cells in OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH.items()
            if any(state.status == "UNRATED" for state in cells.values())
        }
        self.assertEqual(self.fixture["unrated_rows"], actual)
        self.assertEqual(
            {
                "STAR.TIANCHU": 7,
                "STAR.JIESHA": 4,
                "STAR.FEILIAN": 12,
                "STAR.LONGDE": 12,
                "STAR.YUEDE": 12,
                "STAR.TAIFU": 12,
                "STAR.FENGGAO": 12,
                "STAR.TIANWU": 4,
                "STAR.TIANYUE_MOON": 8,
                "STAR.YINSHA": 6,
            },
            {entity_id: len(branches) for entity_id, branches in actual.items()},
        )

    def test_generator_reachable_domain_equals_dependency_minor_registry_exactly(self) -> None:
        observed: set[tuple[str, str]] = set()

        def collect(rows) -> None:
            for row in rows:
                if row.entity_id in DEPENDENCY_MINOR_DIGNITY_ENTITY_IDS:
                    observed.add((row.entity_id, row.address.branch))

        for stem in HEAVENLY_STEMS:
            collect(self.minor.stem_stars(stem))
        for index in range(60):
            stem = HEAVENLY_STEMS[index % 10]
            branch = EARTHLY_BRANCHES[index % 12]
            collect(self.minor.xunkong(stem, branch))

        for branch_index, branch in enumerate(EARTHLY_BRANCHES):
            stem = HEAVENLY_STEMS[branch_index % 10]
            for life_index in range(12):
                collect(self.minor.year_branch_stars(branch, stem, life_index))

        for hour in range(12):
            collect(self.minor.hour_stars(hour))
        for month in range(1, 13):
            collect(self.minor.month_stars(month))

        for anchor in range(12):
            for lunar_day in range(1, 31):
                collect(
                    self.derived.san_tai_ba_zuo(
                        {"STAR.ZUOFU": anchor, "STAR.YOUBI": anchor},
                        lunar_day,
                    )
                )
                collect(
                    self.derived.en_guang_tian_gui(
                        {"STAR.WENCHANG": anchor, "STAR.WENQU": anchor},
                        lunar_day,
                    )
                )

        registry = {
            (entity_id, branch)
            for entity_id, cells in OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH.items()
            for branch in cells
        }
        self.assertEqual(registry, observed)
        self.assertEqual(379, len(observed))

    def test_r3_materializes_all_67_current_physical_entities(self) -> None:
        aux_context = AuxiliaryContext(
            ziwei_birth_year_stem="壬",
            ziwei_birth_year_branch="申",
            raw_lunar_month=5,
            is_leap_month=False,
            birth_hour_branch=address(7),
            lunar_day=10,
            lunar_month_length_days=30,
        )
        placements = list(self.main.generate_from_ziwei_anchor(0))
        placements.extend(self.aux.generate(aux_context))
        placements.extend(self.derived.generate(placements, 10))
        placements.extend(
            self.minor.generate(
                MinorStarContext(
                    ziwei_birth_year_stem="壬",
                    ziwei_birth_year_branch="申",
                    raw_lunar_month=5,
                    is_leap_month=False,
                    lunar_day=10,
                    birth_hour_branch=address(7),
                    life_address=address(0),
                    body_address=address(6),
                )
            )
        )
        annotations = self.dignity.generate(placements)
        self.assertEqual(67, len(annotations))
        unrated_ids = {
            row.target_entity_id
            for row in annotations
            if row.status == "UNRATED"
        }
        self.assertEqual(set(self.fixture["unrated_rows"]), unrated_ids)
        self.assertEqual(10, len(unrated_ids))
        self.assertTrue(all(row.grade is None for row in annotations if row.status == "UNRATED"))

    def test_r3_profile_requires_both_compatible_placement_families(self) -> None:
        good = ResolvedZiweiCalculationProfile(
            profile_id="OPERATIONAL-ZIWEI-DIGNITY-R3-TEST",
            profile_version="3.0.0",
            time_calendar_policy_registry_version=self.policy_registry.version,
            time_calendar_policies=self.policy_registry.default_selection(),
            auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
            minor_rule_set_id=WENMO_DEFAULT_MINOR_RULE_SET_ID,
            minor_rule_set_version=WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
            minor_algorithm_id=MINOR_STAR_ALGORITHM_ID,
            minor_algorithm_version=MINOR_STAR_ALGORITHM_VERSION,
            dignity_rule_set_id=OPERATIONAL_FULL_DIGNITY_RULE_SET_ID,
            dignity_rule_set_version=OPERATIONAL_FULL_DIGNITY_RULE_SET_VERSION,
            dignity_algorithm_id=DIGNITY_ALGORITHM_ID,
            dignity_algorithm_version=DIGNITY_ALGORITHM_VERSION,
        )
        good.validate(self.policy_registry)

        without_minor = replace(
            good,
            minor_rule_set_id=None,
            minor_rule_set_version=None,
            minor_algorithm_id=None,
            minor_algorithm_version=None,
        )
        with self.assertRaisesRegex(ValueError, "R3_REQUIRES_COMPATIBLE_MINOR_STAR_PROFILE"):
            without_minor.validate(self.policy_registry)

        without_aux = replace(
            good,
            auxiliary_rule_set_id=None,
            auxiliary_rule_set_version=None,
            auxiliary_algorithm_id=None,
            auxiliary_algorithm_version=None,
        )
        with self.assertRaisesRegex(ValueError, "REQUIRES_COMPATIBLE_CORE_AUXILIARY_PROFILE"):
            without_aux.validate(self.policy_registry)


if __name__ == "__main__":
    unittest.main()

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
from fortune_training.ziwei_chart.dignity import DIGNITY_ALGORITHM_ID, DIGNITY_ALGORITHM_VERSION
from fortune_training.ziwei_chart.dignity_r3 import (
    OPERATIONAL_FULL_DIGNITY_RULE_SET_ID,
    OPERATIONAL_FULL_DIGNITY_RULE_SET_VERSION,
)
from fortune_training.ziwei_chart.dignity_r4 import (
    OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH,
    OPERATIONAL_R4_DIGNITY_RULE_SET_ID,
    OPERATIONAL_R4_DIGNITY_RULE_SET_VERSION,
    OperationalZiweiDignityR4Generator,
)
from fortune_training.ziwei_chart.main_stars import MainStarGenerator
from fortune_training.ziwei_chart.minor_stars import (
    MINOR_STAR_ALGORITHM_ID,
    MINOR_STAR_ALGORITHM_VERSION,
    WENMO_DEFAULT_MINOR_RULE_SET_ID,
    WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
    MinorStarContext,
)
from fortune_training.ziwei_chart.minor_stars_r4 import (
    R4_ADDED_MINOR_ENTITY_IDS,
    WENMO_DEFAULT_MINOR_R4_RULE_SET_VERSION,
    WenmoDefaultMinorStarR4Generator,
)
from fortune_training.ziwei_chart.profile import ResolvedZiweiCalculationProfile
from fortune_training.ziwei_chart.registries import EARTHLY_BRANCHES, address


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "wenmo-tianshou-tianshang-tianshi-dignity-r4.json"


class ZiweiTianShouTianShangTianShiDignityR4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.policy_registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.main = MainStarGenerator()
        cls.aux = WenmoDefaultCoreAuxiliaryGenerator()
        cls.derived = DerivedAuxiliaryGenerator()
        cls.minor = WenmoDefaultMinorStarR4Generator()
        cls.dignity = OperationalZiweiDignityR4Generator()

    @staticmethod
    def _fixture_cells(fixture: dict) -> dict[str, dict[str, tuple[str, str | None]]]:
        return {
            entity_id: {
                branch: ("GRADED", grade)
                for branch, grade in zip(branches, grades)
            }
            for entity_id, (branches, grades) in fixture["graded_rows"].items()
        }

    @staticmethod
    def _matrix_sha(cells: dict[str, dict[str, tuple[str, str | None]]]) -> str:
        rows: list[str] = []
        for entity_id in sorted(cells):
            for branch in EARTHLY_BRANCHES:
                status, grade = cells[entity_id][branch]
                rows.append(f"{entity_id}|{branch}|{status}|{grade or ''}")
        return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()

    def test_fixture_and_runtime_added_registry_match_exactly(self) -> None:
        fixture_cells = self._fixture_cells(self.fixture)
        runtime_cells = {
            entity_id: {
                branch: (state.status, state.grade)
                for branch, state in cells.items()
            }
            for entity_id, cells in OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH.items()
        }
        self.assertEqual(fixture_cells, runtime_cells)
        self.assertEqual(3, self.fixture["entity_count"])
        self.assertEqual(36, self.fixture["reachable_cell_count"])
        self.assertEqual(36, self.fixture["graded_cell_count"])
        self.assertEqual(0, self.fixture["unrated_cell_count"])
        self.assertEqual(0, self.fixture["conflict_count"])
        self.assertEqual(
            "5bac16b2f13d240f3adc7846a8aa45ce58f1c9bb2b89c6f7a450aef606b40e23",
            self.fixture["matrix_sha256"],
        )
        self.assertEqual(self.fixture["matrix_sha256"], self._matrix_sha(fixture_cells))

    def test_r4_registry_summary_is_full_70_entity_scope(self) -> None:
        summary = self.dignity.registry_summary()
        self.assertEqual(70, summary.entity_count)
        self.assertEqual(717, summary.cell_count)
        self.assertEqual(625, summary.graded_cell_count)
        self.assertEqual(92, summary.unrated_cell_count)

    def test_new_generator_domain_equals_three_full_rows_exactly(self) -> None:
        observed: set[tuple[str, str]] = set()
        for year_branch in EARTHLY_BRANCHES:
            for life_index in range(12):
                for body_index in range(12):
                    context = MinorStarContext(
                        ziwei_birth_year_stem="甲",
                        ziwei_birth_year_branch=year_branch,
                        raw_lunar_month=1,
                        is_leap_month=False,
                        lunar_day=1,
                        birth_hour_branch=address(0),
                        life_address=address(life_index),
                        body_address=address(body_index),
                    )
                    for row in self.minor.r4_stars(context):
                        observed.add((row.entity_id, row.address.branch))

        registry = {
            (entity_id, branch)
            for entity_id, cells in OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH.items()
            for branch in cells
        }
        self.assertEqual(R4_ADDED_MINOR_ENTITY_IDS, {entity_id for entity_id, _ in observed})
        self.assertEqual(registry, observed)
        self.assertEqual(36, len(observed))

    def test_two_minimal_closure_geometries(self) -> None:
        cases = (
            ("辰", "酉", "酉", {"STAR.TIANSHOU": "丑", "STAR.TIANSHANG": "寅", "STAR.TIANSHI": "辰"}),
            ("戌", "辰", "辰", {"STAR.TIANSHOU": "寅", "STAR.TIANSHANG": "酉", "STAR.TIANSHI": "亥"}),
        )
        for year_branch, life_branch, body_branch, expected in cases:
            context = MinorStarContext(
                ziwei_birth_year_stem="甲",
                ziwei_birth_year_branch=year_branch,
                raw_lunar_month=1,
                is_leap_month=False,
                lunar_day=1,
                birth_hour_branch=address(0),
                life_address=address(EARTHLY_BRANCHES.index(life_branch)),
                body_address=address(EARTHLY_BRANCHES.index(body_branch)),
            )
            actual = {row.entity_id: row.address.branch for row in self.minor.r4_stars(context)}
            self.assertEqual(expected, actual)

    def test_r4_materializes_all_70_physical_entities(self) -> None:
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
        self.assertEqual(70, len({row.entity_id for row in placements}))
        self.assertEqual(70, len(annotations))
        self.assertEqual(
            {"STAR.TIANSHOU", "STAR.TIANSHANG", "STAR.TIANSHI"},
            {
                row.target_entity_id
                for row in annotations
                if row.target_entity_id in R4_ADDED_MINOR_ENTITY_IDS
            },
        )

    def test_profile_keeps_r3_legacy_and_requires_r4_minor_v2(self) -> None:
        base_kwargs = dict(
            profile_id="OPERATIONAL-ZIWEI-DIGNITY-R4-TEST",
            profile_version="4.0.0",
            time_calendar_policy_registry_version=self.policy_registry.version,
            time_calendar_policies=self.policy_registry.default_selection(),
            auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
            auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
            auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
            minor_rule_set_id=WENMO_DEFAULT_MINOR_RULE_SET_ID,
            minor_algorithm_id=MINOR_STAR_ALGORITHM_ID,
            minor_algorithm_version=MINOR_STAR_ALGORITHM_VERSION,
            dignity_algorithm_id=DIGNITY_ALGORITHM_ID,
            dignity_algorithm_version=DIGNITY_ALGORITHM_VERSION,
        )
        r4 = ResolvedZiweiCalculationProfile(
            **base_kwargs,
            minor_rule_set_version=WENMO_DEFAULT_MINOR_R4_RULE_SET_VERSION,
            dignity_rule_set_id=OPERATIONAL_R4_DIGNITY_RULE_SET_ID,
            dignity_rule_set_version=OPERATIONAL_R4_DIGNITY_RULE_SET_VERSION,
        )
        r4.validate(self.policy_registry)

        wrong_r4_minor = replace(r4, minor_rule_set_version=WENMO_DEFAULT_MINOR_RULE_SET_VERSION)
        with self.assertRaisesRegex(ValueError, "R4_MINOR_STAR_VERSION_MISMATCH"):
            wrong_r4_minor.validate(self.policy_registry)

        r3 = replace(
            r4,
            profile_id="OPERATIONAL-ZIWEI-DIGNITY-R3-REPLAY",
            profile_version="3.0.0",
            minor_rule_set_version=WENMO_DEFAULT_MINOR_RULE_SET_VERSION,
            dignity_rule_set_id=OPERATIONAL_FULL_DIGNITY_RULE_SET_ID,
            dignity_rule_set_version=OPERATIONAL_FULL_DIGNITY_RULE_SET_VERSION,
        )
        r3.validate(self.policy_registry)


if __name__ == "__main__":
    unittest.main()

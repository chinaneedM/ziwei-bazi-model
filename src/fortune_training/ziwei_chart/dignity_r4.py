from __future__ import annotations

from .dignity import (
    CORE_AUX_DIGNITY_ENTITY_IDS,
    DIGNITY_GRADES,
    DIGNITY_STATUSES,
    DignityGenerationError,
    DignityRegistryCell,
    DignityRegistrySummary,
    MAIN_STAR_ENTITY_IDS,
    OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH,
    OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS,
    _DignityAnnotationFactory,
    _graded,
)
from .dignity_r3 import (
    DEPENDENCY_MINOR_DIGNITY_ENTITY_IDS,
    OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH,
    OperationalFullZiweiDignityGenerator,
)
from .dignity_registry_r4 import OPERATIONAL_R4_ADDED_DIGNITY_RAW_BY_BRANCH
from .models import DignityAnnotation, Placement


OPERATIONAL_R4_DIGNITY_RULE_SET_ID = "OPERATIONAL-ZIWEI-DIGNITY-R4"
OPERATIONAL_R4_DIGNITY_RULE_SET_VERSION = "4.0.0"


def _registry_cell(raw: tuple[str, str | None]) -> DignityRegistryCell:
    status, grade = raw
    return DignityRegistryCell(status=status, grade=grade)


OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH: dict[str, dict[str, DignityRegistryCell]] = {
    entity_id: {branch: _registry_cell(raw) for branch, raw in cells.items()}
    for entity_id, cells in OPERATIONAL_R4_ADDED_DIGNITY_RAW_BY_BRANCH.items()
}

R4_ADDED_DIGNITY_ENTITY_IDS = frozenset(OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH)
OPERATIONAL_R4_DIGNITY_ENTITY_IDS = (
    MAIN_STAR_ENTITY_IDS
    | CORE_AUX_DIGNITY_ENTITY_IDS
    | DEPENDENCY_MINOR_DIGNITY_ENTITY_IDS
    | R4_ADDED_DIGNITY_ENTITY_IDS
)


class OperationalZiweiDignityR4Generator(_DignityAnnotationFactory):
    """R4 project-owned Dignity for the 70-entity Ziwei V1 physical inventory."""

    rule_set_id = OPERATIONAL_R4_DIGNITY_RULE_SET_ID
    rule_set_version = OPERATIONAL_R4_DIGNITY_RULE_SET_VERSION

    @classmethod
    def validate_registry(cls) -> None:
        OperationalFullZiweiDignityGenerator.validate_registry()
        if R4_ADDED_DIGNITY_ENTITY_IDS != {
            "STAR.TIANSHOU",
            "STAR.TIANSHANG",
            "STAR.TIANSHI",
        }:
            raise DignityGenerationError("DIGNITY_R4_ADDED_ENTITY_SET")

        cell_count = 0
        graded = 0
        unrated = 0
        for entity_id, cells in OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH.items():
            if set(cells) != set("子丑寅卯辰巳午未申酉戌亥"):
                raise DignityGenerationError(f"DIGNITY_R4_INCOMPLETE_BRANCH_ROW:{entity_id}")
            for branch, state in cells.items():
                cell_count += 1
                if state.status not in DIGNITY_STATUSES:
                    raise DignityGenerationError(f"DIGNITY_INVALID_STATUS:{entity_id}:{branch}")
                if state.status == "GRADED":
                    graded += 1
                    if state.grade not in DIGNITY_GRADES:
                        raise DignityGenerationError(f"DIGNITY_INVALID_GRADE:{entity_id}:{branch}")
                else:
                    unrated += 1
                    if state.grade is not None:
                        raise DignityGenerationError(f"DIGNITY_UNRATED_HAS_GRADE:{entity_id}:{branch}")

        if cell_count != 36:
            raise DignityGenerationError(f"DIGNITY_R4_ADDED_CELL_COUNT:{cell_count}")
        if graded != 36 or unrated != 0:
            raise DignityGenerationError(f"DIGNITY_R4_ADDED_STATE_COUNTS:{graded}:{unrated}")

    @classmethod
    def registry_summary(cls) -> DignityRegistrySummary:
        cls.validate_registry()
        base = OperationalFullZiweiDignityGenerator.registry_summary()
        added = [
            state
            for cells in OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH.values()
            for state in cells.values()
        ]
        return DignityRegistrySummary(
            entity_count=len(OPERATIONAL_R4_DIGNITY_ENTITY_IDS),
            address_count=12,
            cell_count=base.cell_count + len(added),
            graded_cell_count=base.graded_cell_count + sum(state.status == "GRADED" for state in added),
            unrated_cell_count=base.unrated_cell_count + sum(state.status == "UNRATED" for state in added),
            rule_set_id=cls.rule_set_id,
            rule_set_version=cls.rule_set_version,
        )

    def generate(self, placements: tuple[Placement, ...] | list[Placement]) -> tuple[DignityAnnotation, ...]:
        self.validate_registry()
        by_entity: dict[str, Placement] = {}
        for row in placements:
            if row.entity_id not in OPERATIONAL_R4_DIGNITY_ENTITY_IDS:
                continue
            if row.entity_id in by_entity:
                raise DignityGenerationError(f"DIGNITY_DUPLICATE_TARGET_PLACEMENT:{row.entity_id}")
            by_entity[row.entity_id] = row

        missing = sorted(OPERATIONAL_R4_DIGNITY_ENTITY_IDS - set(by_entity))
        if missing:
            raise DignityGenerationError("DIGNITY_INCOMPLETE_R4_OPERATIONAL_PLACEMENTS:" + ",".join(missing))

        rows: list[DignityAnnotation] = []
        for entity_id in sorted(OPERATIONAL_R4_DIGNITY_ENTITY_IDS):
            placement = by_entity[entity_id]
            if entity_id in MAIN_STAR_ENTITY_IDS:
                state = _graded(OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS[entity_id][placement.address.index])
                evidence = f"CALIBRATION_FIXTURE:WENMO_MAIN_DIGNITY_R1:ADDRESS={placement.address.branch}"
            elif entity_id in CORE_AUX_DIGNITY_ENTITY_IDS:
                try:
                    state = OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH[entity_id][placement.address.branch]
                except KeyError as exc:
                    raise DignityGenerationError(
                        f"DIGNITY_UNREACHABLE_CORE_AUX_ADDRESS:{entity_id}:{placement.address.branch}"
                    ) from exc
                evidence = f"CALIBRATION_FIXTURE:WENMO_CORE_AUX_DIGNITY_R2:{entity_id}:{placement.address.branch}"
            elif entity_id in DEPENDENCY_MINOR_DIGNITY_ENTITY_IDS:
                try:
                    state = OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH[entity_id][placement.address.branch]
                except KeyError as exc:
                    raise DignityGenerationError(
                        f"DIGNITY_UNREACHABLE_DEPENDENCY_MINOR_ADDRESS:{entity_id}:{placement.address.branch}"
                    ) from exc
                evidence = f"CALIBRATION_FIXTURE:WENMO_DEPENDENCY_MINOR_DIGNITY_R3:{entity_id}:{placement.address.branch}"
            else:
                try:
                    state = OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH[entity_id][placement.address.branch]
                except KeyError as exc:
                    raise DignityGenerationError(
                        f"DIGNITY_UNREACHABLE_R4_ADDRESS:{entity_id}:{placement.address.branch}"
                    ) from exc
                evidence = f"CALIBRATION_FIXTURE:WENMO_TIANSHOU_TIANSHANG_TIANSHI_R4:{entity_id}:{placement.address.branch}"

            rows.append(
                self._annotation(
                    placement,
                    state,
                    rule_set_id=self.rule_set_id,
                    rule_set_version=self.rule_set_version,
                    source_refs=(
                        "OPERATIONAL_REGISTRY:OPERATIONAL-ZIWEI-DIGNITY-R4",
                        "CALIBRATION_EVIDENCE:WENMO_TIANJI:APP=2.5.9:API=1.1.2:STAR_CODE=C5VUC",
                        evidence,
                    ),
                )
            )
        return tuple(rows)

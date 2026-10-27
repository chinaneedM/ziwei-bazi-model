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
    OperationalZiweiDignityGenerator,
    _DignityAnnotationFactory,
    _graded,
)
from .dignity_registry_r3 import OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_RAW_BY_BRANCH
from .models import DignityAnnotation, Placement


OPERATIONAL_FULL_DIGNITY_RULE_SET_ID = "OPERATIONAL-ZIWEI-DIGNITY-R3"
OPERATIONAL_FULL_DIGNITY_RULE_SET_VERSION = "3.0.0"


def _registry_cell(raw: tuple[str, str | None]) -> DignityRegistryCell:
    status, grade = raw
    return DignityRegistryCell(status=status, grade=grade)


OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH: dict[str, dict[str, DignityRegistryCell]] = {
    entity_id: {branch: _registry_cell(raw) for branch, raw in cells.items()}
    for entity_id, cells in OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_RAW_BY_BRANCH.items()
}

DEPENDENCY_MINOR_DIGNITY_ENTITY_IDS = frozenset(OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH)
OPERATIONAL_FULL_DIGNITY_ENTITY_IDS = (
    MAIN_STAR_ENTITY_IDS | CORE_AUX_DIGNITY_ENTITY_IDS | DEPENDENCY_MINOR_DIGNITY_ENTITY_IDS
)


class OperationalFullZiweiDignityGenerator(_DignityAnnotationFactory):
    """R3 project-owned Dignity for every physical star currently emitted by Ziwei V1.

    R1 and R2 remain unchanged. R3 adds the four dependency stars and the 35
    operational minor stars. The dependency/minor rows are reachable-domain
    complete: impossible entity/address pairs are absent, while `UNRATED`
    explicitly records a calibrated no-seven-grade state.
    """

    rule_set_id = OPERATIONAL_FULL_DIGNITY_RULE_SET_ID
    rule_set_version = OPERATIONAL_FULL_DIGNITY_RULE_SET_VERSION

    @classmethod
    def validate_registry(cls) -> None:
        OperationalZiweiDignityGenerator.validate_registry()
        if len(OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH) != 39:
            raise DignityGenerationError("DIGNITY_DEPENDENCY_MINOR_REGISTRY_ENTITY_COUNT")

        cell_count = 0
        graded = 0
        unrated = 0
        for entity_id, cells in OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH.items():
            if not cells:
                raise DignityGenerationError(f"DIGNITY_EMPTY_DEPENDENCY_MINOR_ROW:{entity_id}")
            for branch, state in cells.items():
                cell_count += 1
                if branch not in "子丑寅卯辰巳午未申酉戌亥":
                    raise DignityGenerationError(f"DIGNITY_INVALID_BRANCH:{entity_id}:{branch}")
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

        if cell_count != 379:
            raise DignityGenerationError(f"DIGNITY_DEPENDENCY_MINOR_REACHABLE_CELL_COUNT:{cell_count}")
        if graded != 290 or unrated != 89:
            raise DignityGenerationError(f"DIGNITY_DEPENDENCY_MINOR_STATE_COUNTS:{graded}:{unrated}")

    @classmethod
    def registry_summary(cls) -> DignityRegistrySummary:
        cls.validate_registry()
        dependency_minor_cells = [
            state
            for cells in OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH.values()
            for state in cells.values()
        ]
        return DignityRegistrySummary(
            entity_count=len(OPERATIONAL_FULL_DIGNITY_ENTITY_IDS),
            address_count=12,
            cell_count=302 + len(dependency_minor_cells),
            graded_cell_count=299 + sum(state.status == "GRADED" for state in dependency_minor_cells),
            unrated_cell_count=3 + sum(state.status == "UNRATED" for state in dependency_minor_cells),
            rule_set_id=cls.rule_set_id,
            rule_set_version=cls.rule_set_version,
        )

    def generate(self, placements: tuple[Placement, ...] | list[Placement]) -> tuple[DignityAnnotation, ...]:
        self.validate_registry()
        by_entity: dict[str, Placement] = {}
        for row in placements:
            if row.entity_id not in OPERATIONAL_FULL_DIGNITY_ENTITY_IDS:
                continue
            if row.entity_id in by_entity:
                raise DignityGenerationError(f"DIGNITY_DUPLICATE_TARGET_PLACEMENT:{row.entity_id}")
            by_entity[row.entity_id] = row

        missing = sorted(OPERATIONAL_FULL_DIGNITY_ENTITY_IDS - set(by_entity))
        if missing:
            raise DignityGenerationError("DIGNITY_INCOMPLETE_R3_OPERATIONAL_PLACEMENTS:" + ",".join(missing))

        rows: list[DignityAnnotation] = []
        for entity_id in sorted(OPERATIONAL_FULL_DIGNITY_ENTITY_IDS):
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
            else:
                try:
                    state = OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_BY_BRANCH[entity_id][placement.address.branch]
                except KeyError as exc:
                    raise DignityGenerationError(
                        f"DIGNITY_UNREACHABLE_DEPENDENCY_MINOR_ADDRESS:{entity_id}:{placement.address.branch}"
                    ) from exc
                evidence = f"CALIBRATION_FIXTURE:WENMO_DEPENDENCY_MINOR_DIGNITY_R3:{entity_id}:{placement.address.branch}"

            rows.append(
                self._annotation(
                    placement,
                    state,
                    rule_set_id=self.rule_set_id,
                    rule_set_version=self.rule_set_version,
                    source_refs=(
                        "OPERATIONAL_REGISTRY:OPERATIONAL-ZIWEI-DIGNITY-R3",
                        "CALIBRATION_EVIDENCE:WENMO_TIANJI:APP=2.5.9:API=1.1.2:STAR_CODE=C5VUC",
                        evidence,
                    ),
                )
            )
        return tuple(rows)

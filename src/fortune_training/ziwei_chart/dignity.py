from __future__ import annotations

from dataclasses import dataclass

from .models import DignityAnnotation, Placement


DIGNITY_ALGORITHM_ID = "ZIWEI-DIGNITY-ANNOTATION-V1"
DIGNITY_ALGORITHM_VERSION = "1.1.0"
OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID = "OPERATIONAL-ZIWEI-MAIN-STAR-DIGNITY-R1"
OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_VERSION = "1.0.0"
OPERATIONAL_DIGNITY_RULE_SET_ID = "OPERATIONAL-ZIWEI-DIGNITY-R2"
OPERATIONAL_DIGNITY_RULE_SET_VERSION = "2.0.0"
DIGNITY_SCALE_ID = "ZIWEI-SEVEN-GRADE-DIGNITY-R1"
DIGNITY_SCALE_VERSION = "1.0.0"

DIGNITY_GRADES = frozenset({"庙", "旺", "得", "利", "平", "不", "陷"})
DIGNITY_STATUSES = frozenset({"GRADED", "UNRATED"})

# Z12 order: 子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥.
# This is the project's own operational registry. Its current values are
# calibration-backed but vendor-neutral at runtime. External software is a
# witness, not the identity or authority of this RuleSet.
OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS: dict[str, tuple[str, ...]] = {
    "STAR.ZIWEI": ("平", "庙", "旺", "旺", "得", "旺", "庙", "庙", "旺", "旺", "得", "旺"),
    "STAR.TIANJI": ("庙", "陷", "得", "旺", "利", "平", "庙", "陷", "得", "旺", "利", "平"),
    "STAR.TAIYANG": ("陷", "不", "旺", "庙", "旺", "旺", "旺", "得", "得", "平", "不", "陷"),
    "STAR.WUQU": ("旺", "庙", "得", "利", "庙", "平", "旺", "庙", "得", "利", "庙", "平"),
    "STAR.TIANTONG": ("旺", "不", "利", "平", "平", "庙", "陷", "不", "旺", "平", "平", "庙"),
    "STAR.LIANZHEN": ("平", "利", "庙", "平", "利", "陷", "平", "利", "庙", "平", "利", "陷"),
    "STAR.TIANFU": ("庙", "庙", "庙", "得", "庙", "得", "旺", "庙", "得", "旺", "庙", "得"),
    "STAR.TAIYIN": ("庙", "庙", "旺", "陷", "陷", "陷", "不", "不", "利", "旺", "旺", "庙"),
    "STAR.TANLANG": ("旺", "庙", "平", "利", "庙", "陷", "旺", "庙", "平", "利", "庙", "陷"),
    "STAR.JUMEN": ("旺", "不", "庙", "庙", "陷", "旺", "旺", "不", "庙", "庙", "陷", "旺"),
    "STAR.TIANXIANG": ("庙", "庙", "庙", "陷", "得", "得", "庙", "得", "庙", "陷", "得", "得"),
    "STAR.TIANLIANG": ("庙", "旺", "庙", "庙", "庙", "得", "庙", "旺", "陷", "得", "庙", "陷"),
    "STAR.QISHA": ("旺", "庙", "庙", "旺", "庙", "平", "旺", "庙", "庙", "旺", "庙", "平"),
    "STAR.POJUN": ("庙", "旺", "得", "陷", "旺", "平", "庙", "旺", "得", "陷", "旺", "平"),
}

MAIN_STAR_ENTITY_IDS = frozenset(OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS)


@dataclass(frozen=True)
class DignityRegistryCell:
    status: str
    grade: str | None


def _graded(grade: str) -> DignityRegistryCell:
    return DignityRegistryCell(status="GRADED", grade=grade)


def _unrated() -> DignityRegistryCell:
    return DignityRegistryCell(status="UNRATED", grade=None)


# Sparse by design: only generator-reachable addresses are registry facts.
# Impossible entity/address pairs are not represented as missing data.
OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH: dict[str, dict[str, DignityRegistryCell]] = {
    "STAR.WENCHANG": {b: _graded(g) for b, g in zip("子丑寅卯辰巳午未申酉戌亥", ("得", "庙", "陷", "利", "得", "庙", "陷", "利", "得", "庙", "陷", "利"))},
    "STAR.WENQU": {b: _graded(g) for b, g in zip("子丑寅卯辰巳午未申酉戌亥", ("得", "庙", "平", "旺", "得", "庙", "陷", "旺", "得", "庙", "陷", "旺"))},
    "STAR.ZUOFU": {b: _graded(g) for b, g in zip("子丑寅卯辰巳午未申酉戌亥", ("旺", "庙", "庙", "陷", "庙", "平", "旺", "庙", "平", "陷", "庙", "不"))},
    "STAR.YOUBI": {b: _graded(g) for b, g in zip("子丑寅卯辰巳午未申酉戌亥", ("庙", "庙", "旺", "陷", "庙", "平", "旺", "庙", "不", "陷", "庙", "平"))},
    "STAR.TIANKUI": {"子": _graded("旺"), "丑": _graded("旺"), "寅": _unrated(), "卯": _graded("庙"), "亥": _graded("旺")},
    "STAR.TIANYUE": {"巳": _graded("旺"), "午": _unrated(), "未": _graded("旺"), "申": _graded("庙"), "酉": _graded("庙")},
    "STAR.TIANMA": {"寅": _graded("旺"), "巳": _graded("平"), "申": _graded("旺"), "亥": _graded("平")},
    "STAR.LUCUN": {"子": _graded("庙"), "寅": _graded("庙"), "卯": _graded("庙"), "巳": _graded("庙"), "午": _graded("庙"), "申": _graded("庙"), "酉": _graded("庙"), "亥": _graded("庙")},
    "STAR.QINGYANG": {"子": _graded("陷"), "丑": _graded("庙"), "卯": _graded("陷"), "辰": _graded("庙"), "午": _graded("陷"), "未": _graded("庙"), "酉": _graded("陷"), "戌": _graded("庙")},
    "STAR.TUOLUO": {"丑": _graded("庙"), "寅": _graded("陷"), "辰": _graded("庙"), "巳": _graded("陷"), "未": _graded("庙"), "申": _graded("陷"), "戌": _graded("庙"), "亥": _graded("陷")},
    "STAR.DIKONG": {b: _graded(g) for b, g in zip("子丑寅卯辰巳午未申酉戌亥", ("平", "陷", "陷", "平", "陷", "庙", "庙", "平", "庙", "庙", "陷", "陷"))},
    "STAR.DIJIE": {"子": _graded("陷"), "丑": _graded("陷"), "寅": _graded("平"), "卯": _graded("平"), "辰": _graded("陷"), "巳": _graded("不"), "午": _graded("庙"), "未": _graded("平"), "申": _graded("庙"), "酉": _graded("平"), "戌": _graded("平"), "亥": _unrated()},
    "STAR.HUOXING": {b: _graded(g) for b, g in zip("子丑寅卯辰巳午未申酉戌亥", ("陷", "得", "庙", "利", "陷", "得", "庙", "利", "陷", "得", "庙", "利"))},
    "STAR.LINGXING": {b: _graded(g) for b, g in zip("子丑寅卯辰巳午未申酉戌亥", ("陷", "得", "庙", "利", "陷", "得", "庙", "利", "陷", "得", "庙", "利"))},
}

CORE_AUX_DIGNITY_ENTITY_IDS = frozenset(OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH)
OPERATIONAL_DIGNITY_ENTITY_IDS = MAIN_STAR_ENTITY_IDS | CORE_AUX_DIGNITY_ENTITY_IDS


class DignityGenerationError(ValueError):
    def __init__(self, diagnostic_code: str) -> None:
        super().__init__(diagnostic_code)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class DignityRegistrySummary:
    entity_count: int
    address_count: int
    cell_count: int
    graded_cell_count: int = 0
    unrated_cell_count: int = 0
    rule_set_id: str = OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID
    rule_set_version: str = OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_VERSION


class _DignityAnnotationFactory:
    algorithm_id = DIGNITY_ALGORITHM_ID
    algorithm_version = DIGNITY_ALGORITHM_VERSION
    scale_id = DIGNITY_SCALE_ID
    scale_version = DIGNITY_SCALE_VERSION

    @classmethod
    def _annotation(
        cls,
        placement: Placement,
        state: DignityRegistryCell,
        *,
        rule_set_id: str,
        rule_set_version: str,
        source_refs: tuple[str, ...],
    ) -> DignityAnnotation:
        return DignityAnnotation(
            annotation_id=f"DIGNITY:{placement.entity_id}:{placement.address.branch}",
            annotation_type="DIGNITY",
            target_entity_id=placement.entity_id,
            target_address=placement.address,
            grade=state.grade,
            scale_id=cls.scale_id,
            scale_version=cls.scale_version,
            rule_set_id=rule_set_id,
            rule_set_version=rule_set_version,
            generator_id=cls.algorithm_id,
            algorithm_version=cls.algorithm_version,
            source_refs=source_refs,
            status=state.status,
        )


class OperationalMainStarDignityGenerator(_DignityAnnotationFactory):
    """Backward-compatible R1: attach main-star graded annotations only."""

    rule_set_id = OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID
    rule_set_version = OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_VERSION

    @classmethod
    def registry_summary(cls) -> DignityRegistrySummary:
        return DignityRegistrySummary(
            entity_count=len(OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS),
            address_count=12,
            cell_count=sum(len(row) for row in OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS.values()),
            graded_cell_count=168,
            rule_set_id=cls.rule_set_id,
            rule_set_version=cls.rule_set_version,
        )

    @classmethod
    def validate_registry(cls) -> None:
        if len(OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS) != 14:
            raise DignityGenerationError("DIGNITY_MAIN_STAR_REGISTRY_ENTITY_COUNT")
        for entity_id, row in OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS.items():
            if len(row) != 12:
                raise DignityGenerationError(f"DIGNITY_INCOMPLETE_ADDRESS_ROW:{entity_id}")
            if any(grade not in DIGNITY_GRADES for grade in row):
                raise DignityGenerationError(f"DIGNITY_INVALID_GRADE:{entity_id}")

    def generate(self, placements: tuple[Placement, ...] | list[Placement]) -> tuple[DignityAnnotation, ...]:
        self.validate_registry()
        by_entity: dict[str, Placement] = {}
        for row in placements:
            if row.entity_id not in MAIN_STAR_ENTITY_IDS:
                continue
            if row.entity_id in by_entity:
                raise DignityGenerationError("DIGNITY_DUPLICATE_MAIN_STAR_PLACEMENT")
            by_entity[row.entity_id] = row
        if set(by_entity) != set(MAIN_STAR_ENTITY_IDS):
            missing = sorted(set(MAIN_STAR_ENTITY_IDS) - set(by_entity))
            raise DignityGenerationError("DIGNITY_INCOMPLETE_MAIN_STAR_PLACEMENTS:" + ",".join(missing))

        ziwei_anchor = by_entity["STAR.ZIWEI"].address.branch
        rows: list[DignityAnnotation] = []
        for entity_id in sorted(MAIN_STAR_ENTITY_IDS):
            placement = by_entity[entity_id]
            state = _graded(OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS[entity_id][placement.address.index])
            rows.append(
                self._annotation(
                    placement,
                    state,
                    rule_set_id=self.rule_set_id,
                    rule_set_version=self.rule_set_version,
                    source_refs=(
                        "OPERATIONAL_REGISTRY:OPERATIONAL-ZIWEI-MAIN-STAR-DIGNITY-R1",
                        "CALIBRATION_EVIDENCE:WENMO_TIANJI:APP=2.5.9:API=1.1.2:STAR_CODE=C5VUC",
                        f"CALIBRATION_FIXTURE:WENMO_MAIN_DIGNITY_R1:ZIWEI_ANCHOR={ziwei_anchor}",
                    ),
                )
            )
        return tuple(rows)


class OperationalZiweiDignityGenerator(_DignityAnnotationFactory):
    """R2 project-owned Dignity for all main stars and the 14 core auxiliaries.

    Core auxiliary rows are reachable-domain complete. An address that its
    placement generator cannot produce is not a registry gap. `UNRATED` is an
    explicit state with no seven-grade value, distinct from 平 and from missing
    calibration evidence.
    """

    rule_set_id = OPERATIONAL_DIGNITY_RULE_SET_ID
    rule_set_version = OPERATIONAL_DIGNITY_RULE_SET_VERSION

    @classmethod
    def validate_registry(cls) -> None:
        OperationalMainStarDignityGenerator.validate_registry()
        if len(OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH) != 14:
            raise DignityGenerationError("DIGNITY_CORE_AUX_REGISTRY_ENTITY_COUNT")
        cell_count = 0
        graded = 0
        unrated = 0
        for entity_id, cells in OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH.items():
            if not cells:
                raise DignityGenerationError(f"DIGNITY_EMPTY_CORE_AUX_ROW:{entity_id}")
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
        if cell_count != 134:
            raise DignityGenerationError(f"DIGNITY_CORE_AUX_REACHABLE_CELL_COUNT:{cell_count}")
        if graded != 131 or unrated != 3:
            raise DignityGenerationError(f"DIGNITY_CORE_AUX_STATE_COUNTS:{graded}:{unrated}")

    @classmethod
    def registry_summary(cls) -> DignityRegistrySummary:
        cls.validate_registry()
        aux_cells = [state for cells in OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH.values() for state in cells.values()]
        return DignityRegistrySummary(
            entity_count=len(OPERATIONAL_DIGNITY_ENTITY_IDS),
            address_count=12,
            cell_count=168 + len(aux_cells),
            graded_cell_count=168 + sum(state.status == "GRADED" for state in aux_cells),
            unrated_cell_count=sum(state.status == "UNRATED" for state in aux_cells),
            rule_set_id=cls.rule_set_id,
            rule_set_version=cls.rule_set_version,
        )

    def generate(self, placements: tuple[Placement, ...] | list[Placement]) -> tuple[DignityAnnotation, ...]:
        self.validate_registry()
        by_entity: dict[str, Placement] = {}
        for row in placements:
            if row.entity_id not in OPERATIONAL_DIGNITY_ENTITY_IDS:
                continue
            if row.entity_id in by_entity:
                raise DignityGenerationError(f"DIGNITY_DUPLICATE_TARGET_PLACEMENT:{row.entity_id}")
            by_entity[row.entity_id] = row
        missing = sorted(OPERATIONAL_DIGNITY_ENTITY_IDS - set(by_entity))
        if missing:
            raise DignityGenerationError("DIGNITY_INCOMPLETE_OPERATIONAL_PLACEMENTS:" + ",".join(missing))

        rows: list[DignityAnnotation] = []
        for entity_id in sorted(OPERATIONAL_DIGNITY_ENTITY_IDS):
            placement = by_entity[entity_id]
            if entity_id in MAIN_STAR_ENTITY_IDS:
                state = _graded(OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS[entity_id][placement.address.index])
                evidence = f"CALIBRATION_FIXTURE:WENMO_MAIN_DIGNITY_R1:ADDRESS={placement.address.branch}"
            else:
                try:
                    state = OPERATIONAL_CORE_AUX_DIGNITY_BY_BRANCH[entity_id][placement.address.branch]
                except KeyError as exc:
                    raise DignityGenerationError(
                        f"DIGNITY_UNREACHABLE_CORE_AUX_ADDRESS:{entity_id}:{placement.address.branch}"
                    ) from exc
                evidence = f"CALIBRATION_FIXTURE:WENMO_CORE_AUX_DIGNITY_R2:{entity_id}:{placement.address.branch}"
            rows.append(
                self._annotation(
                    placement,
                    state,
                    rule_set_id=self.rule_set_id,
                    rule_set_version=self.rule_set_version,
                    source_refs=(
                        "OPERATIONAL_REGISTRY:OPERATIONAL-ZIWEI-DIGNITY-R2",
                        "CALIBRATION_EVIDENCE:WENMO_TIANJI:APP=2.5.9:API=1.1.2:STAR_CODE=C5VUC",
                        evidence,
                    ),
                )
            )
        return tuple(rows)

from __future__ import annotations

from dataclasses import dataclass

from .models import DignityAnnotation, Placement


DIGNITY_ALGORITHM_ID = "ZIWEI-DIGNITY-ANNOTATION-V1"
DIGNITY_ALGORITHM_VERSION = "1.0.0"
OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID = "OPERATIONAL-ZIWEI-MAIN-STAR-DIGNITY-R1"
OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_VERSION = "1.0.0"
DIGNITY_SCALE_ID = "ZIWEI-SEVEN-GRADE-DIGNITY-R1"
DIGNITY_SCALE_VERSION = "1.0.0"

DIGNITY_GRADES = frozenset({"庙", "旺", "得", "利", "平", "不", "陷"})

# Z12 order: 子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥.
# This is the project's own operational registry. Its current R1 values were
# calibrated against an external Wenmo Tianji observation set, but the runtime
# identity is vendor-neutral and may later be revalidated against additional
# witnesses without changing ChartState or renderer semantics.
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


class DignityGenerationError(ValueError):
    def __init__(self, diagnostic_code: str) -> None:
        super().__init__(diagnostic_code)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class DignityRegistrySummary:
    entity_count: int
    address_count: int
    cell_count: int
    rule_set_id: str = OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID
    rule_set_version: str = OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_VERSION


class OperationalMainStarDignityGenerator:
    """Attach project-owned profile-bound dignity annotations without mutating placements."""

    rule_set_id = OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID
    rule_set_version = OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_VERSION
    algorithm_id = DIGNITY_ALGORITHM_ID
    algorithm_version = DIGNITY_ALGORITHM_VERSION
    scale_id = DIGNITY_SCALE_ID
    scale_version = DIGNITY_SCALE_VERSION

    @classmethod
    def registry_summary(cls) -> DignityRegistrySummary:
        return DignityRegistrySummary(
            entity_count=len(OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS),
            address_count=12,
            cell_count=sum(len(row) for row in OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS.values()),
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
        main_rows = [row for row in placements if row.entity_id in MAIN_STAR_ENTITY_IDS]
        by_entity: dict[str, Placement] = {}
        for row in main_rows:
            if row.entity_id in by_entity:
                raise DignityGenerationError("DIGNITY_DUPLICATE_MAIN_STAR_PLACEMENT")
            by_entity[row.entity_id] = row
        if set(by_entity) != set(MAIN_STAR_ENTITY_IDS):
            missing = sorted(set(MAIN_STAR_ENTITY_IDS) - set(by_entity))
            raise DignityGenerationError("DIGNITY_INCOMPLETE_MAIN_STAR_PLACEMENTS:" + ",".join(missing))

        ziwei_anchor = by_entity["STAR.ZIWEI"].address.branch
        source_refs = (
            "OPERATIONAL_REGISTRY:OPERATIONAL-ZIWEI-MAIN-STAR-DIGNITY-R1",
            "CALIBRATION_EVIDENCE:WENMO_TIANJI:APP=2.5.9:API=1.1.2:STAR_CODE=C5VUC",
            f"CALIBRATION_FIXTURE:WENMO_MAIN_DIGNITY_R1:ZIWEI_ANCHOR={ziwei_anchor}",
        )
        rows: list[DignityAnnotation] = []
        for entity_id in sorted(MAIN_STAR_ENTITY_IDS):
            placement = by_entity[entity_id]
            grade = OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS[entity_id][placement.address.index]
            rows.append(
                DignityAnnotation(
                    annotation_id=f"DIGNITY:{entity_id}:{placement.address.branch}",
                    annotation_type="DIGNITY",
                    target_entity_id=entity_id,
                    target_address=placement.address,
                    grade=grade,
                    scale_id=self.scale_id,
                    scale_version=self.scale_version,
                    rule_set_id=self.rule_set_id,
                    rule_set_version=self.rule_set_version,
                    generator_id=self.algorithm_id,
                    algorithm_version=self.algorithm_version,
                    source_refs=source_refs,
                )
            )
        return tuple(rows)

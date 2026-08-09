from __future__ import annotations

from dataclasses import dataclass

from .models import Placement, TransformationActivation


TRANSFORMATION_ALGORITHM_ID = "ZIWEI-TRANSFORMATION-ACTIVATION-V1"
TRANSFORMATION_ALGORITHM_VERSION = "1.0.0"
S08_TRANSFORMATION_RULE_SET_ID = "S08_CURRENT_40_ASSIGNMENT_R1"
S08_TRANSFORMATION_RULE_SET_VERSION = "1.0.0"


class TransformationGenerationError(ValueError):
    def __init__(self, diagnostic_code: str) -> None:
        super().__init__(diagnostic_code)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class TransformationAssignment:
    assignment_id: str
    mechanism_id: str
    source_stem: str
    transformation_type: str
    target_entity_id: str
    target_display_name: str


# Canonical S08 "唯一运行四化表".  Order is always 禄、权、科、忌.
_TARGETS = {
    "甲": (("廉贞", "STAR.LIANZHEN"), ("破军", "STAR.POJUN"), ("武曲", "STAR.WUQU"), ("太阳", "STAR.TAIYANG")),
    "乙": (("天机", "STAR.TIANJI"), ("天梁", "STAR.TIANLIANG"), ("紫微", "STAR.ZIWEI"), ("太阴", "STAR.TAIYIN")),
    "丙": (("天同", "STAR.TIANTONG"), ("天机", "STAR.TIANJI"), ("文昌", "STAR.WENCHANG"), ("廉贞", "STAR.LIANZHEN")),
    "丁": (("太阴", "STAR.TAIYIN"), ("天同", "STAR.TIANTONG"), ("天机", "STAR.TIANJI"), ("巨门", "STAR.JUMEN")),
    "戊": (("贪狼", "STAR.TANLANG"), ("太阴", "STAR.TAIYIN"), ("右弼", "STAR.YOUBI"), ("天机", "STAR.TIANJI")),
    "己": (("武曲", "STAR.WUQU"), ("贪狼", "STAR.TANLANG"), ("天梁", "STAR.TIANLIANG"), ("文曲", "STAR.WENQU")),
    "庚": (("太阳", "STAR.TAIYANG"), ("武曲", "STAR.WUQU"), ("太阴", "STAR.TAIYIN"), ("天同", "STAR.TIANTONG")),
    "辛": (("巨门", "STAR.JUMEN"), ("太阳", "STAR.TAIYANG"), ("文曲", "STAR.WENQU"), ("文昌", "STAR.WENCHANG")),
    "壬": (("天梁", "STAR.TIANLIANG"), ("紫微", "STAR.ZIWEI"), ("左辅", "STAR.ZUOFU"), ("武曲", "STAR.WUQU")),
    "癸": (("破军", "STAR.POJUN"), ("巨门", "STAR.JUMEN"), ("太阴", "STAR.TAIYIN"), ("贪狼", "STAR.TANLANG")),
}
_TYPES = ("化禄", "化权", "化科", "化忌")
# S08-ASG-39 intentionally shares S08-TN-27 with 庚太阴科.
_MECHANISM_NUMBERS = (
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 16,
    17, 18, 19, 20,
    21, 22, 23, 24,
    25, 26, 27, 28,
    29, 30, 31, 32,
    33, 34, 35, 36,
    37, 38, 27, 39,
)


def _build_assignments() -> dict[str, tuple[TransformationAssignment, ...]]:
    rows: dict[str, tuple[TransformationAssignment, ...]] = {}
    assignment_number = 1
    mechanism_offset = 0
    for stem, targets in _TARGETS.items():
        stem_rows: list[TransformationAssignment] = []
        for transformation_type, (display_name, entity_id) in zip(_TYPES, targets, strict=True):
            mechanism_number = _MECHANISM_NUMBERS[mechanism_offset]
            stem_rows.append(
                TransformationAssignment(
                    assignment_id=f"S08-ASG-{assignment_number:02d}",
                    mechanism_id=f"S08-TN-{mechanism_number:02d}",
                    source_stem=stem,
                    transformation_type=transformation_type,
                    target_entity_id=entity_id,
                    target_display_name=display_name,
                )
            )
            assignment_number += 1
            mechanism_offset += 1
        rows[stem] = tuple(stem_rows)
    return rows


ASSIGNMENTS_BY_STEM = _build_assignments()


class TransformationGenerator:
    """Activate S08 transformations against immutable physical star placements.

    The same generator is intentionally reusable for natal, palace-stem, Daxian,
    annual and monthly contexts.  Context changes the causal stem/layer; it never
    moves the target star's physical address.
    """

    rule_set_id = S08_TRANSFORMATION_RULE_SET_ID
    rule_set_version = S08_TRANSFORMATION_RULE_SET_VERSION

    @staticmethod
    def assignments(source_stem: str) -> tuple[TransformationAssignment, ...]:
        try:
            return ASSIGNMENTS_BY_STEM[source_stem]
        except KeyError as exc:
            raise ValueError(f"unsupported transformation source stem: {source_stem}") from exc

    def activate(
        self,
        source_stem: str,
        placements: tuple[Placement, ...] | list[Placement],
        *,
        source_layer: str,
        context_id: str,
    ) -> tuple[TransformationActivation, ...]:
        by_entity: dict[str, Placement] = {}
        for placement in placements:
            if placement.entity_id in by_entity:
                raise TransformationGenerationError("TRANSFORMATION_DUPLICATE_TARGET_ENTITY_PLACEMENT")
            by_entity[placement.entity_id] = placement

        rows: list[TransformationActivation] = []
        for assignment in self.assignments(source_stem):
            try:
                target = by_entity[assignment.target_entity_id]
            except KeyError as exc:
                raise TransformationGenerationError(
                    f"TRANSFORMATION_TARGET_PLACEMENT_MISSING:{assignment.target_entity_id}"
                ) from exc
            rows.append(
                TransformationActivation(
                    activation_id=f"{context_id}:{assignment.assignment_id}",
                    transformation_type=assignment.transformation_type,
                    target_entity_id=assignment.target_entity_id,
                    target_display_name=assignment.target_display_name,
                    target_address=target.address,
                    source_layer=source_layer,
                    source_stem=source_stem,
                    context_id=context_id,
                    assignment_id=assignment.assignment_id,
                    mechanism_id=assignment.mechanism_id,
                    generator_id=TRANSFORMATION_ALGORITHM_ID,
                    algorithm_version=TRANSFORMATION_ALGORITHM_VERSION,
                    source_refs=(
                        f"S08:{assignment.assignment_id}",
                        f"S08:{assignment.mechanism_id}",
                    ),
                )
            )
        return tuple(rows)

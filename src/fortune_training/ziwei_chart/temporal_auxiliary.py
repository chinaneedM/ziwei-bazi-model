from __future__ import annotations

from .auxiliary import BRANCH_TO_INDEX, QSCoreAuxiliaryGenerator
from .models import TemporalAuxiliaryActivation
from .registries import address


TEMPORAL_AUXILIARY_RULE_ID = "S10-STEM-LUCUN-QINGYANG-TUOLUO-R1"
TEMPORAL_AUXILIARY_GENERATOR_ID = "ZIWEI-TEMPORAL-LUCUN-YANG-TUO-V1"
TEMPORAL_AUXILIARY_ALGORITHM_VERSION = "1.0.0"
TEMPORAL_CHANG_QU_RULE_ID = "S10-STEM-FLOW-WENCHANG-WENQU-R1"
TEMPORAL_CHANG_QU_GENERATOR_ID = "ZIWEI-TEMPORAL-FLOW-WENCHANG-WENQU-V1"
TEMPORAL_CHANG_QU_ALGORITHM_VERSION = "1.0.0"


# S10:ZZZA-A-1101 / S10:ZZZA-A-1102. The source table intentionally has no
# 辰、戌、丑、未 result; alternative schools must be represented separately.
FLOW_CHANG_QU_BY_STEM = {
    "甲": ("巳", "酉"),
    "乙": ("午", "申"),
    "丙": ("申", "午"),
    "丁": ("酉", "巳"),
    "戊": ("申", "午"),
    "己": ("酉", "巳"),
    "庚": ("亥", "卯"),
    "辛": ("子", "寅"),
    "壬": ("寅", "子"),
    "癸": ("卯", "亥"),
}


class TemporalAuxiliaryGenerator:
    """Activate source-layer 禄羊陀、流昌曲 without merging natal instances."""

    rule_id = TEMPORAL_AUXILIARY_RULE_ID
    generator_id = TEMPORAL_AUXILIARY_GENERATOR_ID
    algorithm_version = TEMPORAL_AUXILIARY_ALGORITHM_VERSION

    @staticmethod
    def activate(
        source_stem: str,
        *,
        source_layer: str,
        context_id: str,
        temporal_source_refs: tuple[str, ...],
    ) -> tuple[TemporalAuxiliaryActivation, ...]:
        placements = QSCoreAuxiliaryGenerator.lucun_yang_tuo(source_stem)
        lucun_yang_tuo = tuple(
            TemporalAuxiliaryActivation(
                activation_id=f"{context_id}:{row.entity_id}",
                entity_id=row.entity_id,
                display_name=row.display_name,
                target_address=row.address,
                source_layer=source_layer,
                source_stem=source_stem,
                context_id=context_id,
                rule_id=TEMPORAL_AUXILIARY_RULE_ID,
                generator_id=TEMPORAL_AUXILIARY_GENERATOR_ID,
                algorithm_version=TEMPORAL_AUXILIARY_ALGORITHM_VERSION,
                source_refs=temporal_source_refs + row.source_refs,
            )
            for row in placements
        )
        try:
            chang_branch, qu_branch = FLOW_CHANG_QU_BY_STEM[source_stem]
        except KeyError as exc:
            raise ValueError(f"unsupported temporal source stem: {source_stem}") from exc
        chang_qu_source_refs = temporal_source_refs + (
            "S10:ZZZA-A-1097",
            "S10:ZZZA-A-1098",
            "S10:ZZZA-A-1099",
            "S10:ZZZA-A-1100",
            "S10:ZZZA-A-1103",
        )
        chang_qu = tuple(
            TemporalAuxiliaryActivation(
                activation_id=f"{context_id}:{entity_id}",
                entity_id=entity_id,
                display_name=display_name,
                target_address=address(BRANCH_TO_INDEX[branch]),
                source_layer=source_layer,
                source_stem=source_stem,
                context_id=context_id,
                rule_id=TEMPORAL_CHANG_QU_RULE_ID,
                generator_id=TEMPORAL_CHANG_QU_GENERATOR_ID,
                algorithm_version=TEMPORAL_CHANG_QU_ALGORITHM_VERSION,
                source_refs=chang_qu_source_refs + (formula_ref,),
            )
            for entity_id, display_name, branch, formula_ref in (
                ("STAR.WENCHANG", "文昌", chang_branch, "S10:ZZZA-A-1101"),
                ("STAR.WENQU", "文曲", qu_branch, "S10:ZZZA-A-1102"),
            )
        )
        return lucun_yang_tuo + chang_qu

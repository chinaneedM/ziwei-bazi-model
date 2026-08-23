from __future__ import annotations

from .auxiliary import QSCoreAuxiliaryGenerator
from .models import TemporalAuxiliaryActivation


TEMPORAL_AUXILIARY_RULE_ID = "S10-STEM-LUCUN-QINGYANG-TUOLUO-R1"
TEMPORAL_AUXILIARY_GENERATOR_ID = "ZIWEI-TEMPORAL-LUCUN-YANG-TUO-V1"
TEMPORAL_AUXILIARY_ALGORITHM_VERSION = "1.0.0"


class TemporalAuxiliaryGenerator:
    """Activate source-layer 禄存、擎羊、陀罗 without merging natal instances."""

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
        return tuple(
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

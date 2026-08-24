from __future__ import annotations

from dataclasses import replace

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .auxiliary import (
    BRANCH_TO_INDEX,
    KUI_YUE_BY_STEM,
    WENMO_KUI_YUE_BY_STEM,
    QSCoreAuxiliaryGenerator,
)
from .models import (
    TemporalAuxiliaryActivation,
    TemporalAuxiliaryCandidateSet,
    TemporalAuxiliaryMethodCandidate,
)
from .registries import address


TEMPORAL_AUXILIARY_RULE_ID = "S10-STEM-LUCUN-QINGYANG-TUOLUO-R1"
TEMPORAL_AUXILIARY_GENERATOR_ID = "ZIWEI-TEMPORAL-LUCUN-YANG-TUO-V1"
TEMPORAL_AUXILIARY_ALGORITHM_VERSION = "1.0.0"
TEMPORAL_CHANG_QU_RULE_ID = "S10-STEM-FLOW-WENCHANG-WENQU-R1"
TEMPORAL_CHANG_QU_GENERATOR_ID = "ZIWEI-TEMPORAL-FLOW-WENCHANG-WENQU-V1"
TEMPORAL_CHANG_QU_ALGORITHM_VERSION = "1.0.0"
TEMPORAL_KUI_YUE_RULE_ID = "S10-STEM-FLOW-KUI-YUE-CANDIDATES-R1"
TEMPORAL_KUI_YUE_GENERATOR_ID = "ZIWEI-TEMPORAL-FLOW-KUI-YUE-CANDIDATES-V1"
TEMPORAL_KUI_YUE_ALGORITHM_VERSION = "1.0.0"
TEMPORAL_KUI_YUE_CANDIDATE_SET_HASH_ID = "ZIWEI-TEMPORAL-AUX-CANDIDATE-SET-HASH-R1"
TEMPORAL_KUI_YUE_CANDIDATE_SET_HASH_VERSION = "1.0.0"
STRICT_KUI_YUE_METHOD_ID = "S01-QS-STRICT-KUI-YUE-R1"
WENMO_KUI_YUE_METHOD_ID = "COMPAT-WENMO-KUI-YUE-R1"
KUI_YUE_SELECTION_STATUS = "CANDIDATES_PRESERVED_NO_SELECTION"
KUI_YUE_ENTITY_IDS = ("STAR.TIANKUI", "STAR.TIANYUE")
KUI_YUE_SOURCE_REFS = (
    "S10:ZZZA-A-1097",
    "S10:ZZZA-A-1098",
    "S10:ZZZA-A-1099",
    "S01:ZZQS-A-1800",
    "S01:ZZQS-A-1801",
    "S01:ZZZA-PR-019",
    "COMPAT:WENMO-CHARTDIFF-005",
)


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


def temporal_auxiliary_method_candidate_hashes(
    candidate: TemporalAuxiliaryMethodCandidate,
) -> tuple[str, str]:
    fact_hash = object_sha256(
        {
            "candidate_id": candidate.candidate_id,
            "method_id": candidate.method_id,
            "authority_status": candidate.authority_status,
            "activations": [json_value(row) for row in candidate.activations],
        }
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_refs": candidate.source_refs,
            "algorithm": (
                f"{TEMPORAL_KUI_YUE_CANDIDATE_SET_HASH_ID}@"
                f"{TEMPORAL_KUI_YUE_CANDIDATE_SET_HASH_VERSION}"
            ),
        }
    )
    return fact_hash, computation_hash


def temporal_auxiliary_candidate_set_hashes(
    candidate_set: TemporalAuxiliaryCandidateSet,
) -> tuple[str, str]:
    fact_hash = object_sha256(
        {
            "candidate_set_id": candidate_set.candidate_set_id,
            "source_layer": candidate_set.source_layer,
            "source_stem": candidate_set.source_stem,
            "context_id": candidate_set.context_id,
            "entity_ids": candidate_set.entity_ids,
            "selection_status": candidate_set.selection_status,
            "method_candidates": tuple(
                (row.candidate_id, row.method_id, row.authority_status, row.fact_hash)
                for row in candidate_set.method_candidates
            ),
        }
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "method_candidate_computation_hashes": tuple(
                row.computation_hash for row in candidate_set.method_candidates
            ),
            "source_refs": candidate_set.source_refs,
            "algorithm": (
                f"{TEMPORAL_KUI_YUE_CANDIDATE_SET_HASH_ID}@"
                f"{TEMPORAL_KUI_YUE_CANDIDATE_SET_HASH_VERSION}"
            ),
        }
    )
    return fact_hash, computation_hash


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

    @staticmethod
    def _kui_yue_method_candidate(
        source_stem: str,
        *,
        source_layer: str,
        context_id: str,
        method_id: str,
        authority_status: str,
        branches: tuple[str, str],
        temporal_source_refs: tuple[str, ...],
        method_source_refs: tuple[str, ...],
    ) -> TemporalAuxiliaryMethodCandidate:
        candidate_id = f"{context_id}:KUI_YUE:{method_id}"
        activations = tuple(
            TemporalAuxiliaryActivation(
                activation_id=f"{candidate_id}:{entity_id}",
                entity_id=entity_id,
                display_name=display_name,
                target_address=address(BRANCH_TO_INDEX[branch]),
                source_layer=source_layer,
                source_stem=source_stem,
                context_id=context_id,
                rule_id=TEMPORAL_KUI_YUE_RULE_ID,
                generator_id=TEMPORAL_KUI_YUE_GENERATOR_ID,
                algorithm_version=TEMPORAL_KUI_YUE_ALGORITHM_VERSION,
                source_refs=temporal_source_refs + method_source_refs,
            )
            for entity_id, display_name, branch in (
                ("STAR.TIANKUI", "天魁", branches[0]),
                ("STAR.TIANYUE", "天钺", branches[1]),
            )
        )
        source_refs = temporal_source_refs + method_source_refs
        provisional = TemporalAuxiliaryMethodCandidate(
            candidate_id=candidate_id,
            method_id=method_id,
            authority_status=authority_status,
            activations=activations,
            source_refs=source_refs,
            fact_hash="",
            computation_hash="",
        )
        fact_hash, computation_hash = temporal_auxiliary_method_candidate_hashes(provisional)
        return replace(provisional, fact_hash=fact_hash, computation_hash=computation_hash)

    @classmethod
    def kui_yue_candidate_set(
        cls,
        source_stem: str,
        *,
        source_layer: str,
        context_id: str,
        temporal_source_refs: tuple[str, ...],
    ) -> TemporalAuxiliaryCandidateSet:
        try:
            strict_branches = KUI_YUE_BY_STEM[source_stem]
            wenmo_branches = WENMO_KUI_YUE_BY_STEM[source_stem]
        except KeyError as exc:
            raise ValueError(f"unsupported temporal source stem: {source_stem}") from exc
        strict = cls._kui_yue_method_candidate(
            source_stem,
            source_layer=source_layer,
            context_id=context_id,
            method_id=STRICT_KUI_YUE_METHOD_ID,
            authority_status="CANONICAL_SOURCE_TABLE",
            branches=strict_branches,
            temporal_source_refs=temporal_source_refs,
            method_source_refs=(
                "S10:ZZZA-A-1097",
                "S10:ZZZA-A-1098",
                "S10:ZZZA-A-1099",
                "S01:ZZQS-A-1800",
                "S01:ZZQS-A-1801",
                "S01:ZZZA-PR-019",
            ),
        )
        wenmo = cls._kui_yue_method_candidate(
            source_stem,
            source_layer=source_layer,
            context_id=context_id,
            method_id=WENMO_KUI_YUE_METHOD_ID,
            authority_status="EXTERNAL_CASE_COMPATIBILITY",
            branches=wenmo_branches,
            temporal_source_refs=temporal_source_refs,
            method_source_refs=(
                (
                    "S10:ZZZA-A-1097",
                    "S10:ZZZA-A-1098",
                    "S10:ZZZA-A-1099",
                    "S01:ZZZA-PR-019",
                    "COMPAT:WENMO-CHARTDIFF-005",
                )
                if source_stem == "辛"
                else (
                    "S10:ZZZA-A-1097",
                    "S10:ZZZA-A-1098",
                    "S10:ZZZA-A-1099",
                    "S01:ZZQS-A-1800",
                    "S01:ZZQS-A-1801",
                    "S01:ZZZA-PR-019",
                )
            ),
        )
        candidate_set_id = f"{context_id}:KUI_YUE:CANDIDATE_SET"
        provisional = TemporalAuxiliaryCandidateSet(
            candidate_set_id=candidate_set_id,
            source_layer=source_layer,
            source_stem=source_stem,
            context_id=context_id,
            entity_ids=KUI_YUE_ENTITY_IDS,
            selection_status=KUI_YUE_SELECTION_STATUS,
            method_candidates=(strict, wenmo),
            source_refs=temporal_source_refs + KUI_YUE_SOURCE_REFS,
            fact_hash="",
            computation_hash="",
        )
        fact_hash, computation_hash = temporal_auxiliary_candidate_set_hashes(provisional)
        return replace(
            provisional,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
        )

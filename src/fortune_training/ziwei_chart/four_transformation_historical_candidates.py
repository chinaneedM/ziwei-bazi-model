from __future__ import annotations

from fortune_training.util import object_sha256


FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_ID = (
    "ZIWEI-FOUR-TRANSFORMATION-HISTORICAL-CANDIDATES-R1"
)
FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_VERSION = "1.0.0"
FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_ID = (
    "ZIWEI-FOUR-TRANSFORMATION-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1"
)
FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_VERSION = "1.0.0"
FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS = "PRESERVED_NOT_SELECTED"
FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_ID = (
    "ZIWEI-FOUR-TRANSFORMATION-HISTORICAL-CANDIDATE-API-R1"
)
FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_VERSION = "1.0.0"
FOUR_TRANSFORMATION_TYPES = ("化禄", "化权", "化科", "化忌")

FULLBOOK_SHIDIAN_CANDIDATE_ID = (
    "RECEIVED-FULLBOOK-SHIDIAN-V3-FOUR-TRANSFORMATION-R1"
)
ZHONGZHOU_WANGTINGZHI_CANDIDATE_ID = (
    "ZHONGZHOU-WANGTINGZHI-FOUR-TRANSFORMATION-R1"
)
FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS = (
    FULLBOOK_SHIDIAN_CANDIDATE_ID,
    ZHONGZHOU_WANGTINGZHI_CANDIDATE_ID,
)

FULLBOOK_SHIDIAN_TABLE = {
    "甲": ("廉贞", "破军", "武曲", "太阳"),
    "乙": ("天机", "天梁", "紫微", "太阴"),
    "丙": ("天同", "天机", "文昌", "廉贞"),
    "丁": ("太阴", "天同", "天机", "巨门"),
    "戊": ("贪狼", "太阴", "右弼", "天机"),
    "己": ("武曲", "贪狼", "天梁", "文曲"),
    "庚": ("太阳", "武曲", "天同", "天相"),
    "辛": ("巨门", "太阳", "文曲", "文昌"),
    "壬": ("天梁", "紫微", "天府", "武曲"),
    "癸": ("破军", "巨门", "太阴", "贪狼"),
}

ZHONGZHOU_WANGTINGZHI_TABLE = {
    "甲": ("廉贞", "破军", "武曲", "太阳"),
    "乙": ("天机", "天梁", "紫微", "太阴"),
    "丙": ("天同", "天机", "文昌", "廉贞"),
    "丁": ("太阴", "天同", "天机", "巨门"),
    "戊": ("贪狼", "太阴", "太阳", "天机"),
    "己": ("武曲", "贪狼", "天梁", "文曲"),
    "庚": ("太阳", "武曲", "天府", "天同"),
    "辛": ("巨门", "太阳", "文曲", "文昌"),
    "壬": ("天梁", "紫微", "天府", "武曲"),
    "癸": ("破军", "巨门", "太阴", "贪狼"),
}

_CANDIDATES = {
    FULLBOOK_SHIDIAN_CANDIDATE_ID: {
        "source_family": "RECEIVED_FULLBOOK_SHIDIAN_DIGITAL_TRANSCRIPTION",
        "source_refs": (
            "EXT-SHIDIAN-ZWDSQS-FOUR-TRANSFORMATIONS",
        ),
        "table": FULLBOOK_SHIDIAN_TABLE,
    },
    ZHONGZHOU_WANGTINGZHI_CANDIDATE_ID: {
        "source_family": "MODERN_ZHONGZHOU_WANGTINGZHI",
        "source_refs": (
            "EXT-WANGTINGZHI-ZHONGZHOU-CHUJI",
            "EXT-XINGQIAO-WANGTINGZHI-ZHONGZHOU-CHUJI",
            "S01:ZZZA-A-0391",
            "S01:ZZZA-A-0392",
            "S01:ZZZA-A-0393",
            "S01:ZZZA-A-0394",
            "S01:ZZZA-A-0395",
        ),
        "table": ZHONGZHOU_WANGTINGZHI_TABLE,
    },
}


def historical_four_transformation_candidate_payload() -> dict[str, object]:
    return {
        "registry_id": FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_ID,
        "registry_version": FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_VERSION,
        "selection_status": FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS,
        "candidate_ids": tuple(_CANDIDATES),
        "candidates": {
            candidate_id: {
                "source_family": data["source_family"],
                "source_refs": data["source_refs"],
                "table": data["table"],
            }
            for candidate_id, data in _CANDIDATES.items()
        },
        "whole_table_only": True,
        "cell_level_hybridization_allowed": False,
    }


def historical_four_transformation_candidate_registry_hash() -> str:
    return object_sha256(historical_four_transformation_candidate_payload())


def resolve_historical_four_transformation_candidate(
    *,
    candidate_id: str,
    source_stem: str,
) -> dict[str, object]:
    try:
        candidate = _CANDIDATES[candidate_id]
    except KeyError as exc:
        raise ValueError(f"unsupported Four-Transformation historical candidate: {candidate_id}") from exc
    try:
        targets = candidate["table"][source_stem]
    except KeyError as exc:
        raise ValueError(f"unsupported Four-Transformation source stem: {source_stem}") from exc

    payload: dict[str, object] = {
        "schema": FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_ID,
        "runtime_resolver_id": FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_ID,
        "runtime_resolver_version": FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_VERSION,
        "registry_id": FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_ID,
        "registry_version": FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_VERSION,
        "registry_hash": historical_four_transformation_candidate_registry_hash(),
        "candidate_id": candidate_id,
        "selection_status": FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS,
        "whole_table_only": True,
        "source_family": candidate["source_family"],
        "source_refs": candidate["source_refs"],
        "source_stem": source_stem,
        "assignments": tuple(
            {
                "transformation_type": transformation_type,
                "target_display_name": target_display_name,
            }
            for transformation_type, target_display_name in zip(
                FOUR_TRANSFORMATION_TYPES, targets, strict=True
            )
        ),
    }
    payload["runtime_hash"] = object_sha256(payload)
    return payload

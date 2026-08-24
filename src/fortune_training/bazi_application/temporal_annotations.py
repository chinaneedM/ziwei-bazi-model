from __future__ import annotations

from typing import Any, Mapping, Sequence

from fortune_training.bazi_chart.registries import (
    HIDDEN_STEMS,
    HIDDEN_STEM_RULE_SET_ID,
    HIDDEN_STEM_RULE_SET_VERSION,
    SEXAGENARY_INDEX,
    STEM_ELEMENTS,
    TEN_GOD_RULE_SET_ID,
    TEN_GOD_RULE_SET_VERSION,
    validate_branch,
    validate_stem,
)
from fortune_training.bazi_chart.ten_gods import (
    TEN_GOD_ALGORITHM_ID,
    TEN_GOD_ALGORITHM_VERSION,
    ten_god,
)
from fortune_training.bazi_nayin_annotation.registry import (
    NAYIN_ALGORITHM_ID,
    NAYIN_ALGORITHM_VERSION,
    NAYIN_ANNOTATION_PROFILE_ID,
    NAYIN_ANNOTATION_PROFILE_VERSION,
    NAYIN_REGISTRY_ID,
    NAYIN_REGISTRY_VERSION,
    entry_for_ganzhi,
)
from fortune_training.util import object_sha256

from .classical_annotations import (
    TWELVE_GROWTH_PROFILE_ID,
    TWELVE_GROWTH_PROFILE_VERSION,
    XUNKONG_PROFILE_ID,
    XUNKONG_PROFILE_VERSION,
    twelve_growth_for,
    xunkong_for_ganzhi,
)


TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_ID = (
    "BAZI-TEMPORAL-CLASSICAL-ANNOTATION-PROJECTION-R1"
)
TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION = "1.0.0"
TEMPORAL_CLASSICAL_ANNOTATION_ALGORITHM_ID = (
    "BAZI-TEMPORAL-CLASSICAL-ANNOTATION-COMPOSER-R1"
)
TEMPORAL_CLASSICAL_ANNOTATION_ALGORITHM_VERSION = "1.0.0"
TEMPORAL_CLASSICAL_ANNOTATION_HASH_ID = (
    "BAZI-TEMPORAL-CLASSICAL-ANNOTATION-HASH-R1"
)
TEMPORAL_CLASSICAL_ANNOTATION_HASH_VERSION = "1.0.0"
TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS = (
    "S11:YHZP-CH-061",
    "S11:YHZP-CH-016",
    "S11:YHZP-CH-017",
    "S11:YHZP-CH-057",
    "S11:YHZP-CH-065",
    "S01:ZZZA-PR-010",
    "S01:ZZZA-PR-011",
    "S14:YHZP-CH-047",
    "S14:7.7",
    "S12:YHZP-CH-016",
    "S12:ZPZQ-CH-05",
    "S12:ZPZQ-R-0006",
)


def _fact_projection(annotation: Mapping[str, Any]) -> dict[str, Any]:
    def strip_lineage(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {
                key: strip_lineage(item)
                for key, item in value.items()
                if key not in {"source_refs", "fact_hash", "computation_hash"}
            }
        if isinstance(value, list):
            return [strip_lineage(item) for item in value]
        return value

    return strip_lineage(annotation)


def temporal_classical_annotation_hashes(
    annotation: Mapping[str, Any],
) -> tuple[str, str]:
    fact_hash = object_sha256(_fact_projection(annotation))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_refs": annotation["source_refs"],
            "algorithm": (
                f"{TEMPORAL_CLASSICAL_ANNOTATION_HASH_ID}@"
                f"{TEMPORAL_CLASSICAL_ANNOTATION_HASH_VERSION}"
            ),
        }
    )
    return fact_hash, computation_hash


def temporal_classical_projection_hashes(
    projection: Mapping[str, Any],
) -> tuple[str, str]:
    def slot_fact(slot: Mapping[str, Any]) -> dict[str, Any]:
        annotation = slot.get("annotation")
        return {
            "status": slot.get("status"),
            "annotation_fact_hash": (
                annotation.get("fact_hash") if isinstance(annotation, Mapping) else None
            ),
        }

    def slot_computation(slot: Mapping[str, Any]) -> str | None:
        annotation = slot.get("annotation")
        return (
            annotation.get("computation_hash")
            if isinstance(annotation, Mapping)
            else None
        )

    xiaoyun = projection["xiaoyun_candidates"]
    fact_hash = object_sha256(
        {
            "profile_id": projection["profile_id"],
            "profile_version": projection["profile_version"],
            "day_master_stem": projection["day_master_stem"],
            "dayun": slot_fact(projection["dayun"]),
            "xiaoyun_candidates": [
                {
                    "profile_id": row["profile_id"],
                    "direction": row["direction"],
                    **slot_fact(row),
                }
                for row in xiaoyun
            ],
            "annual": slot_fact(projection["annual"]),
            "monthly": slot_fact(projection["monthly"]),
            "daily": slot_fact(projection["daily"]),
            "hourly": slot_fact(projection["hourly"]),
            "selection_semantics": projection["selection_semantics"],
            "semantic_scope": projection["semantic_scope"],
        }
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "dayun": slot_computation(projection["dayun"]),
            "xiaoyun_candidates": [slot_computation(row) for row in xiaoyun],
            "annual": slot_computation(projection["annual"]),
            "monthly": slot_computation(projection["monthly"]),
            "daily": slot_computation(projection["daily"]),
            "hourly": slot_computation(projection["hourly"]),
            "source_refs": projection["source_refs"],
            "algorithm": (
                f"{TEMPORAL_CLASSICAL_ANNOTATION_HASH_ID}@"
                f"{TEMPORAL_CLASSICAL_ANNOTATION_HASH_VERSION}"
            ),
        }
    )
    return fact_hash, computation_hash


def temporal_classical_annotation(
    ganzhi: str,
    day_master_stem: str,
    *,
    source_layer: str,
    context_id: str,
) -> dict[str, Any]:
    if ganzhi not in SEXAGENARY_INDEX:
        raise ValueError(f"invalid temporal Ganzhi: {ganzhi!r}")
    day_master_stem = validate_stem(day_master_stem)
    stem = validate_stem(ganzhi[0])
    branch = validate_branch(ganzhi[1])
    visible_semantic_id, visible_display_name = ten_god(day_master_stem, stem)
    hidden_stems = []
    for ordinal, hidden_stem in enumerate(HIDDEN_STEMS[branch]):
        semantic_id, display_name = ten_god(day_master_stem, hidden_stem)
        hidden_stems.append(
            {
                "stem": hidden_stem,
                "element": STEM_ELEMENTS[hidden_stem],
                "registry_ordinal": ordinal,
                "ten_god_semantic_role_id": semantic_id,
                "ten_god": display_name,
            }
        )
    nayin = entry_for_ganzhi(ganzhi)
    provisional = {
        "profile_id": TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_ID,
        "profile_version": TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION,
        "source_layer": source_layer,
        "context_id": context_id,
        "day_master_stem": day_master_stem,
        "ganzhi": ganzhi,
        "sexagenary_index": SEXAGENARY_INDEX[ganzhi],
        "stem": stem,
        "branch": branch,
        "visible_ten_god": {
            "semantic_role_id": visible_semantic_id,
            "display_name": visible_display_name,
        },
        "hidden_stems": hidden_stems,
        "nayin": {
            "profile_id": NAYIN_ANNOTATION_PROFILE_ID,
            "profile_version": NAYIN_ANNOTATION_PROFILE_VERSION,
            "registry_id": NAYIN_REGISTRY_ID,
            "registry_version": NAYIN_REGISTRY_VERSION,
            "semantic_id": nayin.semantic_id,
            "display_name": nayin.display_name,
            "element": nayin.element,
        },
        "xunkong": xunkong_for_ganzhi(ganzhi),
        "day_master_twelve_growth": twelve_growth_for(day_master_stem, branch),
        "self_twelve_growth": twelve_growth_for(stem, branch),
        "rule_bindings": {
            "hidden_stem_rule_set_id": HIDDEN_STEM_RULE_SET_ID,
            "hidden_stem_rule_set_version": HIDDEN_STEM_RULE_SET_VERSION,
            "ten_god_rule_set_id": TEN_GOD_RULE_SET_ID,
            "ten_god_rule_set_version": TEN_GOD_RULE_SET_VERSION,
            "ten_god_algorithm_id": TEN_GOD_ALGORITHM_ID,
            "ten_god_algorithm_version": TEN_GOD_ALGORITHM_VERSION,
            "nayin_algorithm_id": NAYIN_ALGORITHM_ID,
            "nayin_algorithm_version": NAYIN_ALGORITHM_VERSION,
            "xunkong_profile_id": XUNKONG_PROFILE_ID,
            "xunkong_profile_version": XUNKONG_PROFILE_VERSION,
            "twelve_growth_profile_id": TWELVE_GROWTH_PROFILE_ID,
            "twelve_growth_profile_version": TWELVE_GROWTH_PROFILE_VERSION,
        },
        "semantic_scope": (
            "IDENTITY_ANNOTATIONS_ONLY_NO_STRENGTH_PATTERN_OR_INTERPRETATION"
        ),
        "source_refs": list(TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS),
        "fact_hash": "",
        "computation_hash": "",
    }
    fact_hash, computation_hash = temporal_classical_annotation_hashes(provisional)
    return {
        **provisional,
        "fact_hash": fact_hash,
        "computation_hash": computation_hash,
    }


def _slot(
    source_layer: str,
    frame: Mapping[str, Any] | None,
    day_master_stem: str,
    *,
    unresolved_status: str,
) -> dict[str, Any]:
    if frame is None or not frame.get("ganzhi"):
        return {"status": unresolved_status, "annotation": None}
    return {
        "status": "RESOLVED",
        "annotation": temporal_classical_annotation(
            str(frame["ganzhi"]),
            day_master_stem,
            source_layer=source_layer,
            context_id=str(frame.get("frame_id") or f"{source_layer}:{frame['ganzhi']}"),
        ),
    }


def temporal_classical_annotation_projection(
    day_master_stem: str,
    *,
    dayun_kind: str,
    dayun_frame: Mapping[str, Any],
    xiaoyun_candidates: Sequence[Mapping[str, Any]],
    annual_frame: Mapping[str, Any],
    monthly_frame: Mapping[str, Any],
    daily_frame: Mapping[str, Any],
    hourly_frame: Mapping[str, Any],
) -> dict[str, Any]:
    day_master_stem = validate_stem(day_master_stem)
    xiaoyun_rows = []
    for candidate in xiaoyun_candidates:
        active_frame = candidate.get("active_frame")
        slot = _slot(
            "XIAOYUN",
            active_frame,
            day_master_stem,
            unresolved_status=str(candidate.get("activation_status", "UNRESOLVED")),
        )
        xiaoyun_rows.append(
            {
                "profile_id": candidate["profile_id"],
                "direction": candidate["direction"],
                **slot,
            }
        )
    dayun = _slot(
        "DAYUN",
        dayun_frame if dayun_kind == "DAYUN" else None,
        day_master_stem,
        unresolved_status="PRE_DAYUN_NO_GANZHI_ANNOTATION",
    )
    provisional = {
        "profile_id": TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_ID,
        "profile_version": TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION,
        "day_master_stem": day_master_stem,
        "dayun": dayun,
        "xiaoyun_candidates": xiaoyun_rows,
        "annual": _slot(
            "ANNUAL", annual_frame, day_master_stem, unresolved_status="UNRESOLVED"
        ),
        "monthly": _slot(
            "MONTHLY", monthly_frame, day_master_stem, unresolved_status="UNRESOLVED"
        ),
        "daily": _slot(
            "DAILY", daily_frame, day_master_stem, unresolved_status="UNRESOLVED"
        ),
        "hourly": _slot(
            "HOURLY", hourly_frame, day_master_stem, unresolved_status="UNRESOLVED"
        ),
        "selection_semantics": "XIAOYUN_CANDIDATES_PRESERVED_NO_WINNER",
        "semantic_scope": (
            "IDENTITY_ANNOTATIONS_ONLY_NO_STRENGTH_PATTERN_OR_INTERPRETATION"
        ),
        "source_refs": list(TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS),
        "fact_hash": "",
        "computation_hash": "",
    }
    fact_hash, computation_hash = temporal_classical_projection_hashes(provisional)
    return {
        **provisional,
        "fact_hash": fact_hash,
        "computation_hash": computation_hash,
    }


def validate_temporal_classical_annotation_projection(
    projection: Mapping[str, Any],
    *,
    dayun_kind: str,
    dayun_frame: Mapping[str, Any],
    xiaoyun_candidates: Sequence[Mapping[str, Any]],
    annual_frame: Mapping[str, Any],
    monthly_frame: Mapping[str, Any],
    daily_frame: Mapping[str, Any],
    hourly_frame: Mapping[str, Any],
) -> bool:
    try:
        expected = temporal_classical_annotation_projection(
            str(projection["day_master_stem"]),
            dayun_kind=dayun_kind,
            dayun_frame=dayun_frame,
            xiaoyun_candidates=xiaoyun_candidates,
            annual_frame=annual_frame,
            monthly_frame=monthly_frame,
            daily_frame=daily_frame,
            hourly_frame=hourly_frame,
        )
    except (KeyError, TypeError, ValueError):
        return False
    return projection == expected

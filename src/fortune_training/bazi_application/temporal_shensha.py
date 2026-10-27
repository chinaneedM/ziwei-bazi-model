from __future__ import annotations

from typing import Any, Mapping, Sequence

from fortune_training.bazi_chart.registries import SEXAGENARY_INDEX
from fortune_training.util import object_sha256


TEMPORAL_SHENSHA_PROFILE_ID = "BAZI-TEMPORAL-SHENSHA-TARGET-PROJECTION-R1"
TEMPORAL_SHENSHA_PROFILE_VERSION = "1.0.0"
TEMPORAL_SHENSHA_ALGORITHM_ID = "BAZI-TEMPORAL-SHENSHA-TARGET-MATCH-R1"
TEMPORAL_SHENSHA_ALGORITHM_VERSION = "1.0.0"
TEMPORAL_SHENSHA_HASH_ID = "BAZI-TEMPORAL-SHENSHA-PROJECTION-HASH-R1"
TEMPORAL_SHENSHA_HASH_VERSION = "1.0.0"
TEMPORAL_LAYERS = ("DAYUN", "XIAOYUN", "ANNUAL", "MONTHLY", "DAILY", "HOURLY")
SIMPLE_TARGET_KINDS = frozenset({"STEM", "BRANCH", "GANZHI"})


def _fact_projection(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            key: _fact_projection(item)
            for key, item in value.items()
            if key not in {"source_refs", "fact_hash", "computation_hash"}
        }
    if isinstance(value, list):
        return [_fact_projection(item) for item in value]
    return value


def temporal_shensha_projection_hashes(
    projection: Mapping[str, Any],
) -> tuple[str, str]:
    fact_hash = object_sha256(_fact_projection(projection))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_refs": projection["source_refs"],
            "algorithm": (
                f"{TEMPORAL_SHENSHA_HASH_ID}@{TEMPORAL_SHENSHA_HASH_VERSION}"
            ),
        }
    )
    return fact_hash, computation_hash


def _layer_policy(candidate: Mapping[str, Any]) -> tuple[tuple[str, ...], str | None]:
    target_kind = str(candidate.get("target_kind", ""))
    match_scope = str(candidate.get("match_scope", ""))
    if target_kind not in SIMPLE_TARGET_KINDS:
        return (), f"STRUCTURAL_TARGET_KIND:{target_kind or 'MISSING'}"
    if match_scope == "ALL_PILLARS":
        return TEMPORAL_LAYERS, None
    if match_scope == "ONLY_DAY":
        return ("DAILY",), None
    return (), f"SOURCE_MATCH_SCOPE_NOT_SINGLE_TARGET_PROJECTABLE:{match_scope or 'MISSING'}"


def _source_candidate_identity(candidate: Mapping[str, Any]) -> dict[str, Any]:
    required = (
        "candidate_id",
        "shensha_id",
        "display_name",
        "anchor_basis",
        "anchor_value",
        "target_kind",
        "target_values",
        "match_scope",
        "selection_status",
        "qualification_status",
        "source_refs",
    )
    missing = [key for key in required if key not in candidate]
    if missing:
        raise ValueError(f"ShenSha source candidate missing fields: {','.join(missing)}")
    if not isinstance(candidate["target_values"], list):
        raise ValueError("ShenSha source candidate target_values must be a list")
    if not isinstance(candidate["source_refs"], list) or not candidate["source_refs"]:
        raise ValueError("ShenSha source candidate must retain source_refs")
    return {
        "candidate_id": str(candidate["candidate_id"]),
        "shensha_id": str(candidate["shensha_id"]),
        "display_name": str(candidate["display_name"]),
        "anchor_basis": str(candidate["anchor_basis"]),
        "anchor_value": str(candidate["anchor_value"]),
        "target_kind": str(candidate["target_kind"]),
        "target_values": [str(item) for item in candidate["target_values"]],
        "match_scope": str(candidate["match_scope"]),
        "selection_status": str(candidate["selection_status"]),
        "qualification_status": str(candidate["qualification_status"]),
        "source_refs": [str(item) for item in candidate["source_refs"]],
    }


def _catalog(source_shensha: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    candidates = source_shensha.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("source ShenSha projection must contain candidates")
    identities = [_source_candidate_identity(row) for row in candidates]
    ids = [row["candidate_id"] for row in identities]
    if len(ids) != len(set(ids)):
        raise ValueError("source ShenSha candidate ids must be unique")

    eligible: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for row in identities:
        allowed_layers, reason = _layer_policy(row)
        if reason is None:
            eligible.append(
                {
                    "candidate_id": row["candidate_id"],
                    "shensha_id": row["shensha_id"],
                    "allowed_layers": list(allowed_layers),
                    "source_match_scope": row["match_scope"],
                    "target_kind": row["target_kind"],
                }
            )
        else:
            excluded.append(
                {
                    "candidate_id": row["candidate_id"],
                    "shensha_id": row["shensha_id"],
                    "reason": reason,
                    "target_kind": row["target_kind"],
                    "source_match_scope": row["match_scope"],
                }
            )
    return identities, eligible, excluded


def _target_value(ganzhi: str, target_kind: str) -> str:
    if ganzhi not in SEXAGENARY_INDEX:
        raise ValueError(f"invalid temporal Ganzhi: {ganzhi!r}")
    if target_kind == "STEM":
        return ganzhi[0]
    if target_kind == "BRANCH":
        return ganzhi[1]
    if target_kind == "GANZHI":
        return ganzhi
    raise ValueError(f"unsupported temporal ShenSha target kind: {target_kind}")


def _slot(
    source_layer: str,
    frame: Mapping[str, Any] | None,
    identities: Sequence[Mapping[str, Any]],
    *,
    unresolved_status: str,
) -> dict[str, Any]:
    if source_layer not in TEMPORAL_LAYERS:
        raise ValueError(f"unsupported temporal ShenSha layer: {source_layer}")
    if frame is None or not frame.get("ganzhi"):
        return {
            "status": unresolved_status,
            "frame_id": None,
            "ganzhi": None,
            "evaluated_candidate_count": 0,
            "matches": [],
        }

    ganzhi = str(frame["ganzhi"])
    if ganzhi not in SEXAGENARY_INDEX:
        raise ValueError(f"invalid temporal Ganzhi: {ganzhi!r}")
    matches: list[dict[str, Any]] = []
    evaluated = 0
    for candidate in identities:
        allowed_layers, reason = _layer_policy(candidate)
        if reason is not None or source_layer not in allowed_layers:
            continue
        evaluated += 1
        matched_value = _target_value(ganzhi, str(candidate["target_kind"]))
        if matched_value not in candidate["target_values"]:
            continue
        matches.append(
            {
                "source_candidate_id": candidate["candidate_id"],
                "shensha_id": candidate["shensha_id"],
                "display_name": candidate["display_name"],
                "anchor_basis": candidate["anchor_basis"],
                "anchor_value": candidate["anchor_value"],
                "target_kind": candidate["target_kind"],
                "target_values": list(candidate["target_values"]),
                "matched_value": matched_value,
                "source_match_scope": candidate["match_scope"],
                "source_selection_status": candidate["selection_status"],
                "source_qualification_status": candidate["qualification_status"],
                "temporal_applicability_status": "NOT_CLASSICALLY_ARBITRATED",
                "source_refs": list(candidate["source_refs"]),
            }
        )
    return {
        "status": "RESOLVED",
        "frame_id": str(frame.get("frame_id") or f"{source_layer}:{ganzhi}"),
        "ganzhi": ganzhi,
        "evaluated_candidate_count": evaluated,
        "matches": matches,
    }


def temporal_shensha_target_projection(
    source_shensha: Mapping[str, Any],
    *,
    dayun_kind: str,
    dayun_frame: Mapping[str, Any] | None,
    xiaoyun_candidates: Sequence[Mapping[str, Any]],
    annual_frame: Mapping[str, Any] | None,
    monthly_frame: Mapping[str, Any] | None,
    daily_frame: Mapping[str, Any] | None,
    hourly_frame: Mapping[str, Any] | None,
) -> dict[str, Any]:
    identities, eligible, excluded = _catalog(source_shensha)
    xiaoyun_rows = []
    for candidate in xiaoyun_candidates:
        active_frame = candidate.get("active_frame")
        slot = _slot(
            "XIAOYUN",
            active_frame if isinstance(active_frame, Mapping) else None,
            identities,
            unresolved_status=str(candidate.get("activation_status", "UNRESOLVED")),
        )
        xiaoyun_rows.append(
            {
                "profile_id": str(candidate.get("profile_id", "")),
                "direction": str(candidate.get("direction", "")),
                **slot,
            }
        )

    source_refs = list(
        dict.fromkeys(
            ref
            for row in identities
            for ref in row["source_refs"]
        )
    )
    provisional = {
        "profile_id": TEMPORAL_SHENSHA_PROFILE_ID,
        "profile_version": TEMPORAL_SHENSHA_PROFILE_VERSION,
        "source_shensha_profile_id": str(source_shensha.get("profile_id", "")),
        "source_shensha_profile_version": str(source_shensha.get("profile_version", "")),
        "source_shensha_candidate_set_id": str(source_shensha.get("candidate_set_id", "")),
        "source_candidate_catalog_hash": object_sha256(_fact_projection(identities)),
        "eligible_source_candidates": eligible,
        "excluded_source_candidates": excluded,
        "dayun": _slot(
            "DAYUN",
            dayun_frame if dayun_kind == "DAYUN" else None,
            identities,
            unresolved_status="PRE_DAYUN_NO_GANZHI_PROJECTION",
        ),
        "xiaoyun_candidates": xiaoyun_rows,
        "annual": _slot("ANNUAL", annual_frame, identities, unresolved_status="UNRESOLVED"),
        "monthly": _slot("MONTHLY", monthly_frame, identities, unresolved_status="UNRESOLVED"),
        "daily": _slot("DAILY", daily_frame, identities, unresolved_status="UNRESOLVED"),
        "hourly": _slot("HOURLY", hourly_frame, identities, unresolved_status="UNRESOLVED"),
        "projection_policy": "ENGINEERING_TARGET_MATCH_NOT_CLASSICAL_TEMPORAL_APPLICABILITY",
        "selection_semantics": "SOURCE_CANDIDATES_PRESERVED_NO_WINNER",
        "semantic_scope": "TARGET_IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS_OR_TEMPORAL_RULE_ADJUDICATION",
        "source_refs": source_refs,
        "fact_hash": "",
        "computation_hash": "",
    }
    fact_hash, computation_hash = temporal_shensha_projection_hashes(provisional)
    return {
        **provisional,
        "fact_hash": fact_hash,
        "computation_hash": computation_hash,
    }


def validate_temporal_shensha_target_projection(
    projection: Mapping[str, Any],
    source_shensha: Mapping[str, Any],
    *,
    dayun_kind: str,
    dayun_frame: Mapping[str, Any] | None,
    xiaoyun_candidates: Sequence[Mapping[str, Any]],
    annual_frame: Mapping[str, Any] | None,
    monthly_frame: Mapping[str, Any] | None,
    daily_frame: Mapping[str, Any] | None,
    hourly_frame: Mapping[str, Any] | None,
) -> bool:
    try:
        expected = temporal_shensha_target_projection(
            source_shensha,
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

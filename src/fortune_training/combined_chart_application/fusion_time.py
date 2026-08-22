from __future__ import annotations

from typing import Any

from fortune_training.calendar_foundation.models import BirthInput, json_value
from fortune_training.util import object_sha256


SHARED_TIME_CREDENTIAL_SCHEMA = "ZIWEI-BAZI-SHARED-TIME-CREDENTIAL-V1"
SHARED_TIME_LINEAGE_SCHEMA = "ZIWEI-BAZI-SHARED-TIME-LINEAGE-V1"

def validate_shared_policy_contract(ziwei_profile: Any, bazi_profile: Any) -> None:
    """Unify physical time facts without collapsing system-specific conventions."""

    if (
        ziwei_profile.time_calendar_policy_registry_version
        != bazi_profile.time_calendar_policy_registry_version
    ):
        raise ValueError("shared time/calendar policy registry version mismatch")
    if (
        ziwei_profile.time_calendar_policies.civil_ambiguous_time_policy
        != bazi_profile.time_calendar_policies.civil_ambiguous_time_policy
    ):
        raise ValueError("shared civil ambiguous-time policy mismatch")


def _lunar_identity(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value[key]
        for key in (
            "year",
            "month",
            "day",
            "is_leap_month",
            "source_gregorian_date",
            "month_start_utc",
            "next_month_start_utc",
        )
    }


def _physical_identity(branch: dict[str, Any]) -> tuple[Any, ...]:
    selected = branch["selected_civil_candidate"]
    solar = branch["solar_time"]
    return (
        branch["sample_reported_local_datetime"],
        selected["utc_instant"],
        selected["fold"],
        solar["local_mean_solar_datetime"],
        solar["local_apparent_solar_datetime"],
    )


def _realization_payload(
    index: int,
    ziwei_branch: dict[str, Any],
    bazi_branch: dict[str, Any],
) -> dict[str, Any]:
    if _physical_identity(ziwei_branch) != _physical_identity(bazi_branch):
        raise ValueError(f"shared physical time branch mismatch at index {index}")
    civil = ziwei_branch["civil_time"]
    selected = ziwei_branch["selected_civil_candidate"]
    solar = ziwei_branch["solar_time"]
    ziwei = ziwei_branch["ziwei_calendar"]
    bazi = bazi_branch["bazi_time"]
    payload = {
        "source_time_branch_index": index,
        "sample_reported_local_datetime": ziwei_branch["sample_reported_local_datetime"],
        "civil_status": civil["status"],
        "timezone_id": civil["timezone_id"],
        "tzdb_version": civil["tzdb_version"],
        "timezone_history_grade": civil["historical_confidence"],
        "fold": selected["fold"],
        "birth_utc": selected["utc_instant"],
        "utc_offset_seconds": selected["utc_offset_seconds"],
        "daylight_saving_seconds": selected["daylight_saving_seconds"],
        "local_mean_solar_datetime": solar["local_mean_solar_datetime"],
        "local_apparent_solar_datetime": solar["local_apparent_solar_datetime"],
        "actual_civil_lunar_date": _lunar_identity(
            ziwei["actual_civil_lunar_date"]
        ),
        "local_solar_lunar_date": _lunar_identity(
            ziwei["local_solar_lunar_date"]
        ),
        "effective_ziwei_lunar_date": _lunar_identity(
            ziwei["effective_ziwei_lunar_date"]
        ),
        "bazi_pillars": [
            bazi["year_pillar"],
            bazi["month_pillar"],
            bazi["day_pillar"],
            bazi["hour_pillar"],
        ],
        "bazi_effective_day_date": bazi["effective_day_date"],
        "bazi_hour_stem_source_date": bazi["hour_stem_source_date"],
        "active_jie": {
            "name": bazi["active_month_boundary"]["name"],
            "utc_instant": bazi["active_month_boundary"]["utc_instant"],
        },
        "next_jie": {
            "name": bazi["next_month_boundary"]["name"],
            "utc_instant": bazi["next_month_boundary"]["utc_instant"],
        },
    }
    return {**payload, "realization_hash": object_sha256(payload)}


def build_shared_time_credential(
    birth: BirthInput,
    ziwei_time_result: dict[str, Any],
    bazi_time_result: dict[str, Any],
    *,
    ziwei_day_boundary_policy: str,
) -> dict[str, Any]:
    ziwei_branches = ziwei_time_result.get("branches", [])
    bazi_branches = bazi_time_result.get("branches", [])
    if len(ziwei_branches) != len(bazi_branches):
        raise ValueError("shared physical time branch count mismatch")
    realizations = [
        _realization_payload(index, ziwei_branch, bazi_branches[index])
        for index, ziwei_branch in enumerate(ziwei_branches)
    ]
    if ziwei_time_result.get("unresolved_samples", []) != bazi_time_result.get(
        "unresolved_samples", []
    ):
        raise ValueError("shared unresolved civil-time samples mismatch")
    unresolved_samples = [
        {
            "sample_reported_local_datetime": row["sample_reported_local_datetime"],
            "civil_status": row["civil_time"]["status"],
            "timezone_id": row["civil_time"]["timezone_id"],
            "tzdb_version": row["civil_time"]["tzdb_version"],
            "timezone_history_grade": row["civil_time"]["historical_confidence"],
        }
        for row in ziwei_time_result.get("unresolved_samples", [])
    ]
    selected_policies = {
        "shared_physical": {
            "civil_ambiguous_time_policy": ziwei_time_result["selected_policies"][
                "civil_ambiguous_time_policy"
            ],
            "time_coordinate_policy": "LOCAL_APPARENT_SOLAR",
        },
        "ziwei": {
            "calendar_date_policy": ziwei_time_result["selected_policies"][
                "ziwei_calendar_date_policy"
            ],
            "life_body_leap_month_policy": ziwei_time_result["selected_policies"][
                "ziwei_life_body_leap_month_policy"
            ],
            "day_boundary_policy": ziwei_day_boundary_policy,
        },
        "bazi": bazi_time_result["selected_policies"],
    }
    status = {
        "ziwei": ziwei_time_result["status"],
        "bazi": bazi_time_result["status"],
    }
    fact_payload = {
        "birth": json_value(birth),
        "status": status,
        "input_interval": ziwei_time_result["input_interval"],
        "realization_hashes": [row["realization_hash"] for row in realizations],
        "unresolved_samples": unresolved_samples,
    }
    fact_hash = object_sha256(fact_payload)
    computation_payload = {
        "schema": SHARED_TIME_CREDENTIAL_SCHEMA,
        "fact_hash": fact_hash,
        "policy_registry_version": ziwei_time_result["policy_registry_version"],
        "selected_policies": selected_policies,
        "realizations": realizations,
    }
    return {
        "schema": SHARED_TIME_CREDENTIAL_SCHEMA,
        "status": status,
        "policy_registry_version": ziwei_time_result["policy_registry_version"],
        "selected_policies": selected_policies,
        "input_interval": ziwei_time_result["input_interval"],
        "realizations": realizations,
        "unresolved_samples": unresolved_samples,
        "fact_hash": fact_hash,
        "computation_hash": object_sha256(computation_payload),
    }


def validate_shared_time_credential(
    birth: BirthInput,
    credential: dict[str, Any],
) -> tuple[str, ...]:
    diagnostics: list[str] = []
    if credential.get("schema") != SHARED_TIME_CREDENTIAL_SCHEMA:
        return ("SHARED_TIME_CREDENTIAL_SCHEMA_MISMATCH",)
    realizations = credential.get("realizations", [])
    for index, row in enumerate(realizations):
        payload = {key: value for key, value in row.items() if key != "realization_hash"}
        if row.get("source_time_branch_index") != index:
            diagnostics.append(f"SHARED_TIME_BRANCH_INDEX_MISMATCH:{index}")
        if row.get("realization_hash") != object_sha256(payload):
            diagnostics.append(f"SHARED_TIME_REALIZATION_HASH_MISMATCH:{index}")
    fact_payload = {
        "birth": json_value(birth),
        "status": credential.get("status"),
        "input_interval": credential.get("input_interval"),
        "realization_hashes": [row.get("realization_hash") for row in realizations],
        "unresolved_samples": credential.get("unresolved_samples", []),
    }
    fact_hash = object_sha256(fact_payload)
    if credential.get("fact_hash") != fact_hash:
        diagnostics.append("SHARED_TIME_FACT_HASH_MISMATCH")
    computation_payload = {
        "schema": SHARED_TIME_CREDENTIAL_SCHEMA,
        "fact_hash": fact_hash,
        "policy_registry_version": credential.get("policy_registry_version"),
        "selected_policies": credential.get("selected_policies"),
        "realizations": realizations,
    }
    if credential.get("computation_hash") != object_sha256(computation_payload):
        diagnostics.append("SHARED_TIME_COMPUTATION_HASH_MISMATCH")
    return tuple(diagnostics)


def build_candidate_lineage(
    credential: dict[str, Any],
    ziwei_bundle: Any | None,
    bazi_bundle: Any | None,
) -> dict[str, Any]:
    ziwei_indices = (
        set(ziwei_bundle.candidate.branch_indices) if ziwei_bundle is not None else set()
    )
    bazi_by_index: dict[int, list[str]] = {}
    if bazi_bundle is not None:
        for candidate in bazi_bundle.candidates:
            indices = {
                int(row["source_time_branch_index"])
                for row in candidate.view.get("time_provenance", [])
            }
            for index in indices:
                bazi_by_index.setdefault(index, []).append(candidate.candidate_id)

    rows = []
    for realization in credential["realizations"]:
        index = realization["source_time_branch_index"]
        ziwei_bound = index in ziwei_indices
        bazi_ids = sorted(set(bazi_by_index.get(index, [])))
        if ziwei_bound and bazi_ids:
            status = "LINKED_BOTH"
        elif ziwei_bound:
            status = "ZIWEI_ONLY"
        elif bazi_ids:
            status = "BAZI_ONLY"
        else:
            status = "UNBOUND"
        rows.append(
            {
                "source_time_branch_index": index,
                "shared_time_realization_hash": realization["realization_hash"],
                "ziwei_natal_fact_hash": (
                    ziwei_bundle.candidate.hashes.fact_hash if ziwei_bound else None
                ),
                "bazi_candidate_ids": bazi_ids,
                "status": status,
            }
        )
    payload = {
        "schema": SHARED_TIME_LINEAGE_SCHEMA,
        "shared_time_computation_hash": credential["computation_hash"],
        "branches": rows,
    }
    return {**payload, "lineage_hash": object_sha256(payload)}


def validate_candidate_lineage(
    credential: dict[str, Any],
    lineage: dict[str, Any],
    ziwei_bundle: Any | None,
    bazi_bundle: Any | None,
) -> tuple[str, ...]:
    expected = build_candidate_lineage(credential, ziwei_bundle, bazi_bundle)
    if lineage != expected:
        return ("SHARED_TIME_CANDIDATE_LINEAGE_MISMATCH",)
    return ()


def validate_subsystem_time_binding(
    credential: dict[str, Any],
    ziwei_bundle: Any | None,
    bazi_bundle: Any | None,
) -> tuple[str, ...]:
    diagnostics: list[str] = []
    realizations = {
        row["source_time_branch_index"]: row
        for row in credential.get("realizations", [])
    }
    if ziwei_bundle is not None:
        for index in ziwei_bundle.candidate.branch_indices:
            if index not in realizations:
                diagnostics.append(f"ZIWEI_SHARED_TIME_BRANCH_MISSING:{index}")
    if bazi_bundle is not None:
        for row in bazi_bundle.time_calendar_provenance.legal_realizations:
            shared = realizations.get(row.source_time_branch_index)
            if shared is None:
                diagnostics.append(
                    f"BAZI_SHARED_TIME_BRANCH_MISSING:{row.source_time_branch_index}"
                )
                continue
            if (
                row.sample_reported_local_datetime
                != shared["sample_reported_local_datetime"]
                or row.birth_utc != shared["birth_utc"]
                or row.fold != shared["fold"]
            ):
                diagnostics.append(
                    f"BAZI_SHARED_PHYSICAL_TIME_MISMATCH:{row.source_time_branch_index}"
                )
        for candidate_index, candidate in enumerate(bazi_bundle.candidates):
            for time_index, row in enumerate(candidate.view.get("time_provenance", [])):
                shared = realizations.get(row["source_time_branch_index"])
                if shared is None:
                    continue
                if row["local_apparent_solar_datetime"] != shared[
                    "local_apparent_solar_datetime"
                ]:
                    diagnostics.append(
                        "BAZI_SHARED_APPARENT_SOLAR_TIME_MISMATCH:"
                        f"{candidate_index}:{time_index}"
                    )
    return tuple(diagnostics)

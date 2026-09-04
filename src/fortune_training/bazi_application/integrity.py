from __future__ import annotations

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import BaziApplicationIntegrityReport, BaziApplicationResolution
from .shensha import classical_shensha_for_pillars


def validate_application_resolution(
    resolution: BaziApplicationResolution,
) -> BaziApplicationIntegrityReport:
    diagnostics: list[str] = []
    try:
        resolution.application_profile.validate()
    except ValueError as exc:
        diagnostics.append(f"APPLICATION_PROFILE_INVALID:{exc}")

    provenance = resolution.time_calendar_provenance
    if provenance.legal_realization_count != len(provenance.legal_realizations):
        diagnostics.append("TIME_CALENDAR_LEGAL_REALIZATION_COUNT_MISMATCH")
    if provenance.unresolved_sample_count != len(provenance.unresolved_samples):
        diagnostics.append("TIME_CALENDAR_UNRESOLVED_SAMPLE_COUNT_MISMATCH")

    legal_by_index = {
        row.source_time_branch_index: row for row in provenance.legal_realizations
    }
    if len(legal_by_index) != len(provenance.legal_realizations):
        diagnostics.append("TIME_CALENDAR_LEGAL_REALIZATION_INDEX_DUPLICATE")

    for index, candidate in enumerate(resolution.candidates):
        expected_view_hash = object_sha256(
            {
                "view_schema": candidate.view_schema,
                "view": candidate.view,
            }
        )
        if candidate.view_schema != resolution.application_profile.view_schema:
            diagnostics.append(f"CANDIDATE_VIEW_SCHEMA_MISMATCH:{index}")
        if candidate.view_hash != expected_view_hash:
            diagnostics.append(f"CANDIDATE_VIEW_HASH_MISMATCH:{index}")
        expected_candidate_id = "BAZI-APPLICATION-CANDIDATE:" + object_sha256(
            {
                "natal_fact_hash": candidate.natal_fact_hash,
                "natal_computation_hash": candidate.natal_computation_hash,
                "temporal_fact_hash": candidate.temporal_fact_hash,
                "temporal_computation_hash": candidate.temporal_computation_hash,
                "view_hash": candidate.view_hash,
            }
        )
        if candidate.candidate_id != expected_candidate_id:
            diagnostics.append(f"CANDIDATE_ID_MISMATCH:{index}")

        try:
            pillar_ganzhi = {
                row["position"]: row["ganzhi"]
                for row in candidate.view.get("pillars", [])
            }
            expected_shensha = classical_shensha_for_pillars(pillar_ganzhi)
            if candidate.view.get("shensha") != expected_shensha:
                diagnostics.append(f"SHENSHA_REPLAY_MISMATCH:{index}")
        except (KeyError, TypeError, ValueError):
            diagnostics.append(f"SHENSHA_REPLAY_INVALID:{index}")

        for time_index, time_row in enumerate(candidate.view.get("time_provenance", [])):
            branch_index = time_row.get("source_time_branch_index")
            legal = legal_by_index.get(branch_index)
            if legal is None:
                diagnostics.append(
                    f"TIME_CALENDAR_LEGAL_REALIZATION_LINEAGE_MISSING:{index}:{time_index}"
                )
                continue
            if (
                time_row.get("sample_reported_local_datetime")
                != legal.sample_reported_local_datetime
                or time_row.get("birth_utc") != legal.birth_utc
            ):
                diagnostics.append(
                    f"TIME_CALENDAR_LEGAL_REALIZATION_LINEAGE_MISMATCH:{index}:{time_index}"
                )

    expected_source_fact_hash = object_sha256(
        {
            "birth": json_value(resolution.birth),
            "sex": resolution.sex.value,
            "time_calendar_provenance": json_value(
                resolution.time_calendar_provenance
            ),
            "natal_fact_hashes": [row.natal_fact_hash for row in resolution.candidates],
            "temporal_fact_hashes": [row.temporal_fact_hash for row in resolution.candidates],
        }
    )
    if resolution.source_fact_hash != expected_source_fact_hash:
        diagnostics.append("SOURCE_FACT_HASH_MISMATCH")

    expected_view_hash = object_sha256(
        {
            "view_schema": resolution.application_profile.view_schema,
            "candidate_view_hashes": [row.view_hash for row in resolution.candidates],
        }
    )
    if resolution.view_hash != expected_view_hash:
        diagnostics.append("AGGREGATE_VIEW_HASH_MISMATCH")

    expected_bundle_hash = object_sha256(
        {
            "source_fact_hash": resolution.source_fact_hash,
            "view_hash": resolution.view_hash,
            "application_profile": json_value(resolution.application_profile),
            "natal_profile": json_value(resolution.natal_profile),
            "temporal_profile": json_value(resolution.temporal_profile),
            "dayun_count": resolution.dayun_count,
            "candidate_ids": [row.candidate_id for row in resolution.candidates],
        }
    )
    if resolution.bundle_hash != expected_bundle_hash:
        diagnostics.append("BUNDLE_HASH_MISMATCH")

    return BaziApplicationIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )

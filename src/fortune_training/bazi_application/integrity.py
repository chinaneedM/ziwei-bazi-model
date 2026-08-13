from __future__ import annotations

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import BaziApplicationIntegrityReport, BaziApplicationResolution


def validate_application_resolution(
    resolution: BaziApplicationResolution,
) -> BaziApplicationIntegrityReport:
    diagnostics: list[str] = []
    try:
        resolution.application_profile.validate()
    except ValueError as exc:
        diagnostics.append(f"APPLICATION_PROFILE_INVALID:{exc}")

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

    expected_source_fact_hash = object_sha256(
        {
            "birth": json_value(resolution.birth),
            "sex": resolution.sex.value,
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

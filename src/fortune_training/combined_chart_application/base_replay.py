from __future__ import annotations

from typing import Protocol

from .models import (
    CombinedApplicationIntegrityReport,
    CombinedChartApplicationRequest,
    CombinedChartApplicationResolution,
)
from .service import validate_combined_resolution


class _CombinedApplicationResolver(Protocol):
    def resolve(
        self,
        request: CombinedChartApplicationRequest,
    ) -> CombinedChartApplicationResolution: ...


def validate_combined_application_full_replay(
    service: _CombinedApplicationResolver,
    request: CombinedChartApplicationRequest,
    resolution: CombinedChartApplicationResolution,
) -> CombinedApplicationIntegrityReport:
    """Re-run the complete base combined composition and compare deterministic outputs.

    Structural integrity can validate hashes and embedded bundles, but a Ziwei
    multi-candidate application failure intentionally carries only minimal natal
    fact-hash lineage rather than full candidate charts. Full replay closes that
    verification gap by regenerating the complete resolution from the original
    request and comparing the resulting deterministic objects.
    """

    diagnostics: list[str] = []
    structural = validate_combined_resolution(resolution)
    if structural.status != "PASS":
        diagnostics.extend(
            f"STRUCTURAL_INTEGRITY_FAILED:{item}"
            for item in structural.diagnostics
        )

    try:
        replayed = service.resolve(request)
    except (ValueError, RuntimeError) as exc:
        diagnostics.append(f"FULL_REPLAY_RESOLUTION_FAILED:{exc}")
        return CombinedApplicationIntegrityReport(
            status="FAIL",
            diagnostics=tuple(diagnostics),
            algorithm_id=(
                "ZIWEI-BAZI-COMBINED-APPLICATION-FULL-REPLAY-INTEGRITY-R1"
            ),
            algorithm_version="1.0.0",
        )

    if replayed.shared_time_credential != resolution.shared_time_credential:
        diagnostics.append("SHARED_TIME_CREDENTIAL_FULL_REPLAY_MISMATCH")
    if replayed.candidate_lineage != resolution.candidate_lineage:
        diagnostics.append("CANDIDATE_LINEAGE_FULL_REPLAY_MISMATCH")
    if (
        replayed.ziwei_bundle != resolution.ziwei_bundle
        or replayed.ziwei_error != resolution.ziwei_error
    ):
        diagnostics.append("ZIWEI_SUBSYSTEM_FULL_REPLAY_MISMATCH")
    if (
        replayed.bazi_bundle != resolution.bazi_bundle
        or replayed.bazi_error != resolution.bazi_error
    ):
        diagnostics.append("BAZI_SUBSYSTEM_FULL_REPLAY_MISMATCH")
    if replayed.manifest_hash != resolution.manifest_hash:
        diagnostics.append("COMBINED_MANIFEST_FULL_REPLAY_MISMATCH")
    if replayed != resolution:
        diagnostics.append("COMBINED_APPLICATION_FULL_REPLAY_MISMATCH")

    return CombinedApplicationIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id="ZIWEI-BAZI-COMBINED-APPLICATION-FULL-REPLAY-INTEGRITY-R1",
        algorithm_version="1.0.0",
    )

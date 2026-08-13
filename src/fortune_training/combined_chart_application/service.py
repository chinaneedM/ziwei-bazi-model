from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from fortune_training.bazi_application import (
    BaziApplicationRequest,
    BaziApplicationResolutionError,
    BaziChartService,
    validate_application_resolution as validate_bazi_application_resolution,
)
from fortune_training.bazi_temporal import BaziSex
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    ApplicationResolutionError,
    ZiweiChartService,
    application_export,
    validate_application_bundle,
)
from fortune_training.ziwei_chart import Sex, ZiweiChartFoundation

from .models import (
    CombinedApplicationIntegrityReport,
    CombinedChartApplicationRequest,
    CombinedChartApplicationResolution,
    CombinedSubsystemError,
)


COMBINED_RESOLUTION_SCHEMA = "ZIWEI-BAZI-COMBINED-APPLICATION-RESOLUTION-V1"
COMBINED_EXPORT_SCHEMA = "ZIWEI-BAZI-COMBINED-APPLICATION-EXPORT-V1"


class CombinedApplicationResolutionError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def _error_payload(error: CombinedSubsystemError | None) -> dict[str, str] | None:
    if error is None:
        return None
    return {"code": error.code, "detail": error.detail}


def _profile_ref(profile: Any) -> dict[str, str]:
    return {
        "profile_id": str(profile.profile_id),
        "profile_version": str(profile.profile_version),
    }


def combined_manifest_payload(
    resolution: CombinedChartApplicationResolution,
) -> dict[str, Any]:
    return {
        "manifest_schema": resolution.combined_profile.manifest_schema,
        "birth": json_value(resolution.birth),
        "sex": resolution.sex,
        "combined_profile": {
            **_profile_ref(resolution.combined_profile),
            "algorithm_id": resolution.combined_profile.algorithm_id,
            "algorithm_version": resolution.combined_profile.algorithm_version,
            "composition_semantics": resolution.combined_profile.composition_semantics,
        },
        "profiles": {
            "ziwei_calculation": _profile_ref(resolution.ziwei_calculation_profile),
            "ziwei_application": _profile_ref(resolution.ziwei_application_profile),
            "ziwei_presentation": _profile_ref(resolution.ziwei_presentation_profile),
            "bazi_natal": _profile_ref(resolution.bazi_natal_profile),
            "bazi_temporal": _profile_ref(resolution.bazi_temporal_profile),
            "bazi_application": _profile_ref(resolution.bazi_application_profile),
        },
        "subsystems": {
            "ziwei": {
                "bundle_hash": (
                    resolution.ziwei_bundle.bundle_hash
                    if resolution.ziwei_bundle is not None
                    else None
                ),
                "error": _error_payload(resolution.ziwei_error),
            },
            "bazi": {
                "bundle_hash": (
                    resolution.bazi_bundle.bundle_hash
                    if resolution.bazi_bundle is not None
                    else None
                ),
                "error": _error_payload(resolution.bazi_error),
            },
        },
        "composition_status": resolution.status,
    }


def combined_manifest_hash(
    resolution: CombinedChartApplicationResolution,
) -> str:
    return object_sha256(combined_manifest_payload(resolution))


def validate_combined_resolution(
    resolution: CombinedChartApplicationResolution,
) -> CombinedApplicationIntegrityReport:
    diagnostics: list[str] = []
    try:
        resolution.combined_profile.validate()
        resolution.ziwei_application_profile.validate()
        resolution.ziwei_presentation_profile.validate()
        resolution.bazi_application_profile.validate()
    except ValueError as exc:
        diagnostics.append(f"PROFILE_INVALID:{exc}")

    if resolution.sex not in {"MALE", "FEMALE"}:
        diagnostics.append("SHARED_SEX_INVALID")

    if resolution.ziwei_bundle is not None:
        try:
            validate_application_bundle(resolution.ziwei_bundle)
        except (ApplicationResolutionError, ValueError) as exc:
            diagnostics.append(f"ZIWEI_BUNDLE_REPLAY_FAILED:{exc}")
        if resolution.ziwei_error is not None:
            diagnostics.append("ZIWEI_BUNDLE_AND_ERROR_BOTH_PRESENT")
        if resolution.ziwei_bundle.calculation_profile != resolution.ziwei_calculation_profile:
            diagnostics.append("ZIWEI_CALCULATION_PROFILE_BINDING_MISMATCH")
        if resolution.ziwei_bundle.application_profile != resolution.ziwei_application_profile:
            diagnostics.append("ZIWEI_APPLICATION_PROFILE_BINDING_MISMATCH")
        if resolution.ziwei_bundle.presentation_profile != resolution.ziwei_presentation_profile:
            diagnostics.append("ZIWEI_PRESENTATION_PROFILE_BINDING_MISMATCH")
    elif resolution.ziwei_error is None:
        diagnostics.append("ZIWEI_RESULT_MISSING")

    if resolution.bazi_bundle is not None:
        report = validate_bazi_application_resolution(resolution.bazi_bundle)
        if report.status != "PASS":
            diagnostics.append(
                "BAZI_BUNDLE_REPLAY_FAILED:" + ";".join(report.diagnostics)
            )
        if resolution.bazi_error is not None:
            diagnostics.append("BAZI_BUNDLE_AND_ERROR_BOTH_PRESENT")
        if resolution.bazi_bundle.natal_profile != resolution.bazi_natal_profile:
            diagnostics.append("BAZI_NATAL_PROFILE_BINDING_MISMATCH")
        if resolution.bazi_bundle.temporal_profile != resolution.bazi_temporal_profile:
            diagnostics.append("BAZI_TEMPORAL_PROFILE_BINDING_MISMATCH")
        if resolution.bazi_bundle.application_profile != resolution.bazi_application_profile:
            diagnostics.append("BAZI_APPLICATION_PROFILE_BINDING_MISMATCH")
        if resolution.bazi_bundle.birth != resolution.birth:
            diagnostics.append("BAZI_SHARED_BIRTH_BINDING_MISMATCH")
        if resolution.bazi_bundle.sex.value != resolution.sex:
            diagnostics.append("BAZI_SHARED_SEX_BINDING_MISMATCH")
    elif resolution.bazi_error is None:
        diagnostics.append("BAZI_RESULT_MISSING")

    present_count = int(resolution.ziwei_bundle is not None) + int(
        resolution.bazi_bundle is not None
    )
    if present_count == 0 and resolution.status != "FAILED":
        diagnostics.append("COMPOSITION_STATUS_MISMATCH")
    if present_count == 1 and resolution.status != "PARTIAL":
        diagnostics.append("COMPOSITION_STATUS_MISMATCH")
    if present_count == 2 and resolution.status not in {
        "RESOLVED_BOTH",
        "UNCERTAINTY_PRESENT",
    }:
        diagnostics.append("COMPOSITION_STATUS_MISMATCH")

    if resolution.manifest_hash != combined_manifest_hash(resolution):
        diagnostics.append("COMBINED_MANIFEST_HASH_MISMATCH")

    return CombinedApplicationIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )


class CombinedChartService:
    def __init__(
        self,
        ziwei_foundation: ZiweiChartFoundation,
        bazi_service: BaziChartService,
    ) -> None:
        self.ziwei_foundation = ziwei_foundation
        self.bazi_service = bazi_service

    @classmethod
    def from_repository(cls, repository_root: Path) -> "CombinedChartService":
        return cls(
            ZiweiChartFoundation.from_repository(repository_root),
            BaziChartService.from_repository(repository_root),
        )

    @staticmethod
    def _normalize_sex(value: str) -> str:
        normalized = value.strip().upper()
        aliases = {"男": "MALE", "女": "FEMALE", "M": "MALE", "F": "FEMALE"}
        normalized = aliases.get(normalized, normalized)
        if normalized not in {"MALE", "FEMALE"}:
            raise CombinedApplicationResolutionError(
                "COMBINED_INVALID_SEX",
                "sex must be MALE or FEMALE",
            )
        return normalized

    def resolve(
        self,
        request: CombinedChartApplicationRequest,
    ) -> CombinedChartApplicationResolution:
        request.combined_profile.validate()
        request.ziwei_application_profile.validate()
        request.ziwei_presentation_profile.validate()
        request.bazi_application_profile.validate()
        sex = self._normalize_sex(request.sex)
        if request.ziwei_daxian_count < 1 or request.ziwei_daxian_count > 20:
            raise CombinedApplicationResolutionError(
                "COMBINED_INVALID_ZIWEI_DAXIAN_COUNT",
                str(request.ziwei_daxian_count),
            )
        if request.bazi_dayun_count < 1 or request.bazi_dayun_count > 20:
            raise CombinedApplicationResolutionError(
                "COMBINED_INVALID_BAZI_DAYUN_COUNT",
                str(request.bazi_dayun_count),
            )

        ziwei_bundle = None
        ziwei_error = None
        try:
            ziwei_service = ZiweiChartService(
                self.ziwei_foundation,
                request.ziwei_application_profile,
            )
            ziwei_bundle = ziwei_service.resolve(
                ApplicationBirthRequest(
                    birth=request.birth,
                    sex=Sex(sex),
                    calculation_profile=request.ziwei_calculation_profile,
                    presentation_profile=request.ziwei_presentation_profile,
                    daxian_frame_id=request.ziwei_daxian_frame_id,
                    annual_year=request.ziwei_annual_year,
                    minor_limit_age=request.ziwei_minor_limit_age,
                    daxian_count=request.ziwei_daxian_count,
                )
            )
            validate_application_bundle(ziwei_bundle)
        except (ApplicationResolutionError, ValueError) as exc:
            ziwei_error = CombinedSubsystemError(
                code=str(
                    getattr(exc, "diagnostic_code", None)
                    or "COMBINED_ZIWEI_RESOLUTION_FAILED"
                ),
                detail=str(exc),
            )
            ziwei_bundle = None

        bazi_bundle = None
        bazi_error = None
        try:
            bazi_bundle = self.bazi_service.resolve(
                BaziApplicationRequest(
                    birth=request.birth,
                    sex=BaziSex(sex),
                    natal_profile=request.bazi_natal_profile,
                    temporal_profile=request.bazi_temporal_profile,
                    application_profile=request.bazi_application_profile,
                    dayun_count=request.bazi_dayun_count,
                )
            )
            report = validate_bazi_application_resolution(bazi_bundle)
            if report.status != "PASS":
                raise BaziApplicationResolutionError(
                    "COMBINED_BAZI_BUNDLE_REPLAY_FAILED",
                    ";".join(report.diagnostics),
                )
        except (BaziApplicationResolutionError, ValueError) as exc:
            bazi_error = CombinedSubsystemError(
                code=str(
                    getattr(exc, "code", None)
                    or "COMBINED_BAZI_RESOLUTION_FAILED"
                ),
                detail=str(exc),
            )
            bazi_bundle = None

        if ziwei_bundle is None and bazi_bundle is None:
            status = "FAILED"
        elif ziwei_bundle is None or bazi_bundle is None:
            status = "PARTIAL"
        else:
            uncertainty = (
                ziwei_bundle.resolution_status != "RESOLVED"
                or bazi_bundle.status != "RESOLVED"
            )
            status = "UNCERTAINTY_PRESENT" if uncertainty else "RESOLVED_BOTH"

        resolution = CombinedChartApplicationResolution(
            schema=COMBINED_RESOLUTION_SCHEMA,
            status=status,
            birth=request.birth,
            sex=sex,
            combined_profile=request.combined_profile,
            ziwei_calculation_profile=request.ziwei_calculation_profile,
            ziwei_application_profile=request.ziwei_application_profile,
            ziwei_presentation_profile=request.ziwei_presentation_profile,
            bazi_natal_profile=request.bazi_natal_profile,
            bazi_temporal_profile=request.bazi_temporal_profile,
            bazi_application_profile=request.bazi_application_profile,
            ziwei_bundle=ziwei_bundle,
            bazi_bundle=bazi_bundle,
            ziwei_error=ziwei_error,
            bazi_error=bazi_error,
            manifest_hash="PENDING",
            integrity=CombinedApplicationIntegrityReport(
                status="PENDING",
                diagnostics=(),
            ),
        )
        resolution = replace(
            resolution,
            manifest_hash=combined_manifest_hash(resolution),
        )
        report = validate_combined_resolution(resolution)
        if report.status != "PASS":
            raise CombinedApplicationResolutionError(
                "COMBINED_BUNDLE_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return replace(resolution, integrity=report)

    def export(self, resolution: CombinedChartApplicationResolution) -> dict[str, Any]:
        report = validate_combined_resolution(resolution)
        if report.status != "PASS":
            raise CombinedApplicationResolutionError(
                "COMBINED_EXPORT_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return {
            "schema": COMBINED_EXPORT_SCHEMA,
            "manifest": {
                **combined_manifest_payload(resolution),
                "manifest_hash": resolution.manifest_hash,
            },
            "ziwei_export": (
                application_export(resolution.ziwei_bundle)
                if resolution.ziwei_bundle is not None
                else None
            ),
            "bazi_export": (
                json_value(resolution.bazi_bundle)
                if resolution.bazi_bundle is not None
                else None
            ),
        }

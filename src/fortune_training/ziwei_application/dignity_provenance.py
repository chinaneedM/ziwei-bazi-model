from __future__ import annotations

from dataclasses import dataclass

from fortune_training.util import object_sha256
from fortune_training.ziwei_chart.dignity import (
    OPERATIONAL_DIGNITY_RULE_SET_ID,
    OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID,
)
from fortune_training.ziwei_chart.dignity_r3 import OPERATIONAL_FULL_DIGNITY_RULE_SET_ID
from fortune_training.ziwei_chart.dignity_r4 import OPERATIONAL_R4_DIGNITY_RULE_SET_ID

from .models import ApplicationChartBundle
from .service import ApplicationResolutionError, validate_application_bundle


DIGNITY_PROVENANCE_SCHEMA = "ZIWEI-DIGNITY-ANNOTATION-PROVENANCE-SIDECAR-R1"
DIGNITY_PROVENANCE_PROFILE_ID = "ZIWEI-DIGNITY-ANNOTATION-PROVENANCE-R1"
DIGNITY_PROVENANCE_PROFILE_VERSION = "1.0.0"
DIGNITY_PROVENANCE_ALGORITHM_ID = "ZIWEI-DIGNITY-ANNOTATION-PROVENANCE-COMPOSER-R1"
DIGNITY_PROVENANCE_ALGORITHM_VERSION = "1.0.0"
DIGNITY_PROVENANCE_INTEGRITY_ID = "ZIWEI-DIGNITY-ANNOTATION-PROVENANCE-INTEGRITY-R1"
DIGNITY_PROVENANCE_INTEGRITY_VERSION = "1.0.0"
DIGNITY_PROVENANCE_AUTHORITY_CLASS = "PROJECT_OPERATIONAL_REGISTRY"
DIGNITY_PROVENANCE_S01_BRIGHTNESS_AUTHORITY = "NOT_CLAIMED"
DIGNITY_PROVENANCE_SEMANTIC_SCOPE = (
    "EXISTING_DIGNITY_ANNOTATION_PROVENANCE_ONLY_"
    "NOT_S01_FROZEN_BRIGHTNESS_NO_AUSPICIOUSNESS_STRENGTH_OR_PREDICTION"
)

_SUPPORTED_OPERATIONAL_RULE_SET_IDS = frozenset(
    {
        OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID,
        OPERATIONAL_DIGNITY_RULE_SET_ID,
        OPERATIONAL_FULL_DIGNITY_RULE_SET_ID,
        OPERATIONAL_R4_DIGNITY_RULE_SET_ID,
    }
)


class ZiweiDignityProvenanceResolutionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.detail = detail


@dataclass(frozen=True)
class ZiweiDignityProvenanceIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = DIGNITY_PROVENANCE_INTEGRITY_ID
    algorithm_version: str = DIGNITY_PROVENANCE_INTEGRITY_VERSION


@dataclass(frozen=True)
class ZiweiDignityProvenanceRow:
    row_id: str
    annotation_id: str
    target_entity_id: str
    target_display_name: str
    address_index: int
    branch: str
    status: str
    grade: str | None
    scale_id: str
    scale_version: str
    rule_set_id: str
    rule_set_version: str
    generator_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]
    fact_hash: str
    computation_hash: str


@dataclass(frozen=True)
class ZiweiDignityProvenanceResolution:
    schema: str
    status: str
    source_application_bundle_hash: str
    source_natal_fact_hash: str
    source_natal_computation_hash: str
    source_dignity_rule_set_id: str
    source_dignity_rule_set_version: str
    source_dignity_algorithm_id: str
    source_dignity_algorithm_version: str
    profile_id: str
    profile_version: str
    authority_class: str
    s01_brightness_authority: str
    semantic_scope: str
    rows: tuple[ZiweiDignityProvenanceRow, ...]
    fact_hash: str
    computation_hash: str
    bundle_hash: str
    integrity: ZiweiDignityProvenanceIntegrityReport


def _row_fact_payload(
    *,
    annotation_id: str,
    target_entity_id: str,
    target_display_name: str,
    address_index: int,
    branch: str,
    status: str,
    grade: str | None,
    scale_id: str,
    scale_version: str,
    rule_set_id: str,
    rule_set_version: str,
    generator_id: str,
    algorithm_version: str,
    source_refs: tuple[str, ...],
) -> dict[str, object]:
    return {
        "annotation_id": annotation_id,
        "target_entity_id": target_entity_id,
        "target_display_name": target_display_name,
        "address_index": address_index,
        "branch": branch,
        "status": status,
        "grade": grade,
        "scale_id": scale_id,
        "scale_version": scale_version,
        "rule_set_id": rule_set_id,
        "rule_set_version": rule_set_version,
        "generator_id": generator_id,
        "algorithm_version": algorithm_version,
        "source_refs": list(source_refs),
    }


def _build_row(**values) -> ZiweiDignityProvenanceRow:
    fact_payload = _row_fact_payload(**values)
    fact_hash = object_sha256(fact_payload)
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "algorithm": (
                f"{DIGNITY_PROVENANCE_ALGORITHM_ID}@"
                f"{DIGNITY_PROVENANCE_ALGORITHM_VERSION}"
            ),
        }
    )
    row_id = f"ZIWEI-DIGNITY-PROVENANCE:{object_sha256({'fact_hash': fact_hash})}"
    return ZiweiDignityProvenanceRow(
        **values,
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        row_id=row_id,
    )


def _resolution_hashes(
    *,
    source_application_bundle_hash: str,
    source_natal_fact_hash: str,
    source_natal_computation_hash: str,
    source_dignity_rule_set_id: str,
    source_dignity_rule_set_version: str,
    source_dignity_algorithm_id: str,
    source_dignity_algorithm_version: str,
    rows: tuple[ZiweiDignityProvenanceRow, ...],
) -> tuple[str, str, str]:
    fact_hash = object_sha256(
        {
            "schema": DIGNITY_PROVENANCE_SCHEMA,
            "source_natal_fact_hash": source_natal_fact_hash,
            "source_dignity_rule_set_id": source_dignity_rule_set_id,
            "source_dignity_rule_set_version": source_dignity_rule_set_version,
            "profile_id": DIGNITY_PROVENANCE_PROFILE_ID,
            "profile_version": DIGNITY_PROVENANCE_PROFILE_VERSION,
            "authority_class": DIGNITY_PROVENANCE_AUTHORITY_CLASS,
            "s01_brightness_authority": DIGNITY_PROVENANCE_S01_BRIGHTNESS_AUTHORITY,
            "semantic_scope": DIGNITY_PROVENANCE_SEMANTIC_SCOPE,
            "row_fact_hashes": [row.fact_hash for row in rows],
        }
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_application_bundle_hash": source_application_bundle_hash,
            "source_natal_computation_hash": source_natal_computation_hash,
            "source_dignity_algorithm_id": source_dignity_algorithm_id,
            "source_dignity_algorithm_version": source_dignity_algorithm_version,
            "row_computation_hashes": [row.computation_hash for row in rows],
            "algorithm": (
                f"{DIGNITY_PROVENANCE_ALGORITHM_ID}@"
                f"{DIGNITY_PROVENANCE_ALGORITHM_VERSION}"
            ),
        }
    )
    bundle_hash = object_sha256(
        {
            "schema": DIGNITY_PROVENANCE_SCHEMA,
            "status": "COMPLETE",
            "profile_id": DIGNITY_PROVENANCE_PROFILE_ID,
            "profile_version": DIGNITY_PROVENANCE_PROFILE_VERSION,
            "fact_hash": fact_hash,
            "computation_hash": computation_hash,
            "row_ids": [row.row_id for row in rows],
        }
    )
    return fact_hash, computation_hash, bundle_hash


def validate_dignity_provenance(
    resolution: ZiweiDignityProvenanceResolution,
) -> ZiweiDignityProvenanceIntegrityReport:
    diagnostics: list[str] = []
    if resolution.schema != DIGNITY_PROVENANCE_SCHEMA:
        diagnostics.append("SCHEMA_MISMATCH")
    if resolution.status != "COMPLETE":
        diagnostics.append("STATUS_NOT_COMPLETE")
    if (
        resolution.profile_id != DIGNITY_PROVENANCE_PROFILE_ID
        or resolution.profile_version != DIGNITY_PROVENANCE_PROFILE_VERSION
    ):
        diagnostics.append("PROFILE_MISMATCH")
    if resolution.authority_class != DIGNITY_PROVENANCE_AUTHORITY_CLASS:
        diagnostics.append("AUTHORITY_CLASS_MISMATCH")
    if resolution.s01_brightness_authority != DIGNITY_PROVENANCE_S01_BRIGHTNESS_AUTHORITY:
        diagnostics.append("S01_BRIGHTNESS_AUTHORITY_MISMATCH")
    if resolution.semantic_scope != DIGNITY_PROVENANCE_SEMANTIC_SCOPE:
        diagnostics.append("SEMANTIC_SCOPE_MISMATCH")
    if resolution.source_dignity_rule_set_id not in _SUPPORTED_OPERATIONAL_RULE_SET_IDS:
        diagnostics.append("SOURCE_RULE_SET_UNSUPPORTED")
    if not resolution.rows:
        diagnostics.append("ROWS_EMPTY")

    row_ids: set[str] = set()
    annotation_ids: set[str] = set()
    expected_rows: list[ZiweiDignityProvenanceRow] = []
    for row in resolution.rows:
        if row.row_id in row_ids:
            diagnostics.append(f"DUPLICATE_ROW_ID:{row.row_id}")
        row_ids.add(row.row_id)
        if row.annotation_id in annotation_ids:
            diagnostics.append(f"DUPLICATE_ANNOTATION_ID:{row.annotation_id}")
        annotation_ids.add(row.annotation_id)
        if row.address_index not in range(12):
            diagnostics.append(f"ADDRESS_OUT_OF_RANGE:{row.row_id}")
            continue
        if row.rule_set_id != resolution.source_dignity_rule_set_id:
            diagnostics.append(f"RULE_SET_ID_MISMATCH:{row.row_id}")
        if row.rule_set_version != resolution.source_dignity_rule_set_version:
            diagnostics.append(f"RULE_SET_VERSION_MISMATCH:{row.row_id}")
        if row.generator_id != resolution.source_dignity_algorithm_id:
            diagnostics.append(f"GENERATOR_ID_MISMATCH:{row.row_id}")
        if row.algorithm_version != resolution.source_dignity_algorithm_version:
            diagnostics.append(f"ALGORITHM_VERSION_MISMATCH:{row.row_id}")
        if not row.source_refs:
            diagnostics.append(f"SOURCE_REFS_EMPTY:{row.row_id}")
        expected = _build_row(
            annotation_id=row.annotation_id,
            target_entity_id=row.target_entity_id,
            target_display_name=row.target_display_name,
            address_index=row.address_index,
            branch=row.branch,
            status=row.status,
            grade=row.grade,
            scale_id=row.scale_id,
            scale_version=row.scale_version,
            rule_set_id=row.rule_set_id,
            rule_set_version=row.rule_set_version,
            generator_id=row.generator_id,
            algorithm_version=row.algorithm_version,
            source_refs=row.source_refs,
        )
        if row.fact_hash != expected.fact_hash:
            diagnostics.append(f"ROW_FACT_HASH_MISMATCH:{row.row_id}")
        if row.computation_hash != expected.computation_hash:
            diagnostics.append(f"ROW_COMPUTATION_HASH_MISMATCH:{row.row_id}")
        if row.row_id != expected.row_id:
            diagnostics.append(f"ROW_ID_MISMATCH:{row.row_id}")
        expected_rows.append(expected)

    if len(expected_rows) == len(resolution.rows):
        fact_hash, computation_hash, bundle_hash = _resolution_hashes(
            source_application_bundle_hash=resolution.source_application_bundle_hash,
            source_natal_fact_hash=resolution.source_natal_fact_hash,
            source_natal_computation_hash=resolution.source_natal_computation_hash,
            source_dignity_rule_set_id=resolution.source_dignity_rule_set_id,
            source_dignity_rule_set_version=resolution.source_dignity_rule_set_version,
            source_dignity_algorithm_id=resolution.source_dignity_algorithm_id,
            source_dignity_algorithm_version=resolution.source_dignity_algorithm_version,
            rows=tuple(expected_rows),
        )
        if resolution.fact_hash != fact_hash:
            diagnostics.append("FACT_HASH_MISMATCH")
        if resolution.computation_hash != computation_hash:
            diagnostics.append("COMPUTATION_HASH_MISMATCH")
        if resolution.bundle_hash != bundle_hash:
            diagnostics.append("BUNDLE_HASH_MISMATCH")

    return ZiweiDignityProvenanceIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )


class ZiweiDignityAnnotationProvenanceService:
    schema = DIGNITY_PROVENANCE_SCHEMA

    def _resolve_once(
        self,
        base_application: ApplicationChartBundle,
    ) -> ZiweiDignityProvenanceResolution:
        try:
            validate_application_bundle(base_application)
        except ApplicationResolutionError as exc:
            raise ZiweiDignityProvenanceResolutionError(
                "ZIWEI_DIGNITY_PROVENANCE_SOURCE_APPLICATION_INVALID",
                str(exc),
            ) from exc

        profile = base_application.calculation_profile
        identity = (
            profile.dignity_rule_set_id,
            profile.dignity_rule_set_version,
            profile.dignity_algorithm_id,
            profile.dignity_algorithm_version,
        )
        if any(value is None for value in identity):
            raise ZiweiDignityProvenanceResolutionError(
                "ZIWEI_DIGNITY_PROVENANCE_SOURCE_DIGNITY_DISABLED",
                "source calculation profile does not enable Dignity annotations",
            )
        rule_set_id, rule_set_version, algorithm_id, algorithm_version = identity
        assert rule_set_id is not None
        assert rule_set_version is not None
        assert algorithm_id is not None
        assert algorithm_version is not None
        if rule_set_id not in _SUPPORTED_OPERATIONAL_RULE_SET_IDS:
            raise ZiweiDignityProvenanceResolutionError(
                "ZIWEI_DIGNITY_PROVENANCE_UNSUPPORTED_RULE_SET",
                rule_set_id,
            )

        placement_by_entity = {
            row.entity_id: row for row in base_application.candidate.chart.placements
        }
        dignity_annotations = tuple(
            row
            for row in base_application.candidate.chart.annotations
            if row.annotation_type == "DIGNITY"
        )
        if not dignity_annotations:
            raise ZiweiDignityProvenanceResolutionError(
                "ZIWEI_DIGNITY_PROVENANCE_ROWS_EMPTY",
                "source chart contains no Dignity annotations",
            )

        rows: list[ZiweiDignityProvenanceRow] = []
        seen: set[str] = set()
        for annotation in dignity_annotations:
            if annotation.annotation_id in seen:
                raise ZiweiDignityProvenanceResolutionError(
                    "ZIWEI_DIGNITY_PROVENANCE_DUPLICATE_ANNOTATION",
                    annotation.annotation_id,
                )
            seen.add(annotation.annotation_id)
            placement = placement_by_entity.get(annotation.target_entity_id)
            if placement is None or placement.address != annotation.target_address:
                raise ZiweiDignityProvenanceResolutionError(
                    "ZIWEI_DIGNITY_PROVENANCE_TARGET_BINDING_MISMATCH",
                    annotation.annotation_id,
                )
            if (
                annotation.rule_set_id != rule_set_id
                or annotation.rule_set_version != rule_set_version
                or annotation.generator_id != algorithm_id
                or annotation.algorithm_version != algorithm_version
            ):
                raise ZiweiDignityProvenanceResolutionError(
                    "ZIWEI_DIGNITY_PROVENANCE_PROFILE_BINDING_MISMATCH",
                    annotation.annotation_id,
                )
            rows.append(
                _build_row(
                    annotation_id=annotation.annotation_id,
                    target_entity_id=annotation.target_entity_id,
                    target_display_name=placement.display_name,
                    address_index=annotation.target_address.index,
                    branch=annotation.target_address.branch,
                    status=annotation.status,
                    grade=annotation.grade,
                    scale_id=annotation.scale_id,
                    scale_version=annotation.scale_version,
                    rule_set_id=annotation.rule_set_id,
                    rule_set_version=annotation.rule_set_version,
                    generator_id=annotation.generator_id,
                    algorithm_version=annotation.algorithm_version,
                    source_refs=tuple(annotation.source_refs),
                )
            )
        sorted_rows = tuple(sorted(rows, key=lambda row: (row.address_index, row.target_entity_id)))
        fact_hash, computation_hash, bundle_hash = _resolution_hashes(
            source_application_bundle_hash=base_application.bundle_hash,
            source_natal_fact_hash=base_application.candidate.hashes.fact_hash,
            source_natal_computation_hash=base_application.candidate.hashes.computation_hash,
            source_dignity_rule_set_id=rule_set_id,
            source_dignity_rule_set_version=rule_set_version,
            source_dignity_algorithm_id=algorithm_id,
            source_dignity_algorithm_version=algorithm_version,
            rows=sorted_rows,
        )
        provisional = ZiweiDignityProvenanceResolution(
            schema=DIGNITY_PROVENANCE_SCHEMA,
            status="COMPLETE",
            source_application_bundle_hash=base_application.bundle_hash,
            source_natal_fact_hash=base_application.candidate.hashes.fact_hash,
            source_natal_computation_hash=base_application.candidate.hashes.computation_hash,
            source_dignity_rule_set_id=rule_set_id,
            source_dignity_rule_set_version=rule_set_version,
            source_dignity_algorithm_id=algorithm_id,
            source_dignity_algorithm_version=algorithm_version,
            profile_id=DIGNITY_PROVENANCE_PROFILE_ID,
            profile_version=DIGNITY_PROVENANCE_PROFILE_VERSION,
            authority_class=DIGNITY_PROVENANCE_AUTHORITY_CLASS,
            s01_brightness_authority=DIGNITY_PROVENANCE_S01_BRIGHTNESS_AUTHORITY,
            semantic_scope=DIGNITY_PROVENANCE_SEMANTIC_SCOPE,
            rows=sorted_rows,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
            bundle_hash=bundle_hash,
            integrity=ZiweiDignityProvenanceIntegrityReport(status="PENDING", diagnostics=()),
        )
        integrity = validate_dignity_provenance(provisional)
        if integrity.status != "PASS":
            raise ZiweiDignityProvenanceResolutionError(
                "ZIWEI_DIGNITY_PROVENANCE_INTEGRITY_FAILED",
                ";".join(integrity.diagnostics),
            )
        return ZiweiDignityProvenanceResolution(
            **{**provisional.__dict__, "integrity": integrity}
        )

    def resolve(
        self,
        base_application: ApplicationChartBundle,
    ) -> ZiweiDignityProvenanceResolution:
        first = self._resolve_once(base_application)
        replay = self._resolve_once(base_application)
        if replay != first:
            raise ZiweiDignityProvenanceResolutionError(
                "ZIWEI_DIGNITY_PROVENANCE_FULL_REPLAY_FAILED",
                "identical application bundle produced different Dignity provenance",
            )
        return first

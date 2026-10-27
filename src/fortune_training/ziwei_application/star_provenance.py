from __future__ import annotations

from dataclasses import dataclass

from fortune_training.util import object_sha256
from fortune_training.ziwei_chart.auxiliary import AUXILIARY_ALGORITHM_ID
from fortune_training.ziwei_chart.derived_auxiliary import DERIVED_AUXILIARY_ALGORITHM_ID
from fortune_training.ziwei_chart.main_stars import (
    MAIN_STAR_ALGORITHM_ID,
    TIANFU_SOURCE_REFS,
    ZIWEI_SOURCE_REFS,
)
from fortune_training.ziwei_chart.minor_stars import MINOR_STAR_ALGORITHM_ID

from .models import ApplicationChartBundle
from .service import ApplicationResolutionError, validate_application_bundle


STAR_PROVENANCE_SCHEMA = "ZIWEI-STAR-PLACEMENT-PROVENANCE-SIDECAR-R1"
STAR_PROVENANCE_PROFILE_ID = "ZIWEI-STAR-PLACEMENT-PROVENANCE-R1"
STAR_PROVENANCE_PROFILE_VERSION = "1.0.0"
STAR_PROVENANCE_ALGORITHM_ID = "ZIWEI-STAR-PLACEMENT-PROVENANCE-COMPOSER-R1"
STAR_PROVENANCE_ALGORITHM_VERSION = "1.0.0"
STAR_PROVENANCE_INTEGRITY_ID = "ZIWEI-STAR-PLACEMENT-PROVENANCE-INTEGRITY-R1"
STAR_PROVENANCE_INTEGRITY_VERSION = "1.0.0"
STAR_PROVENANCE_CLASSIFICATION_POLICY = "GENERATOR_IDENTITY_AND_RELEASED_MAIN_STAR_SOURCE_REFS_ONLY"
STAR_PROVENANCE_SEMANTIC_SCOPE = (
    "PLACEMENT_GENERATOR_PROVENANCE_ONLY_NO_AUSPICIOUSNESS_OR_DOCTRINAL_STAR_CLASSIFICATION"
)

_GENERATOR_FAMILIES = {
    MAIN_STAR_ALGORITHM_ID: ("FOURTEEN_MAIN_STARS", "十四主星"),
    AUXILIARY_ALGORITHM_ID: ("CORE_AUXILIARY", "核心辅曜"),
    DERIVED_AUXILIARY_ALGORITHM_ID: ("DERIVED_AUXILIARY", "派生辅曜"),
    MINOR_STAR_ALGORITHM_ID: ("OPERATIONAL_MINOR_STARS", "小星"),
}


class ZiweiStarProvenanceResolutionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.detail = detail


@dataclass(frozen=True)
class ZiweiStarProvenanceIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = STAR_PROVENANCE_INTEGRITY_ID
    algorithm_version: str = STAR_PROVENANCE_INTEGRITY_VERSION


@dataclass(frozen=True)
class ZiweiStarProvenanceRow:
    row_id: str
    entity_id: str
    display_name: str
    address_index: int
    branch: str
    generator_id: str
    algorithm_version: str
    generator_family_id: str
    generator_family_label: str
    main_star_system_id: str | None
    main_star_system_label: str | None
    source_refs: tuple[str, ...]
    fact_hash: str
    computation_hash: str


@dataclass(frozen=True)
class ZiweiStarProvenanceResolution:
    schema: str
    status: str
    source_application_bundle_hash: str
    source_natal_fact_hash: str
    source_natal_computation_hash: str
    profile_id: str
    profile_version: str
    classification_policy: str
    semantic_scope: str
    rows: tuple[ZiweiStarProvenanceRow, ...]
    fact_hash: str
    computation_hash: str
    bundle_hash: str
    integrity: ZiweiStarProvenanceIntegrityReport


def _family_for_generator(generator_id: str) -> tuple[str, str]:
    try:
        return _GENERATOR_FAMILIES[generator_id]
    except KeyError as exc:
        raise ZiweiStarProvenanceResolutionError(
            "ZIWEI_STAR_PROVENANCE_UNKNOWN_GENERATOR",
            generator_id,
        ) from exc


def _main_star_system(
    generator_id: str,
    source_refs: tuple[str, ...],
) -> tuple[str | None, str | None]:
    if generator_id != MAIN_STAR_ALGORITHM_ID:
        return None, None
    if tuple(source_refs) == tuple(ZIWEI_SOURCE_REFS):
        return "ZIWEI_SYSTEM", "紫微星系"
    if tuple(source_refs) == tuple(TIANFU_SOURCE_REFS):
        return "TIANFU_SYSTEM", "天府星系"
    raise ZiweiStarProvenanceResolutionError(
        "ZIWEI_STAR_PROVENANCE_MAIN_STAR_SOURCE_REFS_UNRECOGNIZED",
        ",".join(source_refs),
    )


def _row_fact_payload(
    *,
    entity_id: str,
    display_name: str,
    address_index: int,
    branch: str,
    generator_id: str,
    algorithm_version: str,
    generator_family_id: str,
    generator_family_label: str,
    main_star_system_id: str | None,
    main_star_system_label: str | None,
    source_refs: tuple[str, ...],
) -> dict[str, object]:
    return {
        "entity_id": entity_id,
        "display_name": display_name,
        "address_index": address_index,
        "branch": branch,
        "generator_id": generator_id,
        "algorithm_version": algorithm_version,
        "generator_family_id": generator_family_id,
        "generator_family_label": generator_family_label,
        "main_star_system_id": main_star_system_id,
        "main_star_system_label": main_star_system_label,
        "source_refs": list(source_refs),
    }


def _build_row(
    *,
    entity_id: str,
    display_name: str,
    address_index: int,
    branch: str,
    generator_id: str,
    algorithm_version: str,
    generator_family_id: str,
    generator_family_label: str,
    main_star_system_id: str | None,
    main_star_system_label: str | None,
    source_refs: tuple[str, ...],
) -> ZiweiStarProvenanceRow:
    fact_payload = _row_fact_payload(
        entity_id=entity_id,
        display_name=display_name,
        address_index=address_index,
        branch=branch,
        generator_id=generator_id,
        algorithm_version=algorithm_version,
        generator_family_id=generator_family_id,
        generator_family_label=generator_family_label,
        main_star_system_id=main_star_system_id,
        main_star_system_label=main_star_system_label,
        source_refs=source_refs,
    )
    fact_hash = object_sha256(fact_payload)
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "algorithm": f"{STAR_PROVENANCE_ALGORITHM_ID}@{STAR_PROVENANCE_ALGORITHM_VERSION}",
        }
    )
    row_id = f"ZIWEI-STAR-PROVENANCE:{object_sha256({'fact_hash': fact_hash})}"
    return ZiweiStarProvenanceRow(
        row_id=row_id,
        entity_id=entity_id,
        display_name=display_name,
        address_index=address_index,
        branch=branch,
        generator_id=generator_id,
        algorithm_version=algorithm_version,
        generator_family_id=generator_family_id,
        generator_family_label=generator_family_label,
        main_star_system_id=main_star_system_id,
        main_star_system_label=main_star_system_label,
        source_refs=source_refs,
        fact_hash=fact_hash,
        computation_hash=computation_hash,
    )


def _compose_row(placement) -> ZiweiStarProvenanceRow:
    family_id, family_label = _family_for_generator(placement.generator_id)
    system_id, system_label = _main_star_system(
        placement.generator_id,
        tuple(placement.source_refs),
    )
    return _build_row(
        entity_id=placement.entity_id,
        display_name=placement.display_name,
        address_index=placement.address.index,
        branch=placement.address.branch,
        generator_id=placement.generator_id,
        algorithm_version=placement.algorithm_version,
        generator_family_id=family_id,
        generator_family_label=family_label,
        main_star_system_id=system_id,
        main_star_system_label=system_label,
        source_refs=tuple(placement.source_refs),
    )


def _resolution_hashes(
    *,
    source_application_bundle_hash: str,
    source_natal_fact_hash: str,
    source_natal_computation_hash: str,
    rows: tuple[ZiweiStarProvenanceRow, ...],
) -> tuple[str, str, str]:
    fact_hash = object_sha256(
        {
            "schema": STAR_PROVENANCE_SCHEMA,
            "source_natal_fact_hash": source_natal_fact_hash,
            "profile_id": STAR_PROVENANCE_PROFILE_ID,
            "profile_version": STAR_PROVENANCE_PROFILE_VERSION,
            "classification_policy": STAR_PROVENANCE_CLASSIFICATION_POLICY,
            "semantic_scope": STAR_PROVENANCE_SEMANTIC_SCOPE,
            "row_fact_hashes": [row.fact_hash for row in rows],
        }
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_application_bundle_hash": source_application_bundle_hash,
            "source_natal_computation_hash": source_natal_computation_hash,
            "row_computation_hashes": [row.computation_hash for row in rows],
            "algorithm": f"{STAR_PROVENANCE_ALGORITHM_ID}@{STAR_PROVENANCE_ALGORITHM_VERSION}",
        }
    )
    bundle_hash = object_sha256(
        {
            "schema": STAR_PROVENANCE_SCHEMA,
            "status": "COMPLETE",
            "profile_id": STAR_PROVENANCE_PROFILE_ID,
            "profile_version": STAR_PROVENANCE_PROFILE_VERSION,
            "fact_hash": fact_hash,
            "computation_hash": computation_hash,
            "row_ids": [row.row_id for row in rows],
        }
    )
    return fact_hash, computation_hash, bundle_hash


def validate_star_provenance(
    resolution: ZiweiStarProvenanceResolution,
) -> ZiweiStarProvenanceIntegrityReport:
    diagnostics: list[str] = []
    if resolution.schema != STAR_PROVENANCE_SCHEMA:
        diagnostics.append("SCHEMA_MISMATCH")
    if resolution.status != "COMPLETE":
        diagnostics.append("STATUS_NOT_COMPLETE")
    if resolution.profile_id != STAR_PROVENANCE_PROFILE_ID or resolution.profile_version != STAR_PROVENANCE_PROFILE_VERSION:
        diagnostics.append("PROFILE_MISMATCH")
    if resolution.classification_policy != STAR_PROVENANCE_CLASSIFICATION_POLICY:
        diagnostics.append("CLASSIFICATION_POLICY_MISMATCH")
    if resolution.semantic_scope != STAR_PROVENANCE_SEMANTIC_SCOPE:
        diagnostics.append("SEMANTIC_SCOPE_MISMATCH")
    if not resolution.rows:
        diagnostics.append("ROWS_EMPTY")

    ids: set[str] = set()
    entities: set[str] = set()
    expected_rows: list[ZiweiStarProvenanceRow] = []
    for row in resolution.rows:
        if row.row_id in ids:
            diagnostics.append(f"DUPLICATE_ROW_ID:{row.row_id}")
        ids.add(row.row_id)
        if row.entity_id in entities:
            diagnostics.append(f"DUPLICATE_ENTITY_ID:{row.entity_id}")
        entities.add(row.entity_id)
        if row.address_index not in range(12):
            diagnostics.append(f"ADDRESS_OUT_OF_RANGE:{row.row_id}")
            continue
        try:
            family_id, family_label = _family_for_generator(row.generator_id)
            system_id, system_label = _main_star_system(row.generator_id, row.source_refs)
        except ZiweiStarProvenanceResolutionError as exc:
            diagnostics.append(f"{exc.diagnostic_code}:{row.row_id}")
            continue
        if (row.generator_family_id, row.generator_family_label) != (family_id, family_label):
            diagnostics.append(f"GENERATOR_FAMILY_MISMATCH:{row.row_id}")
        if (row.main_star_system_id, row.main_star_system_label) != (system_id, system_label):
            diagnostics.append(f"MAIN_STAR_SYSTEM_MISMATCH:{row.row_id}")
        if not row.source_refs:
            diagnostics.append(f"SOURCE_REFS_EMPTY:{row.row_id}")
        expected = _build_row(
            entity_id=row.entity_id,
            display_name=row.display_name,
            address_index=row.address_index,
            branch=row.branch,
            generator_id=row.generator_id,
            algorithm_version=row.algorithm_version,
            generator_family_id=family_id,
            generator_family_label=family_label,
            main_star_system_id=system_id,
            main_star_system_label=system_label,
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
            rows=tuple(expected_rows),
        )
        if resolution.fact_hash != fact_hash:
            diagnostics.append("FACT_HASH_MISMATCH")
        if resolution.computation_hash != computation_hash:
            diagnostics.append("COMPUTATION_HASH_MISMATCH")
        if resolution.bundle_hash != bundle_hash:
            diagnostics.append("BUNDLE_HASH_MISMATCH")

    return ZiweiStarProvenanceIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )


class ZiweiStarPlacementProvenanceService:
    schema = STAR_PROVENANCE_SCHEMA

    def _resolve_once(
        self,
        base_application: ApplicationChartBundle,
    ) -> ZiweiStarProvenanceResolution:
        try:
            validate_application_bundle(base_application)
        except ApplicationResolutionError as exc:
            raise ZiweiStarProvenanceResolutionError(
                "ZIWEI_STAR_PROVENANCE_SOURCE_APPLICATION_INVALID",
                str(exc),
            ) from exc

        rows = tuple(
            sorted(
                (_compose_row(row) for row in base_application.candidate.chart.placements),
                key=lambda row: (row.address_index, row.entity_id),
            )
        )
        fact_hash, computation_hash, bundle_hash = _resolution_hashes(
            source_application_bundle_hash=base_application.bundle_hash,
            source_natal_fact_hash=base_application.candidate.hashes.fact_hash,
            source_natal_computation_hash=base_application.candidate.hashes.computation_hash,
            rows=rows,
        )
        provisional = ZiweiStarProvenanceResolution(
            schema=STAR_PROVENANCE_SCHEMA,
            status="COMPLETE",
            source_application_bundle_hash=base_application.bundle_hash,
            source_natal_fact_hash=base_application.candidate.hashes.fact_hash,
            source_natal_computation_hash=base_application.candidate.hashes.computation_hash,
            profile_id=STAR_PROVENANCE_PROFILE_ID,
            profile_version=STAR_PROVENANCE_PROFILE_VERSION,
            classification_policy=STAR_PROVENANCE_CLASSIFICATION_POLICY,
            semantic_scope=STAR_PROVENANCE_SEMANTIC_SCOPE,
            rows=rows,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
            bundle_hash=bundle_hash,
            integrity=ZiweiStarProvenanceIntegrityReport(status="PENDING", diagnostics=()),
        )
        integrity = validate_star_provenance(provisional)
        if integrity.status != "PASS":
            raise ZiweiStarProvenanceResolutionError(
                "ZIWEI_STAR_PROVENANCE_INTEGRITY_FAILED",
                ";".join(integrity.diagnostics),
            )
        return ZiweiStarProvenanceResolution(
            **{**provisional.__dict__, "integrity": integrity}
        )

    def resolve(
        self,
        base_application: ApplicationChartBundle,
    ) -> ZiweiStarProvenanceResolution:
        first = self._resolve_once(base_application)
        replay = self._resolve_once(base_application)
        if replay != first:
            raise ZiweiStarProvenanceResolutionError(
                "ZIWEI_STAR_PROVENANCE_FULL_REPLAY_FAILED",
                "identical application bundle produced different star provenance",
            )
        return first

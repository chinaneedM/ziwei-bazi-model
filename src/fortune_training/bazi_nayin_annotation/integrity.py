from __future__ import annotations

from typing import Any

from fortune_training.bazi_chart.integrity import natal_hash_bundle, validate_natal_state
from fortune_training.bazi_chart.models import BaziNatalState
from fortune_training.bazi_chart.profile import ResolvedBaziCalculationProfile
from fortune_training.bazi_chart.registries import PILLAR_POSITIONS, sexagenary_index
from fortune_training.util import object_sha256

from .models import (
    BaziNayinAnnotationResolution,
    NayinIntegrityDiagnostic,
    NayinIntegrityReport,
    NayinPillarAnnotation,
)
from .registry import (
    NAYIN_ALGORITHM_ID,
    NAYIN_ALGORITHM_VERSION,
    NAYIN_ANNOTATION_PROFILE_ID,
    NAYIN_ANNOTATION_PROFILE_VERSION,
    NAYIN_REGISTRY_ID,
    NAYIN_REGISTRY_ORIGIN,
    NAYIN_REGISTRY_VERSION,
    NAYIN_SOURCE_REFS,
    entry_for_sexagenary_index,
    released_registry_hash,
    validate_released_registry,
)


NAYIN_INTEGRITY_ALGORITHM_ID = "BAZI-NAYIN-INTEGRITY-R1"
NAYIN_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
NAYIN_HASH_ALGORITHM_ID = "BAZI-NAYIN-HASH-R1"
NAYIN_HASH_ALGORITHM_VERSION = "1.0.0"


def _diag(rows: list[NayinIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(NayinIntegrityDiagnostic(code=code, path=path, detail=detail))


def generate_nayin_annotations(natal: BaziNatalState) -> tuple[NayinPillarAnnotation, ...]:
    upstream = validate_natal_state(natal)
    if upstream.status != "PASS":
        summary = ", ".join(f"{row.code}:{row.path}" for row in upstream.diagnostics)
        raise ValueError(f"invalid upstream Bazi Natal state: {summary}")
    validate_released_registry()

    annotations: list[NayinPillarAnnotation] = []
    for pillar in natal.pillars:
        expected_index = sexagenary_index(pillar.ganzhi)
        if expected_index != pillar.sexagenary_index:
            raise ValueError(f"pillar sexagenary identity mismatch: {pillar.position}")
        entry = entry_for_sexagenary_index(pillar.sexagenary_index)
        if pillar.ganzhi not in entry.ganzhi:
            raise ValueError(
                f"Nayin registry does not bind pillar identity: {pillar.position}:{pillar.ganzhi}"
            )
        annotations.append(
            NayinPillarAnnotation(
                annotation_id=f"BAZI-NAYIN:{pillar.position}:{pillar.sexagenary_index:02d}",
                source_pillar_position=pillar.position,
                source_pillar_ganzhi=pillar.ganzhi,
                source_pillar_sexagenary_index=pillar.sexagenary_index,
                source_stem_instance_id=pillar.stem_instance_id,
                source_branch_instance_id=pillar.branch_instance_id,
                nayin_semantic_id=entry.semantic_id,
                display_name=entry.display_name,
                element=entry.element,
                registry_id=NAYIN_REGISTRY_ID,
                registry_version=NAYIN_REGISTRY_VERSION,
                source_refs=NAYIN_SOURCE_REFS,
            )
        )
    return tuple(annotations)


def nayin_fact_projection(
    source_natal_fact_hash: str,
    annotations: tuple[NayinPillarAnnotation, ...],
) -> dict[str, Any]:
    return {
        "source_natal_fact_hash": source_natal_fact_hash,
        "annotations": [
            {
                "annotation_id": row.annotation_id,
                "source_pillar_position": row.source_pillar_position,
                "source_pillar_ganzhi": row.source_pillar_ganzhi,
                "source_pillar_sexagenary_index": row.source_pillar_sexagenary_index,
                "source_stem_instance_id": row.source_stem_instance_id,
                "source_branch_instance_id": row.source_branch_instance_id,
                "nayin_semantic_id": row.nayin_semantic_id,
                "display_name": row.display_name,
                "element": row.element,
                "registry_id": row.registry_id,
                "registry_version": row.registry_version,
                "source_refs": list(row.source_refs),
            }
            for row in annotations
        ],
    }


def compute_nayin_hashes(
    *,
    source_natal_fact_hash: str,
    source_natal_computation_hash: str,
    annotations: tuple[NayinPillarAnnotation, ...],
) -> tuple[str, str]:
    fact_hash = object_sha256(nayin_fact_projection(source_natal_fact_hash, annotations))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_natal_computation_hash": source_natal_computation_hash,
            "annotation_profile_id": NAYIN_ANNOTATION_PROFILE_ID,
            "annotation_profile_version": NAYIN_ANNOTATION_PROFILE_VERSION,
            "registry_id": NAYIN_REGISTRY_ID,
            "registry_version": NAYIN_REGISTRY_VERSION,
            "registry_origin": NAYIN_REGISTRY_ORIGIN,
            "registry_hash": released_registry_hash(),
            "source_refs": list(NAYIN_SOURCE_REFS),
            "algorithm_id": NAYIN_ALGORITHM_ID,
            "algorithm_version": NAYIN_ALGORITHM_VERSION,
            "hash_algorithm_id": NAYIN_HASH_ALGORITHM_ID,
            "hash_algorithm_version": NAYIN_HASH_ALGORITHM_VERSION,
        }
    )
    return fact_hash, computation_hash


def validate_nayin_resolution(
    natal: BaziNatalState,
    profile: ResolvedBaziCalculationProfile,
    resolution: BaziNayinAnnotationResolution,
) -> NayinIntegrityReport:
    diagnostics: list[NayinIntegrityDiagnostic] = []

    upstream = validate_natal_state(natal)
    if upstream.status != "PASS":
        for row in upstream.diagnostics:
            _diag(
                diagnostics,
                "UPSTREAM_NATAL_INVALID",
                f"natal.{row.path}",
                f"{row.code}:{row.detail}",
            )
        return NayinIntegrityReport(
            status="FAIL",
            diagnostics=tuple(diagnostics),
            algorithm_id=NAYIN_INTEGRITY_ALGORITHM_ID,
            algorithm_version=NAYIN_INTEGRITY_ALGORITHM_VERSION,
        )

    try:
        validate_released_registry()
    except ValueError as exc:
        _diag(diagnostics, "NAYIN_REGISTRY_DRIFT", "registry", str(exc))

    expected_metadata = {
        "schema": "BAZI-NAYIN-ANNOTATION-RESOLUTION-R1",
        "annotation_profile_id": NAYIN_ANNOTATION_PROFILE_ID,
        "annotation_profile_version": NAYIN_ANNOTATION_PROFILE_VERSION,
        "registry_id": NAYIN_REGISTRY_ID,
        "registry_version": NAYIN_REGISTRY_VERSION,
        "registry_origin": NAYIN_REGISTRY_ORIGIN,
        "registry_hash": released_registry_hash(),
    }
    for field, expected in expected_metadata.items():
        if getattr(resolution, field) != expected:
            _diag(
                diagnostics,
                "ANNOTATION_METADATA_MISMATCH",
                field,
                f"expected {expected!r}, got {getattr(resolution, field)!r}",
            )

    upstream_hashes = natal_hash_bundle(natal, profile)
    if resolution.source_natal_fact_hash != upstream_hashes.fact_hash:
        _diag(
            diagnostics,
            "SOURCE_NATAL_FACT_HASH_MISMATCH",
            "source_natal_fact_hash",
            resolution.source_natal_fact_hash,
        )
    if resolution.source_natal_computation_hash != upstream_hashes.computation_hash:
        _diag(
            diagnostics,
            "SOURCE_NATAL_COMPUTATION_HASH_MISMATCH",
            "source_natal_computation_hash",
            resolution.source_natal_computation_hash,
        )

    positions = tuple(row.source_pillar_position for row in resolution.annotations)
    if positions != PILLAR_POSITIONS:
        _diag(
            diagnostics,
            "ANNOTATION_PILLAR_ORDER_MISMATCH",
            "annotations",
            str(positions),
        )

    try:
        expected_annotations = generate_nayin_annotations(natal)
    except ValueError as exc:
        _diag(diagnostics, "ANNOTATION_REPLAY_FAILED", "annotations", str(exc))
        expected_annotations = ()

    if resolution.annotations != expected_annotations:
        _diag(
            diagnostics,
            "ANNOTATION_REPLAY_MISMATCH",
            "annotations",
            "published Nayin annotations do not exactly replay from source Natal pillars",
        )

    for index, row in enumerate(resolution.annotations):
        if not row.source_refs or any(not ref.strip() for ref in row.source_refs):
            _diag(
                diagnostics,
                "MISSING_PROVENANCE",
                f"annotations[{index}].source_refs",
                "source_refs must be non-empty",
            )
        if row.registry_id != NAYIN_REGISTRY_ID or row.registry_version != NAYIN_REGISTRY_VERSION:
            _diag(
                diagnostics,
                "ANNOTATION_REGISTRY_IDENTITY_MISMATCH",
                f"annotations[{index}]",
                row.annotation_id,
            )

    expected_fact_hash, expected_computation_hash = compute_nayin_hashes(
        source_natal_fact_hash=upstream_hashes.fact_hash,
        source_natal_computation_hash=upstream_hashes.computation_hash,
        annotations=resolution.annotations,
    )
    if resolution.fact_hash != expected_fact_hash:
        _diag(
            diagnostics,
            "ANNOTATION_FACT_HASH_MISMATCH",
            "fact_hash",
            resolution.fact_hash,
        )
    if resolution.computation_hash != expected_computation_hash:
        _diag(
            diagnostics,
            "ANNOTATION_COMPUTATION_HASH_MISMATCH",
            "computation_hash",
            resolution.computation_hash,
        )

    return NayinIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=NAYIN_INTEGRITY_ALGORITHM_ID,
        algorithm_version=NAYIN_INTEGRITY_ALGORITHM_VERSION,
    )

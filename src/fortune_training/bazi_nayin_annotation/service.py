from __future__ import annotations

from dataclasses import replace

from fortune_training.bazi_chart.integrity import natal_hash_bundle, validate_natal_state
from fortune_training.bazi_chart.models import BaziNatalState
from fortune_training.bazi_chart.profile import ResolvedBaziCalculationProfile

from .integrity import compute_nayin_hashes, generate_nayin_annotations, validate_nayin_resolution
from .models import BaziNayinAnnotationResolution, NayinIntegrityReport
from .registry import (
    NAYIN_ANNOTATION_PROFILE_ID,
    NAYIN_ANNOTATION_PROFILE_VERSION,
    NAYIN_REGISTRY_ID,
    NAYIN_REGISTRY_ORIGIN,
    NAYIN_REGISTRY_VERSION,
    released_registry_hash,
    validate_released_registry,
)


class BaziNayinAnnotationService:
    schema = "BAZI-NAYIN-ANNOTATION-RESOLUTION-R1"

    def resolve(
        self,
        natal: BaziNatalState,
        profile: ResolvedBaziCalculationProfile,
    ) -> BaziNayinAnnotationResolution:
        upstream = validate_natal_state(natal)
        if upstream.status != "PASS":
            summary = ", ".join(f"{row.code}:{row.path}" for row in upstream.diagnostics)
            raise ValueError(f"invalid upstream Bazi Natal state: {summary}")
        if natal.profile_id != profile.profile_id or natal.profile_version != profile.profile_version:
            raise ValueError(
                "Bazi Natal/profile identity mismatch: "
                f"natal={natal.profile_id}@{natal.profile_version} "
                f"profile={profile.profile_id}@{profile.profile_version}"
            )

        validate_released_registry()
        upstream_hashes = natal_hash_bundle(natal, profile)
        annotations = generate_nayin_annotations(natal)
        fact_hash, computation_hash = compute_nayin_hashes(
            source_natal_fact_hash=upstream_hashes.fact_hash,
            source_natal_computation_hash=upstream_hashes.computation_hash,
            annotations=annotations,
        )
        provisional = BaziNayinAnnotationResolution(
            schema=self.schema,
            annotation_profile_id=NAYIN_ANNOTATION_PROFILE_ID,
            annotation_profile_version=NAYIN_ANNOTATION_PROFILE_VERSION,
            registry_id=NAYIN_REGISTRY_ID,
            registry_version=NAYIN_REGISTRY_VERSION,
            registry_origin=NAYIN_REGISTRY_ORIGIN,
            registry_hash=released_registry_hash(),
            source_natal_fact_hash=upstream_hashes.fact_hash,
            source_natal_computation_hash=upstream_hashes.computation_hash,
            annotations=annotations,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
            integrity=NayinIntegrityReport(status="PASS", diagnostics=()),
        )
        report = validate_nayin_resolution(natal, profile, provisional)
        if report.status != "PASS":
            summary = ", ".join(f"{row.code}:{row.path}" for row in report.diagnostics)
            raise ValueError(f"Bazi Nayin annotation integrity failed: {summary}")
        return replace(provisional, integrity=report)

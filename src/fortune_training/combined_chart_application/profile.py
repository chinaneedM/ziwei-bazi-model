from __future__ import annotations

from dataclasses import dataclass


COMBINED_PROFILE_ID = "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1"
COMBINED_PROFILE_VERSION = "1.0.0"
COMBINED_ALGORITHM_ID = "ZIWEI-BAZI-INDEPENDENT-BUNDLE-COMPOSER-V1"
COMBINED_ALGORITHM_VERSION = "1.0.0"
COMBINED_MANIFEST_SCHEMA = "ZIWEI-BAZI-COMBINED-MANIFEST-V1"


@dataclass(frozen=True)
class CombinedChartApplicationProfile:
    profile_id: str = COMBINED_PROFILE_ID
    profile_version: str = COMBINED_PROFILE_VERSION
    algorithm_id: str = COMBINED_ALGORITHM_ID
    algorithm_version: str = COMBINED_ALGORITHM_VERSION
    manifest_schema: str = COMBINED_MANIFEST_SCHEMA
    composition_semantics: str = "INDEPENDENT_BUNDLE_IDENTITY_COMPOSITION_ONLY"
    cross_system_interpretation: str = "NOT_INCLUDED"
    cross_system_scoring: str = "NOT_INCLUDED"
    prediction_semantics: str = "NOT_INCLUDED"

    def validate(self) -> "CombinedChartApplicationProfile":
        expected = {
            "profile_id": COMBINED_PROFILE_ID,
            "profile_version": COMBINED_PROFILE_VERSION,
            "algorithm_id": COMBINED_ALGORITHM_ID,
            "algorithm_version": COMBINED_ALGORITHM_VERSION,
            "manifest_schema": COMBINED_MANIFEST_SCHEMA,
            "composition_semantics": "INDEPENDENT_BUNDLE_IDENTITY_COMPOSITION_ONLY",
            "cross_system_interpretation": "NOT_INCLUDED",
            "cross_system_scoring": "NOT_INCLUDED",
            "prediction_semantics": "NOT_INCLUDED",
        }
        for field, value in expected.items():
            if getattr(self, field) != value:
                raise ValueError(
                    f"unsupported combined application {field}: {getattr(self, field)!r}"
                )
        return self


def combined_chart_application_v1_profile() -> CombinedChartApplicationProfile:
    return CombinedChartApplicationProfile().validate()

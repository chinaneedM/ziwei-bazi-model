from __future__ import annotations

from dataclasses import dataclass


APPLICATION_PROFILE_ID = "BAZI-LOCAL-APPLICATION-V1-R1"
APPLICATION_PROFILE_VERSION = "1.0.0"
APPLICATION_ALGORITHM_ID = "BAZI-LOCAL-APPLICATION-COMPOSER-V1"
APPLICATION_ALGORITHM_VERSION = "1.0.0"
VIEW_SCHEMA = "BAZI-LOCAL-APPLICATION-VIEW-V1"


@dataclass(frozen=True)
class BaziApplicationProfile:
    profile_id: str = APPLICATION_PROFILE_ID
    profile_version: str = APPLICATION_PROFILE_VERSION
    algorithm_id: str = APPLICATION_ALGORITHM_ID
    algorithm_version: str = APPLICATION_ALGORITHM_VERSION
    view_schema: str = VIEW_SCHEMA
    presentation_semantics: str = "READ_ONLY_PROJECTION_OF_RELEASED_BAZI_FACTS"
    classical_interaction_semantics: str = "NOT_INCLUDED"
    prediction_semantics: str = "NOT_INCLUDED"

    def validate(self) -> "BaziApplicationProfile":
        expected = {
            "profile_id": APPLICATION_PROFILE_ID,
            "profile_version": APPLICATION_PROFILE_VERSION,
            "algorithm_id": APPLICATION_ALGORITHM_ID,
            "algorithm_version": APPLICATION_ALGORITHM_VERSION,
            "view_schema": VIEW_SCHEMA,
            "presentation_semantics": "READ_ONLY_PROJECTION_OF_RELEASED_BAZI_FACTS",
            "classical_interaction_semantics": "NOT_INCLUDED",
            "prediction_semantics": "NOT_INCLUDED",
        }
        for field, value in expected.items():
            if getattr(self, field) != value:
                raise ValueError(
                    f"unsupported Bazi application {field}: {getattr(self, field)!r}"
                )
        return self


def bazi_local_application_v1_profile() -> BaziApplicationProfile:
    return BaziApplicationProfile()

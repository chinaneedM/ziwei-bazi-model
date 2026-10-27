from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart import PresentationProfile


ZIWEI_APPLICATION_V1_PROFILE_ID = "ZIWEI-APPLICATION-V1"
ZIWEI_APPLICATION_V1_PROFILE_VERSION = "1.0.0"
ZIWEI_APPLICATION_SERVICE_ALGORITHM_ID = "ZIWEI-APPLICATION-ORCHESTRATOR-V1"
ZIWEI_APPLICATION_SERVICE_ALGORITHM_VERSION = "1.0.0"
ZIWEI_APPLICATION_BUNDLE_HASH_ALGORITHM_ID = "ZIWEI-APPLICATION-BUNDLE-HASH-V1"
ZIWEI_APPLICATION_BUNDLE_HASH_ALGORITHM_VERSION = "1.0.0"
ZIWEI_APPLICATION_DEFAULT_PRESENTATION_PROFILE_ID = "ZIWEI-APPLICATION-V1-DEFAULT-VIEW"
ZIWEI_APPLICATION_DEFAULT_PRESENTATION_PROFILE_VERSION = "1.0.0"


@dataclass(frozen=True)
class ZiweiApplicationProfile:
    profile_id: str = ZIWEI_APPLICATION_V1_PROFILE_ID
    profile_version: str = ZIWEI_APPLICATION_V1_PROFILE_VERSION
    service_algorithm_id: str = ZIWEI_APPLICATION_SERVICE_ALGORITHM_ID
    service_algorithm_version: str = ZIWEI_APPLICATION_SERVICE_ALGORITHM_VERSION
    bundle_hash_algorithm_id: str = ZIWEI_APPLICATION_BUNDLE_HASH_ALGORITHM_ID
    bundle_hash_algorithm_version: str = ZIWEI_APPLICATION_BUNDLE_HASH_ALGORITHM_VERSION

    def validate(self) -> "ZiweiApplicationProfile":
        expected = {
            "profile_id": ZIWEI_APPLICATION_V1_PROFILE_ID,
            "profile_version": ZIWEI_APPLICATION_V1_PROFILE_VERSION,
            "service_algorithm_id": ZIWEI_APPLICATION_SERVICE_ALGORITHM_ID,
            "service_algorithm_version": ZIWEI_APPLICATION_SERVICE_ALGORITHM_VERSION,
            "bundle_hash_algorithm_id": ZIWEI_APPLICATION_BUNDLE_HASH_ALGORITHM_ID,
            "bundle_hash_algorithm_version": ZIWEI_APPLICATION_BUNDLE_HASH_ALGORITHM_VERSION,
        }
        for field_name, expected_value in expected.items():
            actual = getattr(self, field_name)
            if actual != expected_value:
                raise ValueError(f"unsupported {field_name}: {actual}")
        return self


def ziwei_application_v1_profile() -> ZiweiApplicationProfile:
    return ZiweiApplicationProfile().validate()


def ziwei_application_default_presentation_profile() -> PresentationProfile:
    return PresentationProfile(
        profile_id=ZIWEI_APPLICATION_DEFAULT_PRESENTATION_PROFILE_ID,
        profile_version=ZIWEI_APPLICATION_DEFAULT_PRESENTATION_PROFILE_VERSION,
    ).validate()

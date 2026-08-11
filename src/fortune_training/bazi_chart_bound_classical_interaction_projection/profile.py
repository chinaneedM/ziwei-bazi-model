from __future__ import annotations

from dataclasses import dataclass


PROJECTION_PROFILE_ID = "BAZI-CHART-BOUND-CLASSICAL-INTERACTION-PROJECTION-FOUNDATION-R1"
PROJECTION_PROFILE_VERSION = "1.0.0"
PROJECTION_ALGORITHM_ID = "BAZI-CHART-BOUND-SOURCE-INTERACTION-CLAIM-PROJECTION-R1"
PROJECTION_ALGORITHM_VERSION = "1.0.0"
SCOPE_RULE_SET_ID = "BAZI-CLASSICAL-INTERACTION-SOURCE-SCOPE-SPECIFICATION-R1"
SCOPE_RULE_SET_VERSION = "1.0.0"
OBSERVATION_RULE_SET_ID = "BAZI-BINDING-SCOPED-NEUTRAL-OBSERVATION-R1"
OBSERVATION_RULE_SET_VERSION = "1.0.0"
CLAIM_PROJECTION_RULE_SET_ID = "BAZI-CHART-BOUND-SOURCE-INTERACTION-CLAIM-BUNDLE-PROJECTION-R1"
CLAIM_PROJECTION_RULE_SET_VERSION = "1.0.0"

EXPECTED_GRAPH_FILE_SHA256 = "cf580bca30f8aaed0b8d1e2fb60a7bb96789c44cb2adae3155bf463214fcde21"
EXPECTED_GRAPH_ARTIFACT_SEMANTICS_SHA256 = "837835ec60c2baabffaff2ba730e71e73e803b4f4c49cc582c87ebf03e3af7a4"
EXPECTED_GRAPH_RECORD_HASH_CHAIN_SHA256 = "040df8fcd40b11b0019f837e41ab15dafe6c5fe81ff553e457f2ca2bd1e93c6b"
EXPECTED_MATRIX_FILE_SHA256 = "50da1ae51b8838ba29520cf114ccb963f34a1ef8b8011a6593be25a48a95eacd"
EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256 = "6d9f4cdc4b44b1b6a78f892690ededea9be1e40f436638d8f5f54b6d3e9cb906"
EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256 = "f32c55a88e8699268ba04fadc0e6f07e26ef79caafe9c75a51f87fd1460d4672"
EXPECTED_BINDABILITY_PLAN_SEMANTICS_SHA256 = "494bf7164fe1e19c56cf1d4e82cd362edfb30bbba8a90f1461833faff6c8bcff"


@dataclass(frozen=True)
class ResolvedBaziChartBoundClassicalInteractionProjectionProfile:
    profile_id: str = PROJECTION_PROFILE_ID
    profile_version: str = PROJECTION_PROFILE_VERSION
    algorithm_id: str = PROJECTION_ALGORITHM_ID
    algorithm_version: str = PROJECTION_ALGORITHM_VERSION
    scope_rule_set_id: str = SCOPE_RULE_SET_ID
    scope_rule_set_version: str = SCOPE_RULE_SET_VERSION
    observation_rule_set_id: str = OBSERVATION_RULE_SET_ID
    observation_rule_set_version: str = OBSERVATION_RULE_SET_VERSION
    claim_projection_rule_set_id: str = CLAIM_PROJECTION_RULE_SET_ID
    claim_projection_rule_set_version: str = CLAIM_PROJECTION_RULE_SET_VERSION
    graph_artifact_semantics_sha256: str = EXPECTED_GRAPH_ARTIFACT_SEMANTICS_SHA256
    graph_record_hash_chain_sha256: str = EXPECTED_GRAPH_RECORD_HASH_CHAIN_SHA256
    matrix_artifact_semantics_sha256: str = EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256
    matrix_record_hash_chain_sha256: str = EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256
    bindability_plan_semantics_sha256: str = EXPECTED_BINDABILITY_PLAN_SEMANTICS_SHA256

    def validate(self) -> "ResolvedBaziChartBoundClassicalInteractionProjectionProfile":
        if self != ResolvedBaziChartBoundClassicalInteractionProjectionProfile():
            raise ValueError(f"unsupported chart-bound Classical interaction projection profile: {self!r}")
        return self


def bazi_chart_bound_classical_interaction_projection_foundation_r1_profile(
) -> ResolvedBaziChartBoundClassicalInteractionProjectionProfile:
    return ResolvedBaziChartBoundClassicalInteractionProjectionProfile()

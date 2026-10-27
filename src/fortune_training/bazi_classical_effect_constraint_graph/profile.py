from __future__ import annotations

from dataclasses import dataclass

from fortune_training.bazi_chart_bound_classical_interaction_projection.profile import (
    EXPECTED_GRAPH_ARTIFACT_SEMANTICS_SHA256,
    EXPECTED_GRAPH_RECORD_HASH_CHAIN_SHA256,
    PROJECTION_PROFILE_ID,
    PROJECTION_PROFILE_VERSION,
)


PROFILE_ID = "BAZI-CLASSICAL-EFFECT-CONSTRAINT-GRAPH-FACTORIZED-COMPOSITION-R1"
PROFILE_VERSION = "1.0.0"
GRAPH_ALGORITHM_ID = "BAZI-CLASSICAL-EFFECT-CONSTRAINT-GRAPH-PROJECTION-R1"
GRAPH_ALGORITHM_VERSION = "1.0.0"
COMPOSITION_ALGORITHM_ID = "BAZI-CLASSICAL-EFFECT-FRAGMENT-FACTORIZED-COMPOSITION-R1"
COMPOSITION_ALGORITHM_VERSION = "1.0.0"
EXPECTED_SOURCE_SCOPE_SEMANTICS_SHA256 = "949009f0521f3d8710e9f11c1341d0961324f1d6b4f197eeeeb8c25279f2daec"

EFFECT_FACETS = (
    "RELATION_EFFECT_DISPOSITION",
    "RELATION_EFFECT_GRADE",
    "RELATION_PARTICIPANT_ALLOCATION",
)
GRAPH_NODE_CLASSES = (
    "RawRelationReferenceNode",
    "ClassicalEffectFacetChannelNode",
    "ClassicalEffectConstraintNode",
)
GRAPH_EDGE_CLASSES = (
    "RAW_RELATION_ACTOR_REFERENCE",
    "CONSTRAINT_TARGETS_EFFECT_CHANNEL",
    "EFFECT_CHANNEL_REFERENCES_RAW_RELATION",
    "SOURCE_NARRATIVE_PRECEDES",
)
SOURCE_CLAIM_TO_EFFECT_FACET = {
    "SOURCE_ASSERTED_RESOLUTION": "RELATION_EFFECT_DISPOSITION",
    "SOURCE_ASSERTED_RESOLUTION_FAILURE": "RELATION_EFFECT_DISPOSITION",
    "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE": "RELATION_EFFECT_DISPOSITION",
    "SOURCE_ASSERTED_ATTENUATION": "RELATION_EFFECT_GRADE",
    "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION": "RELATION_PARTICIPANT_ALLOCATION",
}
HARD_EXCLUDED_EDGE_OR_STATE_SEMANTICS = (
    "SUPPRESSES",
    "ACTIVATES",
    "DEACTIVATES",
    "RELEASES",
    "CANCELS",
    "OVERRIDES",
    "NEGATES",
    "DEFEATS",
    "WINS_OVER",
    "LOSES_TO",
    "SELECTS_PARTICIPANT",
    "SELECTS_PATH",
    "HAS_PRIORITY_OVER",
    "TRANSITIONS_TO",
    "CAUSES_STATE_CHANGE",
    "CONFLICTS_WITH",
)


@dataclass(frozen=True)
class ResolvedBaziClassicalEffectConstraintGraphProfile:
    profile_id: str = PROFILE_ID
    profile_version: str = PROFILE_VERSION
    graph_algorithm_id: str = GRAPH_ALGORITHM_ID
    graph_algorithm_version: str = GRAPH_ALGORITHM_VERSION
    composition_algorithm_id: str = COMPOSITION_ALGORITHM_ID
    composition_algorithm_version: str = COMPOSITION_ALGORITHM_VERSION
    upstream_projection_profile_id: str = PROJECTION_PROFILE_ID
    upstream_projection_profile_version: str = PROJECTION_PROFILE_VERSION
    source_graph_artifact_semantics_sha256: str = EXPECTED_GRAPH_ARTIFACT_SEMANTICS_SHA256
    source_graph_record_hash_chain_sha256: str = EXPECTED_GRAPH_RECORD_HASH_CHAIN_SHA256
    source_scope_semantics_sha256: str = EXPECTED_SOURCE_SCOPE_SEMANTICS_SHA256

    def validate(self) -> "ResolvedBaziClassicalEffectConstraintGraphProfile":
        if self != ResolvedBaziClassicalEffectConstraintGraphProfile():
            raise ValueError(f"unsupported Classical effect constraint graph profile: {self!r}")
        return self


def bazi_classical_effect_constraint_graph_factorized_composition_r1_profile(
) -> ResolvedBaziClassicalEffectConstraintGraphProfile:
    return ResolvedBaziClassicalEffectConstraintGraphProfile()

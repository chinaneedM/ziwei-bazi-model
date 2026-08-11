from __future__ import annotations

from dataclasses import dataclass


BINDING_PROFILE_ID = "BAZI-CHART-SPECIFIC-EXACT-SOURCE-PATTERN-BINDING-CANDIDATES-R1"
BINDING_PROFILE_VERSION = "1.0.0"
BINDING_ALGORITHM_ID = "BAZI-CHART-SOURCE-PATTERN-EXACT-BINDING-ENUMERATOR-R1"
BINDING_ALGORITHM_VERSION = "1.0.0"
BINDABILITY_RULE_SET_ID = "BAZI-SOURCE-GRAPH-BINDABILITY-PLAN-R1"
BINDABILITY_RULE_SET_VERSION = "1.0.0"
LINEAGE_RULE_SET_ID = "BAZI-SOURCE-PATTERN-BINDING-LINEAGE-R1"
LINEAGE_RULE_SET_VERSION = "1.0.0"
EXCHANGEABILITY_ALGORITHM_ID = "BAZI-SOURCE-SLOT-EXCHANGEABILITY-CANONICALIZATION-R1"
EXCHANGEABILITY_ALGORITHM_VERSION = "1.0.0"
GRAPH_ARTIFACT_SEMANTICS_SHA256 = "837835ec60c2baabffaff2ba730e71e73e803b4f4c49cc582c87ebf03e3af7a4"
GRAPH_RECORD_HASH_CHAIN_SHA256 = "040df8fcd40b11b0019f837e41ab15dafe6c5fe81ff553e457f2ca2bd1e93c6b"


@dataclass(frozen=True)
class ResolvedBaziChartSourcePatternBindingProfile:
    profile_id: str = BINDING_PROFILE_ID
    profile_version: str = BINDING_PROFILE_VERSION
    algorithm_id: str = BINDING_ALGORITHM_ID
    algorithm_version: str = BINDING_ALGORITHM_VERSION
    bindability_rule_set_id: str = BINDABILITY_RULE_SET_ID
    bindability_rule_set_version: str = BINDABILITY_RULE_SET_VERSION
    lineage_rule_set_id: str = LINEAGE_RULE_SET_ID
    lineage_rule_set_version: str = LINEAGE_RULE_SET_VERSION
    exchangeability_algorithm_id: str = EXCHANGEABILITY_ALGORITHM_ID
    exchangeability_algorithm_version: str = EXCHANGEABILITY_ALGORITHM_VERSION
    graph_artifact_semantics_sha256: str = GRAPH_ARTIFACT_SEMANTICS_SHA256
    graph_record_hash_chain_sha256: str = GRAPH_RECORD_HASH_CHAIN_SHA256

    def validate(self) -> "ResolvedBaziChartSourcePatternBindingProfile":
        if self != ResolvedBaziChartSourcePatternBindingProfile():
            raise ValueError(f"unsupported chart source-pattern binding profile: {self!r}")
        return self


def bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile(
) -> ResolvedBaziChartSourcePatternBindingProfile:
    return ResolvedBaziChartSourcePatternBindingProfile()

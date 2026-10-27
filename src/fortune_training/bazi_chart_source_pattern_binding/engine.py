from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from fortune_training.bazi_branch_relation_positional import (
    BaziBranchRelationPositionalCandidate,
    bazi_branch_relation_positional_context_foundation_r1_profile,
    branch_relation_positional_hash_bundle,
)
from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceCandidate
from fortune_training.bazi_stem_relation_positional import (
    BaziStemRelationPositionalCandidate,
    bazi_stem_relation_positional_context_foundation_r1_profile,
    stem_relation_positional_hash_bundle,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .bindability import BindingPlanError, derive_bindability_plan
from .enumeration import enumerate_graph_inventory
from .integrity import (
    binding_hash_bundle,
    binding_snapshot_fact_payload,
    validate_outer_candidate,
)
from .models import (
    BaziChartSourcePatternBindingResolution,
    ChartSourcePatternBindingOuterCandidate,
    ChartSourcePatternBindingSnapshot,
)
from .profile import (
    BINDABILITY_RULE_SET_ID,
    BINDABILITY_RULE_SET_VERSION,
    ResolvedBaziChartSourcePatternBindingProfile,
)


class BaziChartSourcePatternBindingGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziChartSourcePatternBindingRequest:
    natal_candidate: BaziChartCandidate
    incidence_candidates: tuple[BaziRelationIncidenceCandidate, ...]
    branch_positional_candidates: tuple[BaziBranchRelationPositionalCandidate, ...]
    stem_positional_candidates: tuple[BaziStemRelationPositionalCandidate, ...]
    source_graph: dict[str, Any]
    binding_profile: ResolvedBaziChartSourcePatternBindingProfile


def _group_incidence(
    candidates: tuple[BaziRelationIncidenceCandidate, ...],
) -> tuple[tuple[tuple[str, str], tuple[int, ...], BaziRelationIncidenceCandidate], ...]:
    if not candidates:
        raise BaziChartSourcePatternBindingGenerationError("NO_INCIDENCE_CANDIDATES", "incidence")
    groups: dict[tuple[str, str], tuple[list[int], BaziRelationIncidenceCandidate]] = {}
    for index, candidate in enumerate(candidates):
        if candidate.integrity.status != "PASS":
            raise BaziChartSourcePatternBindingGenerationError("UPSTREAM_INCIDENCE_INTEGRITY_FAILED", str(index))
        key = (candidate.hashes.fact_hash, candidate.hashes.computation_hash)
        if key not in groups:
            groups[key] = ([index], candidate)
        else:
            indices, first = groups[key]
            if candidate != first:
                raise BaziChartSourcePatternBindingGenerationError("INCIDENCE_COMPLETE_CONTRACT_COLLISION", candidate.hashes.fact_hash)
            indices.append(index)
    return tuple((key, tuple(groups[key][0]), groups[key][1]) for key in sorted(groups))


def _same_lineage(
    candidate: Any,
    incidence: BaziRelationIncidenceCandidate,
    incidence_indices: tuple[int, ...],
) -> bool:
    snapshot = candidate.context.snapshot
    return (
        candidate.source_incidence_candidate_indices == incidence_indices
        and candidate.source_flow_candidate_indices == incidence.source_flow_candidate_indices
        and candidate.source_structural_candidate_indices == incidence.source_structural_candidate_indices
        and candidate.source_support_candidate_indices == incidence.source_support_candidate_indices
        and candidate.source_temporal_candidate_indices == incidence.source_temporal_candidate_indices
        and candidate.source_temporal_seed_ids == incidence.source_temporal_seed_ids
        and candidate.source_incidence_lineage_binding_keys == incidence.lineage_binding_keys
        and snapshot.source_incidence_snapshot_id == incidence.context.snapshot.snapshot_id
        and snapshot.source_incidence_snapshot_fact_hash == incidence.context.snapshot.snapshot_fact_hash
        and snapshot.source_incidence_fact_hash == incidence.hashes.fact_hash
        and snapshot.source_incidence_computation_hash == incidence.hashes.computation_hash
        and snapshot.target_utc == incidence.context.snapshot.target_utc
    )


def _exact_join(
    candidates: tuple[Any, ...],
    incidence: BaziRelationIncidenceCandidate,
    incidence_indices: tuple[int, ...],
    label: str,
) -> tuple[int, Any]:
    matches = tuple(
        (index, candidate) for index, candidate in enumerate(candidates)
        if _same_lineage(candidate, incidence, incidence_indices)
    )
    if len(matches) != 1:
        raise BaziChartSourcePatternBindingGenerationError(
            f"{label}_POSITIONAL_EXACT_JOIN_CARDINALITY_MISMATCH", str(tuple(index for index, _ in matches))
        )
    index, candidate = matches[0]
    if candidate.integrity.status != "PASS":
        raise BaziChartSourcePatternBindingGenerationError(f"UPSTREAM_{label}_POSITIONAL_INTEGRITY_FAILED", str(index))
    if label == "BRANCH":
        replayed_hashes = branch_relation_positional_hash_bundle(
            candidate.context, incidence, candidate.source_incidence_candidate_indices,
            candidate.source_flow_candidate_indices, candidate.source_structural_candidate_indices,
            candidate.source_support_candidate_indices, candidate.source_temporal_candidate_indices,
            candidate.source_temporal_seed_ids, candidate.source_incidence_lineage_binding_keys,
            candidate.lineage_binding_keys,
            bazi_branch_relation_positional_context_foundation_r1_profile(),
        )
    else:
        replayed_hashes = stem_relation_positional_hash_bundle(
            candidate.context, incidence, candidate.source_incidence_candidate_indices,
            candidate.source_flow_candidate_indices, candidate.source_structural_candidate_indices,
            candidate.source_support_candidate_indices, candidate.source_temporal_candidate_indices,
            candidate.source_temporal_seed_ids, candidate.source_incidence_lineage_binding_keys,
            candidate.lineage_binding_keys,
            bazi_stem_relation_positional_context_foundation_r1_profile(),
        )
    if replayed_hashes != candidate.hashes:
        raise BaziChartSourcePatternBindingGenerationError(f"UPSTREAM_{label}_POSITIONAL_HASH_REPLAY_MISMATCH", str(index))
    return index, candidate


def _snapshot(
    request: BaziChartSourcePatternBindingRequest,
    incidence: BaziRelationIncidenceCandidate,
    branch: BaziBranchRelationPositionalCandidate,
    stem: BaziStemRelationPositionalCandidate,
) -> ChartSourcePatternBindingSnapshot:
    source = incidence.context.snapshot
    provisional = ChartSourcePatternBindingSnapshot(
        snapshot_id="",
        snapshot_fact_hash="",
        target_utc=source.target_utc,
        source_graph_artifact_semantics_sha256=request.binding_profile.graph_artifact_semantics_sha256,
        source_graph_record_hash_chain_sha256=request.binding_profile.graph_record_hash_chain_sha256,
        source_natal_fact_hash=request.natal_candidate.hashes.fact_hash,
        source_natal_computation_hash=request.natal_candidate.hashes.computation_hash,
        source_incidence_snapshot_id=source.snapshot_id,
        source_incidence_snapshot_fact_hash=source.snapshot_fact_hash,
        source_incidence_fact_hash=incidence.hashes.fact_hash,
        source_incidence_computation_hash=incidence.hashes.computation_hash,
        source_branch_positional_snapshot_id=branch.context.snapshot.snapshot_id,
        source_branch_positional_fact_hash=branch.hashes.fact_hash,
        source_branch_positional_computation_hash=branch.hashes.computation_hash,
        source_stem_positional_snapshot_id=stem.context.snapshot.snapshot_id,
        source_stem_positional_fact_hash=stem.hashes.fact_hash,
        source_stem_positional_computation_hash=stem.hashes.computation_hash,
        profile_id=request.binding_profile.profile_id,
        profile_version=request.binding_profile.profile_version,
        rule_set_id=BINDABILITY_RULE_SET_ID,
        rule_set_version=BINDABILITY_RULE_SET_VERSION,
    )
    digest = object_sha256(binding_snapshot_fact_payload(provisional))
    return replace(
        provisional,
        snapshot_id=f"CHART_SOURCE_PATTERN_BINDING_SNAPSHOT:{digest}",
        snapshot_fact_hash=digest,
    )


class BaziChartSourcePatternBindingEngine:
    schema = "BAZI-CHART-SPECIFIC-EXACT-SOURCE-PATTERN-BINDING-CANDIDATES-RESULT-R1"
    typed_schema = "BAZI-CHART-SPECIFIC-EXACT-SOURCE-PATTERN-BINDING-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziChartSourcePatternBindingRequest,
    ) -> BaziChartSourcePatternBindingResolution:
        try:
            request.binding_profile.validate()
            plan = derive_bindability_plan(request.source_graph, request.binding_profile)
            if request.natal_candidate.integrity.status != "PASS":
                raise BaziChartSourcePatternBindingGenerationError("UPSTREAM_NATAL_INTEGRITY_FAILED", "natal")
            rows: list[ChartSourcePatternBindingOuterCandidate] = []
            for _, incidence_indices, incidence in _group_incidence(request.incidence_candidates):
                if incidence.context.snapshot.upstream_natal_fact_hash != request.natal_candidate.hashes.fact_hash:
                    raise BaziChartSourcePatternBindingGenerationError("INCIDENCE_NATAL_LINEAGE_MISMATCH", incidence.hashes.fact_hash)
                branch_index, branch = _exact_join(request.branch_positional_candidates, incidence, incidence_indices, "BRANCH")
                stem_index, stem = _exact_join(request.stem_positional_candidates, incidence, incidence_indices, "STEM")
                if branch.context.snapshot.source_natal_computation_hash != request.natal_candidate.hashes.computation_hash or stem.context.snapshot.source_natal_computation_hash != request.natal_candidate.hashes.computation_hash:
                    raise BaziChartSourcePatternBindingGenerationError("POSITIONAL_NATAL_COMPUTATION_LINEAGE_MISMATCH", incidence.hashes.fact_hash)
                snapshot = _snapshot(request, incidence, branch, stem)
                inventories = enumerate_graph_inventory(
                    request.source_graph, plan, request.natal_candidate, incidence, branch, stem
                )
                lineage_keys = (
                    f"INCIDENCE_FACT:{incidence.hashes.fact_hash}",
                    f"INCIDENCE_COMPUTATION:{incidence.hashes.computation_hash}",
                    *(f"INCIDENCE_CANDIDATE_INDEX:{value}" for value in incidence_indices),
                    f"BRANCH_POSITIONAL_CANDIDATE_INDEX:{branch_index}",
                    f"BRANCH_POSITIONAL_FACT:{branch.hashes.fact_hash}",
                    f"BRANCH_POSITIONAL_COMPUTATION:{branch.hashes.computation_hash}",
                    f"STEM_POSITIONAL_CANDIDATE_INDEX:{stem_index}",
                    f"STEM_POSITIONAL_FACT:{stem.hashes.fact_hash}",
                    f"STEM_POSITIONAL_COMPUTATION:{stem.hashes.computation_hash}",
                    *incidence.lineage_binding_keys,
                )
                hashes = binding_hash_bundle(
                    snapshot, inventories, incidence_indices, branch_index, stem_index,
                    incidence.source_flow_candidate_indices, incidence.source_structural_candidate_indices,
                    incidence.source_support_candidate_indices, incidence.source_temporal_candidate_indices,
                    incidence.source_temporal_seed_ids, incidence.lineage_binding_keys,
                    lineage_keys, request.binding_profile,
                )
                integrity = validate_outer_candidate(
                    snapshot, inventories, plan, request.natal_candidate, incidence, branch, stem,
                    incidence_indices, branch_index, stem_index,
                    incidence.source_flow_candidate_indices, incidence.source_structural_candidate_indices,
                    incidence.source_support_candidate_indices, incidence.source_temporal_candidate_indices,
                    incidence.source_temporal_seed_ids, incidence.lineage_binding_keys,
                    lineage_keys, request.binding_profile, hashes,
                )
                if integrity.status != "PASS":
                    return BaziChartSourcePatternBindingResolution(
                        self.typed_schema, "FAILED", plan, (), (),
                        tuple(f"INTEGRITY:{value.code}:{value.path}" for value in integrity.diagnostics),
                    )
                rows.append(ChartSourcePatternBindingOuterCandidate(
                    incidence_indices, branch_index, stem_index,
                    incidence.source_flow_candidate_indices, incidence.source_structural_candidate_indices,
                    incidence.source_support_candidate_indices, incidence.source_temporal_candidate_indices,
                    incidence.source_temporal_seed_ids, incidence.lineage_binding_keys, lineage_keys,
                    snapshot, inventories,
                    {
                        "binding": request.binding_profile.algorithm_version,
                        "bindability": request.binding_profile.bindability_rule_set_version,
                        "lineage": request.binding_profile.lineage_rule_set_version,
                        "exchangeability": request.binding_profile.exchangeability_algorithm_version,
                    },
                    integrity, hashes,
                ))
            candidates = tuple(rows)
            return BaziChartSourcePatternBindingResolution(
                self.typed_schema,
                "RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                plan,
                candidates,
                ("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",) if len(candidates) > 1 else (),
                (),
            )
        except (BindingPlanError, BaziChartSourcePatternBindingGenerationError, ValueError, KeyError) as exc:
            code = getattr(exc, "diagnostic_code", "BINDING_GENERATION_FAILED")
            return BaziChartSourcePatternBindingResolution(self.typed_schema, "FAILED", (), (), (), (f"{code}:{exc}",))

    def resolve(self, request: BaziChartSourcePatternBindingRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "binding_profile": json_value(request.binding_profile),
            "bindability_plan": json_value(typed.bindability_plan),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }


def validate_binding_resolution_replay(
    request: BaziChartSourcePatternBindingRequest,
    expected: BaziChartSourcePatternBindingResolution,
) -> bool:
    """Reconstruct the complete enumeration and compare every lineage/fact/hash field."""
    return BaziChartSourcePatternBindingEngine().resolve_typed(request) == expected

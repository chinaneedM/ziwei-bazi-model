from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_structural import (
    BaziStructuralCandidate,
    bazi_structural_context_r1_profile,
    structural_hash_bundle,
    validate_structural_context,
)
from fortune_training.bazi_structural_support import (
    BaziStructuralSupportCandidate,
    bazi_structural_support_foundation_r1_profile,
    structural_support_hash_bundle,
    validate_structural_support_context,
)
from fortune_training.calendar_foundation.models import json_value

from .generation import (
    RelationIncidenceSnapshotInputs,
    build_relation_incidence_context,
)
from .models import (
    BaziRelationIncidenceCandidate,
    BaziRelationIncidenceResolution,
)
from .profile import ResolvedBaziRelationIncidenceProfile


class BaziRelationIncidenceGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziRelationIncidenceRequest:
    natal_candidate: BaziChartCandidate
    target_utc: datetime
    flow_candidates: tuple[BaziFlowCandidate, ...]
    structural_candidates: tuple[BaziStructuralCandidate, ...]
    support_candidates: tuple[BaziStructuralSupportCandidate, ...]
    incidence_profile: ResolvedBaziRelationIncidenceProfile


@dataclass(frozen=True)
class _ValidatedSupportLineage:
    flow_indices: tuple[int, ...]
    structural_indices: tuple[int, ...]
    temporal_indices: tuple[int, ...]
    seed_ids: tuple[str, ...]
    flow: BaziFlowCandidate
    structural: BaziStructuralCandidate


def _candidate_indices(values, label: str) -> tuple[int, ...]:
    if not values:
        raise BaziRelationIncidenceGenerationError(
            f"{label}_LINEAGE_MISSING", label
        )
    if any(type(index) is not int or index < 0 for index in values):
        raise BaziRelationIncidenceGenerationError(
            f"{label}_LINEAGE_INDEX_INVALID", str(values)
        )
    if len(values) != len(set(values)):
        raise BaziRelationIncidenceGenerationError(
            f"{label}_LINEAGE_INDEX_DUPLICATE", str(values)
        )
    return tuple(sorted(values))


def _seed_ids(values, label: str) -> tuple[str, ...]:
    if not values or any(not isinstance(value, str) or not value for value in values):
        raise BaziRelationIncidenceGenerationError(
            f"{label}_LINEAGE_MISSING", str(values)
        )
    if len(values) != len(set(values)):
        raise BaziRelationIncidenceGenerationError(
            f"{label}_LINEAGE_DUPLICATE", str(values)
        )
    return tuple(sorted(values))


def _candidate_at(rows, index: int, label: str):
    if index >= len(rows):
        raise BaziRelationIncidenceGenerationError(
            f"{label}_LINEAGE_INDEX_OUT_OF_RANGE", str(index)
        )
    return rows[index]


def _validate_structural_lineage(
    natal: BaziChartCandidate,
    expected_target: datetime,
    flows: tuple[BaziFlowCandidate, ...],
    structural: BaziStructuralCandidate,
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[str, ...]]:
    if structural.integrity.status != "PASS":
        raise BaziRelationIncidenceGenerationError(
            "UPSTREAM_STRUCTURAL_INTEGRITY_FAILED", structural.hashes.fact_hash
        )
    flow_indices = _candidate_indices(
        structural.source_flow_candidate_indices, "STRUCTURAL_FLOW_CANDIDATE"
    )
    temporal_indices: set[int] = set()
    seed_ids: set[str] = set()
    first_flow_hashes = None
    structural_profile = bazi_structural_context_r1_profile()
    for flow_index in flow_indices:
        flow = _candidate_at(flows, flow_index, "STRUCTURAL_FLOW_CANDIDATE")
        if flow.integrity.status != "PASS":
            raise BaziRelationIncidenceGenerationError(
                "UPSTREAM_FLOW_INTEGRITY_FAILED", flow.hashes.fact_hash
            )
        if flow.context.target_utc.astimezone(timezone.utc) != expected_target:
            raise BaziRelationIncidenceGenerationError(
                "TARGET_FLOW_MISMATCH", flow.context.target_utc.isoformat()
            )
        if flow.context.upstream_natal_fact_hash != natal.hashes.fact_hash:
            raise BaziRelationIncidenceGenerationError(
                "FLOW_NATAL_LINEAGE_MISMATCH", flow.context.upstream_natal_fact_hash
            )
        if structural.context.upstream_flow_fact_hash != flow.hashes.fact_hash:
            raise BaziRelationIncidenceGenerationError(
                "STRUCTURAL_FLOW_FACT_LINEAGE_MISMATCH", str(flow_index)
            )
        if first_flow_hashes is None:
            first_flow_hashes = flow.hashes
        elif flow.hashes != first_flow_hashes:
            raise BaziRelationIncidenceGenerationError(
                "STRUCTURAL_FLOW_COMPLETE_CONTRACT_MISMATCH", str(flow_index)
            )
        expected_hashes = structural_hash_bundle(
            structural.context, natal, flow, structural_profile
        )
        expected_integrity = validate_structural_context(
            structural.context,
            natal,
            flow,
            structural_profile,
            structural.hashes,
        )
        if structural.hashes != expected_hashes or expected_integrity.status != "PASS":
            raise BaziRelationIncidenceGenerationError(
                "STRUCTURAL_FLOW_COMPUTATION_LINEAGE_MISMATCH", str(flow_index)
            )
        temporal_indices.update(
            _candidate_indices(
                flow.source_temporal_candidate_indices,
                "FLOW_TEMPORAL_CANDIDATE",
            )
        )
        seed_ids.update(_seed_ids(flow.source_temporal_seed_ids, "FLOW_TEMPORAL_SEED"))

    expected_temporal_indices = _candidate_indices(
        structural.source_temporal_candidate_indices,
        "STRUCTURAL_TEMPORAL_CANDIDATE",
    )
    expected_seed_ids = _seed_ids(
        structural.source_temporal_seed_ids, "STRUCTURAL_TEMPORAL_SEED"
    )
    if expected_temporal_indices != tuple(sorted(temporal_indices)):
        raise BaziRelationIncidenceGenerationError(
            "STRUCTURAL_TEMPORAL_CANDIDATE_LINEAGE_MISMATCH",
            structural.hashes.fact_hash,
        )
    if expected_seed_ids != tuple(sorted(seed_ids)):
        raise BaziRelationIncidenceGenerationError(
            "STRUCTURAL_TEMPORAL_SEED_LINEAGE_MISMATCH",
            structural.hashes.fact_hash,
        )
    return flow_indices, expected_temporal_indices, expected_seed_ids


def _validated_support_lineage(
    natal: BaziChartCandidate,
    target_utc: datetime,
    flows: tuple[BaziFlowCandidate, ...],
    structurals: tuple[BaziStructuralCandidate, ...],
    supports: tuple[BaziStructuralSupportCandidate, ...],
    support_index: int,
) -> _ValidatedSupportLineage:
    support = _candidate_at(supports, support_index, "SUPPORT_CANDIDATE")
    if support.integrity.status != "PASS":
        raise BaziRelationIncidenceGenerationError(
            "UPSTREAM_SUPPORT_INTEGRITY_FAILED", support.hashes.fact_hash
        )
    structural_indices = _candidate_indices(
        support.source_structural_candidate_indices,
        "SUPPORT_STRUCTURAL_CANDIDATE",
    )
    support_flow_indices = _candidate_indices(
        support.source_flow_candidate_indices, "SUPPORT_FLOW_CANDIDATE"
    )
    support_temporal_indices = _candidate_indices(
        support.source_temporal_candidate_indices,
        "SUPPORT_TEMPORAL_CANDIDATE",
    )
    support_seed_ids = _seed_ids(
        support.source_temporal_seed_ids, "SUPPORT_TEMPORAL_SEED"
    )
    expected_target = target_utc.astimezone(timezone.utc)
    all_flow_indices: set[int] = set()
    all_temporal_indices: set[int] = set()
    all_seed_ids: set[str] = set()
    first_structural = None
    first_structural_hashes = None
    support_profile = bazi_structural_support_foundation_r1_profile()
    for structural_index in structural_indices:
        structural = _candidate_at(
            structurals, structural_index, "SUPPORT_STRUCTURAL_CANDIDATE"
        )
        flow_indices, temporal_indices, seed_ids = _validate_structural_lineage(
            natal, expected_target, flows, structural
        )
        if (
            structural.context.upstream_natal_fact_hash != natal.hashes.fact_hash
            or support.context.upstream_structural_fact_hash
            != structural.hashes.fact_hash
        ):
            raise BaziRelationIncidenceGenerationError(
                "SUPPORT_STRUCTURAL_FACT_LINEAGE_MISMATCH", str(structural_index)
            )
        if first_structural is None:
            first_structural = structural
            first_structural_hashes = structural.hashes
        elif structural.hashes != first_structural_hashes:
            raise BaziRelationIncidenceGenerationError(
                "SUPPORT_STRUCTURAL_COMPLETE_CONTRACT_MISMATCH",
                str(structural_index),
            )
        all_flow_indices.update(flow_indices)
        all_temporal_indices.update(temporal_indices)
        all_seed_ids.update(seed_ids)

        flow = _candidate_at(flows, flow_indices[0], "SUPPORT_FLOW_CANDIDATE")
        expected_hashes = structural_support_hash_bundle(
            support.context, natal, flow, structural, support_profile
        )
        expected_integrity = validate_structural_support_context(
            support.context,
            natal,
            flow,
            structural,
            support_profile,
            support.hashes,
        )
        if support.hashes != expected_hashes or expected_integrity.status != "PASS":
            raise BaziRelationIncidenceGenerationError(
                "SUPPORT_STRUCTURAL_COMPUTATION_LINEAGE_MISMATCH",
                str(structural_index),
            )

    if support_flow_indices != tuple(sorted(all_flow_indices)):
        raise BaziRelationIncidenceGenerationError(
            "SUPPORT_FLOW_CANDIDATE_LINEAGE_MISMATCH", support.hashes.fact_hash
        )
    if support_temporal_indices != tuple(sorted(all_temporal_indices)):
        raise BaziRelationIncidenceGenerationError(
            "SUPPORT_TEMPORAL_CANDIDATE_LINEAGE_MISMATCH", support.hashes.fact_hash
        )
    if support_seed_ids != tuple(sorted(all_seed_ids)):
        raise BaziRelationIncidenceGenerationError(
            "SUPPORT_TEMPORAL_SEED_LINEAGE_MISMATCH", support.hashes.fact_hash
        )
    if first_structural is None:
        raise BaziRelationIncidenceGenerationError(
            "SUPPORT_STRUCTURAL_CANDIDATE_LINEAGE_MISSING", support.hashes.fact_hash
        )
    flow = _candidate_at(flows, support_flow_indices[0], "SUPPORT_FLOW_CANDIDATE")
    if any(
        _candidate_at(flows, index, "SUPPORT_FLOW_CANDIDATE").hashes != flow.hashes
        for index in support_flow_indices
    ):
        raise BaziRelationIncidenceGenerationError(
            "SUPPORT_FLOW_COMPLETE_CONTRACT_MISMATCH", support.hashes.fact_hash
        )
    return _ValidatedSupportLineage(
        flow_indices=support_flow_indices,
        structural_indices=structural_indices,
        temporal_indices=support_temporal_indices,
        seed_ids=support_seed_ids,
        flow=flow,
        structural=first_structural,
    )


def _compatible_chains(
    natal: BaziChartCandidate,
    target_utc: datetime,
    flows: tuple[BaziFlowCandidate, ...],
    structurals: tuple[BaziStructuralCandidate, ...],
    supports: tuple[BaziStructuralSupportCandidate, ...],
) -> tuple[RelationIncidenceSnapshotInputs, ...]:
    if not flows:
        raise BaziRelationIncidenceGenerationError("NO_FLOW_CANDIDATES", "flow")
    if not structurals:
        raise BaziRelationIncidenceGenerationError(
            "NO_STRUCTURAL_CANDIDATES", "structural"
        )
    if not supports:
        raise BaziRelationIncidenceGenerationError(
            "NO_SUPPORT_CANDIDATES", "support"
        )
    grouped: dict[tuple[Any, ...], dict[str, Any]] = {}
    for support_index, support in enumerate(supports):
        lineage = _validated_support_lineage(
            natal,
            target_utc,
            flows,
            structurals,
            supports,
            support_index,
        )
        key = (
            support.hashes.fact_hash,
            support.hashes.computation_hash,
            lineage.flow_indices,
            lineage.structural_indices,
            lineage.temporal_indices,
            lineage.seed_ids,
        )
        existing = grouped.get(key)
        if existing is None:
            grouped[key] = {
                "support_indices": [support_index],
                "support": support,
                "lineage": lineage,
            }
        else:
            if (
                existing["support"].context != support.context
                or existing["support"].hashes != support.hashes
            ):
                raise BaziRelationIncidenceGenerationError(
                    "SUPPORT_COMPLETE_CONTRACT_COLLISION", support.hashes.fact_hash
                )
            existing["support_indices"].append(support_index)

    return tuple(
        RelationIncidenceSnapshotInputs(
            flow_index=row["lineage"].flow_indices[0],
            structural_index=row["lineage"].structural_indices[0],
            support_index=row["support_indices"][0],
            flow=row["lineage"].flow,
            structural=row["lineage"].structural,
            support=row["support"],
            source_flow_candidate_indices=row["lineage"].flow_indices,
            source_structural_candidate_indices=row["lineage"].structural_indices,
            source_support_candidate_indices=tuple(row["support_indices"]),
            request_flow_candidates=flows,
            request_structural_candidates=structurals,
            request_support_candidates=supports,
        )
        for row in grouped.values()
    )


def _lineage_binding_keys(chain: RelationIncidenceSnapshotInputs) -> tuple[str, ...]:
    flow_indices = chain.source_flow_candidate_indices or (chain.flow_index,)
    structural_indices = (
        chain.source_structural_candidate_indices or (chain.structural_index,)
    )
    support_indices = chain.source_support_candidate_indices or (chain.support_index,)
    return (
        f"TEMPORAL_FACT:{chain.flow.context.upstream_temporal_fact_hash}",
        f"FLOW_FACT:{chain.flow.hashes.fact_hash}",
        f"FLOW_COMPUTATION:{chain.flow.hashes.computation_hash}",
        f"STRUCTURAL_FACT:{chain.structural.hashes.fact_hash}",
        f"STRUCTURAL_COMPUTATION:{chain.structural.hashes.computation_hash}",
        f"SUPPORT_FACT:{chain.support.hashes.fact_hash}",
        f"SUPPORT_COMPUTATION:{chain.support.hashes.computation_hash}",
        *(f"FLOW_CANDIDATE_INDEX:{index}" for index in sorted(flow_indices)),
        *(
            f"STRUCTURAL_CANDIDATE_INDEX:{index}"
            for index in sorted(structural_indices)
        ),
        *(f"SUPPORT_CANDIDATE_INDEX:{index}" for index in sorted(support_indices)),
        *(
            f"TEMPORAL_CANDIDATE_INDEX:{index}"
            for index in sorted(chain.support.source_temporal_candidate_indices)
        ),
        *(
            f"TEMPORAL_SEED:{seed_id}"
            for seed_id in sorted(chain.support.source_temporal_seed_ids)
        ),
    )


class BaziRelationIncidenceEngine:
    schema = "BAZI-RELATION-INCIDENCE-FOUNDATION-RESULT-V1"
    typed_schema = "BAZI-RELATION-INCIDENCE-TYPED-RESOLUTION-V1"

    def resolve_typed(
        self,
        request: BaziRelationIncidenceRequest,
    ) -> BaziRelationIncidenceResolution:
        try:
            request.incidence_profile.validate()
        except ValueError as exc:
            return BaziRelationIncidenceResolution(
                self.typed_schema, "FAILED", (), (), (f"PROFILE_INVALID:{exc}",)
            )
        if (
            request.target_utc.tzinfo is None
            or request.target_utc.utcoffset() is None
        ):
            return BaziRelationIncidenceResolution(
                self.typed_schema,
                "FAILED",
                (),
                (),
                ("INVALID_TARGET:timezone-aware UTC instant required",),
            )

        from .integrity import (
            relation_incidence_hash_bundle,
            validate_relation_incidence_context,
        )

        unique: dict[tuple[str, str], dict[str, Any]] = {}
        try:
            chains = _compatible_chains(
                request.natal_candidate,
                request.target_utc,
                request.flow_candidates,
                request.structural_candidates,
                request.support_candidates,
            )
            for chain in chains:
                flow_indices = tuple(
                    sorted(chain.source_flow_candidate_indices or (chain.flow_index,))
                )
                structural_indices = tuple(sorted(
                    chain.source_structural_candidate_indices
                    or (chain.structural_index,)
                ))
                support_indices = tuple(sorted(
                    chain.source_support_candidate_indices or (chain.support_index,)
                ))
                temporal_indices = tuple(
                    sorted(chain.support.source_temporal_candidate_indices)
                )
                seed_ids = tuple(sorted(chain.support.source_temporal_seed_ids))
                binding_keys = _lineage_binding_keys(chain)
                context = build_relation_incidence_context(
                    request.natal_candidate,
                    chain,
                    request.incidence_profile,
                )
                hashes = relation_incidence_hash_bundle(
                    context,
                    request.natal_candidate,
                    chain,
                    flow_indices,
                    structural_indices,
                    support_indices,
                    temporal_indices,
                    seed_ids,
                    binding_keys,
                    request.incidence_profile,
                )
                integrity = validate_relation_incidence_context(
                    context,
                    request.natal_candidate,
                    chain,
                    flow_indices,
                    structural_indices,
                    support_indices,
                    temporal_indices,
                    seed_ids,
                    binding_keys,
                    request.incidence_profile,
                    hashes,
                )
                if integrity.status != "PASS":
                    return BaziRelationIncidenceResolution(
                        self.typed_schema,
                        "FAILED",
                        (),
                        (),
                        tuple(
                            f"INTEGRITY:{row.code}:{row.path}"
                            for row in integrity.diagnostics
                        ),
                    )
                # Deduplicate only a byte-identical complete FactHash +
                # ComputationHash contract. Any valid upstream lineage change is
                # computation identity and therefore remains a separate candidate.
                key = (hashes.fact_hash, hashes.computation_hash)
                existing = unique.get(key)
                if existing is None:
                    unique[key] = {
                        "flow_indices": list(flow_indices),
                        "structural_indices": list(structural_indices),
                        "support_indices": list(support_indices),
                        "temporal_indices": list(temporal_indices),
                        "seed_ids": list(seed_ids),
                        "binding_keys": list(binding_keys),
                        "context": context,
                        "integrity": integrity,
                        "hashes": hashes,
                    }
                else:
                    if (
                        tuple(existing["flow_indices"]) != flow_indices
                        or tuple(existing["structural_indices"])
                        != structural_indices
                        or tuple(existing["support_indices"]) != support_indices
                    ):
                        raise BaziRelationIncidenceGenerationError(
                            "INCIDENCE_COMPLETE_CONTRACT_COLLISION",
                            hashes.computation_hash,
                        )
        except (BaziRelationIncidenceGenerationError, ValueError, KeyError) as exc:
            code = getattr(exc, "diagnostic_code", "INCIDENCE_GENERATION_FAILED")
            return BaziRelationIncidenceResolution(
                self.typed_schema, "FAILED", (), (), (f"{code}:{exc}",)
            )

        candidates = tuple(
            BaziRelationIncidenceCandidate(
                source_flow_candidate_indices=tuple(
                    dict.fromkeys(row["flow_indices"])
                ),
                source_structural_candidate_indices=tuple(
                    dict.fromkeys(row["structural_indices"])
                ),
                source_support_candidate_indices=tuple(
                    dict.fromkeys(row["support_indices"])
                ),
                source_temporal_candidate_indices=tuple(row["temporal_indices"]),
                source_temporal_seed_ids=tuple(row["seed_ids"]),
                lineage_binding_keys=tuple(row["binding_keys"]),
                context=row["context"],
                integrity=row["integrity"],
                hashes=row["hashes"],
            )
            for row in unique.values()
        )
        return BaziRelationIncidenceResolution(
            schema=self.typed_schema,
            status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
            candidates=candidates,
            events=("AMBIGUOUS_LINEAGE_CANDIDATES_PRESERVED",)
            if len(candidates) > 1
            else (),
            diagnostics=(),
        )

    def resolve(self, request: BaziRelationIncidenceRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "upstream_natal_fact_hash": request.natal_candidate.hashes.fact_hash,
            "target_utc": json_value(request.target_utc),
            "incidence_profile": json_value(request.incidence_profile),
            "candidate_counts": {
                "flow": len(request.flow_candidates),
                "structural": len(request.structural_candidates),
                "support": len(request.support_candidates),
            },
            "candidates": [json_value(row) for row in typed.candidates],
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }

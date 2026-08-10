from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.bazi_structural_support import BaziStructuralSupportCandidate
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


def _unique_by_fact_hash(rows, label: str):
    result = {}
    for index, row in enumerate(rows):
        existing = result.get(row.hashes.fact_hash)
        if (
            existing is not None
            and existing[1].hashes.computation_hash != row.hashes.computation_hash
        ):
            raise BaziRelationIncidenceGenerationError(
                f"SAME_{label}_FACT_DIFFERENT_COMPUTATION_LINEAGE",
                row.hashes.fact_hash,
            )
        result.setdefault(row.hashes.fact_hash, (index, row))
    return result


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
    flow_by_hash = _unique_by_fact_hash(flows, "FLOW")
    structural_by_hash = _unique_by_fact_hash(structurals, "STRUCTURAL")
    expected_target = target_utc.astimezone(timezone.utc)
    chains: list[RelationIncidenceSnapshotInputs] = []
    for support_index, support in enumerate(supports):
        if support.integrity.status != "PASS":
            raise BaziRelationIncidenceGenerationError(
                "UPSTREAM_SUPPORT_INTEGRITY_FAILED", support.hashes.fact_hash
            )
        structural_match = structural_by_hash.get(
            support.context.upstream_structural_fact_hash
        )
        flow_match = flow_by_hash.get(support.context.upstream_flow_fact_hash)
        if structural_match is None:
            raise BaziRelationIncidenceGenerationError(
                "UPSTREAM_STRUCTURAL_CANDIDATE_MISSING",
                support.context.upstream_structural_fact_hash,
            )
        if flow_match is None:
            raise BaziRelationIncidenceGenerationError(
                "UPSTREAM_FLOW_CANDIDATE_MISSING",
                support.context.upstream_flow_fact_hash,
            )
        structural_index, structural = structural_match
        flow_index, flow = flow_match
        if flow.integrity.status != "PASS":
            raise BaziRelationIncidenceGenerationError(
                "UPSTREAM_FLOW_INTEGRITY_FAILED", flow.hashes.fact_hash
            )
        if structural.integrity.status != "PASS":
            raise BaziRelationIncidenceGenerationError(
                "UPSTREAM_STRUCTURAL_INTEGRITY_FAILED",
                structural.hashes.fact_hash,
            )
        if flow.context.target_utc.astimezone(timezone.utc) != expected_target:
            raise BaziRelationIncidenceGenerationError(
                "TARGET_FLOW_MISMATCH", flow.context.target_utc.isoformat()
            )
        if flow.context.upstream_natal_fact_hash != natal.hashes.fact_hash:
            raise BaziRelationIncidenceGenerationError(
                "FLOW_NATAL_LINEAGE_MISMATCH",
                flow.context.upstream_natal_fact_hash,
            )
        if (
            structural.context.upstream_natal_fact_hash != natal.hashes.fact_hash
            or structural.context.upstream_flow_fact_hash != flow.hashes.fact_hash
        ):
            raise BaziRelationIncidenceGenerationError(
                "STRUCTURAL_LINEAGE_MISMATCH", structural.hashes.fact_hash
            )
        if (
            support.context.upstream_natal_fact_hash != natal.hashes.fact_hash
            or support.context.upstream_flow_fact_hash != flow.hashes.fact_hash
            or support.context.upstream_structural_fact_hash
            != structural.hashes.fact_hash
        ):
            raise BaziRelationIncidenceGenerationError(
                "SUPPORT_LINEAGE_MISMATCH", support.hashes.fact_hash
            )
        if (
            support.context.upstream_temporal_fact_hash
            != flow.context.upstream_temporal_fact_hash
            or structural.context.upstream_temporal_fact_hash
            != flow.context.upstream_temporal_fact_hash
        ):
            raise BaziRelationIncidenceGenerationError(
                "TEMPORAL_LINEAGE_MISMATCH",
                flow.context.upstream_temporal_fact_hash,
            )
        if (
            not support.source_temporal_candidate_indices
            or not support.source_temporal_seed_ids
        ):
            raise BaziRelationIncidenceGenerationError(
                "TEMPORAL_LINEAGE_MISSING", support.hashes.fact_hash
            )
        chains.append(RelationIncidenceSnapshotInputs(
            flow_index=flow_index,
            structural_index=structural_index,
            support_index=support_index,
            flow=flow,
            structural=structural,
            support=support,
        ))
    return tuple(chains)


def _lineage_binding_keys(chain: RelationIncidenceSnapshotInputs) -> tuple[str, ...]:
    return (
        f"TEMPORAL_FACT:{chain.flow.context.upstream_temporal_fact_hash}",
        f"FLOW_FACT:{chain.flow.hashes.fact_hash}",
        f"STRUCTURAL_FACT:{chain.structural.hashes.fact_hash}",
        f"SUPPORT_FACT:{chain.support.hashes.fact_hash}",
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
                    temporal_indices,
                    seed_ids,
                    binding_keys,
                    request.incidence_profile,
                )
                integrity = validate_relation_incidence_context(
                    context,
                    request.natal_candidate,
                    chain,
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
                        "flow_indices": [chain.flow_index],
                        "structural_indices": [chain.structural_index],
                        "support_indices": [chain.support_index],
                        "temporal_indices": list(temporal_indices),
                        "seed_ids": list(seed_ids),
                        "binding_keys": list(binding_keys),
                        "context": context,
                        "integrity": integrity,
                        "hashes": hashes,
                    }
                else:
                    existing["flow_indices"].append(chain.flow_index)
                    existing["structural_indices"].append(chain.structural_index)
                    existing["support_indices"].append(chain.support_index)
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

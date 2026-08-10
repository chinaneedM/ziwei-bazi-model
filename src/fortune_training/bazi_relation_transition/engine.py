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
    RelationTransitionSnapshotInputs,
    build_relation_transition_context,
)
from .models import (
    BaziRelationTransitionCandidate,
    BaziRelationTransitionResolution,
)
from .profile import ResolvedBaziRelationTransitionProfile


class BaziRelationTransitionGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziRelationTransitionRequest:
    natal_candidate: BaziChartCandidate
    before_target_utc: datetime
    after_target_utc: datetime
    before_flow_candidates: tuple[BaziFlowCandidate, ...]
    before_structural_candidates: tuple[BaziStructuralCandidate, ...]
    before_support_candidates: tuple[BaziStructuralSupportCandidate, ...]
    after_flow_candidates: tuple[BaziFlowCandidate, ...]
    after_structural_candidates: tuple[BaziStructuralCandidate, ...]
    after_support_candidates: tuple[BaziStructuralSupportCandidate, ...]
    transition_profile: ResolvedBaziRelationTransitionProfile


def _unique_by_fact_hash(rows, label: str):
    result = {}
    for index, row in enumerate(rows):
        existing = result.get(row.hashes.fact_hash)
        if existing is not None and existing[1].hashes.computation_hash != row.hashes.computation_hash:
            raise BaziRelationTransitionGenerationError(
                f"SAME_{label}_FACT_DIFFERENT_COMPUTATION_LINEAGE",
                row.hashes.fact_hash,
            )
        result.setdefault(row.hashes.fact_hash, (index, row))
    return result


def _snapshot_chains(
    side: str,
    natal: BaziChartCandidate,
    target_utc: datetime,
    flows: tuple[BaziFlowCandidate, ...],
    structurals: tuple[BaziStructuralCandidate, ...],
    supports: tuple[BaziStructuralSupportCandidate, ...],
) -> tuple[RelationTransitionSnapshotInputs, ...]:
    if not flows:
        raise BaziRelationTransitionGenerationError(f"NO_{side}_FLOW_CANDIDATES", side)
    if not structurals:
        raise BaziRelationTransitionGenerationError(f"NO_{side}_STRUCTURAL_CANDIDATES", side)
    if not supports:
        raise BaziRelationTransitionGenerationError(f"NO_{side}_SUPPORT_CANDIDATES", side)
    flow_by_hash = _unique_by_fact_hash(flows, f"{side}_FLOW")
    structural_by_hash = _unique_by_fact_hash(structurals, f"{side}_STRUCTURAL")
    chains: list[RelationTransitionSnapshotInputs] = []
    for support_index, support in enumerate(supports):
        if support.integrity.status != "PASS":
            raise BaziRelationTransitionGenerationError(
                f"UPSTREAM_{side}_SUPPORT_INTEGRITY_FAILED",
                support.hashes.fact_hash,
            )
        structural_match = structural_by_hash.get(
            support.context.upstream_structural_fact_hash
        )
        flow_match = flow_by_hash.get(support.context.upstream_flow_fact_hash)
        if structural_match is None:
            raise BaziRelationTransitionGenerationError(
                f"UPSTREAM_{side}_STRUCTURAL_CANDIDATE_MISSING",
                support.context.upstream_structural_fact_hash,
            )
        if flow_match is None:
            raise BaziRelationTransitionGenerationError(
                f"UPSTREAM_{side}_FLOW_CANDIDATE_MISSING",
                support.context.upstream_flow_fact_hash,
            )
        structural_index, structural = structural_match
        flow_index, flow = flow_match
        if flow.integrity.status != "PASS":
            raise BaziRelationTransitionGenerationError(
                f"UPSTREAM_{side}_FLOW_INTEGRITY_FAILED", flow.hashes.fact_hash
            )
        if structural.integrity.status != "PASS":
            raise BaziRelationTransitionGenerationError(
                f"UPSTREAM_{side}_STRUCTURAL_INTEGRITY_FAILED",
                structural.hashes.fact_hash,
            )
        expected_target = target_utc.astimezone(timezone.utc)
        if flow.context.target_utc.astimezone(timezone.utc) != expected_target:
            raise BaziRelationTransitionGenerationError(
                f"{side}_TARGET_FLOW_MISMATCH",
                flow.context.target_utc.isoformat(),
            )
        if flow.context.upstream_natal_fact_hash != natal.hashes.fact_hash:
            raise BaziRelationTransitionGenerationError(
                f"{side}_FLOW_NATAL_LINEAGE_MISMATCH",
                flow.context.upstream_natal_fact_hash,
            )
        if (
            structural.context.upstream_natal_fact_hash != natal.hashes.fact_hash
            or structural.context.upstream_flow_fact_hash != flow.hashes.fact_hash
        ):
            raise BaziRelationTransitionGenerationError(
                f"{side}_STRUCTURAL_LINEAGE_MISMATCH",
                structural.hashes.fact_hash,
            )
        if (
            support.context.upstream_natal_fact_hash != natal.hashes.fact_hash
            or support.context.upstream_flow_fact_hash != flow.hashes.fact_hash
            or support.context.upstream_structural_fact_hash != structural.hashes.fact_hash
        ):
            raise BaziRelationTransitionGenerationError(
                f"{side}_SUPPORT_LINEAGE_MISMATCH", support.hashes.fact_hash
            )
        if not support.source_temporal_candidate_indices or not support.source_temporal_seed_ids:
            raise BaziRelationTransitionGenerationError(
                f"{side}_TEMPORAL_LINEAGE_MISSING", support.hashes.fact_hash
            )
        chains.append(RelationTransitionSnapshotInputs(
            flow_index=flow_index,
            structural_index=structural_index,
            support_index=support_index,
            flow=flow,
            structural=structural,
            support=support,
        ))
    return tuple(chains)


def _pairing_lineage(
    before: RelationTransitionSnapshotInputs,
    after: RelationTransitionSnapshotInputs,
):
    before_temporal = before.flow.context.upstream_temporal_fact_hash
    after_temporal = after.flow.context.upstream_temporal_fact_hash
    if before_temporal != after_temporal:
        return None
    seeds = tuple(sorted(
        set(before.support.source_temporal_seed_ids)
        & set(after.support.source_temporal_seed_ids)
    ))
    indices = tuple(sorted(
        set(before.support.source_temporal_candidate_indices)
        & set(after.support.source_temporal_candidate_indices)
    ))
    if not seeds or not indices:
        return None
    keys = (
        f"TEMPORAL_FACT:{before_temporal}",
        *(f"TEMPORAL_CANDIDATE_INDEX:{index}" for index in indices),
        *(f"TEMPORAL_SEED:{seed_id}" for seed_id in seeds),
    )
    return indices, seeds, keys


class BaziRelationTransitionEngine:
    schema = "BAZI-RELATION-TRANSITION-FOUNDATION-RESULT-V1"
    typed_schema = "BAZI-RELATION-TRANSITION-TYPED-RESOLUTION-V1"

    def resolve_typed(
        self,
        request: BaziRelationTransitionRequest,
    ) -> BaziRelationTransitionResolution:
        try:
            request.transition_profile.validate()
        except ValueError as exc:
            return BaziRelationTransitionResolution(
                self.typed_schema, "FAILED", (), (), (f"PROFILE_INVALID:{exc}",)
            )
        for label, target in (
            ("BEFORE", request.before_target_utc),
            ("AFTER", request.after_target_utc),
        ):
            if target.tzinfo is None or target.utcoffset() is None:
                return BaziRelationTransitionResolution(
                    self.typed_schema,
                    "FAILED",
                    (),
                    (),
                    (f"INVALID_{label}_TARGET:timezone-aware UTC instant required",),
                )
        if request.before_target_utc.astimezone(timezone.utc) >= request.after_target_utc.astimezone(timezone.utc):
            return BaziRelationTransitionResolution(
                self.typed_schema,
                "FAILED",
                (),
                (),
                ("INVALID_TARGET_ORDER:before_target_utc must be strictly earlier",),
            )

        from .integrity import (
            relation_transition_hash_bundle,
            validate_relation_transition_context,
        )

        unique: dict[tuple[str, str], dict[str, Any]] = {}
        try:
            before_chains = _snapshot_chains(
                "BEFORE",
                request.natal_candidate,
                request.before_target_utc,
                request.before_flow_candidates,
                request.before_structural_candidates,
                request.before_support_candidates,
            )
            after_chains = _snapshot_chains(
                "AFTER",
                request.natal_candidate,
                request.after_target_utc,
                request.after_flow_candidates,
                request.after_structural_candidates,
                request.after_support_candidates,
            )
            compatible_pairs = []
            for before in before_chains:
                for after in after_chains:
                    lineage = _pairing_lineage(before, after)
                    if lineage is not None:
                        compatible_pairs.append((before, after, lineage))
            if not compatible_pairs:
                raise BaziRelationTransitionGenerationError(
                    "NO_COMPATIBLE_BEFORE_AFTER_LINEAGE",
                    "no same-Temporal compatible candidate continuation",
                )

            for before, after, lineage in compatible_pairs:
                paired_indices, paired_seeds, pairing_keys = lineage
                context = build_relation_transition_context(
                    request.natal_candidate,
                    before,
                    after,
                    request.transition_profile,
                )
                hashes = relation_transition_hash_bundle(
                    context,
                    request.natal_candidate,
                    before,
                    after,
                    paired_indices,
                    paired_seeds,
                    pairing_keys,
                    request.transition_profile,
                )
                integrity = validate_relation_transition_context(
                    context,
                    request.natal_candidate,
                    before,
                    after,
                    paired_indices,
                    paired_seeds,
                    pairing_keys,
                    request.transition_profile,
                    hashes,
                )
                if integrity.status != "PASS":
                    return BaziRelationTransitionResolution(
                        self.typed_schema,
                        "FAILED",
                        (),
                        (),
                        tuple(
                            f"INTEGRITY:{row.code}:{row.path}"
                            for row in integrity.diagnostics
                        ),
                    )
                key = (hashes.fact_hash, hashes.computation_hash)
                existing = unique.get(key)
                if existing is None:
                    unique[key] = {
                        "before_flow": [before.flow_index],
                        "before_structural": [before.structural_index],
                        "before_support": [before.support_index],
                        "after_flow": [after.flow_index],
                        "after_structural": [after.structural_index],
                        "after_support": [after.support_index],
                        "paired_indices": list(paired_indices),
                        "paired_seeds": list(paired_seeds),
                        "pairing_keys": list(pairing_keys),
                        "context": context,
                        "integrity": integrity,
                        "hashes": hashes,
                    }
                else:
                    existing["before_flow"].append(before.flow_index)
                    existing["before_structural"].append(before.structural_index)
                    existing["before_support"].append(before.support_index)
                    existing["after_flow"].append(after.flow_index)
                    existing["after_structural"].append(after.structural_index)
                    existing["after_support"].append(after.support_index)
                    existing["paired_indices"].extend(paired_indices)
                    existing["paired_seeds"].extend(paired_seeds)
                    existing["pairing_keys"].extend(pairing_keys)
        except (BaziRelationTransitionGenerationError, ValueError, KeyError) as exc:
            code = getattr(exc, "diagnostic_code", "TRANSITION_GENERATION_FAILED")
            return BaziRelationTransitionResolution(
                self.typed_schema, "FAILED", (), (), (f"{code}:{exc}",)
            )

        candidates = tuple(
            BaziRelationTransitionCandidate(
                source_before_flow_candidate_indices=tuple(dict.fromkeys(row["before_flow"])),
                source_before_structural_candidate_indices=tuple(dict.fromkeys(row["before_structural"])),
                source_before_support_candidate_indices=tuple(dict.fromkeys(row["before_support"])),
                source_after_flow_candidate_indices=tuple(dict.fromkeys(row["after_flow"])),
                source_after_structural_candidate_indices=tuple(dict.fromkeys(row["after_structural"])),
                source_after_support_candidate_indices=tuple(dict.fromkeys(row["after_support"])),
                paired_temporal_candidate_indices=tuple(dict.fromkeys(row["paired_indices"])),
                paired_temporal_seed_ids=tuple(dict.fromkeys(row["paired_seeds"])),
                lineage_pairing_keys=tuple(dict.fromkeys(row["pairing_keys"])),
                context=row["context"],
                integrity=row["integrity"],
                hashes=row["hashes"],
            )
            for row in unique.values()
        )
        return BaziRelationTransitionResolution(
            schema=self.typed_schema,
            status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
            candidates=candidates,
            events=("AMBIGUOUS_LINEAGE_CANDIDATES_PRESERVED",)
            if len(candidates) > 1 else (),
            diagnostics=(),
        )

    def resolve(self, request: BaziRelationTransitionRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "upstream_natal_fact_hash": request.natal_candidate.hashes.fact_hash,
            "before_target_utc": json_value(request.before_target_utc),
            "after_target_utc": json_value(request.after_target_utc),
            "transition_profile": json_value(request.transition_profile),
            "before_candidate_counts": {
                "flow": len(request.before_flow_candidates),
                "structural": len(request.before_structural_candidates),
                "support": len(request.before_support_candidates),
            },
            "after_candidate_counts": {
                "flow": len(request.after_flow_candidates),
                "structural": len(request.after_structural_candidates),
                "support": len(request.after_support_candidates),
            },
            "candidates": [json_value(row) for row in typed.candidates],
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }

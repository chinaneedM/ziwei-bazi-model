from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.calendar_foundation.models import json_value

from .generation import build_structural_support_context
from .integrity import (
    structural_support_hash_bundle,
    validate_structural_support_context,
)
from .models import (
    BaziStructuralSupportCandidate,
    BaziStructuralSupportResolution,
)
from .profile import ResolvedBaziStructuralSupportProfile


class BaziStructuralSupportGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziStructuralSupportRequest:
    natal_candidate: BaziChartCandidate
    flow_candidates: tuple[BaziFlowCandidate, ...]
    structural_candidates: tuple[BaziStructuralCandidate, ...]
    support_profile: ResolvedBaziStructuralSupportProfile


class BaziStructuralSupportEngine:
    schema = "BAZI-STRUCTURAL-SUPPORT-FOUNDATION-RESULT-V1"
    typed_schema = "BAZI-STRUCTURAL-SUPPORT-TYPED-RESOLUTION-V1"

    def resolve_typed(
        self,
        request: BaziStructuralSupportRequest,
    ) -> BaziStructuralSupportResolution:
        try:
            request.support_profile.validate()
        except ValueError as exc:
            return BaziStructuralSupportResolution(
                self.typed_schema, "FAILED", (), (), (f"PROFILE_INVALID:{exc}",)
            )
        if not request.flow_candidates:
            return BaziStructuralSupportResolution(
                self.typed_schema, "FAILED", (), (), ("NO_FLOW_CANDIDATES",)
            )
        if not request.structural_candidates:
            return BaziStructuralSupportResolution(
                self.typed_schema, "FAILED", (), (), ("NO_STRUCTURAL_CANDIDATES",)
            )

        flow_by_fact_hash: dict[str, tuple[int, BaziFlowCandidate]] = {}
        for index, flow in enumerate(request.flow_candidates):
            existing = flow_by_fact_hash.get(flow.hashes.fact_hash)
            if existing is not None and existing[1].hashes != flow.hashes:
                return BaziStructuralSupportResolution(
                    self.typed_schema,
                    "FAILED",
                    (),
                    (),
                    ("SAME_FLOW_FACT_DIFFERENT_COMPUTATION_LINEAGE",),
                )
            flow_by_fact_hash.setdefault(flow.hashes.fact_hash, (index, flow))

        unique: dict[str, dict[str, Any]] = {}
        try:
            for structural_index, structural in enumerate(
                request.structural_candidates
            ):
                if structural.integrity.status != "PASS":
                    raise BaziStructuralSupportGenerationError(
                        "UPSTREAM_STRUCTURAL_INTEGRITY_FAILED",
                        structural.hashes.fact_hash,
                    )
                matched = flow_by_fact_hash.get(
                    structural.context.upstream_flow_fact_hash
                )
                if matched is None:
                    raise BaziStructuralSupportGenerationError(
                        "UPSTREAM_FLOW_CANDIDATE_MISSING",
                        structural.context.upstream_flow_fact_hash,
                    )
                flow_index, flow = matched
                if flow.integrity.status != "PASS":
                    raise BaziStructuralSupportGenerationError(
                        "UPSTREAM_FLOW_INTEGRITY_FAILED",
                        flow.hashes.fact_hash,
                    )
                context = build_structural_support_context(
                    request.natal_candidate,
                    flow,
                    structural,
                    request.support_profile,
                )
                hashes = structural_support_hash_bundle(
                    context,
                    request.natal_candidate,
                    flow,
                    structural,
                    request.support_profile,
                )
                integrity = validate_structural_support_context(
                    context,
                    request.natal_candidate,
                    flow,
                    structural,
                    request.support_profile,
                    hashes,
                )
                if integrity.status != "PASS":
                    return BaziStructuralSupportResolution(
                        self.typed_schema,
                        "FAILED",
                        (),
                        (),
                        tuple(
                            f"INTEGRITY:{row.code}:{row.path}"
                            for row in integrity.diagnostics
                        ),
                    )

                existing = unique.get(hashes.fact_hash)
                if existing is None:
                    unique[hashes.fact_hash] = {
                        "structural_indices": [structural_index],
                        "flow_indices": list(
                            structural.source_flow_candidate_indices
                            or (flow_index,)
                        ),
                        "temporal_indices": list(
                            structural.source_temporal_candidate_indices
                        ),
                        "seed_ids": list(structural.source_temporal_seed_ids),
                        "context": context,
                        "integrity": integrity,
                        "hashes": hashes,
                    }
                else:
                    if existing["hashes"].computation_hash != hashes.computation_hash:
                        raise BaziStructuralSupportGenerationError(
                            "SAME_SUPPORT_FACT_DIFFERENT_COMPUTATION_LINEAGE",
                            hashes.fact_hash,
                        )
                    existing["structural_indices"].append(structural_index)
                    existing["flow_indices"].extend(
                        structural.source_flow_candidate_indices or (flow_index,)
                    )
                    existing["temporal_indices"].extend(
                        structural.source_temporal_candidate_indices
                    )
                    existing["seed_ids"].extend(
                        structural.source_temporal_seed_ids
                    )
        except (BaziStructuralSupportGenerationError, ValueError, StopIteration) as exc:
            code = getattr(exc, "diagnostic_code", "SUPPORT_GENERATION_FAILED")
            return BaziStructuralSupportResolution(
                self.typed_schema, "FAILED", (), (), (f"{code}:{exc}",)
            )

        candidates = tuple(
            BaziStructuralSupportCandidate(
                source_structural_candidate_indices=tuple(
                    dict.fromkeys(row["structural_indices"])
                ),
                source_flow_candidate_indices=tuple(
                    dict.fromkeys(row["flow_indices"])
                ),
                source_temporal_candidate_indices=tuple(
                    dict.fromkeys(row["temporal_indices"])
                ),
                source_temporal_seed_ids=tuple(
                    dict.fromkeys(row["seed_ids"])
                ),
                context=row["context"],
                integrity=row["integrity"],
                hashes=row["hashes"],
            )
            for row in unique.values()
        )
        return BaziStructuralSupportResolution(
            schema=self.typed_schema,
            status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
            candidates=candidates,
            events=("STRUCTURAL_CANDIDATES_PRESERVED",)
            if len(candidates) > 1 else (),
            diagnostics=(),
        )

    def resolve(self, request: BaziStructuralSupportRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "upstream_natal_fact_hash": request.natal_candidate.hashes.fact_hash,
            "support_profile": json_value(request.support_profile),
            "flow_candidate_count": len(request.flow_candidates),
            "structural_candidate_count": len(request.structural_candidates),
            "candidates": [json_value(row) for row in typed.candidates],
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }

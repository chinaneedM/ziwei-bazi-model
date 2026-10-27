from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.calendar_foundation.models import json_value

from .generation import build_structural_context
from .integrity import structural_hash_bundle, validate_structural_context
from .models import BaziStructuralCandidate, BaziStructuralResolution
from .profile import ResolvedBaziStructuralProfile


class BaziStructuralGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziStructuralRequest:
    natal_candidate: BaziChartCandidate
    flow_candidates: tuple[BaziFlowCandidate, ...]
    structural_profile: ResolvedBaziStructuralProfile


class BaziStructuralEngine:
    schema = "BAZI-STRUCTURAL-CONTEXT-RESULT-V1"
    typed_schema = "BAZI-STRUCTURAL-CONTEXT-TYPED-RESOLUTION-V1"

    def resolve_typed(self, request: BaziStructuralRequest) -> BaziStructuralResolution:
        try:
            request.structural_profile.validate()
        except ValueError as exc:
            return BaziStructuralResolution(
                self.typed_schema, "FAILED", (), (), (f"PROFILE_INVALID:{exc}",)
            )
        if not request.flow_candidates:
            return BaziStructuralResolution(
                self.typed_schema, "FAILED", (), (), ("NO_FLOW_CANDIDATES",)
            )

        unique: dict[str, dict[str, Any]] = {}
        try:
            for index, flow in enumerate(request.flow_candidates):
                if flow.integrity.status != "PASS":
                    raise BaziStructuralGenerationError(
                        "UPSTREAM_FLOW_INTEGRITY_FAILED", flow.hashes.fact_hash
                    )
                if flow.context.upstream_natal_fact_hash != request.natal_candidate.hashes.fact_hash:
                    raise BaziStructuralGenerationError(
                        "UPSTREAM_NATAL_HASH_MISMATCH",
                        flow.context.upstream_natal_fact_hash,
                    )
                context = build_structural_context(
                    request.natal_candidate,
                    flow,
                    request.structural_profile,
                )
                hashes = structural_hash_bundle(
                    context,
                    request.natal_candidate,
                    flow,
                    request.structural_profile,
                )
                integrity = validate_structural_context(
                    context,
                    request.natal_candidate,
                    flow,
                    request.structural_profile,
                    hashes,
                )
                if integrity.status != "PASS":
                    return BaziStructuralResolution(
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
                        "flow_indices": [index],
                        "temporal_indices": list(flow.source_temporal_candidate_indices),
                        "seed_ids": list(flow.source_temporal_seed_ids),
                        "context": context,
                        "integrity": integrity,
                        "hashes": hashes,
                    }
                else:
                    if existing["hashes"].computation_hash != hashes.computation_hash:
                        raise BaziStructuralGenerationError(
                            "SAME_STRUCTURAL_FACT_DIFFERENT_COMPUTATION_LINEAGE",
                            hashes.fact_hash,
                        )
                    existing["flow_indices"].append(index)
                    existing["temporal_indices"].extend(
                        flow.source_temporal_candidate_indices
                    )
                    existing["seed_ids"].extend(flow.source_temporal_seed_ids)
        except (BaziStructuralGenerationError, ValueError) as exc:
            code = getattr(exc, "diagnostic_code", "STRUCTURAL_GENERATION_FAILED")
            return BaziStructuralResolution(
                self.typed_schema, "FAILED", (), (), (f"{code}:{exc}",)
            )

        candidates = tuple(
            BaziStructuralCandidate(
                source_flow_candidate_indices=tuple(row["flow_indices"]),
                source_temporal_candidate_indices=tuple(
                    dict.fromkeys(row["temporal_indices"])
                ),
                source_temporal_seed_ids=tuple(dict.fromkeys(row["seed_ids"])),
                context=row["context"],
                integrity=row["integrity"],
                hashes=row["hashes"],
            )
            for row in unique.values()
        )
        return BaziStructuralResolution(
            schema=self.typed_schema,
            status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
            candidates=candidates,
            events=("FLOW_CANDIDATES_PRESERVED",) if len(candidates) > 1 else (),
            diagnostics=(),
        )

    def resolve(self, request: BaziStructuralRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "upstream_natal_fact_hash": request.natal_candidate.hashes.fact_hash,
            "structural_profile": json_value(request.structural_profile),
            "flow_candidate_count": len(request.flow_candidates),
            "candidates": [json_value(row) for row in typed.candidates],
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }

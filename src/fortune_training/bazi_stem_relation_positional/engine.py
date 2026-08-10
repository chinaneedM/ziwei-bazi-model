from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.calendar_foundation.models import json_value

from .generation import build_stem_relation_positional_context
from .integrity import (
    stem_relation_positional_hash_bundle,
    validate_stem_relation_positional_context,
)
from .models import (
    BaziStemRelationPositionalCandidate,
    BaziStemRelationPositionalResolution,
)
from .profile import ResolvedBaziStemRelationPositionalProfile


class BaziStemRelationPositionalGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziStemRelationPositionalRequest:
    natal_candidate: BaziChartCandidate
    structural_candidates: tuple[BaziStructuralCandidate, ...]
    incidence_candidates: tuple[BaziRelationIncidenceCandidate, ...]
    positional_profile: ResolvedBaziStemRelationPositionalProfile


def _source_structural_candidate(
    incidence: BaziRelationIncidenceCandidate,
    structurals: tuple[BaziStructuralCandidate, ...],
) -> BaziStructuralCandidate:
    indices = incidence.source_structural_candidate_indices
    if (
        not indices
        or any(type(index) is not int or index < 0 or index >= len(structurals) for index in indices)
        or tuple(sorted(set(indices))) != indices
    ):
        raise BaziStemRelationPositionalGenerationError(
            "STRUCTURAL_LINEAGE_INDEX_INVALID", str(indices)
        )
    rows = tuple(structurals[index] for index in indices)
    first = rows[0]
    source_snapshot = incidence.context.snapshot
    for index, row in zip(indices, rows, strict=True):
        if row.integrity.status != "PASS":
            raise BaziStemRelationPositionalGenerationError(
                "UPSTREAM_STRUCTURAL_INTEGRITY_FAILED", str(index)
            )
        if (
            row.hashes.fact_hash != source_snapshot.upstream_structural_fact_hash
            or row.hashes.computation_hash
            != source_snapshot.upstream_structural_computation_hash
        ):
            raise BaziStemRelationPositionalGenerationError(
                "STRUCTURAL_HASH_LINEAGE_MISMATCH", str(index)
            )
        if row.hashes != first.hashes or row.context != first.context:
            raise BaziStemRelationPositionalGenerationError(
                "STRUCTURAL_COMPLETE_CONTRACT_MISMATCH", str(index)
            )
    return first


def _group_incidence_candidates(
    candidates: tuple[BaziRelationIncidenceCandidate, ...],
) -> tuple[dict[str, Any], ...]:
    if not candidates:
        raise BaziStemRelationPositionalGenerationError(
            "NO_INCIDENCE_CANDIDATES", "incidence"
        )
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for index, candidate in enumerate(candidates):
        if candidate.integrity.status != "PASS":
            raise BaziStemRelationPositionalGenerationError(
                "UPSTREAM_INCIDENCE_INTEGRITY_FAILED", str(index)
            )
        key = (candidate.hashes.fact_hash, candidate.hashes.computation_hash)
        existing = grouped.get(key)
        if existing is None:
            grouped[key] = {"indices": [index], "candidate": candidate}
        else:
            if existing["candidate"] != candidate:
                raise BaziStemRelationPositionalGenerationError(
                    "INCIDENCE_COMPLETE_CONTRACT_COLLISION", candidate.hashes.fact_hash
                )
            existing["indices"].append(index)
    return tuple(grouped.values())


def _lineage_binding_keys(
    incidence: BaziRelationIncidenceCandidate,
    incidence_indices: tuple[int, ...],
) -> tuple[str, ...]:
    return (
        f"INCIDENCE_FACT:{incidence.hashes.fact_hash}",
        f"INCIDENCE_COMPUTATION:{incidence.hashes.computation_hash}",
        *(f"INCIDENCE_CANDIDATE_INDEX:{index}" for index in incidence_indices),
        *incidence.lineage_binding_keys,
    )


class BaziStemRelationPositionalEngine:
    schema = "BAZI-STEM-RELATION-POSITIONAL-CONTEXT-FOUNDATION-RESULT-V1"
    typed_schema = "BAZI-STEM-RELATION-POSITIONAL-TYPED-RESOLUTION-V1"

    def resolve_typed(
        self,
        request: BaziStemRelationPositionalRequest,
    ) -> BaziStemRelationPositionalResolution:
        try:
            request.positional_profile.validate()
        except ValueError as exc:
            return BaziStemRelationPositionalResolution(
                self.typed_schema, "FAILED", (), (), (f"PROFILE_INVALID:{exc}",)
            )

        rows = []
        try:
            for group in _group_incidence_candidates(request.incidence_candidates):
                incidence = group["candidate"]
                incidence_indices = tuple(group["indices"])
                if (
                    incidence.context.snapshot.upstream_natal_fact_hash
                    != request.natal_candidate.hashes.fact_hash
                ):
                    raise BaziStemRelationPositionalGenerationError(
                        "INCIDENCE_NATAL_LINEAGE_MISMATCH",
                        incidence.context.snapshot.upstream_natal_fact_hash,
                    )
                structural = _source_structural_candidate(
                    incidence, request.structural_candidates
                )
                context = build_stem_relation_positional_context(
                    request.natal_candidate,
                    structural,
                    incidence,
                    request.positional_profile,
                )
                binding_keys = _lineage_binding_keys(incidence, incidence_indices)
                hashes = stem_relation_positional_hash_bundle(
                    context,
                    incidence,
                    incidence_indices,
                    incidence.source_flow_candidate_indices,
                    incidence.source_structural_candidate_indices,
                    incidence.source_support_candidate_indices,
                    incidence.source_temporal_candidate_indices,
                    incidence.source_temporal_seed_ids,
                    incidence.lineage_binding_keys,
                    binding_keys,
                    request.positional_profile,
                )
                integrity = validate_stem_relation_positional_context(
                    context,
                    request.natal_candidate,
                    structural,
                    incidence,
                    incidence_indices,
                    incidence.source_flow_candidate_indices,
                    incidence.source_structural_candidate_indices,
                    incidence.source_support_candidate_indices,
                    incidence.source_temporal_candidate_indices,
                    incidence.source_temporal_seed_ids,
                    incidence.lineage_binding_keys,
                    binding_keys,
                    request.positional_profile,
                    hashes,
                    request.incidence_candidates,
                )
                if integrity.status != "PASS":
                    return BaziStemRelationPositionalResolution(
                        self.typed_schema,
                        "FAILED",
                        (),
                        (),
                        tuple(
                            f"INTEGRITY:{row.code}:{row.path}"
                            for row in integrity.diagnostics
                        ),
                    )
                rows.append(BaziStemRelationPositionalCandidate(
                    source_incidence_candidate_indices=incidence_indices,
                    source_flow_candidate_indices=incidence.source_flow_candidate_indices,
                    source_structural_candidate_indices=incidence.source_structural_candidate_indices,
                    source_support_candidate_indices=incidence.source_support_candidate_indices,
                    source_temporal_candidate_indices=incidence.source_temporal_candidate_indices,
                    source_temporal_seed_ids=incidence.source_temporal_seed_ids,
                    source_incidence_lineage_binding_keys=incidence.lineage_binding_keys,
                    lineage_binding_keys=binding_keys,
                    context=context,
                    integrity=integrity,
                    hashes=hashes,
                ))
        except (BaziStemRelationPositionalGenerationError, ValueError, KeyError) as exc:
            code = getattr(exc, "diagnostic_code", "POSITIONAL_GENERATION_FAILED")
            return BaziStemRelationPositionalResolution(
                self.typed_schema, "FAILED", (), (), (f"{code}:{exc}",)
            )

        candidates = tuple(rows)
        return BaziStemRelationPositionalResolution(
            schema=self.typed_schema,
            status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
            candidates=candidates,
            events=("AMBIGUOUS_LINEAGE_CANDIDATES_PRESERVED",)
            if len(candidates) > 1 else (),
            diagnostics=(),
        )

    def resolve(self, request: BaziStemRelationPositionalRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "upstream_natal_fact_hash": request.natal_candidate.hashes.fact_hash,
            "positional_profile": json_value(request.positional_profile),
            "candidate_counts": {
                "structural": len(request.structural_candidates),
                "incidence": len(request.incidence_candidates),
            },
            "candidates": [json_value(row) for row in typed.candidates],
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from fortune_training.bazi_chart_bound_classical_interaction_projection.release import (
    SCOPE_ARTIFACT_PATH,
    validate_source_scope_artifact,
)
from fortune_training.bazi_structured_source_interaction_pattern_graph import (
    GRAPH_PATH,
    validate_structured_source_interaction_pattern_graph,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import (
    TrainingError,
    atomic_write_bytes,
    atomic_write_json,
    load_json,
    object_sha256,
    sha256_file,
)

from .profile import (
    EFFECT_FACETS,
    GRAPH_EDGE_CLASSES,
    GRAPH_NODE_CLASSES,
    HARD_EXCLUDED_EDGE_OR_STATE_SEMANTICS,
    SOURCE_CLAIM_TO_EFFECT_FACET,
    EXPECTED_SOURCE_SCOPE_SEMANTICS_SHA256,
    bazi_classical_effect_constraint_graph_factorized_composition_r1_profile,
)


AUDIT_ID = "BAZI-CLASSICAL-EFFECT-CONSTRAINT-GRAPH-FACTORIZED-COMPOSITION-R1"
AUDIT_ROOT = Path("audits/bazi-classical-effect-constraint-graph-factorized-composition-r1")
CONTRACT_PATH = AUDIT_ROOT / "contract.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-classical-effect-constraint-graph-factorized-composition-r1.schema.json")
RUNTIME_SCHEMA_PATH = Path("schemas/bazi-classical-effect-constraint-graph-factorized-composition-runtime-r1.schema.json")

EXPECTED_CLAIM_CLASS_COUNTS = {
    "SOURCE_ASSERTED_RESOLUTION": 12,
    "SOURCE_ASSERTED_RESOLUTION_FAILURE": 2,
    "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE": 3,
    "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION": 1,
    "SOURCE_ASSERTED_ATTENUATION": 1,
}


def build_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    source_scope = validate_source_scope_artifact(root)
    if source_scope["source_scope_specifications_semantics_sha256"] != EXPECTED_SOURCE_SCOPE_SEMANTICS_SHA256:
        raise TrainingError("released #249 source-scope semantic identity changed")
    source_graph_validation = validate_structured_source_interaction_pattern_graph(root)
    if source_graph_validation["status"] != "PASS":
        raise TrainingError("released source interaction graph validation failed")
    graph = load_json(root / GRAPH_PATH)
    scope_artifact = load_json(root / SCOPE_ARTIFACT_PATH)
    scoped_ids = tuple(
        scope_artifact["summary"]["scope_class_source_occurrence_ids"]["EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED"]
    )
    scoped_set = set(scoped_ids)
    if len(scoped_ids) != 13 or len(scoped_set) != 13:
        raise TrainingError("Unit 2 exact source-record universe changed")
    graph_record_by_source = {row["source_occurrence_id"]: row for row in graph["graph_records"]}
    scoped_records = [graph_record_by_source[source_id] for source_id in scoped_ids]
    source_layers = tuple(dict.fromkeys(row["source_layer"] for row in scoped_records))
    if source_layers != ("SHEN_CLASSICAL_SOURCE",):
        raise TrainingError(f"Unit 2 source-layer universe changed: {source_layers}")
    projected_claims = [row for row in graph["interaction_claim_edges"] if row["source_occurrence_id"] in scoped_set]
    claim_counts = dict(sorted(Counter(row["edge_class"] for row in projected_claims).items()))
    if len(projected_claims) != 19 or claim_counts != EXPECTED_CLAIM_CLASS_COUNTS:
        raise TrainingError(f"Unit 2 claim-template universe changed: {len(projected_claims)} {claim_counts}")
    chains = [row for row in graph["interaction_chain_patterns"] if row["source_occurrence_id"] in scoped_set]
    if len(chains) != 3:
        raise TrainingError(f"Unit 2 narrative-chain universe changed: {len(chains)}")
    for chain in chains:
        if (
            chain["sequence_semantics"] != "SOURCE_NARRATIVE_ORDER_ONLY"
            or chain["runtime_state_transition_emitted"] is not False
            or chain["suppression_or_activation_emitted"] is not False
        ):
            raise TrainingError(f"released source narrative chain semantics changed: {chain['chain_pattern_id']}")

    profile = bazi_classical_effect_constraint_graph_factorized_composition_r1_profile()
    contract = {
        "schema": "BAZI-CLASSICAL-EFFECT-CONSTRAINT-GRAPH-FACTORIZED-COMPOSITION-CONTRACT-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "source_graph_path": GRAPH_PATH.as_posix(),
            "source_graph_file_sha256": sha256_file(root / GRAPH_PATH),
            "source_graph_artifact_semantics_sha256": graph["determinism"]["artifact_semantics_sha256"],
            "source_graph_record_hash_chain_sha256": graph["determinism"]["graph_record_hash_chain_sha256"],
            "source_scope_artifact_path": SCOPE_ARTIFACT_PATH.as_posix(),
            "source_scope_artifact_file_sha256": sha256_file(root / SCOPE_ARTIFACT_PATH),
            "source_scope_specifications_semantics_sha256": source_scope["source_scope_specifications_semantics_sha256"],
            "upstream_projection_profile_id": profile.upstream_projection_profile_id,
            "upstream_projection_profile_version": profile.upstream_projection_profile_version,
        },
        "profile": json_value(profile),
        "closed_vocabularies": {
            "effect_facets": list(EFFECT_FACETS),
            "graph_node_classes": list(GRAPH_NODE_CLASSES),
            "graph_edge_classes": list(GRAPH_EDGE_CLASSES),
            "source_claim_to_effect_facet": dict(SOURCE_CLAIM_TO_EFFECT_FACET),
        },
        "composition_contract": {
            "binding_candidate_to_graph_fragment": "EXACTLY_ONE",
            "source_claim_to_effect_constraint": "EXACTLY_ONE",
            "member_selection_semantics": "NOT_RELEASED",
            "member_coexistence_semantics": "NOT_RELEASED",
            "member_exclusivity_semantics": "NOT_RELEASED",
            "cross_source_layer_composition": "NOT_RELEASED",
            "cartesian_expansion": "NOT_RELEASED",
            "shared_indexes": "EXACT_IDENTITY_ONLY",
            "raw_relation_immutability_contract": "IMMUTABLE_EXACT_REFERENCE_ONLY",
            "lifecycle_global_admission_gate": "NOT_RELEASED",
        },
        "summary": {
            "exact_source_record_count": 13,
            "source_layers": list(source_layers),
            "projected_claim_template_count": len(projected_claims),
            "projected_claim_class_counts": claim_counts,
            "source_narrative_chain_count": len(chains),
            "effect_facet_count": len(EFFECT_FACETS),
            "graph_node_class_count": len(GRAPH_NODE_CLASSES),
            "graph_edge_class_count": len(GRAPH_EDGE_CLASSES),
        },
        "hard_exclusions": list(HARD_EXCLUDED_EDGE_OR_STATE_SEMANTICS) + [
            "RESOLVER_ADMISSION",
            "SOURCE_SEMANTIC_PROFILE",
            "SEMANTIC_ATOM",
            "REWRITE_RULE",
            "MECHANISM_CANDIDATE_MATRIX",
            "CLOSURE_GAP_MATRIX",
            "G6_ALLOCATION_ELABORATION",
            "LIFECYCLE_ELIGIBILITY_SOLVING",
            "RELATION_STATE",
            "FIXPOINT_RESOLUTION",
            "FINAL_CLASSICAL_VERDICT",
        ],
    }
    contract["determinism"] = {
        "contract_semantics_sha256": object_sha256(contract),
    }
    return contract


def build_coverage_report(contract: dict[str, Any]) -> str:
    digest = contract["determinism"]["contract_semantics_sha256"]
    return "\n".join((
        "# Bazi Classical Effect Constraint Graph & Factorized Composition R1",
        "",
        "- Upstream exact-bindable source universe: 13 records, all `SHEN_CLASSICAL_SOURCE`.",
        "- Source claim templates: 19, preserved one-to-one as non-resolving effect constraints when their exact binding candidate is present.",
        "- Effect facets are closed to disposition, grade, and participant allocation; channels carry coordinates only and no state/value.",
        "- Exactly one graph fragment is created per exact #249 binding candidate; fragments from different outer lineages never compose.",
        "- Graph edges are closed to actor-reference, constraint-to-channel, channel-to-raw-reference, and source-narrative adjacency.",
        "- Source narrative order is adjacency-only; no transitive closure, state transition, conflict, negate, override, suppression, activation, or release edge is emitted.",
        "- `SOURCE_ASSERTED_ATTENUATION` targets grade only and never synthesizes disposition/resolution.",
        "- `SOURCE_ASSERTED_PARTICIPANT_ALLOCATION` preserves exact #247 multiplicity provenance and all compatible exact instance paths without selecting a participant/path.",
        "- Composition is factorized by source layer and source record; member selection/coexistence/exclusivity and Cartesian expansion are all `NOT_RELEASED`.",
        "- Shared raw-relation/channel indexes are exact identity indexes only; they do not merge channels or infer support/conflict/precedence.",
        "- Resolver Admission / Source Semantic Profile and all final Classical solving remain outside this release.",
        f"- Deterministic Unit 2 contract semantics: `{digest}`.",
        "",
    ))


def validate_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    actual = load_json(root / CONTRACT_PATH)
    expected = build_release_contract(root)
    if actual != expected:
        raise TrainingError("Classical effect constraint graph contract is stale or tampered")
    schema = load_json(root / SCHEMA_PATH)
    runtime_schema = load_json(root / RUNTIME_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(runtime_schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(actual), key=lambda row: list(row.path))
    if errors:
        raise TrainingError(f"Unit 2 release contract schema validation failed: {errors[0].message}")
    report_path = root / REPORT_PATH
    expected_report = build_coverage_report(actual)
    if not report_path.is_file() or report_path.read_text(encoding="utf-8") != expected_report:
        raise TrainingError("Unit 2 coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "exact_source_record_count": actual["summary"]["exact_source_record_count"],
        "projected_claim_template_count": actual["summary"]["projected_claim_template_count"],
        "source_narrative_chain_count": actual["summary"]["source_narrative_chain_count"],
        "contract_semantics_sha256": actual["determinism"]["contract_semantics_sha256"],
        "schema_sha256": sha256_file(root / SCHEMA_PATH),
        "runtime_schema_sha256": sha256_file(root / RUNTIME_SCHEMA_PATH),
        "report_sha256": sha256_file(report_path),
    }


def write_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    contract = build_release_contract(root)
    atomic_write_json(root / CONTRACT_PATH, contract)
    atomic_write_bytes(root / REPORT_PATH, build_coverage_report(contract).encode("utf-8"))
    return validate_release_contract(root)

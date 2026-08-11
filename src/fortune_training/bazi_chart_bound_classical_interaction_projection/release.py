from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

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
    EXPECTED_BINDABILITY_PLAN_SEMANTICS_SHA256,
    EXPECTED_GRAPH_ARTIFACT_SEMANTICS_SHA256,
    EXPECTED_GRAPH_FILE_SHA256,
    EXPECTED_GRAPH_RECORD_HASH_CHAIN_SHA256,
    EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256,
    EXPECTED_MATRIX_FILE_SHA256,
    EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256,
    bazi_chart_bound_classical_interaction_projection_foundation_r1_profile,
)
from .scope import (
    EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED,
    NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION,
    derive_source_scope_specifications,
)


AUDIT_ID = "BAZI-CHART-BOUND-CLASSICAL-INTERACTION-PROJECTION-FOUNDATION-R1"
GRAPH_PATH = Path("audits/bazi-structured-source-interaction-pattern-graph-r1/graph.json")
MATRIX_PATH = Path("audits/bazi-classical-relation-interaction-assertion-matrix-r1/matrix.json")
BINDABILITY_PLAN_PATH = Path("audits/bazi-chart-specific-exact-source-pattern-binding-candidates-r1/bindability-plan.json")
AUDIT_ROOT = Path("audits/bazi-chart-bound-classical-interaction-projection-foundation-r1")
SCOPE_ARTIFACT_PATH = AUDIT_ROOT / "source-scope-specifications.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-chart-bound-classical-interaction-projection-foundation-r1.schema.json")
RUNTIME_SCHEMA_PATH = Path("schemas/bazi-chart-bound-classical-interaction-projection-runtime-r1.schema.json")

UPSTREAM_CONTRACT_FILE_SHA256 = {
    GRAPH_PATH.as_posix(): EXPECTED_GRAPH_FILE_SHA256,
    MATRIX_PATH.as_posix(): EXPECTED_MATRIX_FILE_SHA256,
    "schemas/bazi-classical-relation-interaction-assertion-matrix-r1.schema.json": "b79c9037b323bcccc03304e7634d707c3ec55b8f60b14192a53e476111dac9e4",
    "schemas/bazi-structured-source-interaction-pattern-graph-r1.schema.json": "a85bbad1a7a7a438ee43f4e52a46a25349ce807e226721c872bb48eafc6c70d1",
    "schemas/bazi-chart-foundation-v1.schema.json": "b9465e7b7bd496ad47372452de0173d6a34c9fe0a9f2362dbc668394ce40d60f",
    "schemas/bazi-relation-incidence-foundation-r1.schema.json": "89af6132dcaafae4d337ce913e12c7a8e031c402ebfdc1206e40f11607cca8c6",
    "schemas/bazi-branch-relation-positional-context-foundation-r1.schema.json": "6aaf67e07b58da15eabf266842345f7433b0166bd1d441f2bd94f254f9923220",
    "schemas/bazi-stem-relation-positional-context-foundation-r1.schema.json": "4ee1b9d4a5e287acaf05b790ed01c3344eef6c1deeab4d0ad41358180264c3a5",
    "src/fortune_training/bazi_relation_incidence/models.py": "cb7d095a756a48e7dadd3091406bde109a78feb8982bcf2ebe06b93c7da1c270",
    "src/fortune_training/bazi_branch_relation_positional/models.py": "00d45cb69ab3ae24c9f16e3eaec7cee5b0b4bdc37192f8b02bad2dd626331213",
    "src/fortune_training/bazi_stem_relation_positional/models.py": "97e50c9ad537a63ee3ecb8d8ffda14b7f1261a480790a50e02fbe8ac21d9bda7",
}

EXPECTED_BINDABILITY_CLASS_COUNTS = {
    "FULL_EXACT_BINDING_ENUMERATION": 11,
    "PARTIAL_EXACT_BINDING_ENUMERATION": 2,
    "NOT_R1_EXACT_BINDABLE": 11,
}
EXPECTED_PROJECTED_CLAIM_CLASS_COUNTS = {
    "SOURCE_ASSERTED_RESOLUTION": 12,
    "SOURCE_ASSERTED_RESOLUTION_FAILURE": 2,
    "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE": 3,
    "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION": 1,
    "SOURCE_ASSERTED_ATTENUATION": 1,
}


def _validate_upstream(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for relative, expected in UPSTREAM_CONTRACT_FILE_SHA256.items():
        actual = sha256_file(root / relative)
        if actual != expected:
            raise TrainingError(f"released upstream Classical interaction projection contract changed: {relative}")
    graph = load_json(root / GRAPH_PATH)
    matrix = load_json(root / MATRIX_PATH)
    plan = load_json(root / BINDABILITY_PLAN_PATH)
    if graph.get("determinism", {}).get("artifact_semantics_sha256") != EXPECTED_GRAPH_ARTIFACT_SEMANTICS_SHA256:
        raise TrainingError("released source graph semantic identity changed")
    if graph.get("determinism", {}).get("graph_record_hash_chain_sha256") != EXPECTED_GRAPH_RECORD_HASH_CHAIN_SHA256:
        raise TrainingError("released source graph record chain changed")
    if matrix.get("determinism", {}).get("artifact_semantics_sha256") != EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256:
        raise TrainingError("released assertion matrix semantic identity changed")
    if matrix.get("determinism", {}).get("record_hash_chain_sha256") != EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256:
        raise TrainingError("released assertion matrix record chain changed")
    if plan.get("determinism", {}).get("bindability_plan_semantics_sha256") != EXPECTED_BINDABILITY_PLAN_SEMANTICS_SHA256:
        raise TrainingError("released chart-specific binding plan semantic identity changed")
    if plan.get("summary", {}).get("class_counts") != EXPECTED_BINDABILITY_CLASS_COUNTS:
        raise TrainingError("released #247 bindability structure changed")
    return graph, matrix, plan


def build_source_scope_artifact(root: Path) -> dict[str, Any]:
    graph, matrix, plan = _validate_upstream(root)
    profile = bazi_chart_bound_classical_interaction_projection_foundation_r1_profile()
    scope_rows = derive_source_scope_specifications(graph)
    matrix_order = tuple(row["source_occurrence_id"] for row in matrix["records"])
    graph_order = tuple(row["source_occurrence_id"] for row in graph["graph_records"])
    if matrix_order != graph_order or tuple(row.source_occurrence_id for row in scope_rows) != graph_order:
        raise TrainingError("source scope matrix does not replay exact 24-row upstream order")

    scoped_ids = {row.source_occurrence_id for row in scope_rows if row.scope_specification_status == EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED}
    projected_claims = [row for row in graph["interaction_claim_edges"] if row["source_occurrence_id"] in scoped_ids]
    claim_counts = dict(sorted(Counter(row["edge_class"] for row in projected_claims).items()))
    if len(projected_claims) != 19 or claim_counts != EXPECTED_PROJECTED_CLAIM_CLASS_COUNTS:
        raise TrainingError(f"chart-bound claim template universe changed: {len(projected_claims)} {claim_counts}")
    transition_users = [
        row["source_occurrence_id"]
        for row in matrix["records"]
        if any(dep["primitive"] == "RELATION_TRANSITION_SET_CHANGE" for dep in row["neutral_runtime_dependency_map"])
    ]
    if transition_users:
        raise TrainingError(f"R1 unexpectedly requires Relation Transition observations: {transition_users}")

    rows = json_value(scope_rows)
    counts = dict(sorted(Counter(row.scope_specification_status for row in scope_rows).items()))
    semantics = object_sha256({
        "profile": json_value(profile),
        "graph_artifact_semantics_sha256": EXPECTED_GRAPH_ARTIFACT_SEMANTICS_SHA256,
        "graph_record_hash_chain_sha256": EXPECTED_GRAPH_RECORD_HASH_CHAIN_SHA256,
        "matrix_artifact_semantics_sha256": EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256,
        "matrix_record_hash_chain_sha256": EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256,
        "bindability_plan_semantics_sha256": EXPECTED_BINDABILITY_PLAN_SEMANTICS_SHA256,
        "source_scope_specifications": rows,
        "projected_claim_template_ids": [row["interaction_claim_edge_id"] for row in projected_claims],
    })
    return {
        "schema": "BAZI-CLASSICAL-INTERACTION-SOURCE-SCOPE-SPECIFICATION-MATRIX-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "source_graph_path": GRAPH_PATH.as_posix(),
            "source_graph_file_sha256": EXPECTED_GRAPH_FILE_SHA256,
            "source_graph_artifact_semantics_sha256": EXPECTED_GRAPH_ARTIFACT_SEMANTICS_SHA256,
            "source_graph_record_hash_chain_sha256": EXPECTED_GRAPH_RECORD_HASH_CHAIN_SHA256,
            "assertion_matrix_path": MATRIX_PATH.as_posix(),
            "assertion_matrix_file_sha256": EXPECTED_MATRIX_FILE_SHA256,
            "assertion_matrix_artifact_semantics_sha256": EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256,
            "assertion_matrix_record_hash_chain_sha256": EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256,
            "bindability_plan_path": BINDABILITY_PLAN_PATH.as_posix(),
            "bindability_plan_semantics_sha256": EXPECTED_BINDABILITY_PLAN_SEMANTICS_SHA256,
            "upstream_contract_file_sha256": dict(UPSTREAM_CONTRACT_FILE_SHA256),
        },
        "projection_profile": json_value(profile),
        "source_scope_specifications": rows,
        "summary": {
            "source_record_count": 24,
            "scope_class_counts": counts,
            "scope_class_source_occurrence_ids": {
                key: [row.source_occurrence_id for row in scope_rows if row.scope_specification_status == key]
                for key in (EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED, NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION)
            },
            "upstream_bindability_class_counts": plan["summary"]["class_counts"],
            "projected_claim_template_count": len(projected_claims),
            "projected_claim_class_counts": claim_counts,
            "relation_transition_observation_usage_count": 0,
        },
        "determinism": {
            "source_scope_specifications_semantics_sha256": semantics,
        },
    }


def build_coverage_report(artifact: dict[str, Any]) -> str:
    digest = artifact["determinism"]["source_scope_specifications_semantics_sha256"]
    return "\n".join((
        "# Bazi Chart-Bound Classical Interaction Projection Foundation R1",
        "",
        "- Source Scope rows: 24 exactly once in released graph/matrix order.",
        "- `EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED`: 13; `NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION`: 11.",
        "- All 13 specified source scenarios are `NATAL_FOUR_PILLAR` with `ALL_BOUND_SOURCE_PARTICIPANTS` and required layer `NATAL`.",
        "- Cross-layer exact binding candidates are preserved and projected as `CROSS_LAYER_EXTENSION_UNRESOLVED`; they are never pruned.",
        "- Structural binding completeness and source-scope compatibility remain independent axes.",
        "- Runtime neutral observations are binding-scoped and limited to Matrix-declared exact identities, topology, incidence, and temporal layer/frame facts.",
        "- Relation-pair topology is claim-scoped; no all-chart topology scan is authorized.",
        "- Relation Transition observation usage is 0 in the released 24-record Matrix and no transition observation exists in R1.",
        "- Current chart-bound projection universe contains 19 source claim templates across the 13 exact-bindable source records.",
        "- `SOURCE_ASSERTED_*` is preserved as source provenance only; no operability, precedence, winner, suppression, activation, release, rewrite, Effect Constraint Graph, resolver admission, or final verdict is emitted.",
        "- Upstream `source_unresolved_graph_requirements` is replayed as provenance and is not a direct runtime blocker.",
        f"- Deterministic scope/projection-plan semantics: `{digest}`.",
        "",
    ))


def validate_source_scope_artifact(root: Path) -> dict[str, Any]:
    actual = load_json(root / SCOPE_ARTIFACT_PATH)
    expected = build_source_scope_artifact(root)
    if actual != expected:
        raise TrainingError("chart-bound Classical interaction source-scope artifact is stale or tampered")
    schema = load_json(root / SCHEMA_PATH)
    runtime_schema = load_json(root / RUNTIME_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(runtime_schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(actual), key=lambda row: list(row.path))
    if errors:
        raise TrainingError(f"source-scope artifact schema validation failed: {errors[0].message}")
    report_path = root / REPORT_PATH
    if not report_path.is_file() or report_path.read_text(encoding="utf-8") != build_coverage_report(actual):
        raise TrainingError("chart-bound Classical interaction coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "source_record_count": actual["summary"]["source_record_count"],
        "scope_class_counts": actual["summary"]["scope_class_counts"],
        "projected_claim_template_count": actual["summary"]["projected_claim_template_count"],
        "source_scope_specifications_semantics_sha256": actual["determinism"]["source_scope_specifications_semantics_sha256"],
        "schema_sha256": sha256_file(root / SCHEMA_PATH),
        "runtime_schema_sha256": sha256_file(root / RUNTIME_SCHEMA_PATH),
        "report_sha256": sha256_file(report_path),
    }


def write_source_scope_artifact(root: Path) -> dict[str, Any]:
    artifact = build_source_scope_artifact(root.resolve())
    atomic_write_json(root / SCOPE_ARTIFACT_PATH, artifact)
    atomic_write_bytes(root / REPORT_PATH, build_coverage_report(artifact).encode("utf-8"))
    return validate_source_scope_artifact(root)

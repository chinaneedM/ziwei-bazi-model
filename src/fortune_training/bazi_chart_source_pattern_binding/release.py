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

from .bindability import derive_bindability_plan
from .profile import bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile


AUDIT_ID = "BAZI-CHART-SPECIFIC-EXACT-SOURCE-PATTERN-BINDING-CANDIDATES-R1"
GRAPH_PATH = Path("audits/bazi-structured-source-interaction-pattern-graph-r1/graph.json")
PLAN_PATH = Path("audits/bazi-chart-specific-exact-source-pattern-binding-candidates-r1/bindability-plan.json")
REPORT_PATH = Path("audits/bazi-chart-specific-exact-source-pattern-binding-candidates-r1/coverage-report.md")
SCHEMA_PATH = Path("schemas/bazi-chart-specific-exact-source-pattern-binding-candidates-r1.schema.json")
RUNTIME_SCHEMA_PATH = Path("schemas/bazi-chart-specific-exact-source-pattern-binding-runtime-r1.schema.json")
UPSTREAM_CONTRACT_FILE_SHA256 = {
    "schemas/bazi-chart-foundation-v1.schema.json": "b9465e7b7bd496ad47372452de0173d6a34c9fe0a9f2362dbc668394ce40d60f",
    "schemas/bazi-relation-incidence-foundation-r1.schema.json": "89af6132dcaafae4d337ce913e12c7a8e031c402ebfdc1206e40f11607cca8c6",
    "schemas/bazi-branch-relation-positional-context-foundation-r1.schema.json": "6aaf67e07b58da15eabf266842345f7433b0166bd1d441f2bd94f254f9923220",
    "schemas/bazi-stem-relation-positional-context-foundation-r1.schema.json": "4ee1b9d4a5e287acaf05b790ed01c3344eef6c1deeab4d0ad41358180264c3a5",
    "schemas/bazi-structured-source-interaction-pattern-graph-r1.schema.json": "a85bbad1a7a7a438ee43f4e52a46a25349ce807e226721c872bb48eafc6c70d1",
    "src/fortune_training/bazi_relation_incidence/models.py": "cb7d095a756a48e7dadd3091406bde109a78feb8982bcf2ebe06b93c7da1c270",
    "src/fortune_training/bazi_branch_relation_positional/models.py": "00d45cb69ab3ae24c9f16e3eaec7cee5b0b4bdc37192f8b02bad2dd626331213",
    "src/fortune_training/bazi_stem_relation_positional/models.py": "97e50c9ad537a63ee3ecb8d8ffda14b7f1261a480790a50e02fbe8ac21d9bda7",
}


def build_bindability_plan_artifact(root: Path) -> dict[str, Any]:
    graph = load_json(root / GRAPH_PATH)
    for relative, expected in UPSTREAM_CONTRACT_FILE_SHA256.items():
        if sha256_file(root / relative) != expected:
            raise TrainingError(f"released upstream binding contract changed: {relative}")
    profile = bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile()
    plan = derive_bindability_plan(graph, profile)
    rows = json_value(plan)
    counts = Counter(row.bindability_class for row in plan)
    semantics = object_sha256({
        "graph_artifact_semantics_sha256": profile.graph_artifact_semantics_sha256,
        "graph_record_hash_chain_sha256": profile.graph_record_hash_chain_sha256,
        "profile": json_value(profile),
        "bindability_plan": rows,
    })
    return {
        "schema": "BAZI-CHART-SPECIFIC-EXACT-SOURCE-PATTERN-BINDABILITY-PLAN-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "source_graph_path": GRAPH_PATH.as_posix(),
            "source_graph_file_sha256": sha256_file(root / GRAPH_PATH),
            "source_graph_artifact_semantics_sha256": profile.graph_artifact_semantics_sha256,
            "source_graph_record_hash_chain_sha256": profile.graph_record_hash_chain_sha256,
            "upstream_contract_file_sha256": dict(UPSTREAM_CONTRACT_FILE_SHA256),
        },
        "binding_profile": json_value(profile),
        "bindability_plan": rows,
        "summary": {
            "graph_record_count": len(plan),
            "class_counts": dict(sorted(counts.items())),
            "class_source_occurrence_ids": {
                key: [row.source_occurrence_id for row in plan if row.bindability_class == key]
                for key in sorted(counts)
            },
        },
        "determinism": {"bindability_plan_semantics_sha256": semantics},
    }


def validate_bindability_plan_artifact(root: Path) -> dict[str, Any]:
    actual = load_json(root / PLAN_PATH)
    expected = build_bindability_plan_artifact(root)
    if actual != expected:
        raise TrainingError("chart source-pattern bindability plan is stale or tampered")
    schema = load_json(root / SCHEMA_PATH)
    runtime_schema = load_json(root / RUNTIME_SCHEMA_PATH)
    Draft202012Validator.check_schema(runtime_schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(actual), key=lambda row: list(row.path))
    if errors:
        raise TrainingError(f"chart source-pattern bindability schema validation failed: {errors[0].message}")
    report_path = root / REPORT_PATH
    if not report_path.is_file() or report_path.read_text(encoding="utf-8") != build_coverage_report(actual):
        raise TrainingError("chart source-pattern binding coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "graph_record_count": actual["summary"]["graph_record_count"],
        "class_counts": actual["summary"]["class_counts"],
        "bindability_plan_semantics_sha256": actual["determinism"]["bindability_plan_semantics_sha256"],
        "schema_sha256": sha256_file(root / SCHEMA_PATH),
        "runtime_schema_sha256": sha256_file(root / RUNTIME_SCHEMA_PATH),
        "report_sha256": sha256_file(report_path),
    }


def build_coverage_report(artifact: dict[str, Any]) -> str:
    return "\n".join((
        "# Bazi Chart-Specific Exact Source Pattern Binding Candidates R1",
        "",
        "- Source graph records: 24, each represented exactly once and in released graph order.",
        "- `FULL_EXACT_BINDING_ENUMERATION`: 11.",
        "- `PARTIAL_EXACT_BINDING_ENUMERATION`: 2 (`ZPZQ-CL-09-007-002`, `ZPZQ-CL-09-007-003`).",
        "- `NOT_R1_EXACT_BINDABLE`: 11.",
        "- Bindability is derived from released relation, participant, position, and multiplicity graph objects.",
        "- Every plan and runtime inventory row replays upstream `unresolved_graph_requirements` in released source order as provenance, separately from binder-local structural constraints.",
        "- Claim edges and narrative chains are carried only by stable IDs and are not candidate predicates.",
        "- QTBJ `05347` / `05370` remain `SOURCE_GRAPH_NOT_R1_EXACT_BINDABLE`.",
        "- Source-time contexts in `007-002` / `007-003` remain unresolved.",
        "- Runtime enumeration uses Relation Incidence as lineage root and Branch/Stem Positional as fact projections.",
        "- No operability, precedence, winner, activation, suppression, release, transition, or resolver semantics are emitted.",
        "",
    ))


def write_bindability_plan_artifact(root: Path) -> dict[str, Any]:
    artifact = build_bindability_plan_artifact(root.resolve())
    atomic_write_json(root / PLAN_PATH, artifact)
    atomic_write_bytes(root / REPORT_PATH, build_coverage_report(artifact).encode("utf-8"))
    return validate_bindability_plan_artifact(root)

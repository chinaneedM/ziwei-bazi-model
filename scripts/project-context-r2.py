#!/usr/bin/env python3
"""Derived, bounded recovery view and exhaustive literal registry search.
The R1 files and existing verifiers remain authoritative."""
from __future__ import annotations
import argparse
import hashlib
import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = {
    "state": "docs/PROJECT-CURRENT-STATE-R1.json",
    "ledger": "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json",
    "manifest": "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json",
    "root": "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json",
    "matrix": "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json",
    "graph": "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json",
}
VIEW = "docs/PROJECT-RECOVERY-VIEW-R2.json"
MAX_VIEW_BYTES = 12000

def need(condition, message):
    if not condition:
        raise ValueError(message)

def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def project(data, bindings):
    s, l, m, root, x, g = (data[k] for k in PATHS)
    ha, rs = s["historical_audit"], s["research_execution_strategy"]
    allowed = {"OPEN", "BLOCKED_SOURCE_ACCESS", "RESOLVED_WITH_EVIDENCE"}
    need(all(q["status"] in allowed for q in l["issues"]), "unknown issue status")
    opened = [q for q in l["issues"] if q["status"] != "RESOLVED_WITH_EVIDENCE"]
    p0 = [q for q in opened if q["priority"] == "P0"]
    cp = l["checkpoint_log"][-1]
    need(l["binding"]["reviewed_state_version"] == s["schema_version"], "ledger/state version")
    need(l["binding"]["source_focus_count"] == len(ha["current_focus"]), "focus/ledger count")
    need(ha["research_omission_guard"]["open_issues"] == len(opened), "open issue count")
    need(ha["research_omission_guard"]["reviewed_state_version"] == s["schema_version"], "guard version")
    need(cp["state_version"] == s["schema_version"], "latest checkpoint version")
    need(m["root_registry_blob_sha"] == bindings[PATHS["root"]], "root registry binding")
    need(len(root["sources"]) == m["root_source_count"] == ha["external_source_registry_root_count"], "root source count")
    need(sum(i["source_count"] for i in m["shards"]) == m["extension_source_count"] == ha["external_source_registry_extension_count"], "extension count")
    need(m["root_source_count"] + m["extension_source_count"] == m["combined_source_count"] == ha["external_source_registry_total_unique_count"], "source total")
    need(ha["row_count"] == len(x["rows"]) and ha["audited_row_count"] == len(x["audited_row_ids"]), "matrix count")
    f = ha["current_focus"][-1]
    return {
        "schema": "TIANWEN-CONTEXT-RECOVERY-VIEW-R2",
        "authority": "DERIVED_ONLY",
        "bindings": bindings,
        "state_version": s["schema_version"],
        "stage": s["current_stage"],
        "invariants": s["invariants"],
        "counts": {
            "matrix_rows": len(x["rows"]), "matrix_audited": len(x["audited_row_ids"]),
            "root_sources": len(root["sources"]), "extension_sources": m["extension_source_count"],
            "total_sources": m["combined_source_count"], "shards": len(m["shards"]),
            "graph_nodes": len(g["nodes"]), "graph_edges": len(g["edges"]),
            "open_issues": len(opened), "p0": len(p0),
        },
        "phase": rs["phase"],
        "next_deliverable": rs["next_deliverable"],
        "latest_matrix_batch": ha["latest_batch_doc"],
        "latest_breadth_batch": rs["latest_breadth_batch_doc"],
        "checkpoint": {"id": cp["id"], "evidence_refs": cp["evidence_refs"]},
        "focus": {"index": len(ha["current_focus"]) - 1, "text": f[:1600], "truncated": len(f) > 1600},
        "p0": [{k: q[k] for k in ("id", "title", "status", "next_action")} for q in p0],
    }

def make_view(root):
    raw = {k: (root / p).read_bytes() for k, p in PATHS.items()}
    bindings = {p: blob_sha(raw[k]) for k, p in PATHS.items()}
    return project({k: json.loads(v) for k, v in raw.items()}, bindings)

def encode(view):
    raw = (json.dumps(view, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    need(len(raw) <= MAX_VIEW_BYTES, "view budget exceeded; use canonical/paged fallback, never omit P0")
    return raw

def verify_view(root):
    expected = make_view(root)
    actual = (root / VIEW).read_bytes()
    need(len(actual) <= MAX_VIEW_BYTES, "stored view exceeds budget")
    need(json.loads(actual) == expected, "stale or inaccurate recovery view")
    encode(expected)
    return {"status": "PASS", "bytes": len(actual), "state_version": expected["state_version"], "counts": expected["counts"]}

def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)
    elif isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from strings(child)

def matching_terms(raw, obj, terms):
    # Exact, case-sensitive raw JSON or decoded individual strings/keys.
    # No normalization, no fuzzy or semantic identity claim.
    texts = [raw, *strings(obj)]
    return [q for q in terms if any(q in t for t in texts)]

def scan_registry(root, terms, limit=20):
    need(terms and all(isinstance(q, str) and q for q in terms), "nonempty search terms required")
    need(1 <= limit <= 100, "limit must be 1..100")
    # Reuse the full R1 source gate, including evidence and global unique IDs.
    verified = runpy.run_path(str(root / "scripts/verify-historical-source-registry-extensions-r1.py"))["verify"](root)
    manifest = json.loads((root / PATHS["manifest"]).read_bytes())
    specs = [{"path": PATHS["root"], "blob_sha": manifest["root_registry_blob_sha"], "source_count": manifest["root_source_count"]}, *manifest["shards"]]
    hits, totals, records = [], {q: 0 for q in terms}, 0
    total_hits = 0
    for spec in specs:
        raw = (root / spec["path"]).read_bytes()
        need(blob_sha(raw) == spec["blob_sha"], "source changed during search: " + spec["path"])
        obj = json.loads(raw)
        need(len(obj["sources"]) == spec["source_count"], "source count changed")
        records += len(obj["sources"])
        found = matching_terms(raw.decode("utf-8"), obj, terms)
        if found:
            total_hits += 1
            for term in found:
                totals[term] += 1
            if len(hits) < limit:
                hits.append({"path": spec["path"], "blob_sha": spec["blob_sha"], "terms": found})
    need(records == verified["combined_source_count"], "incomplete registry scan")
    return {"status": "PASS", "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY", "files": len(specs), "records": records, "matching_files": total_hits, "per_term_matching_files": totals, "hits": hits, "truncated": total_hits > len(hits)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("build")
    sub.add_parser("verify")
    scan = sub.add_parser("search")
    scan.add_argument("terms", nargs="+")
    scan.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    try:
        if args.action == "build":
            view = make_view(args.root)
            (args.root / VIEW).write_bytes(encode(view))
            result = verify_view(args.root)
        elif args.action == "verify":
            result = verify_view(args.root)
        else:
            result = scan_registry(args.root, args.terms, args.limit)
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as err:
        print(json.dumps({"status": "FAIL", "error": str(err)}, ensure_ascii=False))
        return 1

if __name__ == "__main__":
    sys.exit(main())

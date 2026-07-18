from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

from .repository_release import object_hash, validate_knowledge_manifest, write_object
from .util import FortuneError, read_json, sha256_bytes, sha256_file, utc_now

FORBIDDEN_KEYS = {
    "answer", "answers", "correct_answer", "answer_key", "revealed_answer",
    "correct_option", "ground_truth", "temporary_winner", "current_winner",
    "predicted_winner", "top1", "top2",
}
CLAUSES = {
    "conditions": re.compile(r"(?:若|当|如|须|必须|只有|条件|前提)[^。；;\n]*"),
    "negations": re.compile(r"(?:不得|不能|不可|不等于|并非|无)[^。；;\n]*"),
    "limitations": re.compile(r"(?:仅|只限|上限|限制|不足以|至多)[^。；;\n]*"),
    "exceptions": re.compile(r"(?:除非|例外|但若|然而)[^。；;\n]*"),
    "alternatives": re.compile(r"(?:否则|亦可能|替代|另一|或为)[^。；;\n]*"),
    "counterexamples": re.compile(r"(?:反例|反证|不适用|失配|归零)[^。；;\n]*"),
}
META = re.compile(r"^(SOURCE_FAMILY_ID|METHOD_ID|PATCH_ID|LIBRARY_ROLE|CURRENT_[A-Z0-9_]+_AUTHORITY)\s*=\s*(.+)$", re.M)


def paragraphs(data: bytes) -> Iterable[tuple[int, int, int, int, str]]:
    text = data.decode("utf-8")
    byte_cursor = 0; line_cursor = 1; current: list[str] = []
    start_byte = 0; start_line = 1
    for line in text.splitlines(keepends=True):
        encoded = line.encode("utf-8")
        if line.strip():
            if not current: start_byte, start_line = byte_cursor, line_cursor
            current.append(line)
        elif current:
            yield start_byte, byte_cursor, start_line, line_cursor - 1, "".join(current)
            current = []
        byte_cursor += len(encoded); line_cursor += 1
    if current: yield start_byte, len(data), start_line, line_cursor - 1, "".join(current)


def forbidden_paths(value: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN_KEYS: hits.append(f"{path}.{key}")
            hits.extend(forbidden_paths(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value): hits.extend(forbidden_paths(child, f"{path}[{index}]"))
    return hits


def build_source_catalog(manifest_path: str | Path, source_dir: str | Path,
                         output: str | Path) -> dict[str, Any]:
    validation = validate_knowledge_manifest(manifest_path, source_dir)
    if validation["status"] != "PASS":
        raise FortuneError("knowledge release failed readback", status="SOURCE_CATALOG_PARENT_INVALID")
    manifest = read_json(manifest_path); root = Path(source_dir); entries = []
    for row in manifest["source_files"]:
        path = root / row["canonical_filename"]
        data = path.read_bytes()
        if sha256_bytes(data) != row["sha256_raw_file_bytes"]:
            raise FortuneError(f"source changed: {row['library_id']}", status="SOURCE_HASH_MISMATCH")
        for ordinal, (b0, b1, l0, l1, text) in enumerate(paragraphs(data), 1):
            normalized = " ".join(text.split())
            if not normalized: continue
            meta = {key.lower(): value.strip() for key, value in META.findall(text)}
            entry = {
                "catalog_entry_id": f"{row['library_id']}-K{ordinal:07d}",
                "knowledge_release_id": manifest["knowledge_release_id"],
                "library_id": row["library_id"],
                "canonical_filename": row["canonical_filename"],
                "repository_relative_path": row["repository_relative_path"],
                "source_sha256": row["sha256_raw_file_bytes"],
                "source_size_bytes": row["file_size_bytes"],
                "byte_start": b0, "byte_end": b1, "line_start": l0, "line_end": l1,
                "parent_text": text, "parent_text_sha256": sha256_bytes(text.encode("utf-8")),
                "source_root_atom": re.split(r"[。；;]", normalized, maxsplit=1)[0][:400],
                "source_family_or_method": meta.get("source_family_id") or meta.get("method_id") or meta.get("patch_id"),
                "school_or_method": meta.get("library_role") or meta.get("current_active_control_root_authority") or "UNSPECIFIED_IN_PARENT",
                "capability_ceiling": "AS_STATED_IN_PARENT_TEXT_NO_UPGRADE",
            }
            for name, pattern in CLAUSES.items(): entry[name] = pattern.findall(text)
            entries.append(entry)
    return write_object(output, {
        "schema": "FORTUNE-SOURCE-CATALOG-V1",
        "knowledge_release_id": manifest["knowledge_release_id"],
        "knowledge_manifest_path": Path(manifest_path).as_posix(),
        "knowledge_manifest_sha256": sha256_file(manifest_path),
        "source_count": 20, "entry_count": len(entries), "entries": entries,
        "catalog_role": "LOCATOR_AND_EXACT_PARENT_TEXT_NOT_SUMMARY_AUTHORITY",
        "answer_material_present": False, "created_at": utc_now(),
    })


def _route_rows(plan: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for key, required in (("required_source_family_rows", True), ("conditional_source_family_rows", False)):
        for row in plan.get(key, []):
            if not isinstance(row, dict): continue
            item = dict(row); item["required"] = required; rows.append(item)
    return rows


def _matches(entry: dict[str, Any], route: dict[str, Any]) -> bool:
    lib = route.get("library_id") or route.get("source_library")
    if lib and entry["library_id"] != lib: return False
    entry_ids = route.get("catalog_entry_ids") or route.get("entry_ids")
    if entry_ids and entry["catalog_entry_id"] not in entry_ids: return False
    terms = route.get("query_terms") or route.get("terms") or []
    if isinstance(terms, str): terms = [terms]
    if terms:
        haystack = entry["source_root_atom"] + "\n" + entry["parent_text"]
        if not any(str(term) in haystack for term in terms): return False
    return bool(lib or entry_ids or terms)


def build_source_packet(catalog_path: str | Path, coverage_plan_path: str | Path,
                        case_freeze_path: str | Path, output: str | Path) -> dict[str, Any]:
    catalog = read_json(catalog_path); plan = read_json(coverage_plan_path); case = read_json(case_freeze_path)
    leaks = forbidden_paths(plan) + forbidden_paths(case)
    if leaks: raise FortuneError("answer or winner material in packet inputs: " + ",".join(leaks), status="SOURCE_PACKET_ANSWER_ISOLATION_FAILED")
    routes = _route_rows(plan); entries = catalog.get("entries", []); selected: dict[str, dict[str, Any]] = {}
    receipts = []; unresolved = []
    for index, route in enumerate(routes):
        route_id = route.get("route_id") or f"ROUTE-{index + 1:04d}"
        not_applicable = route.get("status") == "NOT_APPLICABLE_WITH_REASON" and bool(route.get("reason"))
        matches = [] if not_applicable else [entry for entry in entries if _matches(entry, route)]
        for entry in matches: selected[entry["catalog_entry_id"]] = entry
        status = "NOT_APPLICABLE_WITH_REASON" if not_applicable else ("PACKED" if matches else "UNRESOLVED")
        receipts.append({"route_id": route_id, "required": route["required"], "status": status,
                         "reason": route.get("reason"), "catalog_entry_ids": [x["catalog_entry_id"] for x in matches]})
        if route["required"] and status == "UNRESOLVED": unresolved.append(route_id)
    if unresolved: raise FortuneError("required routes unresolved: " + ",".join(unresolved), status="SOURCE_PACKET_REQUIRED_ROUTE_UNRESOLVED")
    items = []
    for entry in sorted(selected.values(), key=lambda row: row["catalog_entry_id"]):
        item = dict(entry); item["packet_item_id"] = "PKT-" + entry["catalog_entry_id"]
        item["packet_item_hash"] = object_hash(item); items.append(item)
    if not items: raise FortuneError("source packet is empty", status="SOURCE_PACKET_EMPTY")
    return write_object(output, {
        "schema": "FORTUNE-SOURCE-PACKET-V1",
        "knowledge_release_id": catalog["knowledge_release_id"],
        "catalog_path": Path(catalog_path).as_posix(), "catalog_sha256": sha256_file(catalog_path),
        "coverage_plan_path": Path(coverage_plan_path).as_posix(), "coverage_plan_sha256": sha256_file(coverage_plan_path),
        "case_freeze_path": Path(case_freeze_path).as_posix(), "case_freeze_sha256": sha256_file(case_freeze_path),
        "case_id": case.get("case_id"), "answer_data_available": False,
        "selection_policy": "COMPLETE_COVERAGE_ROUTES_NO_TEMPORARY_WINNER_FILTER",
        "route_receipts": receipts, "unresolved_required_routes": [],
        "item_count": len(items), "items": items, "created_at": utc_now(),
    })

#!/usr/bin/env python3
"""Fail-closed validation of separately auditable historical source shards."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
MANIFEST = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
REQUIRED = {"source_id", "title", "provider", "url", "historical_period", "source_role", "quality_notes", "physical_glyph_authority", "access_date", "evidence", "verification_status"}

def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def fail(message: str) -> None:
    raise ValueError(message)

def verified_path(root: Path, path: str) -> Path:
    if not isinstance(path, str) or not path.startswith("docs/research/") or not path.endswith(".json"):
        fail("shard path must be a docs/research/*.json file")
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()):
        fail("shard escapes repository root")
    return target

def verify(root: Path) -> dict:
    registry_bytes = (root / BASE).read_bytes()
    registry = json.loads(registry_bytes)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if registry.get("schema") != "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1":
        fail("incorrect root registry schema")
    if manifest.get("schema") != "FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1":
        fail("incorrect shard manifest schema")
    if manifest.get("root_registry") != BASE.as_posix():
        fail("root registry path mismatch")
    root_sha = git_blob_sha(registry_bytes)
    if manifest.get("root_registry_blob_sha") != root_sha:
        fail("root registry changed without extension manifest update")
    root_items = registry.get("sources")
    if not isinstance(root_items, list):
        fail("root registry sources must be an array")
    seen = set()
    for item in root_items:
        sid = item.get("source_id")
        if not isinstance(sid, str) or not sid or sid in seen:
            fail("duplicate/invalid root source id")
        seen.add(sid)
    if manifest.get("root_source_count") != len(root_items):
        fail("root source count mismatch")
    shards = manifest.get("shards")
    if not isinstance(shards, list) or not shards:
        fail("at least one shard is required")
    shard_paths = set()
    count = 0
    for spec in shards:
        path = spec.get("path")
        if path in shard_paths:
            fail("duplicate shard path")
        shard_paths.add(path)
        target = verified_path(root, path)
        raw = target.read_bytes()
        if spec.get("blob_sha") != git_blob_sha(raw):
            fail(f"shard hash mismatch: {path}")
        shard = json.loads(raw)
        if shard.get("schema") != spec.get("schema"):
            fail(f"shard schema mismatch: {path}")
        items = shard.get("sources")
        if not isinstance(items, list) or len(items) != spec.get("source_count"):
            fail(f"shard count mismatch: {path}")
        for item in items:
            if not isinstance(item, dict) or any(not item.get(k) for k in REQUIRED - {"physical_glyph_authority"}):
                fail(f"incomplete source record: {path}")
            if type(item.get("physical_glyph_authority")) is not bool:
                fail("physical_glyph_authority must be an explicit bool")
            if item["physical_glyph_authority"] is not False:
                fail("unreviewed external source shard cannot claim physical glyph authority")
            if item["verification_status"] not in {"RECEIVED_TEXT_VERIFIED", "UNVERIFIED_TARGET_LOCATOR_QUARANTINED", "ACCESS_BOUNDARY_UNVERIFIED", "BIBLIOGRAPHIC_METADATA_ONLY"}:
                fail("unrecognized source verification status")
            sid = item["source_id"]
            if sid in seen:
                fail(f"duplicate source id: {sid}")
            seen.add(sid)
            count += 1
    if manifest.get("extension_source_count") != count:
        fail("extension count mismatch")
    if manifest.get("combined_source_count") != len(seen):
        fail("combined unique count mismatch")
    return {"status": "PASS", "root_source_count": len(root_items), "extension_source_count": count, "combined_source_count": len(seen), "root_registry_blob_sha": root_sha, "shard_count": len(shards)}

def main() -> int:
    try:
        print(json.dumps(verify(ROOT), ensure_ascii=False, sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as err:
        print(json.dumps({"status": "FAIL", "error": str(err)}, ensure_ascii=False))
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

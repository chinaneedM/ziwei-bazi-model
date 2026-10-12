#!/usr/bin/env python3
"""12UN: fail-closed composition of 12UK historical six and two registered 1827 candidates."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENT = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UN-ADDITIONAL-1827-PHYSICAL-COPY-BACKLOG-R1.json"
BASE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"
CONTROL = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UF-SOURCE-READING-CONTROL-AND-IMPRESSION-GATES-R1.json"
REGISTRY = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
OLDER_GATE = ROOT / "scripts/verify-yehuobian-original-leaf-intake-r1.py"
spec = importlib.util.spec_from_file_location("original_leaf_12uk_for_12un", OLDER_GATE)
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)

REQUIRED = {
    "KYOTO_1827_EASTASIAN_200023037620": (
        "EXT-CINII-BB05477307-YEHUOBIAN-1827-FULISHANFANG-KYOTO-EASTASIANHISTORY",
        "https://ci.nii.ac.jp/ncid/BB05477307",
        "BVIb||Y||2 200023037620"),
    "TOKYO_1827_OKI_6403767830": (
        "EXT-CINII-BC0492354X-YEHUOBIAN-1827-TOKYO-DAIMOKU-V20",
        "https://ci.nii.ac.jp/ncid/BC0492354X",
        "大木;子部:雜家類:16-20 6403767830"),
}
def fail(reason):
    raise ValueError(reason)

def validate(data, base, control, registry):
    if data.get("schema") != "TIANWEN-12UN-ADDITIONAL-1827-EXEMPLAR-BACKLOG-R1":
        fail("bad 12UN schema")
    if data.get("historical_vote_authority") != "NONE_INTAKE_ONLY" or data.get("algorithm_reopen_authorized") is not False:
        fail("no historical vote or algorithm reopen authorized")
    if data.get("new_external_source_count") != 0 or data.get("base_candidate_count") != 6 or data.get("new_candidate_count") != 2 or data.get("composite_pending_candidate_count") != 8:
        fail("snapshot vs new source count mismatch")
    if len(base.get("candidates", [])) != 6:
        fail("12UK six-item historical snapshot changed")
    registered = {x["source_id"]: x for x in registry.get("sources", [])}
    adds = data.get("candidates", [])
    if len(adds) != 2 or {x.get("id") for x in adds} != set(REQUIRED):
        fail("two precise already-registered candidates required")
    old_ids = {x.get("id") for x in base["candidates"]}
    old_objects = {x.get("object_identifier") for x in base["candidates"]}
    for a in adds:
        id_ = a["id"]
        registered_id, url, object_id = REQUIRED[id_]
        if id_ in old_ids or object_id in old_objects:
            fail("new candidate duplicates historical object")
        if (a.get("source_registry_id"), a.get("catalog_url"), a.get("object_identifier")) != (registered_id, url, object_id):
            fail("catalog item/source binding does not match registry")
        r = registered.get(registered_id)
        if r is None or r["url"] != url or r.get("physical_glyph_authority") is not False:
            fail("original existing catalog registration missing or miscast as glyph")
        if a.get("stage") != "CATALOG_ONLY" or a.get("historical_vote") is not False or a.get("verified_unrepaired_1827_original") is not False:
            fail("only unverified catalog lead allowed")
        if a.get("historical_volume_arrangement") != "THEMATIC_30":
            fail("old chronological and thematic volume20 confused")
        if "卷20" not in a.get("volume_binding", ""):
            fail("missing exact juan20 book scope")
        if any(v is not None for v in a.get("four_locus_readings", {}).values()):
            fail("no original characters may be filled without acquisition")
    combined = dict(base)
    combined["candidates"] = base["candidates"] + adds
    outcome = original.validate(combined, control)
    if outcome["candidate_count"] != 8 or outcome["captured_images"] != 0 or outcome["independent_ancient_glyph_votes"] != 0:
        fail("composite intake is not fail-closed")
    if any(data.get("acquisition", {}).get(k) is not False for k in ("first_impression_1827_proven", "original_1869_repair_leaf_proven", "item_issued_manifest_found", "outreach_sent", "paid_copy_order_placed")):
        fail("an unverified acquisition is asserted")
    if data.get("acquisition", {}).get("original_image_count") != 0 or data.get("acquisition", {}).get("ancient_glyph_votes") != 0:
        fail("no original images or glyph votes acquired")
    y = data.get("prior_known_but_not_queued", {})
    if y.get("registry_id") != "EXT-CINII-BC08398372-YEHUOBIAN-TOKYO-1827-V19-LACUNA" or y["registry_id"] not in registered or y.get("new_source") is not False:
        fail("old lower-priority holding must not be newly counted")
    return {"status": "PASS", "old_candidates": 6, "incremental_candidates": 2, "total_pending_objects": 8, "new_external_sources": 0, "ancient_glyph_votes": 0}

def verify(root=ROOT):
    def load(p):
        return json.loads((root / p).read_text(encoding="utf-8"))
    return validate(load("docs/research/MING-DATONG-YEHUOBIAN-12UN-ADDITIONAL-1827-PHYSICAL-COPY-BACKLOG-R1.json"),
                    load("docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"),
                    load("docs/research/MING-DATONG-YEHUOBIAN-12UF-SOURCE-READING-CONTROL-AND-IMPRESSION-GATES-R1.json"),
                    load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"))

if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, sort_keys=True))

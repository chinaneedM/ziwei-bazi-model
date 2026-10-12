#!/usr/bin/env python3
"""Structural, fail-closed intake for Yehuobian juan 20 physical-leaf candidates.

This gate cannot authenticate a physical original. Even a structurally complete
image record must be manually adjudicated before entering the historical graph.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = "docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"
CONTROL = "docs/research/MING-DATONG-YEHUOBIAN-12UF-SOURCE-READING-CONTROL-AND-IMPRESSION-GATES-R1.json"
LOCI = ("GONGJIN", "CLOCK_NOUN", "BEIJING_WINTER_SUNRISE", "BEIJING_SUMMER_SUNSET")
STAGES = ("CATALOG_ONLY", "DIGITIZATION_PLAN_ONLY", "IMAGE_CAPTURED", "PRINT_STATE_CANDIDATE")

def reject(reason):
    raise ValueError(reason)

def digest(v):
    return isinstance(v, str) and len(v) == 64 and all(x in "0123456789abcdef" for x in v)

def validate(data, control):
    if data.get("schema") != "TIANWEN-12UK-ORIGINAL-LEAF-INTAKE-R1":
        reject("wrong intake schema")
    if data.get("historical_vote_authority") != "NONE_INTAKE_ONLY":
        reject("intake queue cannot cast original glyph votes")
    if data.get("algorithm_reopen_authorized") is not False:
        reject("chart algorithm reopen is prohibited")
    if tuple(control.get("locus_order", [])) != LOCI:
        reject("unexpected canonical locus order")
    known_sha = {s["sha256"] for s in control["source_surfaces"]}
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        reject("missing candidate records")
    ids = set()
    images = 0
    print_states = 0
    for c in candidates:
        if not isinstance(c, dict) or not isinstance(c.get("id"), str) or not c["id"] or c["id"] in ids:
            reject("duplicate or invalid candidate ID")
        ids.add(c["id"])
        stage = c.get("stage")
        if stage not in STAGES:
            reject("unknown candidate stage")
        if not all(isinstance(c.get(k), str) and c[k].strip() for k in ("catalog_url", "object_identifier", "holder", "date_scope")):
            reject("incomplete source-issued catalog identity")
        if not c["catalog_url"].startswith("https://"):
            reject("source-issued catalog URL required")
        if c.get("historical_vote") is not False or c.get("verified_unrepaired_1827_original") is not False:
            reject("staging records cannot claim an ancient witness or first impression")
        if c.get("historical_volume_arrangement") not in ("THEMATIC_30", "UNBOUND"):
            reject("chronological old20 and thematic30 cannot be equated")
        loci = c.get("four_locus_readings")
        if not isinstance(loci, dict) or set(loci) != set(LOCI):
            reject("four labeled, independent loci required")
        source_sha = c.get("source_binary_sha256")
        image_url = c.get("source_issued_image_url")
        pages = c.get("pages")
        if not isinstance(pages, list):
            reject("pages must be a list")
        if stage in ("CATALOG_ONLY", "DIGITIZATION_PLAN_ONLY"):
            if source_sha is not None or image_url is not None or pages or any(v is not None for v in loci.values()):
                reject("catalog/plan cannot carry unacquired images or glyphs")
            if c.get("target_original_folio") is not None or c.get("printing_state_evidence") is not None:
                reject("catalog cannot determine original folio or print state")
            continue
        images += 1
        if not digest(source_sha) or not isinstance(image_url, str) or not image_url.startswith("https://"):
            reject("image capture requires source-issued URL and 64-character source hash")
        if not pages or any(not isinstance(p, dict) or not isinstance(p.get("page_label"), str) or not p["page_label"] or not digest(p.get("sha256")) for p in pages):
            reject("image capture requires hashed page images")
        if len({p["page_label"] for p in pages}) != len(pages):
            reject("duplicate page identifiers")
        if not isinstance(c.get("target_original_folio"), str) or not c["target_original_folio"].strip():
            reject("image capture requires original target folio identity")
        if c.get("relationship_to_prior_surfaces") not in ("SAME_DIGITAL_OBJECT", "DISTINCT_BYTES_RELATION_UNRESOLVED", "RECHECK_REQUIRED"):
            reject("no inferred physical copy independence")
        if source_sha in known_sha and c["relationship_to_prior_surfaces"] != "SAME_DIGITAL_OBJECT":
            reject("known control binary must be treated as an existing digital object")
        if any(v is not None and not isinstance(v, str) for v in loci.values()):
            reject("glyphs must be strings or unread/null")
        if stage == "IMAGE_CAPTURED":
            if c.get("printing_state_evidence") is not None:
                reject("image capture must not assert print state")
        else:
            print_states += 1
            proof = c.get("printing_state_evidence")
            if not isinstance(proof, dict) or not digest(proof.get("source_page_sha256")) or proof.get("adjudication") != "MANUAL_REVIEW_PENDING":
                reject("printing state claims require page-scoped pending manual adjudication")
            if not isinstance(proof.get("dated_paratext_quotation"), str) or not proof["dated_paratext_quotation"].strip():
                reject("must point to image-backed edition paratext, not catalog year")
    return {"status": "PASS", "candidate_count": len(candidates), "captured_images": images,
            "print_state_candidates": print_states, "independent_ancient_glyph_votes": 0,
            "historical_control_surfaces": len(known_sha)}

def verify(root=ROOT):
    data = json.loads((root / QUEUE).read_text(encoding="utf-8"))
    control = json.loads((root / CONTROL).read_text(encoding="utf-8"))
    return validate(data, control)

if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, sort_keys=True))

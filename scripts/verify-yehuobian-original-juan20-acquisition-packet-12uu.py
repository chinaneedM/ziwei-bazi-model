#!/usr/bin/env python3
"""Ensure original folio acquisition plan never becomes a historical vote or permission."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = "docs/research/MING-DATONG-YEHUOBIAN-12UU-ORIGINAL-JUAN20-ACQUISITION-PACKET-R1.json"
BASE = "docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"
EXTRA = "docs/research/MING-DATONG-YEHUOBIAN-12UN-ADDITIONAL-1827-PHYSICAL-COPY-BACKLOG-R1.json"
DAMAGED = "docs/research/MING-DATONG-YEHUOBIAN-12UT-TOKYO-YURAN-DAMAGED-COPY-GATE-R1.json"
LOCI = {"GONGJIN", "CLOCK_NOUN", "BEIJING_WINTER_SUNRISE", "BEIJING_SUMMER_SUNSET"}
EXPECTED_GROUPS = {"KYOTO":2,"TOKYO_IOC":2,"HOKKAIDO":1,"TSUKUBA":1,"NDL":1,"NAJ":1}

def validate(packet, base, extra, damaged):
    if packet.get("schema") != "TIANWEN-12UU-SOURCE-BOUND-JUAN20-ACQUISITION-PACKET-R1":
        raise ValueError("schema")
    targets = base["candidates"] + extra["candidates"]
    data = packet.get("original_copy_candidates")
    if len(targets) != 8 or not isinstance(data, list) or len(data) != 8:
        raise ValueError("must retain exactly eight actionable prior candidates")
    target_by_id = {x["id"]:x for x in targets}
    if len(target_by_id) != 8 or {x.get("queue_id") for x in data} != set(target_by_id):
        raise ValueError("candidate source identity does not match prior queue")
    priorities = [x.get("priority") for x in data]
    if priorities != list(range(1,9)):
        raise ValueError("stable priority sequence")
    groups = {g["institution"]:g["candidate_count"] for g in packet.get("source_groups", [])}
    if groups != EXPECTED_GROUPS:
        raise ValueError("unverified or omitted holding group")
    for row in data:
        before = target_by_id[row["queue_id"]]
        if row["source_catalog_url"] != before["catalog_url"] or row["source_issued_item_identifier"] != before["object_identifier"]:
            raise ValueError("original source identifier drift")
        if row["prior_stage"] != before["stage"] or row["prior_stage"] not in ("CATALOG_ONLY","DIGITIZATION_PLAN_ONLY"):
            raise ValueError("image-stage promotion without evidence")
        if row["prior_stage"] == "DIGITIZATION_PLAN_ONLY" and row["date_class"] != "DIGITIZATION_PLAN_ONLY_AND_V20_UNBOUND":
            raise ValueError("unbound planned scan is not an existing original volume")
        if row["queue_id"] == "TOKYO_1869_6403148395" and row["date_class"] != "CATALOGUED_1869_REVISED_IMPRESSION_UNVERIFIED":
            raise ValueError("1869 revised status must not collapse into 1827 preface")
        if row["queue_id"] == "TSUKUBA_V20_10076865665" and row["date_class"] != "PRINT_YEAR_UNBOUND_10X23_DIFFERENT_SETTING":
            raise ValueError("10x23 branch cannot be silently relabeled as 1827 10x21")
        if row["queue_id"] == "KYOTO_1827_188987L" and "188987" not in row["print_paratext_to_verify"]:
            raise ValueError("188987 opening fascicle must remain distinct from 188987L target")
        if any(row.get(k) is not None for k in ("original_target_folio","source_issued_original_image_url","source_binary_sha256","page_sha256")):
            raise ValueError("uncaptured original image or folio")
        if set(row.get("four_locus_readings",{})) != LOCI or any(v is not None for v in row["four_locus_readings"].values()):
            raise ValueError("no historical glyph votes from catalog")
        if any(row.get(k) is not False for k in ("user_contact_or_institutional_action_already_authorized","item_specific_copy_permission_obtained","fee_quote_obtained","query_sent","available_public_original_image_confirmed","confirmed_original_1827_first_print","confirmed_1869_repair_plate","confirmed_independent_physical_text_vote")):
            raise ValueError("unauthorized permission, impression or independent glyph inference")
        if len(row.get("required_capture",[])) != 6 or "source-issued repository item ID" not in row["required_capture"][0]:
            raise ValueError("missing source-linked image and original folio capture requirements")
    e = packet.get("exclusion_control",{})
    if e.get("damaged_copy_source") != damaged["physical_copy"]["catalog_url"] or e.get("damaged_copy_item") != damaged["physical_copy"]["source_issued_identifier"]:
        raise ValueError("damaged Yuran item binding")
    if any(x["source_issued_item_identifier"] == e["damaged_copy_item"] for x in data):
        raise ValueError("catalogued unavailable damaged item promoted as actionable")
    for k in ("counted_in_eight_actionable_candidates","irreparable_or_deleted_volume20_proven","inherited_old20_manuscript_counts_as_1827_edition","preface_1827_proves_1827_print_state","received_text_or_OCR_is_original_leaf","source_catalogue_is_copyright_copy_permission","external_requests_submitted","fees_paid"):
        if e.get(k) is not False:
            raise ValueError("unsafe evidence or authorization inference: " + k)
    c = packet.get("null_evidence_accounting",{})
    for k in ("original_physical_1827_image_pages","original_physical_1869_image_pages","new_original_glyph_votes","new_external_source_registry_items","formal_batches_advanced","algorithm_reopens"):
        if c.get(k) != 0:
            raise ValueError("unearned provenance or algorithm count: " + k)
    if (c.get("source_registry_total"),c.get("matrix_rows"),c.get("audited_rows"),c.get("metadata_repairs"),c.get("transmission_graph_nodes"),c.get("transmission_graph_edges")) != (687,222,222,45,250,237):
        raise ValueError("project accounting unexpectedly moved")
    return {"status":"PASS","catalogued_actionable_candidates":len(data),"institution_groups":len(groups),"original_pages":0,"independent_glyph_votes":0}

def verify(root=ROOT):
    def load(p):return json.loads((root/p).read_text(encoding="utf-8"))
    return validate(load(DATA),load(BASE),load(EXTRA),load(DAMAGED))

if __name__ == "__main__":
    print(json.dumps(verify(),sort_keys=True))

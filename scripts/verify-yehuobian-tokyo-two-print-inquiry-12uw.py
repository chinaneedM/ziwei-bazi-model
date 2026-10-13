#!/usr/bin/env python3
"""Tokyo 1827 / 1869 item-specific manuscript/print inquiries: never treat preflight as images."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/research/MING-DATONG-YEHUOBIAN-12UW-TOKYO-IOC-TWO-PRINT-INQUIRY-R1.json"
PACKET = "docs/research/MING-DATONG-YEHUOBIAN-12UU-ORIGINAL-JUAN20-ACQUISITION-PACKET-R1.json"
EXPECTED = {
    ("TOKYO_1827_OKI_6403767830", "BC0492354X", "6403767830", "卷20", "CATALOGUED_1827_IMPRESSION_UNVERIFIED"),
    ("TOKYO_1869_6403148395", "BB23196128", "6403148395", "卷19-20", "CATALOGUED_1869_REVISED_IMPRESSION_UNVERIFIED"),
}
FOUR = {"GONGJIN", "CLOCK_NOUN", "BEIJING_WINTER_SUNRISE", "BEIJING_SUMMER_SUNSET"}
GUARDS = (
    "2026_library_branch_status_not_copy_specific_service_permission",
    "2023_reservation_guide_not_assumed_updated_2026_policy",
    "university_opac_and_cinii_holdings_not_original_target_images",
    "lecture_notes_archive_not_kuraishi_rare_book_scan",
    "2009_shanben_A_B_scope_not_item_inclusion_or_2026_access",
    "1827_preface_in_1869_copy_not_1827_print_impression",
    "1827_printed_target_not_verified_from_catalog_date",
    "1869_juan20_target_not_verified_from_colophon",
    "two_catalog_items_not_two_independent_glyph_votes",
    "condition_damage_not_juan20_leaf_absence",
    "special_rare_book_form_only_if_item_classification_requires",
    "no_print_plate_identity_inferred_from_ten_by_twenty_one_grid",
    "no_online_IIIF_manifest_unless_item_link_emitted",
    "no_contact_or_order_submitted",
    "no_algorithm_reopen",
)
def validate(record, packet):
    if record.get("schema") != "TIANWEN-12UW-TOKYO-IOC-TWO-PRINT-INQUIRY-GATE-R1" or record.get("status") != "DRAFT_NOT_SENT":
        raise ValueError("schema or status")
    items = record.get("physical_targets", [])
    if len(items) != 2 or {(x.get("queue_id"), x.get("ncid"), x.get("item"), x.get("volume"), x.get("date_class")) for x in items} != EXPECTED:
        raise ValueError("physical catalog item bindings")
    prior = {x["queue_id"]:x for x in packet.get("original_copy_candidates", [])}
    if len(prior) != 8:
        raise ValueError("prior packet cardinality")
    for x in items:
        p = prior.get(x["queue_id"])
        if not p or x["item"] not in p["source_issued_item_identifier"] or x["volume"] not in p["original_target_scope"]:
            raise ValueError("prior source copy crosswalk")
        if x["catalog_url"] != "https://ci.nii.ac.jp/ncid/" + x["ncid"]:
            raise ValueError("bibliographic URL not copy-specific")
        if (x.get("original_folio"), x.get("source_issued_image_url"), x.get("source_binary_sha256"), x.get("target_page_sha256")) != (None,None,None,None):
            raise ValueError("unevidenced image/folio hash")
        if x.get("physical_impression_verified") is not False or x.get("copy_specific_permission") is not False or x.get("source_glyph_votes") != 0:
            raise ValueError("unevidenced print, permission or glyph vote")
        if set(x.get("readings", {})) != FOUR or any(v is not None for v in x["readings"].values()):
            raise ValueError("four source-bound glyphs must be pending")
    roles = {x.get("role"): x.get("url") for x in record.get("authority_sources", [])}
    required = {"1827_OKI_COPY_BIBLIOGRAPHIC_ITEM","1869_KURAISHI_COPY_BIBLIOGRAPHIC_ITEM",
                "CURRENT_INSTITUTIONAL_LIBRARY_SERVICE_AND_2026_BRANCH_STATUS",
                "CURRENT_SPECIAL_RARE_BOOK_AND_COPY_APPLICATION_CONDITIONS",
                "LINKED_RESERVATION_GUIDANCE_LAST_REVISED_2023",
                "KURAISHI_LECTURE_NOTES_NOT_KURAISHI_ANCIENT_BOOKS"}
    if not required <= set(roles):
        raise ValueError("source authority roles")
    if roles["KURAISHI_LECTURE_NOTES_NOT_KURAISHI_ANCIENT_BOOKS"] != "https://kuraishi.ioc.u-tokyo.ac.jp/about_system.html":
        raise ValueError("Kuraishi lecture-notes exclusion")
    if any(record.get("scope_firewalls",{}).get(k) is not True for k in GUARDS):
        raise ValueError("bibliographic or permission safety boundary")
    if len(record.get("source_scoped_questions", [])) != 5:
        raise ValueError("source-dependent unanswered questions")
    if any(record.get("external_actions",{}).get(k) is not False for k in ("sent","reading_reservation","reproduction_order","fees_paid","item_specific_permission_obtained")):
        raise ValueError("outside communication or service was not authorized/executed")
    if any(record.get("acquisition",{}).get(k) != 0 for k in ("new_original_target_images","new_target_glyph_votes","new_historical_source_registry_rows","printing_state_determinations")):
        raise ValueError("unsupported original text or copy upgrade")
    a=record.get("accounting",{})
    if tuple(a.get(k) for k in ("matrix_rows","audited","metadata_repairs","sources_root","sources_extensions","sources_total","genealogy_nodes","genealogy_edges","formal_batches","latest_formal","product","algorithm_reopens")) != (222,222,45,647,40,687,250,237,487,"12QD","CLOSED",0):
        raise ValueError("handoff counters changed without corresponding evidence")
    return {"status":"PASS","item_bound_print_candidates":2,"contacts_sent":0,"original_images":0,"historical_glyph_votes":0}
def verify(root=ROOT):
    def get(p):return json.loads((root/p).read_text(encoding="utf-8"))
    return validate(get(RECORD),get(PACKET))
if __name__ == "__main__":
    print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))

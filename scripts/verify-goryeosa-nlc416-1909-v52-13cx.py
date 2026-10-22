#!/usr/bin/env python3
"""13CX: explicit 1909 NLC scan TOC for v52, not scanned D16 glyph or independent ancient original."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CX-GORYEOSA-NLC416-1909-V52-IMAGE-OBJECT-TARGET-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(path):return json.loads((R/path).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CX-GORYEOSA-NLC416-1909-V52-IMAGE-OBJECT-TARGET-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 p=e["publication_and_digital_surrogate"]
 assert p["source_page"].endswith("NLC416-13jh005095-74760_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf")
 assert p["original_file_link"].startswith("https://upload.wikimedia.org/wikipedia/commons/6/63/NLC416-13jh005095")
 assert p["record_class"]=="COMMONS_MIRROR_METADATA_NOT_DIRECT_NLC_FIRSTPARTY_ITEM_DETAIL"
 assert (p["printed_publication_year"],p["published_by"],p["digital_pdf_pages"],p["printed_content_paginated"])==(1909,"市島謙吉",755,746)
 assert p["content_page_offset_from_pdf"]=="UNBOUND_NO_SUBTRACT_9_RULE"
 assert p["source_bytes_downloaded_in_this_batch"] is False
 assert p["digital_pdf_sha256"]=="UNBOUND" and p["source_folio_and_target_day16_glyph"]=="NOT_VISUALLY_COLLATED"
 x=e["positive_concrete_volume_locator"]
 assert x["index_scope"]=="COMMONS_MIRROR_DESCRIPTIVE_TABLE_OF_CONTENTS"
 assert (x["textual_boundary"],x["item_order"],x["work_juan"],x["genre_juan"],x["title"])==("志三十九卷",6,52,6,"曆三")
 assert x["adjacent_entries"]==[{"ordinal":5,"work_juan":51,"title":"曆二"},{"ordinal":7,"work_juan":53,"title":"五行一"}]
 assert x["index_printed_not_target_image"] and x["v52_located_at_volume_manifest_level"]
 assert x["v52_exact_pdf_page"] is None
 assert e["nearby_series_edition_controls"][0]["catalog_start_juan"]==88
 assert e["nearby_series_edition_controls"][1]["catalog_start_juan"]==47
 assert "NOT_TARGET" in e["nearby_series_edition_controls"][0]["status"]
 z=e["cross_source_firewall"]
 assert z["ndl_and_nlc_same_printing_batch"]=="UNDETERMINED"
 assert z["ndl_and_nlc_same_physical_copy"]=="NOT_PROVEN"
 assert z["nlc1909_new_independent_early_original"] is False
 assert z["krdb_official_received_d16"]==z["prior_waseda_naj_direct_historical_original_d16"]=="5.1362"
 assert z["derived_math_candidate_only"]=="5.2362"
 assert z["ncl_taiwan_208_03130_original_folio"]==z["ncl_taiwan_1905_hand"]=="UNBOUND"
 assert z["do_not_infer_d16_from_table_of_contents"] and z["do_not_compute_print_pdf_page_offset_from_counts"]
 t=e["transmission_impact"]
 assert not t["nodes_added_or_strengthened"] and not t["edges_supported"] and not t["edges_revised"]
 c=e["counts"]
 assert (c["matrix_rows"],c["audited_rows"],c["registered_sources"],c["graph_nodes"],c["graph_edges"],c["unresolved_risks"],c["new_early_physical_witnesses"],c["algorithm_reopens"],c["deterministic_product"])==(222,222,754,252,238,11,0,0,"CLOSED")
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13CX ") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"] and "docs/research/TIANWEN-13CX-GORYEOSA-NLC416-1909-V52-IMAGE-OBJECT-TARGET-R1.md" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13CX-NLC416-1909-V52-TARGET-VOLUME" for x in issue["history"])
 assert "CURRENT ACTION:" in issue["next_action"]
 assert any(x.get("id")=="OMISSIONS-13CX-NLC416-1909-V52-TARGET-VOLUME-20261022" for x in l["checkpoint_log"])
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13CX_1909_NLC416_TARGET_V52_TABLE_OF_CONTENTS_BOUNDARY=PASS")

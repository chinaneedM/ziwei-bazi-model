#!/usr/bin/env python3
"""13CR: check NCL 03130 public digital part intake without claiming primary folios."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CR-NCL03130-COMMONS-24PART-FRONT-INTAKE-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,s,l):
    assert e["schema"]=="TIANWEN-13CR-NCL03130-COMMONS-DIGITAL-PART-INVENTORY-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    assert e["previous_checkpoint"]=="docs/research/TIANWEN-13CQ-GORYEOSA-NCL03130-MISSING-JUAN-1905-STRATA-R1.json"
    assert e["mirror_part_count"]==24
    parts=e["mirror_parts"]
    assert len(parts)==24 and [x["part"] for x in parts]==[f"{i:02}" for i in range(1,25)]
    assert [x["commons_pdf_pages"] for x in parts]==[204,201,198,208,189,189,187,189,189,198,180,188,178,182,187,155,163,172,168,166,171,176,168,73]
    assert all(x["source_scope"]=="COMMONS_CATEGORY_LISTING_ONLY" for x in parts)
    assert e["exemplar_caption"]["historical_book_count_reported"]==40
    assert e["exemplar_caption"]["authority"].startswith("COMMONS_REPRODUCED_")
    front=e["priority_front_part"]
    assert front["part"]=="01" and front["pages_catalog_listing"]==204
    assert front["is_register_known_on_this_part"] is False
    assert front["image_obtained"] is False and front["pdf_sha256"] is None
    m=e["mismatch_firewall"]
    for k in ["mirror_part_count_is_physical_book_count","part_numbers_establish_juan_mapping","pdf_part_08_proves_juan52","red_register_directly_read"]:
        assert m[k] is False
    assert m["juan52_missing_membership"]=="UNRESOLVED" and m["juan52_original_layer"]=="UNBOUND"
    assert m["digital_surrogate_to_firstparty_original_link"]=="UNBOUND"
    assert m["native_original_d16_glyphs_new"]==m["third_independent_historical_d16_copy_votes"]==0
    assert m["verified_historical_numeric_d16_original"]=="5.1362" and m["arithmetic_conjecture_not_original"]=="5.2362"
    a=e["proposed_acquisition"]
    assert a["workflow"]==".github/workflows/acquire-ncl03130-front-13cr.yml"
    assert a["manual_page_review_required"] and a["direct_red_list_claim_requires_original_image_hash"]
    assert not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["nodes_added_or_strengthened"]
    c=e["counts"]
    assert (c["historical_audit_rows"],c["source_registry_count"],c["genealogy_nodes"],c["genealogy_edges"],c["open_or_blocked_risks"],c["algorithm_reopens"],c["product"])==(222,754,252,238,11,0,"CLOSED")
    assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
    assert s["historical_audit"]["external_source_registry_total_unique_count"]==s["historical_audit"]["external_source_registry_root_count"]+s["historical_audit"]["external_source_registry_extension_count"]
    assert s["invariants"]["algorithm_reopen_count"]==0 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    assert any(x.startswith("13CR ") for x in s["historical_audit"]["current_focus"])
    assert l["binding"]["reviewed_state_version"]==s["schema_version"]
    assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
    risk=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
    assert risk["status"]=="OPEN" and E in risk["source_refs"]
    assert any(x.get("revision_id")=="TW-OPEN-0005-13CR-COMMONS-PARTS" for x in risk["history"])
    assert any(x["id"]=="OMISSIONS-13CR-COMMONS-24PART-20261022" for x in l["checkpoint_log"])
    assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
    return True
if __name__=="__main__":
    assert check(load(E),load(S),load(L))
    print("TIANWEN_13CR_PUBLIC_24PART_ACQUISITION_INDEX=PASS; ORIGINAL_RED_REGISTER_UNREAD")

#!/usr/bin/env python3
"""12WB secondary Wenzhou holding route: no original print or glyph entitlement."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WB-WENZHOU-1827-1869-HOLDING-LEAD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"

def ensure(ok, message):
    if not ok:
        raise ValueError(message)

def validate(rec, state):
    ensure(rec["schema"]=="TIANWEN-12WB-WENZHOU-1827-1869-MIXED-EDITION-SECONDARY-LEAD-R1","schema")
    ensure(rec["status"]=="SECONDARY_ITEM_UNVERIFIED_ACCESS_ROUTE_ONLY_NOT_ADMITTED_AS_PHYSICAL_WITNESS","status")
    s=rec["secondary_catalogue"]
    ensure(s["url"]=="https://m.guoxuedashi.com/shumu/gj-1392143zp.html","secondary URL")
    ensure(s["literal_version"]=="清道光七年（1827）錢塘姚氏羊城扶荔山房刻同治八年（1869）補刻本","mixed edition wording")
    ensure(s["claimed_holding"]=="溫州市圖書館" and s["literal_volume_count"]=="20册","holding claim")
    ensure(s["item_specific_official_confirmation"] is False and s["original_target_page_attestation"] is False,"no false official item")
    a=rec["first_party_access"]
    ensure(a["official_homepage"]=="https://www.wzlib.cn/" and a["exact_title_item_page_observed"] is False,"first-party homepage vs holding")
    ensure(a["opac_probe_result"]=="TIMEOUT_FROM_CURRENT_WEB_ENVIRONMENT" and a["opac_timeout_not_negative_catalogue_result"] is True,"scoped OPAC boundary")
    ensure(all(a[k] is False for k in ("exact_shelfmark_observed","contact_attempted","reproduction_requested","permission_granted")),"no external action")
    t=rec["physical_target_gate"]
    for k in ("physical_object_accession","copy_shelfmark","target_juan20_page","folio_number","provider_issued_image_url","original_source_binary_sha256","target_page_image_sha256"):
        ensure(t[k] is None,"physical folio not obtained")
    ensure(t["edition_impression_on_target_copy"]=="UNBOUND" and t["independent_1827_versus_1869_glyph_votes"]==0,"no print comparison")
    ensure(all(v is None for v in t["four_loci"].values()) and len(t["four_loci"])==4,"no glyph votes")
    ensure(t["composite_1827_and_1869_description_not_proof_of_two_complete_comparators"] is True and t["copy_cannot_be_counted_as_certified_ninth_candidate"] is True,"no copy inflation")
    x=rec["crosswalk"]
    ensure(x["preexisting_eight_item_packet"]=="12UU" and x["add_to_existing_eight_verified_item_bound_candidates"] is False and x["new_registry_source"] is False,"eight item packet unchanged")
    v=rec["accounting"]
    h=state["historical_audit"]
    ensure((v["matrix_total"],v["audited"],v["metadata_defects_repaired"]) == (h["row_count"],h["audited_row_count"],h["repaired_provenance_metadata_defect_count"]),"matrix")
    ensure(v["external_registry_union"]<=h["external_source_registry_total_unique_count"] and v["genealogy_nodes"]==252 and v["genealogy_edges"]==238,"no source/graph growth")
    ensure(v["formal_batches"]<=len(h["completed_batches"]) and v["algorithm_reopens"]==0 and v["product_r1"]=="CLOSED","no algorithm reopen")
    ensure(rec["transmission_impact"]["edges_supported"]==[] and v["new_direct_copy_lineage_edges"]==0,"no genealogy fabrication")
    ensure(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product not reopened")
    return {"status":"PASS","wenzhou_official_item_verified":False,"new_independent_print_votes":0,"secondary_lead_only":True}

def verify():
    return validate(json.loads((ROOT/REC).read_text()),json.loads((ROOT/STATE).read_text()))

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False))

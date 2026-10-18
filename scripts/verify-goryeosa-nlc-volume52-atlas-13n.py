#!/usr/bin/env python3
"""13N bounded scan atlas: do not confuse PDF group number, edition, folio or glyph."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13N-NLC-411999022809-V52-FASCICLE-ATLAS-R1.json"
def read(p): return json.loads((R/p).read_text(encoding="utf-8"))
def check(e):
 assert e["schema"]=="TIANWEN-13N-NLC411999022809-VOLUME52-FASCICLE-SCOPED-CANDIDATES-R1"
 a=e["scope"]; c=e["scan_atlas"]; n=e["adjudication"]; o=e["existing_prior_witness"]; v=e["cadal_misleading_title_control"]
 assert a["target_work_volume"]==52 and a["digital_proxy_series_id"]=="411999022809"
 assert a["physical_copy_binding"]=="NLC_FIRST_PARTY_ITEM_NOT_VERIFIED"
 assert a["root_source_registry_count"]==647 and a["extension_source_registry_count"]==87 and a["combined_registry_count"]==734
 assert o["cadal_container_id"]=="CADAL02050311" and o["cadal_container_number"]==49 and o["existing_source_id"]=="EXT-COMMONS-CADAL-GORYEOSA-V52-FACSIMILE" and o["recreate_source"] is False
 assert v["cadal_container_id"]=="CADAL02050314" and v["displayed_container_number"]==52 and v["suggested_internal_work_volume"]==55
 assert v["original_image_verified_this_batch"] is False and v["may_vote_on_work52"] is False and v["adjudicated_not_work52"] is False
 assert c["scan_band_status"]=="SEARCH_HYPOTHESIS_NONEXHAUSTIVE" and c["exact_file_names_from_commons_inventory"] is True
 assert c["first_pass_groups"]==list(range(36,44)) and c["boundary_control_groups"]==[33,34,35,44,45]
 records=c["records"]
 assert len(records)==13 and [x["digital_group"] for x in records]==list(range(33,46))
 expected=["48403","48404","48405","48457","48453","48454","48455","48456","48499","48500","48501","48502","48548"]
 for item,num in zip(records,expected):
  assert item["locator_id"]=="411999022809-"+num and str(item["digital_group"])+"冊.pdf" in item["commons_file_title"]
  assert item["first_party_item_verified"] is False and item["contains_target_work_volume52"] is None
  assert all(item[k] is None for k in ["work_volume_numbers_originally_read","target_page_number","source_pdf_sha256","source_page_sha256","d16_original_glyph","d18_original_glyph"])
  assert item["numeric_witness_vote"] is False
 assert e["nlc_sources"]["first_party_nlc_catalog_confirmed"] is False
 assert [(x["digital_group"],x["proxy_description"]) for x in e["external_context_anchors"]]==[(54,"卷之二十五 志"),(70,"卷之七 列傅")]
 assert all(x["page_image_verified"] is False for x in e["external_context_anchors"])
 assert n["exact_target_nlc_digital_group"] is None and n["exact_target_nlc_page"] is None
 for key in ["verified_new_work52_scan_page","verified_target_source_image_sha"]: assert n[key] is False
 for key in ["new_source_registry_records","original_glyph_votes_added","independent_copy_numeric_votes_added","algorithm_reopens","transmission_edges_added"]: assert n[key]==0
 assert n["previous_g893_direct_target_controls"]==5 and n["previous_g893_target_control_count"]==6 and n["previous_g893_independent_crosscopy_controls"]==0
 assert n["open_research_issues"]==11 and n["product_r1"]=="CLOSED"
def verify():
 e=read(E);check(e)
 s=read("docs/PROJECT-CURRENT-STATE-R1.json");l=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 m=read("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
 rr=read("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
 assert any(x["source_id"]=="EXT-COMMONS-CADAL-GORYEOSA-V52-FACSIMILE" for x in rr["sources"])
 assert m["root_source_count"]==647 and m["extension_source_count"]==87 and m["combined_source_count"]==734
 assert s["schema_version"]=="1.674.0" and s["historical_audit"]["external_source_registry_total_unique_count"]==734
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert s["historical_audit"]["current_focus"][-1].startswith("13N ") and l["binding"]["latest_research_focus_prefix"]=="13N"
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in [E,"docs/research/TIANWEN-13N-NLC-411999022809-V52-FASCICLE-ATLAS-R1.md"])
 assert len(l["issues"])==11 and {x["id"] for x in l["issues"]}==set(l["checkpoint_log"][-1]["reviewed_issue_ids"])
 assert l["checkpoint_log"][-1]["state_version"]=="1.674.0"
 assert s["invariants"]["algorithm_reopen_count"]==0 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","candidate_digital_groups":13,"registered_sources_unchanged":734,"ancient_votes_added":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))

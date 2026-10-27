#!/usr/bin/env python3
"""13P non-voting Commons metadata anchors: descriptions never substitute for original leaves."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13P-NLC411999022809-LATER-GROUP-METADATA-ANCHORS-R1.json"
def read(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e):
 assert e["schema"]=="TIANWEN-13P-NLC411999022809-LATER-GROUP-METADATA-ANCHORS-R1"
 assert e["digital_series"]=="411999022809" and e["research_issue"]=="TW-OPEN-0005"
 assert e["preceding_record"]=="docs/research/TIANWEN-13N-NLC-411999022809-V52-FASCICLE-ATLAS-R1.json"
 a=e["documented_anchors"]
 assert len(a)==3
 assert [(x["digital_group"],x["locator_id"],x["uploader_description_internal_zhi_juan"],x["pdf_pages_reported_by_commons"]) for x in a]==[(49,"411999022809-48601",[16,17],52),(50,"411999022809-48602",[18],31),(54,"411999022809-48650",[25],38)]
 for x in a:
  assert x["commons_file_title"].startswith("NLC892-"+x["locator_id"])
  assert x["commons_file_page_url"].startswith("https://commons.wikimedia.org/wiki/File:")
  assert x["evidence_grade"]=="COMMONS_UPLOADER_SUMMARY_METADATA_ONLY" and x["uploader_description_division"]=="志"
  assert x["first_party_nlc_item_verified"] is False and x["original_pdf_inspected"] is False and x["original_leaf_juan_directly_inspected"] is False
  assert x["target_work52_in_this_digital_group"] is None and x["independent_numeric_vote"] is False
  assert all(x[k] is None for k in ("source_pdf_sha256","source_page_number","source_page_sha256","d16_original_glyph","d18_original_glyph"))
 t=e["target_scope"]
 assert t["work_volume"]==52 and t["division"]=="志第六 曆三" and t["numeric_targets"]==["D16","D18"]
 assert t["search_groups_firstpass"]==list(range(36,44)) and t["search_groups_boundary"]==[33,34,35,44,45]
 assert all(t[k] is None for k in ("verified_target_digital_group","verified_original_leaf_image_sha256","verified_d16_glyph","verified_d18_glyph"))
 d=e["adjudication"]
 assert d["anchor_grade"]=="SECONDARY_UPLOADER_DESCRIPTIONS_ONLY_NOT_ORIGINAL_GLYPH_WITNESSES"
 assert d["no_interpolation_of_digital_group_to_work_juan"] is True and d["no_target_absence_in_unchecked_files_proven"] is True
 assert d["first_party_physical_copy_binding_verified"] is False
 assert all(d[k]==0 for k in ("new_source_registry_records","independent_original_numeric_votes_added","transmission_edges_added","algorithm_reopens"))
 assert d["open_research_issues"]==11 and d["product_r1"]=="CLOSED"
 assert (d["root_source_count"],d["extension_source_count"])==(647,87)
def verify():
 e=read(E);check(e)
 prior=read(e["preceding_record"])
 assert prior["adjudication"]["exact_target_nlc_digital_group"] is None and all(x["contains_target_work_volume52"] is None for x in prior["scan_atlas"]["records"])
 s=read("docs/PROJECT-CURRENT-STATE-R1.json");l=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,675,0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(x.startswith("13P ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"] and E[:-5]+".md" in issue["source_refs"]
 assert len(l["issues"])==11 and set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in l["issues"]}
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert any(x["id"]=="OMISSIONS-13P-NLC411999022809-LATER-GROUP-METADATA-20261019" and x["state_version"]=="1.675.0" for x in l["checkpoint_log"])
 assert s["invariants"]["algorithm_reopen_count"]==0 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","nonvoting_upload_metadata_anchors":3,"independent_numeric_votes":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))

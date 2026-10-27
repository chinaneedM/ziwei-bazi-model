#!/usr/bin/env python3
"""13GH FAQ routes and source nulls must never be promoted to ancient evidence."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13GH-NCL-FAQ-DETAIL-ROUTES-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13GH-NCL-FAQ-DETAIL-ROUTES-R1"
 assert e["grade"]=="FIRSTPARTY_SERVICE_SCOPE_ONLY_NO_NEW_ORIGINAL_OR_GLYPH"
 assert e["firstparty_sources"][0]["url"]=="https://rbook.ncl.edu.tw/NCLSearch/FAQ"
 p=e["verified_policy"]
 assert all(p[k] is True for k in ("onsite_route_from_item_detail","existing_scanned_image_default_online_reading","onsite_exceptions_require_reason","digital_license_route_from_item_detail","digital_license_requires_existing_scan","no_scan_digital_license_not_available","higher_res_research_copy_requires_written_approval","higher_res_copy_is_personal_research_only","onsite_form_is_not_proven_remote_copy_order","digital_license_is_not_automatically_high_res_research_copy"))
 assert p["onsite_multiple_book_max"]==3
 t=e["unverified_item"]
 assert t["mirror_segment"]=="NCL-03130_09" and t["mirror_call_number"]=="208 03130"
 for k in ("firstparty_catalog_detail_url","firstparty_physical_item_id","book_to_segment_binding","target_d9_original","target_d14_original","target_d30_original","copy_layer_qing_vs_guangxu","highres_existing"):
  assert t[k] is None,k
 assert t["physical_leaf_numbers"]==[None,None]
 assert t["target_pdf_pages"]==[74,76]
 assert t["page74_png_sha256"]=="a3f597f96f494a5ee9a6d582850f0642035d858bcbc587abc6fac11853018a14"
 assert t["page76_png_sha256"]=="ce4eb8b044868fe48bb41fe5453b10fa7bbd949d8fdf2c8e31037f8b89f32fad"
 assert t["later_1909_d30_other_copy"]=="四分九二二二"
 q=e["request_manifest"]
 assert q["status"]=="DRAFT_NOT_SENT"
 assert all(q[k] is False for k in ("submitted","identity_supplied","fee_paid","rights_approved","image_received"))
 h=e["negative_guards"]
 assert h["G893_six_original_controls"]=="OPEN" and h["legacy_13EI"]=="RETRACTED"
 assert h["old_unit_fourfen_bridge"] is None
 for k in ("new_original_images","new_original_glyphs","new_registry_sources","new_physical_witnesses","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens","candidate_collapses","chart_defects"):assert h[k]==0,k
 assert e["counts"]=={"matrix":[222,222],"sources":761,"graph_nodes":252,"graph_edges":238,"open_risks":11,"chart":"CLOSED"}
 assert not e["transmission_impact"]["edges_supported"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,837,0)
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert "docs/research/TIANWEN-13GH-NCL-FAQ-DETAIL-ROUTES-R1.json" in issue["source_refs"] and "docs/research/TIANWEN-13GH-NCL-FAQ-DETAIL-ROUTES-R1.md" in issue["source_refs"]
 assert any(z.get("revision_id")=="TW-OPEN-0005-13GH-NCL-FAQ-20261025" for z in issue["history"])
 assert any(z.get("id")=="OMISSIONS-13GH-NCL-FAQ-20261025" for z in l["checkpoint_log"])
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("13GH_PASS_FIRSTPARTY_ROUTING_WITHOUT_TARGET_PROMOTION")

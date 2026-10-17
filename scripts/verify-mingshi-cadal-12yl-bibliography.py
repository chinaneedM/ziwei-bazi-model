#!/usr/bin/env python3
"""12YL bibliography-only Mingshi CADAL route; do not promote unexamined source glyphs."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YL-MINGSHI-V33-CADAL-IMAGE-LOCATOR-R1.json"
def need(value,msg):
 if not value:raise ValueError(msg)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,ledger,state):
 need(d["schema"]=="TIANWEN-12YL-MINGSHI-V33-CADAL-BIBLIOGRAPHIC-ORIGINAL-ROUTE-R1" and d["research_grade"]=="BIBLIOGRAPHIC_DIGITAL_SOURCE_LOCATOR_ONLY_NOT_SOURCE_GLYPH","evidence grade")
 a=d["source_cadal"]
 need(a["id"]=="CADAL06056955" and a["fascicle"]=="卷三十二至卷三十四" and a["catalog_pages"]==168 and a["catalog_bytes"]==6001348 and a["catalog_sha1"]=="903ac33c6409ff95a5eff64c19b6eacd90f41a5e","catalog original identity")
 need(a["holding_reported"]=="浙江大学图书馆" and a["scanner_reported"]=="CADAL" and a["catalog_pixels"]==[957,1359] and "commons.wikimedia.org" in a["commons_catalog"] and "ctext.org" in a["ctext_catalog"],"source route")
 need(a["physical_copy_impression_date"]=="UNVERIFIED" and a["full_bytes_local_sha_verified"] is False and a["original_target_page_identified"] is False and a["original_target_glyph_read"] is False,"unsupported original claim")
 b=d["source_ssid"]
 need(b["id"]=="SSID-14059739" and b["catalog_bytes"]==36398055 and b["catalog_pages"]==369 and b["target_page_read"] is False and b["physical_relation_to_cadal"]=="UNPROVEN","same original not proven")
 e=d["secondary_editorial_control"]
 need(e["changed_at_utc"]=="2026-10-03T16:00:00Z" and e["modern_received_not_independent_original"] is True and "daizhige.org" in e["url"],"2026 digital editorial status")
 t=d["research_target"]
 need(t["volume"]=="明史卷三十三" and t["verified_imprint_glyph_1"] is t["verified_imprint_glyph_2"] is t["folio"] is t["original_pixel_sha"] is None,"pretend original glyph")
 k=d["independence"]
 need(k["ctext_vs_commons_same_cadal_id"]=="SAME_DIGITIZATION_IDENTIFIER_NOT_TWO_INDEPENDENT_PHYSICAL_ORIGINALS" and k["cadal_vs_ssid_physical_copy"]=="NOT_ADJUDICATED" and k["four_digital_received_texts_independent_original_count"]==0,"false independent evidence")
 s=d["safeguards"]
 need(all(s[x]==0 for x in ("new_original_target_decisions","new_independent_physical_witness_votes","new_source_registry_entries","new_genealogy_edges","algorithm_reopens")),"false historical award")
 need(s["g893_formal_targets"]=="5/6" and s["cross_witness_final"]=="0/6" and s["open_research_issues"]==11 and s["product"]=="CLOSED","false project closure")
 risk=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(risk["status"]=="OPEN" and DOC in risk["source_refs"] and DOC.replace(".json",".md") in risk["source_refs"],"open risk binding")
 reviews=risk["mingshi_12yl_cadal_locator_reviews"]
 need(len(reviews)==1 and reviews[0]["source_id"]=="CADAL06056955" and reviews[0]["evidence_doc"]==DOC and reviews[0]["original_numeric_glyphs_verified"]==0 and reviews[0]["physical_witness_votes"]==0,"risk audit append")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,626,0) and any(x.startswith("12YL ") for x in state["historical_audit"]["current_focus"]),"continuity synchronization")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"algorithm block")
 return {"status":"PASS","source_routes":2,"precise_cadal_pages":168,"original_glyphs_verified":0,"new_original_votes":0}
if __name__=="__main__":
 print(json.dumps(verify(*load()),ensure_ascii=False))

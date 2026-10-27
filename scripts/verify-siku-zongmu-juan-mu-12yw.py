#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YW-SIKU-ZONGMU-V106-DIRECT-JUAN-MU-ORIGINAL-FOLIOS-R1.json"
def read():
 return [json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json")]
def must(ok,label):
 if not ok:raise ValueError(label)
def verify(d,l,s):
 must(d["schema"]=="TIANWEN-12YW-SIKU-ZONGMU-ORIGINAL-FOLIO-READ-R1","schema")
 a=d["original_source"]
 must(a["id"]=="SSID-11564461" and a["total_pages"]==101 and a["reported_bytes"]==8724887 and a["commons_reported_sha1"]=="1a355a64336198573a0bd9495997e30889be4fbe","known source metadata")
 must(a["sha1_self_verified"] is False and a["source_pixel_sha256_self_verified"] is False and a["physical_holding_identity"]=="UNVERIFIED" and a["impression_year"]=="UNVERIFIED","cannot manufacture local immutable native source")
 q=d["page_reviews"]
 must(len(q)==2 and [(z["zero_based_pdf_page"],z["viewer_page"]) for z in q]==[(86,87),(88,89)],"real page controls")
 must([z["direct_printed"] for z in q]==["大統歷志八卷附錄一卷","其書舊不分卷今以所立十七目一目定爲一卷以便循覽焉"] and all(z["ocr_used"] is False for z in q),"exact visible glyphs")
 t=d["textual_result"]
 must(t["eight_juan_and_seventeen_mu_on_same_scan"] is True and t["received_seventeen_juan_rubric_different_original_verified"] is False and t["separate_seventeen_juan_physical_edition_proven"] is False and t["explanation_for_concurrent_title_and_note"]=="UNRESOLVED","no fake edition conclusion")
 n=d["nlc_locator"]
 must(n["correct_nlc_item"]=="NLC892-001945406-317607" and n["correct_nlc_fascicle"]==50 and n["correct_catalog_juans"]==[105,106] and n["correct_nlc_folio_visually_reviewed"] is False,"correct locator is not a glyph")
 must(n["wrong_nlc_item"]=="NLC892-001945406-317562" and n["wrong_fascicle"]==106 and n["wrong_actual_juan"]==193 and n["relationship_to_ssid_copy"]=="UNVERIFIED","fascicle-juan firewall")
 e=d["scope"]
 must(all(e[k]==0 for k in ("new_source_registry_entries","new_historical_physical_copy_votes","new_genealogy_nodes","new_genealogy_edges","new_runtime_reopens","new_g893_numeric_loci")),"invented witness or algorithm")
 must(e["g893_primary"]=="5/6" and e["g893_cross_source"]=="0/6" and e["open_omissions"]==11 and e["chart_product"]=="CLOSED","fixed product state")
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 must(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC[:-5]+".md" in issue["source_refs"],"issue binding")
 must(issue["mei_12yw_catalog_original_page_reviews"][0]["printed_pages_zero_based"]==[86,88] and issue["mei_12yw_catalog_original_page_reviews"][0]["full_file_sha_recomputed"] is False,"no overstated evidence grade")
 must(l["binding"]["reviewed_state_version"]==s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state mismatch")
 must(l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and any(x.startswith("12YW ") for x in s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0] and l["checkpoint_log"][-1]["state_version"]==s["schema_version"],"checkpoint forward progress")
 return {"result":"PASS","original_page_loci":2,"locally_hashed":False,"historical_copy_added":0,"issues_open":11}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))

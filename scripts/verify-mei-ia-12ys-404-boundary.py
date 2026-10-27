#!/usr/bin/env python3
"""12YS source locator and negative HTTP404 evidence; no false original image promotion."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YS-MEI-CADAL06054965-EXACT-IA-OBJECT-404-ACCESS-BOUNDARY-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def require(ok,msg):
 if not ok:raise ValueError(msg)
def verify(doc,ledger,state):
 c=doc["catalog_provenance"];p=doc["acquisition_attempt"];t=doc["target"];g=doc["evidence_grade"]
 require(doc["schema"]=="TIANWEN-12YS-MEI-DATONG-LIZHI-CADAL06054965-EXACT-IA-OBJECT-ACCESS-BOUNDARY-R1" and doc["status"]=="EXACT_DIGITAL_CATALOG_ROUTE_RESOLVED_REMOTE_ORIGINAL_BYTES_NOT_OBTAINED","no fake original upgrade")
 require(t["file_identifier"]=="06054965.cn" and t["original_target_glyphs_direct_read"]==0 and t["source_file_sha256"] is None and t["original_scan_page_count"] is None and t["source_physical_print_date"]=="UNVERIFIED","no original file")
 require(c["wikicode_link"]=="//archive.org/download/06054965.cn//06054965.cn.djvu" and c["live_html_verified"] is True and c["direct_catalog_item_id_proven"] is True and c["original_djvu_downloaded"] is False and c["cadal_same_physical_copy_as_12yo_ctext"]=="UNPROVEN","source identity or CText same copy invented")
 require(p["workflow"].endswith("/39007082727") and len(p["attempts"])==2 and all(x["result"]=="HTTP_404_NOT_FOUND" for x in p["attempts"]) and p["downloaded_source_bytes"]==0 and p["source_sha_verified"] is False and p["historical_original_readings"]==0 and "NOT_PROOF" in p["conclusion"],"unbounded negative or fake download")
 paid=next(x for x in doc["alternate_routes"] if "jiguzuo" in x["url"])
 require(paid["payment_made"] is False and paid["original_bytes_verified"] is False,"no purchase or false paid original witness")
 require(all(g[k]==0 for k in ("new_mei_original_images","new_mei_original_loci","new_independent_physical_print_voting","source_registry_entries","new_genealogy_edges","new_algorithm_reopens")) and g["G893_formal"]=="5/6" and g["cross_witness_mechanical"]=="0/6" and g["open_issues"]==11 and g["fusion_product"]=="CLOSED","source promotion forbidden")
 i=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 require(i["status"]=="OPEN" and DOC in i["source_refs"] and DOC.replace(".json",".md") in i["source_refs"] and i["mei_12ys_exact_ia_digital_identity_and_404_reviews"][0]["mei_printed_original_target_loci"]==0,"research issue crossbinding")
 require(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,631,0),"state version")
 require(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"]) and any(z.startswith("12YS ") for z in state["historical_audit"]["current_focus"]),"research continuity")
 require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"chart product invariants")
 return {"status":"PASS","exact_catalog_item_id":"06054965.cn","direct_source_URL_forms_tested":2,"source_original_bytes":0,"Mei_original_glyphs":0,"unresolved_issues":len(ledger["issues"])}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))

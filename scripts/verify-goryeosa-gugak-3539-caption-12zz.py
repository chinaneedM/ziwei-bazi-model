#!/usr/bin/env python3
"""12ZZ GK3539 media dates: fail closed on year scope, folio/page and witness duplication."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZZ-GORYEOSA-GK3539-GUGAK-1454-1613-CAPTION-SCOPE-R1.json"
SHARD="docs/research/TIANWEN-12ZZ-GORYEOSA-NATIONAL-GUGAK-EXHIBIT-SOURCE-SHARD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
PRIOR="docs/research/TIANWEN-12ZU-GORYEOSA-HERITAGE-GK-ID-AND-SHARED-MICROFILM-R1.json"
def read(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def ck(ok,why):
 if not ok: raise ValueError(why)
def verify():
 d,sh,st,l,m,p=map(read,(P,SHARD,STATE,LEDGER,MANIFEST,PRIOR))
 ck(d["schema"]=="TIANWEN-12ZZ-GK3539-2024-GUGAK-CAPTION-YEAR-MISMATCH-R1" and d["prior"]==PRIOR,"research identity")
 ck(p["items"][0]["snu_catalog_code"]=="GK03539_00","original 12ZU kept")
 copy=d["original_snu_copy"]
 ck(copy["catalog_item"]=="GK03539_00" and copy["call_no"]=="奎貴3539" and copy["catalog_print_year"]=="[光海君5年(1613)]" and copy["physical_books"]==85,"catalog copy")
 ck(copy["work52_exact_physical_book"] is None and copy["work52_original_folio_sha256"] is None,"target still missing")
 a,b=d["media_items"]
 ck([(z["id"],z["physical_book_number"],z["work_juan"],z["caption_year_literal"]) for z in (a,b)]==[(6426,42,70,1454),(6545,10,18,1613)],"positive book/juan/date controls")
 ck(all(z["holding_call_number"]=="奎貴3539" and not z["complete_original_leaf_pixels_attested"] and not z["verified_target_work52"] for z in (a,b)),"metadata not original")
 ck(d["further_same_copy_confirmation"]["id"]==6425 and d["further_same_copy_confirmation"]["new_source_registry_entry"] is False,"same-source supplementary check")
 scope=d["historical_inference"]
 ck(scope["date_label_disagreement_is_proven"] and scope["same_gk3539_implies_same_registered_physical_set"] and scope["actual_book_to_work_map_attested_by_media_catalog_only"],"date scope")
 ck(scope["ngc_media_caption_1454_meaning"]=="UNRESOLVED_WORK_PRINTING_REPRODUCTION_DATE_OR_EDITORIAL_UNSCOPED_LABEL","do not assign 1454")
 ck(scope["media_year_1454_proves_original_copy_printed_1454"] is False,"year 1454 cannot date original item")
 ck(scope["media_year_1454_proves_original_copy_printed_1454"] is False and scope["first_1454_printing_as_current_physical_witness_unproven"] is True,"date still unproven")
 ck(scope["independent_physical_witnesses_from_6426_and_6545"]==scope["new_target_work52_page_images"]==scope["new_target_D16_D18_numeric_votes"]==0 and scope["work52_physical_book_number"] is None,"no original")
 items=sh["sources"]
 ck(sh["schema"]=="TIANWEN-12ZZ-GK3539-NATIONAL-GUGAK-CAPTION-DUAL-SOURCE-SHARD-R1" and len(items)==2,"shard")
 ck({x["source_id"] for x in items}=={a["recorded_source_id"],b["recorded_source_id"]},"source IDs")
 ck(all(x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["physical_glyph_authority"] is False and x["evidence"]==P for x in items),"no false glyph authority")
 cs=d["source_controls"]
 ck(cs["registry_total_before"]==717 and cs["registry_total_after"]==719 and cs["registered_sources_added"]==2,"historical source increment")
 ck(m["combined_source_count"]==st["historical_audit"]["external_source_registry_total_unique_count"]>=719 and m["extension_source_count"]>=72 and m["root_source_count"]+m["extension_source_count"]==m["combined_source_count"],"live source count")
 ck(any(e["path"]==SHARD and e["source_count"]==2 for e in m["shards"]),"source shard linked")
 ck(st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state sync")
 ck(any(x.startswith("12ZZ ") for x in st["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0] and l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"]),"live focus")
 risk=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 ck(risk["status"]=="OPEN" and all(x in risk["source_refs"] for x in (P,P.replace(".json",".md"),SHARD)),"TW-OPEN-0005")
 ck(len(l["issues"])==11 and all(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in l["issues"]),"no closure")
 ck(l["checkpoint_log"][-1]["state_version"]==st["schema_version"] and set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={i["id"] for i in l["issues"]},"review")
 ck(st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0,"chart invariant")
 return {"status":"PASS","first_party_media_records":2,"same_original_physical_set":1,"new_target_originals":0,"registered_sources":719}
if __name__=="__main__": print(json.dumps(verify(),ensure_ascii=False))

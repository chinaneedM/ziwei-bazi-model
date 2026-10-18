#!/usr/bin/env python3
"""13F: Received 1454 historical print command is distinct from completed physical impression."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13F-GUKJOBOGAM-1454-PRINT-ORDER-1782-COPY-SCOPE-R1.json"
SH="docs/research/TIANWEN-13F-GUKJOBOGAM-V9-SOURCE-SHARD-R1.json"
def rd(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def verify():
 e=rd(E);sh=rd(SH);st=rd("docs/PROJECT-CURRENT-STATE-R1.json");l=rd("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json");m=rd("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
 assert e["schema"]=="TIANWEN-13F-GUKJOBOGAM-1454-COMMAND-1782-EDITION-FIREWALL-R1"
 a=e["read_locus"];b=e["catalog"];c=e["adjudication"]
 assert a["text"]=="命刊印高麗全史。廣布中外。" and a["section"]=="甲戌二年(1454) 九月"
 assert a["text_proves_command_to_print"] and not a["text_proves_printing_completed"] and not a["text_proves_copies_delivered"]
 assert b["code"]=="GK03942_00" and b["edition_catalog_date"]==1782 and b["volume9"]=="端宗"
 assert b["physical_books"]==22 and b["text_volumes"]==68 and not b["folio_work9_verified"] and b["original_page_sha256"] is None
 assert all(c[k] is True for k in ("year_1454_is_narrated_event_not_edition_date","year_1782_is_later_catalog_date","earlier_13d_unread_snapshot_retained","received_text_target_now_located","received_text_and_1454_annals_are_not_independent_proof_of_completed_print"))
 assert all(c[k] is False for k in ("verified_print_run_1454","verified_distribution_1454","verified_1782_original_book9_leaf","underlying_wikisource_physical_copy_identity_known"))
 assert c["goryeosa_work52_original_glyph_sha256"] is None and c["original_goryeosa_numeric_votes_added"]==c["new_physical_1454_witnesses"]==c["new_transmission_edges"]==c["algorithm_reopen_count"]==0
 assert sh["schema"]=="TIANWEN-13F-GUKJOBOGAM-RECEIVED-AND-SNU-CATALOG-SHARD-R1" and len(sh["sources"])==2
 assert {x["verification_status"] for x in sh["sources"]}=={"RECEIVED_TEXT_VERIFIED","BIBLIOGRAPHIC_METADATA_ONLY"}
 assert all(x["evidence"]==E and x["physical_glyph_authority"] is False for x in sh["sources"])
 assert any(x["path"]==SH and x["source_count"]==2 for x in m["shards"])
 assert m["combined_source_count"]==st["historical_audit"]["external_source_registry_total_unique_count"]>=728 and m["extension_source_count"]>=81
 assert st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13F ") for x in st["historical_audit"]["current_focus"])
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["status"]=="OPEN" and all(x in i["source_refs"] for x in (E,E.replace(".json",".md"),SH))
 assert len(l["issues"])==11 and all(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in l["issues"])
 assert l["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in l["issues"]}
 assert st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0
 return {"status":"PASS","registered_sources":m["combined_source_count"],"ancient_numeric_votes":0}
if __name__=="__main__": print(json.dumps(verify(),ensure_ascii=False))

#!/usr/bin/env python3
"""13D fail-closed: modern printed scholarly page != ancient completed-print receipt."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13D-GORYEOSA-1454-MODERN-PRINT-FULFILLMENT-INFERENCE-R1.json"
S="docs/research/TIANWEN-13D-GORYEOSA-NIKH-SCHOLARLY-AND-AKS-ENCY-SHARD-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def verify():
 e=read(E);sh=read(S);st=read("docs/PROJECT-CURRENT-STATE-R1.json");l=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json");m=read("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
 assert e["schema"]=="TIANWEN-13D-GORYEOSA-SCHOLARLY-1454-FULFILLMENT-INFERENCE-SCOPE-R1"
 n=e["scholarship"]["nihk"];a=e["scholarship"]["aks"];b=e["evidence_scope"]
 assert n["printed_pages"]==[124,125] and n["pdf_page_zero_based"]==[114,115]
 assert n["historical_1454_completion_original_witness"] is False and "footnote_64" in n
 assert a["initial_authorship_year"]==1995 and a["last_revision_date"]=="2024-05-22"
 assert a["original_GK03539_folio"] is False and b["physical_book_75_not_universal_work_volume_count"] is True
 for k in ["nihk_text_and_pdf_same_intellectual_source","aks_and_snu_13c_same_1454_claim_do_not_count_as_two_original_1454_prints","later_literature_citing_a_1454_annals_approval_cannot_bootstrap_completed_print","footnote_64_received_statement_does_not_alone_observe_approved_reprint","nihk_1454_widespread_distribution_is_scholarly_interpretation","aks_1454_widespread_distribution_is_scholarly_interpretation","both_original_baogam_bigo_target_passages_unread"]:
  assert b[k] is True,k
 assert all(b[k] is None for k in ["first_print_completion_timestamp","verified_1454_distribution_delivery_receipt","gk03539_work52_physical_book","work52_D16_D18_native_folio_sha256"])
 assert b["new_target_ancient_original_glyph_votes"]==b["new_independent_physical_ancient_print_witnesses"]==b["new_graph_edges"]==b["chart_algorithm_reopens"]==0
 assert sh["schema"]=="TIANWEN-13D-GORYEOSA-NIKH-SCHOLARLY-AND-AKS-ENCYCLOPEDIA-SHARD-R1" and len(sh["sources"])==2
 assert {x["source_id"] for x in sh["sources"]}=={n["source_id"],a["source_id"]}
 assert all(x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["physical_glyph_authority"] is False and x["evidence"]==E for x in sh["sources"])
 assert any(x["path"]==S and x["source_count"]==2 for x in m["shards"])
 assert m["combined_source_count"]==st["historical_audit"]["external_source_registry_total_unique_count"]>=724 and m["extension_source_count"]>=77
 assert st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13D ") for x in st["historical_audit"]["current_focus"])
 z=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert z["status"]=="OPEN" and all(x in z["source_refs"] for x in (E,E.replace(".json",".md"),S))
 assert len(l["issues"])==11 and all(i["status"]!="RESOLVED_WITH_EVIDENCE" for i in l["issues"])
 assert l["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 assert {x for x in l["checkpoint_log"][-1]["reviewed_issue_ids"]}=={i["id"] for i in l["issues"]}
 assert st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0
 return {"status":"PASS","new_secondary_sources":2,"total_registered_sources":m["combined_source_count"],"completed_print_receipts":0,"work52_glyphs":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))

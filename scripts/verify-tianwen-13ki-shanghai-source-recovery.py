#!/usr/bin/env python3
"""13KI: digital PDF acquisition attested, target text and copy identity unawarded."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KI-SHANGHAI-HUANG-97PAGE-DIGITAL-ACQUISITION-R1.json"
S="docs/research/TIANWEN-13KI-SHANGHAI-HUANG-DIGITAL-OBJECT-SOURCE-SHARD-R1.json"
A="c524693e7bad502d222a1444d688cc7d63ca4a4037d7d4e08cee4aa94f9adbae"

def verify(e,shard,state,ledger,manifest):
 def chk(p,msg):
  if not p:raise ValueError(msg)
 chk(e["schema"]=="TIANWEN-13KI-SHANGHAI-HUANG-97PAGE-DIGITAL-ACQUISITION-R1","schema")
 d=e["digital_source"];history=e["historical_scope"]
 chk(d["sha256"]==A and d["sha1"]=="73c2017bb9eb109edf069f9563c397e7fcb2cba4" and d["size_bytes"]==14376480 and d["pdf_pages"]==97,"source digest")
 chk(d["artifact_id"]==12890397318 and d["run_id"]==40858637903,"work unit")
 chk(d["full_pdf_digitally_acquired"] is True and d["target_pdf_page_mapped"] is False and
     d["target_glyphs_collated"] is False and d["ocr_used"] is False,"source page scope")
 chk(e["immutable_coverage_snapshot"]["source_pdf_sha256"]==A and e["immutable_coverage_snapshot"]["target_text_pages_native_glyph_collated"]==0,"coverage snapshot")
 chk(all(v is False for k,v in e["critical_readings_not_awarded"].items() if k.endswith("_original_glyph_proven")),"no false original")
 chk(e["critical_readings_not_awarded"]["G893_six_cross_witness_numeric_winners"]==0,"no numeric award")
 chk(history["source_registry_digital_object_delta"]==1 and history["new_independent_physical_copy_votes"]==0 and not history["issue_closed"] and history["product"]=="CLOSED","physical copy scope")
 chk(history["transmission_graph_nodes_delta"]==0 and history["transmission_graph_edges_delta"]==0 and history["chart_algorithm_reopens"]==0,"graph/algorithm")
 chk(shard["schema"]=="TIANWEN-13KI-SHANGHAI-HUANG-DIGITAL-OBJECT-SOURCE-SHARD-R1" and len(shard["sources"])==1,"source shard")
 src=shard["sources"][0]
 chk(src["evidence"]==E and src["url"]==d["commons_file_page"] and src["physical_glyph_authority"] is False and src["verification_status"]=="UNVERIFIED_TARGET_LOCATOR_QUARANTINED","quarantine")
 h=state["historical_audit"];b=ledger["binding"]
 chk(state["schema_version"]==b["reviewed_state_version"]==h["research_omission_guard"]["reviewed_state_version"],"handoff version")
 chk(len(h["current_focus"])==b["source_focus_count"] and h["current_focus"][-1].startswith(b["latest_research_focus_prefix"]+" "),"focus")
 chk(h["external_source_registry_total_unique_count"]>=765 and h["external_source_registry_total_unique_count"]==h["external_source_registry_root_count"]+h["external_source_registry_extension_count"],"registry totals")
 chk(manifest["combined_source_count"]==h["external_source_registry_total_unique_count"] and manifest["extension_source_count"]==h["external_source_registry_extension_count"],"manifest sync")
 chk(any(z["path"]==S for z in manifest["shards"]),"source in registry")
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 chk(issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith(b["latest_research_focus_prefix"]+" CURRENT ACTION:"),"open P0")
 chk(E in issue["source_refs"] and S in issue["source_refs"],"issue source crosswalk")
 chk(any(z.get("revision_id")=="TW-OPEN-0005-13KI-SHANGHAI-ACQUISITION-20261029" for z in issue["history"]),"append-only issue")
 chk(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["issues"])==11,"checkpoint")
 chk(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"algorithm")
 return {"status":"PASS","acquired_pdf_pages":97,"target_glyphs_collated":0,"historical_winners":0}

def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in
   [E,S,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json",
    "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"])

if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))

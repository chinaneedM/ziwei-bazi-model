#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13C-GORYEOSA-1469-PETITION-AND-1454-SECONDARY-R1.json"
def load(x):return json.loads((ROOT/x).read_text(encoding="utf-8"))
def verify():
 e=load(E); sh=load("docs/research/TIANWEN-13C-GORYEOSA-ANNALS-SNU-SOURCE-SHARD-R1.json"); st=load("docs/PROJECT-CURRENT-STATE-R1.json"); l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"); m=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
 assert e["annals"]["id"]=="kha_10106029_002" and e["annals"]["excerpt"]=="一頒《麗史》"
 a=e["scope"]
 assert a["annals_petition_attested"] and not any(a[k] for k in ("prior_1454_distribution_disproved","petition_1469_fulfilled","secondary_1454_delivered_proven","eulhae_1455_physical_impression_proven"))
 assert e["snu"]["later_compilations_original_pages_read"] is False and e["snu"]["surviving_GK05554_print_date_proven"] is False
 assert a["exact_work52_book"] is None and a["original_work52_D16_D18_sha256"] is None
 assert a["physical_witness_votes_added"]==a["original_numeric_votes_added"]==a["genealogy_edges_added"]==a["algorithms_reopened"]==0
 assert len(sh["sources"])==2 and {x["verification_status"] for x in sh["sources"]}=={"RECEIVED_TEXT_VERIFIED","BIBLIOGRAPHIC_METADATA_ONLY"}
 assert all(x["physical_glyph_authority"] is False for x in sh["sources"])
 assert any(z["path"]=="docs/research/TIANWEN-13C-GORYEOSA-ANNALS-SNU-SOURCE-SHARD-R1.json" and z["source_count"]==2 for z in m["shards"])
 assert m["combined_source_count"]==st["historical_audit"]["external_source_registry_total_unique_count"]>=722
 assert st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert any(z.startswith("13C ") for z in st["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in (E,E.replace(".json",".md"),"docs/research/TIANWEN-13C-GORYEOSA-ANNALS-SNU-SOURCE-SHARD-R1.json"))
 assert len(l["issues"])==11 and all(z["status"]!="RESOLVED_WITH_EVIDENCE" for z in l["issues"])
 assert l["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 assert st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0
 return {"status":"PASS","sources":m["combined_source_count"],"original_votes":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))

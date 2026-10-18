#!/usr/bin/env python3
"""13B: keep retrospective SNU print-date interpretation distinct from 1454 contemporary report."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13B-GORYEOSA-SNU-CURATORIAL-1452-1453-VS-1454-ANNALS-SCOPE-R1.json"
SHARD="docs/research/TIANWEN-13B-GORYEOSA-SNU-CURATORIAL-CHRONOLOGY-SOURCE-SHARD-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
OLD="docs/research/TIANWEN-12ZP-GORYEOSA-1452-1454-1482-ROYAL-ANNALS-PRINT-STATE-COLLATION-R1.json"
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def must(b,s):
 if not b:raise ValueError(s)
def verify():
 a,s,st,l,m,o=map(load,(P,SHARD,STATE,LEDGER,MANIFEST,OLD))
 must(a["schema"]=="TIANWEN-13B-GORYEOSA-SNU-CURATORIAL-CHRONOLOGY-AND-ANNALS-SCOPE-R1" and a["prior"]==OLD,"batch identity")
 must(a["source"]["catalog_item"]=="GK03269_00" and a["source"]["original_work52_folio_sha256"] is None,"no photo")
 assert len(a["curatorial_interpretations"])==2
 must(all(x["witness_grade"]=="RETROSPECTIVE_CURATORIAL_INTERPRETATION" and not any([x.get("asserted_as_verified_completion",False),x.get("asserted_as_verified_distribution",False)]) for x in a["curatorial_interpretations"]),"curatorial hypotheses not proof")
 must({z["source_id"] for z in a["historical_annals_crosscontrols"]}=={x["source_id"] for x in o["events"] if x["key"] in ["goryeosa_approval_1452_11_28","limited_full_history_1454_10_13"]},"annals source IDs stable")
 v=a["decision"]
 must(v["chronology_disagreement"]=="CURATORIAL_1453_WIDESPREAD_ESTIMATE_IN_TENSION_WITH_1454_CONTEMPORANEOUS_LIMITED_INNER_PALACE_REPORT","chronology tension")
 must(all(v[k] is False for k in ("can_prove_1452_dec_completion","can_prove_1453_oct_wide_print_distribution","can_prove_1454_new_approval_completed")),"unproven events")
 must(v["earliest_print_completed_month"]=="UNRESOLVED" and v["target_work52_book_number"] is None,"unknown print/photo")
 must(v["target_d16_d18_glyph_votes_added"]==v["new_independent_ancient_physical_witnesses"]==v["transmission_genealogy_edge_added"]==v["algorithm_reopens"]==0,"scope firewall")
 must(s["schema"]=="TIANWEN-13B-GORYEOSA-SNU-CURATORIAL-CHRONOLOGY-SOURCE-SHARD-R1" and len(s["sources"])==1,"source shard")
 must(s["sources"][0]["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and s["sources"][0]["physical_glyph_authority"] is False and s["sources"][0]["evidence"]==P,"no fabricated original")
 must(any(x["path"]==SHARD and x["source_count"]==1 for x in m["shards"]),"manifest shard")
 must(m["combined_source_count"]==st["historical_audit"]["external_source_registry_total_unique_count"]>=720 and m["extension_source_count"]>=73,"registered source count")
 must(st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"continuity sync")
 must(any(x.startswith("13B ") for x in st["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0],"forward prefix")
 must(l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"]),"focus length")
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 must(issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in (P,P.replace(".json",".md"),SHARD)),"issue unresolved")
 must(len(l["issues"])==11 and all(i["status"]!="RESOLVED_WITH_EVIDENCE" for i in l["issues"]),"open set")
 must(l["checkpoint_log"][-1]["state_version"]==st["schema_version"] and set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={i["id"] for i in l["issues"]},"omission checkpoint")
 must(st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0,"chart boundary")
 return {"status":"PASS","source_count":m["combined_source_count"],"new_target_originals":0,"research_risks_open":11}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))

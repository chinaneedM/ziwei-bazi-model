#!/usr/bin/env python3
"""13AD two UTokyo work52 holdings; manuscript catalog is not target folio."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AD-UTOKYO-GORYEOSA-WORK52-MANUSCRIPT-PRINT-DUAL-HOLDING-R1.json"
S="docs/research/TIANWEN-13AD-UTOKYO-GORYEOSA-MANUSCRIPT-SOURCE-SHARD-R1.json"
M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(p): return json.loads((P/p).read_text(encoding="utf-8"))
def verify():
 e=load(E);s=load(S);m=load(M)
 assert e["schema"]=="TIANWEN-13AD-UTOKYO-GORYEOSA-WORK52-PRINT-MANUSCRIPT-DUAL-CATALOG-CONTROL-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["evidence_grade"]=="OFFICIAL_NII_UNION_CATALOG_METADATA_ONLY"
 a=e["new_manuscript_holding"];b=e["known_print_holding"]
 assert (a["ncid"],a["call_number"],a["individual_registration"],a["volume"])==("BC15670118","G23:12","0008535809",52)
 assert (b["ncid"],b["call_number"],b["individual_registration"],b["volume"])==("BC15973641","G23:194","0008542011",52)
 assert (a["material_class"],a["set_extent"],b["material_class"],b["set_extent"])==("朝鮮鈔本","60冊","朝鮮刊本","81冊")
 assert a["copy_date"]=="UNKNOWN" and a["source_image_sha256"] is None
 assert a["original_d16_short_glyph"] is None and a["original_d18_cumulative_glyph"] is None
 assert e["comparison"]["textual_independence"]=="UNVERIFIED_NO_TARGET_FOLIO"
 assert e["comparison"]["edition_or_copy_independent_numeric_vote_added"] is False
 assert e["safety"]["no_original_glyph_attested"] and e["safety"]["no_d16_winner"]
 assert all(e["safety"][k]==0 for k in ("physical_numeric_votes_added","transmission_graph_nodes_added","transmission_graph_edges_added","algorithm_reopens"))
 assert len(s["sources"])==1 and s["sources"][0]["physical_glyph_authority"] is False
 assert s["sources"][0]["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY"
 assert s["sources"][0]["url"]==a["url"] and s["sources"][0]["evidence"]==E
 assert m["root_source_count"]==647 and m["extension_source_count"]>=91 and m["combined_source_count"]>=738
 assert any(x["path"]==S and x["schema"]==s["schema"] and x["source_count"]==1 for x in m["shards"])
 st=load("docs/PROJECT-CURRENT-STATE-R1.json");le=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert st["schema_version"]==le["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,689,0)
 assert any(x.startswith("13AD ") for x in st["historical_audit"]["current_focus"])
 assert le["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert le["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert st["historical_audit"]["external_source_registry_extension_count"]==m["extension_source_count"]
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 issue=next(x for x in le["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in (E,"docs/research/TIANWEN-13AD-UTOKYO-GORYEOSA-WORK52-MANUSCRIPT-PRINT-DUAL-HOLDING-R1.md",S))
 assert len(le["issues"])>=11 and all(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in le["issues"][:11])
 assert any(x["id"]=="OMISSIONS-13AD-UTOKYO-DUAL-PRINT-MANUSCRIPT-20261019" for x in le["checkpoint_log"])
 assert le["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 assert st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AD_UTOKYO_DUAL_MANUSCRIPT_PRINT_CATALOG_GATE_PASS")

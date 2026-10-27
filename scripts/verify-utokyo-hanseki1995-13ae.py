#!/usr/bin/env python3
"""13AE catalog preservation and no-primary-glyph-promotion CI gate."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AE-UTOKYO-1995-HANSEKI-CATALOG-PUBLIC-REPRODUCTION-ROUTE-R1.json"
S="docs/research/TIANWEN-13AE-UTOKYO-HANSEKI1995-REPOSITORY-SOURCE-SHARD-R1.json"
M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(p):return json.loads((P/p).read_text(encoding="utf8"))
def verify():
 e=load(E);s=load(S);m=load(M)
 assert e["schema"]=="TIANWEN-13AE-UTOKYO-HANSEKI-CATALOG-1995-1998-OFFICIAL-REPOSITORY-ACCESS-BOUNDARY-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["source"]["edition_main_year"]==1995 and e["source"]["edition_corrections_year"]==1998
 assert e["source"]["repository_deposit_year"]==2025
 assert len(e["source"]["repository_section_files"])==3
 assert all(x["direct_binary_attained"] is False for x in e["source"]["repository_section_files"])
 assert e["observed_access"]["source_pdf_sha256"] is None
 assert e["observed_access"]["fulltext_page_level_entry_read"] is False
 assert e["observed_access"]["negative_entry_absence_proven"] is False
 assert e["observed_access"]["firstparty_exact_G2312_item_bound"] is False
 assert e["observed_access"]["firstparty_exact_G23194_item_bound"] is False
 assert e["nonpromotion"]["physical_numeric_votes_added"]==e["nonpromotion"]["original_goryeosa_target_pages_added"]==0
 assert e["nonpromotion"]["algorithm_reopens"]==0 and e["nonpromotion"]["chart_product"]=="CLOSED"
 assert len(s["sources"])==1 and s["sources"][0]["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and s["sources"][0]["physical_glyph_authority"] is False
 assert s["sources"][0]["evidence"]==E and s["sources"][0]["url"]==e["source"]["firstparty_record"]
 assert m["root_source_count"]==647 and m["extension_source_count"]>=92 and m["combined_source_count"]>=739
 assert any(t["path"]==S and t["schema"]==s["schema"] and t["source_count"]==1 for t in m["shards"])
 st=load("docs/PROJECT-CURRENT-STATE-R1.json");l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert st["schema_version"]==l["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,690,0)
 assert any(t.startswith("13AE ") for t in st["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert l["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert st["historical_audit"]["external_source_registry_extension_count"]==m["extension_source_count"]
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in (E,"docs/research/TIANWEN-13AE-UTOKYO-1995-HANSEKI-CATALOG-PUBLIC-REPRODUCTION-ROUTE-R1.md",S))
 assert any(x["id"]=="OMISSIONS-13AE-UTOKYO-HANSEKI-CATALOG-PDF-ROUTE-20261019" for x in l["checkpoint_log"])
 assert l["checkpoint_log"][-1]["state_version"]==st["schema_version"] and len(l["issues"])>=11
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AE_UTOKYO_1995_HANSEKI_CATALOG_SCOPE_PASS")

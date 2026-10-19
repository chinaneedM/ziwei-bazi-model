#!/usr/bin/env python3
"""13AG scope: Korean collection/library reference/catalog bibliography != volume52 numeric original."""
from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AG-UTOKYO-AGAWA-1998-KOREAN-BOOKS-CATALOG-ROUTE-R1.json";S="docs/research/TIANWEN-13AG-UTOKYO-AGAWA-KOREAN-COLLECTION-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(p):return json.loads((P/p).read_text(encoding="utf-8"))
def verify():
 e=load(E);s=load(S);m=load(M)
 assert e["schema"]=="TIANWEN-13AG-UTOKYO-KOREAN-AGAWA-1998-CATALOG-SCOPE-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["no_new_numeric_witnesses"]
 assert e["official_collection"]["acquired_year"]==1924 and e["official_collection"]["moved_to_library_year"]==1930
 assert e["university_library_answer"]["case_id"]=="ASK0000025540" and e["university_library_answer"]["Nanki_independent_Korean_only_catalog"] is False
 z=e["original_1998_special_list"];assert z["ncid"]=="BB26657704" and z["call_number"]=="目録:AG:2" and z["individual_registration"]=="0014588842"
 assert z["journal_page_range"]=="139-202" and z["separate_offprint_page_range"]=="25-88"
 assert z["same_work_one_list_not_two"] and z["firstparty_original_list_pages_retrieved"] is False
 assert z["list_attests_target_Goryeosa"] is False and z["negative_exclusion_of_Goryeosa_proven"] is False
 assert len(e["checked_items"])==2 and all(i["agawa_membership"]=="UNVERIFIED" and i["Nanki_membership"]=="UNVERIFIED" and i["original_day16_glyph"] is None for i in e["checked_items"])
 assert e["prior_1995_scanned_pdf"]["no_Goryeosa_title_match_unproven"] and e["prior_1995_scanned_pdf"]["not_a_complete_negative_Korean_holding_register"]
 assert e["algorithm_reopened_count"]==0 and e["product"]=="CLOSED" and e["open_issues"]==11
 assert len(s["sources"])==4 and len({x["source_id"] for x in s["sources"]})==4 and all(x["physical_glyph_authority"] is False and x["evidence"]==E for x in s["sources"])
 assert m["root_source_count"]==647 and m["extension_source_count"]>=96 and m["combined_source_count"]>=743
 assert any(t["path"]==S and t["schema"]==s["schema"] and t["source_count"]==4 for t in m["shards"])
 st=load("docs/PROJECT-CURRENT-STATE-R1.json");le=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,692,0)
 assert st["schema_version"]==le["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert le["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert le["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13AG ") for x in st["historical_audit"]["current_focus"])
 assert st["historical_audit"]["external_source_registry_extension_count"]==m["extension_source_count"]
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 issue=next(x for x in le["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in [E,"docs/research/TIANWEN-13AG-UTOKYO-AGAWA-1998-KOREAN-BOOKS-CATALOG-ROUTE-R1.md",S])
 assert any(x["event"]=="UTOKYO_KOREAN_OLD_BOOKS_AGAWA_1998_SPECIAL_BIBLIOGRAPHY_LOCATED" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13AG-UTOKYO-AGAWA-1998-CATALOG-NANKI-20261019" for x in le["checkpoint_log"])
 assert len(le["issues"])>=11 and le["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 return True
if __name__=="__main__":
 assert verify();print("TIANWEN_13AG_UTOKYO_AGAWA_KOREAN_BIBLIOGRAPHY_FIREWALL_PASS")

#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13JX-FUJIWARA1941-SHOUSHI-ALTERNATE-TITLE-BOUNDARY-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def verify(e,s,l):
 assert e["schema"]=="TIANWEN-13JX-FUJIWARA1941-SHOUSHI-ALTERNATE-TITLE-BOUNDARY-R1"
 a=e["modern_publication"];d=e["distinct_object_1941_claim"];g=e["g893_object"];x=e["scope_guard"]
 assert (a["author"],a["year"],a["volume"],a["printed_page_range"])==("藤原松三郎",1941,48,[78,88])
 assert a["direct_article_page_scans_visually_checked"]==[78,79]
 assert not a["original_1941_pdf_bytes_acquired"] and a["original_1941_pdf_sha256"] is None
 assert d["historical_title_reported"]=="授時暦捷法立成" and d["reported_editor_in_scholarship"]=="姜保編"
 assert d["narrative_is_not_direct_ancient_original"] and not d["call_number_independently_confirmed_in_1941_scan"] and not d["current_physical_copy_identity_confirmed"]
 assert g["title"]=="授時曆立成" and g["catalog_identifier"]=="GK00893_00 / 奎貴893"
 assert all(not g[z] for z in ("title_identity_proven_with_1941_subject","same_physical_copy_proven","same_numerical_table_proven","exact_impression_year_proven"))
 assert all(x[z] for z in ("no_source_registry_change","no_ancient_physical_witness_added","no_lineage_edge_added","no_G893_six_original_control_awards","no_algorithm_or_candidate_winner_change"))
 assert all(x[z]==0 for z in ("g893_six_original_decisions","new_source_registry_entries","new_graph_nodes","new_graph_edges","algorithm_reopens"))
 assert x["chart_product"]=="CLOSED" and x["previous_13IO_physical29"]=="RETRACTED_UNBOUND"
 f=s["historical_audit"]["current_focus"];b=l["binding"]
 assert any(q.startswith("13JX ") for q in f) and any(q.startswith("13JW ") for q in f)
 assert s["schema_version"]==b["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert len(f)==b["source_focus_count"] and f[-1].split(" ",1)[0]==b["latest_research_focus_prefix"]
 issue=next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"]
 assert sum(q.get("revision_id")=="TW-OPEN-0005-13JX-FUJIWARA1941-20261029" for q in issue["history"])==1
 assert any(q.get("revision_id")=="TW-OPEN-0005-13JW-KYOTO-20261028" for q in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return {"status":"PASS","ancient_original_1298_pages":0,"g893_numeric_winners":0}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))

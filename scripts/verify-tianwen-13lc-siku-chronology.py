#!/usr/bin/env python3
"""13LC: archival chronology boundary; bibliography never licenses original-glyph voting."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LC-MINGSHI-SIKU-1739-1782-EDITION-CHRONOLOGY-SCOPE-R1.json"
OLD="docs/research/TIANWEN-13LB-CADAL-SIKU-MINGSHI-V35-NATIVE-TARGET-COLLATION-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def ck(cond, reason):
 if not cond:raise ValueError(reason)
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (E,OLD,S,L))
def verify(e,old,state,ledger):
 ck(e["schema"]=="TIANWEN-13LC-MINGSHI-SIKU-1739-1782-EDITION-CHRONOLOGY-SCOPE-R1" and e["issue_id"]=="TW-OPEN-0005","identity")
 by={r["id"]:r for r in e["institutional_witnesses"]}
 ck(len(by)==4,"source classes")
 ck(by["DPM-MINGSHI-1739-WUYING"]["url"]=="https://www.dpm.org.cn/ancient/hall/181550.html" and by["DPM-MINGSHI-1739-WUYING"]["year"]==1739,"Wuying edition")
 ck(by["CINII-MINGSHI-1739-CATALOG"]["url"]=="https://ci.nii.ac.jp/ncid/BD00540342" and by["CINII-MINGSHI-1739-CATALOG"]["year"]==1739,"CiNii")
 ck(by["DPM-SIKU-FIRST-1782"]["url"]=="https://www.dpm.org.cn/court/lineage/226263.html" and by["DPM-SIKU-FIRST-1782"]["year"]==1782,"Siku first")
 ck(by["NPM-SIKU-1772-1787"]["url"]=="https://theme.npm.edu.tw/selection/Article.aspx?sNo=04001076" and (by["NPM-SIKU-1772-1787"]["start_year"],by["NPM-SIKU-1772-1787"]["end_year"])==(1772,1787),"Siku bounds")
 ck(all(z["target_juan35_glyph_observed"] is False for z in by.values()),"no catalog glyph votes")
 b=e["chronological_firewall"]
 for key in ("ming_shi_1739_wuying_print_exists","siku_compilation_order_1772_attested","siku_first_completed_copy_1782_attested","siku_broad_completion_1787_attested"):ck(b[key] is True,"date positives "+key)
 for key in ("citable_museum_metadata_implies_cadal_copy_1739","cadal_physical_copy_linked_to_wuying_1739","cadal_physical_copy_linked_to_wenyuan_1782","cadal_earliest_physical_impression_established","harvard_v11_exact_1739_impression_authenticated","direct_target_numeric_witness_added","chronology_can_prove_numeric_corruption"):ck(b[key] is False,"false physical award "+key)
 n=e["source_native_preservation"]
 ck(n["cadal_positive_evidence"]==OLD and n["cadal_source_sha256"]==old["source"]["sha256"],"old hash-bound original")
 ck(n["cadal_original_13month"]=="288977.09" and n["harvard_original_13month"]=="238977.09","two original readings")
 ck(n["independently_authenticated_historical_physical_editions"]==n["original_historical_g893_six_control_winners"]==0 and n["dated_historic_calendar_to_limit_worked_example"] is False and n["original_83_84_or_167_168_historic_index_winner"] is False,"no historical winner")
 ck(e["counts"]==dict(sources_root=647,sources_extensions=118,sources_total=765,matrix_rows=222,matrix_audited=222,graph_nodes=252,graph_edges=238,open_risks=11),"counts")
 x=e["scope"]
 ck(x["product"]=="CLOSED" and x["physical_copy_edition_binding_still_open"] is True and all(x[k]==0 for k in ("algorithm_reopens","new_external_source_registry_entries","new_physical_witness_votes","new_chart_winner_selections")),"scope")
 ck(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"not ancient lineage")
 a=state["historical_audit"];h=a["current_focus"]; li=ledger["binding"]
 ck(any(z.startswith("13LB ") for z in h) and any(z.startswith("13LC ") for z in h),"research continuity")
 ck(li["latest_research_focus_prefix"]==h[-1].split(" ",1)[0] and li["source_focus_count"]==len(h),"rolling latest focus")
 ck(state["schema_version"]==li["reviewed_state_version"]==a["research_omission_guard"]["reviewed_state_version"] and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"state review")
 issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
 ck(issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith(li["latest_research_focus_prefix"]+" CURRENT ACTION:"),"issue forward")
 ck(E in issue["source_refs"] and "docs/research/TIANWEN-13LC-MINGSHI-SIKU-1739-1782-EDITION-CHRONOLOGY-SCOPE-R1.md" in issue["source_refs"] and any(z.get("revision_id")=="TW-OPEN-0005-13LC-SIKU-CHRONOLOGY-20261030" for z in issue["history"]),"evidence history")
 ck(len(ledger["issues"])==11 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product")
 return {"status":"PASS","wuying_year":1739,"siku_first_copy":1782,"new_original_numeric_votes":0,"open_risks":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))

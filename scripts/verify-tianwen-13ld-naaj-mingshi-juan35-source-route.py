#!/usr/bin/env python3
"""13LD source-route gate: official NAAJ exact volume identity, physical copy firewall, no ancient target vote."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LD-NAJDA-2810038-MINGSHI-JUAN35-ORIGINAL-SOURCE-ROUTE-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(a,s):
 if not a:raise ValueError(s)
def load():return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,S,L))
def verify(e,state,ledger):
 check(e["schema"]=="TIANWEN-13LD-NAJDA-2810038-MINGSHI-JUAN35-ORIGINAL-SOURCE-ROUTE-R1" and e["issue_id"]=="TW-OPEN-0005","identity")
 x=e["original_catalog"]
 check(x["reference_code"]=="281-0038" and x["catalog_url"]=="https://www.digital.archives.go.jp/file/en/3610285" and x["physical_set_size_volumes"]==112,"holding")
 check(x["target_book_order"]=="0011" and x["target_item_title"]=="明史 志第11-13" and x["target_chapter"]=="明史卷三十五 = 志第十一","source part")
 check(not x["original_target_glyph_observed"] and not x["direct_physical_impression_date_observed"],"uncollated pages")
 y=e["cross_holdings_control"]
 check(y["another_reference_code"]=="281-0037" and y["another_set_size_volumes"]==120 and not y["same_holding_as_2810038_proven"] and not y["actual_printing_block_identity_equivalence_proven"] and not y["independent_original_glyph_vote"],"two separate copies")
 q=e["commons_source_route"]
 check(q["exact_filename"]=="NAJDA-281-0038 明史 志第11-13.pdf" and q["commons_api"]=="https://commons.wikimedia.org/w/api.php","source filename")
 check(q["acquisition_script"]=="scripts/probe-tianwen-13ld-naaj-mingshi-juan35-original.py" and q["acquisition_workflow"]==".github/workflows/probe-tianwen-13ld-naaj-mingshi-juan35-original.yml","probe")
 check(all(q[k] is None for k in ("expected_pdf_sha1","expected_pdf_size","expected_pdf_page_count")) and q["original_pdf_bytes_acquired"] is False and q["target_page_human_gloss_review"] is False and q["roi_hash_review_complete"] is False,"no pre-award")
 check(e["counts"]==dict(source_registry_root=647,source_registry_extension=118,source_registry_total=765,matrix_rows=222,audited_rows=222,graph_nodes=252,graph_edges=238,risks_open=11),"baseline")
 z=e["scope"]
 check(z["product"]=="CLOSED" and all(z[k]==0 for k in ("algorithm_reopens","new_confirmed_original_numeric_winners","new_external_registered_sources","new_graph_nodes","new_graph_edges")),"scope")
 check(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"ancestry")
 h=state["historical_audit"]["current_focus"]; binding=ledger["binding"]
 check(any(z.startswith("13LD ") for z in h) and binding["latest_research_focus_prefix"]==h[-1].split(" ",1)[0] and binding["source_focus_count"]==len(h),"focus")
 check(state["schema_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"]==ledger["checkpoint_log"][-1]["state_version"],"sync")
 issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
 check(issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(binding["latest_research_focus_prefix"]+" CURRENT ACTION:") and E in issue["source_refs"] and "docs/research/TIANWEN-13LD-NAJDA-2810038-MINGSHI-JUAN35-ORIGINAL-SOURCE-ROUTE-R1.md" in issue["source_refs"],"risk")
 check(any(x.get("revision_id")=="TW-OPEN-0005-13LD-NAJDA-2810038-20261030" for x in issue["history"]),"forward append")
 check(len(ledger["issues"])==11 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product")
 return {"status":"PASS","official_catalog":"281-0038","exact_book_order":"0011","numeric_winners":0,"risks_open":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))

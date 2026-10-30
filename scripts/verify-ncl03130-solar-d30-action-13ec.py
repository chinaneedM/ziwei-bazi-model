#!/usr/bin/env python3
"""13EC P0 queue reconcile original source readings without new witness claims."""
import json
from pathlib import Path
# Backward-looking assertions use append-only history, never overwrite live next_action.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EC-NCL03130-SOLAR-D30-NEXT-ACTION-RECONCILIATION-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EA="docs/research/TIANWEN-13EA-NCL03130-SOLAR-D28-D29-ORIGINAL-XINGDU-GLYPH-R1.json";EB="docs/research/TIANWEN-13EB-NCL03130-SOLAR-D27-D30-ORIGINAL-ROI-R1.json"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e,s,l,a,b):
 assert e["schema"]=="TIANWEN-13EC-NCL03130-SOLAR-D30-NEXT-ACTION-RECONCILIATION-R1" and e["kind"]=="QUEUE_CORRECTION_NO_NEW_ORIGINAL_GLYPH"
 assert e["issue_id"]=="TW-OPEN-0005" and e["sources"]["original_d28_d29"]==EA and e["sources"]["original_d27_d30"]==EB
 assert e["sources"]["part09_pdf_sha256"]==b["source"]["pdf_sha256"]
 assert e["sources"]["image_png_sha256"]==b["capture"]["png_sha256"]
 assert (e["sources"]["run"],e["sources"]["artifact"],e["sources"]["image_page"])==(b["capture"]["run"],b["capture"]["artifact_id"],76)
 assert [(z["day"],z["value"]) for z in e["established_source_positive"]]==[(27,b["rows"][0]["value"]),(28,a["original_source_rows"][0]["source_value"]),(29,a["original_source_rows"][1]["source_value"])]
 x=e["bounded_unresolved"];assert x["day"]==30 and x["visible_prefix"]==b["rows"][1]["visible_prefix"] and x["value"] is None and x["complete_literal"] is None
 assert all(e[k]==0 for k in ("actual_new_original_images","actual_new_glyph_readings","new_independent_physical_votes","new_matrix_rows","new_registry_sources","new_graph_edges","algorithm_reopens")) and e["issue_closed"] is False
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13EC FORWARD-ONLY P0 ACTION CORRECTION:") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 current_prefix=historical_action_view(issue).split(" ",1)[0]
 assert historical_action_view(issue).startswith(current_prefix+" CURRENT ACTION")
 assert "D30" in historical_action_view(issue) and e["bounded_unresolved"]["value"] is None
 assert all(z["day"] in (27,28,29) for z in e["established_source_positive"])
 assert set([EA,EB,E,E.replace(".json",".md")]).issubset(set(issue["source_refs"]))
 changes=[h for h in issue["history"] if h.get("event")=="ISSUE_REVISION" and "next_action" in h.get("changed_fields",[])]
 historic=next(h for h in changes if h.get("revision_id")=="TW-OPEN-0005-13EC-NEXT-ACTION-CORRECTION-20261023")
 assert changes[-1]["revision_id"].startswith("TW-OPEN-0005-"+current_prefix+"-")
 assert historic["previous_next_action"].startswith("13DZ CURRENT ACTION")
 assert set(historic["changed_fields"])=={"source_refs","next_action"}
 assert bool(changes[-1].get("evidence_refs")) and any(x.startswith(current_prefix+" ") for x in s["historical_audit"]["current_focus"])
 assert set([EA,EB,E,E.replace(".json",".md")]).issubset(set(historic["evidence_refs"]))
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L),load(EA),load(EB))
 print("13EC_PASS SOURCE_POSITIVE_27_28_29 D30_OPEN ACTION_CURRENT")

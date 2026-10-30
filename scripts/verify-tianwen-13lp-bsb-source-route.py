#!/usr/bin/env python3
"""13LP catalog-only evidence gate with forward-only state / ledger binding."""
import json
from pathlib import Path
# Archived action terms come from preserved revisions, never from stale live next_action.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-13LP-BSB1739-MINGSHI-IIIF-CATALOG-AND-ATLAS-TRIAGE-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf8")) for p in [PATH,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
def check(e,s,l):
 assert e["issue_id"]=="TW-OPEN-0005" and e["schema"]=="TIANWEN-13LP-BSB1739-MINGSHI-IIIF-CATALOG-AND-ATLAS-TRIAGE-R1"
 c=e["first_party_catalog"]
 assert c["provider_item_id"]=="bsb11166692"
 assert c["institutional_manifest"]=="https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11166692/manifest"
 assert c["actual_chapter_juan35_in_this_object"]=="NOT_YET_LOCATED"
 assert c["specific_target_leaf_and_glyph"]=="NOT_YET_EXAMINED"
 assert c["exact_holding_and_specific_1739_impression_binding"]=="NOT_YET_ESTABLISHED"
 assert c["historical_witness_vote"]==0
 assert e["acquisition_probe"]["no_ocr"] is True and e["acquisition_probe"]["provider_transport_status_at_commit"]=="UNRUN"
 assert e["source_inventory_crosscheck"]["new_source_record_added"]==0
 a=e["adjudication"]
 for key in ["new_juan35_original_glyph_positive","new_exactly_dated_physical_impression","same_or_distinct_woodblock_decided","original_calendar_worked_case_located"]:
  assert a[key] is False
 assert a["new_g893_numeric_winners"]==a["algorithm_reopens"]==0 and a["product"]=="CLOSED"
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 assert e["counts"]==dict(sources=765,matrix="222/222",genealogy_nodes=252,genealogy_edges=238,open_issues=11,chart="CLOSED",algorithm_reopens=0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,960,0)
 assert any(x.startswith("13LP ") for x in s["historical_audit"]["current_focus"])
 # Forward-only batches move the current prefix; archived 13LP must remain cited.
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and "13LP CURRENT ACTION:" in historical_action_view(issue)
 assert "13LO CURRENT ACTION:" in historical_action_view(issue) and PATH in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13LP-BSB-CATALOG-20261030" for x in issue["history"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","source_grade":"CATALOG_ONLY","original_glyph_winners":0}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))

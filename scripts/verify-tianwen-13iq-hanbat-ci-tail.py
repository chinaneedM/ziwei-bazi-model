#!/usr/bin/env python3
"""13IQ: official library list-only identity + exact-head CI tail guards."""
import json
from pathlib import Path
# Verify historical action text through append-only revisions, not the current instruction.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-13IQ-1972-HANBAT-SEARCH-AND-CI-TAIL-ERRATA-R1.json"
def load(path=DOC):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(d, with_repo=True):
 assert d["schema"]=="TIANWEN-13IQ-1972-HANBAT-SEARCH-AND-CI-TAIL-ERRATA-R1" and d["issue_id"]=="TW-OPEN-0005"
 h=d["first_party_hanbat"];a=h["list_results"]
 assert len(a)==2 and [(x["list_number"],x["detail_control"]) for x in a]==[(9,"000000277137"),(10,"000000277587")]
 assert all(x["catalog_year"]==1972 and x["catalog_publisher_literal"]=="亞世亞文化社" and x["detail_replay"]=="PAGE_NOT_FOUND" and x["photographed_original"] is False for x in a)
 assert h["relation_to_journal_GK5554"]=="UNBOUND_NO_1972_PRINTED_TARGET" and h["new_ancient_witness_votes"]==0
 ci=d["ci_tail"]
 assert ci["exact_head_workflow_total"]==225 and ci["completed_success"]==222 and ci["completed_failure"]==3
 assert set(ci["failures"])=={"verify-tianwen-13in-gk5553-material","verify-tianwen-13hz-nikh-d18","clean-training-system"}
 b=d["adjudication"]
 assert b["NLC03130_solar_D30_complete_original_numeric_value"] is None and b["NLC03130_summer_D14_numeric_value"] is None
 assert b["distinct_solar_summer_tables"] is True and b["prior_13io_retraction_preserved"] is True
 assert all(b[k]==0 for k in ("actual_new_old_book_leaf_images","new_source_registry_records","new_graph_nodes","new_graph_edges","algorithm_reopens","candidate_collapses"))
 if with_repo:
  st=load("docs/PROJECT-CURRENT-STATE-R1.json");ld=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  assert tuple(map(int,st["schema_version"].split(".")))>=(1,896,0)
  assert st["schema_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==ld["binding"]["reviewed_state_version"]
  assert ld["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
  assert any(q.startswith("13IQ ") for q in st["historical_audit"]["current_focus"])
  i=next(x for x in ld["issues"] if x["id"]=="TW-OPEN-0005")
  assert i["status"]=="OPEN" and DOC in i["source_refs"] and "solar D30" in historical_action_view(i) and "summer D14" in historical_action_view(i)
  test=(ROOT/"tests/test_tianwen_13in_gk5553_material.py").read_text(encoding="utf-8")
  assert 'a["snu_firstparty"]["book29_original_folio_images_obtained"]=True' in test
  v=(ROOT/"scripts/verify-tianwen-13hz-nikh-d18.py").read_text(encoding="utf-8")
  assert 'for tag in ("13HZ","13HY")' in v
  assert len(ld["issues"])==11 and ld["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 return True
if __name__=="__main__":
 assert check(load());print("TIANWEN_13IQ_HANBAT_CI_TAIL_PASS")

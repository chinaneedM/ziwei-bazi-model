#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-13IK-GK3467-JOURNAL-FIRSTPAGE-INDEX-AND-LACUNA-FIREWALL-R1.json"
def read(path=PATH): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(x,with_state=True):
    assert x["schema"]=="TIANWEN-13IK-GK3467-JOURNAL-FIRSTPAGE-INDEX-AND-LACUNA-FIREWALL-R1"
    assert x["issue_id"]=="TW-OPEN-0005"
    a=x["source_layer"]
    assert a["institutional_page_publication_date"]=="2020-03-15"
    assert a["journal_year"]==2020 and a["journal_issue"]==1 and a["journal_serial_issue"]==177
    assert a["indexed_pdf_first_page_authors"]==["魏志江","陈卓"]
    assert a["indexed_pdf_first_page_article_number"]=="1002-5332(2020)01-0093-12"
    assert a["article_number_last_page_arithmetic_only"]==104
    assert a["first_page_bibliography_evidence_grade"]=="SEARCH_ENGINE_INDEXED_PDF_TEXT_NOT_OBTAINED_SOURCE_PDF_OR_ORIGINAL_PAGE_IMAGE"
    assert a["pdf_binary_obtained"] is False and a["pdf_sha256"] is None
    for k in ("original_article_target_paragraph_original_page_verified","original_article_target_footnotes_verified","full_pdf_paginated_extent_verified"):
        assert a[k] is False
    b=x["received_republication"]
    assert b["source_type"]=="SECONDARY_WEB_REPUBLICATION" and b["footnotes"]=="OMITTED_IN_REPUBLICATION"
    assert b["second_independent_original_witness"] is False
    c=x["copy_layer"]
    assert c["printed_right_folio_anchors"]==[[4,2],[6,10],[7,11]]
    assert c["physically_missing_leaf_count"] is None
    for k in ("physical_intermediate_leaves_verified","own_winter_table_title_verified","original_day1_to_day7_verified","digital_surrogate_missing_leaf_proven","other_volume_lacuna_reporting_implies_volume52_completeness"):
        assert c[k] is False
    d=x["adjudication"]
    for k in ("new_physical_source_count","new_independent_historical_vote_count","source_registry_increment","graph_node_increment","graph_edge_increment","algorithm_reopen_count","candidate_collapse_count"):
        assert d[k]==0
    assert d["journal_identifier_for_precise_copy_request"] is True
    assert d["search_index_can_substitute_for_article_original"] is False
    assert d["secondary_republication_can_certify_local_missing_leaves"] is False
    assert d["journal_original_page_status"]=="OPEN" and d["holding_specific_physical_collation_status"]=="OPEN"
    v=x["invariants"]
    assert v=={"matrix":[222,222],"source_registry":761,"graph":[252,238],"research_risks":11,"product":"CLOSED","algorithm_reopens":0,"candidate_collapses":0}
    if with_state:
        state=read("docs/PROJECT-CURRENT-STATE-R1.json")
        ledger=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]
        assert ledger["binding"]["latest_research_focus_prefix"]=="13IK"
        assert state["historical_audit"]["current_focus"][-1].startswith("13IK ")
        issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
        assert issue["status"]=="OPEN" and PATH in issue["source_refs"]
        assert issue["history"][-1]["new_action_prefix"]=="13IK"
    return True
if __name__=="__main__":
    assert check(read())
    print("TIANWEN_13IK_JOURNAL_INDEX_AND_LACUNA_FIREWALL_PASS")

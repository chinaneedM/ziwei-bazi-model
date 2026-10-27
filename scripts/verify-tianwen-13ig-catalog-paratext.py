#!/usr/bin/env python3
"""Restrict GK3467 catalog-frontmatter statements to bibliography, not its original leaves."""
import gzip
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE="docs/research/TIANWEN-13IG-GK3467-CATALOG-PARATEXT-VS-PHYSICAL-LEAF-BOUNDARY-R1.json"
def load(path=EVIDENCE):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(d,with_state=True):
    assert d["schema"]=="TIANWEN-13IG-GK3467-BIBLIOGRAPHIC-PARATEXT-AND-PHYSICAL-LEAF-SCOPE-R1"
    assert d["issue_id"]=="TW-OPEN-0005"
    source=d["source"]
    archived=gzip.decompress((ROOT/source["archived_html"]).read_bytes())
    assert hashlib.sha256(archived).hexdigest()==source["archived_html_sha256_uncompressed"]
    html=archived.decode("utf-8")
    for token in ("乙亥字","[刊年未詳]","1冊外缺","卷首","進高麗史箋"):
        assert token in html, ("not found in original catalog",token)
    old=(ROOT/source["prior_original_cover"]).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(old)).encode()+b"\\0"+old).hexdigest()==source["prior_original_cover_blob_sha"]
    older=json.loads(old)
    assert older["navigation_transition"]["before"]=="002b"
    assert older["navigation_transition"]["after"]=="003a"
    assert older["review_grade"]["title_rubric_and_initial_D7_recovered"] is False
    assert source["publication_year_label"]=="[刊年未詳]"
    assert d["catalog_level"]["has_frontmatter_bibliographic_field"] is True
    assert "NOT_SOURCE-PIXEL" in d["catalog_level"]["means"]
    grade=d["source_copy_grade"]
    for k in ("first_day_0_to_7_original_page","own_winter_table_title_original_page","own_technical_A_rubric_original_page","frontmatter_physical_presence_in_book6","catalog_date_as_print_date","exact_impression_year","book_level_physical_leaf_missing_count"):
        assert grade[k] is None,k
    assert grade["all_104_source_listed_images_acquired"] is False
    assert grade["whole_book_linewise_negative_proof"] is False
    for key,val in d["adjudication"].items():
        if isinstance(val,bool): assert val is False,key
    inv=d["invariants"]
    assert inv["matrix"]==[222,222] and inv["registered_sources"]==761
    assert (inv["genealogy_nodes"],inv["genealogy_edges"])==(252,238)
    assert inv["omission_issues_open"]==11 and inv["product"]=="CLOSED"
    assert inv["algorithm_reopens"]==inv["candidate_collapses"]==0
    if with_state:
        state=load("docs/PROJECT-CURRENT-STATE-R1.json")
        ledger=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        assert tuple(map(int,state["schema_version"].split(".")))>=(1,886,0)
        assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]
        assert state["historical_audit"]["current_focus"][-1].startswith("13IG ")
        issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
        assert issue["status"]=="OPEN" and EVIDENCE in issue["source_refs"]
        assert issue["next_action"].startswith("13IG CURRENT ACTION:")
    return True
if __name__=="__main__":
    assert check(load())
    print("TIANWEN_13IG_FIRSTPARTY_CATALOG_PARATEXT_COPY_GRADE_PASS")

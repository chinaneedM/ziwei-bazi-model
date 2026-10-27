#!/usr/bin/env python3
import json, hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-13IJ-GK3467-SOURCE-SPREAD-AND-JOURNAL-ROUTE-R1.json"
def read(path=PATH):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(x,with_state=True):
    assert x["schema"]=="TIANWEN-13IJ-GK3467-SOURCE-SPREAD-AND-JOURNAL-ROUTE-R1"
    assert x["issue_id"]=="TW-OPEN-0005"
    pages=x["source"]["native_original_pages"]
    assert [p["page"] for p in pages]==[4,5]
    for p in pages:
        raw=(ROOT/p["path"]).read_bytes()
        assert len(raw)==p["bytes"] and hashlib.sha256(raw).hexdigest()==p["raw_sha256"]
        im=Image.open(ROOT/p["path"]).convert("RGB")
        assert list(im.size)==p["size"]
        assert hashlib.sha256(im.tobytes()).hexdigest()==p["rgb_sha256"]
    a=x["original_spread_visual_sequence"]
    assert [(y["page"],y["side"]) for y in a]==[(4,"RIGHT"),(4,"LEFT"),(5,"RIGHT"),(5,"LEFT")]
    assert [y["day_range"] for y in a]==[None,[8,11],[12,16],[17,20]]
    assert x["old_source_original_right_folios"]==[[4,2],[6,10],[7,11]]
    j=x["article_probe"]
    assert j["response"]=="HTTP_404_GITHUB_RUNNER" and j["run_id"]==40502065242
    assert j["pdf_sha256"] is None
    for k in ("pdf_magic_obtained","original_target_page_seen","article_absent_proven"):assert j[k] is False
    d=x["adjudication"]
    for k in ("first_day1_to_day7_original_obtained","own_table_title_obtained","left_hand_folio_number_obtained","source_physical_adjacency_proven","original_physical_leaf_loss_proven","microfilm_omission_proven"):assert d[k] is False
    assert d["number_of_physically_missing_leaves"] is None
    assert all(d[k]==0 for k in ("second_independent_witness_count","new_source_registry_entries","new_graph_edges","algorithm_reopens"))
    inv=x["invariants"]
    assert inv["matrix"]==[222,222] and inv["sources"]==761 and inv["graph"]==[252,238]
    assert inv["open_issues"]==11 and inv["product"]=="CLOSED"
    if with_state:
        s=read("docs/PROJECT-CURRENT-STATE-R1.json")
        l=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        assert s["schema_version"]==l["binding"]["reviewed_state_version"]
        assert any(f.startswith("13IJ ") for f in s["historical_audit"]["current_focus"])
        issue=next(i for i in l["issues"] if i["id"]==x["issue_id"])
        assert issue["status"]=="OPEN" and PATH in issue["source_refs"]
        assert any(h.get("new_action_prefix")=="13IJ" for h in issue["history"])
    return True
if __name__=="__main__":
    assert check(read())
    print("TIANWEN_13IJ_SOURCE_AND_PDF_ACCESS_BOUNDARY_PASS")

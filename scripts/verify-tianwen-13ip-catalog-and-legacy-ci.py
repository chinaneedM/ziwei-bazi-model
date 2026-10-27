#!/usr/bin/env python3
"""13IP: bibliographic non-equivalence and append-only history replay."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-13IP-1972-GORYEOSA-CATALOG-AND-HISTORIC-CI-R1.json"
def read(path=DOC):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e, with_repo=True):
    assert e["schema"]=="TIANWEN-13IP-1972-GORYEOSA-CATALOG-AND-HISTORIC-CI-R1" and e["issue_id"]=="TW-OPEN-0005"
    a,b,c,y=e["bibliographic_controls"]
    assert (a["ncid"],a["volumes"],a["size_cm"])==("BA63617326",3,21)
    assert (b["ncid"],b["volumes"],b["size_cm"])==("BB04922175",3,22)
    assert (c["ncid"],c["issued"],c["reprint"])==("BA6602288X","1983.4",True)
    assert (y["publisher"],y["volumes"])==("延世大學校 東方學硏究所",4)
    x=e["adjudication"]
    assert x["specific_NCID_bound_to_GK5554_paper_claim"] is False
    assert x["book29_to_juan81_83_binding_retracted_by_13io"] is True
    assert x["reprint_1983_not_original_1972_page"] is True
    assert all(x[k]==0 for k in ("new_original_pages","new_source_registry_records","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
    assert e["paper_2020"]["physical_1972_original_leaf_obtained"] is False
    ci=e["ci_repair"]
    assert (ci["sampled_runs"],ci["sampled_failure_runs"])==(224,24)
    assert len(ci["patched_verifiers"])==24 and len(set(ci["patched_verifiers"]))==24
    assert ci["historical_source_json_untouched"] is True
    if with_repo:
        s=read("docs/PROJECT-CURRENT-STATE-R1.json")
        ld=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        assert tuple(map(int,s["schema_version"].split(".")))>=(1,895,0)
        assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==ld["binding"]["reviewed_state_version"]
        assert ld["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
        assert any(t.startswith("13IP ") for t in s["historical_audit"]["current_focus"])
        issue=next(z for z in ld["issues"] if z["id"]=="TW-OPEN-0005")
        assert issue["status"]=="OPEN" and DOC in issue["source_refs"]
        assert any(q.get("revision_id","").startswith("TW-OPEN-0005-13IP-") for q in issue["history"])
        for path in ci["patched_verifiers"]:
            p=ROOT/path
            assert p.is_file()
            content=p.read_text(encoding="utf-8")
            if path.endswith("13in-gk5553-material.py"):
                assert 'a["book29_original_folio_images_obtained"]' in content
            else:
                assert 'h.get("revision_id"' in content and '"next_action" in h.get("changed_fields"' in content
        old=read("docs/research/TIANWEN-13IN-GK5553-BOOK29-MATERIAL-CONFLICT-R1.json")
        err=read("docs/research/TIANWEN-13IO-GK5553-CROSSWALK-AND-CONCURRENT-HANDOFF-ERRATUM-R1.json")
        assert old["snu_firstparty"]["book29_juan"]==[81,82,83]
        assert err["historical_erratum"]["new_status"]=="RETRACTED_UNBOUND_COPY_TO_JUAN_CROSSWALK"
        assert len(ld["issues"])==11
        assert ld["checkpoint_log"][-1]["state_version"]==s["schema_version"]
    return True
if __name__=="__main__":
    assert check(read())
    print("TIANWEN_13IP_CATALOG_AND_HISTORY_REPLAY_PASS")

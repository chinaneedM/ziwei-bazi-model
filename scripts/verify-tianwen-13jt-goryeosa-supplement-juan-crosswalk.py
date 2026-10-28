#!/usr/bin/env python3
"""13JT: reconcile Goryeosa 世家/志 internal versus global juan across 1972 facsimile descriptions."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
P = "docs/research/TIANWEN-13JT-1972-GORYEOSA-WOODBLOCK-SUPPLEMENT-JUAN-NUMBER-CROSSWALK-R1.json"
PRIOR = "docs/research/TIANWEN-12ZL-GORYEOSA-1972-MIXED-FACSIMILE-AND-5553-SUPPLEMENT-CONFLICT-R1.json"

def load():
    return tuple(json.loads((ROOT / name).read_text(encoding="utf-8")) for name in
                 (P, PRIOR, "docs/PROJECT-CURRENT-STATE-R1.json", "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))

def verify(e, prior, state, ledger):
    assert e["schema"] == "TIANWEN-13JT-1972-GORYEOSA-WOODBLOCK-SUPPLEMENT-JUAN-CROSSWALK-R1"
    assert e["issue_id"] == "TW-OPEN-0005"
    assert len(e["source_records"]) == 3
    assert all(z["original_1972_colophon_or_folio_seen"] is False for z in e["source_records"])
    assert e["source_records"][0]["url"] == "https://encykorea.aks.ac.kr/Article/E0003456"
    assert e["source_records"][1]["repository_prior"] == PRIOR
    n = e["normalization"]
    assert n["sega_global_start"] == 1 and n["sega_global_end"] == 46
    assert (n["ji_global_start"], n["ji_global_end"], n["ji_relative_offset"], n["ji_length"]) == (47,85,46,39)
    a, w, c = n["aks"], n["wei_chen_2020"], n["comparison"]
    assert a["sega_juan"] == [19,20,21,31] and a["ji_internal_juan"] == [27,28,31,33,35,37]
    assert all(1 <= x <= 39 for x in a["ji_internal_juan"])
    normalized = sorted(a["sega_juan"] + [x + n["ji_relative_offset"] for x in a["ji_internal_juan"]])
    assert normalized == a["expected_global_juan"]
    assert prior["source_evidence"]["academic"]["replaced_work_volumes"] == w["reported_global_juan"]
    assert w["previous_immutable_data_path"] == PRIOR
    p, q = set(normalized), set(w["reported_global_juan"])
    assert len(p) == 10 and len(q) == 12 and len(q) == len(w["reported_global_juan"])
    assert sorted(p & q) == c["intersection_global_juan"]
    assert sorted(p - q) == c["only_aks_global_juan"] == []
    assert sorted(q - p) == c["only_wei_chen_global_juan"] == [78,82]
    assert [x - 46 for x in sorted(q - p)] == c["only_wei_chen_ji_internal_juan"] == [32,36]
    assert [(r["work_global_juan"],r["ji_internal_juan"],r["topic"]) for r in c["contested_context"]] == [(78,32,"食貨一"),(82,36,"兵二")]
    assert 52 not in p and 52 not in q
    assert c["full_work_juan_52_in_aks_or_wei_chen_supplement_lists"] is False
    assert c["no_list_proves_1972_work_juan_52_printing_copy"] and c["distinct_secondary_descriptions_not_two_ancient_copy_votes"]
    z = e["conclusion"]
    for k in ("modern_descriptions_show_two_entry_supplement_scope_disagreement", "not_sufficient_to_adjudicate_1972_edition_winner", "akademy_institution_name_is_not_physical_leaf_provenance", "akademy_catalog_does_not_invalidate_2020_paper_without_1972_original", "past_12zl_2020_record_must_remain_unchanged"):
        assert z[k] is True, k
    assert all(z[k] is False for k in ("source_1972_page_read", "juan_78_original_leaf_read", "juan_82_original_leaf_read"))
    assert z["khs_8_12_26_vs_snu_8_26_29"] == "OPEN" and z["old_13io_physical_book29"] == "RETRACTED_UNBOUND"
    assert z["deterministic_chart_product"] == "CLOSED"
    assert all(z[k] == 0 for k in ("new_g893_six_numeric_decisions","independent_ancient_physical_copy_votes","registry_growth","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"))
    focus = state["historical_audit"]["current_focus"]
    assert any(x.startswith("13JS ") for x in focus) and any(x.startswith("13JT ") for x in focus)
    assert state["schema_version"] == ledger["binding"]["reviewed_state_version"] == state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert len(focus) == ledger["binding"]["source_focus_count"]
    assert ledger["binding"]["latest_research_focus_prefix"] == focus[-1].split(" ",1)[0]
    issue = next(x for x in ledger["issues"] if x["id"] == "TW-OPEN-0005")
    assert issue["status"] == "OPEN" and issue["priority"] == "P0"
    assert P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"]
    revisions = [(idx,x) for idx,x in enumerate(issue["history"]) if x.get("revision_id") == "TW-OPEN-0005-13JT-1972-SUPPLEMENT-CROSSWALK-20261028"]
    assert len(revisions) == 1
    index, row = revisions[0]
    assert row["event"] == "ISSUE_REVISION" and row["evidence_refs"] == [P,P.replace(".json",".md")]
    assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13JS-") for x in issue["history"][:index])
    assert ledger["checkpoint_log"][-1]["state_version"] == state["schema_version"]
    assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"]) == {x["id"] for x in ledger["issues"]}
    return {"status":"PASS","aks_global_juan":10,"wei_chen_global_juan":12,"contested_juan":[78,82],"ancient_original_witnesses_added":0}

if __name__ == "__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))

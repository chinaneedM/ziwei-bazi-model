#!/usr/bin/env python3
"""13BI: ensure current P0 handoff does not regress to obsolete 12YY no-original claim."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BI-GORYEOSA-P0-ORIGINAL-RECOVERY-ACTION-HANDOFF-ERRATUM-R1.json"
PBE="docs/research/TIANWEN-13BE-GORYEOSA-D16-ORIGINAL-LONG-LANE-DUAL-COPY-COLLATION-R1.json"
PBG="docs/research/TIANWEN-13BG-GORYEOSA-NAJ-ADJACENT-FOLIOS-CUMULATIVE-D17-D19-R1.json"
PBH="docs/research/TIANWEN-13BH-GORYEOSA-NAJ-ORIGINAL-RECEIVED-CUMULATIVE-FIVEPOINT-OFFSET-R1.json"
MD="docs/research/TIANWEN-13BI-GORYEOSA-P0-ORIGINAL-RECOVERY-ACTION-HANDOFF-ERRATUM-R1.md"
def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,be,bg,bh,ledger,state):
    assert e["schema"]=="TIANWEN-13BI-GORYEOSA-P0-RESEARCH-HANDOFF-STALE-ACTION-CORRECTION-R1"
    assert e["issue_id"]=="TW-OPEN-0005" and e["prior_12YY_action_is_historical_snapshot"] is True
    assert "尚未取得对应《高丽史》印本原叶" in e["prior_action_text"]
    assert e["revision_class"]=="SOURCE_SCOPED_FORWARD_ONLY_CURRENT_ACTION_CORRECTION_NOT_NEW_PHYSICAL_COLLATION"
    refs=e["source_positive_reconciliation"]
    assert len(refs)==3
    assert [(x["source"],x["evidence"],x["verified_sha"]) for x in refs]==[
       ("NAJ-282-0006-PHYSICAL51",PBE,be["source_original_image_reviews"][0]["original_image_sha256"]),
       ("WASEDA-RI06-02809-BOOK33",PBE,be["source_original_image_reviews"][1]["original_image_sha256"]),
       ("NAJ-282-0006-PHYSICAL51",PBG,bg["source_canvases"][2]["source_jpeg_sha256"])]
    assert e["received_text_alignment"]["evidence"]==PBH
    assert e["received_text_alignment"]["five_local_values_replayed"]==len(bh["observed_original_vs_received"])==5
    assert e["received_text_alignment"]["proof_of_universal_index"] is False
    w=e["first_party_Waseda_catalog"]
    assert w["call_number"]=="リ06 02809" and w["volumes"]=="80冊"
    assert w["imprint"]=="[出版地不明] : [出版者不明], [出版年不明]"
    assert e["D16_facts"]=={"NAJ_original_short":"5.1362","Waseda_original_short":"5.1362","NAJ_original_long_delta":"5.2362","G893_different_work_short":"5.2362","historical_archetype":"UNRESOLVED"}
    assert set(e["unresolved_scopes"])>={"WASEDA_P23_D18_D19_ORIGINAL_CUM_NATIVE_ROI","NAJ_SOURCE_TABLE_START_AND_END","G893_CROSS_WORK_COLUMN_UNIT_EQUALITY"}
    assert all(v==0 for k,v in e["counters"].items() if k in ("new_original_images","new_source_registry_items","new_matrix_rows","new_lineage_nodes","new_lineage_edges","algorithm_reopens"))
    assert e["counters"]["research_issues_open_or_blocked"]==11 and e["counters"]["chart_product"]=="CLOSED"
    i=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    assert i["priority"]=="P0" and i["status"]=="OPEN"
    assert i["source_refs"].count(MD)==i["source_refs"].count(P)==1
    assert i["source_refs"].index(P)==i["source_refs"].index(MD)+1
    assert "[13BI 2026-10-21 FORWARD-ONLY CURRENT-BOUNDARY REVISION]" in i["evidence_boundary"]
    assert "[13BI 2026-10-21 FORWARD-ONLY CURRENT-GAPS REVISION]" in i["missing_evidence"]
    revision=next(x for x in i["history"] if x.get("revision_id")=="TW-OPEN-0005-CURRENT-ACTION-13BI")
    assert revision["event"]=="ISSUE_REVISION"
    assert set(revision["changed_fields"])=={"evidence_boundary","missing_evidence","next_action"}
    assert revision["previous_next_action"]==e["prior_action_text"]
    assert set([PBE,PBG,PBH,MD,P]).issubset(set(revision["evidence_refs"]))
    assert i["next_action"]==e["corrected_next_action"] or any(
       x.get("event")=="ISSUE_REVISION" and "next_action" in x.get("changed_fields",[]) and x is not revision
       for x in i["history"][i["history"].index(revision)+1:])
    assert "尚未取得对应《高丽史》印本原叶" not in i["next_action"]
    assert e["future_sessions_must_not_reopen_acquisition_gap_from_12YY"] is True
    assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert any(x.startswith("13BI ") for x in state["historical_audit"]["current_focus"])
    assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
    assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0]
    assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
    assert len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11
    return True
if __name__=="__main__":
    assert check(load(P),load(PBE),load(PBG),load(PBH),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
    print("13BI P0 original recovery handoff erratum gate PASS")

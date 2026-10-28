#!/usr/bin/env python3
"""13JQ: fail-closed 1972 Goryeosa publisher/volume disambiguation."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
P = "docs/research/TIANWEN-13JQ-GORYEOSA-1972-IMPRINT-COLLISION-BIBLIOGRAPHIC-FIREWALL-R1.json"

def load():
    return tuple(json.loads((R / p).read_text(encoding="utf-8")) for p in (
        P, "docs/PROJECT-CURRENT-STATE-R1.json", "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))

def check(proof, state, ledger):
    assert proof["schema"] == "TIANWEN-13JQ-GORYEOSA-1972-IMPRINT-COLLISION-BIBLIOGRAPHIC-FIREWALL-R1"
    assert proof["issue_id"] == "TW-OPEN-0005"
    riss, cinii, ndl = proof["catalog_records"]
    assert (riss["provider"],riss["year"],riss["publisher"]) == ("RISS Korean academic research catalog", 1972, "延世大學校 東方學硏究所")
    assert riss["control_no"] == "fcd7675d736aef1d" and len(riss["internal_volume_map"]) == 4
    assert riss["internal_volume_map"]["842"] == "志 年表"
    assert cinii["ncid"] == "BA63617326" and cinii["year"] == 1972
    assert cinii["publisher"] == "亞細亞文化社" and cinii["edition_description"].startswith("3冊")
    assert ndl["ncid"] == "BN11459541" and ndl["year"] == 1981
    assert all(not row["original_folio_examined"] and not row["copy_gk5553_or_gk5554_bound"] for row in proof["catalog_records"])
    a = proof["adjudication"]
    assert a["year_only_1972_is_nonunique"] and a["four_volume_yonsei_record_is_not_three_volume_asia_record"]
    assert a["three_volume_asia_and_four_volume_yonsei_must_not_be_merged"]
    assert a["direct_modern_catalogs_do_not_establish_original_edition_composition"]
    assert a["proof_asia_1972_is_exact_12zl_reported_facsimile"] is False
    assert a["source_original_1972_pages_verified"] == a["new_independent_ancient_physical_witnesses"] == 0
    assert a["g893_six_target_original_numeric_decisions"] == a["algorithm_reopens"] == 0
    assert a["external_source_registry_additions"] == a["genealogy_nodes_added"] == a["genealogy_edges_added"] == 0
    assert a["khs_8_12_26_vs_snu_8_26_29"] == "OPEN"
    assert a["prior_13io_physical_volume29_binding"] == "RETRACTED_UNBOUND"
    assert a["deterministic_chart"] == "CLOSED"
    f = state["historical_audit"]["current_focus"]
    assert any(x.startswith("13JP ") for x in f) and any(x.startswith("13JQ ") for x in f)
    assert len(f) == ledger["binding"]["source_focus_count"]
    assert ledger["binding"]["latest_research_focus_prefix"] == f[-1].split(" ",1)[0]
    assert state["schema_version"] == ledger["binding"]["reviewed_state_version"] == state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    issue = next(i for i in ledger["issues"] if i["id"] == "TW-OPEN-0005")
    assert issue["status"] == "OPEN"
    assert P in issue["source_refs"] and P.replace(".json", ".md") in issue["source_refs"]
    assert issue["history"][-1]["event"] == "ISSUE_REVISION"
    assert issue["history"][-1]["revision_id"] == "TW-OPEN-0005-13JQ-1972-BIBLIOGRAPHIC-IMPRINT-COLLISION-20261028"
    assert ledger["checkpoint_log"][-1]["state_version"] == state["schema_version"]
    assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"]) == {i["id"] for i in ledger["issues"]}
    return {"status":"PASS","modern_1972_imprints_distinguished":2,"new_ancient_witnesses":0,"g893_numeric_decisions":0}

if __name__ == "__main__":
    print(json.dumps(check(*load()), ensure_ascii=False))

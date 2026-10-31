#!/usr/bin/env python3
"""13MM received-text D16 arithmetic check; never promotes to original G893."""
import json
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MM-GORYEOSA-D16-RECEIVED-DISCREPANCY-1569-PRINT-GATE-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def dec(s):
    d=Decimal(s)
    assert d.as_tuple().exponent == -4, "four displayed decimal places required"
    return d
def check(e,s,l):
    assert e["schema"]=="TIANWEN-13MM-GORYEOSA-D16-RECEIVED-DISCREPANCY-1569-PRINT-GATE-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    src=e["source_layers"]
    k=src["official_korean_received"]
    assert k["url"]=="https://db.history.go.kr/id/kr_052r_0010_0010_0020_0010"
    assert k["day_index"]==[14,15,16,17,18]
    values=list(map(dec,k["received_day_difference"]))
    assert values==list(map(Decimal,["5.1990","5.2176","5.1362","5.2548","5.2734"]))
    assert src["wikisource_received"]["day16_string"]=="五分一三六二"
    assert src["wikisource_received"]["physical_copy_bound"] is False
    z=src["zhouxiang_1569_original"]
    assert z["prior_evidence"]=="docs/research/TIANWEN-13MJ-ZHOUXIANG-1569-D15-D17-PRINTED-SOURCE-VS-G893-GATE-R1.json"
    assert z["pdf_sha256"]=="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
    assert z["page_rgb_sha256"]=="7b35af0e1e802c9346c927a02c67d1681e01b5120c3cf891160126f2018478d5"
    assert z["crop_rgb_sha256"]=="72f4069db6044ce0b77f85259303c830b4f1cd14407469f73ac37e6d00632e41"
    assert z["printed_day_index"]==[15,16,17]
    orig=list(map(dec,z["printed_decimals"]))
    assert orig==list(map(Decimal,["5.2176","5.2362","5.2548"]))
    g=src["g893_original"]
    assert g["page_001a_sha256"]=="8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5"
    assert g["page_002b_sha256"]=="f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"
    assert g["header_001a_observed"]=="加一秒八十六少"
    assert g["page_002b_D16_day_heading_verified"] is True
    assert g["page_002b_D16_exact_numeric_lane_collected_for_this_batch"] is False
    a=e["arithmetic"]
    assert values[1]-values[0]==dec(a["d15_minus_d14"])==dec(a["normal_increment"])
    assert values[2]-values[1]==dec(a["received_d16_minus_d15"])
    assert values[3]-values[2]==dec(a["received_d17_minus_d16"])
    assert values[4]-values[3]==dec(a["d18_minus_d17"])
    interpolated=(values[1]+values[3])/2
    assert interpolated==dec(a["interpolated_d16_from_neighbors"])==orig[1]
    assert values[2]==dec(a["received_d16"])
    assert values[2]-interpolated==dec(a["received_d16_minus_interpolated"])==Decimal("-0.1000")
    assert orig[0]==values[1] and orig[2]==values[3]
    assert orig[1]-orig[0]==orig[2]-orig[1]==Decimal("0.0186")
    assert a["independent_1569_print_d16"]==z["printed_decimals"][1]
    assert a["exact_digit_replacement_candidate"]=="5.1362 -> 5.2362 (tenths digit, received-text candidate only)"
    guard=e["safeguards"]
    for name in ("online_transcriptions_are_independent_print_votes","received_d16_anomaly_proves_korean_physical_typo","independent_original_print_proves_G893_same_numeric_column","G893_001a_to_002b_D16_full_field_and_radix_bound"):
        assert guard[name] is False
    for name in ("cross_original_G893_six_historical_winners","new_registry_sources","new_independent_physical_copies","matrix_rows_changed","graph_nodes_added","graph_edges_added","candidate_collapse","algorithm_reopens"):
        assert type(guard[name]) is int and guard[name]==0
    assert guard["product"]=="CLOSED" and guard["transmission_impact"].startswith("NONE;")
    assert tuple(map(int,s["schema_version"].split(".")))>=(1,975,0)
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    focus=s["historical_audit"]["current_focus"]
    assert any(x.startswith("13MM ") for x in focus)
    assert len(focus)==l["binding"]["source_focus_count"]
    assert focus[-1].split(" ",1)[0]==l["binding"]["latest_research_focus_prefix"]
    issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
    assert issue["priority"]=="P0" and issue["status"]=="OPEN"
    assert {"docs/research/TIANWEN-13MM-GORYEOSA-D16-RECEIVED-DISCREPANCY-1569-PRINT-GATE-R1.json","docs/research/TIANWEN-13MM-GORYEOSA-D16-RECEIVED-DISCREPANCY-1569-PRINT-GATE-R1.md"}.issubset(set(issue["source_refs"]))
    event=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-13MM-RECEIVED-D16-20261031")
    assert {"docs/research/TIANWEN-13MM-GORYEOSA-D16-RECEIVED-DISCREPANCY-1569-PRINT-GATE-R1.json","docs/research/TIANWEN-13MM-GORYEOSA-D16-RECEIVED-DISCREPANCY-1569-PRINT-GATE-R1.md"}.issubset(set(event["evidence_refs"]))
    assert any(x.get("id")=="OMISSIONS-13MM-RECEIVED-D16-PRINT-GATE-20261031" and x.get("state_version")=="1.975.0" for x in l["checkpoint_log"])
    assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
    assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
    return {"status":"PASS","received_D16_outlier":"5.1362","interpolated_D16":"5.2362","historical_G893_winners":0}
if __name__=="__main__":
    print(json.dumps(check(*[json.loads(p.read_text(encoding="utf-8")) for p in (E,S,L)]),ensure_ascii=False))

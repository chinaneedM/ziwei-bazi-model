#!/usr/bin/env python3
"""13MV: test source-local day-zero and exact finite-difference scope, not historical cross-copy identity."""
import json
from pathlib import Path
from decimal import Decimal as D
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MV-ZHOU1569-DAYZERO-THREE-LANE-RECURRENCE-R1.json"
MU=R/"docs/research/TIANWEN-13MU-ZHOU1569-G893-D15-D16-THREE-LANE-CROSSWALK-R1.json"
MR=R/"docs/research/TIANWEN-13MR-ZHOU1569-ORIGINAL-OPERATOR-PRINTED-FIELD-SCOPE-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(e,mu,mr,s,l):
 assert e["schema"]=="TIANWEN-13MV-ZHOU1569-DAYZERO-THREE-LANE-RECURRENCE-R1"
 z=e["sources"]["zhou"]; a=e["original_source_local_day_anchor"]; b=e["original_source_local_lane_recurrence"]; t=e["received_text_comparator"]; q=e["bounds"]
 assert z["prior_verified_pdf_sha256"]==mu["originals"]["zhou"]["sha256"]==mr["source"]["prior_archived_source_sha256"]
 assert z["original_pages_1based"]==[14,15] and z["physical_impression"]=="UNBOUND"
 assert a["day0_label"]=="初日" and a["day1_label"]=="一日"
 assert a["day15_label"]=="十五日" and a["day16_label"]=="十六日"
 assert a["day1_high_place_inherited_from_adjacent_cells"] is True and a["page14_firstday_glyph_pixels_newly_rehashed"] is False
 s0=D(a["day0_short"]);s1=D(a["day1_short_normalized"]);delta=D(a["equal_step_hypothesis"])
 assert s0==D("4.9386") and delta==D("0.0186") and s1-s0==delta
 assert s0+15*delta==D(a["day15_short"])==D(mu["rows"][0]["zhou_short"])
 assert s0+16*delta==D(a["day16_short"])==D(mu["rows"][1]["zhou_short"])
 assert a["calendar_epoch"]=="UNPROVEN_OUTSIDE_THIS_SOURCE_LOCAL_TABLE"
 m15,m16=D(b["d15_middle"]),D(b["d16_middle"])
 c15,c16=D(b["d15_lower_cumulative"]),D(b["d16_lower_cumulative"])
 assert [str(m15),str(m16)]==[x["zhou_middle_normalized"] for x in mu["rows"]]
 assert [str(c15),str(c16)]==[x["zhou_lower_normalized"] for x in mu["rows"]]
 assert m15-m16==D(a["day15_short"]) and c16-c15==m15
 assert b["historical_unit_and_radix"]=="UNPROVEN"
 assert t["copied_1569_table_proven"] is False and t["use_scope"]=="CONFIRMS_RECEIVED_RULE_DESCRIPTION_COMPATIBLE_WITH_LOCAL_FINITE_DIFFERENCES_ONLY"
 assert q["new_original_physical_copies"]==q["new_source_registry_entries"]==q["new_graph_nodes"]==q["new_graph_edges"]==0
 assert q["g893_final_historical_winners"]==q["algorithm_reopens"]==0
 assert q["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert q["day0_is_absolute_calendar_epoch"] is False and q["received_mei_is_not_original_zhou_image"] is True
 assert all(q[k]=="OPEN" for k in ("g893_001a_to_002b_exact_header_unit_epoch","cross_source_unit_radix_epoch","naaj_official_item_impression"))
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==765
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,984,0)
 f=s["historical_audit"]["current_focus"]
 assert len(f)==l["binding"]["source_focus_count"] and any(x.startswith("13MV ") for x in f)
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert str(E.relative_to(R)) in issue["source_refs"] and str(E.with_suffix(".md").relative_to(R)) in issue["source_refs"]
 assert any(z.get("revision_id")=="TW-OPEN-0005-13MV-DAYZERO-RECURRENCE-20261031" for z in issue["history"])
 assert any(z.get("id")=="OMISSIONS-13MV-DAYZERO-RECURRENCE-20261031" for z in l["checkpoint_log"])
 assert "13MV" in [x.split(" ",1)[0] for x in f]
 return {"status":"PASS","source_original_pixels_newly_replayed":False,"source_local_recurrence_edges":4,"historic_cross_original_winners":0}
if __name__=="__main__":
 e,mu,mr,s,l=(json.loads(x.read_text(encoding="utf-8")) for x in (E,MU,MR,S,L))
 print(json.dumps(check(e,mu,mr,s,l),ensure_ascii=False))

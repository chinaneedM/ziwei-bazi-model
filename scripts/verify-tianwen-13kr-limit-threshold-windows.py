#!/usr/bin/env python3
"""13KR exact rational floor crossings and 83/84 threshold windows. No historic method award."""
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KR-HUANG-MING-DAILY-FLOOR-AND-83-84-THRESHOLD-WINDOW-R1.json"
def check(p,msg):
 if not p: raise ValueError(msg)
def read():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def fl(x):
 check(x>=0,"negative not supported")
 return x.numerator//x.denominator
def fraction_string(v):
 return str(v)
def verify(e,state,ledger):
 check(e["schema"]=="TIANWEN-13KR-LIMIT-THRESHOLD-WINDOWS-R1","schema")
 s=e["source_identity"]
 check(s["huang_pdf_sha256"]=="c524693e7bad502d222a1444d688cc7d63ca4a4037d7d4e08cee4aa94f9adbae","Huang PDF")
 check(s["ming_pdf_sha256"]=="dde1bfd5d3cf15954ddc6dbf1c020971806038bbc7f737b9053d5643e5c7c264","Ming PDF")
 check(s["source_pdf_byte_hashes_reverified_this_batch"] is True and s["source_pixel_hashes_reverified_this_batch"] is True,"source rereview")
 check(s["new_original_target_glyphs"]==0 and s["new_independent_witnesses"]==0,"no new source award")
 check(s["huang_physical_copy_authenticated"] is False and s["ming_specific_physical_impression_authenticated"] is False,"physical scope")
 x=e["conditional_model"]
 Eday=F(500,41);Aday=F(61,5)
 check(x["exact_daily_limit_fraction"]==str(Eday) and x["rounded_daily_limit_fraction"]==str(Aday),"daily rates")
 check(Aday-Eday==F(1,205) and x["approx_minus_exact"]=="t/205","daily delta")
 check(x["integer_day_domain"]==[0,28] and "not an attested historical rule" in x["integer_conversion"],"conditional floor")
 diffs=[];samples=[]
 for d in range(29):
  exact=d*Eday;approx=d*Aday
  check(approx-exact==F(d,205),"error for each day")
  diff=fl(approx)-fl(exact)
  check(diff in (0,1),"floor bound")
  if diff:
   diffs.append(d)
   samples.append(dict(elapsed_day=d,exact_raw_limits=str(exact),approx_raw_limits=str(approx),exact_trunc_limit=fl(exact),approx_trunc_limit=fl(approx),ceil_difference=diff,extra_approx_limits=str(F(d,205))))
 check(diffs==[5,10,15,20,25] and x["integer_day_disagreement_days"]==diffs and x["integer_day_disagreement_records"]==samples,"floor matches in all 29 inputs")
 check(x["source_counted_calendrical_epoch"] is False and x["physical_wall_clock_minute_translation_historically_attested"] is False,"clock/epoch")
 expected=[]
 for L in [83,84]:
  te=F(41*L,500);ta=F(5*L,61);w=te-ta
  check(w==F(L,30500) and w>0,"threshold width")
  mid=(te+ta)/2
  check(fl(mid*Eday)==L-1 and fl(mid*Aday)==L,"mid-window floor crossing")
  check(fl(te*Eday)==L and fl(te*Aday)>=L,"exact point closes window")
  expected.append(dict(integer_limit=L,exact_crossing_day=str(te),approx_crossing_day=str(ta),crossing_advance_day=str(w),illustrative_1440_minute_advance=str(1440*w)))
 check(x["thresholds"]==expected,"explicit exact 83/84 threshold records")
 check(x["limit_83_to_84_exact_gap"]==str(F(41,500)) and x["limit_83_to_84_approx_gap"]==str(F(5,61)),"one full limit interval not rounding window")
 b=e["claim_boundaries"]
 check(b["difference_less_than_one_limit_can_alter_floor"] is True,"positive limited claim")
 for k in ("proof_83_84_index_offset_caused_by_rounding","source_historic_integer_truncation_or_floor_attested","all_worked_orig_source_dates_collated","same_epoch_day_origin_proven","huang_ming_same_limit_variable_proven","modern_0_based_historical_choice_proven","ancient_copying_error_proven","chart_algorithm_reopened"):
  check(b[k] is False,"no historic promotion:"+k)
 check(e["counts"]==dict(source_registry=765,matrix_rows=222,graph_nodes=252,graph_edges=238,open_risks=11,g893_six_historical_numeric_winners=0,algorithm_reopens=0,chart_product="CLOSED"),"count invariants")
 check(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"no stemma award")
 a=state["historical_audit"];link=ledger["binding"]
 check(state["schema_version"]==a["research_omission_guard"]["reviewed_state_version"]==link["reviewed_state_version"],"state versions")
 check(len(a["current_focus"])==link["source_focus_count"] and a["current_focus"][-1].startswith(link["latest_research_focus_prefix"]+" "),"focus")
 check(a["external_source_registry_total_unique_count"]==765 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product")
 issue=next(i for i in ledger["issues"] if i["id"]==e["issue_id"])
 check(issue["priority"]=="P0" and issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"issue references")
 check(any(v.get("revision_id")=="TW-OPEN-0005-13KR-ROUNDING-FLOOR-20261029" and E in v.get("evidence_refs",[]) for v in issue["history"]),"append only")
 check(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"review")
 return {"status":"PASS","days":29,"divergent_integer_days":diffs,"threshold_windows":["83/30500","21/7625"],"historical_winners":0,"algorithm_reopens":0}
if __name__=="__main__":
 print(json.dumps(verify(*read()),ensure_ascii=False))

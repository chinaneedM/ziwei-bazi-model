from __future__ import annotations
import importlib.util,json
from decimal import localcontext
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
FIRST_YEAR=1368;LAST_YEAR=1644
def _load(name:str,path:Path):
 spec=importlib.util.spec_from_file_location(name,path);assert spec and spec.loader
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
oy=_load("ming_datong_multi_year_pb",ROOT/"scripts/research_ming_datong_multi_year_leap_validation_r1.py")
pa=_load("ming_datong_preyear_pb",ROOT/"scripts/research_ming_datong_preyear_leap_civil_year_binding_r1.py")
def _provisional_received_owner(constants:dict[str,Any],label:int)->int|None:
 item=pa.placement(constants,label)
 if not item["has_leap_by_runyu_threshold"]: return None
 return label-1 if item["preyear_branch"] else label
def run(root:Path=ROOT)->dict[str,Any]:
 with localcontext() as decimal_ctx:
  decimal_ctx.prec=50
  oracle=json.loads((root/"docs/research/MING-DATONG-PREYEAR-LEAP-CIVIL-YEAR-ORACLE-R1.json").read_text(encoding="utf-8"))
  ctx=oy.d1._load(root);constants=pa._load_constants(root);profile_controls=[];year_summaries=[]
  for control in oracle["controls"]:
   threshold=int(control["threshold_label_year"]);civil=int(control["civil_year"]);placement=pa.placement(constants,threshold);per=[]
   for profile in oy.d1.PROFILES:
    result=oy._month_sequence(ctx,civil,profile);leaps=result["leap_months"];leap=leaps[0] if len(leaps)==1 else None
    row={"threshold_label_year":threshold,"civil_year":civil,"profile":profile,"expected_leap_month":int(control["expected_leap_month"]),"generated_leap_month":leap,"leap_month_match":leap==int(control["expected_leap_month"]),"assigned_preceding_civil_year_match":placement["assigned_preceding_civil_year"]==civil,"civil_year_start_k":result["civil_year_start_k"],"civil_year_end_k_exclusive":result["civil_year_end_k_exclusive"],"fixed_k2_anchor_used":result["fixed_k2_anchor_used"]}
    profile_controls.append(row);per.append(row)
   year_summaries.append({"threshold_label_year":threshold,"civil_year":civil,"expected_leap_month":int(control["expected_leap_month"]),"source_id":control["source_id"],"all_profiles_match":all(x["leap_month_match"] and x["assigned_preceding_civil_year_match"] for x in per),"civil_year_start_k_values":sorted({x["civil_year_start_k"] for x in per})})
  structural=[];ownership=[];startks={};civil_leaps={}
  for year in range(FIRST_YEAR,LAST_YEAR+1):
   by={p:oy._month_sequence(ctx,year,p) for p in oy.d1.PROFILES}
   sig={p:tuple((x["month"],x["is_leap"]) for x in r["calendar_year"]) for p,r in by.items()}
   if len(set(sig.values()))!=1: structural.append(year)
   full=by[oy.d1.PROFILE_FULL];leaps=full["leap_months"];civil_leaps[str(year)]=leaps[0] if len(leaps)==1 else None;startks[str(year)]=int(full["civil_year_start_k"])
   if year<LAST_YEAR:
    labels=[year,year+1];owners=[label for label in labels if _provisional_received_owner(constants,label)==year]
    if bool(owners)!=bool(leaps): ownership.append({"civil_year":year,"provisional_received_owner_threshold_labels":owners,"generated_leap_months":leaps})
  matched=sum(1 for x in profile_controls if x["leap_month_match"] and x["assigned_preceding_civil_year_match"])
  return {"year_range":[FIRST_YEAR,LAST_YEAR],"year_count":LAST_YEAR-FIRST_YEAR+1,"profile_count":len(oy.d1.PROFILES),"preyear_candidate_year_count":len(oracle["controls"]),"profile_year_control_count":len(profile_controls),"matched_profile_year_controls":matched,"all_preyear_profile_year_controls_match":matched==len(profile_controls),"controls":profile_controls,"year_summaries":year_summaries,"profile_structural_divergence_years":structural,"provisional_received_ownership_mismatches_1368_1643":ownership,"civil_year_start_k_histogram":{str(k):list(startks.values()).count(k) for k in sorted(set(startks.values()))},"candidate_civil_year_start_k_values":sorted({x["civil_year_start_k"] for x in profile_controls}),"fixed_k2_anchor_used":any(x["fixed_k2_anchor_used"] for x in profile_controls),"civil_leap_month_by_year":civil_leaps,"terminal_year_1644_formula_ownership_comparison_excluded":True,"terminal_year_note":"1644 month structure is generated/profile-compared; owner comparison avoids importing post-Ming 1645 threshold label across the regime boundary."}
def main()->int:
 print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())

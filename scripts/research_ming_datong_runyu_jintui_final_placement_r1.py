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
oy=_load("ming_datong_multi_year_pc",ROOT/"scripts/research_ming_datong_multi_year_leap_validation_r1.py")
pa=_load("ming_datong_preyear_pc",ROOT/"scripts/research_ming_datong_preyear_leap_civil_year_binding_r1.py")
def _leap_month(result:dict[str,Any])->int|None:
 leaps=result["leap_months"]
 if len(leaps)>1: raise AssertionError("civil year produced multiple intercalary months")
 return int(leaps[0]) if leaps else None
def _owner_for_threshold(ctx:dict[str,Any],constants:dict[str,Any],label:int,profile:str)->dict[str,Any]:
 placement=pa.placement(constants,label)
 if not placement["has_leap_by_runyu_threshold"]:
  return {"threshold_label_year":label,"owner_civil_year":None,"leap_month":None,"candidate_hits":[]}
 hits=[]
 for civil in (label-1,label):
  result=oy._month_sequence(ctx,civil,profile)
  leap=_leap_month(result)
  if leap is not None:hits.append({"civil_year":civil,"leap_month":leap})
 return {"threshold_label_year":label,"owner_civil_year":hits[0]["civil_year"] if len(hits)==1 else None,"leap_month":hits[0]["leap_month"] if len(hits)==1 else None,"candidate_hits":hits}
def run(root:Path=ROOT)->dict[str,Any]:
 with localcontext() as decimal_ctx:
  decimal_ctx.prec=50
  oracle=json.loads((root/"docs/research/MING-DATONG-RUNYU-JINTUI-BOUNDARY-ORACLE-R1.json").read_text(encoding="utf-8"))
  ctx=oy.d1._load(root);constants=pa._load_constants(root)
  controls=[];summaries=[]
  for control in oracle["controls"]:
   label=int(control["threshold_label_year"]);placement=pa.placement(constants,label);per=[]
   for profile in oy.d1.PROFILES:
    owner=_owner_for_threshold(ctx,constants,label,profile)
    row={"threshold_label_year":label,"profile":profile,"placement_quotient_floor":placement["placement_quotient_floor"],"expected_owner_civil_year":int(control["expected_owner_civil_year"]),"generated_owner_civil_year":owner["owner_civil_year"],"expected_leap_month":int(control["expected_leap_month"]),"generated_leap_month":owner["leap_month"],"owner_match":owner["owner_civil_year"]==int(control["expected_owner_civil_year"]),"leap_month_match":owner["leap_month"]==int(control["expected_leap_month"]),"candidate_hits":owner["candidate_hits"]}
    controls.append(row);per.append(row)
   summaries.append({"threshold_label_year":label,"expected_owner_civil_year":int(control["expected_owner_civil_year"]),"expected_leap_month":int(control["expected_leap_month"]),"disposition":control["disposition"],"source_id":control["source_id"],"all_profiles_match":all(x["owner_match"] and x["leap_month_match"] and x["placement_quotient_floor"]==2 for x in per)})
  threshold_labels=[y for y in range(FIRST_YEAR,LAST_YEAR+1) if pa.placement(constants,y)["has_leap_by_runyu_threshold"]]
  full_owner=[];ambiguities=[]
  for label in threshold_labels:
   owner=_owner_for_threshold(ctx,constants,label,oy.d1.PROFILE_FULL)
   full_owner.append(owner)
   if len(owner["candidate_hits"])!=1:ambiguities.append(owner)
  structural=[];civil_mismatches=[]
  for year in range(FIRST_YEAR,LAST_YEAR+1):
   by={p:oy._month_sequence(ctx,year,p) for p in oy.d1.PROFILES}
   sig={p:tuple((x["month"],x["is_leap"]) for x in r["calendar_year"]) for p,r in by.items()}
   if len(set(sig.values()))!=1:structural.append(year)
   if year<LAST_YEAR:
    generated=_leap_month(by[oy.d1.PROFILE_FULL])
    owners=[x["threshold_label_year"] for x in full_owner if x["owner_civil_year"]==year]
    if bool(generated)!=bool(owners):
     civil_mismatches.append({"civil_year":year,"generated_leap_month":generated,"owner_threshold_labels":owners})
  matched=sum(1 for x in controls if x["owner_match"] and x["leap_month_match"] and x["placement_quotient_floor"]==2)
  retreat=[x["threshold_label_year"] for x in oracle["controls"] if x["disposition"]=="RETREAT_TO_PRECEDING_CIVIL_YEAR"]
  stay=[x["threshold_label_year"] for x in oracle["controls"] if x["disposition"]=="STAY_IN_THRESHOLD_LABEL_CIVIL_YEAR"]
  return {"year_range":[FIRST_YEAR,LAST_YEAR],"year_count":LAST_YEAR-FIRST_YEAR+1,"precision_profile_count":len(oy.d1.PROFILES),"runyu_threshold_label_count":len(threshold_labels),"q2_boundary_count":len(oracle["controls"]),"q2_profile_control_count":len(controls),"matched_q2_profile_controls":matched,"all_q2_profile_controls_match":matched==len(controls),"retreat_threshold_labels":retreat,"stay_threshold_labels":stay,"retreat_count":len(retreat),"stay_count":len(stay),"controls":controls,"summaries":summaries,"full_owner_count":sum(1 for x in full_owner if x["owner_civil_year"] is not None),"full_owner_ambiguities":ambiguities,"profile_structural_divergence_years":structural,"final_owner_existence_mismatches_1368_1643":civil_mismatches,"terminal_year_1644_owner_comparison_excluded":True}
def main()->int:
 print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())

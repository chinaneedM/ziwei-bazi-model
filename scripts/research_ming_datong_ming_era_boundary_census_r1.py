from __future__ import annotations
import importlib.util, json
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
def _load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
d1=_load_module("d1_profiles_oz",ROOT/"scripts/research_ming_datong_d1_precision_profile_sensitivity_r1.py")
oy=_load_module("leap_validation_oz",ROOT/"scripts/research_ming_datong_multi_year_leap_validation_r1.py")
DAY=Decimal("10000"); ZHONGQI_STEP=Decimal("304368.75"); LEAP_LIMIT=Decimal("186552.09")
FIRST_YEAR=1368; LAST_YEAR=1644
def _day(v:Decimal)->int:return int(v//DAY)
def _technical_sui(ctx:dict[str,Any],year:int,profile:str,exact_time:bool=False)->dict[str,Any]:
    source=oy._source_context(ctx,year); moons=[oy._new_moon(ctx,year,k,profile) for k in range(18)]; intervals=[]
    for k in range(len(moons)-1):
        start,end=moons[k],moons[k+1]; zq=[]
        for z in range(-2,15):
            event=source["winter"]+Decimal(z)*ZHONGQI_STEP; ed=_day(event)
            inside=(start["source"]<=event<end["source"]) if exact_time else (int(start["day"])<=ed<int(end["day"]))
            if inside:zq.append({"z":z,"source":event,"day":ed})
        intervals.append({"k":k,"start":start,"end":end,"zhongqi":zq})
    i0=next(i for i,r in enumerate(intervals) if any(x["z"]==0 for x in r["zhongqi"]))
    i12=next(i for i,r in enumerate(intervals) if i>i0 and any(x["z"]==12 for x in r["zhongqi"]))
    span=intervals[i0:i12]; count=len(span); has_leap=count==13; month=11; leap_used=False; labeled=[]
    for idx,r in enumerate(span):
        is_leap=False
        if idx==0:month=11
        elif has_leap and not r["zhongqi"] and not leap_used:is_leap=True;leap_used=True
        else:month=1 if month==12 else month+1
        labeled.append({"k":r["k"],"month":month,"is_leap":is_leap,"start_day":int(r["start"]["day"]),"start_source":r["start"]["source"],"zhongqi":[x["z"] for x in r["zhongqi"]]})
    return {"runyu_remainder":source["run"],"runyu_threshold_flag":source["run"]>=LEAP_LIMIT,"month_count":count,"has_intercalary_month":has_leap,"leap_month":next((r["month"] for r in labeled if r["is_leap"]),None),"labeled":labeled,"source":source}
def run(root:Path=ROOT)->dict[str,Any]:
    # Decimal precision is part of this research harness contract.  Never
    # inherit process-global precision from unrelated tests/imports.
    with localcontext() as decimal_ctx:
        decimal_ctx.prec=50
        decimal_ctx.rounding=ROUND_HALF_EVEN
        ctx=d1._load(root); struct=[]; daydiv=[]; tensions=[]; dx=[]; boundaries=[]; pairs=[]
        for year in range(FIRST_YEAR,LAST_YEAR+1):
            bp={p:_technical_sui(ctx,year,p) for p in d1.PROFILES}
            sk={p:json.dumps([(r["month"],r["is_leap"]) for r in v["labeled"]],ensure_ascii=False) for p,v in bp.items()}
            if len(set(sk.values()))!=1:struct.append(year)
            dk={p:tuple((r["k"],r["start_day"]) for r in v["labeled"]) for p,v in bp.items()}
            if len(set(dk.values()))!=1:daydiv.append(year)
            full=bp[d1.PROFILE_FULL]
            if full["runyu_threshold_flag"] is not full["has_intercalary_month"]:
                tensions.append({"year":year,"runyu_remainder":str(full["runyu_remainder"]),"runyu_threshold_flag":full["runyu_threshold_flag"],"sui_month_count":full["month_count"],"sui_has_intercalary_month":full["has_intercalary_month"],"sui_leap_month":full["leap_month"]})
            exact=_technical_sui(ctx,year,d1.PROFILE_FULL,True)
            if full["leap_month"]!=exact["leap_month"]:dx.append({"year":year,"day_level_leap_month":full["leap_month"],"exact_order_counterfactual_leap_month":exact["leap_month"]})
            for r in full["labeled"]:
                rem=r["start_source"]%DAY; margin=min(rem,DAY-rem)
                boundaries.append({"year":year,"k":r["k"],"month":r["month"],"is_leap":r["is_leap"],"margin_source_units":margin,"margin_minutes":margin/DAY*Decimal("1440")})
            source=full["source"]
            for z in range(12):
                event=source["winter"]+Decimal(z)*ZHONGQI_STEP; ed=_day(event)
                for r in full["labeled"]:
                    if r["start_day"]==ed:
                        gap=r["start_source"]-event
                        pairs.append({"year":year,"z":z,"k":r["k"],"month":r["month"],"is_leap":r["is_leap"],"gap_source_units":gap,"gap_hours":gap/DAY*Decimal("24")})
        boundaries.sort(key=lambda r:r["margin_source_units"]);pairs.sort(key=lambda r:abs(r["gap_source_units"]))
        d1596=_technical_sui(ctx,1596,d1.PROFILE_FULL);e1596=_technical_sui(ctx,1596,d1.PROFILE_FULL,True)
        cv=lambda r:{k:(str(v) if isinstance(v,Decimal) else v) for k,v in r.items()}
        return {"year_count":LAST_YEAR-FIRST_YEAR+1,"profile_count":len(d1.PROFILES),"profile_structural_divergence_years":struct,"profile_new_moon_source_day_divergence_years":daydiv,"runyu_vs_true_sui_tensions":tensions,"day_vs_exact_leap_difference_count":len(dx),"day_vs_exact_leap_differences":dx,"closest_new_moon_day_boundaries":[cv(r) for r in boundaries[:20]],"same_day_zhongqi_new_moon_pair_count":len(pairs),"closest_same_day_zhongqi_new_moon_pairs":[cv(r) for r in pairs[:20]],"1596_day_level_leap_month":d1596["leap_month"],"1596_exact_order_counterfactual_leap_month":e1596["leap_month"]}
if __name__=="__main__":print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))

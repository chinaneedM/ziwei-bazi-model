from __future__ import annotations
import json
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
FIRST_YEAR=1368; LAST_YEAR=1644
SHUO_CE=Decimal("295305.93"); YUE_RUN=Decimal("9062.82"); RUN_LIMIT=Decimal("186552.09")
def _load_constants(root:Path)->dict[str,Decimal]:
    replay=json.loads((root/"docs/research/MING-DATONG-1578-D1-SOURCE-REPLAY-R1.json").read_text(encoding="utf-8")); c=replay["source_constants"]
    return {"epoch_year":Decimal(str(c["epoch_year"])),"year_source_units":Decimal(c["year_source_units"]),"run_response_source_units":Decimal(c["run_response_source_units"])}
def runyu_for_year(constants:dict[str,Decimal],year:int)->Decimal:
    distance=Decimal(year)-constants["epoch_year"]; middle=distance*constants["year_source_units"]
    return (middle+constants["run_response_source_units"])%SHUO_CE
def placement(constants:dict[str,Decimal],year:int)->dict[str,Any]:
    runyu=runyu_for_year(constants,year); has_leap=runyu>=RUN_LIMIT; residual=SHUO_CE-runyu; quotient=int(residual//YUE_RUN); preyear=has_leap and quotient<=1
    return {"threshold_label_year":year,"runyu_remainder_source_units":str(runyu),"has_leap_by_runyu_threshold":has_leap,"shuo_minus_runyu_source_units":str(residual),"placement_quotient_floor":quotient,"preyear_branch":preyear,"assigned_preceding_civil_year":year-1 if preyear else None}
def run(root:Path=ROOT)->dict[str,Any]:
    with localcontext() as decimal_ctx:
        decimal_ctx.prec=50; constants=_load_constants(root); rows=[placement(constants,y) for y in range(FIRST_YEAR,LAST_YEAR+1)]; candidates=[r for r in rows if r["preyear_branch"]]; by_year={r["threshold_label_year"]:r for r in rows}
        return {"year_count":LAST_YEAR-FIRST_YEAR+1,"candidate_count":len(candidates),"candidate_threshold_label_years":[r["threshold_label_year"] for r in candidates],"candidate_preceding_civil_years":[r["assigned_preceding_civil_year"] for r in candidates],"tension_controls":{"1385":by_year[1385],"1480":by_year[1480]}}
def main()->int:
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())

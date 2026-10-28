#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13JU-GK5553-THREEWAY-FASCICLE-MATERIAL-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def verify(e,s,l):
 assert e["schema"]=="TIANWEN-13JU-GK5553-THREEWAY-FASCICLE-MATERIAL-R1"
 assert [x["fascicles"] for x in e["sources"]]==[[8,12,26],[8,26,29],[8,26,28]]
 assert e["sources"][1]["material"]=="일부 필사본" and e["sources"][2]["material"]=="木板补写本"
 assert e["sources"][2]["source_2021_print_page_examined"] is False
 a=e["comparison"]
 assert a["common"]==[8,26] and a["disputed"]==[12,28,29]
 assert a["different_material_concepts"] and not a["physical_cover_verified"]
 assert a["digital0029_ancient_fascicle29_proven"] is False
 assert a["ancient_copy_votes"]==a["g893_six_decisions"]==a["algorithm_reopens"]==a["registry_growth"]==a["graph_growth"]==0
 assert a["chart_product"]=="CLOSED"
 f=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13JU ") for x in f) and any(x.startswith("13JT ") for x in f)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert len(f)==l["binding"]["source_focus_count"]
 assert l["binding"]["latest_research_focus_prefix"]==f[-1].split(" ",1)[0]
 i=next(v for v in l["issues"] if v["id"]=="TW-OPEN-0005")
 assert (i["priority"],i["status"])==("P0","OPEN")
 assert P in i["source_refs"] and P.replace(".json",".md") in i["source_refs"]
 assert sum(v.get("revision_id")=="TW-OPEN-0005-13JU-THREEWAY-20261028" for v in i["history"])==1
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return {"status":"PASS","physical_originals_added":0,"g893_target_decisions":0}
if __name__=="__main__":
 print(json.dumps(verify(*load())))

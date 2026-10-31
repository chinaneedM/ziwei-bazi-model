#!/usr/bin/env python3
"""13MX modern bibliography identity and ancient source nonpromotion."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MX-2019-DATONG-FACSIMILE-CROSSWALK-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(e,s,l):
 a=e["source_2019"];b=e["source_2022"];g=e["guards"];q=e["limits"]
 assert e["schema"]=="TIANWEN-13MX-2019-DATONG-FACSIMILE-CROSSWALK-R1"
 assert (a["date"],a["isbn"],a["ncid"])==("2019.12","9787571001780","BC02309303")
 assert (b["date"],b["isbn"],b["ncids"])==("2022.2","9787571012489",["BC18449469","BC18449673"])
 assert a["grade"].startswith("INSTITUTIONAL_SECONDARY_") and a["exact_original_table_page"]=="UNBOUND"
 assert b["sixth_datong_original_page_proven"] is False
 assert q["naaj_sixth_item_impression"]=="OPEN" and q["source_2019_zou_table_page"]=="OPEN"
 assert q["new_original_image"] is False and q["new_historical_physical_copy"] is False and q["new_direct_transmission_edge"] is False
 assert tuple(g[k] for k in ("sources","matrix_rows","matrix_audited","graph_nodes","graph_edges","issues","historical_winners","algorithm_reopens"))==(765,222,222,252,238,11,0,0)
 assert g["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,986,0)
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"] and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert all(x in issue["source_refs"] for x in ("docs/research/TIANWEN-13MX-2019-DATONG-FACSIMILE-CROSSWALK-R1.json","docs/research/TIANWEN-13MX-2019-DATONG-FACSIMILE-CROSSWALK-R1.md"))
 assert any(x.get("revision_id")=="TW-OPEN-0005-13MX-2019-DATONG-20261031" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13MX-2019-DATONG-20261031" for x in l["checkpoint_log"])
 return {"status":"PASS","historical_winners":0}
if __name__=="__main__":print(json.dumps(check(*[json.loads(p.read_text(encoding="utf-8")) for p in (E,S,L)]),ensure_ascii=False))

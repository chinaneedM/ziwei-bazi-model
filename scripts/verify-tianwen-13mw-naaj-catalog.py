#!/usr/bin/env python3
"""13MW: a modern facsimile catalogue is not a physical Ming-original vote."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MW-NAJ-2022-FACSIMILE-CATALOG-SCOPE-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13MW-NAJ-2022-FACSIMILE-CATALOG-SCOPE-R1"
 a=e["catalogues"]
 assert [(x["ncid"],x["volume"]) for x in a]==[("BC18449469","上"),("BC18449673","下")]
 assert all(x["url"]=="https://ci.nii.ac.jp/ncid/"+x["ncid"] and not x["sixth_book_datong_item_proven"] for x in a)
 assert e["set_isbn"]=="9787571012489"
 assert e["academic_crosscheck"]["year"]==2014 and e["academic_crosscheck"]["footnote"]==38 and e["academic_crosscheck"]["printed_page"]==96
 assert tuple(e["date_separation"][k] for k in ("calculation_year","preface_year","photograph_year","reprint_year"))==(1477,1569,2019,2022)
 assert e["date_separation"]["impression_year"]=="UNPROVEN"
 assert e["photographer"]["exact_naj_item_level_page"]=="NOT_FOUND_IN_THIS_REVIEW"
 assert all(e["adjudication"].values())
 g=e["guards"]
 assert (g["registered_sources"],g["matrix_rows"],g["matrix_audited"])==(s["historical_audit"]["external_source_registry_total_unique_count"],s["historical_audit"]["row_count"],s["historical_audit"]["audited_row_count"])==(765,222,222)
 assert (g["graph_nodes"],g["graph_edges"],g["open_issues"])==(252,238,11)
 assert all(g[k]==0 for k in ("new_registered_sources","new_physical_copies","new_historical_g893_winners","new_graph_edges","algorithm_reopens"))
 assert g["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and g["transmission_impact"]=="NONE"
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,985,0)
 assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith("13MW CURRENT ACTION:")
 assert str(E.relative_to(R)) in issue["source_refs"] and str(E.with_suffix(".md").relative_to(R)) in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13MW-NII-2022-CATALOG-20261031" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13MW-NII-2022-CATALOG-20261031" for x in l["checkpoint_log"])
 return {"status":"PASS","NII_catalogues":2,"new_physical_originals":0,"final_numeric_winners":0}
if __name__=="__main__":
 print(json.dumps(check(*[json.loads(p.read_text(encoding="utf-8")) for p in (E,S,L)]),ensure_ascii=False))

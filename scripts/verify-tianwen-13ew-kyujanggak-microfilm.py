#!/usr/bin/env python3
"""13EW microfilm owner and physical-copy non-promotion verifier."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13EW-KYUJANGGAK-MICROFILM-COPY-IDENTITY-BOUNDARY-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(x,s,l):
 assert x["schema"]=="TIANWEN-13EW-KYUJANGGAK-MICROFILM-COPY-IDENTITY-BOUNDARY-R1" and x["issue_id"]=="TW-OPEN-0005"
 g=x["microfilm_groups"]
 assert len(g)==7 and [z["microfilm"] for z in g]==[f"M/F74-102-{i}" for i in range(1,8)]
 assert [z["physical_book_span"] for z in g]==["v.1-11","v.12-23","v.24-36","v.37-47","v.48-60","v.61-76","v.77-85"]
 assert all(z["source_catalog_shelfmark"]=="奎 3539" and z["work_juan_52_bound"] is False and z["cross_bind_to_GK03579"] is False and z["original_target_folio_sha256"] is None for z in g)
 assert [y["book_cd"] for y in x["official_records"]]==["GK03539_00","GK03579_00"]
 assert all(y["edition_catalog_year"]==1613 and y["book_count"]==85 and y["work_juan_count"]==139 for y in x["official_records"])
 assert x["same_seven_3539_labelled_microfilm_lines_displayed_under_both_catalog_entries"] is True
 assert x["catalog_3539_microfilm_automatically_proves_3579_scan"] is False and x["physical_volume_order_equals_work_juan_order"] is False
 assert x["work_juan_52_exact_physical_book"] is x["source_3539_volume52_target_page_sha256"] is x["source_3579_volume52_target_page_sha256"] is None
 assert x["inherited_original_ncl_p74_d5"]=="四分〇一七二" and x["inherited_secondary_krdb_d5"]=="四分五一七二"
 assert x["G893_six_original_controls"]=="OPEN" and x["old_13EI_false_attribution"]=="RETRACTED"
 assert x["source_original_glyph_readings_added"]==0 and x["transmission_impact"]["edges_supported"]==[]
 im=x["impact"]
 assert all(im[k]==0 for k in ["new_external_registry_entries","new_matrix_rows","new_original_glyph_votes","new_original_target_folios","new_genealogy_nodes","new_genealogy_edges","risk_closures","algorithm_reopens"])
 assert (im["product"],im["open_or_blocked_issues"],im["registry_sources"],im["genealogy_nodes"],im["genealogy_edges"],im["matrix_rows"])==("CLOSED",11,757,252,238,222)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert s["historical_audit"]["current_focus"][-1].startswith("13EW ") and l["binding"]["latest_research_focus_prefix"]=="13EW"
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and {P,P.replace(".json",".md")}.issubset(issue["source_refs"])
 assert issue["next_action"].startswith("13EW CURRENT ACTION:")
 assert all(z in issue["next_action"] for z in ("GK03539_00","GK03579_00","GK03269_00","D1","D2","D3","D4","D5","D6","四分","初度","G893","NULL","13EI"))
 assert any(q.get("revision_id")=="TW-OPEN-0005-13EW-3539-3579-MF-BOUNDARY-20261024" for q in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]=="1.800.0" and len(l["issues"])==11
 return True
if __name__=="__main__":
 assert check(load(P),load(S),load(L))
 print("13EW_PASS_MICROFILM_CATALOG_OWNER_NOT_A_SOURCE_ORIGINAL_GLYPH")

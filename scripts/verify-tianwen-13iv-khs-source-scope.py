#!/usr/bin/env python3
"""13IV source-scope and forward-only active-state strict gate."""
import json
from pathlib import Path
# Historical source text is validated through immutable issue revisions.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13IV-KHS-OFFICIAL-DESCRIPTION-XML-1482-SCOPE-R1.json"
def load(p=P):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,s=None,l=None):
 assert e["schema"]=="TIANWEN-13IV-KHS-OFFICIAL-DESCRIPTION-XML-1482-SCOPE-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["predecessor"]["prior_retraction"]=="13IO_RETRACTED_UNBOUND"
 a=e["official_api"]
 assert a["documented_required"]==["ccbaKdcd","ccbaAsno","ccbaCtcd"] and a["documented_response"]=="XML"
 assert a["documentation_confirmed"] and not a["returned_official_long_text_confirmed"]
 assert a["https_probe_result_at_document_write"]=="NOT_YET_EXECUTED"
 assert a["target_code_variants"]==["21140200","0021140000200"] and a["target_category"]=="12" and a["target_locality"]=="11"
 assert a["no_identifier_enumeration"] and a["https_only_no_downgrade"]
 assert e["hypothesis_fence"]["government_label_not_copy_specific_proof"] and e["hypothesis_fence"]["snu_conjecture_not_government_error_proof"]
 assert e["hypothesis_fence"]["physical_copy_impression_year"]=="UNBOUND"
 assert "추측될 뿐이다" in e["sources"][0]["quoted_phrase"]
 q=e["pending"]
 assert q["gk5553_book29_to_juan81_83"]=="RETRACTED_UNBOUND" and q["older_13EI"]=="RETRACTED"
 assert all(q[k] is None for k in ("official_2114_2_korean_long_description","verified_copy_specific_5554_image","g893_six_original_numbers","gk3467_winter_D1_D7","nlc03130_solar_D30","nlc03130_summer_D14","d5_zero_five_glyph","fourfen_to_chudu_bridge"))
 assert e["counts"]=={"matrix":[222,222],"sources":761,"genealogy":[252,238],"issues":11,"chart":"CLOSED","algorithm_reopen":0,"new_ancient_originals":0,"new_numerical_winners":0,"new_lineage_edges":0}
 assert e["transmission_impact"]["edges_supported"]==[]
 s=load("docs/PROJECT-CURRENT-STATE-R1.json") if s is None else s
 l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json") if l is None else l
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,901,0)
 f=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13IV ") for x in f) and len(f)==l["binding"]["source_focus_count"] and f[-1].split(" ",1)[0]==l["binding"]["latest_research_focus_prefix"]
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and P in issue["source_refs"]
 assert all(t in historical_action_view(issue) for t in ("D1-D6","四分","初度","G893","NLC03130 solar D30","NLC03130 summer D14","GK03539_00","GK03579_00","GK03269_00","NULL","13EI","RETRACTED"))
 assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13IV-") and P in x.get("evidence_refs",[]) for x in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(load())
 print("TIANWEN_13IV_KHS_API_HISTORICAL_SCOPE_PASS")

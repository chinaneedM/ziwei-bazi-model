#!/usr/bin/env python3
"""13GF: official NCL access policy is not an original folio or historical glyph."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13GF-NCL03130-HIGHRES-ACCESS-GATE-R1.json";S=R/"docs/PROJECT-CURRENT-STATE-R1.json";L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
GD=R/"docs/research/TIANWEN-13GD-NLC-P74-P75-D10-D15-BOUNDED-ORIGINAL-LANES-R1.json"
GE=R/"docs/research/TIANWEN-13GE-NLC416-1909-P152-D29-D31-DIRECT-FOURFEN-R1.json"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def check(e,s,l,gd,ge):
 assert e["schema"]=="TIANWEN-13GF-NCL03130-HIGHRES-ACCESS-GATE-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="OFFICIAL_CURRENT_SERVICE_POLICY_NOT_TARGET_ORIGINAL_IMAGE"
 assert [x["url"] for x in e["official_policy"]]==["https://rbook.ncl.edu.tw/NCLSearch/Search/Index/8","https://rbook.ncl.edu.tw/NCLSearch/Search/Index/9"]
 assert e["official_policy"][0]["specific_target_approved"] is False and e["official_policy"][1]["republication_license"] is None
 c=e["catalog_description"];assert c["firstparty_physical_item_id"] is None and c["source_specific_folio_id"] is None and c["early_qing_versus_guangxu_leaf"] is None
 a=e["access"];assert a["research_copy_and_public_image_license_are_distinct"] is True
 assert all(a[k] is False for k in ("applicant_identified","submitted","approved","paid","downloaded","public_image_reuse_approved","high_res_image_existence_verified"))
 assert e["surrogate"]["pdf_sha256"]==gd["source"]["pdf_sha256"]
 assert e["surrogate"]["p74_sha256"]==gd["source"]["original_page_images"][0]["png_sha256"]
 assert e["surrogate"]["p76_sha256"]=="ce4eb8b044868fe48bb41fe5453b10fa7bbd949d8fdf2c8e31037f8b89f32fad"
 t=e["targets"];assert [x["day"] for x in t]==[9,14,30,5] and [x["pdf_page"] for x in t]==[74,74,76,74]
 assert [x["old_printed_value"] for x in t[:3]]==[None,None,None] and t[2]["old_candidate_roi"] is None
 assert t[0]["old_candidate_roi"]==gd["non_adjudicated_original_scopes"][0]["candidate_roi_xyxy"]
 assert t[1]["old_candidate_roi"]==gd["non_adjudicated_original_scopes"][1]["candidate_roi_xyxy"]
 u=e["unresolved"];assert u["old_d9"] is None and u["old_d14"] is None and u["old_d30"] is None
 assert u["later_1909_d30"]=="四分九二二二" and ge["unresolved"]["NLC_03130_original_d30"] is None
 assert u["historical_fourfen_unit"] is None and u["g893_direct_six"]=="OPEN" and u["historical_winner"] is None and u["legacy_13EI"]=="RETRACTED"
 assert e["counts"]=={"matrix_rows":222,"matrix_audited":222,"sources":761,"graph_nodes":252,"graph_edges":238,"risk_issues_open_or_blocked":11,"product":"CLOSED","algorithm_reopens":0,"candidate_collapses":0,"new_source_registry_entries":0,"new_ancient_physical_witnesses":0,"new_genealogy_nodes":0,"new_genealogy_edges":0}
 assert not e["transmission_impact"]["edges_supported"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,s["schema_version"].split(".")))>=(1,835,0)
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and any(x.startswith("13GF ") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and (issue["next_action"].startswith("13GF CURRENT ACTION:") or "ARCHIVED 13GF PRIOR ACTION" in issue["next_action"])
 assert str(E.relative_to(R)) in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13GF-NCL-HIGHRES-POLICY-20261025" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13GF-NCL-HIGHRES-POLICY-20261025" for x in l["checkpoint_log"])
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L),load(GD),load(GE))
 print("13GF_PASS_NCL_POLICY_NO_ORIGINAL_GLYPH_PROMOTION")

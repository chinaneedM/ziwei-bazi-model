#!/usr/bin/env python3
"""13GG: NCL onsite application form does not prove a digital-image order or glyph."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13GG-NCL-RESEARCH-FORM-VS-IMAGE-COPY-SCOPE-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
GF=R/"docs/research/TIANWEN-13GF-NCL03130-HIGHRES-ACCESS-GATE-R1.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def check(e,s,l,gf):
 assert e["schema"]=="TIANWEN-13GG-NCL-RESEARCH-FORM-VS-IMAGE-COPY-SCOPE-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 o=e["official_page"]
 assert o["policy_and_form"]=="https://rbook.ncl.edu.tw/NCLSearch/Search/Index/8"
 assert o["in_person_acknowledgement_visible"] is True
 assert o["visible_form_scope"]=="ON_SITE_RARE_BOOK_READING_APPLICATION_NOT_PROVEN_DIGITAL_IMAGE_ONLY_ORDER"
 assert o["library_public_contact"]=="rbook@ncl.edu.tw"
 assert {"applicant_name","reading_card_or_national_id_or_passport_number","email","telephone","research_purpose"}.issubset(o["fields_visible"])
 a=e["original_replay"]
 assert a["actions_artifact_id"]==gf["surrogate"]["prior_artifact"]==12494518841
 assert a["p74"]["sha256"]==gf["surrogate"]["p74_sha256"] and a["p74"]["target_originals"]==[None,None]
 assert a["p76"]["sha256"]==gf["surrogate"]["p76_sha256"] and a["p76"]["target_originals"]==[None]
 assert (a["p74"]["width"],a["p74"]["height"],a["p76"]["width"],a["p76"]["height"])==(1305,873,1305,875)
 assert a["new_original_images_obtained"]==a["new_direct_historical_glyph_readings"]==0
 r=e["request_channel"]
 assert r["library_contact_required_before_submission"] is True
 for k in ("applicant_identity_supplied","physical_copy_and_folio_crosswalk_confirmed","remote_digital_copy_form_confirmed","request_submitted","payment_made","target_approved","higher_resolution_image_received","reuse_license_granted"):
  assert r[k] is False,k
 h=e["historical_boundaries"]
 assert [h[k] for k in ("old_copy_day9","old_copy_day14","old_copy_day30","old_fourfen_unit_bridge","historical_winner")]==[None]*5
 assert h["other_later_1909_print_day30"]=="四分九二二二" and h["legacy_13EI"]=="RETRACTED"
 assert (h["confirmed_chart_algorithm_defects"],h["algorithm_reopens"],h["candidate_collapses"])==(0,0,0)
 assert e["counts"]=={"matrix_rows":222,"matrix_audited":222,"sources":761,"genealogy_nodes":252,"genealogy_edges":238,"open_or_blocked_risks":11,"new_registry_entries":0,"new_historical_physical_witnesses":0}
 assert not e["transmission_impact"]["edges_supported"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,836,0)
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert "docs/research/TIANWEN-13GG-NCL-RESEARCH-FORM-VS-IMAGE-COPY-SCOPE-R1.json" in issue["source_refs"] and "docs/research/TIANWEN-13GG-NCL-RESEARCH-FORM-VS-IMAGE-COPY-SCOPE-R1.md" in issue["source_refs"]
 assert any(z.get("revision_id")=="TW-OPEN-0005-13GG-NCL-FORM-SCOPE-20261025" for z in issue["history"])
 assert any(z.get("id")=="OMISSIONS-13GG-NCL-FORM-SCOPE-20261025" for z in l["checkpoint_log"])
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L),load(GF))
 print("13GG_PASS_FORM_SCOPE_ARCHIVE_DIGEST_AND_NULL_TARGETS")

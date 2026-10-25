#!/usr/bin/env python3
"""13HF: access policy does not imply source-specific high-res image or reuse rights."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "docs/research/TIANWEN-13HF-NCL03130-FIRSTPARTY-HIGHRES-SERVICE-AND-RIGHTS-SCOPE-R1.json"
def blob_sha(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
def check(e, root=ROOT):
    assert e["schema"] == "TIANWEN-13HF-NCL03130-FIRSTPARTY-HIGHRES-SERVICE-AND-RIGHTS-SCOPE-R1"
    assert e["issue_id"] == "TW-OPEN-0005"
    assert e["authority_grade"].startswith("INSTITUTIONAL_SERVICE_RULE")
    for prior in e["previous_evidence"]:
        assert blob_sha(root / prior["path"]) == prior["git_blob_sha"]
    official = e["firstparty"]
    assert official["research_reading_url"].endswith("/Search/Index/8")
    assert official["reproduction_authorization_url"].endswith("/Search/Index/9")
    research = official["reading_scope"]
    assert research["original_inspection_requires_approval"]
    assert not research["research_high_resolution_approval_granted"]
    assert not research["original_reading_approval_granted"]
    assert research["applies_to_NCL_03130_individually"] is None
    assert not research["onsite_original_photography_permitted"]
    licensing = official["licensing_scope"]
    assert licensing["separate_formal_authorization_process"]
    assert set(licensing["print_grade_formats"]) == {"300dpi JPEG","300dpi TIFF"}
    assert licensing["public_information_format"] == "72dpi JPEG"
    assert licensing["max_image_count_for_same_purpose_on_policy_page"] == 30
    assert not licensing["formal_request_submitted"] and not licensing["authorization_granted"]
    assert licensing["image_available_for_item_03130_in_format"] is None
    assert licensing["quote_or_fee_for_target_item"] is None
    assert not licensing["commercial_or_rehosting_permission_granted"]
    assert official["site_image_rights_notice"].startswith("CC BY-NC-ND 3.0 Taiwan")
    assert "public domain" in official["commons_rights_notice"].lower()
    assert not official["notices_are_a_copy_specific_legal_resolution"]
    assert official["one_host_tag_does_not_override_other_host_policy"]
    t=e["target"]
    for key in ("original_physical_folio","provider_native_item_detail","official_high_resolution_image","original_vs_guangxu_supplement_status","NCL_original_full_D14_literal","NCL_original_D14_terminal","NCL_ancient_unit","fourfen_chudu_equivalence"):
        assert t[key] is None,key
    assert t["NIKH_photo4_summer_D14"] == "四分六六三〇"
    assert t["NIKH_value_only_attests_that_photo"] and t["old_D5"] == "〇/五_UNRESOLVED"
    assert t["G893_six"] == "OPEN" and t["prior_13EI"] == "RETRACTED"
    guard=e["epistemic_guard"]
    for key in ("official_service_page_is_not_item_record","application_rule_is_not_an_approved_application","public_web_licensed_view_is_not_a_physical_original_glyph","commons_license_label_is_not_NCL_item_reproduction_grant","no_guess_of_item_link_image_endpoint_or_folio","no_scraping_of_unauthorized_hires","no_request_or_application_was_submitted"):
        assert guard[key],key
    for key in ("direct_original_new_witnesses","new_glyph_adjudications","new_transmission_edges"):
        assert guard[key] == 0,key
    assert e["transmission_impact"] == "NONE"
    assert e["invariants"] == {"matrix":[222,222],"sources":761,"genealogy":[252,238],"open_issues":11,"chart":"CLOSED","algorithm_reopens":0,"candidate_collapses":0}
    state=json.loads((root/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
    ledger=json.loads((root/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
    assert state["schema_version"] == ledger["binding"]["reviewed_state_version"]
    assert any(str(s).startswith("13HF ") for s in state["historical_audit"]["current_focus"])
    assert len(state["historical_audit"]["current_focus"]) == ledger["binding"]["source_focus_count"]
    issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
    assert str(E.relative_to(root)) in issue["source_refs"]
    assert state["invariants"]["deterministic_fusion_chart_product_r1"] == "CLOSED"
    return True
if __name__ == "__main__":
    print("TIANWEN_13HF_NCL03130_ACCESS_RIGHTS_PASS" if check(json.loads(E.read_text(encoding="utf8"))) else "FAIL")

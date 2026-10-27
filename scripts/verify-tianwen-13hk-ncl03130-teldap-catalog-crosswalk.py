#!/usr/bin/env python3
"""13HK: TELDAP 549927 NCL03130 holding metadata is not direct native glyph or folio evidence."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HK-NCL03130-TELDAP-ITEM549927-CATALOG-COPY-DATE-CROSSWALK-R1.json"
def gitblob(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def check(e,root=ROOT,*,ledger=None):
    assert e["schema"]=="TIANWEN-13HK-NCL03130-TELDAP-ITEM549927-CATALOG-COPY-DATE-CROSSWALK-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    c=e["institutional_catalog"]
    assert c["url"]=="https://catalog.digitalarchives.tw/item/00/08/64/27.html"
    assert c["unique_catalog_aggregation_item_id"]=="549927"
    assert c["directly_followed_link_final_url"]=="https://rbook.ncl.edu.tw/NCLSearch/Search/Index/1"
    assert c["final_url_is_generic_search_page"] and c["original_catalog_system_record_not_recovered"]
    assert not c["provider_native_exact_item_record_obtained"] and not c["provider_native_folio_page_obtained"]
    meta=e["catalog_literal_fields"]
    assert meta["資料識別"]=="書號:03130" and meta["資料類型"]=="善本書-原件"
    assert meta["格式_數量"]=="40冊" and meta["日期_製作時間"]=="1644-1735"
    assert "光緒間(1644-1735)" in meta["描述_版本"]
    chrono=e["chronology_disambiguation"]
    for k in ("metadata_has_mixed_layers","1644-1735_range_is_early_qing_scope_not_full_composite_leaf_date","guangxu_supplement_different_from_1644_1735_range","catalog_does_not_attribute_specific_juan_to_supplement","catalog_production_field_does_not_date_juan52_p74_ink"):
        assert chrono[k],k
    for k in ("work_composition_date","edition_impression_date","physical_copy_item_specific_folio_date","digital_surrogate_date","juan52_old_or_supplemented_copy_layer"):
        assert chrono[k] is None,k
    dedup=e["deduplication"]
    assert dedup["same_catalog_shelfmark"]=="03130" and dedup["same_physically_reported_booklets"]==40
    assert dedup["does_not_create_an_independent_physical_copy"] and dedup["digital_file_count_is_not_physical_volume_count"]
    for prior in e["provenance_bound_predecessors"]:
        assert gitblob(root/prior["path"])==prior["git_blob_sha"],prior["path"]
    t=e["unresolved_original"]
    for k in ("national_library_native_d14_complete_literal","national_library_native_d14_terminal","physical_leaf_identifier","original_ink_date","source_original_higher_resolution","四分_初度_equivalence","ancient_unit"):
        assert t[k] is None,k
    assert t["NIKH_original_photo4_D14"]=="四分六六三〇" and t["do_not_transfer_NIKH_literal_into_NCL"]
    assert t["old_day5_〇_五"]==t["G893_six"]=="OPEN" and t["13EI"]=="RETRACTED"
    effects=e["evidence_effect"]
    for k in ("new_registry_entries","new_physical_witnesses","new_target_original_glyphs","new_genealogy_nodes","new_genealogy_edges","new_algorithms"):
        assert effects[k]==0,k
    assert e["invariants"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"open_issues":11,"chart":"CLOSED","algorithm_reopens":0,"candidate_collapses":0}
    assert e["transmission_impact"]=="NONE"
    s=json.loads((root/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
    l=ledger if ledger is not None else json.loads((root/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]
    assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
    assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
    assert any(x.startswith("13HK ") for x in s["historical_audit"]["current_focus"])
    i=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
    # Historical action transitions live in append-only history; next_action may advance.
    for tag in ('13HK',):
        assert any(
            h.get("event")=="ISSUE_REVISION"
            and h.get("revision_id", "").startswith("TW-OPEN-0005-"+tag+"-")
            and "next_action" in h.get("changed_fields", [])
            and (tag!="13HK" or str(E.relative_to(root)) in h.get("evidence_refs", []))
            for h in i["history"]
        ), tag
    assert i["priority"]=="P0" and i["status"]=="OPEN"
    assert str(E.relative_to(root)) in i["source_refs"] and str(E.relative_to(root)).replace(".json",".md") in i["source_refs"]
    assert any(h.get("event")=="ISSUE_REVISION" and h.get("revision_id","").startswith("TW-OPEN-0005-13HK-") and "next_action" in h.get("changed_fields",[]) for h in i["history"])
    return True
if __name__=="__main__":
    print("TIANWEN_13HK_NCL03130_INSTITUTIONAL_CATALOG_SCOPE_PASS" if check(json.loads(E.read_text(encoding="utf8"))) else "FAIL")

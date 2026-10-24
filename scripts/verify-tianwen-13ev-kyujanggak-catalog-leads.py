#!/usr/bin/env python3
"""13EV Kyujanggak three physical holding catalogue locators; never infer actual glyph."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13EV-KYUJANGGAK-GORYEOSA-THREE-OBJECT-CATALOG-LEADS-R1.json";S="docs/research/TIANWEN-13EV-KYUJANGGAK-GORYEOSA-THREE-OBJECT-CATALOG-LEADS-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json";C="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(x,sh,m,c,l):
    assert x["schema"]=="TIANWEN-13EV-KYUJANGGAK-GORYEOSA-THREE-OBJECT-CATALOG-LEADS-R1" and x["issue_id"]=="TW-OPEN-0005"
    a=x["catalog_objects"]
    assert len(a)==3 and [z["book_cd"] for z in a]==["GK03539_00","GK03579_00","GK03269_00"]
    assert [z["shelfmark"] for z in a]==["奎貴3539-v.1-85","奎貴3579-v.1-85","奎3269-v.1-101"]
    assert [z["books"] for z in a]==[85,85,101] and all(z["volumes"]==139 and z["print_type"]=="木版本" for z in a)
    assert [z["catalog_impression_date"] for z in a]==["1613","1613",None]
    assert a[0]["same_edition_group"]==a[1]["same_edition_group"]=="1613_KYUJANGGAK_3539_3579" and a[2]["same_edition_group"] is None
    assert [z["repository_subcollection"] for z in a]==["太白山史庫","五臺山史庫",None]
    assert all(z["exact_work_volume_52_leaf_image_sha256"] is None and z["exact_d5_glyph"] is None and z["original_image_target_bound"] is False for z in a)
    f=x["catalog_fact_controls"]
    assert f["catalog_records"]==3 and f["new_original_target_folio_images"]==f["new_original_glyph_readings"]==0
    assert f["date_1451_is_work_compilation_not_attested_3269_print_year"] and f["same_impression_does_not_mean_two_independent_editions"]
    assert f["calendar_juan"]=="卷50–52:曆志" and f["source_1613_microfilm_listing_may_mention_3539_for_3579"]=="DO_NOT_REASSIGN_MICROFILM_BY_GUESS"
    assert len(x["next_original_folio_targets"])==3
    for target,copy in zip(x["next_original_folio_targets"],a):
        assert target["book_cd"]==copy["book_cd"] and target["juan"]==52 and target["days"]==[4,5,6]
        assert target["artifact_sha256"] is target["exact_leaf_number"] is target["exact_book_number"] is None
        assert target["status"]=="NOT_ACQUIRED"
    db=x["official_db"]
    assert db["record_id"]=="kr_052_0010_0010_0020_0020" and db["day5_han_transcription"]=="四分五一七二"
    assert db["page_displays_original_image_ui_entry"] is True and db["actual_image_viewer_target_folio_retrieved"] is False
    assert db["exact_catalog_object_link"]=="UNBOUND" and db["snu_physical_object_associated_with_krdb_viewer"]=="UNPROVEN"
    assert x["prior_study"]["ncl_d5_original_photo_visual"]=="四分〇一七二" and x["prior_study"]["former_13ei_erratum"]=="RETRACTED"
    assert x["barriers"]["book_count_does_not_identify_juan52_fascicle"] is True
    assert x["barriers"]["similar_catalog_or_same_printing_does_not_prove_original_d5_glyph"] is True
    assert x["barriers"]["one_krdb_transcription_not_a_separate_original_witness"] is True
    assert x["barriers"]["other_early_g893_six_targets"]=="OPEN" and x["barriers"]["winter_d16_numerics"] is x["barriers"]["solar_d30_numerics"] is None
    impact=x["impact"]
    assert impact["registered_catalog_sources_added"]==3 and impact["registered_original_glyph_witnesses_added"]==impact["physical_folio_pages_collated"]==0
    assert all(impact[z]==0 for z in ("history_matrix_rows_changed","genealogy_nodes_added","genealogy_edges_added","risks_closed","algorithm_reopens"))
    assert impact["product"]=="CLOSED" and impact["current_open_or_blocked_risks"]==11
    assert impact["extension_manifest_shards_now"]==len(m["shards"])==62
    assert impact["source_registry_combined_now"]==m["combined_source_count"]==757
    assert sh["schema"]=="TIANWEN-13EV-KYUJANGGAK-GORYEOSA-THREE-CATALOG-HOLDING-LOCATORS-SOURCE-SHARD-R1"
    assert len(sh["sources"])==3
    for item,copy in zip(sh["sources"],a):
        assert item["url"]==copy["url"] and item["evidence"]==P
        assert item["physical_glyph_authority"] is False and item["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY"
        assert item["source_id"]=="EXT-TIANWEN-13EV-KYUDB-GORYEOSA-"+copy["book_cd"].replace("_00","")
    assert m["shards"][-1]["path"]==S and m["shards"][-1]["source_count"]==3
    assert m["extension_source_count"]==110 and m["root_source_count"]==647
    assert c["historical_audit"]["external_source_registry_extension_count"]==110 and c["historical_audit"]["external_source_registry_total_unique_count"]==757
    assert c["schema_version"]==l["binding"]["reviewed_state_version"]==c["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert l["binding"]["source_focus_count"]==len(c["historical_audit"]["current_focus"])
    assert l["binding"]["latest_research_focus_prefix"]==c["historical_audit"]["current_focus"][-1].split(" ",1)[0]
    assert any(f.startswith("13EV ") for f in c["historical_audit"]["current_focus"])
    issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
    assert issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
    assert all(z in issue["next_action"] for z in ("D1","D2","D3","D4","D5","D6","四分","初度","G893","NULL","13EI","GK03539_00","GK03579_00","GK03269_00"))
    assert {P,P.replace(".json",".md"),S}.issubset(set(issue["source_refs"]))
    assert next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-13EV-KYUDB-THREE-HOLDING-CATALOG-20261024")["previous_next_action"].startswith("13EU CURRENT ACTION:")
    assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==c["schema_version"]
    return True
if __name__=="__main__":
    assert check(load(P),load(S),load(M),load(C),load(L))
    print("13EV_PASS_THREE_INSTITUTIONAL_HOLDING_LOCATORS_ZERO_ORIGINAL_GLYPH_VOTES")

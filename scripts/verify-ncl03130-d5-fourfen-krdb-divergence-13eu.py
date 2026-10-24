#!/usr/bin/env python3
"""13EU: preserve NCL original D5 〇 versus KRDB textual 五, NO historical variant inference."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13EU-NCL03130-P74-D5-FOURFEN-KRDB-TRANSCRIPTION-DIVERGENCE-R1.json";EN="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json";ET="docs/research/TIANWEN-13ET-NCL03130-SIX-DAY-SOURCE-PIXEL-INTERSECTIONS-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def verify(v,en,et,s,l):
    assert v["schema"]=="TIANWEN-13EU-NCL03130-P74-D5-FOURFEN-KRDB-TRANSCRIPTION-DIVERGENCE-R1" and v["issue_id"]=="TW-OPEN-0005"
    n,k,a=v["ncl_original"],v["krdb_original_text"],v["alignment_candidate"]
    assert n["pdf_page"]==74 and n["image_file"]=="original-p074.png"
    assert n["original_png_sha256"]==et["source"]["original_pages"][1]["png_sha256"]
    assert n["original_rgb_sha256"]==et["source"]["original_pages"][1]["rgb_sha256"]
    assert n["image_dimensions"]==et["source"]["original_pages"][1]["image_size"]
    assert n["archived_action_run"]==et["source"]["archive_run"] and n["archive_artifact_id"]==et["source"]["artifact_id"]
    z=next(x for x in en["rois"] if x["name"]=="D5_FOURFEN_PREFIX")
    assert n["source_roi"]=={"bbox":z["bbox"],"rgb_sha256":z["rgb_sha256"]}
    assert n["previous_image_reading"]==en["findings"]["fourfen_d5_clear_prefix"]=="四分〇一七二"
    assert n["positive_d5_digit_roi"]=={"bbox":[835,480,855,516],"rgb_sha256":"73bdb68cc2145cad5f79af4ab65b98709e414e52a6f457b425b1289c4b390914","literal_visual_shape":"〇","grade":"DIRECT_PHOTOGRAPH_PIXEL_BOUNDED_SINGLE_CHARACTER_VISIBLE"}
    assert n["transcription_not_retroactively_edited"] is True and n["physical_copy_identity"]==n["impression_date"]=="UNBOUND"
    assert k["source_registry_id"]=="EXT-KRDB-GORYEOSA-V52-SHOUSHI-LICHENG"
    assert k["url"]=="https://db.history.go.kr/id/kr_052_0010_0010_0020_0020" and k["record_id"]=="kr_052_0010_0010_0020_0020"
    assert k["column_label"]=="日差加一秒六十二少"
    assert k["adjacent_daily_original_text_transcriptions"]==[{"day":4,"original_transcription":"四分五〇一〇"},{"day":5,"original_transcription":"四分五一七二"},{"day":6,"original_transcription":"四分五三三四"}]
    assert k["image_viewer_source_copy_identity"]=="NOT_BOUND_TO_NCL_COPY" and k["same_edition_or_direct_copy"]=="UNPROVEN"
    assert "NOT_INDEPENDENT_PHYSICAL_COPY" in k["page_type"]
    assert a["source_roi_literal"]==n["previous_image_reading"]=="四分〇一七二"
    assert a["krdb_text_literal"]=="四分五一七二" and a["day"]==5 and a["unmatched_slot_index_1_based"]==3
    assert a["source_slot_literal"]=="〇" and a["database_slot_literal"]=="五"
    assert a["source_roi_literal"][:2]==a["krdb_text_literal"][:2] and a["source_roi_literal"][3:]==a["krdb_text_literal"][3:]
    assert a["other_recorded_slots_match"] is True and a["apparent_single_slot_conflict"] is True
    assert a["confirmed_historical_edition_variant"] is a["confirmed_krdb_transcription_error"] is a["confirmed_copyist_error"] is False
    assert a["normalized_digit_for_algorithm"] is None and "NOT_HISTORICAL_NUMERIC" in a["image_visual_reading_scope"]
    u=v["limits"]
    assert all(u[t] is True for t in ("samescan_one_witness_only","krdb_o_not_second_original_witness","wikipedia_wikisource_ctext_not_independent_edition_witness","ncl_d5_visual_ellipse_is_not_zero_fixed_point_value"))
    assert u["source_field_identity_to_ncl_unruled_columns"]=="CANDIDATE_ONLY"
    assert u["g893_six_controls"]=="OPEN" and u["winter_d16_original_historic_numeric"] is u["solar_d30_historic_numeric"] is None
    assert u["qing_vs_1905_physical_hands"]=="UNBOUND" and u["retired_13ei_claim"]=="RETRACTED" and u["retired_claim_restored"] is False
    x=v["impact"]
    assert all(x[t]==0 for t in ("new_verified_source_edition","registry_sources_added","matrix_rows_changed","genealogy_nodes_added","genealogy_edges_added","risks_closed","algorithm_reopened"))
    assert x["open_or_blocked_risks"]==11 and x["chart"]=="CLOSED"
    assert [z["path"] for z in v["source_ancestors"]]==[EN,ET]
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
    assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
    assert any(z.startswith("13EU ") for z in s["historical_audit"]["current_focus"])
    issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
    assert issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
    assert all(z in issue["next_action"] for z in ("四分〇一七二","四分五一七二","D5","G893","NULL","13EI"))
    assert {P,P.replace(".json",".md")}.issubset(set(issue["source_refs"]))
    assert next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-13EU-D5-FOURFEN-DIVERGENCE-20261024")["previous_next_action"].startswith("13ET CURRENT ACTION:")
    assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["issues"])==11
    return True
def replay(v,folder):
    from PIL import Image
    n=v["ncl_original"]; p=Path(folder)/n["image_file"]
    assert hashlib.sha256(p.read_bytes()).hexdigest()==n["original_png_sha256"]
    with Image.open(p) as im: rgb=im.convert("RGB")
    assert list(rgb.size)==n["image_dimensions"] and hashlib.sha256(rgb.tobytes()).hexdigest()==n["original_rgb_sha256"]
    for roi in ("source_roi","positive_d5_digit_roi"):
        z=n[roi];assert hashlib.sha256(rgb.crop(tuple(z["bbox"])).tobytes()).hexdigest()==z["rgb_sha256"]
    return True
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--source-dir");a=p.parse_args()
    v=load(P);assert verify(v,load(EN),load(ET),load(S),load(L))
    if a.source_dir:assert replay(v,a.source_dir)
    print("13EU_PASS_NCL_P74_D5_CIRCULAR_GLYPH_KRDB_TRANSCRIPTION_UNRESOLVED")

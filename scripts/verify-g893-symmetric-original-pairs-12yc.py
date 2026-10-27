#!/usr/bin/env python3
"""12YC verified-original four-source-row pair equality; CI validates sealed evidence, not image viewing."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YC-G893-L8-L159-L35-L132-ORIGINAL-PAIR-GLYPH-COLLATION-R1.json"
PAGES={"018b":"4decd1801d832ba5b471b047dd84cca487245038622a589b48552a0fb43ab83a","019b":"05d6a658664475540333965079363e476c58f708819636f5137558b05a35bcda","023b":"f5f732a4db9636ab563af47a5c8332e1f00eed1e587cc138d150da53f557d94f","036b":"8acb0c32bcdd0be8827bc2851f089bf5d73a2378c3b7ffcfa80eeaf725d1dd84","040a":"ba5cb6bcc8ec21ce59b6a33c402cd6ee661f1466239649eaa8c661d80c63143a"}
ROIS={"ORIGINAL_CHIJI_LOSSGAIN_HEADER":"143639e6dc2fed98c61a9d4f3197276869d58e8f50e339b7529be309b93d3cf5","L8_COMPLETE_ORIGINAL_LOSSGAIN_COLUMN":"2189fbc2c721cbb1c27019050c8cfeda7314175bdfed173629dddd72707c7596","L35_COMPLETE_ORIGINAL_LOSSGAIN_COLUMN":"88fd0c52b7f45ac0f1d995cdc249bf540c192994cc1fe26cfa1cbdc2ee40bfad","L132_COMPLETE_ORIGINAL_LOSSGAIN_COLUMN":"6af672e0132d9bffde4f6f7c5e62f29fc5cee6de87d99566349e3543e499dbbe","L159_COMPLETE_ORIGINAL_LOSSGAIN_COLUMN":"4835b3d4bb9919f4c3d9e40c828487b1682f14ac6dec690109c5650ef1c475ac","L8_DAY_HEADING":"dbccc60b064dd6a82d687d4fd00a6a666ae4a7015341b7a1b3c107434384319b","L35_DAY_HEADING":"f4db9d6d1c312253dff9b90f70475170801f0fdabf667130f1fb5a203dda1792","L132_DAY_HEADING":"92ecc60db8c8d070c4d9b5b337e70a0ef2d0d12e98080e5b1a2575e68e68b55c","L159_DAY_HEADING":"fc823fb481e5edf844c63704dae979183a96943e5c4ee5623596e205dcaedc6c"}
def need(ok,why):
    if not ok: raise ValueError(why)
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/research/TIANWEN-12XU-G893-L8-L132-SOURCE-GLYPH-AND-SYMMETRIC-LOCATORS-R1.json","docs/research/TIANWEN-12YB-G893-L35-L159-SAME-COPY-LOSSGAIN-POLARITY-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,xu,yb,ledger,state):
    need(d["schema"]=="TIANWEN-12YC-G893-SAME-ORIGINAL-LOSSGAIN-FOUR-ROW-GLYPH-EQUALITY-R1" and d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","original source or schema")
    z=d["archive"]
    need(z["byte_count"]==33525981 and z["zip_sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and z["zip_crc_verified"] is True and z["original_jpeg_sha256_replay_pass"]==z["original_jpeg_count"]==204 and z["original_jpeg_dimensions"]==[1150,2000] and z["images_committed"]==0,"single source original archive")
    need(len(d["original_page_evidence"])==5 and {x["page_id"]:x["jpeg_sha256"] for x in d["original_page_evidence"]}==PAGES,"five exact provider original page digests")
    rois=d["original_rgb_roi"]
    need(rois["ocr"] is False and len(rois["regions"])==9 and {x["role"]:x["sha256"] for x in rois["regions"]}==ROIS,"original pixel region digests")
    for x in rois["regions"]:
        l,t,r,b=x["rect_px"]
        need(x["page_id"] in PAGES and all(type(a) is int for a in (l,t,r,b)) and 0<=l<r<=1150 and 0<=t<b<=2000,"original pixel rectangle")
    c=d["direct_original_collation"];rows=c["rows"]
    need(c["source_header"]=={"page_id":"018b","literal":"遲疾損益分"} and len(rows)==4,"original lunar header and four row scope")
    expected=[(8,"019b","益","一十〇分五六一七七五"),(35,"023b","益","七分八八六〇七五"),(132,"036b","損","七分八八六〇七五"),(159,"040a","損","一十〇分五六一七七五")]
    need([(x["limit"],x["page_id"],x["polarity"],x["numeric_glyphs"]) for x in rows]==expected,"source complete original vertical literals")
    need(all(x["complete_field"]==x["polarity"]+x["numeric_glyphs"] for x in rows),"source glyph sequence changed")
    by_limit={x["limit"]:x for x in rows}
    need(len(c["same_copy_textual_pairs"])==2 and [p["limits"] for p in c["same_copy_textual_pairs"]]==[[8,159],[35,132]],"two source-bounded matching pairs")
    for p in c["same_copy_textual_pairs"]:
        i,j=p["limits"];a,b=by_limit[i],by_limit[j]
        need(i+j==p["sum_of_limit_numbers"]==167 and a["polarity"]=="益" and b["polarity"]=="損" and a["numeric_glyphs"]==b["numeric_glyphs"]==p["identical_numeric_glyph_string"],"same-copy opposite glyph or index equality")
        need(p["positive_glyph"]==a["complete_field"] and p["negative_glyph"]==b["complete_field"],"source pair glyph provenance")
    old={8:xu["original_fields"][0],132:xu["original_fields"][1]}
    for i in (8,132):
        need(old[i]["complete_original_literal"]==by_limit[i]["complete_field"] and old[i]["page_id"]==by_limit[i]["page_id"] and old[i]["source_jpeg_sha256"]==PAGES[by_limit[i]["page_id"]],"12XU source primary glyph history rewritten")
    need([(x["limit"],x["polarity_glyph"]) for x in yb["direct_human_reading"]["rows"]]==[(35,"益"),(159,"損")],"12YB polarity ancestor changed")
    need(c["evidence_grade"]=="DIRECT_ORIGINAL_SOURCE_GLYPH_PAIR_EQUALITY_AND_OPPOSITE_POLARITY" and c["normalized_numeric_values"] is None and c["mechanical_equal_absolute_magnitude_rule"] is None and c["complete_limit_table_global_symmetry_rule"] is None and c["negative_inference_about_other_limits"] is False,"print equality promoted to algorithm")
    ctrl=d["controls"]
    need(ctrl["supplementary_full_glyph_rows_new"]==2 and ctrl["previous_l8_l132_full_fields_independently_rechecked"]==2 and ctrl["primary_six_target_original_full_field_count_remains"]==5 and ctrl["primary_solar_d16_field_identity"]=="UNRESOLVED" and ctrl["primary_six_cross_witness_numeric_mechanical_adjudications"]==0,"six primary controls changed without proof")
    need(all(ctrl[k]==0 for k in ("new_independent_physical_witnesses","new_external_source_registry_records","new_genealogy_nodes","new_genealogy_edges","chart_algorithm_reopen_count")) and ctrl["mathematical_replay_of_general_symmetry"] is False,"source/lineage/runtime scope violated")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and "docs/research/TIANWEN-12YC-G893-L8-L159-L35-L132-ORIGINAL-PAIR-GLYPH-COLLATION-R1.md" in issue["source_refs"],"omission issue/source link lost")
    rev=issue["g893_same_copy_full_original_pair_reviews"]
    need(len(rev)==1 and rev[0]["evidence_doc"]==DOC and rev[0]["source_glyph_pair_matches"]==2 and rev[0]["final_cross_witness_mechanical_decisions"]==rev[0]["new_physical_witness_count"]==0,"risk issue original-only source grade")
    need(any(h["event"]=="G893_SAME_COPY_COMPLETE_ORIGINAL_PAIR_COLLATION_APPEND" and DOC in h["evidence_refs"] for h in issue["history"]),"no forward research checkpoint")
    need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,616,0) and any(x.startswith("12YC ") for x in state["historical_audit"]["current_focus"]),"handoff state mismatch")
    need(sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in ledger["issues"])==11 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"issue/chart status")
    return {"status":"PASS","original_same_copy_literal_pairs":2,"original_supplementary_full_fields_added":2,"six_primary_full_fields":5,"D16":"UNRESOLVED","all_cross_witness_final_decisions":0}
if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))

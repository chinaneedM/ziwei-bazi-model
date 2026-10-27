#!/usr/bin/env python3
"""12YB source-only L35 and L159 gain/loss original polarity guard; CI has no original images."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YB-G893-L35-L159-SAME-COPY-LOSSGAIN-POLARITY-R1.json"
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json","docs/research/TIANWEN-12YA-G893-D16-SOLAR-HEADER-AND-EXTERNAL-ARITHMETIC-R1.json"))
def need(v,msg):
    if not v: raise ValueError(msg)
PAGES={"018b":"4decd1801d832ba5b471b047dd84cca487245038622a589b48552a0fb43ab83a","023b":"f5f732a4db9636ab563af47a5c8332e1f00eed1e587cc138d150da53f557d94f","040a":"ba5cb6bcc8ec21ce59b6a33c402cd6ee661f1466239649eaa8c661d80c63143a"}
ROIS={"CHIJI_LOSS_GAIN_COLUMN_HEADER":"143639e6dc2fed98c61a9d4f3197276869d58e8f50e339b7529be309b93d3cf5","L35_DAY_HEADING":"ce8914b76659514012bde6f25d3f47349d9c446e44eacbf201146507cc5e9ef0","L35_GAIN_SIGN":"11cdaee2604f07595754c323cfd127945ec1801a22d4cda3d3a10eecf56d464b","L34_L35_L36_ROW_NEIGHBORS":"d93b42a5b1de95386693bd2606a692a8440bc278a66cd2f1837137d22b8906d5","L159_DAY_HEADING":"5f86ac23430eabcd8249d04c822001bc8f2675f60f5dbe3f6014d1bba0c4e018","L159_LOSS_SIGN":"c4ca8c11a7ba85fb7e9b6f0d74c5007e8edb17f104839ed34a3984d3d3d13e1a","L157_L158_L159_ROW_NEIGHBORS":"9c65a6b8d49d313d86f4190a05c9ae399622955ac13547e8e38369fc9f0a87dd"}
def verify(d,ledger,state,ya):
    need(d["schema"]=="TIANWEN-12YB-G893-L35-L159-SAME-COPY-LOSSGAIN-POLARITY-R1" and d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","source identity")
    z=d["archive"]
    need(z["original_zip_sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and z["original_zip_bytes"]==33525981 and z["zip_crc_pass"] is True and z["source_original_jpg_sha256_verified"]==204 and z["ancient_image_files_committed_to_repo"]==0,"original source archive")
    need((z["source_image_width"],z["source_image_height"])==(1150,2000),"source resolution")
    need(len(d["source_pages"])==3 and {x["page_id"]:x["jpeg_sha256"] for x in d["source_pages"]}==PAGES,"direct source original page hashes")
    regs=d["original_rgb_regions"]
    need(len(regs)==7 and {x["role"]:x["sha256"] for x in regs}==ROIS and d["original_image_ocr_used"] is False,"source RGB crop evidence")
    for x in regs:
        l,t,r,b=x["rect_px"]
        need(x["page_id"] in PAGES and all(type(q) is int for q in (l,t,r,b)) and 0<=l<r<=1150 and 0<=t<b<=2000,"bad source native ROI")
    c=d["direct_human_reading"]
    need(c["original_header_018b"]=="遲疾損益分" and len(c["rows"])==2,"source printed header")
    need([(x["limit"],x["original_page"],x["day_heading"],x["polarity_glyph"],x["evidence_grade"]) for x in c["rows"]]==[(35,"023b","三十五","益","DAY_HEADING_AND_POLARITY_ONLY"),(159,"040a","一百五十九","損","DAY_HEADING_AND_POLARITY_ONLY")],"bounded source glyph reading")
    need(all(x["full_numeric_original_literal"] is None and x["normalized_value"] is None for x in c["rows"]) and c["complete_source_numeric_lanes_collated"] is False and c["opposite_signs_not_equivalent_to_equal_absolute_values"] is True,"numeric symmetry falsely inferred")
    e=d["epistemic_boundary"]
    need(e["single_original_copy"] is True and all(e[k]==0 for k in ("added_independent_physical_witnesses","final_six_cross_witness_mechanical_decisions","external_source_records_delta","genealogy_nodes_delta","genealogy_edges_delta","chart_algorithm_reopens")),"invented source lineage or algorithm effect")
    need(e["original_primary_six_full_fields_still"]==5 and e["original_solar_d16_value_and_column"] is None and e["original_l35_l159_symmetric_numeric_relation"] is None and e["negative_whole_work_claim"] is False,"invalid numerical/source closure")
    need(ya["visual_interpretation"]["candidate_full_d16_original_target_literal"] is None and ya["visual_interpretation"]["explicit_source_to_other_edition_second_column_mapping"]=="UNPROVEN","older D16 evidence overwritten")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and "docs/research/TIANWEN-12YB-G893-L35-L159-SAME-COPY-LOSSGAIN-POLARITY-R1.md" in issue["source_refs"],"risk ledger references")
    pol=issue["g893_same_copy_polarity_source_reviews"]
    need(len(pol)==1 and pol[0]["evidence_doc"]==DOC and pol[0]["observed_signs"]==["益","損"] and pol[0]["new_full_numeric_fields"]==pol[0]["new_numeric_symmetric_rules"]==pol[0]["new_independent_witness_votes"]==0,"risk ledger overclaim")
    need(any(h["event"]=="G893_SAME_COPY_LOSSGAIN_POLARITY_SOURCE_APPEND" and DOC in h["evidence_refs"] for h in issue["history"]),"forward evidence event")
    need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,615,0) and any(f.startswith("12YB ") for f in state["historical_audit"]["current_focus"]),"handoff continuity")
    need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0 and sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in ledger["issues"])==11,"no algorithm or risk closure")
    return {"status":"PASS","same_copy_source_polarity":"L35=益; L159=損","source_numeric_symmetry":"UNRESOLVED","primary_source_complete_fields":"5/6","D16_original_print":"UNRESOLVED","cross_witness_final":"0/6"}
if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))

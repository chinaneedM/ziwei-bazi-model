#!/usr/bin/env python3
"""12YA: independent original-page/neighbor source scope + exact external-only arithmetic."""
from decimal import Decimal
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE="docs/research/TIANWEN-12YA-G893-D16-SOLAR-HEADER-AND-EXTERNAL-ARITHMETIC-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
XY="docs/research/TIANWEN-12XY-G893-L101-D16-ADJACENT-ORIGINAL-COLUMN-SCOPE-R1.json"
XZ="docs/research/TIANWEN-12XZ-G893-L101-DIRECT-FULL-GLYPH-R1.json"
VARIANT="docs/research/MING-DATONG-1569-CROSS-EDITION-VARIANT-LEDGER-R1.json"
def need(x,reason):
    if not x: raise ValueError(reason)
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (EVIDENCE,LEDGER,STATE,XY,XZ,VARIANT))
PAGES={"001a":"8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5","002a":"31d0452e9350e32ff73549f49d894ab26f6e588654926d45b3a603ae4da9a914","002b":"f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"}
ROIS={"SOLAR_WINTER_ACTIVE_PRINTED_COLUMN_LABELS":"79587768ac45f0a989de16eb0738357f2b6da18ab31985e452c3f3cbe231ff4e","DAY15_SINGLE_PRINT_PAIR":"1889dd7bf7643d7c908c70964921c78b973a7771e7f0a90000a91752f06e40d0","DAY16_SINGLE_PRINT_PAIR":"1a0e93cbac318563e799e79259280deb94bc06ad69aa364151511655c6a3d353","DAY17_SINGLE_PRINT_PAIR":"f474bc7b8fcfccb220dd4654379ce2eb0ca5da642f524a322950a526b8abf2b0","D15_D16_D17_BOUNDARY_UNBROKEN":"234af60ba561fb3df28e51cdefe64e9716c0cb11b0e32786206c97ef4bb77777","D13_SAME_SERIES_CONTINUITY":"7cc4bdc662f59b3e72e4fb478e03e685450ed7807bc7f91f91363a81b917b38d"}

def verify(d,ledger,state,xy,xz,variant):
    need(d["schema"]=="TIANWEN-12YA-G893-D16-SOLAR-PRINTED-COLUMNS-AND-EXTERNAL-ARITHMETIC-CONTROL-R1","12YA schema")
    need(d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and "GK00893_00" in d["provider_copy"],"wrong physical witness")
    ziprec=d["archive"]
    need(ziprec["byte_count"]==33525981 and ziprec["zip_sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and ziprec["source_jpegs_sha256_replayed"]==204 and ziprec["original_images_committed"]==0,"source original archive and image publication boundary")
    need({x["page_id"]:x["jpeg_sha256"] for x in d["direct_original_page_evidence"]}==PAGES,"three original page hashes")
    rois=d["original_rgb_roi"]
    need(rois["pixel_width"]==1150 and rois["pixel_height"]==2000 and rois["ocr_used"] is False,"native pixel/OCR grade")
    regs=rois["regions"]
    need(len(regs)==6 and {x["role"]:x["sha256"] for x in regs}==ROIS,"source original ROI digests")
    for row in regs:
        l,t,r,b=row["rect_px"]
        need(all(type(q) is int for q in (l,t,r,b)) and 0<=l<r<=1150 and 0<=t<b<=2000 and row["page_id"] in PAGES and re.fullmatch("[0-9a-f]{64}",row["sha256"]), "source ROI geometry")
    obs=d["visual_interpretation"]
    need(obs["direct_original_day_headings"]==["十五日","十六日","十七日"] and obs["original_header_terms_directly_visible"]==["積日","盈縮加分","盈縮積","日差加一秒八十六少"],"day/solar source header evidence")
    need(obs["candidate_full_d16_original_target_literal"] is None and obs["explicit_source_to_other_edition_second_column_mapping"]=="UNPROVEN" and obs["original_d16_numeric_variant_result"] is None and obs["negative_evidence_whole_manuscript"] is False,"unsupported D16 source target identity or whole-book absence")
    scope=d["historical_edition_comparability"]
    need(scope["g893_current_status"].endswith("UNPROVEN") and scope["not_a_negative_exhaustive_proof"] is True and scope["older_variant_ledger_not_modified"] is True,"D16 comparability/negative-proof guard")
    a=d["external_edition_arithmetic"]
    need(a["status"]=="EXTERNAL_LEDGER_INTERNAL_SEQUENCE_CONSISTENCY_ONLY_NOT_G893_SOURCE_NUMBER" and a["does_not_identify_transmission_cause"] is True and a["does_not_overwrite_received_original_5_1362"] is True,"external arithmetic imported as G893 reading")
    v=next(x for x in variant["numeric_variant_controls"] if x["id"]=="VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE")
    raw=a["input_strings"]
    need(raw=={"day15":v["neighboring_sequence_controls"]["day15"],"day17":v["neighboring_sequence_controls"]["day17"],"constant_day_increment":v["neighboring_sequence_controls"]["increment"],"ming1569_day16":v["ming_1569_primary"],"goryeosa_received_day16":v["krdb_goryeosa_current_transcript"]},"independent edition inputs mismatched")
    p15,p17,step,ming,received=(Decimal(raw[k]) for k in ("day15","day17","constant_day_increment","ming1569_day16","goryeosa_received_day16"))
    midpoint=(p15+p17)/2
    got={"day15_plus_increment":p15+step,"day17_minus_increment":p17-step,"symmetric_neighbor_midpoint":midpoint,"ming1569_residual":ming-midpoint,"goryeosa_received_residual":received-midpoint,"goryeosa_d16_minus_day15":received-p15,"day17_minus_goryeosa_d16":p17-received}
    need(all(a["derived_strings"][k]==str(v) for k,v in got.items()),"four-decimal external numeric replay mismatch")
    need(ming==midpoint and received!=midpoint and (received-midpoint)==Decimal("-0.1000"),"external D16 precision/branch fence")
    old=xy["original_manual_visual"]["solar"]
    need(old["original_second_difference_numeric_literal"] is None and old["original_second_difference_column_exact_identity"]=="UNRESOLVED_NO_ONE_TO_ONE_MAPPING_PROVED" and xy["research_grade"]["complete_source_literal_fields_prior_and_now"]==4,"12XY older original column conclusion overwritten")
    need(xz["target"]["original_literal_full_field"]=="五度二十〇分四八一一二五" and xz["scope"]["original_full_literal_fields_now"]==5,"12XZ L101 source completeness lost")
    safe=d["safeguards"]
    need((safe["source_full_fields_before"],safe["source_full_fields_after"],safe["all_six_cross_edition_mechanical_variant_final_decisions"],safe["open_research_issues"])==(5,5,0,11),"D16 source grade inflated")
    need(all(safe[k]==0 for k in ("new_independent_physical_witnesses","new_external_source_records","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens")) and safe["old_12xy_and_12xz_evidence_not_rewritten"] is True,"unsupported source/lineage/algorithm change")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    need(issue["status"]=="OPEN" and EVIDENCE in issue["source_refs"],"D16 issue/record disconnected")
    reviews=issue.get("g893_d16_solar_bounded_structural_reviews",[])
    need(len(reviews)==1 and reviews[0]["evidence_doc"]==EVIDENCE and reviews[0]["source_full_field_added"]==0 and reviews[0]["mechanical_variant_decisions_awarded"]==0,"forward-only D16 structure review absent")
    need(issue["history"][-1]["event"]=="G893_D16_SOLAR_BOUNDED_ARITHMETIC_CONTEXT_APPEND" and EVIDENCE in issue["history"][-1]["evidence_refs"],"D16 source+external arithmetic history missing")
    need(len(issue["g893_target_field_reviews"])==3 and len(issue["g893_loss_gain_complete_field_reviews"])==2,"other five original target fields overwritten")
    need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.614.0","12YA live state mismatch")
    need(state["historical_audit"]["current_focus"][-1].startswith("12YA ") and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product/chart invariant")
    need(sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in ledger["issues"])==11,"open research issue count")
    return {"status":"PASS","G893_D16_full_field":"UNPROVEN","six_source_original_complete_literal_fields":5,"external_midpoint":str(midpoint),"received_minus_midpoint":str(received-midpoint),"final_cross_witness_numeric_decisions":0}
if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))

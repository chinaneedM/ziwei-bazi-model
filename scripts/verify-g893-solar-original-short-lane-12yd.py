#!/usr/bin/env python3
"""12YD exact source-origin three-day solar lexical sequence, not proven field identity."""
from decimal import Decimal
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YD-G893-D15-D17-DIRECT-SOLAR-PRINTED-FIVE-FEN-SEQUENCE-R1.json"
PAGES={"001a":"8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5","002b":"f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"}
ROIS={"SOLAR_ORIGINAL_HEADER":"c62fa68a04efe945f8375610c51425c978072781a1d992b98b6d74467894ae0d","D15_PRINTED_DAY_HEADING":"f842112fbd1181a4f900b27e857cca4c896044dcced7af3b81d1f9fe6c25c87f","D16_PRINTED_DAY_HEADING":"50d615a2cd6aa887353f0ecca1283e470b5b64625d1ebe0dbf5df7f0565fc6bf","D17_PRINTED_DAY_HEADING":"04bc782eb91e6094e259fe80af5407331f987ad8dfecafb59680b289369cdd0a","D15_PRINTED_CANDIDATE_LANE":"e594682be69f1e6c293a8bb84e66c77f929ef28d6647fa7658f04e5a8c3ba69f","D16_PRINTED_CANDIDATE_LANE":"adca5d1c4026f68eb269e2e04597a4f8eeeb833c81c944095dc789294fd8270f","D17_PRINTED_CANDIDATE_LANE":"19f1cf42e1b7e149bb4595a0cd96706f6db6d199ed02236f82773854581aa0a6","D15_D17_UNBROKEN_LAYOUT":"a9f03e62ecb24ea14fb613b12a1af44573c9f7b35e66c6d4f199fad44e673425"}
def need(x,msg):
 if not x: raise ValueError(msg)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf8")) for p in (DOC,"docs/research/TIANWEN-12YA-G893-D16-SOLAR-HEADER-AND-EXTERNAL-ARITHMETIC-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,ya,ledger,state):
 need(d["schema"]=="TIANWEN-12YD-G893-BOUNDED-D15-D17-SOLAR-SHORT-COLUMN-READINGS-R1" and d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","source identity")
 z=d["archive"]
 need(z["size_bytes"]==33525981 and z["sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and z["zip_crc"]=="PASS" and z["total_original_jpegs_sha_replayed"]==204 and z["original_dimension"]==[1150,2000] and z["original_images_committed"]==0,"source archive")
 need(len(d["direct_original_pages"])==2 and {x["page_id"]:x["jpeg_sha256"] for x in d["direct_original_pages"]}==PAGES,"original source page hashes")
 o=d["native_rgb_regions"]
 need(o["ocr_used"] is False and len(o["regions"])==8 and {x["role"]:x["sha256"] for x in o["regions"]}==ROIS,"source native pixel ROI hashes")
 for x in o["regions"]:
  l,t,r,b=x["rect_px"]
  need(x["page_id"] in PAGES and all(type(q) is int for q in (l,t,r,b)) and 0<=l<r<=1150 and 0<=t<b<=2000,"bad original ROI geometry")
 r=d["original_reading_scope"]
 need(r["header_page_id"]=="001a" and r["header_terms_visible"]==["積日","盈縮加分","盈縮積","日差加一秒八十六少"] and r["adjacent_original_day_headings"]==["十五日","十六日","十七日"],"original header/row labels")
 rows=r["source_bounded_candidate_vertical_lane"]
 need(len(rows)==3 and [(x["day"],x["original_short_glyph_string"],x["derived_candidate_decimal_string"]) for x in rows]==[(15,"五分二一七六","5.2176"),(16,"五分二三六二","5.2362"),(17,"五分二五四八","5.2548")],"original copied glyph not matching source-bound numeric candidate")
 need(all(x["semantic_scope"]=="SOURCE_PRINTED_SHORT_LANE_CANDIDATE_NO_HEADER_COLUMN_IDENTITY_AWARD" for x in rows),"unsupported source field identity")
 a,b,c=(Decimal(x["derived_candidate_decimal_string"]) for x in rows); n=d["arithmetic_on_source_scoped_candidate_digits"]
 need(str(b-a)==n["day16_minus_day15"]=="0.0186" and str(c-b)==n["day17_minus_day16"]=="0.0186" and str(c-a)==n["day15_to_day17_double_step"]=="0.0372" and n["same_increment_twice"] is True,"source candidate Decimal replay")
 need(n["solar_header_increment_unit_identity"]=="UNPROVEN" and n["copying_or_transmission_causality"]=="UNPROVEN" and n["independent_physical_witness_vote_for_external_edition"]==0,"arithmetic promoted to historical causality")
 need(r["header_to_specific_short_lane_mechanical_equivalence"]=="UNPROVEN" and r["candidate_full_d16_target_second_difference_field_literal"] is None and r["confirmed_target_original_field_count_after"]==5 and r["does_not_prove_absence_elsewhere"] is True,"target field prematurely closed")
 need(ya["visual_interpretation"]["candidate_full_d16_original_target_literal"] is None and ya["visual_interpretation"]["explicit_source_to_other_edition_second_column_mapping"]=="UNPROVEN","historical 12YA rewritten")
 g=d["scope_guard"]
 need((g["six_principal_g893_original_complete_target_fields_before"],g["six_principal_g893_original_complete_target_fields_after"],g["six_final_cross_witness_mechanical_variant_decisions"],g["open_omission_issues"])==(5,5,0,11),"target count inflated")
 need(all(g[k]==0 for k in ("new_source_registry_records","new_independent_physical_copies","new_genealogy_nodes","new_genealogy_edges","chart_algorithm_reopens")),"fake source or algorithm vote")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and "docs/research/TIANWEN-12YD-G893-D15-D17-DIRECT-SOLAR-PRINTED-FIVE-FEN-SEQUENCE-R1.md" in issue["source_refs"],"omission research evidence missing")
 review=issue["g893_d16_three_day_short_lane_reviews"]
 need(len(review)==1 and review[0]["evidence_doc"]==DOC and review[0]["original_target_source_field_finalized"] is False and review[0]["principal_source_fields_awarded"]==review[0]["cross_witness_final_decisions_awarded"]==0,"issue numeric overclaim")
 need(any(h["event"]=="G893_D16_THREE_DAY_DIRECT_SHORT_LANE_APPEND" and DOC in h["evidence_refs"] for h in issue["history"]),"12YD forward-only event")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,617,0) and any(f.startswith("12YD ") for f in state["historical_audit"]["current_focus"]),"state handoff mismatch")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0 and sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in ledger["issues"])==11,"product or issue grade changed")
 return {"status":"PASS","same_original_printed_candidate_strings":3,"candidate_increment":"0.0186","D16_full_target_original_field":"UNPROVEN","main_target_fields":"5/6","cross_witness_mechanical_final":"0/6"}
if __name__=="__main__":
 print(json.dumps(verify(*load()),ensure_ascii=False))

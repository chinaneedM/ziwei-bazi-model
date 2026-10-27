#!/usr/bin/env python3
"""13BG NAJ historical original cross-folio cumulative collation (strict local scope)."""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PC="docs/research/TIANWEN-13BG-GORYEOSA-NAJ-ADJACENT-FOLIOS-CUMULATIVE-D17-D19-R1.json"
PBE="docs/research/TIANWEN-13BE-GORYEOSA-D16-ORIGINAL-LONG-LANE-DUAL-COPY-COLLATION-R1.json"
PBF="docs/research/TIANWEN-13BF-GORYEOSA-D14-D17-ORIGINAL-ACCUMULATIVE-LOCAL-INDEX-OFFSET-R1.json"
PYZ="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
MD=PC.replace(".json",".md")
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,be,bf,yz,ledger,state):
    assert e["schema"]=="TIANWEN-13BG-NAJ-GORYEOSA-CANVAS16-18-ORIGINAL-CROSSFOLIO-CUMULATIVE-LOCAL-RECURRENCE-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    assert e["prior_original_positive_evidence"]=={"d16_d17_source":PBE,"d14_d17_cumulative":PBF,"institutional_received_text":PYZ}
    assert e["source_holding"]=="NAJ-282-0006-PHYSICAL51"
    assert e["source_manifest"]=="https://www.digital.archives.go.jp/api/iiif/4898853/manifest.json"
    assert e["manifest_sha256"]=="3f38f52860bd06ca7f4b89cec65a32b8529fcb547ac098548120e8071fe370a1"
    assert e["previous_original_capture_artifact_id"]==12258234108
    assert e["previous_original_capture_part2_zip_sha256"]=="dd7e35494898f5a3dae1c9cff1a05627c2fe4ca530ebea0434c67f8f356320f4"
    pages=e["source_canvases"]
    assert [z["canvas_1based"] for z in pages]==[16,17,18]
    assert [z["source_jpeg_sha256"] for z in pages]==[
      "23814245c0e7952a4d8581068d23448e285cd14b145b8824c8bfa9aeb6501884",
      "8362e8a2b8ddf5f36408d4450a81ebad2d9548b32f49dbe37e01493592b7c3e9",
      "88cecf62c8cd0dd623199eb06e3044efbe61771c1ffe058b8e7a87cc2f8f88cc"]
    assert all(z["image_dimensions"]==[3000,2215] for z in pages)
    h=pages[0]["new_rgb_roi"]
    assert h["bbox"]==[1690,525,2070,1370]
    assert h["rgb_pixel_sha256"]=="ef56c086161332799d8057d4afe9e86660ebff5000d28685ca9ecae44e40ec8b"
    assert h["direct_heading_glyph"]=="積日"
    old=be["source_original_image_reviews"][0]
    assert pages[1]["source_jpeg_sha256"]==old["original_image_sha256"]==bf["manuscript_originals"][0]["source_JPEG_sha256"]
    assert pages[1]["reuse_prior_original_glyphs"]=={
      "apparent_layout_day17_cumulative":be["adjacent_cumulative_scope"]["printed_day17_decimal"],
      "day16_original_long":be["roman_decimal_bridge"]["day16_long"],
      "day17_original_long":be["roman_decimal_bridge"]["day17_long"]}
    new=pages[2]["new_day_slots"]
    assert len(new)==2
    assert [(z["apparent_layout_day"],z["field"],z["literal"],z["decimal"],z["original_rgb_roi_bbox"],z["original_rgb_pixel_sha256"]) for z in new]==[
      (18,"CUMULATIVE","八千〇〇〇二六九七","8000.2697",[2420,845,2540,1785],"72b8eb3bbbbaeb28709ab34cce656420645089eba248a0dfd3eb8cba2be48d11"),
      (19,"CUMULATIVE","八千四百二十四六四〇八","8424.6408",[2250,845,2390,1785],"ce11ad92df2c10b8d4ee17c60338b6683180a4626542c6a461330d4ab50a5251")]
    c={17:Decimal(pages[1]["reuse_prior_original_glyphs"]["apparent_layout_day17_cumulative"]),18:Decimal(new[0]["decimal"]),19:Decimal(new[1]["decimal"])}
    longs={16:Decimal(old["day_rois"][0]["long_original"].replace("四百二十九六〇七三","429.6073")),
           17:Decimal(be["roman_decimal_bridge"]["day17_long"])}
    assert longs[16]==Decimal("429.6073")
    edges=e["crossfolio_original_decimal_relations"]
    assert len(edges)==2
    for edge,n in zip(edges,(17,18)):
       assert edge["from_layout_day"]==n and edge["to_layout_day"]==n+1
       assert edge["matches_original_long_day"]==n-1
       assert Decimal(edge["original_cumulative_delta"])==c[n+1]-c[n]==longs[n-1]==Decimal(edge["long"])
    assert e["local_four_edge_span"]=={"first_app_layout_day":15,"last_app_layout_day":19,"covered_differences":4,"source_per_original_page_glyph_counted_as_independent_witness":False}
    assert len(bf["bounded_original_local_numeric_equations"])==2
    assert e["original_image_capture_new_objects"]==0 and e["previously_archived_image_reuse"] is True and e["number_of_new_physical_witnesses"]==0
    assert e["original_label_mechanical_definition"]=="UNADJUDICATED" and e["full_day_index_convention"]=="UNADJUDICATED"
    assert e["cross_work_equivalence_G893"]=="UNPROVEN" and e["historical_earliest_D16_one_vs_two"]=="UNRESOLVED"
    assert e["original_NAJ_vs_WASEDA_textually_independent"]=="UNPROVEN"
    assert all(x is True for x in e["evidence_negative_controls"].values())
    counts=e["scope_counters"]
    assert all(counts[k]==0 for k in ("new_registry_entries","matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","independent_stemmatic_votes_added","algorithm_reopens"))
    assert counts["open_issues"]==11 and counts["chart_product"]=="CLOSED"
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    assert issue["status"]=="OPEN" and issue["priority"]=="P0"
    assert issue["source_refs"].count(MD)==1 and issue["source_refs"].count(PC)==1
    assert issue["source_refs"].index(PC)==issue["source_refs"].index(MD)+1
    assert any(x["event"]=="GORYEOSA_13BG_NAJ_ORIGINAL_CROSSFOLIO_CUMULATIVE_AND_SOURCE_HEADING" for x in issue["history"])
    assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert any(x.startswith("13BG ") for x in state["historical_audit"]["current_focus"])
    assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
    assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0]
    assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
    assert len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11
    return True
if __name__=="__main__":
    assert check(load(PC),load(PBE),load(PBF),load(PYZ),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
    print("13BG NAJ cross-folio D17-19 original cumulative local gate PASS")

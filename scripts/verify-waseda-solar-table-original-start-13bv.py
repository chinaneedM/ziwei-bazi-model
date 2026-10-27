#!/usr/bin/env python3
"""13BV original Waseda solar table title, JIRI printed heading, and D0-D20 folio seam source."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BV-GORYEOSA-WASEDA-P21-P23-ORIGINAL-SOLAR-TABLE-TITLE-AND-FIRST-DAY-INDEX-R1.json"
MD="docs/research/TIANWEN-13BV-GORYEOSA-WASEDA-P21-P23-ORIGINAL-SOLAR-TABLE-TITLE-AND-FIRST-DAY-INDEX-R1.md"
BU="docs/research/TIANWEN-13BU-GORYEOSA-WASEDA-D16-FOLIO-SEAM-AND-PRECEDING-SOURCE-R1.json"
BS="docs/research/TIANWEN-13BS-GORYEOSA-WASEDA-D16-NAJ-D18-D19-SOURCE-NATIVE-GLYPH-COLLATION-R1.json"
BN="docs/research/TIANWEN-13BN-GORYEOSA-WASEDA-P23-P24-TIGHT-CUMULATIVE-AND-LONG-ROI-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
SHA=[[21,64,"acf08f57fcd82d35f6b2b3359449dd72def4b7124f9a25412bbec3812bc96bb7",[2592,1728]],[22,67,"4dbfc14caef81f63566d40db6f57fd73e23cbd1fd2cb627ee88def02ae98901d",[2592,1728]],[23,70,"388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66",[2592,1728]]]
ROIS=[["P21_SOLAR_TABLE_FULL_TITLE",21,"太陽冬至前後二象盈初縮末限",[1075,340,1195,1200],"f1201d193a77652b89e38b26019dfc29adbb13c78f5862c5459a947a45937b05","ORIGINAL_TABLE_TITLE_VERTICAL"],["P21_JIRI_HEADING",21,"積日",[1020,350,1098,605],"811ef14bf261f82edbed1aad9b69facd4437129f5bf8d68e37b8a9c4c2f4f1f5","ORIGINAL_DAY_INDEX_HEADING"],["P21_D0_HEADING",21,"初日",[815,350,920,615],"69d9a2779c7a2e71dd6683951d0842d5240dd4cc3309e2b958c66b1b4d3ac92f","ORIGINAL_DAY_SLOT"],["P21_D1_HEADING",21,"一日",[650,350,760,615],"4dd2cf279be8b92e6c9a8e231c1392ef83cf50f98d78be5d4834e033379523d4","ORIGINAL_DAY_SLOT"],["P21_D2_HEADING",21,"二日",[485,350,600,615],"a66275a5ebe93da19d6978fbee58402e947da387e2589ce14f80f874a2756d06","ORIGINAL_DAY_SLOT"],["P22_D3_HEADING",22,"三日",[2070,340,2180,605],"b91f618942678124cf3afa68979e2af61f63c4053b5faf2f1579c8547ae5105d","ORIGINAL_DAY_SLOT"],["P22_D11_HEADING",22,"十一日",[480,340,600,620],"811ec98a5ed0d3d5daf557e6a07f037c7f948473a207e37b4421b8646e37bdba","ORIGINAL_DAY_SLOT"],["P23_D12_HEADING",23,"十二日",[2070,340,2190,625],"ca8f1994a5941b146097b1821af6a253ddabb9c82d9a2ce411405da1feaa5020","ORIGINAL_DAY_SLOT"],["P23_D20_HEADING",23,"二十日",[470,340,595,625],"dfaebdab71c359d255f7e49b1f9c5add00aa6811d31ffa9b6dae5d266fcc54b8","ORIGINAL_DAY_SLOT"]]
def load(path):return json.loads((R/path).read_text(encoding="utf-8"))
def replay_source_images(e,p21,p22,p23):
 from PIL import Image
 for info,path in zip(e["source"]["firstparty_original_images"],[p21,p22,p23]):
  b=Path(path).read_bytes()
  assert hashlib.sha256(b).hexdigest()==info["jpeg_sha256"]
  with Image.open(path) as im:
   rgb=im.convert("RGB")
   assert list(rgb.size)==info["dimensions"]
   for r in e["source_original_header_rois"]:
    if r["page"]==info["page"]:
     assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"]
 return True
def check(e,s,l,old):
 assert e["schema"]=="TIANWEN-13BV-WASEDA-FIRSTPARTY-ORIGINAL-SOLAR-TABLE-TITLE-AND-D0-D20-PAGE_SEQUENCE-R1"
 assert e["date"]=="2026-10-21" and e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="DIRECT_MANUAL_FIRSTPARTY_ORIGINAL_JPEG_RGB_SHA_NO_OCR_HEADER_AND_PAGE_ORDER_ONLY"
 src=e["source"]
 assert src["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert src["pdf_sha256"]==old["BU"]["source"]["pdf_sha256"]
 assert src["artifact_source_run_id"]==39594574917 and src["artifact_id"]==12342817907
 assert src["artifact_zip_sha256"]=="8bd5928c12df7f04900574b2bc610aa2ac31ed1c417d314a6854a484336070cc"
 assert src["source_same_copy_previous_p23_artifact_id"]==12340588249
 assert [(z["page"],z["xref"],z["jpeg_sha256"],z["dimensions"]) for z in src["firstparty_original_images"]]==[tuple(z) for z in SHA]
 assert src["firstparty_original_images"][2]["jpeg_sha256"]==old["BU"]["source"]["known_embedded_jpeg_sha256"]==old["BS"]["source_images"][0]["jpeg_sha256"]
 assert src["source_p20_usage"]=="PRECEDING_PROSE_NOT_BOUND_TO_SOLAR_TABLE_HEADER"
 assert len(e["source_original_header_rois"])==9
 assert [(z["key"],z["page"],z["literal"],z["bbox"],z["rgb_sha256"],z["kind"]) for z in e["source_original_header_rois"]]==[tuple(z) for z in ROIS]
 expected=[(21,["初日","一日","二日"]),(22,["三日","十一日"]),(23,["十二日","二十日"])]
 seq=e["source_local_table_sequence"]
 assert [(z["pdf_page_1based"],z.get("visible_initial_days",[z.get("visible_days_first"),z.get("visible_days_last")])) for z in seq]==expected
 facts=e["finding"]
 assert facts["solar_table_original_title"]=="太陽冬至前後二象盈初縮末限"
 assert facts["original_printed_day_index_heading"]=="積日"
 assert facts["original_initial_day_heading"]=="初日"
 assert facts["bounded_table_start_and_page_sequence_direct"] is True
 assert facts["original_table_end"]=="UNCOLLATED_AFTER_DAY20"
 assert facts["Waseda_day16_exact_independent_cumulative"]=="UNBOUND"
 assert facts["printed_JIRI_equivalent_to_cumulative_numeric_field"]=="NOT_ESTABLISHED"
 assert facts["whole_table_day_index_formula"]=="NOT_ESTABLISHED"
 assert facts["G893_SHAO_WEI_TO_MING1569_FIELD_UNITS"]==facts["two_copy_direct_textual_lineage"]=="UNPROVEN"
 assert e["prior_dependencies"]=={"source_acquisition_and_folio_boundary":BU,"day16_original_read":BS,"waseda_d19_d21_numeric_control":BN}
 fw=e["scope_firewall"]
 assert fw["new_original_folio_image_objects_read"]==2
 assert all(fw[k]==0 for k in ("new_physical_source_witnesses","new_independent_stemmatic_votes","new_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert fw["open_research_risks"]==len(l["issues"])==11 and fw["product"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-ORIGINAL-SOLAR-TABLE-START-13BV")
 assert rev["previous_next_action"].startswith("13BU CURRENT ACTION")
 assert {MD,P,BU,BS,BN}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in x.get("changed_fields",[]) for x in issue["history"][issue["history"].index(rev)+1:])
 prefix=l["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BV CURRENT ACTION") or (later and prefix!="13BV" and (issue["next_action"].startswith(prefix+" CURRENT ACTION") or issue["next_action"].startswith(next((z["revision_id"].split("-")[3]+" CURRENT ACTION" for z in reversed(issue["history"]) if "next_action" in z.get("changed_fields",[]) and len(z.get("revision_id","").split("-"))>3 and z["revision_id"].split("-")[3].startswith("13")),"__NO_RECORDED_ACTION__"))))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(z.startswith("13BV ") for z in s["historical_audit"]["current_focus"])
 assert prefix==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in l["issues"]}
 assert (R/MD).is_file()
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--p21");p.add_argument("--p22");p.add_argument("--p23")
 a=p.parse_args();e=load(P)
 assert check(e,load(S),load(L),{"BU":load(BU),"BS":load(BS),"BN":load(BN)})
 if a.p21 or a.p22 or a.p23:
  assert a.p21 and a.p22 and a.p23
  assert replay_source_images(e,a.p21,a.p22,a.p23)
 print("13BV Waseda original solar D0-D20 table heading/source folios source pixel SHA PASS")

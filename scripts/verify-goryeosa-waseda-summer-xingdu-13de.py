#!/usr/bin/env python3
"""13DE: original Waseda XingDu triple, fail closed on physical/edition independence."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13DE-WASEDA-SUMMER-XINGDU-D28-D30-THREE-ROW-ORIGINAL-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13DE-WASEDA-SUMMER-THREE-ROW-SOURCE-NATIVE-XINGDU-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 h=e["holding"]
 assert h["artifact_id"]==12346735638 and h["archive_workflow_run"]==39601924438
 assert h["zip_sha256"]=="0ce306c099a1ed62dd24a3256ba043062490409bd5d531b543c16f1b00017710"
 assert h["ocr_used"] is False and h["same_holding_and_existing_physical_copy"] is True
 assert h["camera_overlap_control"]["status"]=="SAME_PRINTED_OPENING_AS_P34_SEPARATE_PHOTOGRAPH_NOT_SEPARATE_PHYSICAL_WITNESS"
 ims=h["source_jpegs"]
 assert [(x["pdf_page"],x["sha256"],x["rgb_sha256"],x["dimensions"]) for x in ims]==[
 (34,"6ee4ead3df88ee2ec5f4a9027ac085c0f017ca44ddcda57e104116a08795eb03","79c795dbfe45ac1dafd06a4611913ed460c68ce8dcebc83572a17306f36ad757",[2592,1728]),
 (36,"cd50d406c9bc446b5583770e1d1454f80520c8e1e4dde2e6a5c5a08e460dbc69","1d98b805e4c086a741ec824c48b9bb0ead2ced5a4db045c9341fbd2035ad50f5",[2592,1728])]
 expected=[
 (28,34,"二十八日",[410,400,490,615],"d7a6811e18f73ab667022f9c5dc6975c73d463fbe32489d800879bf7f9cdc0b5","初度九十六四〇六二","0.964062",[515,660,565,1285],"c323f072cbe095e13b4b349d41d1d6e09da2b1ab946b8e108821155b4a5a5352",27),
 (29,36,"二十九日",[1960,380,2060,625],"1ed83efda69d5ac6407adcd901b4188da70b478dc0741f378eaa666d3979a801","初度九十九四五四九","0.994549",[2078,625,2137,1300],"167c76dea9dbba74f3b1e1b7c825b6b9031ac46ec6ee2016b62f42aae2313389",28),
 (30,36,"三十日",[1790,380,1890,625],"a30f297106e5addbe90b3d8068e0a8adc4d7a821b420a1557e53961542fc2cce","初度九十六五〇三八","0.965038",[1890,625,1960,1300],"3ade678f6bfc013aedbb94fa37390366ee63973cbd4cf9cc94fb63d4dce52fe3",29)]
 vals=[(z["waseda_printed_day"],z["pdf_page"],z["heading_literal"],z["heading_bbox"],z["heading_rgb_sha256"],z["xingdu_literal"],z["xingdu_value"],z["xingdu_bbox"],z["xingdu_rgb_sha256"],z["corresponding_1909_printed_day"]) for z in e["source_native_loci"]]
 assert vals==expected
 for z in e["source_native_loci"]:
  for key in ("heading_bbox","xingdu_bbox"):
   a,b,c,d=z[key];assert 0<=a<c<=2592 and 0<=b<d<=1728
 c=e["cross_original_locus_comparison"]
 assert c["nineteen_oh_nine_pdf_page"]==152
 assert c["nineteen_oh_nine_printed_days"]==[27,28,29]
 assert c["waseda_printed_days"]==[28,29,30]
 assert c["nineteen_oh_nine_xingdu"]==c["waseda_xingdu"]==["0.964062","0.994549","0.965038"]
 assert c["local_day_header_offset_waseda_minus_1909"]==1
 assert c["scope"]=="THREE_CONSECUTIVE_XINGDU_READINGS_ONLY_NO_WHOLE_TABLE_INDEX_LAW"
 assert c["misleading_same_numbered_D28_comparison_rejected"] is True
 a=e["arithmetic_scope"]
 assert a["waseda_printed_heading_day"]==29 and a["waseda_original_corresponding_xingdu"]=="0.994549"
 assert a["derived_candidate_only"]=="0.964549" and a["difference"]=="0.030000"
 assert a["earlier_source_candidate_0_964549_attested"] is False
 assert a["unique_historical_typographic_error_diagnosed"] is False
 q=e["adjudication"]
 assert q["status"]=="TWO_HOLDINGS_SOURCE_ORIGINAL_SAME_XINGDU_GLYPH_WITH_THREE_ROW_PRINTED_DAY_OFFSET_UNPROVEN_STEMMATIC_INDEPENDENCE"
 assert q["naj_summer_original"]=="UNCOLLATED"
 assert q["separate_winter_D16"]=="OPEN" and q["early_archetype_winner"]=="UNRESOLVED"
 assert all(q[k]==0 for k in ("new_source_registry_entries","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_stemmatic_votes","algorithm_reopens"))
 p=e["impact"];assert (p["matrix_rows"],p["matrix_audited"],p["sources"],p["genealogy_nodes"],p["genealogy_edges"],p["open_issues"])==(222,222,754,252,238,11)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13DE ") for x in s["historical_audit"]["current_focus"]), "historical 13DE focus lost"
 assert any(x.startswith("13DD ") for x in s["historical_audit"]["current_focus"])
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["status"]=="OPEN" and E in i["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13DE-WASEDA-ROW-OFFSET" for x in i["history"])
 assert any(x.get("id")=="OMISSIONS-13DE-WASEDA-SUMMER-20261023" for x in l["checkpoint_log"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 return True
def replay(e,w34,w36):
 from PIL import Image
 import io
 im={}
 for page,path in ((34,w34),(36,w36)):
  row=next(x for x in e["holding"]["source_jpegs"] if x["pdf_page"]==page)
  raw=Path(path).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==row["sha256"]
  pic=Image.open(io.BytesIO(raw)).convert("RGB")
  assert list(pic.size)==row["dimensions"]
  assert hashlib.sha256(pic.tobytes()).hexdigest()==row["rgb_sha256"]
  im[page]=pic
 for row in e["source_native_loci"]:
  pic=im[row["pdf_page"]]
  for roi,hashname in (("heading_bbox","heading_rgb_sha256"),("xingdu_bbox","xingdu_rgb_sha256")):
   assert hashlib.sha256(pic.crop(row[roi]).tobytes()).hexdigest()==row[hashname]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--p34-original");ap.add_argument("--p36-original");a=ap.parse_args()
 e=load(E);assert check(e,load(S),load(L))
 if a.p34_original or a.p36_original:
  assert a.p34_original and a.p36_original
  assert replay(e,a.p34_original,a.p36_original)
 print("TIANWEN_13DE_WASEDA_THREE_SOURCE_NATIVE_XINGDU=PASS")

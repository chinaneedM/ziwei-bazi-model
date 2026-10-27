#!/usr/bin/env python3
"""13CG: source-native original solar first-page header and coverage firewall, no OCR."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CG-GORYEOSA-TWO-HOLDING-ORIGINAL-INITIAL-TABLE-HEADINGS-AND-OBSCURED-DAY0-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
ROI_KEYS=["NAJ:SOLAR_TITLE","NAJ:DAY_INDEX_JIRI","NAJ:INITIAL_DAY_CHURI",
          "NAJ:TECHNICAL_FIELD_RUBRIC","WASEDA:SOLAR_TITLE","WASEDA:DAY_INDEX_JIRI",
          "WASEDA:INITIAL_DAY_CHURI","WASEDA:TECHNICAL_FIELD_RUBRIC",
          "WASEDA:INITIAL_DAY_VISIBLE_OVERLAY"]
ROI_SHAS=["c1f4a552b9368b237581a97dcf4f8879fad41aef335426b5aea08155fbc5bb11","512c98971992cbd581d02c133659c9d7894dff9eac282a53b94b30167d78e9b1","0fd91c685c019fed4fda9b93d3cae733b9f704af5860103b1b9efa998c79e6a6","b5fef1c8afd673e892f496e2f8e863d56ea73aefe443760ebda187350c19ab56","414565b42386217ff4a475ad62962a4714de8c91a37124945af0f691b8e45bca","12ea1124bcaa69400727b38aa3ba6d739f6ef52cd5b66fb1bf899b7590a30e95","fc24c601300c3d48633e8ef0c9ece6bf936a1c34978c41a65f91e6ca556fc296","25685bf0aef3c091e0e54b3d030da30b52b167bf0aac059ad44fa0a784c34aba","4383132ad02f4185fa0a03a84c7ec2a6302d05c6d305fef680902f81dff53c6a"]
ZIP_SHAS={"NAJ":"dd7e35494898f5a3dae1c9cff1a05627c2fe4ca530ebea0434c67f8f356320f4",
 "WASEDA":"8bd5928c12df7f04900574b2bc610aa2ac31ed1c417d314a6854a484336070cc"}
JPEG_SHAS={"NAJ":"23814245c0e7952a4d8581068d23448e285cd14b145b8824c8bfa9aeb6501884",
 "WASEDA":"acf08f57fcd82d35f6b2b3359449dd72def4b7124f9a25412bbec3812bc96bb7"}
EXPECTED_LABELS={
 "SOLAR_TITLE":"大陽冬至前後二象盈初縮末限",
 "DAY_INDEX_JIRI":"積日",
 "INITIAL_DAY_CHURI":"初日",
 "TECHNICAL_FIELD_RUBRIC":"行度 / 盈縮積 / 盈縮加分 / 日差加一秒八十六少"}

def load(path):
 return json.loads((ROOT/path).read_text(encoding="utf-8"))

def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CG-DIRECT-TWO-FIRSTPARTY-SOLAR-HEADER-DAYINDEX-AND-OBSTRUCTION-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and "NO_OCR" in e["evidence_grade"]
 assert set(e["sources"])=={"NAJ","WASEDA"}
 assert e["sources"]["NAJ"]["holding"]=="NAJ-282-0006-PHYSICAL51"
 assert e["sources"]["WASEDA"]["holding"]=="WASEDA-RI06-02809-BOOK33"
 for name,doc in e["sources"].items():
  assert doc["archive_zip_sha256"]==ZIP_SHAS[name]
  assert doc["original_jpeg_sha256"]==JPEG_SHAS[name]
  assert doc["archive_artifact_id"]==({"NAJ":12258234108,"WASEDA":12342817907}[name])
  assert doc["archive_file"]==({"NAJ":"book51-full-leaf-016.jpg","WASEDA":"p21-xref64-1.jpg"}[name])
  assert doc["dimensions"]==({"NAJ":[3000,2215],"WASEDA":[2592,1728]}[name])
 rois=e["original_rgb_rois"]
 assert len(rois)==9
 assert [x["source"]+":"+x["key"] for x in rois]==ROI_KEYS
 assert [x["rgb_sha256"] for x in rois]==ROI_SHAS
 for x in rois:
  lft,top,right,bottom=x["bbox"]
  width,height=e["sources"][x["source"]]["dimensions"]
  assert 0<=lft<right<=width and 0<=top<bottom<=height
  if x["key"] in EXPECTED_LABELS:
   assert x["observed"]==EXPECTED_LABELS[x["key"]]
 assert rois[-1]["key"]=="INITIAL_DAY_VISIBLE_OVERLAY"
 assert rois[-1]["bbox"]==[720,465,1065,795]
 assert "partially obscured" in rois[-1]["observed"]
 o=e["observations"]
 assert o["two_original_title_observations"] is True
 assert o["both_printed_day_index_heading"]=="積日"
 assert o["both_printed_initial_day_heading"]=="初日"
 assert o["technical_field_rubric_distinct_from_day_index"]==["行度","盈縮積","盈縮加分","日差加一秒八十六少"]
 assert o["waseda_original_visible_annotation_occlusion"] is True
 assert o["annotation_origin_or_date"]=="UNBOUND"
 assert o["full_initial_row_pixel_complete_in_waseda"]=="NOT_PROVEN"
 assert o["same_historical_mechanical_column_layout_between_copies"]=="UNPROVEN"
 assert o["cross_copy_column_mapping"]=="UNRESOLVED"
 assert o["source_original_EAST_ASIAN_DAY_LABEL_NOT_CUMULATIVE_FIELD"] is True
 t=e["scope_firewall"]
 assert t["new_direct_pixel_ROI_signatures"]==9 and t["open_research_issues"]==11 and t["deterministic_product"]=="CLOSED"
 for k in ("new_original_source_JPEG_objects","new_physical_witnesses","new_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_independent_stemmatic_votes","algorithm_reopens"):
  assert t[k]==0
 a=s["historical_audit"]
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 assert a["row_count"]==a["audited_row_count"]==222
 assert a["external_source_registry_total_unique_count"]==a["external_source_registry_root_count"]+a["external_source_registry_extension_count"]
 assert any(x.startswith("13CG ") for x in a["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(a["current_focus"])
 q=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert q["status"]=="OPEN" and E in q["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-INITIAL-TABLE-13CG" for x in q["history"])
 assert any(x["id"]=="OMISSIONS-13CG-SOURCE-HEADER-20261022" for x in l["checkpoint_log"])
 assert len([x for x in l["issues"] if x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
 return True

def replay(e,source,path):
 from PIL import Image
 b=Path(path).read_bytes()
 d=e["sources"][source]
 assert hashlib.sha256(b).hexdigest()==d["archive_zip_sha256"]
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  assert z.testzip() is None
  src=z.read(d["archive_file"])
 assert hashlib.sha256(src).hexdigest()==d["original_jpeg_sha256"]
 im=Image.open(io.BytesIO(src)).convert("RGB")
 assert list(im.size)==d["dimensions"]
 for x in e["original_rgb_rois"]:
  if x["source"]==source:
   actual=hashlib.sha256(im.crop(tuple(x["bbox"])).tobytes()).hexdigest()
   assert actual==x["rgb_sha256"],(source,x["key"],actual)
 return True

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--naj-zip");p.add_argument("--waseda-zip");args=p.parse_args()
 e,s,l=load(E),load(S),load(L)
 assert check(e,s,l)
 if bool(args.naj_zip)!=bool(args.waseda_zip):p.error("both firstparty original archive ZIPs required")
 if args.naj_zip:replay(e,"NAJ",args.naj_zip);replay(e,"WASEDA",args.waseda_zip)
 print("TIANWEN_13CG_TWO_FIRSTPARTY_ORIGINAL_SOLAR_HEADERS=PASS")

#!/usr/bin/env python3
"""13CH — original-source photographed D01–D20 heading atlas, zero field-identity claims."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CH-GORYEOSA-TWO-HOLDING-D01-D20-ORIGINAL-HEADING-ATLAS-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
KEYS=["N16","N17","N18","W21","W22","W23"]
CENTERS={"N16":[1300,1140,970,802,632,470],"N17":[2400,2240,2070,1900,1740,1300,1140,970,800,635,485],"N18":[2410,2240,2070],"W21":[685,550],"W22":[2130,1960,1790,1630,1480,1060,880,720,550],"W23":[2110,1950,1790,1625,1460,1065,900,730,550]}
DAY_RANGES={"N16":(1,6),"N17":(7,17),"N18":(18,20),"W21":(1,2),"W22":(3,11),"W23":(12,20)}
ORIGINAL_JPEG_SHA={"N16":"23814245c0e7952a4d8581068d23448e285cd14b145b8824c8bfa9aeb6501884","N17":"8362e8a2b8ddf5f36408d4450a81ebad2d9548b32f49dbe37e01493592b7c3e9","N18":"88cecf62c8cd0dd623199eb06e3044efbe61771c1ffe058b8e7a87cc2f8f88cc","W21":"acf08f57fcd82d35f6b2b3359449dd72def4b7124f9a25412bbec3812bc96bb7","W22":"4dbfc14caef81f63566d40db6f57fd73e23cbd1fd2cb627ee88def02ae98901d","W23":"388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"}
ORIGINAL_ZIP_SHA={"N16":"dd7e35494898f5a3dae1c9cff1a05627c2fe4ca530ebea0434c67f8f356320f4","N17":"dd7e35494898f5a3dae1c9cff1a05627c2fe4ca530ebea0434c67f8f356320f4","N18":"dd7e35494898f5a3dae1c9cff1a05627c2fe4ca530ebea0434c67f8f356320f4","W21":"8bd5928c12df7f04900574b2bc610aa2ac31ed1c417d314a6854a484336070cc","W22":"8bd5928c12df7f04900574b2bc610aa2ac31ed1c417d314a6854a484336070cc","W23":"41863a3d931122d53cce3bcdd59af1828eb41cc7efbab53b32ec738273a9306c"}
GROUP_SHA={"N16":"e9d737abf9d56d87e83369ac98b792e26e9c16c0a8bb9790dfd9212f6de55623","N17":"1f8f27d6564eedf51a90a1ec0c9de04cd4a5ef4184c6fd4f3446875392c311ea","N18":"567113d9ffc38e08ff1a65ba3f650da123f357cc1da4ef99f2dc4312f0372ac1","W21":"23444f81b4c6d5237dca2eb910cd43c3a639cf9aa0bb44040d3f7922b006ad8e","W22":"beccda957112eb5ef98f8c4adc16c81fbb8fa3851254fa4c44ae3fdd5c724915","W23":"669c0c0a9fbf71f366638bf9314274b0af8fca075ae4b6235dd2e0e796b7c019"}
WHOLE_SHA="ab05ae2688823d81a61ae34dc567e4c1a284252313bd738aa97703d47c3fcacc"
CHINESE=["","一","二","三","四","五","六","七","八","九","十","十一","十二","十三","十四","十五","十六","十七","十八","十九","二十"]
TRANSITIONS=[{"holding":"NAJ","from_photo":"N16","from_day":6,"to_photo":"N17","to_day":7,"kind":"NEXT_DIGITAL_CANVAS"},{"holding":"NAJ","from_photo":"N17","from_day":11,"to_photo":"N17","to_day":12,"kind":"WITHIN_SAME_PHOTO_OVER_GUTTER"},{"holding":"NAJ","from_photo":"N17","from_day":17,"to_photo":"N18","to_day":18,"kind":"NEXT_DIGITAL_CANVAS"},{"holding":"WASEDA","from_photo":"W21","from_day":2,"to_photo":"W22","to_day":3,"kind":"NEXT_PDF_PAGE"},{"holding":"WASEDA","from_photo":"W22","from_day":7,"to_photo":"W22","to_day":8,"kind":"WITHIN_SAME_PHOTO_OVER_GUTTER"},{"holding":"WASEDA","from_photo":"W22","from_day":11,"to_photo":"W23","to_day":12,"kind":"NEXT_PDF_PAGE"},{"holding":"WASEDA","from_photo":"W23","from_day":16,"to_photo":"W23","to_day":17,"kind":"WITHIN_SAME_PHOTO_OVER_GUTTER"}]

def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))

def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CH-TWO-HOLDING-TWENTY-CONSECUTIVE-PRINTED-DAY-HEADING-ORIGINAL-ATLAS-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and "NO_OCR" in e["evidence_grade"]
 assert e["photo_order"]==KEYS and set(e["photos"])==set(KEYS)
 assert e["photo_transitions"]==TRANSITIONS
 assert e["holdings"]==["NAJ-282-0006-PHYSICAL51","WASEDA-RI06-02809-BOOK33"]
 assert e["photographic_gutter_x"]=={"NAJ":1500,"WASEDA":1300}
 all_hashes=[]; holder_days={"NAJ":[],"WASEDA":[]};source_ids=set()
 for key in KEYS:
  p=e["photos"][key]
  holder="NAJ" if key.startswith("N") else "WASEDA"
  assert p["holding"]==holder
  assert p["original_jpeg_sha256"]==ORIGINAL_JPEG_SHA[key]
  assert p["archive_zip_sha256"]==ORIGINAL_ZIP_SHA[key]
  assert p["source_dimensions"]==([3000,2215] if holder=="NAJ" else [2592,1728])
  assert p["source_photographic_number"]==int(key[1:])
  assert p["archive_artifact_id"]==({"N16":12258234108,"N17":12258234108,"N18":12258234108,"W21":12342817907,"W22":12342817907,"W23":12340588249}[key])
  assert p["archive_original_name"]==({"N16":"book51-full-leaf-016.jpg","N17":"book51-full-leaf-017.jpg","N18":"book51-full-leaf-018.jpg","W21":"p21-xref64-1.jpg","W22":"p22-xref67-1.jpg","W23":"original-source.jpg"}[key])
  start,end=DAY_RANGES[key]
  assert (p["printed_day_first"],p["printed_day_last"])==(start,end)
  rows=p["day_header_rois"];assert len(rows)==end-start+1==len(CENTERS[key])
  for row,day,center in zip(rows,range(start,end+1),CENTERS[key]):
   bbox=[center-78,450 if holder=="NAJ" else 315,center+78,820 if holder=="NAJ" else 670]
   assert row["day"]==day and row["literal"]==CHINESE[day]+"日"
   assert row["bbox"]==bbox
   assert row["leaf"]==("RIGHT" if center>e["photographic_gutter_x"][holder] else "LEFT")
   assert len(row["rgb_sha256"])==64 and all(c in "0123456789abcdef" for c in row["rgb_sha256"])
   all_hashes.append(row["rgb_sha256"]);holder_days[holder].append(day)
  group=hashlib.sha256("".join(row["rgb_sha256"] for row in rows).encode("ascii")).hexdigest()
  assert group==GROUP_SHA[key],(key,"ROI signature group changed")
  source_ids.add(p["original_jpeg_sha256"])
 assert hashlib.sha256("".join(all_hashes).encode("ascii")).hexdigest()==WHOLE_SHA
 assert all(holder_days[x]==list(range(1,21)) for x in holder_days)
 assert len(source_ids)==6
 assert e["first_twenty_day_heading_coverage"]=={
  "NAJ":"D01..D20","WASEDA":"D01..D20",
  "each_holding_all_days_1_through_20_once":True,"roi_count":40,"source_jpeg_count":6,"archival_zip_count":3,"physical_holding_count":2}
 b=e["interpretation_boundary"]
 assert b["original_visible_day_heading_is_direct_source_witness"] is True
 assert b["source_local_numeric_row_column_assignment"]=="NOT_ADJUDICATED"
 assert b["NAJ_D17_7570_technical_yingsuoji"]=="UNBOUND"
 assert b["WASEDA_D16_original_same_day_yingsuoji"]=="UNBOUND"
 assert b["global_day_shift_between_copies"]=="UNPROVEN"
 assert b["NAJ_WASEDA_independent_textual_stemma"]=="UNPROVEN"
 assert b["G893_shao_wei_Ming1569_unit_identity"]=="UNPROVEN"
 assert b["no_inference_from_photo_gutter_to_calendar_day_mechanics"] is True
 t=e["source_grade_firewall"]
 assert t["reused_official_source_jpeg_objects"]==6 and t["new_native_RGB_crop_SHA_bindings"]==40
 assert t["open_research_risks"]==11 and t["product"]=="CLOSED"
 for k in ("new_provider_jpeg_downloads","new_physical_historical_witnesses","new_external_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_stemmatic_votes","algorithm_reopens"):
  assert t[k]==0
 a=s["historical_audit"]
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["invariants"]["algorithm_reopen_count"]==0
 assert a["row_count"]==a["audited_row_count"]==222
 assert a["external_source_registry_total_unique_count"]==754
 assert any(x.startswith("13CH ") for x in a["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(a["current_focus"])
 issue=next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-ORIGINAL-FIRST20-13CH" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CH-FIRST20-SOURCEHEADINGS-20261022" for x in l["checkpoint_log"])
 assert len([x for x in l["issues"] if x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
 return True

def replay_original_zip_sources(e,archives):
 from PIL import Image
 for key in KEYS:
  p=e["photos"][key]
  zipdata=Path(archives[{"N16":"NAJ","N17":"NAJ","N18":"NAJ","W21":"W21","W22":"W21","W23":"W23"}[key]]).read_bytes()
  assert hashlib.sha256(zipdata).hexdigest()==p["archive_zip_sha256"]
  with zipfile.ZipFile(io.BytesIO(zipdata)) as z:
   assert z.testzip() is None
   b=z.read(p["archive_original_name"])
  assert hashlib.sha256(b).hexdigest()==p["original_jpeg_sha256"]
  im=Image.open(io.BytesIO(b)).convert("RGB")
  assert list(im.size)==p["source_dimensions"]
  for row in p["day_header_rois"]:
   actual=hashlib.sha256(im.crop(tuple(row["bbox"])).tobytes()).hexdigest()
   assert actual==row["rgb_sha256"],(key,row["day"],actual)
 return True

if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--naj-zip");parser.add_argument("--waseda21-zip");parser.add_argument("--waseda23-zip")
 args=parser.parse_args();e=load(E);assert check(e,load(S),load(L))
 supplied=[args.naj_zip,args.waseda21_zip,args.waseda23_zip]
 if any(supplied):
  if not all(supplied):parser.error("all three previously SHA-bound original ZIPs required")
  assert replay_original_zip_sources(e,{"NAJ":args.naj_zip,"W21":args.waseda21_zip,"W23":args.waseda23_zip})
 print("TIANWEN_13CH_D01_D20_TWO_HOLDING_ORIGINAL_ATLAS=PASS")

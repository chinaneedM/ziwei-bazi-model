#!/usr/bin/env python3
"""13EG independent source-original cross-folio day-heading boundary controls."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EG-NCL03130-SOLAR-FOLIO-DAY-BOUNDARIES-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json";DZ="docs/research/TIANWEN-13DZ-NCL03130-CORRECT-SOLAR-D28-ORIGINAL-P76-LOCATOR-R1.json";EF="docs/research/TIANWEN-13EF-NCL03130-SOLAR-P73-TECHNICAL-HEADINGS-R1.json";EE="docs/research/TIANWEN-13EE-NCL03130-SOLAR-SAME-COLUMN-THREE-FOLIO-R1.json"
EXPECTED_HEADINGS=[(73,0,"初日",3,"三日"),(74,4,"四日",14,"十四日"),(75,15,"十五日",25,"二十五日"),(76,26,"二十六日",36,"三十六日"),(77,37,"三十七日",47,"四十七日")]
EXPECTED_ROI_SHA=[["982ccbbb8d159bc27ece9bf4ee3f456985c250d02238a5e8b6bdaf4ae7583f1c","4eea9e732e71bc9c83d13aeb409e416dc9b05ce5dba5f2c5be72688347fddee2"],["dac2d4865d428da1a875428c6542a24b5192ac05b0bcb49799d6ed625b23bb38","edd452643cfcd1b08d3dba1054c395bca259b5a3144701e7e78d5843c6ff7692"],["8151a9a612353a2f25721fe8305f36d665647ef28277b39ecdefa793197e8afe","3f0f52ad51f6e7d873bfb023a37d44b2ae73c9215709e8806bcf327e440c5856"],["9852a843d4b59510f751cdcac4700f905538cad12cea413cfefd8d58fcbdc5de","505a5e9209d20b6771f86691d7134a42a62fc5b3d334c4ed5222a795e8d25ff1"],["0d51b3c27299920a8d71fdb1298c5ea4e29a9cf9f0d4ced0b9efdea0a9d7bba8","c053c3b770267954127650548c27e8fea08fd05169bab472457fbd9410b09684"]]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e,s,l,dz,ef,ee):
 assert e["schema"]=="TIANWEN-13EG-NCL03130-SOLAR-FOLIO-DAY-BOUNDARIES-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["kind"]=="DIRECT_SAME_DIGITAL_SOURCE_PRINTED_DAY_BOUNDARY_CONTINUITY_ONLY"
 src=e["source"]
 assert src["pdf_sha256"]==dz["source"]["source_sha256"]==ef["source"]["pdf_sha256"]==ee["source"]["pdf_sha256"]
 assert src["archive_workflow_run"]==ef["source"]["original_archive_run"] and src["archive_artifact_id"]==ef["source"]["original_archive_artifact_id"]
 assert src["ocr_used"] is False and src["physical_copy"]==src["qing_vs_1905_leaf_hand"]=="UNBOUND"
 pp=e["pages"];assert len(pp)==5
 anchors=dz["original_page_register"]
 original={z["page"]:z for z in anchors}
 for i,p in enumerate(pp):
  reg=original[p["pdf_page"]]
  assert p["png_size"]==reg["size"] and p["png_sha256"]==reg["png_sha256"] and p["rgb_sha256"]==reg["rgb_sha256"]
  hd=p["boundaries"];assert len(hd)==2
  d0,o0,g0,d1,o1=EXPECTED_HEADINGS[i]
  assert (p["pdf_page"],hd[0]["printed_ordinal"],hd[0]["source_literal"],hd[1]["printed_ordinal"],hd[1]["source_literal"])==(d0,o0,g0,d1,o1)
  for j,z in enumerate(hd):
   x=317 if p["pdf_page"]==73 and j==0 else (885 if p["pdf_page"] in (74,75) else 905) if j==0 else 65
   assert z["bbox"]==[x,150,x+66,300] and z["roi_rgb_sha256"]==EXPECTED_ROI_SHA[i][j]
   assert z["read_grade"]=="DIRECT_ORIGINAL_HEADING_BOUNDED_NOT_COMPLETE_PAGE_TRANSCRIPTION"
 assert pp[0]["png_sha256"]==ef["source"]["original_page"]["png_sha256"]
 for p in pp[2:]:
  anchor=next(x for x in ee["pages"] if x["pdf_page"]==p["pdf_page"])
  assert p["png_sha256"]==anchor["png_sha256"] and p["rgb_sha256"]==anchor["rgb_sha256"]
 pairs=e["boundary_pairs"]
 assert [(x["from_page"],x["from_day"],x["to_page"],x["to_day"]) for x in pairs]==[(73,3,74,4),(74,14,75,15),(75,25,76,26),(76,36,77,37)]
 assert all(z["same_source_original"] is True and z["printed_day_difference"]==1 and z["numeric_field_transfer_claim"] is False for z in pairs)
 c=e["conclusion"]
 assert c["visible_source_heading_anchors"]==10 and c["visible_page_crossing_pairs"]==4 and c["source_local_boundary_day_sequence_positive"] is True
 assert c["first_source_heading"]=="初日" and c["last_source_heading"]=="四十七日"
 assert c["all_intermediate_day_numeric_fields_transcribed"] is False and c["all_intermediate_day_headings_exhaustively_read"] is False
 assert c["source_local_any_global_day_offset_rule"]=="UNPROVEN" and c["cross_page_technical_lane_identity"]=="UNRESOLVED" and c["cross_page_arithmetic_formula"]=="UNPROVEN"
 assert c["p73_technical_original_labels"]==ef["positive_source_facts"]["visible_original_technical_names"]==["行度","盈縮積","日差"]
 assert c["d30_original_literal"]==ee["observation"]["d30_existing_literal"]=="初度九十六二〇三" and c["d30_exact_numeric"] is None
 assert c["nonzero_new_independent_copies"] is False
 impact=e["impact"];assert (impact["original_source_pages_replayed"],impact["new_bounded_source_original_day_headings"],impact["new_boundary_pairs"],impact["risks_open_or_blocked"],impact["product"])==(5,10,4,11,"CLOSED")
 assert all(impact[k]==0 for k in ("new_independent_physical_witnesses","new_registry_sources","new_matrix_rows","new_transmission_nodes","new_transmission_edges","new_alternative_numeric_assignments","algorithm_reopens","risks_closed"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(z.startswith("13EG NCL03130 SOURCE-LOCAL FIVE-FOLIO") for z in s["historical_audit"]["current_focus"])
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith("13EG CURRENT ACTION")
 assert all(x in issue["next_action"] for x in ("D30","行度","盈縮積","日差","3→4","36→37"))
 assert set([E,E.replace(".json",".md")]).issubset(set(issue["source_refs"]))
 h=issue["history"][-1];assert h["revision_id"]=="TW-OPEN-0005-13EG-FIVE-FOLIO-BOUNDARY-CONTINUITY-20261023"
 assert h["previous_next_action"].startswith("13EF CURRENT ACTION") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert set([E,E.replace(".json",".md"),EF,EE]).issubset(set(h["evidence_refs"]))
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,directory):
 from PIL import Image
 root=Path(directory)
 for page in e["pages"]:
  f=root/f'original-p{page["pdf_page"]:03d}.png'
  assert hashlib.sha256(f.read_bytes()).hexdigest()==page["png_sha256"]
  with Image.open(f) as im:rgb=im.convert("RGB")
  assert list(rgb.size)==page["png_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==page["rgb_sha256"]
  for heading in page["boundaries"]:
   x0,y0,x1,y1=heading["bbox"]
   assert 0<=x0<x1<=rgb.width and 0<=y0<y1<=rgb.height
   assert hashlib.sha256(rgb.crop((x0,y0,x1,y1)).tobytes()).hexdigest()==heading["roi_rgb_sha256"],(page["pdf_page"],heading["printed_ordinal"])
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-dir");args=ap.parse_args()
 e=read(E);assert check(e,read(S),read(L),read(DZ),read(EF),read(EE))
 if args.source_dir:assert replay(e,args.source_dir)
 print("13EG_PASS FIVE_FOLIO_ORIGINAL_BOUNDARY_HEADINGS_0_47 D30_NUMERIC_UNRESOLVED")

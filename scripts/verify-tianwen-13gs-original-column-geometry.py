#!/usr/bin/env python3
"""13GS: exact-pixel heading alignment, lower tail and disjoint technical lane; NO glyph decoding."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13GS-NLC-P74-D14-GEOMETRIC-LANE-CONTINUITY-R1.json"
def digest(b): return hashlib.sha256(b).hexdigest()
def check(e,output_dir=None):
 s=e["source"];prior=json.loads((ROOT/s["prior_13gr"]).read_text(encoding="utf8"))
 gq=json.loads((ROOT/s["prior_13gq"]).read_text(encoding="utf8"))
 assert e["grade"]=="SOURCE_NATIVE_PIXEL_GEOMETRY_AND_LOWER_REGION_CAPTURE_WITHOUT_ANCIENT_LITERAL_CERTIFICATION"
 assert e["issue_id"]=="TW-OPEN-0005" and s["page"]==74 and s["xref"]==291
 assert s["original_pdf_sha256"]==prior["source"]["pdf_sha256"]
 assert s["origin"]==prior["source"]["origin_image"]
 assert s["origin_rgb_sha256"]==prior["source"]["origin_image_rgb_sha256"]
 frame=next(p for p in gq["context_panels"] if p["tag"]=="D14")
 assert frame["box"]==prior["source"]["origin_image_box"] and frame["image_file"]==s["origin"]
 im=Image.open(ROOT/s["origin"]).convert("RGB")
 assert digest(im.tobytes())==s["origin_rgb_sha256"]
 outer=frame["box"]; assert list(im.size)==[outer[2]-outer[0],outer[3]-outer[1]]
 prev={x["day"]:x for x in prior["same_original_positive_controls"]}
 n={x["role"]:x for x in prior["d14_nested_existing_source_rois"]}
 assert sorted(prev)==[12,13] and len(n)==3
 for day in (12,13):
  assert prev[day]["source_native_heading"][2]==prev[day]["source_native_numeric"][2]==e["prior_date_heading_numeric_right_edges"]["day"+str(day)]
 assert n["D14_PRINTED_DAY_HEADING"]["source_xyxy"][2]==n["D14_UNADJUDICATED_NUMBER_LANE"]["source_xyxy"][2]==e["prior_date_heading_numeric_right_edges"]["day14"]
 boxes={r["tag"]:r["box"] for r in e["rects"]}
 assert list(boxes)==["D14_PREVIOUS_CANDIDATE","D14_UNINSPECTED_LOWER_CONTINUATION","D14_FULL_VERTICAL_PROJECTION","D14_NEIGHBOR_TECHNICAL_COLUMN","D14_INTERCOLUMN_GUTTER"]
 a,b,full,neighbor,gutter=[boxes[k] for k in boxes]
 assert a==n["D14_UNADJUDICATED_NUMBER_LANE"]["source_xyxy"]
 assert b==[a[0],a[3],a[2],1060]
 assert full==[a[0],a[1],a[2],b[3]]
 assert neighbor==[180,545,230,1060] and gutter==[171,545,180,1060]
 assert a[2]==b[2]==full[2]==gutter[0] and gutter[2]==neighbor[0]
 assert neighbor[0]-full[2]==9
 assert e["evaluation"]["alignment"]=="NUMERIC_RIGHT_EDGE_EQUALS_SAME_DAY_HEADING_RIGHT_EDGE_FOR_D12_D13_D14_GEOMETRY_ONLY"
 for k in ("original_date_heading_literal","source_specific_field_identity","complete_day14_fourfen","day14_terminal_original_glyph","ancient_unit"):
  assert e["evaluation"][k] is None
 for k in ("old_nlc_D9","old_nlc_D14","old_nlc_D30","physical_leaf"): assert e["unresolved"][k] is None
 assert e["unresolved"]["old_D5"]=="〇/五_UNRESOLVED" and e["unresolved"]["G893_six"]=="OPEN" and e["unresolved"]["prior_13EI"]=="RETRACTED"
 assert e["counters"]=={"new_original_witnesses":0,"source_registry_additions":0,"genealogy_edges_added":0,"algorithms_reopened":0,"candidates_collapsed":0,"matrix":[222,222],"sources":761,"graph":[252,238],"issues":11,"chart":"CLOSED"}
 target=Path(output_dir) if output_dir else None
 if target:target.mkdir(parents=True,exist_ok=True)
 rois=[]
 for tag,box in boxes.items():
  assert outer[0]<=box[0]<box[2]<=outer[2] and outer[1]<=box[1]<box[3]<=outer[3]
  imcrop=im.crop((box[0]-outer[0],box[1]-outer[1],box[2]-outer[0],box[3]-outer[1]))
  h=digest(imcrop.tobytes())
  if tag=="D14_PREVIOUS_CANDIDATE": assert h==n["D14_UNADJUDICATED_NUMBER_LANE"]["rgb_sha256"]
  rois.append({"tag":tag,"xyxy":box,"rgb_sha256":h,"original_image_source":s["origin"],"interpretation":"PIXELS_ONLY_NOT_A_TRANSCRIPTION"})
  if target:imcrop.save(target/(tag.lower()+".png"))
 report={"result":"13GS_PASS_GEOMETRY_ONLY_ORIGINAL_VALUE_NULL","source_pdf_sha256":s["original_pdf_sha256"],"origin_rgb_sha256":s["origin_rgb_sha256"],"rects":rois,"original_glyph_certified":False,"new_physical_witnesses":0}
 if target:(target/"13gs-source-native-geometry-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 return report
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output-dir");a=p.parse_args()
 print(json.dumps(check(json.loads(E.read_text(encoding="utf8")),a.output_dir),ensure_ascii=False))

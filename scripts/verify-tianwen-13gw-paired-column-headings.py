#!/usr/bin/env python3
"""13GW: check original native-pixel provenance for visually proposed column headings,
not a machine transcription nor certification of any ancient number."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13GW-NLC-P74-D14-PAIR-PRINTED-COLUMN-HEADERS-R1.json"
def sh(b):return hashlib.sha256(b).hexdigest()
def check(e,outdir=None):
 assert e["schema"]=="TIANWEN-13GW-NLC-P74-D14-PAIR-PRINTED-COLUMN-HEADERS-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 s=e["source"];gs=json.loads((ROOT/s["prior_column_geometry"]).read_text(encoding="utf8"))
 gv=json.loads((ROOT/s["prior_date_label"]).read_text(encoding="utf8"))
 gq=json.loads((ROOT/s["prior_context"]).read_text(encoding="utf8"))
 assert s["source_pdf_sha256"]==gs["source"]["original_pdf_sha256"]==gv["original_source"]["pdf_sha256"]
 assert s["permanent_image"]==gs["source"]["origin"]==gv["original_source"]["permanent_context_path"]
 assert s["source_image_rgb_sha256"]==gs["source"]["origin_rgb_sha256"]==gv["original_source"]["permanent_context_rgb_sha256"]
 assert [s["pdf_page"],s["xref"]]==[74,291] and s["native_size"]==[1754,1173]
 source=next(x for x in gq["context_panels"] if x["tag"]=="D14")
 assert s["permanent_image_source_xyxy"]==source["box"]==[60,185,230,1080]
 img=Image.open(ROOT/s["permanent_image"]).convert("RGB")
 assert sh(img.tobytes())==s["source_image_rgb_sha256"]
 items=e["scope"];assert [r["role"] for r in items]==["PRINTED_FOURFEN_COLUMN_HEADING_PROVISIONAL","PRINTED_CHUDU_NEIGHBOR_HEADING_PROVISIONAL","INTERCOLUMN_SEPARATION_CONTROL"]
 assert [r["visible_label"] for r in items]==["四分","初度",None]
 assert [r["source_xyxy"] for r in items]==[[135,563,171,680],[180,545,230,680],[171,545,180,680]]
 for r in items:
  assert r["numeric_field_or_unit_certified"] is False
  assert r["text_grade"] in ("VISUAL_PROVISIONAL_SAME_SURROGATE","PIXEL_GUTTER_GEOMETRY_ONLY")
 a,b,g=[r["source_xyxy"] for r in items]
 assert a[2]==g[0] and g[2]==b[0] and b[0]-a[2]==9
 assert a[0]==gs["rects"][0]["box"][0] and a[2]==gs["rects"][0]["box"][2]
 assert b[0]==gs["rects"][3]["box"][0] and b[2]==gs["rects"][3]["box"][2]
 guard=e["inference_firewall"]
 for k in ("source_specific_day14_fourfen_field_bound","source_specific_day14_chudu_field_bound","d14_fourfen_complete_literal","d14_fourfen_terminal_original_glyph","old_nlc_d9","old_nlc_d30","original_ancient_unit","source_physical_folio","copying_layer"):assert guard[k] is None,k
 assert guard["printed_day_header"]=="十四日_SOURCE_SURROGATE_PROVISIONAL_13GV"
 assert guard["independent_physical_edition_proven"] is False
 assert guard["fourfen_chudu_are_mechanical_identical"] is False and guard["fourfen_chudu_relation_adjudicated"] is False
 assert guard["adjacent_columns_are_distinct_image_regions"] is True
 assert guard["old_nlc_day5"]=="〇/五_UNRESOLVED" and guard["g893_six"]=="OPEN" and guard["prior_13EI"]=="RETRACTED"
 assert guard["source_text_not_derived_from_ocr"] is True and guard["numerical_interpolation_prohibited"] is True
 assert e["counters"]=={"matrix":[222,222],"external_sources":761,"genealogy":[252,238],"open_issues":11,"chart":"CLOSED","new_independent_witnesses":0,"new_glyph_values":0,"algorithm_reopens":0,"candidate_collapses":0}
 assert gv["still_unresolved"]["same_day_fourfen_row"] is None
 out=Path(outdir) if outdir else None
 if out:out.mkdir(parents=True,exist_ok=True)
 base=s["permanent_image_source_xyxy"];report=[]
 for r in items:
  q=r["source_xyxy"]
  assert base[0]<=q[0]<q[2]<=base[2] and base[1]<=q[1]<q[3]<=base[3]
  crop=img.crop((q[0]-base[0],q[1]-base[1],q[2]-base[0],q[3]-base[1]))
  report.append({"role":r["role"],"source_native_box":q,"rgb_sha256":sh(crop.tobytes()),"visual_label":r["visible_label"],"interpretation":"HUMAN_PROVISIONAL_LABEL_NOT_MACHINE_CERTIFIED"})
  if out:crop.save(out/(r["role"].lower()+".png"))
 results={"result":"13GW_SOURCE_BOUND_PRINTED_HEADERS_ONLY_NUMERICAL_VALUE_NULL","original_image_sha256":s["source_image_rgb_sha256"],"crops":report,"certified_numeric_rows":0,"new_physical_sources":0}
 if out:(out/"13gw-native-heading-pixels.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 return results
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--output-dir");opt=ap.parse_args()
 print(json.dumps(check(json.loads(E.read_text(encoding="utf8")),opt.output_dir),ensure_ascii=False))

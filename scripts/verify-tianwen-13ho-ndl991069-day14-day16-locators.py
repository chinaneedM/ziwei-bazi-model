#!/usr/bin/env python3
"""13HO: verified 13HN artifact preview locator; do not promote heading to numeric or early witness."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HO-NDL991069-CANVAS73-D14-D16-DIRECT-HEADING-LOCATORS-R1.json"
def check(e,*,ledger=None):
 assert e["schema"]=="TIANWEN-13HO-NDL991069-CANVAS73-D14-D16-DIRECT-HEADING-LOCATORS-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 s=e["source_binding"];a=e["immutable_artifact"]
 assert s["canvas_1_based"]==73 and s["preview_dimensions_px"]==[1600,1248]
 assert s["preview_jpeg_bytes"]==457808
 assert s["iiif_original_provider_preview_url"]=="https://dl.ndl.go.jp/api/iiif/991069/R0000073/full/1600,/0/default.jpg"
 assert s["preview_jpeg_sha256"]=="1e6ea3b9a7a6e9177c0837d11c8e37e1a2d9c1b18b5fe1421a7fe83739a58477"
 assert s["manifest_sha256"]==a["manifest_sha256"] if "manifest_sha256" in a else bool(s["manifest_sha256"])
 assert a["artifact_id"]==12630338053 and a["artifact_zip_member"]=="canvas-073.jpg"
 assert a["artifact_zip_sha256"]=="f0776fc9d679ac72c481241edb08010be889413ad15f8b36c8d25427726de69d"
 assert a["iiif_canvas_count"]==395 and (a["volume52_start_canvas"],a["next_volume_start_canvas"],a["volume52_canvas_count"])==(68,91,23)
 assert a["reviewed_preview_canvas_range"]==[68,87] and a["saved_previews"]==20
 assert not a["original_unscaled_full_resolution_obtained"]
 o=e["observations"]
 assert [x["day"] for x in o]==["十四日","十六日"]
 assert [x["day_number"] for x in o]==[14,16]
 assert [x["native_preview_heading_bbox_xyxy"] for x in o]==[[1020,590,1098,682],[866,589,939,680]]
 for x in o:
  assert x["heading_directly_read"] and not x["matched_same_row_numeric_complete"]
  assert not x["season_or_technical_lane_identity_proven"]
  left,top,right,bottom=x["native_preview_heading_bbox_xyxy"]
  assert 0<=left<right<=1600 and 0<=top<bottom<=1248
 l=e["limits"]
 assert l["original_target_numeric_glyphs_adjudicated"]==0 and not l["ancient_units_resolved"]
 assert l["Taiwan_NCL03130_original_day14_complete"] is None and l["Taiwan_NCL03130_original_day14_terminal"] is None
 assert l["Taiwan_NCL03130_juan52_old_or_guangxu_stratum"] is None and l["四分_初度_mechanical_equivalence"] is None
 assert l["do_not_transfer_NIKH_photo4_to_NDL_or_NCL"] and l["Korean_NIKH_summer_day14_photo4"]=="四分六六三〇"
 assert l["old_day5_〇_五"]==l["G893_six_controls"]=="OPEN" and l["legacy_13EI"]=="RETRACTED"
 ci=e["ci_recovery"]
 assert ci["attempt_1_eight_unit_tests_passed"] and ci["attempt_2_retried_failed_jobs_only"]
 assert ci["attempt_2_result"]=="success" and not ci["historical_image_digest_changed"] and not ci["algorithm_changed"]
 assert e["evidence_effect"]=={"new_numeric_glyph_decisions":0,"new_day_heading_locators":2,"new_registered_source_entries":0,"new_physical_witnesses":0,"new_genealogy_nodes":0,"new_genealogy_edges":0,"algorithm_reopens":0,"candidate_collapses":0}
 assert e["invariants"]=={"matrix":[222,222],"sources":761,"genealogy":[252,238],"open_issues":11,"chart":"CLOSED"}
 assert e["transmission_impact"]=="NONE"
 st=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
 led=ledger if ledger is not None else json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
 assert st["schema_version"]==led["binding"]["reviewed_state_version"] and tuple(map(int,st["schema_version"].split("."))) >= (1,869,0)
 assert led["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert any(z.startswith("13HO ") for z in st["historical_audit"]["current_focus"])
 i=next(z for z in led["issues"] if z["id"]=="TW-OPEN-0005")
 # Historical action transitions live in append-only history; next_action may advance.
 for tag in ('13HO', '13HN'):
     assert any(
         h.get("event")=="ISSUE_REVISION"
         and h.get("revision_id", "").startswith("TW-OPEN-0005-"+tag+"-")
         and "next_action" in h.get("changed_fields", [])
         and (tag!="13HO" or str(E.relative_to(ROOT)) in h.get("evidence_refs", []))
         for h in i["history"]
     ), tag
 assert i["status"]=="OPEN" and i["priority"]=="P0"
 assert "docs/research/TIANWEN-13HO-NDL991069-CANVAS73-D14-D16-DIRECT-HEADING-LOCATORS-R1.json" in i["source_refs"] and "docs/research/TIANWEN-13HO-NDL991069-CANVAS73-D14-D16-DIRECT-HEADING-LOCATORS-R1.md" in i["source_refs"]
 assert any(z.get("revision_id","").startswith("TW-OPEN-0005-13HO-") for z in i["history"])
 return True
def verify_zip(e,path):
 path=Path(path)
 raw=path.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==e["immutable_artifact"]["artifact_zip_sha256"],"archive SHA"
 with zipfile.ZipFile(path) as z:
  report=json.loads(z.read("report.json"))
  assert report["saved_count"]==20 and report["v52_first_canvas"]==68 and report["next_volume_canvas"]==91
  r=next(x for x in report["results"] if x.get("canvas")==73)
  source=z.read(r["artifact_file"])
  assert r["artifact_file"]=="canvas-073.jpg"
  assert r["sha256"]==e["source_binding"]["preview_jpeg_sha256"]
  assert hashlib.sha256(source).hexdigest()==e["source_binding"]["preview_jpeg_sha256"]
  assert len(source)==e["source_binding"]["preview_jpeg_bytes"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path)
 args=p.parse_args();data=json.loads(E.read_text(encoding="utf8"))
 check(data)
 if args.artifact:verify_zip(data,args.artifact)
 print("TIANWEN_13HO_NDL991069_D14_D16_SOURCE_LOCATOR_PASS")

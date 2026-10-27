#!/usr/bin/env python3
"""13HB: source-native NIKH image4 D14 photo glyph with NCL original kept NULL."""
import argparse,hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HB-NIKH-JUAN52-GALLERY04-D14-DIRECT-PHOTO-GLYPHS-R1.json"
def sh(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()
def check(e,image_path=None):
 assert e["schema"]=="TIANWEN-13HB-NIKH-JUAN52-GALLERY04-D14-DIRECT-PHOTO-GLYPHS-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="FIRSTPARTY_SAVED_HISTORICAL_SOURCE_PHOTO_BOUNDED_DIRECT_GLYPH_POSITIVE_NOT_PHYSICAL_EDITION_IDENTITY"
 pri={}
 for r in e["immutable_sources"]:
  raw=(ROOT/r["file"]).read_bytes()
  assert blob(raw)==r["git_blob_sha"]
  pri[Path(r["file"]).name[8:12]]=json.loads(raw)
 assert sorted(pri)==["13FG","13GZ","13HA"]
 s=e["source"];art=e["artifact"]
 assert [art["original_run_id"],art["artifact_id"]]==[40057001564,12545602956]
 assert art["inside_jpeg"]=="target-source-viewer-04.jpg"
 assert art["archive_recovered_this_review"] and art["archive_jpeg_sha_verified"] and art["previous_13FF_source_emitted_not_guessed"]
 assert s["gallery_viewer_index"]==4 and s["source_emitted_file"]=="kr/052/kr_052_1058.jpg"
 assert s["source_emitted_download_url"]=="https://db.history.go.kr/common/imageProxy.do?filePath=/kr/052/kr_052_1058.jpg&mode=download"
 assert [s["jpeg_bytes"],s["size_px"]]==[247816,[1032,2000]]
 assert s["jpeg_sha256"]==pri["13FG"]["source_image_recovery"]["captured_modern_index_to_exact_sha256"]["4"]
 assert s["rgb_sha256"]=="0fe484d4e7d340a6760d4274d9587bf01acef6f504be1fb5bd3135e225628c2e"
 assert s["one_source_original_surrogate"] is True and s["physical_folio_or_book_ordinal"] is None
 assert s["physical_edition_and_print_stratum_unbound"] is True
 assert s["not_new_independent_authenticated_physical_copy"] is True
 v=e["direct_visual_glyph_reviews"];assert [x["tag"] for x in v]==["SAME_IMAGE_DAY14_HEADING","SAME_IMAGE_DAY14_SUMMER_FOURFEN"]
 assert [x["xyxy"] for x in v]==[[110,260,245,505],[184,697,260,1260]]
 assert [x["rgb_sha256"] for x in v]==["aa06b6e4145bfdc02a7f5868b3c3c61b796c326eb6369a3eeac63385ca20558a","71a034f1c129d7bfd36e06288b7527b3ca6f1661eee02039b31ace5361f9b5e6"]
 assert [x["visible_literal"] for x in v]==["十四日","四分六六三〇"]
 assert v[1]["terminal_glyph"]=="〇"
 assert all(x["grade"]=="SOURCE_NATIVE_RGB_HUMAN_DIRECT_REVIEW_NO_OCR" for x in v)
 x=e["crosscheck"]
 assert x["first_party_modern_received_summer_D14"]==pri["13HA"]["seasonal_tables"][1]["day14"]["first_field"]==v[1]["visible_literal"]
 assert x["winter_received_D14"]==pri["13HA"]["seasonal_tables"][0]["day14"]["first_field"]=="五分一九九〇"
 assert x["direct_source_photo_agrees_with_received_this_copy"] is True and x["received_text_not_independent_photo_vote"] is True
 assert x["seasonal_key"]=="SUMMER_EARLY_SUO_LATE_YING" and x["winter_not_same_target"] is True
 b=e["boundaries"]
 for key in ("NCL_03130_p74_D14_original_complete_literal","NCL_03130_p74_D14_terminal_glyph","NCL_old_D9","NCL_old_D30","ancient_unit","fourfen_chudu_mechanical_identity"):
  assert b[key] is None,key
 assert b["NIKH_photo_D14_source_specific_positive"] is True
 assert b["NLC_vs_NIKH_independent_physical_copy_certified"] is False and b["inheritance_direct_copy_proven"] is False
 assert b["old_D5"]=="〇/五_UNRESOLVED" and b["G893_six"]=="OPEN" and b["prior_13EI"]=="RETRACTED"
 assert b["chart"]=="CLOSED"
 for k in ("new_physical_witnesses","source_registry_delta","graph_edge_delta","algorithm_reopens","candidate_collapses"): assert b[k]==0,k
 assert e["counters"]=={"matrix":[222,222],"sources":761,"genealogy":[252,238],"open_issues":11}
 assert all(e["transmission_impact"][k]==[] for k in ("edges_supported","edges_revised","edges_rejected","non_edges_added"))
 if image_path:
  from PIL import Image
  data=Path(image_path).read_bytes()
  assert len(data)==s["jpeg_bytes"] and sh(data)==s["jpeg_sha256"]
  im=Image.open(image_path).convert("RGB")
  assert list(im.size)==s["size_px"] and sh(im.tobytes())==s["rgb_sha256"]
  for r in v:
   crop=im.crop(tuple(r["xyxy"]))
   assert sh(crop.tobytes())==r["rgb_sha256"],r["tag"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--image");a=p.parse_args()
 assert check(json.loads(E.read_text(encoding="utf8")),a.image)
 print("13HB_PASS_SAME_SOURCE_NIKH_PHOTO4_D14_ORIGINAL_LITERAL_NCL_REMAINS_NULL")

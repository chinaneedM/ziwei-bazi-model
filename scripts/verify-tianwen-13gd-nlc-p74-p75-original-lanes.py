#!/usr/bin/env python3
"""13GD source-native NLC p74/p75 D10..13,D15 positive; preserve D9,D14,D30 NULL."""
import argparse,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13GD-NLC-P74-P75-D10-D15-BOUNDED-ORIGINAL-LANES-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
FU=ROOT/"docs/research/TIANWEN-13FU-NLC-D16-DIRECT-FOURFEN-ORIGINAL-GLYPHS-R1.json"
GB=ROOT/"docs/research/TIANWEN-13GB-NLC-P75-D21-D25-CROSSPAGE-ORIGINAL-FEN-LANES-R1.json"
CN={c:i for i,c in enumerate("〇一二三四五六七八九")}
EXPECTED_ROWS=[{"day":10,"page":74,"source_heading":"十日","remainder":"五九八二","integer_grid":45982,"heading_rgb_sha256":"df6e6aaa55e81191beb637c1e143d6d048f4aa300f5713fb6f65c66e51374cb0","roi_rgb_sha256":"6eae89b1cb94d72f7dcbc9d2d9d6e7d7eae70ee7aaa03f3bd3987384b33ddca1"},{"day":11,"page":74,"source_heading":"十一日","remainder":"六一四四","integer_grid":46144,"heading_rgb_sha256":"2189d6a3a119341bc66a1d070b95bbfb6f6e06f3ccbb059d7dcb86def75ce914","roi_rgb_sha256":"4c95fdea7ec58a040067fdca2181834dc66cb0e6a7056c681d0260f68ef4f233"},{"day":12,"page":74,"source_heading":"十二日","remainder":"六三〇六","integer_grid":46306,"heading_rgb_sha256":"5ab0bc32439ef01110efd897c0232102df0a216d7af2d743ca2140fbc1e37abf","roi_rgb_sha256":"12264ba19e4710f6179c9dc08a5a50e3ae49ec40f9633e575569fd0a33ac4330"},{"day":13,"page":74,"source_heading":"十三日","remainder":"六四六八","integer_grid":46468,"heading_rgb_sha256":"a92b0a8c963244ca03a3be3d79d04c4be8ccdf8773d7bff9cc8768d867a524f0","roi_rgb_sha256":"9d6b26d3f36dfede1a0c1e070a22157387be48002c8bbd6d04ee94994320f7e5"},{"day":15,"page":75,"source_heading":"十五日","remainder":"六七九二","integer_grid":46792,"heading_rgb_sha256":"aa25c3d6f2372a3fac55da12741b0dd66d672e454bf69d79e2be09110285dc9f","roi_rgb_sha256":"e9c4039e0bcecd4926d33874f85d77e2df62f2ce23fc27213117d80c4d748044"}]
EXPECTED_SHA74="a3f597f96f494a5ee9a6d582850f0642035d858bcbc587abc6fac11853018a14"
EXPECTED_SHA75="059821b008f41c1cdf11bf0daab89de01b44dc5ffee1263e569decb567f76458"
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def check(e,l,s,fu,gb,source_p74=None,source_p75=None):
 assert e["schema"]=="TIANWEN-13GD-NLC-P74-P75-D10-D15-BOUNDED-ORIGINAL-LANES-R1" and e["issue_id"]=="TW-OPEN-0005"
 src=e["source"]
 assert src["artifact_id"]==12494518841 and src["new_physical_witnesses"]==0 and src["physical_copy_identity"] is None
 assert [x["png_sha256"] for x in src["original_page_images"]]==[EXPECTED_SHA74,EXPECTED_SHA75]
 assert src["original_page_images"][1]["png_sha256"]==fu["source"]["original_image_sha256"]==gb["source"]["png_sha256"]
 rows=e["positive_source_rows"];assert len(rows)==5 and [x["day"] for x in rows]==[10,11,12,13,15]
 for row,expected in zip(rows,EXPECTED_ROWS):
  for k,v in expected.items():assert row[k]==v
  assert row["prefix"]=="四" and row["integer_grid"]==40000+sum(CN[c]*10**(3-j) for j,c in enumerate(row["remainder"]))
  for k in ("heading_rgb_sha256","heading_png_sha256","roi_rgb_sha256","roi_png_sha256"):
   assert len(row[k])==64 and all(z in "0123456789abcdef" for z in row[k])
 c=e["cross_original"]
 assert c["p74_contiguous_days"]==[10,11,12,13] and c["p74_values"]==[x["integer_grid"] for x in rows[:4]]
 assert [b-a for a,b in zip(c["p74_values"],c["p74_values"][1:])]==c["p74_local_differences"]==[162]*3
 assert c["p75_day15_grid"]==rows[4]["integer_grid"]==46792
 assert c["p75_day16_already_verified"]==fu["original_field"]["complete_field_original_literal"]=="四分六九五四"
 assert c["p75_day16_grid"]-c["p75_day15_grid"]==c["p75_d15_d16_difference"]==162
 assert c["p74_to_p75_d13_d15_gap_day14_original"] is None and c["nlc_day9_original"] is None and c["nlc_day30_original"] is None
 assert c["do_not_interpolate_missing_days"] and c["integer_encoding_not_historical_unit"] and c["same_surrogate_not_independent_ancient_copy"]
 bounds=e["non_adjudicated_original_scopes"]
 assert [b["day"] for b in bounds]==[9,14] and all(b["complete_source_original_literal"] is None and b["field_identity_adjudicated"] is False for b in bounds)
 u=e["unresolved"]
 assert u["NLC_day9_exact_original"] is None and u["NLC_day14_exact_original"] is None and u["NLC_day30_exact_original"] is None and u["NLC_day30_original_field_roi"] is None
 assert u["historic_unit_equivalence"] is None and u["copy_edition_independence"] is None and u["source_historical_winner"] is None
 assert u["G893_six_direct_original_controls"]=="OPEN" and u["legacy_13EI"]=="RETRACTED"
 counts=e["counts"]
 assert [counts[x] for x in ("matrix_rows","matrix_audited","sources","graph_nodes","graph_edges","risk_issues_open_or_blocked")]==[222,222,761,252,238,11] and counts["product"]=="CLOSED"
 for k in ("algorithm_reopens","candidate_collapses","new_source_registry_entries","new_ancient_physical_witnesses","new_genealogy_nodes","new_genealogy_edges"):assert counts[k]==0
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 assert l["binding"]["reviewed_state_version"]==s["schema_version"] and s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(f.startswith("13GD ") for f in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert str(E.relative_to(ROOT)) in issue["source_refs"] and str(E.relative_to(ROOT)).replace(".json",".md") in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13GD-P74-P75-D10-D15-20261025" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13GD-P74-P75-D10-D15-20261025" for x in l["checkpoint_log"])
 if source_p74 or source_p75:
  from PIL import Image
  for page,img_file in ((74,source_p74),(75,source_p75)):
   if not img_file:continue
   meta=src["original_page_images"][0 if page==74 else 1]
   data=Path(img_file).read_bytes();assert hashlib.sha256(data).hexdigest()==meta["png_sha256"]
   img=Image.open(io.BytesIO(data)).convert("RGB")
   assert list(img.size)==meta["native_wh"] and hashlib.sha256(img.tobytes()).hexdigest()==meta["rgb_sha256"]
   scoped=[(x,"heading_","heading_") for x in rows if x["page"]==page]+[(x,"","") for x in rows if x["page"]==page]
   for item,source_prefix,digest_prefix in scoped:
    crop=img.crop(tuple(item[source_prefix+"roi_xyxy"]))
    assert hashlib.sha256(crop.tobytes()).hexdigest()==item[digest_prefix+"rgb_sha256"]
    buf=io.BytesIO();crop.save(buf,format="PNG")
    assert hashlib.sha256(buf.getvalue()).hexdigest()==item[digest_prefix+"png_sha256"]
   for b in bounds:
    if b["page"]!=page:continue
    for kp in ("source_heading_roi","candidate_roi"):
     crop=img.crop(tuple(b[kp+"_xyxy"]))
     assert hashlib.sha256(crop.tobytes()).hexdigest()==b[kp+"_rgb_sha256"]
     buf=io.BytesIO();crop.save(buf,format="PNG")
     assert hashlib.sha256(buf.getvalue()).hexdigest()==b[kp+"_png_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-p74");ap.add_argument("--source-p75");a=ap.parse_args()
 assert check(read(E),read(L),read(S),read(FU),read(GB),a.source_p74,a.source_p75)
 print("13GD_PASS_DIRECT_P74_P75_D10_D13_D15_D9_D14_D30_NULL")

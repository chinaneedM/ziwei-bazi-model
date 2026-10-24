#!/usr/bin/env python3
"""13GB direct-original NLC p75 day21..25 positive source with day26 crosspage; D30 NULL."""
import argparse, hashlib, io, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13GB-NLC-P75-D21-D25-CROSSPAGE-ORIGINAL-FEN-LANES-R1.json"
GA=ROOT/"docs/research/TIANWEN-13GA-NLC-P76-D26-D28-ORIGINAL-FEN-LANES-R1.json"
FU=ROOT/"docs/research/TIANWEN-13FU-NLC-D16-DIRECT-FOURFEN-ORIGINAL-GLYPHS-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
EXPECTED=json.loads("[{\"day\":21,\"source_heading\":\"二十一日\",\"prefix\":\"四\",\"remainder\":\"七七六四\",\"integer_grid\":47764,\"heading_roi_xyxy\":[403,159,466,303],\"heading_rgb_sha256\":\"a215c28e3d364548f435db74d56678d275b0b35501b7a5bf90f8ee4f84346c5e\",\"heading_png_sha256\":\"14ed1065b1436bfa8da480d8f67b4d3ea2de9abb0efe209bf2ce501cb3676432\",\"roi_xyxy\":[442,419,466,611],\"roi_rgb_sha256\":\"670726ce3523599a18770f186ea4e6dfbd10995f606600575e3914870a46d222\",\"roi_png_sha256\":\"deefbf87323c8f0bf5df2ad0cbef48ada60eda92a94098ed944561561e9e65e6\"},{\"day\":22,\"source_heading\":\"二十二日\",\"prefix\":\"四\",\"remainder\":\"七九二六\",\"integer_grid\":47926,\"heading_roi_xyxy\":[317,159,380,303],\"heading_rgb_sha256\":\"b236eaa3f03a2ca8c9f6aeef4deeb8266eb3603b7ea779290a96422e1fc8133f\",\"heading_png_sha256\":\"836241508b484af1e1e14137ae06e1bb662817b699472d361531922277b14f18\",\"roi_xyxy\":[356,419,380,611],\"roi_rgb_sha256\":\"0023bc8f360aaba3b3f71c130ebd4f04eaa8b43801fdf5702c5b4b1770a6c6a7\",\"roi_png_sha256\":\"66b7f25bccebdb899fae7835a0941178f3e813a5b75ded97f009228fe60043ac\"},{\"day\":23,\"source_heading\":\"二十三日\",\"prefix\":\"四\",\"remainder\":\"八〇八八\",\"integer_grid\":48088,\"heading_roi_xyxy\":[231,159,295,303],\"heading_rgb_sha256\":\"215b30c1b0b6b6f83cb47b45ca3e533c7150abd78fff51cab9df90b730db2880\",\"heading_png_sha256\":\"8d10657c60876eab88e4ee8ad077b365f7a2a6f785adaf50f32234dd6ef04b37\",\"roi_xyxy\":[270,419,295,611],\"roi_rgb_sha256\":\"02782494bc0337c8d25b47450ad530ba8ff63ae172242c1095dc19b626c5bfdf\",\"roi_png_sha256\":\"16c20c820a04e59ddff1c0c98d2f38caeb5686d5280a72cf05e8d4f124e2bd55\"},{\"day\":24,\"source_heading\":\"二十四日\",\"prefix\":\"四\",\"remainder\":\"八二五〇\",\"integer_grid\":48250,\"heading_roi_xyxy\":[145,159,210,303],\"heading_rgb_sha256\":\"e69470a705597db96bba6310535f70fa4bc3e4428dc31b32482e64e0258698df\",\"heading_png_sha256\":\"dd9105f138e6e43aa345fab65ebdb4abfce43eae752fa57bf76069c03cba50cb\",\"roi_xyxy\":[186,419,210,611],\"roi_rgb_sha256\":\"cde5bb08a21950cf85b5d40d71ca18239586247ce16f929d9fae0d4845c52ce7\",\"roi_png_sha256\":\"f04add3f196f5b20399b52a3b43d2f6edcb8e79aaec3831e855114db544fb0ac\"},{\"day\":25,\"source_heading\":\"二十五日\",\"prefix\":\"四\",\"remainder\":\"八四一二\",\"integer_grid\":48412,\"heading_roi_xyxy\":[60,159,127,303],\"heading_rgb_sha256\":\"64e966b3e3bbcf7a18f2b5b57bbcb07eecdd36cfe44f41850ae3dd1a7442954a\",\"heading_png_sha256\":\"8a8f30bb8edb91c3853f507d755c0b37e1d31c87f9d9a62247d4a580b44293aa\",\"roi_xyxy\":[101,419,127,611],\"roi_rgb_sha256\":\"09a423cf6612e41a543174588f8296c8e2e8bc74139b8d95515f2b675b933e99\",\"roi_png_sha256\":\"83bf3345b5e6d4cf945c5994bc2fb7efffd82ce47a448d160679f7defa94f4a2\"}]")
CN={c:i for i,c in enumerate("〇一二三四五六七八九")}
def read(path):return json.loads(path.read_text(encoding="utf-8"))
def check(e,ga,fu,ledger,state,source_image=None):
 assert e["schema"]=="TIANWEN-13GB-NLC-P75-D21-D25-CROSSPAGE-ORIGINAL-FEN-LANES-R1" and e["issue_id"]=="TW-OPEN-0005"
 src=e["source"]
 assert src["artifact_id"]==12494518841 and src["original_png"]=="original-p075.png" and src["pdf_page_one_based"]==75
 assert src["png_sha256"]==fu["source"]["original_image_sha256"]
 assert src["rgb_sha256"]==fu["source"]["native_rgb_sha256"] and src["native_wh"]==fu["source"]["native_rgb_size"]==[1305,878]
 assert src["physical_copy_identity"] is None and src["impression_date"] is None and src["no_new_physical_witnesses"] is True
 assert e["direct_original_rows"]==EXPECTED
 values=[]
 for row in EXPECTED:
  assert row["prefix"]=="四" and row["integer_grid"]==40000+sum(CN[c]*10**(3-i) for i,c in enumerate(row["remainder"]))
  values.append(row["integer_grid"])
 assert ga["direct_original_rows"][0]["day"]==26 and ga["direct_original_rows"][0]["integer_grid"]==48574
 x=e["cross_page"]
 assert x["page76_day26_source"]==str(GA.relative_to(ROOT))
 assert x["grid_21_to_26"]==values+[ga["direct_original_rows"][0]["integer_grid"]]
 assert [b-a for a,b in zip(x["grid_21_to_26"],x["grid_21_to_26"][1:])]==x["neighbor_differences"]==[162]*5
 assert x["series_gapped_at_original_day30"] and x["day30_original_lanes_can_not_be_interpolated"] and x["one_digital_surrogate_not_independent_witnesses"]
 u=e["unresolved"]
 assert u["NLC_day30_exact_original"] is None and u["NLC_day30_original_field_roi"] is None
 assert u["NLC_day9_fourfen"] is None and u["G893_six_direct_original_controls"]=="OPEN"
 assert u["historic_unit_equivalence"] is None and u["copy_edition_independence"] is None and u["source_historical_winner"] is None and u["legacy_13EI"]=="RETRACTED"
 assert e["counts"]["product"]=="CLOSED" and e["counts"]["risk_issues_open_or_blocked"]==11
 for k in ("algorithm_reopens","candidate_collapses","new_source_registry_entries","new_ancient_physical_witnesses","new_genealogy_nodes","new_genealogy_edges"):assert e["counts"][k]==0
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 assert ledger["binding"]["reviewed_state_version"]==state["schema_version"]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(f.startswith("13GB ") for f in state["historical_audit"]["current_focus"])
 issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["next_action"].startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert "13GA CURRENT ACTION:" in issue["next_action"] and "13FZ CURRENT ACTION:" in issue["next_action"]
 assert str(E.relative_to(ROOT)) in issue["source_refs"] and str(E.relative_to(ROOT)).replace(".json",".md") in issue["source_refs"]
 assert any(z.get("revision_id")=="TW-OPEN-0005-13GB-P75-D21-D25-20261025" for z in issue["history"])
 assert any(z.get("id")=="OMISSIONS-13GB-P75-CROSSPAGE-D21-D25-20261025" for z in ledger["checkpoint_log"])
 if source_image:
  from PIL import Image
  data=Path(source_image).read_bytes()
  assert hashlib.sha256(data).hexdigest()==src["png_sha256"]
  im=Image.open(io.BytesIO(data)).convert("RGB")
  assert list(im.size)==src["native_wh"] and hashlib.sha256(im.tobytes()).hexdigest()==src["rgb_sha256"]
  for row in EXPECTED:
   for prefix in ("heading_",""):
    crop=im.crop(tuple(row[prefix+"roi_xyxy"]))
    assert hashlib.sha256(crop.tobytes()).hexdigest()==row[prefix+"roi_rgb_sha256"]
    tmp=io.BytesIO();crop.save(tmp,format="PNG")
    assert hashlib.sha256(tmp.getvalue()).hexdigest()==row[prefix+"roi_png_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-image");args=ap.parse_args()
 assert check(read(E),read(GA),read(FU),read(L),read(S),args.source_image)
 print("13GB_PASS_DIRECT_P75_D21_D25_CROSSPAGE_D26_D30_NULL")

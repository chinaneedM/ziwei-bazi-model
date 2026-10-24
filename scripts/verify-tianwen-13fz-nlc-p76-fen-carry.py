#!/usr/bin/env python3
"""13FZ NLC original p76 variable <four/five>-fen prefix, carry, D30 fail-closed."""
import argparse, hashlib, io, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13FZ-NLC-P76-D32-D36-FEN-CARRY-SOURCE-COLLATION-R1.json"
FY=ROOT/"docs/research/TIANWEN-13FY-NLC-P76-D29-D31-FOURFEN-SOURCE-NATIVE-COLLATION-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
P=[(32,"四","九五四六",49546,[438,419,461,611],"a9aa795aef5ab2a09c57260116af0361fd53808488929af42521859c95f91095","6f19e4a00ffadb5ffb21c8a00a1198b5681f1c8e1a631df034d87c5f704f0f64"),
(33,"四","九七〇八",49708,[354,419,377,611],"65d8e47f5fed0ef9aa6121c42aa3fc8fe68f6a8540a33f3caa64e4023aa4792c","0a7b987313f0b49fa3471c667c5fa41758408dbcc2048dc532da9d0d1c2949ce"),
(34,"四","九八七〇",49870,[261,419,284,611],"717ad4dcd1f1e0eead1d0e7d2255a0e223f68206fc87598a6641425e5c176ca4","50f041807fe3172563514ccd1dae1a66efbeb06dd58d6178634ee9933e479922"),
(35,"五","〇〇三二",50032,[174,419,197,611],"c2da7cfdb71f7d79fbb0e046d554696d78142cb3059d60230a067f4e59092ec4","5f39ccb0b923e35556dc120a7a4b8f0d2e26561995803fd3d3833148529fafdb"),
(36,"五","〇一九四",50194,[89,419,112,611],"7ba3ca021b586f62619d53451ea705f12b03cd89d2590a785713a29a51c93c24","a5e082d517427c8531db55cef92660dc3ee4ed68a312e169d42ffcc0850b44fb")]
D={c:i for i,c in enumerate("〇一二三四五六七八九")}
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def hash256(data):return hashlib.sha256(data).hexdigest()
def check(e,fy,l,s,source_image=None):
 assert e["schema"]=="TIANWEN-13FZ-NLC-P76-D32-D36-FEN-CARRY-SOURCE-COLLATION-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 src=e["source"]
 assert src["artifact_id"]==12494518841 and src["archive"]=="ncl13dy-original-p73-p80.zip"
 assert src["pdf_page_one_based"]==76 and src["png"]=="original-p076.png"
 assert src["png_sha256"]==fy["source"]["source_png_sha256"]
 assert src["rgb_sha256"]==fy["source"]["source_native_rgb_sha256"]
 assert src["native_wh"]==fy["source"]["native_wh"]==[1305,875]
 assert src["physical_copy_identity"] is None and src["impression_date"] is None
 assert src["no_new_independent_ancient_copy"] is True
 rows=e["direct_original_rows"]
 assert len(rows)==len(P)==5
 for row,(day,pre,rem,n,box,rgb,png) in zip(rows,P):
  assert (row["day"],row["prefix"],row["remainder"],row["numeric_10000_grid"],row["roi_xyxy"],row["roi_rgb_sha256"],row["roi_png_sha256"])==(day,pre,rem,n,box,rgb,png)
  assert int(D[pre])*10000+sum(int(D[x])*10**(3-i) for i,x in enumerate(rem))==n
 assert all(rows[i]["roi_xyxy"][0]>rows[i+1]["roi_xyxy"][2] for i in range(4))
 assert fy["direct_original_fields"][1]["day"]==31 and fy["direct_original_fields"][1]["digits"]=="九三八四"
 a=e["replay"]
 assert a["prior_day31_grid"]==49384 and a["prior_day31_from_13fy"]=="四分九三八四"
 assert a["day31_to_36_grids"]==[49384]+[r["numeric_10000_grid"] for r in rows]
 assert [y-x for x,y in zip(a["day31_to_36_grids"],a["day31_to_36_grids"][1:])]==a["adjacent_differences"]==[162]*5
 assert a["carry_boundary"]["from_original"]=="四分九八七〇" and a["carry_boundary"]["to_original"]=="五分〇〇三二"
 assert a["carry_boundary"]["difference"]==162
 assert e["unresolved"]["nlc_day30_exact_original"] is None and e["unresolved"]["day30_numeric_inference_prohibited"] is True
 assert e["unresolved"]["nlc_day9_original"] is None and e["unresolved"]["g893_original_six_controls"]=="OPEN"
 assert e["unresolved"]["source_copy_independence"] is e["unresolved"]["historic_unit_bridge"] is e["unresolved"]["historiographical_winner"] is None
 assert e["unresolved"]["legacy_13ei"]=="RETRACTED"
 assert e["forward_only"]["prior_13fy_original_unchanged"] and e["forward_only"]["prior_13fx_erratum_unchanged"]
 assert e["counts"]["product"]=="CLOSED" and e["counts"]["risk_issues_open_or_blocked"]==11
 for k in ("algorithm_reopens","candidate_collapses","new_ancient_witnesses","new_source_registry_entries","new_graph_nodes","new_graph_edges"):assert e["counts"][k]==0
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13FZ ") for x in s["historical_audit"]["current_focus"]) # Preserve 13FZ checkpoint without freezing global head
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith("13FZ CURRENT ACTION:")
 assert str(E.relative_to(ROOT)) in issue["source_refs"] and str(E.relative_to(ROOT)).replace(".json",".md") in issue["source_refs"]
 assert any(h.get("revision_id")=="TW-OPEN-0005-13FZ-NLC-D32-D36-FEN-CARRY-20261024" for h in issue["history"])
 if source_image is not None:
  from PIL import Image
  b=Path(source_image).read_bytes()
  assert hash256(b)==src["png_sha256"]
  with Image.open(io.BytesIO(b)) as source:
   image=source.convert("RGB")
   assert list(image.size)==src["native_wh"] and hash256(image.tobytes())==src["rgb_sha256"]
   for row in rows:
    crop=image.crop(tuple(row["roi_xyxy"]))
    assert hash256(crop.tobytes())==row["roi_rgb_sha256"]
    out=io.BytesIO();crop.save(out,format="PNG")
    assert hash256(out.getvalue())==row["roi_png_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-image");args=ap.parse_args()
 assert check(read(E),read(FY),read(L),read(S),args.source_image)
 print("13FZ_PASS_NLC_SOURCE_ORIGINAL_FEN_PREFIX_CARRY_D30_NULL")

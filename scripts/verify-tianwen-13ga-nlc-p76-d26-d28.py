#!/usr/bin/env python3
"""13GA native NLC D26-D28 heading and numeral field checks; never fill D30."""
import argparse, hashlib, io, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13GA-NLC-P76-D26-D28-ORIGINAL-FEN-LANES-R1.json"
FY=ROOT/"docs/research/TIANWEN-13FY-NLC-P76-D29-D31-FOURFEN-SOURCE-NATIVE-COLLATION-R1.json"
FZ=ROOT/"docs/research/TIANWEN-13FZ-NLC-P76-D32-D36-FEN-CARRY-SOURCE-COLLATION-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
ROWS=[
 {
  "day": 26,
  "source_heading": "二十六日",
  "prefix": "四",
  "remainder": "八五七四",
  "integer_grid": 48574,
  "heading_roi_xyxy": [
   890,
   166,
   956,
   292
  ],
  "heading_rgb_sha256": "2c906885de8115d6405d2a8126b97eb99cdcc7c7ba8ea6a113503ecdb107a1f2",
  "heading_png_sha256": "6f5cbec854a0ba68b352f3966f5fdb5b0bc76a4594e1ac5f596936ea2a96aea7",
  "roi_xyxy": [
   921,
   419,
   944,
   611
  ],
  "roi_rgb_sha256": "f6a8bc5fb8766ca12213c06bf5a37e457c24c711f58cf07319de27a325daf50e",
  "roi_png_sha256": "a426d6ef56594206e515c68dee8c053c162c84b0a33fbfc28db2fc76c3eb8dff"
 },
 {
  "day": 27,
  "source_heading": "二十七日",
  "prefix": "四",
  "remainder": "八七三六",
  "integer_grid": 48736,
  "heading_roi_xyxy": [
   804,
   166,
   870,
   292
  ],
  "heading_rgb_sha256": "8cfd34bb8923c9fe01ad86fde91f8b7491ed48217eb9a148e903b8f79f625654",
  "heading_png_sha256": "f9a42a0ec5d15f36bf4c7cba76dd7078ba6f80f9b12a532c54ed7209f6e16cbd",
  "roi_xyxy": [
   835,
   419,
   858,
   611
  ],
  "roi_rgb_sha256": "6c097f66b47658629bcf8d5a50a69b9d71ad1535de173c2e257044c31faa5fd4",
  "roi_png_sha256": "0d47762eeea362933e829e0acc24f89d3395ad45a90eef83f6ebd353e8f5540a"
 },
 {
  "day": 28,
  "source_heading": "二十八日",
  "prefix": "四",
  "remainder": "八八九八",
  "integer_grid": 48898,
  "heading_roi_xyxy": [
   717,
   166,
   783,
   292
  ],
  "heading_rgb_sha256": "86b775247a2b3e4272701564138defbe837272174090317cdc7d8477caf73458",
  "heading_png_sha256": "f31e13b05e8dceec8b20255c5549c08b4350e5e6cf1b9d9a4de87884fe402ccf",
  "roi_xyxy": [
   748,
   419,
   771,
   611
  ],
  "roi_rgb_sha256": "c1e49a040bcd7e2e2797053b7fe937e7c388e97c64f7438afffb0cd65eaeb15a",
  "roi_png_sha256": "27ea8e41aa6ada13329bcb17ddc78674fe493ae570ef9ed16354de8a2f9ed991"
 }
] 
DIGITS={v:i for i,v in enumerate("〇一二三四五六七八九")}
def read(p): return json.loads(p.read_text(encoding="utf-8"))
def check(e,fy,fz,ledger,state,source_image=None):
 assert e["schema"]=="TIANWEN-13GA-NLC-P76-D26-D28-ORIGINAL-FEN-LANES-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 a=e["source"]
 assert a["artifact_id"]==12494518841 and a["original_png"]=="original-p076.png"
 assert a["original_png_sha256"]==fy["source"]["source_png_sha256"]==fz["source"]["png_sha256"]
 assert a["original_rgb_sha256"]==fy["source"]["source_native_rgb_sha256"]==fz["source"]["rgb_sha256"]
 assert a["wh"]==[1305,875] and a["one_source_surrogate_not_independent_ancient_votes"]
 assert a["physical_copy_identity"] is None and a["edition_impression_date"] is None
 assert e["direct_original_rows"]==ROWS
 for r in ROWS:
  assert r["prefix"]=="四" and r["integer_grid"]==40000+sum(DIGITS[c]*10**(3-i) for i,c in enumerate(r["remainder"]))
 assert all(ROWS[i]["roi_xyxy"][0]>ROWS[i+1]["roi_xyxy"][2] for i in range(2))
 assert fy["direct_original_fields"][0]["day"]==29 and fy["direct_original_fields"][0]["digits"]=="九〇六〇"
 n=[r["integer_grid"] for r in ROWS]+[49060]
 assert e["replay"]["integer_grid"]==n and e["replay"]["differences"]==[y-x for x,y in zip(n,n[1:])]==[162]*3
 assert e["replay"]["NO_DAY30_INFERENCE"] is True
 assert e["day30_boundary"]["day30_complete_source_glyph"] is None and e["day30_boundary"]["day30_source_field_exact_roi"] is None
 assert e["day30_boundary"]["day30_inferred_49222_not_original"] and e["day30_boundary"]["do_not_assert_original_field_absent"]
 assert e["unresolved"]["nlc_day9"] is None and e["unresolved"]["g893_six"]=="OPEN"
 assert e["unresolved"]["historical_numerical_unit_bridge"] is None and e["unresolved"]["physical_copy_and_impression_independence"] is None
 assert e["unresolved"]["historical_winner"] is None and e["unresolved"]["legacy_13ei"]=="RETRACTED"
 assert e["counts"]["product"]=="CLOSED" and e["counts"]["issues_open_or_blocked"]==11
 for key in ("new_source_records","new_ancient_witnesses","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens","candidate_collapses"): assert e["counts"][key]==0
 assert ledger["binding"]["reviewed_state_version"]==state["schema_version"]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13GA ") for x in state["historical_audit"]["current_focus"])
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["next_action"].startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:") # rolling current contract; historic 13FZ retained
 assert all(any(h.get("revision_id", "").startswith("TW-OPEN-0005-" + t + "-") and "next_action" in h.get("changed_fields", []) for h in issue["history"]) for t in ['13GA','13FZ'])
 assert str(E.relative_to(ROOT)) in issue["source_refs"] and str(E.relative_to(ROOT)).replace(".json",".md") in issue["source_refs"]
 assert any(h.get("revision_id")=="TW-OPEN-0005-13GA-D26-D28-NLC-20261024" for h in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13GA-NLC-P76-D26-D28-20261024" for x in ledger["checkpoint_log"])
 if source_image:
  from PIL import Image
  b=Path(source_image).read_bytes()
  assert hashlib.sha256(b).hexdigest()==a["original_png_sha256"]
  im=Image.open(io.BytesIO(b)).convert("RGB")
  assert list(im.size)==a["wh"] and hashlib.sha256(im.tobytes()).hexdigest()==a["original_rgb_sha256"]
  for r in ROWS:
   for label in ("heading_",""):
    rect=r[label+"roi_xyxy"];c=im.crop(tuple(rect))
    assert hashlib.sha256(c.tobytes()).hexdigest()==r[label+"roi_rgb_sha256"]
    out=io.BytesIO();c.save(out,format="PNG")
    assert hashlib.sha256(out.getvalue()).hexdigest()==r[label+"roi_png_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-image");args=ap.parse_args()
 assert check(read(E),read(FY),read(FZ),read(L),read(S),args.source_image)
 print("13GA_PASS_NLC_DIRECT_D26_D28_AND_D30_NULL")

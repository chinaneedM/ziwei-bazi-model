#!/usr/bin/env python3
"""13FY original-page NLC p76 positive neighbor Fourfen fields, D30 fail-closed."""
import argparse
import hashlib
import io
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13FY-NLC-P76-D29-D31-FOURFEN-SOURCE-NATIVE-COLLATION-R1.json"
FV=ROOT/"docs/research/TIANWEN-13FV-NLC-D30-GUTTER-DAY-HEADER-GEOMETRY-R1.json"
FX=ROOT/"docs/research/TIANWEN-13FX-GK3467-P17-THREE-DAY-FOURFEN-SOURCE-FIELD-ERRATUM-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
DIGITS=dict(zip("〇一二三四五六七八九","0123456789"))
EXPECTED=[
 (29,"二十九日","九〇六〇",9060,[662,419,685,611],"67eea44e3a6bb7a6074abb3b33586d5992e7f0575e676fdffc09bd9b1bbb9d87","11279a96a8c95c8c2bd34b50d0b39e42165fa6f61f5ac6091d8488f4fc2ec54e"),
 (31,"三十一日","九三八四",9384,[512,419,535,611],"d339437d3111d6f8fb5a32e3717bde5bec476c7e39a38cbb8c664432e61e91a6","7689fd3ba77686b92ca325e6e35ee7bbc91117aff1a314c80379e07769a1a52e")
]
def read(path):return json.loads(path.read_text(encoding="utf-8"))
def sha(b):return hashlib.sha256(b).hexdigest()
def check(e,fv,fx,ledger,state,source_image=None):
 assert e["schema"]=="TIANWEN-13FY-NLC-P76-D29-D31-FOURFEN-SOURCE-NATIVE-COLLATION-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 src=e["source"]
 assert src["original_page_pdf_one_based"]==76 and src["source_png"]=="original-p076.png"
 assert src["archive_file"]=="ncl13dy-original-p73-p80.zip" and src["artifact_id"]==12494518841
 assert src["source_pdf_sha256"]==fv["source"]["source_pdf_sha256"]
 assert src["source_png_sha256"]==fv["source"]["png_sha256"]=="ce4eb8b044868fe48bb41fe5453b10fa7bbd949d8fdf2c8e31037f8b89f32fad"
 assert src["source_native_rgb_sha256"]==fv["source"]["native_rgb_sha256"]
 assert src["native_wh"]==fv["source"]["native_wh"]==[1305,875]
 assert src["reused_archived_original"] and src["physical_copy_identity"] is None
 assert len(e["direct_original_fields"])==2
 for row,expected in zip(e["direct_original_fields"],EXPECTED):
  d,heading,digits,n,box,rgb,png=expected
  assert (row["day"],row["source_heading"],row["source_field"],row["digits"],row["numeric"],row["roi_xyxy"],row["roi_rgb_sha256"],row["roi_png_sha256"])==(d,heading,"四分",digits,n,box,rgb,png)
  assert int("".join(DIGITS[c] for c in digits))==n
 assert e["direct_original_fields"][0]["roi_xyxy"][0]>e["direct_original_fields"][1]["roi_xyxy"][2]
 d30=e["day30"]
 assert d30["day_header"]==fv["geometry"]["day30_day_header_original"]=="三十日"
 assert d30["printed_fourfen_field_exact_roi"] is d30["original_complete_fourfen_digits"] is None
 assert d30["derived_linear_midpoint_9222_not_original_glyph"] and d30["do_not_assume_missing_field"]
 assert d30["nearby_numeric_strips_not_a_proven_fourfen_field"]
 assert fv["geometry"]["day30_complete_fourfen_original_digits"] is None
 assert (9060+9384)//2==9222
 assert e["cross_original"]["day30_gk_source_only"]=="九二二二"
 assert e["cross_original"]["day30_nlc_original"] is None
 assert e["cross_original"]["source_copy_independence"] is None
 assert e["cross_original"]["original_numeric_unit_bridge"] is None
 assert [r["digits"] for r in fx["original_fourfen_rows"] if r["day"] in (29,31)]==[x["digits"] for x in e["direct_original_fields"]]
 inv=e["invariants"]
 assert inv["NLC_day9_fourfen"] is inv["winner"] is None
 assert inv["G893_original_six_controls"]=="OPEN" and inv["retracted_13EI"]=="RETRACTED"
 assert inv["product"]=="CLOSED"
 for k in ("algorithm_reopens","chart_candidate_collapses","new_registry_records","new_physical_witnesses","new_genealogy_nodes","new_genealogy_edges","closed_risk_issues"): assert inv[k]==0
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 assert e["counts"]["matrix_total"]==e["counts"]["matrix_audited"]==222
 assert e["counts"]["external_sources"]==761 and e["counts"]["genealogy_nodes"]==252 and e["counts"]["genealogy_edges"]==238
 assert e["counts"]["issues_open_or_blocked"]==11
 assert ledger["binding"]["reviewed_state_version"]==state["schema_version"]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert any(x.startswith("13FY ") for x in state["historical_audit"]["current_focus"])
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN"
 assert str(E.relative_to(ROOT)) in issue["source_refs"]
 assert str(E.relative_to(ROOT)).replace(".json",".md") in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13FY-NLC-P76-D29-D31-POSITIVE-NEIGHBOR-20261024" for x in issue["history"])
 if source_image:
  from PIL import Image
  raw=Path(source_image).read_bytes()
  assert sha(raw)==src["source_png_sha256"]
  with Image.open(io.BytesIO(raw)) as image:
   im=image.convert("RGB")
   assert list(im.size)==src["native_wh"] and sha(im.tobytes())==src["source_native_rgb_sha256"]
   for row in e["direct_original_fields"]:
    roi=im.crop(tuple(row["roi_xyxy"]))
    assert sha(roi.tobytes())==row["roi_rgb_sha256"]
    dest=io.BytesIO();roi.save(dest,format="PNG")
    assert sha(dest.getvalue())==row["roi_png_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("--source-image",default=None)
 args=ap.parse_args()
 assert check(read(E),read(FV),read(FX),read(L),read(S),args.source_image)
 print("13FY_PASS_NLC_ORIGINAL_D29_D31_FOURFEN_POSITIVE_D30_NULL_NO_HISTORICAL_WINNER")

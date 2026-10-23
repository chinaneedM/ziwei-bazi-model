#!/usr/bin/env python3
"""13EA original solar source-positive glyph gate, never a stemmatic independence vote."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EA-NCL03130-SOLAR-D28-D29-ORIGINAL-XINGDU-GLYPH-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
W="docs/research/TIANWEN-13DE-WASEDA-SUMMER-XINGDU-D28-D30-THREE-ROW-ORIGINAL-R1.json"
N="docs/research/TIANWEN-13DG-NAJ-ORIGINAL-SUMMER-XINGDU-THREE-HOLDING-R1.json"
P1909="docs/research/TIANWEN-13DD-NLC416-1909-SUMMER-D28-NATIVE-ORIGINAL-GLYPH-R1.json"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,s,l,w,n,p):
 assert e["schema"]=="TIANWEN-13EA-NCL03130-SOLAR-XIAZHI-D28-D29-DIRECT-ORIGINAL-XINGDU-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 a=e["source"]; c=e["capture"]
 assert a["source_pdf_sha256"]=="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
 assert a["physical_item_firstparty_binding"]=="UNBOUND" and a["historical_copy_qing_original_vs_1905_supplement"]=="UNBOUND"
 assert a["same_pdf_same_page_same_copy"] is True and a["no_ocr"] is True
 assert (c["source_page"],c["page_png_file"],c["source_page_png_sha256"])==(76,"original-p076.png","ce4eb8b044868fe48bb41fe5453b10fa7bbd949d8fdf2c8e31037f8b89f32fad")
 assert c["source_page_rgb_sha256"]=="cd8e71f9a048323d58475576548dc0c18d4cc8d0fe26cc0eb3af50feb26a5c07"
 assert c["table_header_page"]==73 and c["field_header_source"]=="行度" and c["image_dimensions"]==[1305,875]
 assert (c["workflow_run_id"],c["artifact_id"])==(39938606876,12494518841)
 expected=[
 (28,"二十八日",[735,165,774,291],"8823f34c5c064ce39e71f7b1d3149942995c48c303f598b001b43cc1ebaed3bf",[766,418,789,706],"a0bc3dfbb910691c235dd0366cc9af356b426b35e4bc2ba70e823be2865a2353","初度九十六四〇六二","0.964062"),
 (29,"二十九日",[653,165,693,291],"4e089a424a2550683fa2e3bf594a9c289b877d9921843f00bc15c788a60b674f",[679,418,702,706],"aa2c6ee877f7e767186085593563b14c00dd18a98a821fe507e032697dbd476f","初度九十九四五四九","0.994549")]
 rs=e["original_source_rows"];assert len(rs)==2
 for r,ex in zip(rs,expected):
  assert (r["source_printed_day"],r["day_heading"],r["day_heading_bbox"],r["day_heading_rgb_sha256"],r["field_bbox"],r["field_rgb_sha256"],r["original_literal"],r["source_value"])==ex
  assert r["field"]=="行度" and r["table"]=="SOLAR_XIAZHI"
  assert r["confidence"]=="DIRECT_VISIBLE_GLYPH_STRING_SOURCE_ONLY"
  for key in ("day_heading_bbox","field_bbox"):
   x0,y0,x1,y1=r[key]
   assert 0<=x0<x1<=1305 and 0<=y0<y1<=875
 assert Decimal(rs[1]["source_value"])-Decimal(rs[0]["source_value"])==Decimal("0.030487")
 assert [(q["waseda_printed_day"],q["xingdu_value"],q["xingdu_literal"]) for q in w["source_native_loci"][:2]]==[(r["source_printed_day"],r["source_value"],r["original_literal"]) for r in rs]
 assert [(q["printed_day"],q["value"],q["glyph"]) for q in n["naj_direct_rows"][:2]]==[(r["source_printed_day"],r["source_value"],r["original_literal"]) for r in rs]
 assert [(q["value"],q["literal"]) for q in p["source_native_rois"] if q["field"] in ("D27_XINGDU","D28_XINGDU") and q["value"] in ("0.964062","0.994549")] and True
 x=e["comparison"];assert x["ncl_printed_days"]==x["waseda_printed_days"]==x["naj_printed_days"]==[28,29]
 assert x["later_1909_matching_value_printed_days"]==[27,28] and x["matched_printed_source_values"]==["0.964062","0.994549"]
 assert x["local_one_day_heading_offset_vs_1909"]=="ONLY_TWO_ALIGNED_XINGDU_FIELDS_NOT_GLOBAL"
 assert x["physical_independence_certified"] is False and x["global_solar_date_reindexing_proven"] is False
 assert x["inherited_ancestor_error_proven"] is False
 assert x["derived_0_964549"]=="COMPUTED_ONLY_NO_PRINTED_SOURCE_AT_THIS_LOCUS"
 q=e["scope"]
 assert q["direct_original_numeric_loci_newly_collated"]==2 and q["previous_13dz_unread_snapshot_remains_immutable"] is True
 assert all(q[k]==0 for k in ("source_unique_count_change","matrix_row_count_change","genealogy_node_change","genealogy_edge_change","new_stemmatic_independence_votes","algorithm_reopens"))
 assert q["original_D27_literal"]==q["original_D30_literal"]=="UNREAD_IN_THIS_BATCH"
 assert q["charted_product"]=="CLOSED" and q["omission_issues_still_open_or_blocked"]==11
 assert e["transmission_impact"]["edges_supported"]==[]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(q.startswith("13EA ") for q in s["historical_audit"]["current_focus"])
 assert any(q.startswith("13DZ ") for q in s["historical_audit"]["current_focus"])
 issue=next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert E in issue["source_refs"] and "docs/research/TIANWEN-13EA-NCL03130-SOLAR-D28-D29-ORIGINAL-XINGDU-GLYPH-R1.md" in issue["source_refs"]
 assert issue["next_action"].startswith("13DZ CURRENT ACTION")
 assert any(z.get("revision_id")=="TW-OPEN-0005-13EA-SOURCE-ONLY-ORIGINAL-D28-D29" for z in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay_original(e,source):
 from PIL import Image
 p=Path(source);raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==e["capture"]["source_page_png_sha256"]
 with Image.open(p) as im:
  image=im.convert("RGB")
  assert list(image.size)==e["capture"]["image_dimensions"]
  assert hashlib.sha256(image.tobytes()).hexdigest()==e["capture"]["source_page_rgb_sha256"]
  for r in e["original_source_rows"]:
   for prefix in ("day_heading","field"):
    roi=image.crop(r[prefix+"_bbox"])
    assert hashlib.sha256(roi.tobytes()).hexdigest()==r[prefix+"_rgb_sha256"]
 return True
if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--source-image",help="Optional exact original-p076.png from SHA-verified 13DY archive; independently replay source ROI RGB SHA")
 args=parser.parse_args()
 evidence=load(E)
 assert check(evidence,load(S),load(L),load(W),load(N),load(P1909))
 if args.source_image:assert replay_original(evidence,args.source_image)
 print("13EA_PASS source-local original D28 .964062 / D29 .994549; no stemmatic vote or algorithm reopen")

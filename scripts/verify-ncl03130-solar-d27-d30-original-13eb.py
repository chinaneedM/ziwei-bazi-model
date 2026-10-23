#!/usr/bin/env python3
"""13EB source-native D27 positive and D30 numeric non-adjudication."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EB-NCL03130-SOLAR-D27-D30-ORIGINAL-ROI-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
P="docs/research/TIANWEN-13EA-NCL03130-SOLAR-D28-D29-ORIGINAL-XINGDU-GLYPH-R1.json"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
def verified_next_action(issue, state):
 active=issue.get("next_action","")
 prefix=active.split(" ",1)[0]
 revisions=[h for h in issue.get("history",[]) if h.get("event")=="ISSUE_REVISION" and "next_action" in h.get("changed_fields",[])]
 if not revisions or not active.startswith(prefix+" CURRENT ACTION"):return False
 last=revisions[-1]
 return (last.get("revision_id","").startswith("TW-OPEN-0005-"+prefix+"-") and bool(last.get("evidence_refs")) and any(x.startswith(prefix+" ") for x in state["historical_audit"]["current_focus"]))

def check(e,s,l,prior):
 assert e["schema"]=="TIANWEN-13EB-NCL03130-SOLAR-D27-D30-ORIGINAL-ROI-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 a=e["source"];c=e["capture"]
 assert a["pdf_sha256"]=="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
 assert a["physical_copy_id"]==a["qing_vs_1905_copy_layer"]=="UNBOUND" and a["no_ocr"] is True
 assert (c["run"],c["artifact_id"],c["page"])==(39938606876,12494518841,76)
 assert c["png_sha256"]=="ce4eb8b044868fe48bb41fe5453b10fa7bbd949d8fdf2c8e31037f8b89f32fad"
 assert c["rgb_sha256"]=="cd8e71f9a048323d58475576548dc0c18d4cc8d0fe26cc0eb3af50feb26a5c07"
 assert c["size"]==[1305,875] and c["field"]=="行度" and c["table_heading_page"]==73
 assert len(e["rows"])==2
 a,b=e["rows"]
 assert (a["day"],a["heading"],a["heading_bbox"],a["heading_rgb_sha256"])==(27,"二十七日",[815,165,850,291],"7511e4e2aae4f88e76231f7cc39de0c1386218daf743c3049f104c79ad54af00")
 assert (a["field_bbox"],a["field_rgb_sha256"],a["literal"],a["value"])==([851,418,876,706],"494f54883763a547ca8cdfde95c7fd235187c9407f2586705026ebb39308cfe6","初度九十六三五七六","0.963576")
 assert a["grade"]=="DIRECT_ORIGINAL_SOURCE_POSITIVE"
 assert (b["day"],b["heading"],b["heading_bbox"],b["heading_rgb_sha256"])==(30,"三十日",[561,165,602,291],"2e18e2334cde0d4a94531053e04b3971ac585c2c2d322bca2e0c917c3d31bbe7")
 assert (b["field_bbox"],b["field_rgb_sha256"])==([590,418,615,706],"fe0d6c893f8487fd066683093e9538abe9da5669b38904cab22b1888911b9b5d")
 assert b["visible_prefix"]=="初度九十六二〇三" and b["literal"] is None and b["value"] is None
 assert b["grade"]=="BOUND_SOURCE_GLYPH_PREFIX_EXACT_DECIMAL_UNRESOLVED"
 for row in (a,b):
  for k in ("heading_bbox","field_bbox"):
   x0,y0,x1,y1=row[k];assert 0<=x0<x1<=1305 and 0<=y0<y1<=875
 assert prior["original_source_rows"][0]["source_value"]==e["cross"]["d28_prior"]=="0.964062"
 assert prior["original_source_rows"][1]["source_value"]==e["cross"]["d29_prior"]=="0.994549"
 assert Decimal(e["cross"]["d28_prior"])-Decimal(a["value"])==Decimal("0.000486")
 assert e["cross"]["ncl_d30"]=="UNREAD_EXACT" and e["cross"]["d30_variant_established"] is False
 assert e["cross"]["global_day_offset_established"] is False and e["cross"]["stemmatic_independence_established"] is False
 q=e["scope"]
 assert (q["source_original_complete_loci_added"],q["source_original_incomplete_loci_bounded"])==(1,1)
 assert all(q[k]==0 for k in ("source_registry_additions","matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","independent_votes_added","algorithm_reopens","research_issues_closed"))
 assert q["open_issues"]==11 and q["product"]=="CLOSED"
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13EB ") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0" and verified_next_action(issue,s)
 assert E in issue["source_refs"] and "docs/research/TIANWEN-13EB-NCL03130-SOLAR-D27-D30-ORIGINAL-ROI-R1.md" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13EB-SOURCE-ROI" for x in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,p):
 from PIL import Image
 assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==e["capture"]["png_sha256"]
 with Image.open(p) as x:im=x.convert("RGB")
 assert list(im.size)==e["capture"]["size"] and hashlib.sha256(im.tobytes()).hexdigest()==e["capture"]["rgb_sha256"]
 for row in e["rows"]:
  for key in ("heading","field"):
   assert hashlib.sha256(im.crop(row[key+"_bbox"]).tobytes()).hexdigest()==row[key+"_rgb_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-image");args=ap.parse_args()
 e=load(E);assert check(e,load(S),load(L),load(P))
 if args.source_image:assert replay(e,args.source_image)
 print("13EB_PASS D27_SOURCE_POSITIVE D30_BOUND_UNRESOLVED")

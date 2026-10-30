#!/usr/bin/env python3
"""13ED exact SHA-pinned native D30 literal and bounded lower source tail."""
import argparse,hashlib,json
from pathlib import Path
# Archived action terms come from preserved revisions, never from stale live next_action.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
B="docs/research/TIANWEN-13EB-NCL03130-SOLAR-D27-D30-ORIGINAL-ROI-R1.json"
A="docs/research/TIANWEN-13EA-NCL03130-SOLAR-D28-D29-ORIGINAL-XINGDU-GLYPH-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,s,l,b,a):
 assert e["schema"]=="TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 v=e["source"]
 assert v["pdf_sha256"]==b["source"]["pdf_sha256"] and v["png_sha256"]==b["capture"]["png_sha256"]
 assert v["rgb_sha256"]==b["capture"]["rgb_sha256"] and v["size"]==[1305,875]
 assert v["archive"]["workflow_run"]==b["capture"]["run"] and v["archive"]["artifact_id"]==b["capture"]["artifact_id"]
 assert v["ocr_used"] is False and v["physical_copy_id"]==v["qing_vs_1905_hand"]=="UNBOUND"
 roi=e["native_rois"];assert len(roi)==8
 observed=[(x["name"],x["bbox"],x["rgb_sha256"]) for x in roi]
 expected=[
 ("d30_heading",[561,165,602,291],"2e18e2334cde0d4a94531053e04b3971ac585c2c2d322bca2e0c917c3d31bbe7"),
 ("d30_prior_bounded_field",[590,418,615,706],"fe0d6c893f8487fd066683093e9538abe9da5669b38904cab22b1888911b9b5d"),
 ("d30_extended_full_strip",[590,418,615,830],"bc91212e7b7a6a98f67913788e0051c3eabfd5af46982aa26f90a3339cf0efd4"),
 ("d30_lower_tail_only",[590,706,615,830],"e4be7390aed463b167271a74aecd3d98046a2b9b5e0b204360411805d5337c6a"),
 ("d30_panel_with_adjacent_columns",[553,418,649,830],"2908bd99867f113858322eb8cef07403b9ae7b6e7550b2a0c9002fdd80b32a87"),
 ("d27_extended_original_control",[851,418,876,830],"2582c5b9703865493b6a5288bd9f1dea44f51468e25d164d97d5fc7144860583"),
 ("d28_extended_original_control",[766,418,789,830],"6e371e442f55edd5b74b687bbbc59ddfbf0c07cddeaf51ead114f1fdfdc51cf3"),
 ("d29_extended_original_control",[679,418,702,830],"cfffac08a8bc4b32ba0a28822b0c6914bddee237ae1c9e1073cda703b817a00a")]
 assert observed==expected
 assert roi[1]["visible_literal"]==b["rows"][1]["visible_prefix"]==roi[2]["visible_literal"]=="初度九十六二〇三"
 assert roi[2]["continuation_observed_after_previous_roi"] is False
 assert roi[3]["human_visual_read"]=="NO_ADDITIONAL_D30_CHARACTER_OBSERVED_IN_NARROW_COLUMN"
 assert roi[4]["human_visual_read"]=="ADJACENT_SEPARATE_COLUMNS_PRESENT_NOT_CONCATENATED"
 assert [x["source_value"] for x in roi[5:]]==["0.963576","0.964062","0.994549"]
 assert roi[5]["source_value"]==b["rows"][0]["value"]
 assert [x["source_value"] for x in roi[6:]]==[x["source_value"] for x in a["original_source_rows"]]
 f=e["finding"];assert f["d30_visible_glyph_group"]=="初度九十六二〇三" and f["full_precision_historical_numeric_assignment"] is None
 assert f["d30_complete_lexical_surface_visible_in_narrow_strip"] and f["other_field_tail_cannot_be_concatenated"]
 assert f["missing_or_elided_digits_caused_by_copyist_proven"] is False and "ONLY_SAME_IMAGE" in f["negative_proof_scope"]
 c=e["comparison"];assert c["original_d30_numeric_value"] is None and c["global_day_offset_law_established"] is False and c["stemmatic_independence_established"] is False and c["other_holding_is_not_same_source_numeric_vote"]
 impact=e["impact"];assert (impact["new_source_original_extended_strip_review"],impact["open_issues"],impact["chart"])==(1,11,"CLOSED")
 assert all(impact[k]==0 for k in ("new_physical_witnesses","new_source_registry_entries","matrix_rows_changed","genealogy_nodes_added","genealogy_edges_added","independent_votes_added","algorithm_reopens","research_issues_closed"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(z.startswith("13ED NCL03130 D30 EXTENDED") for z in s["historical_audit"]["current_focus"])
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 active_prefix=historical_action_view(issue).split(" ",1)[0]
 assert historical_action_view(issue).startswith(active_prefix+" CURRENT ACTION")
 action_revisions=[q for q in issue["history"] if q.get("event")=="ISSUE_REVISION" and "next_action" in q.get("changed_fields",[])]
 assert action_revisions and action_revisions[-1].get("revision_id","").startswith("TW-OPEN-0005-"+active_prefix+"-")
 assert action_revisions[-1].get("evidence_refs") and any(z.startswith(active_prefix+" ") for z in s["historical_audit"]["current_focus"])
 assert "D30" in historical_action_view(issue) and e["next"].startswith("Review adjacent D26-D36")
 assert set([E,E.replace(".json",".md"),B]).issubset(set(issue["source_refs"]))
 revision=next(q for q in issue["history"] if q.get("revision_id")=="TW-OPEN-0005-13ED-EXTENDED-ORIGINAL-STRIP-20261023")
 assert revision["revision_id"]=="TW-OPEN-0005-13ED-EXTENDED-ORIGINAL-STRIP-20261023"
 assert revision["previous_next_action"].startswith("13EC CURRENT ACTION")
 assert set(revision["changed_fields"])=={"source_refs","next_action"}
 assert set([E,E.replace(".json",".md"),B]).issubset(set(revision["evidence_refs"]))
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["issues"])==11
 return True
def replay(e,p):
 from PIL import Image
 raw=Path(p).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==e["source"]["png_sha256"]
 with Image.open(p) as im:rgb=im.convert("RGB")
 assert list(rgb.size)==e["source"]["size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for q in e["native_rois"]:
  x0,y0,x1,y1=q["bbox"];assert 0<=x0<x1<=rgb.width and 0<=y0<y1<=rgb.height
  assert hashlib.sha256(rgb.crop(q["bbox"]).tobytes()).hexdigest()==q["rgb_sha256"],q["name"]
 return True
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--source-image");args=parser.parse_args()
 data=read(E);assert check(data,read(S),read(L),read(B),read(A))
 if args.source_image:assert replay(data,args.source_image)
 print("13ED_PASS SOURCE_FULL_STRIP_REPLAY D30_SHORT_TEXT_POSITIVE NUMERIC_UNRESOLVED")
